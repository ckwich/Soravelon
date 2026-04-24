"""
Tests for world/ability_registry.py and world/ability_engine.py.

Covers ABL-01 (registry structure), ABL-02 (dispatch routing),
ABL-03 (tier gating via CharacterAbility), ABL-05 (cooldowns),
ABL-06 (resource management), ABL-04 (resource systems).

Uses unittest.TestCase + MagicMock -- pure logic with mocked ORM.
"""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
django.setup()

from world.ability_registry import (
    ABILITIES,
    ABILITY_TIERS,
    DOMAIN_ABILITIES,
    EFFECT_TYPES,
    SUBCLASS_SIGNATURES,
    get_ability,
)


# ---------------------------------------------------------------------------
# Helper: mock character with ndb namespace
# ---------------------------------------------------------------------------

def _mock_character(
    ability_cooldowns=None,
    domain_resource=None,
    ancestry_ability_used=False,
    guild_id=None,
    location=None,
    echoes_investigation_bonus=None,
    reagent_stock=None,
    component_stock=None,
    char_id=1,
    key="TestChar",
    combat_handler=None,
    group_leader_id=None,
):
    """Create a MagicMock character with ndb/db for ability engine tests."""
    char = MagicMock()
    char.id = char_id
    char.key = key
    char.ndb = SimpleNamespace(
        ability_cooldowns=ability_cooldowns if ability_cooldowns is not None else {},
        domain_resource=domain_resource,
        ancestry_ability_used=ancestry_ability_used,
        active_effects=[],
        ability_used_this_turn=False,
        combat_handler=combat_handler,
        group_leader_id=group_leader_id,
    )
    char.db = SimpleNamespace(
        guild_id=guild_id,
        abilities=None,
        echoes_investigation_bonus=echoes_investigation_bonus,
        reagent_stock=reagent_stock,
        component_stock=component_stock,
        base_stats={"strength": 10, "agility": 10, "intellect": 10},
        backend_level=10,
        hp=100,
        hp_max=100,
        immunities=[],
    )
    char.location = location
    return char


# ===========================================================================
# ABL-01: Registry structure validation
# ===========================================================================


REQUIRED_ABILITY_FIELDS = {
    "id", "name", "domain", "tier", "resource_cost", "resource_type",
    "cooldown", "charge_turns", "effect_type", "scaling_primary",
    "scaling_secondary", "application_chance", "description",
    "room_flag_written", "attuned_variants", "subclass_id",
}


class TestAbilityRegistryStructure(unittest.TestCase):
    """ABILITIES dict has correct structure and required fields."""

    def test_all_abilities_have_required_fields(self):
        """Every ability entry has all 16 required fields."""
        for ability_id, ability in ABILITIES.items():
            missing = REQUIRED_ABILITY_FIELDS - set(ability.keys())
            self.assertEqual(
                missing, set(),
                f"Ability '{ability_id}' missing fields: {missing}",
            )

    def test_domain_abilities_populated(self):
        """DOMAIN_ABILITIES has at least 10 keys (one per domain)."""
        self.assertGreaterEqual(len(DOMAIN_ABILITIES), 10)

    def test_subclass_signatures_populated(self):
        """SUBCLASS_SIGNATURES has at least 1 entry."""
        self.assertGreaterEqual(len(SUBCLASS_SIGNATURES), 1)

    def test_all_effect_types_covered(self):
        """All EFFECT_TYPES appear in at least one ability."""
        used_effects = {a["effect_type"] for a in ABILITIES.values()}
        for et in EFFECT_TYPES:
            self.assertIn(et, used_effects,
                          f"Effect type '{et}' not used by any ability")

    def test_get_ability_returns_dict(self):
        """get_ability returns a dict for a known ability."""
        result = get_ability("crushing_advance")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "Crushing Advance")

    def test_get_ability_unknown_returns_none(self):
        """get_ability returns None for unknown ability_id."""
        self.assertIsNone(get_ability("fake_ability"))

    def test_ability_tiers_thresholds(self):
        """ABILITY_TIERS has 4 entries with correct GTS thresholds."""
        self.assertEqual(len(ABILITY_TIERS), 4)
        self.assertEqual(ABILITY_TIERS[1], 0)
        self.assertEqual(ABILITY_TIERS[4], 85)

    def test_ancestry_abilities_are_authored_and_not_mixed_into_domain_pool(self):
        """Starting ancestry abilities exist but do not auto-grant through domain tiers."""
        for ability_id in ("second_wind", "immovable", "vanish", "audacity"):
            self.assertIn(ability_id, ABILITIES)

        self.assertNotIn("second_wind", DOMAIN_ABILITIES["combat"][1])
        self.assertNotIn("vanish", DOMAIN_ABILITIES["subterfuge"][1])


# ===========================================================================
# ABL-02: use_ability dispatch routing
# ===========================================================================


class TestUseAbilityDispatch(unittest.TestCase):
    """use_ability dispatches to correct effect handler."""

    @patch("world.combat_engine.resolve_ability_damage", return_value=(True, "Crushing Advance hits Goblin for 25 damage.", 25))
    @patch("world.models.CharacterAbility")
    def test_dispatches_damage(self, mock_ca_cls, mock_resolve):
        """use_ability for crushing_advance returns success with ability name."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        target = MagicMock()
        target.key = "Goblin"

        ok, msg = use_ability(char, "crushing_advance", target=target)

        self.assertTrue(ok)
        self.assertIn("Crushing Advance", msg)

    @patch("world.models.CharacterAbility")
    def test_unknown_ability(self, mock_ca_cls):
        """use_ability for unknown ability_id returns failure."""
        from world.ability_engine import use_ability

        char = _mock_character()
        ok, msg = use_ability(char, "fake_ability")

        self.assertFalse(ok)
        self.assertIn("Unknown ability", msg)

    @patch("world.models.CharacterAbility")
    def test_not_unlocked(self, mock_ca_cls):
        """use_ability fails when CharacterAbility record doesn't exist."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = False

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        ok, msg = use_ability(char, "crushing_advance")

        self.assertFalse(ok)
        self.assertIn("not unlocked", msg.lower())


