"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

import time

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

        # LLM quest system — data collection (implementation post-Milestone-2)
        # Populated by quest consequence system when branching quests complete.
        # Format: list of {quest_id, choice, context, timestamp, arc} dicts.
        self.db.questline_choices = []
        # FK to SeerQuest record when a generated quest is active.
        self.db.active_llm_quest_id = None

        # Command alias system (CMD-03, CMD-04, CMD-05)
        self.db.aliases = {}           # persistent alias dict: {alias_key: expansion_string}

        # Trigger and flight state (used by patrol trigger system and Dragon Courier)
        self.db.fired_triggers = set()          # trigger_ids that have fired once-per-char
        self.db.trigger_cooldowns = {}          # trigger_id -> datetime of last fire
        self.db.discovered_flight_points = set()  # room dbrefs of discovered Dragon Courier stops

        # OOB map state — fog-of-war visited rooms (CLI-07)
        self.db.visited_room_ids = set()        # room_id tags of rooms the character has visited

        # Tag for queryset filtering
        self.tags.add("player_character", category="character_type")

    def at_post_puppet(self, **kwargs):
        """Called after a player connects to this character."""
        super().at_post_puppet(**kwargs)
        from world.world_state import init_session_accumulators

        init_session_accumulators(self)

        # Start per-character session script (XP flush + debt countdown).
        # persistent=False on the script means it auto-removes on logout,
        # so we always create fresh on login. Check for existing first
        # to handle reconnect-without-disconnect edge case.
        from evennia import create_script
        from typeclasses.scripts import SessionCommitScript
        if not self.scripts.get("session_commit_script"):
            create_script(SessionCommitScript, obj=self)

        # Initialize OOB debounce dict on (re)connect (Pitfall 1: ndb is None until set)
        self.ndb.oob_debounce = {}
        # Push full initial state to newly connected client (per D-05)
        from world import oob_publisher
        oob_publisher.push_status_update(self)
        oob_publisher.push_stat_update(self)
        oob_publisher.push_map_update(self)
        oob_publisher.push_inventory_update(self)
        # push_node_event, push_flight_progress, push_combat_update, push_quest_update
        # are event-driven — not pushed on login unless those states are active

        # Ability system volatile state (D-12, D-13)
        self.ndb.ability_cooldowns = {}
        self.ndb.ancestry_ability_used = False
        self.ndb.domain_resource = None  # Default; overwritten below if guild member
        # Initialize domain resource at login for guild members (review feedback:
        # utility/social abilities used outside combat need resources available)
        if self.db.guild_id:
            from world.ability_engine import initialize_domain_resource
            initialize_domain_resource(self)

    def at_pre_unpuppet(self):
        """Called just before a player disconnects from this character."""
        from world.world_state import commit_session_xp
        from world.group_engine import on_member_disconnect

        commit_session_xp(self)
        on_member_disconnect(self)
        super().at_pre_unpuppet()

    def at_after_move(self, source_location, **kwargs):
        """Track visited rooms and push map_update on movement."""
        super().at_after_move(source_location, **kwargs)
        # Track visited room (for fog-of-war, Pitfall 5)
        if self.location:
            room_id = self.location.tags.get(category="room_id")
            if room_id:
                visited = set(self.db.visited_room_ids or set())
                if room_id not in visited:
                    visited.add(room_id)
                    self.db.visited_room_ids = visited
        # Skip map_update during Dragon Courier flight — _arrive_final pushes it instead (Pitfall 6)
        if self.ndb.in_flight:
            return
        from world import oob_publisher
        oob_publisher.push_map_update(self)

        # Update room activity timestamp for still flag logic (review feedback:
        # room_state.py _room_qualifies_as_still reads room.ndb.last_activity)
        if self.location:
            self.location.ndb.last_activity = time.time()

        # Resonance Sense passive (D-22)
        if self.db.guild_id and self.location:
            from world.guild_engine import GUILDS
            guild = GUILDS.get(self.db.guild_id, {})
            if guild.get("primary_domain") == "resonance":
                from world.room_state import get_dominant_flag, SENSE_DISPLAY
                flag = get_dominant_flag(self.location)
                if flag:
                    text = SENSE_DISPLAY.get(flag, "")
                    if text:
                        self.msg(f"|m[Sense] {text}|n")

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
