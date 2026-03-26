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

        # Companion
        self.db.companion_id = None
        self.db.companion_type = None
        self.db.companion_tier = None

        # Currency
        self.db.carried_scales = 0

        # Exploration state
        self.db.discovered_exits = []

        # Base attributes (7-stat system)
        from world.base_attributes import STAT_NAMES
        self.db.base_stats = {stat: 10 for stat in STAT_NAMES}
        self.db.stat_xp = {stat: 0.0 for stat in STAT_NAMES}

        # Tag for queryset filtering
        self.tags.add("player_character", category="character_type")

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

    def at_pre_unpuppet(self):
        """Called just before a player disconnects from this character."""
        from world.world_state import commit_session_xp
        from world.base_attributes import commit_stat_growth
        from world.group_engine import on_member_disconnect

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

    def at_before_move(self, destination, **kwargs):
        """Block movement if overloaded."""
        from world.inventory_helpers import get_carry_state
        state = get_carry_state(self)
        if state == "overloaded":
            self.msg(
                "You cannot move under this weight. "
                "Drop something first."
            )
            return False
        return True

    @property
    def banked_scales(self):
        from world.banking import get_balance
        return get_balance(self)
