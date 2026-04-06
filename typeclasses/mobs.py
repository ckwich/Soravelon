"""
Mob typeclasses for Soravelon.

SoravelonMob is the base typeclass for all hostile and neutral creatures.
Handles affix display, affix reveal in combat, and loot tier.
"""

from evennia.objects.objects import DefaultCharacter
from world.mob_affix_roller import apply_affixes_to_mob, get_star_prefix
from world.mob_affixes import MOB_AFFIXES


class SoravelonMob(DefaultCharacter):
    """
    Base typeclass for all Soravelon mobs.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.rarity = "normal"
        self.db.affix_list = []
        self.db.mob_type = None
        self.db.zone_id = None
        self.db.faction = None
        self.db.base_aggression = "passive"
        self.db.base_disposition = 0.0
        self.db.trust_sensitive = False
        self.db.quest_modifier = None
        self.db.prestige_modifier = 1.0

        # Stat ranges (authored at REFERENCE_LEVEL = backend 10)
        self.db.hp_min = 80
        self.db.hp_max = 120
        self.db.damage_min = 8
        self.db.damage_max = 14
        self.db.speed = 1.0
        self.db.accuracy = 0.0
        self.db.evasion = 0.0
        self.db.resistances = {}

        # hp, hp_max, ref_damage_min, ref_damage_max set at spawn
        # by initialize_mob_combat_stats() — not initialized here

        # Abilities (data-driven, authored by builder)
        self.db.abilities = []

        # Patrol system attributes
        self.db.patrol = None          # patrol definition dict; None = not a patrol mob
        self.db.combat_enabled = True  # D-03: set False for invulnerable mobs (e.g., Caldenmere)
        self.db.triggers = []          # trigger list for trigger_engine
        self.db.tome_drop = None       # D-18: item_id of tome to drop on named mob death

    def spawn_with_affixes(self, room):
        """Roll and apply affixes. Call after creation, not in at_object_creation."""
        return apply_affixes_to_mob(self, room)

    def initialize_for_spawn(self, room):
        """
        Call after mob is placed and rarity is set.
        Rolls affixes AND combat stats. Replaces spawn_with_affixes
        for new code — spawn_with_affixes kept for backward compat.
        """
        apply_affixes_to_mob(self, room)
        from world.zone_scaling import initialize_mob_combat_stats
        initialize_mob_combat_stats(self)

    def get_display_name(self, looker=None, **kwargs):
        """Prepend star prefix based on rarity."""
        base_name = super().get_display_name(looker, **kwargs)
        prefix = get_star_prefix(self.db.rarity)
        if prefix:
            return f"{prefix} {base_name}"
        return base_name

    def reveal_affix(self, looker, affix_tag):
        """
        Reveal a specific affix on first interaction.
        Returns reveal message or None if already revealed.
        """
        if not hasattr(self.ndb, "revealed_affixes") or self.ndb.revealed_affixes is None:
            self.ndb.revealed_affixes = set()

        if affix_tag in self.ndb.revealed_affixes:
            return None

        self.ndb.revealed_affixes.add(affix_tag)
        affix_def = MOB_AFFIXES.get(affix_tag)
        if not affix_def:
            return None

        mob_name = self.get_display_name(looker)
        return affix_def["reveal_message"].format(mob_name=mob_name)

    def get_combat_modifiers(self):
        """Return merged dict of all active combat modifiers from affixes."""
        modifiers = {}
        for affix_tag in (self.db.affix_list or []):
            affix_def = MOB_AFFIXES.get(affix_tag, {})
            for key, value in affix_def.get("combat_modifiers", {}).items():
                if key in modifiers:
                    modifiers[key] += value
                else:
                    modifiers[key] = value
        return modifiers

    def has_immunity(self, effect_type):
        """
        Check if mob is immune to a given effect.
        Returns (bool immune, str|None reveal_message).
        """
        immunity_map = {
            "burn": "fire_immune",
            "poison": "poison_immune",
            "stun": "stun_immune",
            "root": "root_immune",
        }
        immunity_tag = immunity_map.get(effect_type)
        if not immunity_tag:
            return False, None

        if self.tags.get(immunity_tag, category="mob_affix"):
            reveal_msg = self.reveal_affix(None, immunity_tag)
            return True, reveal_msg

        return False, None

    def get_loot_tier(self):
        """Return loot tier based on rarity."""
        return self.db.rarity or "normal"

    def get_disposition(self, character):
        """Return disposition float toward this character. Computed fresh."""
        from world.mob_disposition import get_mob_disposition
        return get_mob_disposition(self, character)

    def get_behavior_toward(self, character):
        """Return behavior string. Combat system should cache per encounter."""
        from world.mob_disposition import get_mob_behavior
        return get_mob_behavior(self, character)

    def at_death(self, killer=None):
        """Clean up ndb on death, fire triggers, drop loot, schedule respawn."""
        from world.death_lifecycle import on_mob_death
        on_mob_death(self, killer)
