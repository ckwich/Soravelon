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
        self.db.threat_level = "solo"

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
        self.db.spawn_record_id = None  # SpawnRecord FK for death → respawn lookup (D-06)

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

    # Threat level display tags
    THREAT_TAGS = {
        "elite": "|!y|530[Elite]|n",
        "boss": "|r[Boss]|n",
    }

    def get_display_name(self, looker=None, **kwargs):
        """Prepend star prefix and threat tag based on rarity and threat_level."""
        base_name = super().get_display_name(looker, **kwargs)
        prefix = get_star_prefix(self.db.rarity)
        if prefix:
            base_name = f"{prefix} {base_name}"
        threat = self.THREAT_TAGS.get(self.db.threat_level)
        if threat:
            base_name = f"{threat} {base_name}"
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
        """Clean up ndb on death, fire triggers, drop loot, schedule respawn via SpawnRecord."""
        self.ndb.revealed_affixes = set()
        if hasattr(self.ndb, 'combat_scales'):
            self.ndb.combat_scales = {}

        # Fire on_mob_death triggers (existing)
        if self.db.triggers:
            from world.trigger_engine import fire_triggers
            context = {"mob": self, "room": self.location}
            if killer and hasattr(killer, 'account') and killer.account:
                fire_triggers(self, "on_mob_death", killer, context=context)

        # Drop loot (D-35: roll_loot called from at_death)
        room = self.location
        if room and killer:
            from world.loot_tables import roll_loot
            from world.item_spawner import create_item_from_template
            drops = roll_loot(self, killer)
            for item_def in drops:
                create_item_from_template(item_def, location=room)

        # Drop tome if named mob (D-18: tome pre-assigned)
        if self.db.tome_drop and room:
            from world.item_spawner import create_item_from_template
            tome_def = {
                "item_id": self.db.tome_drop,
                "key": self.db.tome_drop.replace("_", " "),
                "item_type": "item",
                "desc": f"A tome recovered from {self.key}.",
                "rarity": "rare",
                "weight": 0.5,
                "value": 50,
            }
            create_item_from_template(tome_def, location=room)

        # Named mob death: write WorldEventLog entry (D-05)
        is_named = self.tags.get("mob_id", category="mob_id") is not None
        if is_named and killer:
            from world.models import WorldEventLog
            WorldEventLog.objects.create(
                event_type="named_mob_death",
                zone_id=self.db.zone_id or "",
                character_id=killer.id if killer else None,
                description=f"{self.key} was slain by {killer.key}",
                data={"named_id": self.db.named_id or self.key, "mob_key": self.key},
            )

        # Write room state flags (D-24)
        if room:
            from world.room_state import add_room_flag
            add_room_flag(room, "blood_soaked")

            # Nature-affinity mob death
            if self.db.faction and self.db.faction.lower() in (
                "verdance", "wardens", "nature"
            ):
                add_room_flag(room, "fading_life")

            # Named/boss mob death
            is_boss = self.db.rarity == "legendary"
            if is_named or is_boss:
                add_room_flag(room, "power_vacuum")

        # Quest progress: kill objectives (D-07, D-19)
        if killer and hasattr(killer, 'account') and killer.account:
            from world.quest_engine import check_kill_objectives
            check_kill_objectives(killer, self)

        # Schedule respawn via SpawnRecord (replaces callLater)
        from world.mob_spawner import schedule_respawn_from_death
        schedule_respawn_from_death(self)
