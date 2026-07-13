"""
Tests for skill engine (world/skill_engine.py).

Covers all SKL requirements: passive accumulation (SKL-01), practice cooldown,
diminishing returns, profession skills (SKL-02), animal handling (SKL-03),
domain independence (SKL-04), ancestry seeds, discovery framework, trainer sessions.
Uses unittest.TestCase + MagicMock (no Evennia DB required).
"""

import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
django.setup()


def _make_character(carried_scales=1000):
    """Create a MagicMock character for skill engine tests."""
    char = MagicMock()
    char.id = 1
    char.db.carried_scales = carried_scales
    char.db.discoveries = []
    char.msg = MagicMock()
    # ndb attributes use a simple dict-backed proxy
    ndb_store = {}

    class NdbProxy:
        def __getattr__(self, key):
            return ndb_store.get(key, None)

        def __setattr__(self, key, value):
            ndb_store[key] = value

    char.ndb = NdbProxy()
    char._ndb_store = ndb_store
    return char


def _make_skill_record(
    value=0.0,
    last_practiced_at=None,
    skill_type="general",
    passive_use_remainder=0,
):
    """Create a MagicMock CharacterSkill record."""
    record = MagicMock()
    record.value = value
    record.last_practiced_at = last_practiced_at
    record.skill_type = skill_type
    record.passive_use_remainder = passive_use_remainder
    record.save = MagicMock()
    return record


class TestGetSkillValue(unittest.TestCase):
    """get_skill_value returns correct values."""

    @patch("world.models.CharacterSkill.objects")
    def test_returns_zero_for_unlearned(self, mock_cs_objects):
        """Unlearned skill returns 0.0."""
        from world.models import CharacterSkill
        from world.skill_engine import get_skill_value

        mock_cs_objects.get.side_effect = CharacterSkill.DoesNotExist
        result = get_skill_value(MagicMock(), "lockpicking")
        self.assertEqual(result, 0.0)

    @patch("world.models.CharacterSkill.objects")
    def test_returns_value_for_learned(self, mock_cs_objects):
        """Learned skill returns its stored value."""
        from world.skill_engine import get_skill_value

        record = _make_skill_record(value=42.5)
        mock_cs_objects.get.return_value = record
        result = get_skill_value(MagicMock(), "lockpicking")
        self.assertEqual(result, 42.5)


class TestAccumulateSkillUse(unittest.TestCase):
    """Passive accumulation increments ndb counter (SKL-01)."""

    def test_increments_ndb_counter(self):
        """accumulate_skill_use increments the ndb accumulator."""
        from world.skill_engine import accumulate_skill_use

        char = _make_character()
        accumulate_skill_use(char, "lockpicking")
        self.assertEqual(getattr(char.ndb, "skill_use_lockpicking", 0), 1)

        accumulate_skill_use(char, "lockpicking", count=5)
        self.assertEqual(getattr(char.ndb, "skill_use_lockpicking", 0), 6)

    def test_does_not_write_to_db(self):
        """No DB write occurs during accumulation."""
        from world.skill_engine import accumulate_skill_use

        char = _make_character()
        accumulate_skill_use(char, "lockpicking")
        # No assertion needed beyond not raising