class TestAbilityUnlockSync(unittest.TestCase):
    def test_expected_unlocks_include_ancestry_and_tiered_primary_domain(self):
        from world.ability_engine import get_expected_unlocked_ability_ids

        char = _mock_character(guild_id="ironblood")
        char.db.ancestry = "human"
        char.db.primary_domain = "combat"
        char.db.secondary_domain = "subterfuge"
        char.db.subclass_id = "duskblade"
        char.db.domain_scores = {"combat": 30.0, "subterfuge": 0.0}

        expected = get_expected_unlocked_ability_ids(char)

        self.assertIn("second_wind", expected)
        self.assertIn("crushing_advance", expected)
        self.assertIn("iron_resolve", expected)
        self.assertNotIn("rending_strike", expected)
        self.assertNotIn("duskblade_shadow_strike", expected)

    def test_expected_unlocks_gain_signature_abilities_when_tier_reached(self):
        from world.ability_engine import get_expected_unlocked_ability_ids

        char = _mock_character(guild_id="ironblood")
        char.db.ancestry = "human"
        char.db.primary_domain = "combat"
        char.db.secondary_domain = "subterfuge"
        char.db.subclass_id = "duskblade"
        char.db.domain_scores = {"combat": 80.0, "subterfuge": 30.0}

        expected = get_expected_unlocked_ability_ids(char)

        self.assertIn("rending_strike", expected)
        self.assertIn("duskblade_shadow_strike", expected)
        self.assertNotIn("duskblade_vanishing_edge", expected)

    @patch("world.models.CharacterAbility")
    def test_sync_unlocks_grants_missing_expected_records(self, mock_ca_cls):
        from world.ability_engine import sync_character_ability_unlocks

        mock_ca_cls.objects.get_or_create.side_effect = (
            lambda **kwargs: (MagicMock(), kwargs["ability_id"] != "second_wind")
        )

        char = _mock_character(guild_id="ironblood")
        char.db.ancestry = "human"
        char.db.primary_domain = "combat"
        char.db.secondary_domain = "subterfuge"
        char.db.subclass_id = "duskblade"
        char.db.domain_scores = {"combat": 30.0, "subterfuge": 0.0}

        granted = sync_character_ability_unlocks(char)

        self.assertNotIn("second_wind", granted)
        self.assertIn("crushing_advance", granted)
        self.assertIn("iron_resolve", granted)


# ===========================================================================
# ABL-05: Cooldown management
# ===========================================================================


class TestCooldowns(unittest.TestCase):
    """Cooldown tracking, decrement, and clear."""

    @patch("world.models.CharacterAbility")
    def test_cooldown_blocks(self, mock_ca_cls):
        """Ability on cooldown returns failure with rounds remaining."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True

        char = _mock_character(
            ability_cooldowns={"crushing_advance": 3},
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        ok, msg = use_ability(char, "crushing_advance")

        self.assertFalse(ok)
        self.assertIn("cooldown", msg.lower())
        self.assertIn("3", msg)

    @patch("world.status_effects.apply_effect", return_value=(True, "Buff applied."))
    @patch("world.models.CharacterAbility")
    def test_cooldown_set_after_use(self, mock_ca_cls, mock_apply):
        """Using an ability with cooldown sets ndb.ability_cooldowns."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        mock_ca_cls.objects.filter.return_value.update.return_value = 1

        char = _mock_character(
            domain_resource={"type": "focus", "current": 100, "max": 100},
        )
        # shadow_step has cooldown=2; mock apply_effect since "evasion" buff
        # type is not yet in the status_effects registry
        ok, msg = use_ability(char, "shadow_step")

        self.assertTrue(ok)
        self.assertEqual(char.ndb.ability_cooldowns["shadow_step"], 2)

    @patch("world.models.CharacterAbility.objects.filter")
    def test_charged_ability_requires_charge_flow_in_combat(self, mock_ca_filter):
        """Charge-turn abilities cannot be fired instantly through use_ability."""
        from world.ability_engine import use_ability

        mock_ca_filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "mana", "current": 100, "max": 100},
            combat_handler=MagicMock(),
        )

        ok, msg = use_ability(char, "meteor_strike", target=MagicMock())

        self.assertFalse(ok)
        self.assertIn("must be charged", msg.lower())
        self.assertEqual(char.ndb.domain_resource["current"], 100)

    @patch("world.models.CharacterAbility.objects.filter")
    def test_internal_charge_release_can_resolve_ability(self, mock_ca_filter):
        """The auto-release path bypasses the manual charge gate."""
        from world.ability_engine import use_ability

        mock_ca_filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "mana", "current": 100, "max": 100},
            combat_handler=MagicMock(),
        )
        char.ndb.resolving_charged_ability = True
        target = MagicMock()

        with patch.dict(
            "world.ability_engine.EFFECT_HANDLERS",
            {"damage": lambda character, ability, resolved_target: (True, "Meteor Strike lands.")},
            clear=False,
        ):
            ok, msg = use_ability(char, "meteor_strike", target=target)

        self.assertTrue(ok)
        self.assertIn("Meteor Strike lands.", msg)

    def test_decrement_cooldowns(self):
        """decrement_cooldowns reduces all by 1, removes expired."""
        from world.ability_engine import decrement_cooldowns

        char = _mock_character(
            ability_cooldowns={"a": 3, "b": 1},
        )
        decrement_cooldowns(char)

        self.assertEqual(char.ndb.ability_cooldowns["a"], 2)
        self.assertNotIn("b", char.ndb.ability_cooldowns)

    def test_clear_encounter_cooldowns(self):
        """clear_encounter_cooldowns resets cooldowns and ancestry flag."""
        from world.ability_engine import clear_encounter_cooldowns

        char = _mock_character(
            ability_cooldowns={"a": 3, "b": 1},
            ancestry_ability_used=True,
        )
        clear_encounter_cooldowns(char)

        self.assertEqual(char.ndb.ability_cooldowns, {})
        self.assertFalse(char.ndb.ancestry_ability_used)


