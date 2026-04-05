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

        # Base attributes (7-stat system)
        from world.base_attributes import STAT_NAMES
        self.db.base_stats = {stat: 10 for stat in STAT_NAMES}
        self.db.stat_xp = {stat: 0.0 for stat in STAT_NAMES}

        # Tag for queryset filtering
        self.tags.add("player_character", category="character_type")

        # D-11: Set spawn location to Vael's Crossing greeter room
        from evennia.utils.search import search_tag
        greeter_rooms = search_tag("greeter_room", category="spawn_point")
        if greeter_rooms:
            self.home = greeter_rooms[0]
            self.location = greeter_rooms[0]

    def at_post_puppet(self, **kwargs):
        """Called after a player connects to this character."""
        super().at_post_puppet(**kwargs)
        from world.world_state import init_session_accumulators
        from world.base_attributes import (
            STAT_NAMES, derive_max_hp, derive_max_stamina,
        )

        init_session_accumulators(self)

        # Stat growth session accumulators (volatile)
        self.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}

        # Combat-relevant ndb state
        self.ndb.combat_handler = None
        self.ndb.combat_target_id = None
        self.ndb.active_effects = []
        self.ndb.actions_remaining = 0
        self.ndb.ability_used_this_turn = False
        self.ndb.hp = derive_max_hp(self)
        self.ndb.stamina = derive_max_stamina(self)
        self.ndb.charged_ability = None

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

        # Dialogue state (NPC quest offers — cleared on room change per Pitfall 4)
        self.ndb.pending_quest_offer = None

        # Ability system volatile state (D-12, D-13)
        self.ndb.ability_cooldowns = {}
        self.ndb.ancestry_ability_used = False
        self.ndb.domain_resource = None  # Default; overwritten below if guild member
        # Initialize domain resource at login for guild members (review feedback:
        # utility/social abilities used outside combat need resources available)
        if self.db.guild_id:
            from world.ability_engine import initialize_domain_resource
            initialize_domain_resource(self)

        # Start passive HP/stamina regen (Phase 15 recovery engine)
        from world.recovery_engine import start_regen
        start_regen(self)

        # New player guidance (after all init is complete)
        self._send_new_player_guidance()

    def _send_new_player_guidance(self):
        """Send context-sensitive guidance prompts to new players."""
        # Skip guidance for experienced players
        if self.db.backend_level and self.db.backend_level > 1:
            return
        domain_scores = self.db.domain_scores or {}
        if len(domain_scores) > 2:
            return

        self.msg("")  # blank line separator

        # Step 1: ancestry not yet chosen
        if self.db.ancestry is None:
            self.msg("|y[New Player]|n You must first choose your ancestry. "
                     "Type |wancestry|n to begin.")
            return

        # Step 2: no guild yet
        if self.db.guild_id is None:
            self.msg("|y[Hint]|n Your actions shape which guilds take notice of you. "
                     "Explore the world and practice your skills — a guild may discover "
                     "you when you have proven yourself.")

        # Step 3: no active quests (ancestry + guild both set)
        if self.db.guild_id is not None:
            active_quests = self.db.active_quest_ids or []
            if not active_quests:
                self.msg("|y[Hint]|n Speak with the townsfolk in Vael's Crossing. "
                         "Type |wtalk|n near an NPC to begin a conversation.")

    def at_look(self, target=None, **kwargs):
        """Override look to handle sleep blindness."""
        if getattr(self.ndb, "is_sleeping", False):
            return "You are asleep. Use |wwake|n to open your eyes."
        return super().at_look(target, **kwargs)

    def at_pre_unpuppet(self):
        """Called just before a player disconnects from this character."""
        from world.world_state import commit_session_xp
        from world.base_attributes import commit_stat_growth
        from world.group_engine import on_member_disconnect

        # Stop regen on disconnect
        from world.recovery_engine import stop_regen
        stop_regen(self)

        # Flush stat growth accumulators before logout
        commit_stat_growth(self)

        commit_session_xp(self)
        on_member_disconnect(self)

        # Combat cleanup — remove from active combat on disconnect
        if self.ndb.combat_handler:
            try:
                self.ndb.combat_handler.remove_combatant(self)
            except Exception:
                pass  # combat handler may already be cleaned up
            self.ndb.combat_handler = None

        super().at_pre_unpuppet()

    def at_after_move(self, source_location, **kwargs):
        """Track visited rooms and push map_update on movement."""
        super().at_after_move(source_location, **kwargs)

        # Cancel rest/sleep on movement (D-07)
        if getattr(self.ndb, "recovery_state", "active") != "active":
            from world.recovery_engine import cancel_recovery
            cancel_recovery(self)

        # Clear fishing state on move (Pitfall 6: cancel ghost timers)
        fishing_state = getattr(self.ndb, "fishing_state", None)
        if fishing_state:
            for key in ("bite_deferred", "reel_deferred", "idle_deferred"):
                d = fishing_state.get(key)
                if d and hasattr(d, "active") and d.active():
                    d.cancel()
            self.ndb.fishing_state = None
            self.msg("|rFishing interrupted by movement.|n")

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

        # Auto-engage: check for aggressive mobs in room (D-13, same-room only)
        # is_hunter BFS aggro deferred to Phase 6b (requires patrol tick integration)
        if self.location and not self.ndb.combat_handler:
            from world.combat_script import start_combat
            aggressive_mobs = []
            for obj in self.location.contents:
                if obj == self:
                    continue
                if hasattr(obj, "get_behavior_toward"):
                    behavior = obj.get_behavior_toward(self)
                    if behavior == "aggressive" and (obj.db.combat_enabled is not False):
                        aggressive_mobs.append(obj)
            if aggressive_mobs:
                # First aggressive mob initiates; others join the same combat
                start_combat(self.location, aggressive_mobs[0], [self])
                for mob in aggressive_mobs[1:]:
                    from world.combat_script import join_combat
                    handler = self.ndb.combat_handler
                    if handler and not handler.is_combatant(mob):
                        join_combat(handler, mob)

        # Clear stale quest offers on room change (Pitfall 4)
        self.ndb.pending_quest_offer = None

        # Fire NPC reactive echo for player entering the room
        if self.location:
            from world.dialogue_engine import fire_npc_reactive_echo
            fire_npc_reactive_echo(self.location, "player_enters")

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