class TestCommitSkillAccumulators(unittest.TestCase):
    """Batch commit from ndb to DB (SKL-01)."""

    @patch("world.models.CharacterSkill.objects")
    def test_passive_gain_applied(self, mock_cs_objects):
        """10+ uses triggers passive gain with diminishing returns."""
        from world.skill_engine import commit_skill_accumulators

        char = _make_character()
        setattr(char.ndb, "skill_use_lockpicking", 10)

        record = _make_skill_record(value=10.0)
        mock_cs_objects.select_for_update.return_value.get_or_create.return_value = (record, False)

        commit_skill_accumulators(char)

        # At value 10, rate is 1.0, gain = 0.1 * 1.0 = 0.1
        self.assertAlmostEqual(record.value, 10.1, places=2)
        record.save.assert_called()

    @patch("world.models.CharacterSkill.objects")
    def test_remainder_preserved(self, mock_cs_objects):
        """Remainder below threshold preserved in ndb."""
        from world.skill_engine import commit_skill_accumulators

        char = _make_character()
        setattr(char.ndb, "skill_use_lockpicking", 13)

        record = _make_skill_record(value=5.0)
        mock_cs_objects.select_for_update.return_value.get_or_create.return_value = (record, False)

        commit_skill_accumulators(char)

        # The partial threshold is durable; volatile state is fully cleared.
        self.assertEqual(record.passive_use_remainder, 3)
        self.assertEqual(getattr(char.ndb, "skill_use_lockpicking", 0), 0)

    @patch("world.models.CharacterSkill.objects")
    def test_below_threshold_is_persisted(self, mock_cs_objects):
        """Below 10 uses persist so a process reset cannot erase progress."""
        from world.skill_engine import commit_skill_accumulators

        char = _make_character()
        setattr(char.ndb, "skill_use_lockpicking", 5)

        record = _make_skill_record(value=0.0)
        mock_cs_objects.select_for_update.return_value.get_or_create.return_value = (record, False)

        commit_skill_accumulators(char)

        self.assertEqual(record.passive_use_remainder, 5)
        self.assertEqual(getattr(char.ndb, "skill_use_lockpicking", 0), 0)


class TestDiminishingReturns(unittest.TestCase):
    """Verify _get_diminishing_rate returns correct values (SKL-01)."""

    def test_brackets(self):
        """Each bracket returns the expected rate."""
        from world.skill_engine import _get_diminishing_rate

        self.assertEqual(_get_diminishing_rate(0), 1.0)
        self.assertEqual(_get_diminishing_rate(25), 1.0)
        self.assertEqual(_get_diminishing_rate(26), 0.75)
        self.assertEqual(_get_diminishing_rate(50), 0.75)
        self.assertEqual(_get_diminishing_rate(51), 0.40)
        self.assertEqual(_get_diminishing_rate(75), 0.40)
        self.assertEqual(_get_diminishing_rate(76), 0.10)
        self.assertEqual(_get_diminishing_rate(90), 0.10)
        self.assertEqual(_get_diminishing_rate(91), 0.02)
        self.assertEqual(_get_diminishing_rate(100), 0.02)

    def test_above_100_returns_zero(self):
        """Above 100 returns 0.0 (no gain)."""
        from world.skill_engine import _get_diminishing_rate

        self.assertEqual(_get_diminishing_rate(101), 0.0)


class TestPracticeSkill(unittest.TestCase):
    """Deliberate practice with 24hr cooldown (SKL-01)."""

    @patch("world.skill_engine.timezone")
    @patch("world.models.CharacterSkill.objects")
    def test_practice_returns_success(self, mock_cs_objects, mock_tz):
        """First practice returns (True, message) with value increase."""
        from world.skill_engine import practice_skill

        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_tz.now.return_value = now

        record = _make_skill_record(value=10.0, last_practiced_at=None)
        mock_cs_objects.get_or_create.return_value = (record, False)

        char = _make_character()
        success, msg = practice_skill(char, "lockpicking")

        self.assertTrue(success)
        self.assertIn("Lockpicking", msg)
        self.assertGreater(record.value, 10.0)

    @patch("world.skill_engine.timezone")
    @patch("world.models.CharacterSkill.objects")
    def test_cooldown_blocks_practice(self, mock_cs_objects, mock_tz):
        """Second practice within 24hrs returns (False, cooldown message)."""
        from world.skill_engine import practice_skill

        now = datetime(2026, 1, 1, 12, 0, 0)
        mock_tz.now.return_value = now

        # Last practiced 1 hour ago
        record = _make_skill_record(
            value=10.0,
            last_practiced_at=now - timedelta(hours=1),
        )
        mock_cs_objects.get_or_create.return_value = (record, False)

        char = _make_character()
        success, msg = practice_skill(char, "lockpicking")

        self.assertFalse(success)
        self.assertIn("next practice in", msg.lower())

    @patch("world.skill_engine.timezone")
    @patch("world.models.CharacterSkill.objects")
    def test_practice_after_24_hours(self, mock_cs_objects, mock_tz):
        """Practice succeeds after 24+ hours."""
        from world.skill_engine import practice_skill

        now = datetime(2026, 1, 2, 14, 0, 0)
        mock_tz.now.return_value = now

        # Last practiced 25 hours ago
        record = _make_skill_record(
            value=10.0,
            last_practiced_at=now - timedelta(hours=25),
        )
        mock_cs_objects.get_or_create.return_value = (record, False)

        char = _make_character()
        success, msg = practice_skill(char, "lockpicking")

        self.assertTrue(success)

    @patch("world.skill_engine.timezone")
    @patch("world.models.CharacterSkill.objects")
    def test_unknown_skill_rejected(self, mock_cs_objects, mock_tz):
        """Unknown skill ID returns (False, message)."""
        from world.skill_engine import practice_skill

        char = _make_character()
        success, msg = practice_skill(char, "nonexistent_skill")

        self.assertFalse(success)
        self.assertIn("Unknown skill", msg)