# ===========================================================================
# ABL-06: Resource management
# ===========================================================================


class TestResourceManagement(unittest.TestCase):
    """Domain resource spend, build, and initialize."""

    def test_spend_resource_success(self):
        """Spending within budget succeeds and deducts."""
        from world.ability_engine import spend_domain_resource

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 50, "max": 100},
        )
        ok, msg = spend_domain_resource(char, 20)

        self.assertTrue(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 30)

    def test_spend_resource_insufficient(self):
        """Spending more than available fails."""
        from world.ability_engine import spend_domain_resource

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 10, "max": 100},
        )
        ok, msg = spend_domain_resource(char, 20)

        self.assertFalse(ok)
        self.assertIn("Insufficient", msg)

    def test_build_resource_capped(self):
        """Building resource caps at max."""
        from world.ability_engine import build_domain_resource

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 90, "max": 100},
        )
        result = build_domain_resource(char, 20)

        self.assertEqual(result, 100)
        self.assertEqual(char.ndb.domain_resource["current"], 100)

    @patch("world.guild_engine.FINGERPRINTS", {
        "combat": {"resource_type": "momentum"},
    })
    @patch("world.guild_engine.GUILDS", {
        "ironblood": {"primary_domain": "combat"},
    })
    def test_initialize_domain_resource(self):
        """initialize_domain_resource sets up ndb.domain_resource from guild."""
        from world.ability_engine import initialize_domain_resource

        char = _mock_character(guild_id="ironblood")
        initialize_domain_resource(char)

        res = char.ndb.domain_resource
        self.assertIsNotNone(res)
        self.assertEqual(res["type"], "momentum")
        self.assertEqual(res["current"], 0)
        self.assertEqual(res["max"], 100)

    def test_initialize_domain_resource_no_guild(self):
        """initialize_domain_resource with no guild sets resource to None."""
        from world.ability_engine import initialize_domain_resource

        char = _mock_character(guild_id=None)
        initialize_domain_resource(char)

        self.assertIsNone(char.ndb.domain_resource)

    def test_get_domain_resource(self):
        """get_domain_resource returns current ndb.domain_resource."""
        from world.ability_engine import get_domain_resource

        resource = {"type": "momentum", "current": 50, "max": 100}
        char = _mock_character(domain_resource=resource)

        self.assertEqual(get_domain_resource(char), resource)

    def test_build_resource_no_resource(self):
        """Building with no resource returns 0."""
        from world.ability_engine import build_domain_resource

        char = _mock_character(domain_resource=None)
        self.assertEqual(build_domain_resource(char, 10), 0)


# ===========================================================================
# ABL-03: Tier gating via CharacterAbility
# ===========================================================================


