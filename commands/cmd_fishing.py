"""
Fishing command system for Soravelon.

Provides active mini-game (cast -> bite -> reel) and idle auto-fishing mode.
Uses gathering_pool infrastructure for fish spot spawning. Bait optionally
improves catch quality. Tool durability consumed per catch.

Design refs: D-16 (active + idle), D-17 (gathering pools), D-18 (bait system).
"""

from commands.command import Command


class CmdFish(Command):
    """
    Fish at a water source.

    Usage:
      fish              - Start active fishing (better rewards)
      fish idle          - Start idle fishing (diminished returns)
      fish stop          - Stop fishing

    Active mode: Cast your line, wait for a bite, then reel to catch.
    Idle mode: Auto-fish with periodic catches at reduced quality.
    """

    key = "fish"
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        character = self.caller
        args = self.args.strip().lower()

        # Handle stop
        if args == "stop":
            self._stop_fishing(character)
            return

        # Check not already fishing
        state = getattr(character.ndb, "fishing_state", None)
        if state:
            character.msg("|rYou are already fishing. Use 'fish stop' to stop.|n")
            return

        # Check tool (fishing_rod)
        tool = self._find_tool(character)
        if not tool:
            character.msg("|rYou need a fishing rod to fish.|n")
            return
        if getattr(tool.db, "durability", None) is not None and tool.db.durability <= 0:
            character.msg(f"|rYour {tool.key} is broken and needs repair.|n")
            return

        # Find fish spot (GatheringNode with node_type="fish")
        node = self._find_fish_spot(character)
        if not node:
            character.msg("|rThere is no fishing spot here.|n")
            return

        # Check for bait (D-18: optional, improves results)
        bait = self._find_bait(character)

        if args == "idle":
            self._start_idle_fishing(character, node, tool, bait)
        else:
            self._start_active_fishing(character, node, tool, bait)

    def _find_tool(self, character):
        """Find a fishing rod in inventory."""
        for item in character.contents:
            if item.tags.has("fishing_rod", category="item_tag"):
                return item
        return None

    def _find_fish_spot(self, character):
        """Find a visible GatheringNode with node_type='fish' in the room."""
        from typeclasses.objects import GatheringNode

        for obj in character.location.contents:
            if isinstance(obj, GatheringNode) and obj.db.node_type == "fish":
                display = obj.get_display_name(looker=character)
                if display is not None:
                    return obj
        return None

    def _find_bait(self, character):
        """Find a bait item in inventory. Returns item or None."""
        for item in character.contents:
            if item.tags.has("bait", category="item_tag"):
                return item
        return None

    # --- Active Mode ---

    def _start_active_fishing(self, character, node, tool, bait):
        """Cast the line. Wait for a random bite timer."""
        import random
        from evennia.utils import delay

        character.msg("|cYou cast your line into the water...|n")
        if bait:
            character.msg(f"|c(Using {bait.key} as bait)|n")

        # Bite timer: 5-15 seconds (bait reduces by 30%)
        bite_time = random.uniform(5, 15)
        if bait:
            bite_time *= 0.7

        start_room = character.location
        character.ndb.fishing_state = {
            "mode": "active",
            "phase": "cast",
            "node": node,
            "start_room": start_room,
            "tool": tool,
            "bait": bait,
        }

        deferred = delay(bite_time, self._on_bite, character)
        character.ndb.fishing_state["bite_deferred"] = deferred

    def _on_bite(self, character):
        """Bite event -- player must reel within 4 seconds."""
        state = getattr(character.ndb, "fishing_state", None)
        if not state or state.get("mode") != "active":
            return
        if character.location != state["start_room"]:
            self._stop_fishing(character)
            return

        from evennia.utils import delay

        character.msg("|y*** You feel a tug on your line! Type 'reel' quickly! ***|n")
        state["phase"] = "bite"

        # Reel window: 4 seconds
        deferred = delay(4.0, self._on_miss, character)
        state["reel_deferred"] = deferred

    def _on_miss(self, character):
        """Player didn't reel in time."""
        state = getattr(character.ndb, "fishing_state", None)
        if not state or state.get("phase") != "bite":
            return
        character.msg("|rThe fish got away! Your line goes slack.|n")
        # Reset to cast phase for another try (don't stop entirely)
        self._start_active_fishing(
            character, state["node"], state["tool"], state.get("bait")
        )

    def _on_reel(self, character):
        """Called by CmdReel when player types 'reel' during bite phase."""
        state = getattr(character.ndb, "fishing_state", None)
        if not state or state.get("phase") != "bite":
            character.msg("|rYou don't have anything on the line.|n")
            return

        # Cancel miss timer
        reel_deferred = state.get("reel_deferred")
        if reel_deferred and reel_deferred.active():
            reel_deferred.cancel()

        # Catch the fish! Full rewards for active mode.
        self._catch_fish(character, state, quality_multiplier=1.0)

    # --- Idle Mode ---

    def _start_idle_fishing(self, character, node, tool, bait):
        """Start auto-fishing with periodic catches."""
        import random
        from evennia.utils import delay

        character.msg("|cYou settle in for idle fishing...|n")
        if bait:
            character.msg(f"|c(Using {bait.key} as bait)|n")

        start_room = character.location
        character.ndb.fishing_state = {
            "mode": "idle",
            "node": node,
            "start_room": start_room,
            "tool": tool,
            "bait": bait,
        }

        # First catch in 15-30 seconds (bait reduces by 20%)
        interval = random.uniform(15, 30)
        if bait:
            interval *= 0.8

        deferred = delay(interval, self._idle_catch, character)
        character.ndb.fishing_state["idle_deferred"] = deferred

    def _idle_catch(self, character):
        """Periodic idle fishing catch."""
        state = getattr(character.ndb, "fishing_state", None)
        if not state or state.get("mode") != "idle":
            return
        if character.location != state["start_room"]:
            self._stop_fishing(character)
            return

        node = state.get("node")
        if not node or not node.pk:
            character.msg("|rThe fishing spot has dried up.|n")
            self._stop_fishing(character)
            return

        # Diminished returns: 50% quality multiplier for idle (D-16)
        self._catch_fish(character, state, quality_multiplier=0.5)

        # Schedule next idle catch
        import random
        from evennia.utils import delay

        interval = random.uniform(20, 40)
        bait = state.get("bait")
        if bait and bait.pk:
            interval *= 0.8
        deferred = delay(interval, self._idle_catch, character)
        state["idle_deferred"] = deferred

    # --- Shared ---

    def _catch_fish(self, character, state, quality_multiplier=1.0):
        """Delegate fish catch to gathering_engine.catch_fish (D-05/D-07)."""
        from world.gathering_engine import catch_fish

        node = state["node"]
        tool = state["tool"]
        bait = state.get("bait")

        success, msg, item, bait_consumed, tool_broken = catch_fish(
            character, node, tool, bait, quality_multiplier
        )
        character.msg(msg)

        if bait_consumed:
            state["bait"] = None

        if not success:
            self._stop_fishing(character)
            return

        if tool_broken:
            self._stop_fishing(character)
            return

        # If active mode, restart cast for another fish
        if state.get("mode") == "active":
            node_ref = state["node"]
            if node_ref and node_ref.pk:
                self._start_active_fishing(
                    character, node_ref, tool, state.get("bait")
                )
            else:
                character.msg("|rThe fishing spot is depleted.|n")
                self._stop_fishing(character)

    def _stop_fishing(self, character):
        """Cancel all fishing timers and clear state."""
        state = getattr(character.ndb, "fishing_state", None)
        if state:
            for key in ("bite_deferred", "reel_deferred", "idle_deferred"):
                deferred = state.get(key)
                if deferred and hasattr(deferred, "active") and deferred.active():
                    deferred.cancel()
        character.ndb.fishing_state = None
        character.msg("|xYou stop fishing.|n")


class CmdReel(Command):
    """
    Reel in a fish when you feel a bite.

    Usage:
      reel

    Only works during active fishing when a fish is biting.
    """

    key = "reel"
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        # Delegate to CmdFish's reel handler
        CmdFish()._on_reel(self.caller)
