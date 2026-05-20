import ast
from pathlib import Path
import unittest


class TestPrimarySkillAffordances(unittest.TestCase):
    def test_every_skill_has_a_primary_affordance(self):
        from world.skill_affordances import PRIMARY_SKILL_AFFORDANCES
        from world.skill_definitions import SKILL_DEFINITIONS

        self.assertEqual(
            set(PRIMARY_SKILL_AFFORDANCES),
            set(SKILL_DEFINITIONS),
        )

    def test_affordance_entries_have_player_useful_contract_fields(self):
        from world.skill_affordances import PRIMARY_SKILL_AFFORDANCES

        required = {
            "primary_verb",
            "system",
            "repeatability",
            "anti_farming_gate",
            "implementation_status",
        }
        allowed_statuses = {"live", "planned", "planned_companions"}

        for skill_id, affordance in PRIMARY_SKILL_AFFORDANCES.items():
            with self.subTest(skill_id=skill_id):
                self.assertEqual(set(affordance), required)
                for field in required:
                    self.assertTrue(str(affordance[field]).strip(), field)
                self.assertIn(affordance["implementation_status"], allowed_statuses)

    def test_known_live_affordances_match_runtime_commands(self):
        from world.crafting_definitions import SKILL_TO_COMMAND
        from world.skill_affordances import PRIMARY_SKILL_AFFORDANCES
        from world.weapon_skills import WEAPON_SKILL_DEFINITIONS

        for skill_id, command in SKILL_TO_COMMAND.items():
            with self.subTest(skill_id=skill_id):
                affordance = PRIMARY_SKILL_AFFORDANCES[skill_id]
                self.assertEqual(affordance["primary_verb"], command)
                self.assertEqual(affordance["implementation_status"], "live")

        expected_live_verbs = {
            "appraisal": "inspect",
            "fishing": "fish",
            "foraging": "forage",
            "herbalism": "harvest",
            "investigation": "search",
            "mining": "mine",
            "skinning": "butcher",
            "woodcutting": "chop",
        }
        for skill_id, verb in expected_live_verbs.items():
            with self.subTest(skill_id=skill_id):
                affordance = PRIMARY_SKILL_AFFORDANCES[skill_id]
                self.assertEqual(affordance["primary_verb"], verb)
                self.assertEqual(affordance["implementation_status"], "live")

        for skill_id in WEAPON_SKILL_DEFINITIONS:
            with self.subTest(skill_id=skill_id):
                affordance = PRIMARY_SKILL_AFFORDANCES[skill_id]
                self.assertEqual(affordance["primary_verb"], "attack")
                self.assertEqual(affordance["implementation_status"], "live")


def _literal_dicts_from_area_files():
    areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
    for path in sorted(areas_dir.glob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            try:
                value = ast.literal_eval(node)
            except (ValueError, SyntaxError):
                continue
            if isinstance(value, dict):
                yield path, value


def _literal_keyword_values_from_area_files(keyword_name):
    areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
    for path in sorted(areas_dir.glob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for keyword in node.keywords:
                if keyword.arg != keyword_name:
                    continue
                try:
                    value = ast.literal_eval(keyword.value)
                except (ValueError, SyntaxError):
                    continue
                yield path, value


def _practice_opportunity_calls_from_area_files():
    areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
    for path in sorted(areas_dir.glob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "practice_opportunity":
                continue
            if not node.args:
                continue
            try:
                opportunity_id = ast.literal_eval(node.args[0])
            except (ValueError, SyntaxError):
                continue
            kwargs = {}
            for keyword in node.keywords:
                try:
                    kwargs[keyword.arg] = ast.literal_eval(keyword.value)
                except (ValueError, SyntaxError):
                    kwargs[keyword.arg] = keyword.value
            yield path, opportunity_id, kwargs


class TestAreaAuthoredSkillReferences(unittest.TestCase):
    def test_area_skill_xp_rewards_reference_defined_skills(self):
        from world.skill_definitions import SKILL_DEFINITIONS

        seen = []
        for path, value in _literal_dicts_from_area_files():
            if value.get("action_type") != "give_skill_xp":
                continue
            skill_id = value.get("skill_id")
            seen.append((path, skill_id))
            with self.subTest(path=path.name, skill_id=skill_id):
                self.assertIn(skill_id, SKILL_DEFINITIONS)

        self.assertTrue(seen, "Expected at least one authored give_skill_xp reward.")

    def test_material_profession_bonuses_reference_defined_skills(self):
        from world.skill_definitions import SKILL_DEFINITIONS

        seen = []
        for path, bonuses in _literal_keyword_values_from_area_files("profession_bonus"):
            if not isinstance(bonuses, dict):
                continue
            for skill_id in bonuses:
                seen.append((path, skill_id))
                with self.subTest(path=path.name, skill_id=skill_id):
                    self.assertIn(skill_id, SKILL_DEFINITIONS)

        self.assertTrue(seen, "Expected at least one authored material profession bonus.")


class TestAreaPracticeOpportunityContracts(unittest.TestCase):
    def test_practice_opportunities_are_one_shot_and_valid(self):
        from world.domain_definitions import ALL_DOMAINS
        from world.skill_definitions import SKILL_DEFINITIONS

        seen = []
        for path, opportunity_id, kwargs in _practice_opportunity_calls_from_area_files():
            seen.append((path, opportunity_id))
            with self.subTest(path=path.name, opportunity_id=opportunity_id):
                self.assertIsInstance(opportunity_id, str)
                self.assertTrue(opportunity_id.strip())
                self.assertIsNot(kwargs.get("once_per_character"), False)
                self.assertTrue(str(kwargs.get("verb", "")).strip())
                self.assertTrue(str(kwargs.get("target", "")).strip())
                self.assertTrue(str(kwargs.get("desc", "")).strip())
                self.assertTrue(str(kwargs.get("success_text", "")).strip())

                skill_awards = kwargs.get("skill_awards", {})
                domain_awards = kwargs.get("domain_awards", {})
                self.assertTrue(skill_awards or domain_awards)

                for skill_id, count in skill_awards.items():
                    self.assertIn(skill_id, SKILL_DEFINITIONS)
                    self.assertIs(type(count), int)
                    self.assertGreater(count, 0)
                for domain, raw_xp in domain_awards.items():
                    self.assertIn(domain, ALL_DOMAINS)
                    self.assertIs(type(raw_xp), int)
                    self.assertGreater(raw_xp, 0)

        self.assertTrue(seen, "Expected authored practice opportunities.")

    def test_early_journey_zones_have_plentiful_practice(self):
        counts = {"vaels_crossing.py": 0, "ashreach_plains.py": 0, "reth_foothills.py": 0}
        for path, _opportunity_id, _kwargs in _practice_opportunity_calls_from_area_files():
            if path.name in counts:
                counts[path.name] += 1

        self.assertGreaterEqual(counts["vaels_crossing.py"], 8)
        self.assertGreaterEqual(counts["ashreach_plains.py"], 8)
        self.assertGreaterEqual(counts["reth_foothills.py"], 8)