class TestAbilityTierGating(unittest.TestCase):
    """Ability access requires CharacterAbility record."""

    @patch("world.models.CharacterAbility")
    def test_tier_gate_blocks_without_record(self, mock_ca_cls):
        """use_ability fails when no CharacterAbility record exists."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = False

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        ok, msg = use_ability(char, "duskblade_shadow_strike")

        self.assertFalse(ok)
        self.assertIn("not unlocked", msg.lower())


# ===========================================================================
# ABL-04: Resource system tests (all 10 domain resources)
# ===========================================================================


class TestResourceInitialization(unittest.TestCase):
    """Type-aware resource initialization for all 10 domain resource types."""

    def _make_char_with_guild(self, guild_id, **db_extras):
        char = _mock_character(guild_id=guild_id)
        for key, val in db_extras.items():
            setattr(char.db, key, val)
        return char

    @patch("world.guild_engine.FINGERPRINTS", {
        "combat": {"resource_type": "momentum"},
    })
    @patch("world.guild_engine.GUILDS", {
        "ironblood": {"primary_domain": "combat"},
    })
    def test_momentum_init(self):
        """Momentum starts at 0 with max 100."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("ironblood")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "momentum")
        self.assertEqual(res["current"], 0)
        self.assertEqual(res["max"], 100)

    @patch("world.guild_engine.FINGERPRINTS", {
        "subterfuge": {"resource_type": "focus"},
    })
    @patch("world.guild_engine.GUILDS", {
        "shadowguild": {"primary_domain": "subterfuge"},
    })
    def test_focus_init(self):
        """Focus starts at 0 with max 5 (combo points)."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("shadowguild")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "focus")
        self.assertEqual(res["current"], 0)
        self.assertEqual(res["max"], 5)

    @patch("world.guild_engine.FINGERPRINTS", {
        "naturalism": {"resource_type": "balance"},
    })
    @patch("world.guild_engine.GUILDS", {
        "wildheart": {"primary_domain": "naturalism"},
    })
    def test_balance_init(self):
        """Balance starts at 50 (center) with max 100."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("wildheart")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "balance")
        self.assertEqual(res["current"], 50)
        self.assertEqual(res["max"], 100)

    @patch("world.guild_engine.FINGERPRINTS", {
        "resonance_domain": {"resource_type": "resonance"},
    })
    @patch("world.guild_engine.GUILDS", {
        "resonator": {"primary_domain": "resonance_domain"},
    })
    def test_resonance_init(self):
        """Resonance starts at 0 with max 100."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("resonator")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "resonance")
        self.assertEqual(res["current"], 0)
        self.assertEqual(res["max"], 100)

    @patch("world.guild_engine.FINGERPRINTS", {
        "arcana": {"resource_type": "mana", "resource_max": 200},
    })
    @patch("world.guild_engine.GUILDS", {
        "arcanist": {"primary_domain": "arcana"},
    })
    def test_mana_init(self):
        """Mana starts full (current == max)."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("arcanist")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "mana")
        self.assertEqual(res["current"], res["max"])
        self.assertEqual(res["max"], 200)

    @patch("world.world_state.get_dimension_score", return_value=60)
    @patch("world.guild_engine.FINGERPRINTS", {
        "diplomacy": {"resource_type": "influence"},
    })
    @patch("world.guild_engine.GUILDS", {
        "diplomat": {"primary_domain": "diplomacy"},
    })
    def test_influence_init_from_reputation(self, mock_dim):
        """Influence pool = 20 + reputation * 0.5. Rep=60 -> pool=50."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("diplomat")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "influence")
        self.assertEqual(res["current"], 50)
        self.assertEqual(res["max"], 50)

    @patch("world.guild_engine.FINGERPRINTS", {
        "alchemy": {"resource_type": "reagents"},
    })
    @patch("world.guild_engine.GUILDS", {
        "alchemist": {"primary_domain": "alchemy"},
    })
    def test_reagents_init(self):
        """Reagents start from db.reagent_stock or default 50."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("alchemist", reagent_stock=35)
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "reagents")
        self.assertEqual(res["current"], 35)

    @patch("world.guild_engine.FINGERPRINTS", {
        "engineering": {"resource_type": "components"},
    })
    @patch("world.guild_engine.GUILDS", {
        "engineer": {"primary_domain": "engineering"},
    })
    def test_components_init(self):
        """Components start from db.component_stock or default 50."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("engineer", component_stock=40)
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "components")
        self.assertEqual(res["current"], 40)

    @patch("world.guild_engine.FINGERPRINTS", {
        "tactics": {"resource_type": "command"},
    })
    @patch("world.guild_engine.GUILDS", {
        "tactician": {"primary_domain": "tactics"},
    })
    def test_command_init(self):
        """Command starts at 0 with max 100."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild("tactician")
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "command")
        self.assertEqual(res["current"], 0)
        self.assertEqual(res["max"], 100)

    @patch("world.guild_engine.FINGERPRINTS", {
        "remnance": {"resource_type": "echoes"},
    })
    @patch("world.guild_engine.GUILDS", {
        "remnant": {"primary_domain": "remnance"},
    })
    def test_echoes_init_with_bonus(self):
        """Echoes start at investigation bonus amount if present."""
        from world.ability_engine import initialize_domain_resource
        char = self._make_char_with_guild(
            "remnant",
            echoes_investigation_bonus={"amount": 20, "encounters_remaining": 2},
        )
        initialize_domain_resource(char)
        res = char.ndb.domain_resource
        self.assertEqual(res["type"], "echoes")
        self.assertEqual(res["current"], 20)
        self.assertEqual(res["max"], 100)


class TestFocusResource(unittest.TestCase):
    """Focus combo point system: cap 5, builders +1, miss resets, skip resets."""

    def _focus_char(self, current=0):
        return _mock_character(
            domain_resource={"type": "focus", "current": current, "max": 5},
        )

    def test_focus_builder_adds_one(self):
        """Focus builder adds 1 combo point on success."""
        from world.ability_engine import _post_ability_resource_hook
        char = self._focus_char(current=2)
        ability = {"effect_params": {"is_builder": True}}
        _post_ability_resource_hook(char, ability, result=True)
        self.assertEqual(char.ndb.domain_resource["current"], 3)

    def test_focus_builder_caps_at_five(self):
        """Focus builder does not exceed max 5."""
        from world.ability_engine import _post_ability_resource_hook
        char = self._focus_char(current=5)
        ability = {"effect_params": {"is_builder": True}}
        _post_ability_resource_hook(char, ability, result=True)
        self.assertEqual(char.ndb.domain_resource["current"], 5)

    def test_focus_spender_deducts(self):
        """Focus spender deducts cost from current."""
        from world.ability_engine import _handle_focus_spend
        char = self._focus_char(current=3)
        ability = {"resource_cost": 2, "effect_params": {}}
        ok, msg = _handle_focus_spend(char, ability)
        self.assertTrue(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 1)

    def test_focus_insufficient(self):
        """Spending more Focus than available fails."""
        from world.ability_engine import _handle_focus_spend
        char = self._focus_char(current=1)
        ability = {"resource_cost": 3, "effect_params": {}}
        ok, msg = _handle_focus_spend(char, ability)
        self.assertFalse(ok)
        self.assertIn("Insufficient Focus", msg)

    def test_focus_miss_resets(self):
        """handle_focus_miss resets Focus to 0."""
        from world.ability_engine import handle_focus_miss
        char = self._focus_char(current=4)
        handle_focus_miss(char)
        self.assertEqual(char.ndb.domain_resource["current"], 0)

    def test_focus_skip_turn_resets(self):
        """Skipping turn (no ability used) resets Focus to 0."""
        from world.ability_engine import on_round_end_resources
        char = self._focus_char(current=3)
        char.ndb.ability_used_this_turn = False
        combat_handler = MagicMock()
        on_round_end_resources(char, combat_handler)
        self.assertEqual(char.ndb.domain_resource["current"], 0)


