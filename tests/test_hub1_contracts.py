import ast
import pathlib
import unittest

from world.areas.equipment_catalog import CATALOG


ROOT = pathlib.Path(__file__).resolve().parents[1]
ZONE_FILES = {
    "vaels_crossing": ROOT / "world" / "areas" / "vaels_crossing.py",
    "ashreach_plains": ROOT / "world" / "areas" / "ashreach_plains.py",
    "reth_foothills": ROOT / "world" / "areas" / "reth_foothills.py",
    "cantera_edge": ROOT / "world" / "areas" / "cantera_edge.py",
    "stormhaven_coast": ROOT / "world" / "areas" / "stormhaven_coast.py",
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


def _resolve_room_ref(node, room_var_to_id):
    if isinstance(node, ast.Name):
        return room_var_to_id[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    raise AssertionError(f"Unsupported room reference: {ast.dump(node)}")


def _extract_trigger_item_ids(call_node):
    action_lists = []
    if len(call_node.args) >= 3 and isinstance(call_node.args[2], ast.List):
        action_lists.append(call_node.args[2])
    for keyword in call_node.keywords:
        if keyword.arg == "actions" and isinstance(keyword.value, ast.List):
            action_lists.append(keyword.value)

    item_ids = set()
    for action_list in action_lists:
        for action in action_list.elts:
            if not isinstance(action, ast.Dict):
                continue
            action_data = _literal(action)
            if action_data.get("action_type") == "give_item":
                item_ids.add(action_data.get("item_id") or action_data.get("template_id"))
    return {item_id for item_id in item_ids if item_id}


def _parse_zone_contract(zone_name, path):
    tree = ast.parse(path.read_text(encoding="utf-8"))

    room_var_to_id = {}
    room_ids = set()
    npc_ids = set()
    npc_room_ids = {}
    npc_zone_ids = {}
    npc_dialogue = {}
    quests = []
    spawn_mob_ids = set()
    named_mob_ids = set()
    lore_count = 0
    trigger_item_ids = set()
    zone_meta = {}

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and _is_area_method(node.value, "room")
        ):
            room_id = _literal(node.value.args[0])
            room_var_to_id[node.targets[0].id] = room_id
            room_ids.add(room_id)

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and _is_area_method(node.value, "npc"):
            npc_id = _literal(node.value.args[1])
            npc_ids.add(npc_id)
            npc_room_ids[npc_id] = _resolve_room_ref(node.value.args[0], room_var_to_id)
            npc_zone_ids[npc_id] = zone_name
            for keyword in node.value.keywords:
                if keyword.arg == "dialogue":
                    npc_dialogue[npc_id] = _literal(keyword.value)
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "spawn"):
            spawn_mob_ids.add(_literal(node.value.args[1]))
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "named_mob"):
            named_mob_ids.add(_literal(node.value.args[0]))
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "lore_fragment"):
            lore_count += 1
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "trigger"):
            trigger_item_ids.update(_extract_trigger_item_ids(node.value))
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "quest"):
            quest = {"quest_id": _literal(node.value.args[0]), "zone_name": zone_name}
            for keyword in node.value.keywords:
                quest[keyword.arg] = _literal(keyword.value)
            quests.append(quest)
            continue

        if isinstance(node, ast.Expr) and _is_area_method(node.value, "zone"):
            for keyword in node.value.keywords:
                zone_meta[keyword.arg] = _literal(keyword.value)

    return {
        "room_ids": room_ids,
        "npc_ids": npc_ids,
        "npc_room_ids": npc_room_ids,
        "npc_zone_ids": npc_zone_ids,
        "npc_dialogue": npc_dialogue,
        "quests": quests,
        "spawn_mob_ids": spawn_mob_ids,
        "named_mob_ids": named_mob_ids,
        "lore_count": lore_count,
        "trigger_item_ids": trigger_item_ids,
        "zone_meta": zone_meta,
    }


