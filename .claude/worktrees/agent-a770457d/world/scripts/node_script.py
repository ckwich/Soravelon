"""
NodeScript — the state machine for zone node failure.

Attached to a ZoneObject. One per zone.
Driven externally by global TickerHandler via receive_tick().
NOT self-ticking — interval=0.
"""

from evennia.scripts.scripts import DefaultScript
from world.node_helpers import get_rooms_in_radius
from world.nodes.node_effects import apply_node_effects, remove_node_effects
import evennia


class NodeScript(DefaultScript):
    """
    Manages node failure state for a zone.
    Driven by the global 30-second TickerHandler.
    """

    def at_script_creation(self):
        self.key = "node_script"
        self.persistent = True
        self.interval = 0  # NOT self-ticking

        self.db.failure = 0.0
        self.db.node_type = None
        self.db.node_radius = 2
        self.db.center_room_id = None
        self.db.state = "dormant"
        self.db.layer1_room_ids = []
        self.db.layer1_active = False
        self.db.session_failure_added = 0.0

        self.tags.add("node_script", category="script_type")

    def receive_tick(self, player_count, scholar_count, stabilizer_count):
        """
        Called by global node_failure_tick() every 30 seconds.
        One DB write per call.
        """
        raw_player_contribution = (
            (player_count * 0.1) + (scholar_count * 0.3)
        )

        remaining_cap = max(0.0, 5.0 - self.db.session_failure_added)
        capped_contribution = min(raw_player_contribution, remaining_cap)
        self.db.session_failure_added += capped_contribution

        stabilization = stabilizer_count * 0.5
        delta = capped_contribution - stabilization

        old_failure = self.db.failure
        self.db.failure = max(0.0, min(100.0, self.db.failure + delta))

        self._update_state(old_failure, self.db.failure)

    def _failure_to_state(self, failure):
        if failure < 30:
            return "dormant"
        if failure < 60:
            return "awakening"
        if failure < 90:
            return "active"
        return "critical"

    def _update_state(self, old_failure, new_failure):
        old_state = self._failure_to_state(old_failure)
        new_state = self._failure_to_state(new_failure)

        if old_state == new_state:
            self.db.state = new_state
            return

        self.db.state = new_state
        self._on_state_transition(old_state, new_state)

    def _on_state_transition(self, old_state, new_state):
        if new_state == "awakening" and old_state == "dormant":
            self._apply_state_tags("node_awakening")

        elif new_state == "active" and old_state not in ("active", "critical"):
            self._activate_layer1()

        elif (old_state in ("active", "critical")
              and new_state in ("dormant", "awakening")):
            self._deactivate_layer1()
            self.db.session_failure_added = 0.0

        # Clean stale tags from L0 rooms when leaving a state
        if old_state == "awakening" and new_state != "awakening":
            self._remove_state_tags("node_awakening")
        if old_state == "critical" and new_state != "critical":
            self._remove_state_tags("node_critical")
        # Also clean on return to dormant (catches all stale tags)
        if new_state == "dormant":
            self._remove_state_tags("node_awakening")
            self._remove_state_tags("node_critical")

        if new_state == "critical" and old_state != "critical":
            self._apply_state_tags("node_critical")

        # OOB: push node_event to all connected players in this zone (CLI-06)
        zone_id = self.obj.db.zone_id if self.obj else None
        if zone_id:
            from world import oob_publisher
            candidates = evennia.search_tag(zone_id, category="zone_id")
            for obj in candidates:
                if (hasattr(obj, "sessions") and obj.sessions.all()
                        and obj.tags.get("player_character", category="character_type")):
                    oob_publisher.push_node_event(obj, zone_id, old_state, new_state)

    def _get_center_room(self):
        if not self.db.center_room_id:
            return None
        results = evennia.search_object("#" + str(self.db.center_room_id))
        return results[0] if results else None

    def _apply_state_tags(self, tag_name):
        center = self._get_center_room()
        if not center:
            return
        affected = get_rooms_in_radius(center, self.db.node_radius)
        for room in affected:
            room.tags.add(tag_name, category="node_state")

    def _remove_state_tags(self, tag_name):
        """Remove a node state tag from all L0 rooms in node radius."""
        center = self._get_center_room()
        if not center:
            return
        affected = get_rooms_in_radius(center, self.db.node_radius)
        for room in affected:
            room.tags.remove(tag_name, category="node_state")

    def _activate_layer1(self):
        self.db.layer1_active = True
        center = self._get_center_room()
        if not center:
            return

        affected_layer0 = get_rooms_in_radius(center, self.db.node_radius)

        for layer0_room in affected_layer0:
            layer1_room_id = layer0_room.db.layer1_room_id
            if not layer1_room_id:
                continue

            layer1_objs = evennia.search_object("#" + str(layer1_room_id))
            if not layer1_objs:
                continue
            layer1_room = layer1_objs[0]

            layer1_room.tags.remove("inactive", category="node_layer")
            layer1_room.tags.add("active", category="node_layer")

            apply_node_effects(layer1_room, self.db.node_type, "active")

            for obj in list(layer0_room.contents):
                if hasattr(obj, 'account') and obj.account:
                    obj.db.layer0_room_id = layer0_room.id
                    obj.move_to(layer1_room, quiet=False)
                    obj.msg(
                        "\nThe air shifts. The world you know "
                        "becomes something else."
                    )

    def _deactivate_layer1(self):
        self.db.layer1_active = False

        for layer1_room_id in self.db.layer1_room_ids:
            layer1_objs = evennia.search_object("#" + str(layer1_room_id))
            if not layer1_objs:
                continue
            layer1_room = layer1_objs[0]

            for obj in list(layer1_room.contents):
                if hasattr(obj, 'account') and obj.account:
                    layer0_id = obj.db.layer0_room_id
                    if layer0_id:
                        layer0_objs = evennia.search_object(
                            "#" + str(layer0_id)
                        )
                        if layer0_objs:
                            obj.move_to(layer0_objs[0], quiet=False)
                            obj.msg(
                                "\nThe world reasserts itself. "
                                "You are where you were."
                            )
                    obj.db.layer0_room_id = None

            remove_node_effects(layer1_room)
            room_tags_to_remove = ["node_awakening", "node_critical"]
            for tag in room_tags_to_remove:
                layer1_room.tags.remove(tag, category="node_state")
            layer1_room.tags.remove("active", category="node_layer")
            layer1_room.tags.add("inactive", category="node_layer")