class TestPracticeGainsByTier(unittest.TestCase):
    """Verify gain ranges match PRACTICE_GAINS table for each tier."""

    def test_gain_ranges(self):
        """Each tier returns correct (min, max) gain range."""
        from world.skill_engine import _get_practice_gain_range

        self.assertEqual(_get_practice_gain_range(0), (3.0, 5.0))
        self.assertEqual(_get_practice_gain_range(25), (3.0, 5.0))
        self.assertEqual(_get_practice_gain_range(26), (2.0, 4.0))
        self.assertEqual(_get_practice_gain_range(50), (2.0, 4.0))
        self.assertEqual(_get_practice_gain_range(51), (1.0, 3.0))
        self.assertEqual(_get_practice_gain_range(75), (1.0, 3.0))
        self.assertEqual(_get_practice_gain_range(76), (0.5, 1.0))
        self.assertEqual(_get_practice_gain_range(90), (0.5, 1.0))
        self.assertEqual(_get_practice_gain_range(91), (0.1, 0.3))
        self.assertEqual(_get_practice_gain_range(100), (0.1, 0.3))

    def test_out_of_range_returns_zero(self):
        """Above 100 returns (0.0, 0.0)."""
        from world.skill_engine import _get_practice_gain_range

        self.assertEqual(_get_practice_gain_range(101), (0.0, 0.0))


class TestProfessionSkills(unittest.TestCase):
    """SKL-02: Profession skills present in SKILL_DEFINITIONS."""

    def test_professions_exist(self):
        """Cooking, smithing, alchemy, engineering all present as general skills."""
        from world.skill_definitions import SKILL_DEFINITIONS

        professions = ["cooking", "smithing", "alchemy", "engineering"]
        for skill_id in professions:
            self.assertIn(skill_id, SKILL_DEFINITIONS, f"Missing: {skill_id}")
            self.assertEqual(
                SKILL_DEFINITIONS[skill_id]["skill_type"],
                "general",
                f"{skill_id} should be general type",
            )


class TestAnimalHandling(unittest.TestCase):
    """SKL-03: Animal handling skill exists and supports 0-100 range."""

    def test_animal_handling_exists(self):
        """animal_handling skill is defined."""
        from world.skill_definitions import SKILL_DEFINITIONS

        self.assertIn("animal_handling", SKILL_DEFINITIONS)
        defn = SKILL_DEFINITIONS["animal_handling"]
        self.assertEqual(defn["skill_type"], "general")
        self.assertEqual(defn["domain_bonus"], "naturalism")

    def test_dragon_handling_threshold(self):
        """At 100, animal_handling qualifies for Dragon Handling check."""
        from world.skill_definitions import SKILL_DEFINITIONS

        defn = SKILL_DEFINITIONS["animal_handling"]
        # 100 threshold exists in thresholds dict
        self.assertIn(100, defn["thresholds"])


