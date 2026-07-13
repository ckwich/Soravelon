"""
Tests for world/guild_engine.py.
Covers DOM-02 (GTS computation), DOM-03 (guild eligibility),
DOM-04 (tier labels), DOM-05 (fingerprint registries).

Pure computation tests use unittest.TestCase + MagicMock (no DB).
Model mutation tests use EvenniaTest (needs DB).
"""
import unittest
from unittest.mock import MagicMock

from world.guild_engine import (
    FINGERPRINTS,
    GUILDS,
    SUBCLASSES,
    GUILD_TIER_LABELS,
    DOMAIN_PROFICIENCY_LABELS,
    GTS_TIER_THRESHOLDS,
    GUILD_ELIGIBILITY_THRESHOLD,
    _DOMAIN_TO_GUILD,
    _DOMAIN_PAIR_TO_SUBCLASS,
    calculate_guild_tier_score,
    get_guild_tier,
    get_guild_tier_label,
    get_domain_proficiency_label,
    check_guild_eligibility,
    join_guild,
    complete_induction,
)
from world.world_state import ALL_DOMAINS


# ---------------------------------------------------------------------------
# Helper: mock character for pure computation tests
# ---------------------------------------------------------------------------

def _mock_character(domain_scores=None, primary_domain=None,
                    secondary_domain=None, guild_id=None,
                    subclass_id=None):
    """Create a MagicMock character with db attributes for guild engine tests."""
    char = MagicMock()
    char.db.domain_scores = domain_scores or {}
    char.db.primary_domain = primary_domain
    char.db.secondary_domain = secondary_domain
    char.db.guild_id = guild_id
    char.db.subclass_id = subclass_id
    return char


# ===========================================================================
# DOM-05: Registry validation tests
# ===========================================================================


class TestFingerprintCount(unittest.TestCase):
    """FINGERPRINTS must have exactly 10 entries, one per domain."""

    def test_count(self):
        self.assertEqual(len(FINGERPRINTS), 10)

    def test_covers_all_domains(self):
        self.assertEqual(set(FINGERPRINTS.keys()), set(ALL_DOMAINS))


class TestFingerprintVerbsDistinct(unittest.TestCase):
    """All 10 fingerprint verbs must be unique."""

    def test_distinct_verbs(self):
        verbs = [fp["verb"] for fp in FINGERPRINTS.values()]
        self.assertEqual(len(verbs), len(set(verbs)))


class TestFingerprintStructure(unittest.TestCase):
    """Each fingerprint must have verb, resource, resource_type, description."""

    def test_required_keys(self):
        for domain, fp in FINGERPRINTS.items():
            for key in ("verb", "resource", "resource_type", "description"):
                self.assertIn(key, fp, f"{domain} missing {key}")


class TestGuildCount(unittest.TestCase):
    """GUILDS must have exactly 10 entries, one per domain."""

    def test_count(self):
        self.assertEqual(len(GUILDS), 10)


class TestGuildStructure(unittest.TestCase):
    """Each guild must have required fields."""

    def test_required_keys(self):
        for guild_id, guild in GUILDS.items():
            for key in ("name", "primary_domain", "hidden", "resource_type"):
                self.assertIn(key, guild, f"{guild_id} missing {key}")


class TestVaelbornHidden(unittest.TestCase):
    """Vaelborn guild must have hidden=True."""

    def test_hidden(self):
        self.assertTrue(GUILDS["vaelborn"]["hidden"])

    def test_others_not_hidden(self):
        for gid, guild in GUILDS.items():
            if gid != "vaelborn":
                self.assertFalse(guild["hidden"], f"{gid} should not be hidden")


class TestSubclassCount90(unittest.TestCase):
    """SUBCLASSES must have exactly 90 entries."""

    def test_count(self):
        self.assertEqual(len(SUBCLASSES), 90)


class TestSubclassValidGuild(unittest.TestCase):
    """Every subclass must reference a valid guild_id."""

    def test_valid_guilds(self):
        for sc_id, sc in SUBCLASSES.items():
            self.assertIn(sc["guild_id"], GUILDS, f"{sc_id} has invalid guild")


class TestSubclassValidDomains(unittest.TestCase):
    """Every subclass must have primary and secondary domains in ALL_DOMAINS."""

    def test_valid_domains(self):
        for sc_id, sc in SUBCLASSES.items():
            self.assertIn(sc["primary_domain"], ALL_DOMAINS,
                          f"{sc_id} invalid primary")
            self.assertIn(sc["secondary_domain"], ALL_DOMAINS,
                          f"{sc_id} invalid secondary")