class TestBalanceResource(unittest.TestCase):
    """Balance pendulum: 0=Feral, 100=Calm, 50=start. Shift, not spend."""

    def _balance_char(self, current=50):
        return _mock_character(
            domain_resource={"type": "balance", "current": current, "max": 100},
        )

    def test_balance_shift_toward_feral(self):
        """Negative shift moves toward Feral (0)."""
        from world.ability_engine import _handle_balance_spend
        char = self._balance_char(current=50)
        ability = {"effect_params": {"balance_shift": -20}}
        _handle_balance_spend(char, ability)
        self.assertEqual(char.ndb.domain_resource["current"], 30)

    def test_balance_shift_toward_calm(self):
        """Positive shift moves toward Calm (100)."""
        from world.ability_engine import _handle_balance_spend
        char = self._balance_char(current=50)
        ability = {"effect_params": {"balance_shift": 20}}
        _handle_balance_spend(char, ability)
        self.assertEqual(char.ndb.domain_resource["current"], 70)

    def test_balance_clamp_min(self):
        """Balance cannot go below 0."""
        from world.ability_engine import _handle_balance_spend
        char = self._balance_char(current=10)
        ability = {"effect_params": {"balance_shift": -20}}
        _handle_balance_spend(char, ability)
        self.assertEqual(char.ndb.domain_resource["current"], 0)

    def test_balance_clamp_max(self):
        """Balance cannot go above 100."""
        from world.ability_engine import _handle_balance_spend
        char = self._balance_char(current=90)
        ability = {"effect_params": {"balance_shift": 20}}
        _handle_balance_spend(char, ability)
        self.assertEqual(char.ndb.domain_resource["current"], 100)

    def test_balance_modifier_feral(self):
        """Feral modifier: position 0 = 1.5, position 50 = 1.0, position 100 = 0.5."""
        from world.ability_engine import get_balance_modifier
        # Position 0 (full feral)
        char0 = self._balance_char(current=0)
        self.assertAlmostEqual(get_balance_modifier(char0, "feral"), 1.5)
        # Position 50 (center)
        char50 = self._balance_char(current=50)
        self.assertAlmostEqual(get_balance_modifier(char50, "feral"), 1.0)
        # Position 100 (full calm)
        char100 = self._balance_char(current=100)
        self.assertAlmostEqual(get_balance_modifier(char100, "feral"), 0.5)


class TestResonanceResource(unittest.TestCase):
    """Resonance: builders generate, decay -10/round, spenders cost from pool."""

    def _resonance_char(self, current=0):
        return _mock_character(
            domain_resource={"type": "resonance", "current": current, "max": 100},
        )

    def test_resonance_builder_generates(self):
        """Resonance builder generates resonance_generated amount."""
        from world.ability_engine import _post_ability_resource_hook
        char = self._resonance_char(current=0)
        ability = {"effect_params": {"resonance_generated": 20}}
        _post_ability_resource_hook(char, ability, result=True)
        self.assertEqual(char.ndb.domain_resource["current"], 20)

    def test_decay_resonance(self):
        """decay_resonance subtracts 10, floored at 0."""
        from world.ability_engine import decay_resonance
        char = self._resonance_char(current=30)
        decay_resonance(char)
        self.assertEqual(char.ndb.domain_resource["current"], 20)
        # Decay below 10 floors at 0
        char2 = self._resonance_char(current=5)
        decay_resonance(char2)
        self.assertEqual(char2.ndb.domain_resource["current"], 0)

    def test_resonance_spender_costs(self):
        """Spending resonance deducts from pool."""
        from world.ability_engine import _handle_resonance_spend
        char = self._resonance_char(current=80)
        ability = {"resource_cost": 60, "effect_params": {}}
        ok, msg = _handle_resonance_spend(char, ability)
        self.assertTrue(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 20)


class TestInfluenceResource(unittest.TestCase):
    """Influence: reputation-fueled pool, no in-combat regen."""

    def test_influence_init_from_reputation(self):
        """Influence pool = 20 + reputation * 0.5."""
        from world.ability_engine import initialize_domain_resource
        with patch("world.guild_engine.GUILDS", {"diplomat": {"primary_domain": "diplomacy"}}), \
             patch("world.guild_engine.FINGERPRINTS", {"diplomacy": {"resource_type": "influence"}}), \
             patch("world.world_state.get_dimension_score", return_value=60):
            char = _mock_character(guild_id="diplomat")
            initialize_domain_resource(char)
            self.assertEqual(char.ndb.domain_resource["current"], 50)

    def test_influence_spend_no_regen(self):
        """Spending Influence depletes; no regen hook restores it."""
        from world.ability_engine import spend_domain_resource, on_round_end_resources
        char = _mock_character(
            domain_resource={"type": "influence", "current": 50, "max": 50},
        )
        ok, msg = spend_domain_resource(char, 20)
        self.assertTrue(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 30)
        # on_round_end should NOT restore influence
        combat_handler = MagicMock()
        on_round_end_resources(char, combat_handler)
        self.assertEqual(char.ndb.domain_resource["current"], 30)


