import ast
import pathlib
import unittest

from world.areas.equipment_catalog import CATALOG


ZONE_PATH = pathlib.Path(__file__).resolve().parents[1] / "world" / "areas" / "ironvein_escarpment.py"


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


def _resolve_room_ref(node, room_var_to_id):
    if isinstance(node, ast.Name):
        return room_var_to_id[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    raise AssertionError(f"Unsupported room reference in ironvein_escarpment.py: {ast.dump(node)}")


def _parse_ironvein_contract():
    tree = ast.parse(ZONE_PATH.read_text(encoding="utf-8"))

    room_var_to_id = {}
    room_ids = set()
    npc_ids = set()
    npc_room_ids = {}
    item_ids = set()
    quests = []
    vendor_configs = {}
    vendor_var_to_npc_id = {}
    spawn_mob_ids = set()
    named_mob_ids = set()

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        if not isinstance(node.targets[0], ast.Name):
            continue
        if not _is_area_method(node.value, "room"):
            continue
        room_var = node.targets[0].id
        room_id = _literal(node.value.args[0])
        room_var_to_id[room_var] = room_id
        room_ids.add(room_id)

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and _is_area_method(node.value, "npc"):
            npc_id = _literal(node.value.args[1])
            npc_ids.add(npc_id)
            npc_room_ids[npc_id] = _resolve_room_ref(node.value.args[0], room_var_to_id)
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "spawn"):
            spawn_mob_ids.add(_literal(node.value.args[1]))
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "named_mob"):
            named_mob_ids.add(_literal(node.value.args[0]))
            continue

        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue

        target = node.targets[0]

        if isinstance(target, ast.Name) and _is_area_method(node.value, "npc"):
            npc_id = _literal(node.value.args[1])
            npc_ids.add(npc_id)
            npc_room_ids[npc_id] = _resolve_room_ref(node.value.args[0], room_var_to_id)
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

    return room_ids, npc_ids, npc_room_ids, item_ids, quests, vendor_configs, spawn_mob_ids, named_mob_ids


class TestIronveinEscarpmentContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (
            cls.room_ids,
            cls.npc_ids,
            cls.npc_room_ids,
            cls.item_ids,
            cls.quests,
            cls.vendor_configs,
            cls.spawn_mob_ids,
            cls.named_mob_ids,
        ) = _parse_ironvein_contract()

    def test_all_quest_givers_exist(self):
        for quest in self.quests:
            self.assertIn(
                quest["quest_giver"],
                self.npc_ids,
                f"{quest['quest_id']} references a missing quest giver",
            )

    def test_quest_objectives_point_to_real_zone_entities(self):
        valid_kill_targets = self.spawn_mob_ids | self.named_mob_ids

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
                if obj_type == "kill":
                    self.assertIn(
                        target,
                        valid_kill_targets,
                        f"{quest['quest_id']} references missing kill target {target}",
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
                        f"{quest['quest_id']} delivery item {flagged_drop} is not defined in ironvein_escarpment",
                    )

    def test_delivery_quests_cross_subregions(self):
        for quest in self.quests:
            for objective in quest.get("objectives", []):
                if objective["type"] != "deliver":
                    continue
                giver_room = self.npc_room_ids[quest["quest_giver"]]
                target_room = self.npc_room_ids[objective["target"]]
                self.assertNotEqual(
                    giver_room.split("_", 1)[0],
                    target_room.split("_", 1)[0],
                    f"{quest['quest_id']} should deliver across Ironvein subregions, not within {giver_room}",
                )

    def test_next_quest_ids_point_to_real_quests(self):
        quest_ids = {quest["quest_id"] for quest in self.quests}
        for quest in self.quests:
            next_quest_id = quest.get("next_quest_id")
            if next_quest_id:
                self.assertIn(
                    next_quest_id,
                    quest_ids,
                    f"{quest['quest_id']} chains to missing quest {next_quest_id}",
                )

    def test_sutler_uses_curated_stock(self):
        self.assertIn("npc_sutler_dera", self.vendor_configs)

        stock = self.vendor_configs["npc_sutler_dera"].get("vendor_item_ids") or []
        accepts = set(self.vendor_configs["npc_sutler_dera"].get("vendor_accepts") or [])

        self.assertTrue(stock, "npc_sutler_dera should define a curated vendor_item_ids list")
        self.assertEqual({"consumable", "tool"}, accepts)

        for item_id in stock:
            self.assertIn(item_id, CATALOG, f"npc_sutler_dera references missing catalog item {item_id}")
            item_def = CATALOG[item_id]
            self.assertFalse(
                item_def.get("is_quest_item"),
                f"npc_sutler_dera should not stock quest item {item_id}",
            )
            self.assertIn(
                item_def.get("item_type"),
                accepts,
                f"npc_sutler_dera stocks {item_id} without accepting its item_type",
            )
            self.assertNotEqual(
                item_def.get("rarity"),
                "rare",
                f"npc_sutler_dera should not stock rare endgame gear on the Ironvein Escarpment",
            )

    def test_sutler_covers_quarry_field_needs(self):
        stocked = set()
        for config in self.vendor_configs.values():
            stocked.update(config.get("vendor_item_ids") or [])

        required_stock = {
            "pickaxe",
            "trail_rations",
            "bandage",
            "minor_healing_potion",
            "minor_stamina_potion",
            "antidote_potion",
        }
        self.assertTrue(required_stock.issubset(stocked))
