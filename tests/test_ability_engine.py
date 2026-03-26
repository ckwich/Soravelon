"""
Tests for world/ability_registry.py and world/ability_engine.py.

Covers ABL-01 (registry structure), ABL-02 (dispatch routing),
ABL-03 (tier gating via CharacterAbility), ABL-05 (cooldowns),
ABL-06 (resource management).

Uses unittest.TestCase + MagicMock -- pure logic with mocked ORM.
"""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

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
):
    """Create a MagicMock character with ndb/db for ability engine tests."""
    char = MagicMock()
    char.ndb = SimpleNamespace(
        ability_cooldowns=ability_cooldowns if ability_cooldowns is not None else {},
        domain_resource=domain_resource,
        ancestry_ability_used=ancestry_ability_used,
    )
    char.db = SimpleNamespace(guild_id=guild_id)
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
        result = get_ability("momentum_strike")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "Momentum Strike")

    def test_get_ability_unknown_returns_none(self):
        """get_ability returns None for unknown ability_id."""
        self.assertIsNone(get_ability("fake_ability"))

    def test_ability_tiers_thresholds(self):
        """ABILITY_TIERS has 4 entries with correct GTS thresholds."""
        self.assertEqual(len(ABILITY_TIERS), 4)
        self.assertEqual(ABILITY_TIERS[1], 0)
        self.assertEqual(ABILITY_TIERS[4], 85)


# ===========================================================================
# ABL-02: use_ability dispatch routing
# ===========================================================================


class TestUseAbilityDispatch(unittest.TestCase):
    """use_ability dispatches to correct effect handler."""

    @patch("world.models.CharacterAbility")
    def test_dispatches_damage(self, mock_ca_cls):
        """use_ability for momentum_strike returns success with ability name."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True

        char = _mock_character(
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        target = MagicMock()
        target.key = "Goblin"

        ok, msg = use_ability(char, "momentum_strike", target=target)

        self.assertTrue(ok)
        self.assertIn("Momentum Strike", msg)

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
        ok, msg = use_ability(char, "momentum_strike")

        self.assertFalse(ok)
        self.assertIn("not unlocked", msg.lower())


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
            ability_cooldowns={"momentum_strike": 3},
            domain_resource={"type": "momentum", "current": 100, "max": 100},
        )
        ok, msg = use_ability(char, "momentum_strike")

        self.assertFalse(ok)
        self.assertIn("cooldown", msg.lower())
        self.assertIn("3", msg)

    @patch("world.models.CharacterAbility")
    def test_cooldown_set_after_use(self, mock_ca_cls):
        """Using an ability with cooldown sets ndb.ability_cooldowns."""
        from world.ability_engine import use_ability

        mock_ca_cls.objects.filter.return_value.exists.return_value = True
        mock_ca_cls.objects.filter.return_value.update.return_value = 1

        char = _mock_character(
            domain_resource={"type": "focus", "current": 100, "max": 100},
        )
        # shadow_read has cooldown=2
        ok, msg = use_ability(char, "shadow_read")

        self.assertTrue(ok)
        self.assertEqual(char.ndb.ability_cooldowns["shadow_read"], 2)

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
        "combat": {"resource": "momentum", "resource_type": "combat_resource"},
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
        ok, msg = use_ability(char, "bladestorm_sig1")

        self.assertFalse(ok)
        self.assertIn("not unlocked", msg.lower())