class TestSubclassNoSelfPair(unittest.TestCase):
    """No subclass may have primary_domain == secondary_domain."""

    def test_no_self_pairs(self):
        for sc_id, sc in SUBCLASSES.items():
            self.assertNotEqual(
                sc["primary_domain"], sc["secondary_domain"],
                f"{sc_id} has same primary and secondary domain"
            )


class TestDomainPairLookupCount(unittest.TestCase):
    """_DOMAIN_PAIR_TO_SUBCLASS must have 90 unique entries."""

    def test_count(self):
        self.assertEqual(len(_DOMAIN_PAIR_TO_SUBCLASS), 90)


class TestDomainToGuildComplete(unittest.TestCase):
    """_DOMAIN_TO_GUILD must cover all 10 domains."""

    def test_complete(self):
        self.assertEqual(set(_DOMAIN_TO_GUILD.keys()), set(ALL_DOMAINS))


# ===========================================================================
# DOM-02: GTS computation tests
# ===========================================================================


class TestGTSNoPrimaryReturnsZero(unittest.TestCase):
    """GTS must be 0.0 when character has no primary domain."""

    def test_no_primary(self):
        char = _mock_character()
        self.assertEqual(calculate_guild_tier_score(char), 0.0)


class TestGTSBothMax(unittest.TestCase):
    """GTS at primary=100, secondary=100 must return 99.0."""

    def test_max(self):
        char = _mock_character(
            domain_scores={"combat": 100, "subterfuge": 100},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertAlmostEqual(calculate_guild_tier_score(char), 99.0)


class TestGTSPrimaryOnly(unittest.TestCase):
    """GTS at primary=100, secondary=0 must return 66.0."""

    def test_primary_only(self):
        char = _mock_character(
            domain_scores={"combat": 100},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertAlmostEqual(calculate_guild_tier_score(char), 66.0)


class TestGTSSecondaryOnly(unittest.TestCase):
    """GTS at primary=0, secondary=100 must return 33.0."""

    def test_secondary_only(self):
        char = _mock_character(
            domain_scores={"subterfuge": 100},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertAlmostEqual(calculate_guild_tier_score(char), 33.0)


class TestGTSMixed(unittest.TestCase):
    """GTS at primary=50, secondary=30 must return 42.9."""

    def test_mixed(self):
        char = _mock_character(
            domain_scores={"combat": 50, "subterfuge": 30},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertAlmostEqual(calculate_guild_tier_score(char), 42.9)


class TestGTSAtThreshold30(unittest.TestCase):
    """GTS at primary=30, secondary=0 must return 19.8 (tier 1)."""

    def test_threshold_30(self):
        char = _mock_character(
            domain_scores={"combat": 30},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertAlmostEqual(calculate_guild_tier_score(char), 19.8)


class TestGTSAtThreshold31(unittest.TestCase):
    """GTS at primary=31, secondary=0 must return 20.46 (tier 2)."""

    def test_threshold_31(self):
        char = _mock_character(
            domain_scores={"combat": 31},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertAlmostEqual(calculate_guild_tier_score(char), 20.46)


# ===========================================================================
# DOM-02 / DOM-04: Tier computation tests
# ===========================================================================


class TestTierAtGTS0(unittest.TestCase):
    """GTS 0.0 maps to tier 1."""

    def test_tier(self):
        char = _mock_character()
        self.assertEqual(get_guild_tier(char), 1)


class TestTierAtGTS19_8(unittest.TestCase):
    """GTS 19.8 maps to tier 1 (below 20 threshold)."""

    def test_tier(self):
        char = _mock_character(
            domain_scores={"combat": 30},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertEqual(get_guild_tier(char), 1)


class TestTierBoundary20(unittest.TestCase):
    """GTS exactly 20.0 maps to tier 2."""

    def test_tier(self):
        # Need primary * 0.66 + secondary * 0.33 = 20.0
        # primary ~ 30.303, let's use 31 + some secondary
        # 31 * 0.66 = 20.46 -> tier 2
        char = _mock_character(
            domain_scores={"combat": 31},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        gts = calculate_guild_tier_score(char)
        self.assertGreaterEqual(gts, 20.0)
        self.assertEqual(get_guild_tier(char), 2)


class TestTierBoundary50(unittest.TestCase):
    """GTS at 50+ maps to tier 3."""

    def test_tier(self):
        # 76 * 0.66 = 50.16
        char = _mock_character(
            domain_scores={"combat": 76},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        gts = calculate_guild_tier_score(char)
        self.assertGreaterEqual(gts, 50.0)
        self.assertEqual(get_guild_tier(char), 3)


class TestTierBoundary85(unittest.TestCase):
    """GTS at 85+ maps to tier 4."""

    def test_tier(self):
        # 100 * 0.66 + 58 * 0.33 = 66 + 19.14 = 85.14
        char = _mock_character(
            domain_scores={"combat": 100, "subterfuge": 58},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        gts = calculate_guild_tier_score(char)
        self.assertGreaterEqual(gts, 85.0)
        self.assertEqual(get_guild_tier(char), 4)


class TestTierAtMax99(unittest.TestCase):
    """GTS 99.0 maps to tier 4."""

    def test_tier(self):
        char = _mock_character(
            domain_scores={"combat": 100, "subterfuge": 100},
            primary_domain="combat",
            secondary_domain="subterfuge",
        )
        self.assertEqual(get_guild_tier(char), 4)


# ===========================================================================
# DOM-04: Tier label tests
# ===========================================================================


class TestTierLabelNoGuild(unittest.TestCase):
    """Character with no guild gets 'Wanderer' label."""

    def test_wanderer(self):
        char = _mock_character()
        self.assertEqual(get_guild_tier_label(char), "Wanderer")


class TestTierLabelIronbloodTier1(unittest.TestCase):
    """Ironblood tier 1 label is 'Scrapper'."""

    def test_label(self):
        char = _mock_character(
            domain_scores={"combat": 10},
            primary_domain="combat",
            secondary_domain="subterfuge",
            guild_id="ironblood",
        )
        self.assertEqual(get_guild_tier_label(char), "Scrapper")


class TestTierLabelIronbloodTier4(unittest.TestCase):
    """Ironblood tier 4 label is 'Bloodsworn'."""

    def test_label(self):
        char = _mock_character(
            domain_scores={"combat": 100, "subterfuge": 100},
            primary_domain="combat",
            secondary_domain="subterfuge",
            guild_id="ironblood",
        )
        self.assertEqual(get_guild_tier_label(char), "Bloodsworn")


class TestTierLabelVaelbornTier1(unittest.TestCase):
    """Vaelborn tier 1 label is empty string."""

    def test_label(self):
        char = _mock_character(
            domain_scores={"remnance": 10},
            primary_domain="remnance",
            secondary_domain="combat",
            guild_id="vaelborn",
        )
        self.assertEqual(get_guild_tier_label(char), "")


class TestTierLabelVaelbornTier4(unittest.TestCase):
    """Vaelborn tier 4 label is 'The Unbroken'."""

    def test_label(self):
        char = _mock_character(
            domain_scores={"remnance": 100, "combat": 100},
            primary_domain="remnance",
            secondary_domain="combat",
            guild_id="vaelborn",
        )
        self.assertEqual(get_guild_tier_label(char), "The Unbroken")


class TestGuildTierLabelsComplete(unittest.TestCase):
    """Every guild has exactly 4 tier labels."""

    def test_four_labels_per_guild(self):
        for guild_id in GUILDS:
            labels = GUILD_TIER_LABELS.get(guild_id)
            self.assertIsNotNone(labels, f"{guild_id} missing tier labels")
            self.assertEqual(len(labels), 4, f"{guild_id} has {len(labels)} labels")


# ===========================================================================
# DOM-03: Guild eligibility tests
# ===========================================================================


class TestEligibilityNoScores(unittest.TestCase):
    """Character with no domain scores is eligible for nothing."""

    def test_empty(self):
        char = _mock_character()
        self.assertEqual(check_guild_eligibility(char), [])


class TestEligibilityBelow30(unittest.TestCase):
    """Combat at 29 does not qualify for ironblood."""

    def test_below_threshold(self):
        char = _mock_character(domain_scores={"combat": 29})
        self.assertEqual(check_guild_eligibility(char), [])


class TestEligibilityAt30(unittest.TestCase):
    """Combat at 30 qualifies for ironblood."""

    def test_at_threshold(self):
        char = _mock_character(domain_scores={"combat": 30})
        result = check_guild_eligibility(char)
        self.assertIn("ironblood", result)


class TestEligibilityMultiple(unittest.TestCase):
    """Multiple domains at 30+ returns multiple guilds."""

    def test_multiple(self):
        char = _mock_character(domain_scores={"combat": 30, "subterfuge": 30})
        result = check_guild_eligibility(char)
        self.assertIn("ironblood", result)
        self.assertIn("veilcraft", result)


class TestEligibilityAlreadyInGuild(unittest.TestCase):
    """Character already in a guild gets empty list."""

    def test_already_in_guild(self):
        char = _mock_character(
            domain_scores={"combat": 50},
            guild_id="ironblood",
        )
        self.assertEqual(check_guild_eligibility(char), [])


# ===========================================================================
# Domain proficiency label tests
# ===========================================================================


class TestProficiencyLabelZero(unittest.TestCase):
    """Score 0 maps to 'Unaware'."""

    def test_zero(self):
        self.assertEqual(get_domain_proficiency_label(0), "Unaware")


class TestProficiencyLabel30(unittest.TestCase):
    """Score 30 maps to 'Practiced'."""

    def test_practiced(self):
        self.assertEqual(get_domain_proficiency_label(30), "Practiced")


class TestProficiencyLabel100(unittest.TestCase):
    """Score 100 maps to 'Transcendent'."""

    def test_transcendent(self):
        self.assertEqual(get_domain_proficiency_label(100), "Transcendent")


# ===========================================================================
# Model mutation tests (require EvenniaTest for DB)
# ===========================================================================

from evennia.utils.test_resources import EvenniaTest
from world.models import CharacterAbility
from world.models import CharacterGuild


class TestLegacyRemoteGuildMutationBlocked(EvenniaTest):
    """Retired mutation helpers cannot bypass authored recruitment."""

    def test_join_valid_guild(self):
        self.char1.db.domain_scores = {"combat": 50, "subterfuge": 30}
        self.char1.db.guild_id = None
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.subclass_id = None

        success, msg = join_guild(self.char1, "ironblood", "subterfuge")
        self.assertFalse(success)
        self.assertIn("in-person induction", msg)
        self.assertIsNone(self.char1.db.guild_id)
        self.assertFalse(CharacterGuild.objects.filter(character=self.char1).exists())

    def test_join_guild_grants_tier_one_domain_abilities(self):
        self.char1.db.ancestry = "human"
        self.char1.db.domain_scores = {"combat": 30, "subterfuge": 0}
        self.char1.db.guild_id = None
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.subclass_id = None

        success, _ = join_guild(self.char1, "ironblood", "subterfuge")
        self.assertFalse(success)

        known = set(
            CharacterAbility.objects.filter(character=self.char1).values_list("ability_id", flat=True)
        )
        self.assertNotIn("second_wind", known)
        self.assertNotIn("crushing_advance", known)
        self.assertNotIn("iron_resolve", known)
        self.assertNotIn("rending_strike", known)

    def test_join_guild_grants_new_tier_unlocks_when_gts_is_high_enough(self):
        self.char1.db.ancestry = "human"
        self.char1.db.domain_scores = {"combat": 80, "subterfuge": 30}
        self.char1.db.guild_id = None
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.subclass_id = None

        success, _ = join_guild(self.char1, "ironblood", "subterfuge")
        self.assertFalse(success)

        known = set(
            CharacterAbility.objects.filter(character=self.char1).values_list("ability_id", flat=True)
        )
        self.assertNotIn("rending_strike", known)
        self.assertNotIn("duskblade_shadow_strike", known)
        self.assertNotIn("duskblade_vanishing_edge", known)


class TestJoinGuildInvalidGuild(EvenniaTest):
    """Invalid guild_id returns failure."""

    def test_invalid_guild(self):
        self.char1.db.guild_id = None
        success, msg = join_guild(self.char1, "bad_guild", "subterfuge")
        self.assertFalse(success)
        self.assertIn("durable invitation", msg)


class TestJoinGuildInvalidDomainPair(EvenniaTest):
    """Invalid domain pair (no subclass) returns failure."""

    def test_invalid_pair(self):
        self.char1.db.guild_id = None
        # combat + combat would be a self-pair with no subclass
        success, msg = join_guild(self.char1, "ironblood", "combat")
        self.assertFalse(success)
        self.assertIn("in-person induction", msg)


class TestJoinGuildAlreadyMember(EvenniaTest):
    """Already in a guild returns failure."""

    def test_already_member(self):
        self.char1.db.guild_id = "ironblood"
        success, msg = join_guild(self.char1, "veilcraft", "combat")
        self.assertFalse(success)
        self.assertIn("Already a member", msg)


class TestCompleteInductionValid(EvenniaTest):
    """Detached induction helper is retired."""

    def test_complete(self):
        self.char1.db.guild_id = None
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.subclass_id = None

        success, msg = complete_induction(self.char1)
        self.assertFalse(success)
        self.assertIn("in person", msg)
        self.assertFalse(CharacterGuild.objects.filter(character=self.char1).exists())


class TestCompleteInductionNoGuild(EvenniaTest):
    """No guild membership returns failure."""

    def test_no_guild(self):
        self.char1.db.guild_id = None
        success, msg = complete_induction(self.char1)
        self.assertFalse(success)
        self.assertIn("in person", msg)