class TestMomentumResource(unittest.TestCase):
    """Momentum: builds on hit/damage, resets at encounter end."""

    def _momentum_char(self, current=0):
        return _mock_character(
            domain_resource={"type": "momentum", "current": current, "max": 100},
        )

    def test_momentum_build_on_hit(self):
        """build_momentum_on_damage adds to Momentum pool."""
        from world.ability_engine import build_momentum_on_damage
        char = self._momentum_char(current=20)
        build_momentum_on_damage(char, 10)
        self.assertEqual(char.ndb.domain_resource["current"], 30)

    def test_momentum_cap(self):
        """Momentum cannot exceed max 100."""
        from world.ability_engine import build_momentum_on_damage
        char = self._momentum_char(current=95)
        build_momentum_on_damage(char, 10)
        self.assertEqual(char.ndb.domain_resource["current"], 100)

    def test_momentum_encounter_end_reset(self):
        """Momentum resets to 0 at encounter end."""
        from world.ability_engine import on_encounter_end_resources
        char = self._momentum_char(current=50)
        on_encounter_end_resources(char)
        self.assertEqual(char.ndb.domain_resource["current"], 0)


class TestFiniteResources(unittest.TestCase):
    """Reagents and Components: finite stock, no regeneration."""

    def test_reagents_deplete(self):
        """Spending reagents reduces stock."""
        from world.ability_engine import spend_domain_resource
        char = _mock_character(
            domain_resource={"type": "reagents", "current": 30, "max": 100},
        )
        ok, msg = spend_domain_resource(char, 15)
        self.assertTrue(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 15)

    def test_components_no_regen(self):
        """Components do not regenerate on round end."""
        from world.ability_engine import on_round_end_resources
        char = _mock_character(
            domain_resource={"type": "components", "current": 10, "max": 100},
        )
        combat_handler = MagicMock()
        on_round_end_resources(char, combat_handler)
        self.assertEqual(char.ndb.domain_resource["current"], 10)


class TestCommandResource(unittest.TestCase):
    """Command: builds from ally actions, solo rate 5/round."""

    def test_command_build_with_allies(self):
        """Command builds 10 per ally action."""
        from world.ability_engine import _build_command_from_allies
        char = _mock_character(
            domain_resource={"type": "command", "current": 0, "max": 100},
        )
        combat_handler = MagicMock()
        combat_handler.ndb = SimpleNamespace(
            ally_action_count={str(char.id): 2},
        )
        _build_command_from_allies(char, combat_handler)
        self.assertEqual(char.ndb.domain_resource["current"], 20)

    def test_command_solo_rate(self):
        """Without allies, Command builds at solo rate (5)."""
        from world.ability_engine import _build_command_from_allies
        char = _mock_character(
            domain_resource={"type": "command", "current": 0, "max": 100},
        )
        combat_handler = MagicMock()
        combat_handler.ndb = SimpleNamespace(ally_action_count={})
        _build_command_from_allies(char, combat_handler)
        self.assertEqual(char.ndb.domain_resource["current"], 5)


class TestEchoesResource(unittest.TestCase):
    """Echoes: builds from ability use, investigation bonus persistence."""

    def test_echoes_build_on_ability(self):
        """Ability use builds 5 echoes."""
        from world.ability_engine import _post_ability_resource_hook
        char = _mock_character(
            domain_resource={"type": "echoes", "current": 10, "max": 100},
        )
        ability = {"effect_params": {}}
        _post_ability_resource_hook(char, ability, result=True)
        self.assertEqual(char.ndb.domain_resource["current"], 15)

    def test_echoes_investigation_bonus_init(self):
        """Investigation bonus sets starting echoes."""
        from world.ability_engine import initialize_domain_resource
        with patch("world.guild_engine.GUILDS", {"remnant": {"primary_domain": "remnance"}}), \
             patch("world.guild_engine.FINGERPRINTS", {"remnance": {"resource_type": "echoes"}}):
            char = _mock_character(guild_id="remnant")
            char.db.echoes_investigation_bonus = {"amount": 30, "encounters_remaining": 2}
            initialize_domain_resource(char)
            self.assertEqual(char.ndb.domain_resource["current"], 30)

    def test_echoes_bonus_decrements(self):
        """Encounter end decrements encounters_remaining."""
        from world.ability_engine import on_encounter_end_resources
        char = _mock_character(
            domain_resource={"type": "echoes", "current": 30, "max": 100},
        )
        char.db.echoes_investigation_bonus = {"amount": 30, "encounters_remaining": 2}
        on_encounter_end_resources(char)
        self.assertEqual(char.db.echoes_investigation_bonus["encounters_remaining"], 1)


