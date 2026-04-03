"""
Rooms for Soravelon.

SoravelonRoom is the base room typeclass.
Layer1Room is a pre-pooled room for the node system.
"""

from evennia.objects.objects import DefaultRoom
from .objects import ObjectParent


def _check_mob_encounter_for_arrival(mob, character, room):
    """
    Module-level helper: check if a patrol mob engages a player who just entered.

    Called from at_object_receive (D-02) — player enters a room containing a patrol mob.
    Triggers combat via the mob's PatrolScript if disposition warrants it.
    """
    if not mob or not mob.pk:
        return
    from world.patrol_engine import check_patrol_encounter
    if check_patrol_encounter(mob, room):
        scripts = mob.scripts.get("patrol_script")
        if scripts:
            scripts[0]._initiate_combat(room)


class Room(ObjectParent, DefaultRoom):
    """Default Evennia room — kept for compatibility."""
    pass


class SoravelonRoom(ObjectParent, DefaultRoom):
    """
    Base room for all Soravelon zones.
    Checks node state when generating descriptions.
    Fires trigger events and checks patrol mob encounters.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.zone_id = None
        self.db.layer1_room_id = None
        self.db.layer0_room_id = None
        self.db.is_layer1 = False
        self.db.awakening_desc = None
        self.db.triggers = []          # trigger list for trigger_engine
        self.db.custom_commands = []   # custom command definitions for custom_command() builder method
        self.db.flight_point_id = None  # set by area.flight_point(); truthy = Dragon Courier stop

    def return_appearance(self, looker, **kwargs):
        """
        Extend default room appearance to show custom commands marked
        visible_in_exits=True (D-21). These commands act as exits or
        interactions that builders want discoverable.
        """
        appearance = super().return_appearance(looker, **kwargs)
        # Append visible custom commands to the appearance string
        custom_cmds = list(self.db.custom_commands or [])
        visible = [c for c in custom_cmds if c.get("visible_in_exits")]
        if not visible:
            return appearance
        lines = []
        for cmd_def in visible:
            key = cmd_def.get("key", "")
            desc = cmd_def.get("desc", "")
            if desc:
                lines.append(f"|w{key}|n - {desc}")
            else:
                lines.append(f"|w{key}|n")
        extra = "\nOther exits: " + ", ".join(lines)
        return appearance + extra

    def get_display_desc(self, looker, **kwargs):
        """Return description appropriate to current node state."""
        if (self.tags.get("node_awakening", category="node_state")
                and self.db.awakening_desc):
            return self.db.awakening_desc
        return self.db.desc or ""

    def at_object_receive(self, obj, source_location, **kwargs):
        """
        Fire on_enter / on_first_visit triggers when a character enters.
        Also checks patrol mob disposition (D-02).

        Only fires for player characters — guards against Pitfall 7.
        """
        super().at_object_receive(obj, source_location, **kwargs)
        # Only fire for player characters (Pitfall 7 guard)
        if not (hasattr(obj, 'account') and obj.account):
            return
        from world.trigger_engine import fire_triggers
        fire_triggers(self, "on_enter", obj)
        fire_triggers(self, "on_first_visit", obj)
        # Auto-discover flight points on room enter (D-08)
        # db.flight_point_id initialized None in at_object_creation; truthy only when set by area.flight_point()
        flight_point_id = self.db.flight_point_id
        if flight_point_id:
            discovered = set(obj.db.discovered_flight_points or set())
            if flight_point_id not in discovered:
                discovered.add(flight_point_id)
                obj.db.discovered_flight_points = discovered
                from world.flight_registry import FlightRegistry
                point = FlightRegistry.get_point(flight_point_id)
                point_name = point["name"] if point else flight_point_id
                obj.msg(f"|yYou have discovered the {point_name} Dragon Courier stop.|n")
        # Quest progress: investigate objectives (D-09, D-19)
        from world.quest_engine import check_investigate_objectives
        check_investigate_objectives(obj, self)

        # D-02: Check disposition against any patrol mobs already in this room
        for mob in list(self.contents):
            if not (hasattr(mob, 'db') and mob.db.patrol):
                continue
            # db.patrol initialized None in at_object_creation; truthy only when set by area.patrol()
            patrol_scripts = mob.scripts.get("patrol_script")
            if not patrol_scripts:
                continue
            patrol_script = patrol_scripts[0]
            patrol_def = dict(patrol_script.db.patrol_def or {})
            encounter_delay = patrol_def.get("encounter_delay", 0)
            if encounter_delay > 0:
                from evennia.utils.utils import delay
                delay(
                    encounter_delay,
                    lambda m=mob: _check_mob_encounter_for_arrival(m, obj, self)
                )
            else:
                _check_mob_encounter_for_arrival(mob, obj, self)

    def at_object_leave(self, obj, target_location, **kwargs):
        """Fire on_exit triggers when a player character leaves."""
        super().at_object_leave(obj, target_location, **kwargs)
        if not (hasattr(obj, 'account') and obj.account):
            return
        from world.trigger_engine import fire_triggers
        fire_triggers(self, "on_exit", obj)


class Layer1Room(SoravelonRoom):
    """
    A pre-pooled Layer 1 room. Starts tagged inactive.
    Activated by NodeScript._activate_layer1() during layer swap.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_layer1 = True
        self.tags.add("layer_1_pool", category="node_layer")
        self.tags.add("inactive", category="node_layer")
