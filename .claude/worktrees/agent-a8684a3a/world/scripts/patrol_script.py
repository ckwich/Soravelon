"""
PatrolScript — tick-driven patrol routing for Soravelon mobs.

Attached to a SoravelonMob. Self-ticking at a configurable interval (default 5s).
Drives BFS-computed patrol routes with encounter checks and interrupt handling.

Key behaviors:
- at_repeat() advances the mob one step along its precomputed route each tick
- Pitfall 2 guard: stops script if mob is dead/deleted
- Disposition check on arrival (D-01 encounter_delay)
- on_combat_end() handles resume/reset_to_start/abandon interrupt modes
"""

from typeclasses.scripts import SoravelonScript


class PatrolScript(SoravelonScript):
    """
    Manages patrol routing for a mob.

    Configured via db.patrol_def dict (set by area builder):
        encounter_delay (int): Seconds before disposition check after arrival (D-01)
        echo_radius (int): BFS radius for movement echo broadcasts (D-04)
        move_echo (str): Message to echo when mob moves
        interrupt_mode (str): 'resume', 'reset_to_start', or 'abandon' (post-combat)

    db.route_ids: list of room dbref integers (e.g. [123, 124, 125])
    db.route_index: current position in route
    db.interrupted: True while mob is in combat
    """

    def at_script_creation(self):
        super().at_script_creation()
        self.key = "patrol_script"
        self.persistent = True
        self.interval = 5    # 5-second tick; tunable per patrol definition
        self.repeats = 0     # infinite
        self.db.route_ids = []       # list of room dbref ints
        self.db.route_index = 0      # current position in route
        self.db.patrol_def = {}      # full patrol definition dict from AreaBuilder
        self.db.interrupted = False  # True while mob is in combat
        self.tags.add("patrol_script", category="script_type")

    def at_repeat(self):
        """Called every self.interval seconds. Advances mob one route step."""
        mob = self.obj
        # Pitfall 2: script may tick after mob deletion — guard here
        if not mob or not mob.pk:
            self.stop()
            return
        if self.db.interrupted:
            return
        self._advance_route()

    def _advance_route(self):
        """Move mob to next room in route and check for encounters."""
        from world.patrol_engine import next_patrol_step, check_patrol_encounter, echo_to_radius

        route_ids = list(self.db.route_ids or [])
        if not route_ids:
            return

        next_room, next_index = next_patrol_step(self.obj, route_ids, self.db.route_index)
        if not next_room:
            return

        # SaverDict: update index atomically
        self.db.route_index = next_index

        patrol_def = dict(self.db.patrol_def or {})
        echo_radius = patrol_def.get("echo_radius", 0)
        encounter_delay = patrol_def.get("encounter_delay", 0)

        # Announce movement to nearby rooms if echo_radius set (D-04)
        if echo_radius > 0:
            echo_msg = patrol_def.get("move_echo", f"{self.obj.key} passes through.")
            echo_to_radius(self.obj, echo_msg, echo_radius)

        # Move mob — fires at_object_leave on current room, at_object_receive on next room
        self.obj.move_to(next_room, quiet=False)

        # Disposition check on arrival (D-01)
        if encounter_delay > 0:
            from evennia.utils.utils import delay
            delay(encounter_delay, lambda r=next_room: self._check_disposition_on_arrival(r))
        else:
            self._check_disposition_on_arrival(next_room)

    def _check_disposition_on_arrival(self, room):
        """Check if mob should engage any player in the room after arrival."""
        mob = self.obj
        if not mob or not mob.pk:
            return
        from world.patrol_engine import check_patrol_encounter
        if check_patrol_encounter(mob, room):
            self._initiate_combat(room)

    def _initiate_combat(self, room):
        """Interrupt patrol and start combat with the first hostile target in room."""
        mob = self.obj
        for obj in list(room.contents):
            if hasattr(obj, 'account') and obj.account:
                from world.mob_disposition import get_mob_behavior
                behavior = get_mob_behavior(mob, obj)
                if behavior in ("aggressive", "territorial"):
                    self.db.interrupted = True
                    mob.ndb.patrol_combat_target = obj
                    mob.execute_cmd(f"attack {obj.key}")
                    return

    def on_combat_end(self, outcome):
        """
        Called by the combat system when a fight resolves.
        Resumes patrol routing according to the interrupt_mode setting.

        Args:
            outcome (str): Combat outcome ('victory', 'defeat', 'fled').

        interrupt_mode values:
            'resume' (default): Continue from current route_index.
            'reset_to_start': Return to route[0] before resuming.
            'abandon': Stop patrolling entirely.
        """
        patrol_def = dict(self.db.patrol_def or {})
        mode = patrol_def.get("interrupt_mode", "resume")

        if mode == "reset_to_start":
            self.db.route_index = 0
        elif mode == "abandon":
            self.stop()
            return
        # "resume" — continue from current position (no index change needed)

        self.db.interrupted = False