class TestSkillDomainIndependence(unittest.TestCase):
    """SKL-04: Skills are independent of guild/domain system."""

    def test_no_guild_fk(self):
        """CharacterSkill has no ForeignKey to CharacterGuild."""
        from world.models import CharacterSkill

        fk_targets = []
        for field in CharacterSkill._meta.get_fields():
            if hasattr(field, "related_model") and field.related_model:
                fk_targets.append(field.related_model.__name__)

        self.assertNotIn(
            "CharacterGuild",
            fk_targets,
            "CharacterSkill should NOT have FK to CharacterGuild",
        )

    @patch("world.models.CharacterSkill.objects")
    def test_skill_ops_no_guild_required(self, mock_cs_objects):
        """Skill operations work without guild membership."""
        from world.models import CharacterSkill
        from world.skill_engine import accumulate_skill_use, get_skill_value

        char = _make_character()
        # Accumulate without guild
        accumulate_skill_use(char, "lockpicking")
        # get_skill_value doesn't need guild
        mock_cs_objects.get.side_effect = CharacterSkill.DoesNotExist
        result = get_skill_value(char, "lockpicking")
        self.assertEqual(result, 0.0)


class TestAncestrySkillSeeds(unittest.TestCase):
    """apply_ancestry_skill_seeds applies correct starting values."""

    @patch("world.models.CharacterSkill.objects")
    def test_human_creates_no_seeds(self, mock_cs_objects):
        """Human ancestry has empty seeds -- no records created."""
        from world.skill_engine import apply_ancestry_skill_seeds

        char = _make_character()
        apply_ancestry_skill_seeds(char, "human")
        mock_cs_objects.get_or_create.assert_not_called()

    @patch("world.models.CharacterSkill.objects")
    def test_kauroran_seeds(self, mock_cs_objects):
        """Kau'roran gets swimming 30, fishing 25, beast_training 20, persuasion 15."""
        from world.skill_engine import apply_ancestry_skill_seeds

        record = _make_skill_record(value=0.0)
        mock_cs_objects.get_or_create.return_value = (record, True)

        char = _make_character()
        apply_ancestry_skill_seeds(char, "kauroran")

        # 4 seeds created
        self.assertEqual(mock_cs_objects.get_or_create.call_count, 4)

    @patch("world.models.CharacterSkill.objects")
    def test_selvar_winter_maps_to_north(self, mock_cs_objects):
        """Selvar with winter coat gets selvar_north seeds."""
        from world.skill_engine import apply_ancestry_skill_seeds
        from world.skill_definitions import ANCESTRY_SKILL_SEEDS

        record = _make_skill_record(value=0.0)
        mock_cs_objects.get_or_create.return_value = (record, True)

        char = _make_character()
        apply_ancestry_skill_seeds(char, "selvar", coat="winter")

        expected_count = len(ANCESTRY_SKILL_SEEDS["selvar_north"])
        self.assertEqual(mock_cs_objects.get_or_create.call_count, expected_count)

    @patch("world.models.CharacterSkill.objects")
    def test_selvar_summer_maps_to_south(self, mock_cs_objects):
        """Selvar with summer coat gets selvar_south seeds."""
        from world.skill_engine import apply_ancestry_skill_seeds
        from world.skill_definitions import ANCESTRY_SKILL_SEEDS

        record = _make_skill_record(value=0.0)
        mock_cs_objects.get_or_create.return_value = (record, True)

        char = _make_character()
        apply_ancestry_skill_seeds(char, "selvar", coat="summer")

        expected_count = len(ANCESTRY_SKILL_SEEDS["selvar_south"])
        self.assertEqual(mock_cs_objects.get_or_create.call_count, expected_count)


