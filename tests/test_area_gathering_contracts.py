import ast
import pathlib
import unittest

from world.material_definitions import MATERIAL_REGISTRY


ROOT = pathlib.Path(__file__).resolve().parents[1]
ZONE_FILES = {
    "vaels_crossing": ROOT / "world" / "areas" / "vaels_crossing.py",
    "ashreach_plains": ROOT / "world" / "areas" / "ashreach_plains.py",
    "reth_foothills": ROOT / "world" / "areas" / "reth_foothills.py",
    "cantera_edge": ROOT / "world" / "areas" / "cantera_edge.py",
    "stormhaven_coast": ROOT / "world" / "areas" / "stormhaven_coast.py",
    "varath_prime": ROOT / "world" / "areas" / "varath_prime.py",
    "crownroad_north": ROOT / "world" / "areas" / "crownroad_north.py",
    "old_causeway": ROOT / "world" / "areas" / "old_causeway.py",
    "ironvein_escarpment": ROOT / "world" / "areas" / "ironvein_escarpment.py",
    "stagcrown_preserve": ROOT / "world" / "areas" / "stagcrown_preserve.py",
    "korahei": ROOT / "world" / "areas" / "korahei.py",
    "veluana_outer_reefs": ROOT / "world" / "areas" / "veluana_outer_reefs.py",
    "kiai_grounds": ROOT / "world" / "areas" / "kiai_grounds.py",
    "veluana_central_isle": ROOT / "world" / "areas" / "veluana_central_isle.py",
    "colonist_ruins": ROOT / "world" / "areas" / "colonist_ruins.py",
    "tremen": ROOT / "world" / "areas" / "tremen.py",
    "greyteeth_lower_passes": ROOT / "world" / "areas" / "greyteeth_lower_passes.py",
    "tremeneth_high_passes": ROOT / "world" / "areas" / "tremeneth_high_passes.py",
    "tremeneth_deep_mines": ROOT / "world" / "areas" / "tremeneth_deep_mines.py",
    "tremeneth_underhalls": ROOT / "world" / "areas" / "tremeneth_underhalls.py",
}

FISHING_EXPECTED_ZONES = {
    "vaels_crossing",
    "ashreach_plains",
    "reth_foothills",
    "cantera_edge",
    "stormhaven_coast",
    "old_causeway",
    "stagcrown_preserve",
    "korahei",
    "veluana_outer_reefs",
    "kiai_grounds",
    "veluana_central_isle",
    "colonist_ruins",
    "greyteeth_lower_passes",
    "tremeneth_high_passes",
    "tremeneth_deep_mines",
    "tremeneth_underhalls",
}


def _is_area_method(call_node, method_name):
    if not isinstance(call_node, ast.Call):
        return False
    func = call_node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == method_name
        and isinstance(func.value, ast.Name)
        and func.value.id == "area"
    )


def _literal(node):
    return ast.literal_eval(node)


def _parse_zone(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    gathering_pools = []
    quests = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and _is_area_method(node.value, "gathering_pool"):
            call = node.value
            keywords = {keyword.arg: keyword.value for keyword in call.keywords}
            rooms_node = call.args[1] if len(call.args) > 1 else keywords["rooms"]
            materials_node = call.args[2] if len(call.args) > 2 else keywords["materials"]
            gathering_pools.append(
                {
                    "pool_type": _literal(call.args[0]),
                    "rooms": _literal(rooms_node),
                    "materials": _literal(materials_node),
                }
            )
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "quest"):
            call = node.value
            quest = {"quest_id": _literal(call.args[0])}
            for keyword in call.keywords:
                quest[keyword.arg] = _literal(keyword.value)
            quests.append(quest)

    return {"gathering_pools": gathering_pools, "quests": quests}


class TestAreaGatheringContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zone_data = {
            zone_name: _parse_zone(path)
            for zone_name, path in ZONE_FILES.items()
        }

    def test_gathering_pool_materials_exist_in_runtime_registry(self):
        """Authored pools should spawn materials the gathering engine can resolve."""
        for zone_name, data in self.zone_data.items():
            for pool in data["gathering_pools"]:
                for material_id in pool["materials"]:
                    self.assertIn(
                        material_id,
                        MATERIAL_REGISTRY,
                        f"{zone_name} {pool['pool_type']} pool uses unregistered material {material_id}",
                    )

    def test_gathering_pool_material_categories_match_pool_type(self):
        """Pool type and material category must agree for player commands to work."""
        for zone_name, data in self.zone_data.items():
            for pool in data["gathering_pools"]:
                for material_id in pool["materials"]:
                    material = MATERIAL_REGISTRY[material_id]
                    self.assertEqual(
                        pool["pool_type"],
                        material["category"],
                        f"{zone_name} pools {material_id} as {pool['pool_type']} but registry marks {material['category']}",
                    )

    def test_expected_fishing_zones_have_fish_pools(self):
        """Zones with meaningful authored water/fishing fiction expose fish pools."""
        for zone_name in FISHING_EXPECTED_ZONES:
            pools = self.zone_data[zone_name]["gathering_pools"]
            self.assertTrue(
                any(pool["pool_type"] == "fish" for pool in pools),
                f"{zone_name} should expose at least one fish gathering pool",
            )

    def test_chained_quests_are_prerequisite_locked(self):
        """A next_quest_id should not create a chain step that can be started mid-story."""
        quests_by_id = {}
        for data in self.zone_data.values():
            for quest in data["quests"]:
                quests_by_id[quest["quest_id"]] = quest

        for quest in quests_by_id.values():
            next_quest_id = quest.get("next_quest_id")
            if not next_quest_id:
                continue
            self.assertIn(next_quest_id, quests_by_id)
            next_quest = quests_by_id[next_quest_id]
            self.assertIn(
                quest["quest_id"],
                next_quest.get("prerequisite_quests", []),
                f"{next_quest_id} should require {quest['quest_id']} before it can be offered directly",
            )