class TestFocusScaling(unittest.TestCase):
    """consumes_all_focus scaling: different Focus amounts -> different results."""

    def test_consumes_all_focus_clears_pool(self):
        """consumes_all_focus sets Focus to 0 regardless of amount."""
        from world.ability_engine import _post_ability_resource_hook
        # With 5 Focus
        char5 = _mock_character(
            domain_resource={"type": "focus", "current": 5, "max": 5},
        )
        ability = {"effect_params": {"consumes_all_focus": True}}
        _post_ability_resource_hook(char5, ability, result=True)
        self.assertEqual(char5.ndb.domain_resource["current"], 0)
        # With 1 Focus
        char1 = _mock_character(
            domain_resource={"type": "focus", "current": 1, "max": 5},
        )
        _post_ability_resource_hook(char1, ability, result=True)
        self.assertEqual(char1.ndb.domain_resource["current"], 0)

    def test_consumes_all_focus_requires_minimum_one(self):
        """consumes_all_focus with 0 Focus fails pre-check when resource_cost > 0."""
        from world.ability_engine import _handle_focus_spend
        char = _mock_character(
            domain_resource={"type": "focus", "current": 0, "max": 5},
        )
        # consumes_all_focus abilities have resource_cost > 0 in practice
        ability = {"resource_cost": 1, "effect_params": {"consumes_all_focus": True}}
        ok, msg = _handle_focus_spend(char, ability)
        self.assertFalse(ok)
        self.assertIn("No Focus", msg)


class TestAbilityRedundancy(unittest.TestCase):
    """Validate no two same-domain same-tier abilities are identical."""

    def test_no_redundant_abilities_per_domain_tier(self):
        """For each domain+tier, no two abilities have identical (effect_type, effect_params)."""
        import json
        from world.ability_registry import ABILITIES, DOMAIN_ABILITIES
        collisions = []
        for domain, tiers in DOMAIN_ABILITIES.items():
            for tier, ability_ids in tiers.items():
                seen = {}
                for aid in ability_ids:
                    ability = ABILITIES[aid]
                    etype = ability["effect_type"]
                    params = ability.get("effect_params", {})
                    # Use JSON serialization for hashable key (handles nested dicts/lists)
                    param_key = json.dumps(params, sort_keys=True) if isinstance(params, dict) else ""
                    fingerprint = (etype, param_key)
                    if fingerprint in seen:
                        collisions.append(
                            f"{domain} T{tier}: '{aid}' identical to '{seen[fingerprint]}'"
                        )
                    seen[fingerprint] = aid
        self.assertEqual(
            collisions, [],
            f"Redundant abilities found:\n" + "\n".join(collisions),
        )


class TestTypedResourceVariants(unittest.TestCase):
    """Verify all alchemy/engineering abilities have typed resource variant fields."""

    def test_all_alchemy_have_reagent_type(self):
        from world.ability_registry import ABILITIES
        valid_types = {"volatile", "curative", "toxic"}
        for aid, a in ABILITIES.items():
            if a.get("domain") == "alchemy":
                rt = a.get("effect_params", {}).get("reagent_type")
                self.assertIn(rt, valid_types, f"{aid} missing/invalid reagent_type: {rt}")

    def test_all_engineering_have_component_type(self):
        from world.ability_registry import ABILITIES
        valid_types = {"gear", "conduit", "plating"}
        for aid, a in ABILITIES.items():
            if a.get("domain") == "engineering":
                ct = a.get("effect_params", {}).get("component_type")
                self.assertIn(ct, valid_types, f"{aid} missing/invalid component_type: {ct}")

    def test_reagents_handler_reads_variant(self):
        from world.ability_engine import _handle_reagents_spend
        char = _mock_character(domain_resource={"type": "reagents", "current": 50, "max": 100})
        ability = {"resource_cost": 10, "effect_params": {"reagent_type": "volatile"}}
        ok, msg = _handle_reagents_spend(char, ability)
        self.assertTrue(ok)

    def test_components_handler_reads_variant(self):
        from world.ability_engine import _handle_components_spend
        char = _mock_character(domain_resource={"type": "components", "current": 50, "max": 100})
        ability = {"resource_cost": 10, "effect_params": {"component_type": "conduit"}}
        ok, msg = _handle_components_spend(char, ability)
        self.assertTrue(ok)


class TestAbilityRuntimeAlignment(unittest.TestCase):
    @patch("world.models.CharacterAbility")
    def test_silence_blocks_ability_before_spending_resources(self, mock_ca_cls):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        char.ndb.active_effects = [{
            "type": "silence",
            "stacks": 1,
            "duration": 2,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": False,
            "data": {},
        }]

        ok, msg = use_ability(char, "crushing_advance")

        self.assertFalse(ok)
        self.assertIn("silenced", msg.lower())
        self.assertEqual(char.ndb.domain_resource["current"], 100)

    @patch("world.models.CharacterAbility")
    def test_failed_handler_restores_resource_and_skips_cooldown(self, mock_ca_cls):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )

        with patch.dict("world.ability_engine.EFFECT_HANDLERS", {"damage": lambda *_: (False, "Handler failed.")}, clear=False):
            ok, msg = use_ability(char, "crushing_advance")

        self.assertFalse(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 100)
        self.assertEqual(char.ndb.ability_cooldowns, {})

    @patch("world.combat_engine.resolve_ability_damage", return_value=(True, "hit", 25))
    @patch("world.models.CharacterAbility")
    def test_aoe_damage_hits_every_enemy_in_combat(self, mock_ca_cls, mock_resolve):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True

        combat_handler = MagicMock()
        mob_a = MagicMock()
        mob_a.key = "Mob A"
        mob_b = MagicMock()
        mob_b.key = "Mob B"
        mob_c = MagicMock()
        mob_c.key = "Mob C"
        combat_handler.get_mob_combatants.return_value = [mob_a, mob_b, mob_c]

        char = _mock_character(
            domain_resource={"type": "mana", "current": 100, "max": 100},
            combat_handler=combat_handler,
        )
        char.ndb.resolving_charged_ability = True

        ok, msg = use_ability(char, "meteor_strike", target=mob_a)

        self.assertTrue(ok)
        self.assertEqual(mock_resolve.call_count, 3)
        second_params = mock_resolve.call_args_list[1].args[1]["effect_params"]
        self.assertEqual(second_params["damage_base"], 120)

    @patch("world.status_effects.apply_effect", return_value=(True, "Applied"))
    @patch("world.combat_engine.resolve_heal", return_value=(True, "healed", 40))
    @patch("world.group_engine._get_group_members")
    @patch("world.group_engine._get_leader")
    @patch("world.models.CharacterAbility")
    def test_group_heal_targets_all_group_members(
        self,
        mock_ca_cls,
        mock_get_leader,
        mock_get_members,
        mock_resolve_heal,
        mock_apply_effect,
    ):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True

        char = _mock_character(
            domain_resource={"type": "influence", "current": 100, "max": 100},
            group_leader_id=1,
        )
        ally = _mock_character(
            domain_resource={"type": "influence", "current": 100, "max": 100},
            char_id=2,
            key="Ally",
            group_leader_id=1,
            location=char.location,
        )
        mock_get_leader.return_value = char
        mock_get_members.return_value = [char, ally]

        ok, msg = use_ability(char, "wayfinder_heart_of_the_wild", target=ally)

        self.assertTrue(ok)
        self.assertEqual(mock_resolve_heal.call_count, 2)
        self.assertEqual(mock_apply_effect.call_count, 2)


