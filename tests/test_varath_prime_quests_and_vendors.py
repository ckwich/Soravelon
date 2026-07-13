import ast
import pathlib
import unittest

from world.item_catalog import CATALOG


ZONE_PATH = pathlib.Path(__file__).resolve().parents[1] / "world" / "areas" / "varath_prime.py"


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


def _attribute_chain(node):
    chain = []
    current = node
    while isinstance(current, ast.Attribute):
        chain.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        chain.append(current.id)
        return list(reversed(chain))
    return None


def _parse_varath_prime_contract():
    tree = ast.parse(ZONE_PATH.read_text(encoding="utf-8"))

    room_ids = set()
    npc_ids = set()
    item_ids = set()
    quests = []
    vendor_configs = {}
    vendor_var_to_npc_id = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and _is_area_method(node.value, "vendor"):
            npc_ref = node.value.args[0]
            npc_id = (
                vendor_var_to_npc_id.get(npc_ref.id)
                if isinstance(npc_ref, ast.Name)
                else None
            )
            if npc_id:
                config = vendor_configs.setdefault(npc_id, {"is_vendor": True})
                keyword_names = {
                    "accepts": "vendor_accepts",
                    "item_ids": "vendor_item_ids",
                    "exclude_item_ids": "vendor_exclude_item_ids",
                    "faction": "vendor_faction",
                }
                for keyword in node.value.keywords:
                    config[keyword_names[keyword.arg]] = _literal(keyword.value)
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "npc"):
            npc_ids.add(_literal(node.value.args[1]))
            continue

        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue

        target = node.targets[0]

        if isinstance(target, ast.Name) and _is_area_method(node.value, "room"):
            room_ids.add(_literal(node.value.args[0]))
            continue

        if isinstance(target, ast.Name) and _is_area_method(node.value, "npc"):
            npc_id = _literal(node.value.args[1])
            npc_ids.add(npc_id)
            vendor_var_to_npc_id[target.id] = npc_id
            continue

        chain = _attribute_chain(target)
        if not chain or len(chain) != 3 or chain[1] != "db":
            continue

        vendor_var, _, prop = chain
        npc_id = vendor_var_to_npc_id.get(vendor_var)
        if not npc_id:
            continue

        vendor_configs.setdefault(npc_id, {})[prop] = _literal(node.value)

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and _is_area_method(node.value, "item"):
            item_ids.add(_literal(node.value.args[0]))
            continue

        if not isinstance(node, ast.Expr) or not _is_area_method(node.value, "quest"):
            continue

        quest = {"quest_id": _literal(node.value.args[0])}
        for keyword in node.value.keywords:
            quest[keyword.arg] = _literal(keyword.value)
        quests.append(quest)

    return room_ids, npc_ids, item_ids, quests, vendor_configs


class TestVarathPrimeQuestAndVendorContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (
            cls.room_ids,
            cls.npc_ids,
            cls.item_ids,
            cls.quests,
            cls.vendor_configs,
        ) = _parse_varath_prime_contract()

    def test_all_quest_givers_exist(self):
        for quest in self.quests:
            self.assertIn(
                quest["quest_giver"],
                self.npc_ids,
                f"{quest['quest_id']} references a missing quest giver",
            )

    def test_quest_objectives_point_to_real_city_entities(self):
        for quest in self.quests:
            for objective in quest.get("objectives", []):
                obj_type = objective["type"]
                target = objective["target"]
                if obj_type == "investigate":
                    self.assertIn(
                        target,
                        self.room_ids,
                        f"{quest['quest_id']} investigates missing room {target}",
                    )
                if obj_type in {"deliver", "talk_to"}:
                    self.assertIn(
                        target,
                        self.npc_ids,
                        f"{quest['quest_id']} references missing NPC target {target}",
                    )
                if obj_type == "deliver":
                    flagged_drop = quest.get("flagged_drop")
                    self.assertTrue(
                        flagged_drop,
                        f"{quest['quest_id']} is missing flagged_drop for delivery item",
                    )
                    self.assertIn(
                        flagged_drop,
                        self.item_ids,
                        f"{quest['quest_id']} delivery item {flagged_drop} is not defined in varath_prime",
                    )

    def test_city_vendors_use_curated_stock_lists(self):
        expected_vendors = {
            "npc_outfitter_loric",
            "npc_stewpot_doria",
            "npc_tinker_solla",
            "npc_clothier_penric",
            "npc_lanternwright_pes",
            "npc_quartermaster_brenn",
            "npc_supply_sergeant_hadrik",
            "npc_forge_sergeant_tomas",
            "npc_harness_master_torin",
            "npc_apothecary_meret",
            "npc_reagent_keeper_olian",
            "npc_fence_ivera_coal",
        }
        self.assertTrue(expected_vendors.issubset(self.vendor_configs.keys()))

        for npc_id in expected_vendors:
            self.assertTrue(
                self.vendor_configs[npc_id].get("vendor_item_ids"),
                f"{npc_id} should define a curated vendor_item_ids list",
            )

    def test_curated_vendor_items_exist_and_fit_vendor_types(self):
        for npc_id, config in self.vendor_configs.items():
            item_ids = config.get("vendor_item_ids") or []
            accepts = set(config.get("vendor_accepts") or [])
            for item_id in item_ids:
                self.assertIn(item_id, CATALOG, f"{npc_id} references missing catalog item {item_id}")
                item_def = CATALOG[item_id]
                self.assertFalse(
                    item_def.get("is_quest_item"),
                    f"{npc_id} should not stock quest item {item_id}",
                )
                self.assertIn(
                    item_def.get("item_type"),
                    accepts,
                    f"{npc_id} stocks {item_id} without accepting its item_type",
                )
                self.assertNotEqual(
                    item_def.get("rarity"),
                    "rare",
                    f"{npc_id} should not stock rare endgame gear in Varath Prime",
                )

    def test_vendor_network_covers_core_city_needs(self):
        stocked = set()
        for config in self.vendor_configs.values():
            stocked.update(config.get("vendor_item_ids") or [])

        required_stock = {
            "iron_sword",
            "iron_dagger",
            "iron_staff",
            "iron_bow",
            "leather_vest",
            "iron_breastplate",
            "bandage",
            "minor_healing_potion",
            "trail_rations",
            "pickaxe",
        }
        self.assertTrue(required_stock.issubset(stocked))
