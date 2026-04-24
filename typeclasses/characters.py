"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character typeclass for Soravelon.

    World-state dimensions, domain scores, and backend level are
    initialized in at_object_creation(). Backend level is internal
    only — never expose to players.
    """

    def at_object_creation(self):
        """Called once when the character is first created."""
        super().at_object_creation()

        # World-state dimension aggregates (fast-read, db_strvalue)
        self.db.reputation_score = 0.0
        self.db.network_score = 0.0
        self.db.bond_score = 0.0
        self.db.legacy_score = 0.0
        self.db.attunement_score = 0.0  # computed aggregate

        # Domain progression
        self.db.domain_scores = {}  # populated as domains are discovered
        self.db.primary_domain = None
        self.db.secondary_domain = None
        self.db.guild_id = None
        self.db.subclass_id = None
        self.db.backend_level = 1  # INTERNAL ONLY — never expose

        # Ancestry
        self.db.ancestry = None

        # Ability system (Phase 5)
        self.db.remnance_discovered = False    # D-25: hide Remnance until discovered
        self.db.active_loadout = []            # D-05: 8 ability_ids from known pool

        # Companion
        self.db.companion_id = None
        self.db.companion_type = None
        self.db.companion_tier = None

        # Currency
        self.db.carried_scales = 0

        # Exploration state
        self.db.discovered_exits = []

        # Command alias system (CMD-03, CMD-04, CMD-05)
        self.db.aliases = {}           # persistent alias dict: {alias_key: expansion_string}

        # Trigger and flight state (used by patrol trigger system and Dragon Courier)
        self.db.fired_triggers = set()          # trigger_ids that have fired once-per-char
        self.db.trigger_cooldowns = {}          # trigger_id -> datetime of last fire
        self.db.discovered_flight_points = set()  # room dbrefs of discovered Dragon Courier stops

        # OOB map state — fog-of-war visited rooms (CLI-07)
        self.db.visited_room_ids = set()        # room_id tags of rooms the character has visited

        # Base attributes (7-stat system)
        from world.base_attributes import STAT_NAMES
        self.db.base_stats = {stat: 10 for stat in STAT_NAMES}
        self.db.stat_xp = {stat: 0.0 for stat in STAT_NAMES}

        # Tag for queryset filtering
        self.tags.add("player_character", category="character_type")

    def at_post_puppet(self, **kwargs):
        """Called after a player connects to this character."""
        super().at_post_puppet(**kwargs)
        from world.session_lifecycle import on_login
        on_login(self)

    def _send_new_player_guidance(self):
        """Delegate contextual login breadcrumbs to the lifecycle layer."""
        from world.session_lifecycle import send_new_player_guidance
        return send_new_player_guidance(self)

    def at_pre_unpuppet(self):
        """Called just before a player disconnects from this character."""
        from world.session_lifecycle import on_logout
        on_logout(self)
        super().at_pre_unpuppet()

    def at_after_move(self, source_location, **kwargs):
        """Track visited rooms and push map_update on movement."""
        super().at_after_move(source_location, **kwargs)
        from world.movement_lifecycle import on_move
        on_move(self, source_location, **kwargs)

    def at_before_move(self, destination, **kwargs):
        """Block movement during Dragon Courier flight (D-12) or when overloaded."""
        if self.ndb.in_flight:
            self.msg("You cannot move while aboard the Dragon Courier.")
            return False
        from world.inventory_helpers import get_carry_state
        state = get_carry_state(self)
        if state == "overloaded":
            self.msg(
                "You cannot move under this weight. "
                "Drop something first."
            )
            return False
        return super().at_before_move(destination, **kwargs)

    def execute_cmd(self, raw_string, session=None, **kwargs):
        """Pre-process input for prefix expansion and alias substitution (CMD-01 through CMD-05)."""
        from world.command_preprocessor import preprocess_input
        processed = preprocess_input(self, raw_string)
        if processed is None:
            # Ambiguity error already sent to player in preprocess_input
            return
        if isinstance(processed, list):
            # Alias expanded to multiple commands (D-16 chaining)
            for cmd_str in processed:
                super().execute_cmd(cmd_str, session=session, **kwargs)
            return
        super().execute_cmd(processed, session=session, **kwargs)

    @property
    def banked_scales(self):
        from world.banking import get_balance
        return get_balance(self)