class TestAbilityTruthfulnessSweep(unittest.TestCase):
    @patch("world.ability_engine.random.random", return_value=0.0)
    @patch("world.models.CharacterAbility")
    def test_venom_coat_applies_next_attack_buff_to_self(self, mock_ca_cls, mock_random):
        from world.ability_engine import use_ability
        from world.status_effects import has_effect

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "reagents", "current": 25, "max": 100},
        )

        ok, _ = use_ability(char, "venom_coat")

        self.assertTrue(ok)
        self.assertTrue(has_effect(char, "venom_coat"))

    @patch("world.models.CharacterAbility")
    def test_node_tap_restores_spent_mana(self, mock_ca_cls):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "mana", "current": 70, "max": 100},
        )

        ok, _ = use_ability(char, "spellseeker_node_tap")

        self.assertTrue(ok)
        self.assertEqual(char.ndb.domain_resource["current"], 85)

    @patch("world.models.CharacterAbility")
    def test_echo_mend_applies_regeneration_buff(self, mock_ca_cls):
        from world.ability_engine import use_ability
        from world.status_effects import has_effect

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "resonance", "current": 100, "max": 100},
        )
        char.ndb.hp = 50

        ok, _ = use_ability(char, "echo_mend", target=char)

        self.assertTrue(ok)
        self.assertTrue(has_effect(char, "regeneration"))

    @patch("world.models.CharacterAbility")
    @patch("world.combat_engine.resolve_ability_damage", return_value=(True, "hit", 40))
    def test_construct_summon_creates_lingering_attack_buff(self, mock_resolve, mock_ca_cls):
        from world.ability_engine import use_ability
        from world.status_effects import has_effect

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "echoes", "current": 80, "max": 100},
        )
        target = MagicMock()
        target.id = 999
        target.key = "Target"
        target.db = SimpleNamespace(base_stats=None)
        target.ndb = SimpleNamespace(hp=100, active_effects=[])

        ok, _ = use_ability(char, "dragonwright_ancient_construct", target=target)

        self.assertTrue(ok)
        self.assertTrue(has_effect(char, "sustained_attack"))

    @patch("world.ability_engine.random.random", return_value=0.0)
    @patch("world.models.CharacterAbility")
    @patch("world.status_effects.apply_effect", return_value=(True, "Applied"))
    def test_volatile_mixture_applies_burn_and_poison(self, mock_apply_effect, mock_ca_cls, mock_random):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "mana", "current": 100, "max": 100},
        )
        target = MagicMock()
        target.key = "Target"
        target.db = SimpleNamespace(base_stats=None)
        target.ndb = SimpleNamespace(hp=100, active_effects=[])

        ok, _ = use_ability(char, "fusewright_volatile_mixture", target=target)

        self.assertTrue(ok)
        effect_types = [call.args[1] for call in mock_apply_effect.call_args_list]
        self.assertIn("burn", effect_types)
        self.assertIn("poison", effect_types)

    @patch("world.status_effects.apply_effect", return_value=(True, "Applied"))
    @patch("world.group_engine._get_group_members")
    @patch("world.group_engine._get_leader")
    @patch("world.models.CharacterAbility")
    def test_rally_buffs_scale_with_party_size(
        self,
        mock_ca_cls,
        mock_get_leader,
        mock_get_members,
        mock_apply_effect,
    ):
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        char = _mock_character(
            domain_resource={"type": "influence", "current": 100, "max": 100},
            group_leader_id=1,
        )
        ally = _mock_character(
            domain_resource={"type": "influence", "current": 100, "max": 100},
            char_id=2,
            key="Ally",
            group_leader_id=1,
            location=char.location,
        )
        mock_get_leader.return_value = char
        mock_get_members.return_value = [char, ally]

        ok, _ = use_ability(char, "rally_the_fallen")

        self.assertTrue(ok)
        reduction_calls = [call for call in mock_apply_effect.call_args_list if call.args[1] == "group_damage_reduction"]
        self.assertTrue(reduction_calls)
        self.assertGreater(reduction_calls[0].args[3], 0.15)