class TestHub1Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zone_data = {
            zone_name: _parse_zone_contract(zone_name, path)
            for zone_name, path in ZONE_FILES.items()
        }
        cls.all_room_ids = set()
        cls.all_npc_ids = set()
        cls.npc_room_ids = {}
        cls.npc_zone_ids = {}
        cls.npc_dialogue = {}
        cls.quests = []
        cls.quest_ids = set()
        cls.catalog_item_ids = set(CATALOG)
        cls.trigger_item_ids = set()

        for zone_name, data in cls.zone_data.items():
            cls.all_room_ids.update(data["room_ids"])
            cls.all_npc_ids.update(data["npc_ids"])
            cls.npc_room_ids.update(data["npc_room_ids"])
            cls.npc_zone_ids.update(data["npc_zone_ids"])
            cls.npc_dialogue.update(data["npc_dialogue"])
            cls.quests.extend(data["quests"])
            cls.trigger_item_ids.update(data["trigger_item_ids"])
            for quest in data["quests"]:
                cls.quest_ids.add(quest["quest_id"])

    def test_hub1_exterior_quest_counts_are_enriched(self):
        self.assertGreaterEqual(len(self.zone_data["ashreach_plains"]["quests"]), 5)
        self.assertGreaterEqual(len(self.zone_data["reth_foothills"]["quests"]), 5)
        self.assertGreaterEqual(len(self.zone_data["cantera_edge"]["quests"]), 5)
        self.assertGreaterEqual(len(self.zone_data["stormhaven_coast"]["quests"]), 5)

    def test_vaels_crossing_has_richer_lore_coverage(self):
        self.assertGreaterEqual(self.zone_data["vaels_crossing"]["lore_count"], 9)

    def test_vaels_crossing_is_authored_on_sorath(self):
        self.assertEqual(
            "sorath",
            self.zone_data["vaels_crossing"]["zone_meta"].get("continent"),
        )

    def test_all_quest_givers_exist(self):
        for quest in self.quests:
            self.assertIn(
                quest["quest_giver"],
                self.all_npc_ids,
                f"{quest['quest_id']} references a missing quest giver",
            )

    def test_quest_objectives_point_to_real_entities(self):
        for quest in self.quests:
            zone_data = self.zone_data[quest["zone_name"]]
            valid_kill_targets = zone_data["spawn_mob_ids"] | zone_data["named_mob_ids"]

            for objective in quest.get("objectives", []):
                obj_type = objective["type"]
                target = objective["target"]

                if obj_type == "investigate":
                    self.assertIn(
                        target,
                        self.all_room_ids,
                        f"{quest['quest_id']} investigates missing room {target}",
                    )
                elif obj_type in {"deliver", "talk_to"}:
                    self.assertIn(
                        target,
                        self.all_npc_ids,
                        f"{quest['quest_id']} references missing NPC target {target}",
                    )
                elif obj_type == "kill":
                    self.assertIn(
                        target,
                        valid_kill_targets,
                        f"{quest['quest_id']} references missing kill target {target}",
                    )

    def test_delivery_quests_have_real_handoff_items(self):
        for quest in self.quests:
            for objective in quest.get("objectives", []):
                if objective["type"] != "deliver":
                    continue

                flagged_drop = quest.get("flagged_drop")
                self.assertTrue(
                    flagged_drop,
                    f"{quest['quest_id']} is missing flagged_drop for its delivery item",
                )
                self.assertIn(
                    flagged_drop,
                    self.catalog_item_ids,
                    f"{quest['quest_id']} references missing delivery item {flagged_drop}",
                )
                self.assertEqual(
                    objective["count"],
                    1,
                    f"{quest['quest_id']} should use single-item delivery counts under the current quest engine",
                )
                giver_room = self.npc_room_ids[quest["quest_giver"]]
                target_room = self.npc_room_ids[objective["target"]]
                self.assertNotEqual(
                    giver_room,
                    target_room,
                    f"{quest['quest_id']} should not hand off a delivery quest in the same room",
                )
                giver_zone = self.npc_zone_ids[quest["quest_giver"]]
                target_zone = self.npc_zone_ids[objective["target"]]
                if giver_zone == target_zone:
                    self.assertNotEqual(
                        giver_room.split("_", 1)[0],
                        target_room.split("_", 1)[0],
                        f"{quest['quest_id']} should cross Hub 1 subregions when it stays within one zone",
                    )

    def test_next_quest_ids_point_to_real_hub1_quests(self):
        for quest in self.quests:
            next_quest_id = quest.get("next_quest_id")
            if not next_quest_id:
                continue
            self.assertIn(
                next_quest_id,
                self.quest_ids,
                f"{quest['quest_id']} chains to missing quest {next_quest_id}",
            )

    def test_vaels_crossing_onboarding_npcs_have_dialogue_guidance(self):
        for npc_id in (
            "npc_greeter_maren",
            "npc_broker_carston",
            "npc_warden_agent_calloway",
            "npc_barkeep_marta_voss",
        ):
            dialogue = self.npc_dialogue.get(npc_id)
            self.assertIsNotNone(
                dialogue,
                f"{npc_id} should have literal dialogue authored for onboarding",
            )
            self.assertTrue(
                dialogue.get("greeting_tiers"),
                f"{npc_id} should have greeting_tiers authored",
            )
            self.assertTrue(
                dialogue.get("topics"),
                f"{npc_id} should have conversation topics authored",
            )
            self.assertTrue(
                dialogue.get("base_hints"),
                f"{npc_id} should surface hint topics for new players",
            )

    def test_collect_quest_sources_are_explicit(self):
        self.assertIn(
            "rare_herb_bundle",
            self.trigger_item_ids,
            "Hub 1 should expose a real trigger source for rare_herb_bundle",
        )
        self.assertIn(
            "rare_alpine_ingredient",
            self.trigger_item_ids,
            "Hub 1 should expose a real trigger source for rare_alpine_ingredient",
        )