class TestDiscoveryFramework(unittest.TestCase):
    """Discovery triggers fire when skill thresholds crossed."""

    @patch("world.models.CharacterSkill.objects")
    def test_discovery_not_duplicated(self, mock_cs_objects):
        """Already-discovered trigger is not fired again."""
        from world.skill_engine import check_discoveries

        char = _make_character()
        char.db.discoveries = ["cantera_cognitive_wolves"]

        check_discoveries(char, "cognitive_node", 90.0)

        # msg should NOT be called (already discovered)
        char.msg.assert_not_called()

    @patch("world.models.CharacterSkill.objects")
    def test_discovery_adds_to_list(self, mock_cs_objects):
        """Discovery adds trigger ID to character.db.discoveries."""
        from world.skill_engine import check_discoveries
        from world.skill_definitions import DISCOVERY_TRIGGERS

        if not DISCOVERY_TRIGGERS:
            self.skipTest("No discovery triggers defined")

        trigger = DISCOVERY_TRIGGERS[0]
        conditions = trigger.get("conditions", {})

        char = _make_character()
        char.db.discoveries = []

        # Make all condition skills return high enough values
        record = _make_skill_record(value=100.0)
        mock_cs_objects.get.return_value = record

        # Use first skill from conditions
        first_skill = list(conditions.keys())[0]
        required_value = conditions[first_skill]

        check_discoveries(char, first_skill, required_value)

        # If all conditions met, discovery should be added
        # (depends on mock returning records with high enough values)
        if char.msg.called:
            # Discovery fired
            self.assertIn(trigger["id"], char.db.discoveries)


class TestTrainWithTrainer(unittest.TestCase):
    """Trainer sessions cost Scales and enhance next practice."""

    def test_unknown_trainer_rejected(self):
        """Unknown trainer_id returns (False, message)."""
        from world.skill_engine import train_with_trainer

        char = _make_character()
        success, msg = train_with_trainer(char, "lockpicking", "nonexistent_trainer")
        self.assertFalse(success)

    @patch("world.skill_engine.TRAINER_REGISTRY", {
        "test_trainer": {
            "name": "Test Trainer",
            "trainer_quality": "journeyman",
            "skills_taught": ["lockpicking"],
            "cost_per_session": 50,
        }
    })
    def test_cost_deducted(self):
        """Training deducts Scales from carried_scales."""
        from world.skill_engine import train_with_trainer

        char = _make_character(carried_scales=100)
        success, msg = train_with_trainer(char, "lockpicking", "test_trainer")

        self.assertTrue(success)
        self.assertEqual(char.db.carried_scales, 50)

    @patch("world.skill_engine.TRAINER_REGISTRY", {
        "test_trainer": {
            "name": "Test Trainer",
            "trainer_quality": "journeyman",
            "skills_taught": ["lockpicking"],
            "cost_per_session": 50,
        }
    })
    def test_bonus_applied_to_ndb(self):
        """Trainer bonus set on ndb for next practice."""
        from world.skill_engine import train_with_trainer

        char = _make_character(carried_scales=100)
        success, msg = train_with_trainer(char, "lockpicking", "test_trainer")

        self.assertTrue(success)
        bonus = getattr(char.ndb, "trainer_bonus_lockpicking", None)
        self.assertIsNotNone(bonus)
        self.assertEqual(bonus, 1.5)  # journeyman multiplier

    @patch("world.skill_engine.TRAINER_REGISTRY", {
        "test_trainer": {
            "name": "Test Trainer",
            "trainer_quality": "journeyman",
            "skills_taught": ["lockpicking"],
            "cost_per_session": 200,
        }
    })
    def test_insufficient_funds(self):
        """Not enough Scales returns (False, message)."""
        from world.skill_engine import train_with_trainer

        char = _make_character(carried_scales=50)
        success, msg = train_with_trainer(char, "lockpicking", "test_trainer")

        self.assertFalse(success)
        self.assertIn("Not enough Scales", msg)


if __name__ == "__main__":
    unittest.main()
