import ast
import pathlib
import unittest
from collections import defaultdict, deque


ROOT = pathlib.Path(__file__).resolve().parents[1]

ZONE_FILES = {
    "korahei": ROOT / "world" / "areas" / "korahei.py",
    "veluana_outer_reefs": ROOT / "world" / "areas" / "veluana_outer_reefs.py",
    "kiai_grounds": ROOT / "world" / "areas" / "kiai_grounds.py",
    "veluana_central_isle": ROOT / "world" / "areas" / "veluana_central_isle.py",
    "colonist_ruins": ROOT / "world" / "areas" / "colonist_ruins.py",
}

START_ROOMS = {
    "korahei": "ac_arrival_circle",
    "veluana_outer_reefs": "rl_korahei_landing",
    "kiai_grounds": "wr_witness_gate",
    "veluana_central_isle": "gc_korahei_track",
    "colonist_ruins": "ld_quiet_landing",
}

COMBAT_LOOP_EXPECTATIONS = {
    "korahei": {"min_spawn_anchors": 4, "min_max_concurrent": 8, "prefixes": {"lt"}},
    "veluana_outer_reefs": {
        "min_spawn_anchors": 14,
        "min_max_concurrent": 24,
        "prefixes": {"tm", "kp", "wr", "sr"},
    },
    "kiai_grounds": {
        "min_spawn_anchors": 10,
        "min_max_concurrent": 16,
        "prefixes": {"cr", "or", "pr", "hr"},
    },
    "veluana_central_isle": {
        "min_spawn_anchors": 12,
        "min_max_concurrent": 18,
        "prefixes": {"gc", "rp", "bs", "lc"},
    },
    "colonist_ruins": {
        "min_spawn_anchors": 12,
        "min_max_concurrent": 18,
        "prefixes": {"ld", "ar", "bn", "cw"},
    },
}

REQUIRED_ANCHORS = {
    "korahei": {
        "ac_arrival_circle",
        "ac_courier_platform",
        "ac_reef_gate",
        "kg_kiai_gate",
        "lt_central_path",
        "qh_ruins_boat",
    },
    "veluana_outer_reefs": {
        "rl_korahei_landing",
        "tm_tide_marker",
        "kp_fishing_shelf",
        "wr_watch_reef",
        "sr_sunscale_pool",
    },
    "kiai_grounds": {
        "wr_witness_gate",
        "wr_silence_ring",
        "cr_care_basin",
        "or_outer_waiting",
        "hr_high_perch",
    },
    "veluana_central_isle": {
        "gc_korahei_track",
        "gc_loop_stone",
        "rp_rain_pools",
        "bs_basalt_ring",
        "hr_humid_ruin",
    },
    "colonist_ruins": {
        "ld_quiet_landing",
        "ld_broken_dock",
        "gr_grief_square",
        "ar_archive_shell",
        "bn_burnt_names",
    },
}

EXPECTED_CROSS_ZONE_EXITS = {
    ("korahei", "ac_reef_gate", "east", "veluana_outer_reefs:rl_korahei_landing"),
    ("veluana_outer_reefs", "rl_korahei_landing", "west", "korahei:ac_reef_gate"),
    ("korahei", "kg_kiai_gate", "north", "kiai_grounds:wr_witness_gate"),
    ("kiai_grounds", "wr_witness_gate", "south", "korahei:kg_kiai_gate"),
    ("korahei", "lt_central_path", "east", "veluana_central_isle:gc_korahei_track"),
    ("veluana_central_isle", "gc_korahei_track", "west", "korahei:lt_central_path"),
    ("korahei", "qh_ruins_boat", "south", "colonist_ruins:ld_quiet_landing"),
    ("colonist_ruins", "ld_quiet_landing", "north", "korahei:qh_ruins_boat"),
}

FORBIDDEN_DRAGON_PHRASES = (
    "dragon speaks",
    "dragon spoke",
    "dragon remembers",
    "dragon remembered",
    "intelligent dragon",
    "sentient dragon",
    "thinking dragon",
    "dragon thought",
    "dragon mind",
)


def _is_area_call(call_node, method_name):
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


def _value_or_name(node):
    if isinstance(node, ast.Name):
        return node.id
    return _literal(node)


def _keyword(call, name, default=None):
    for keyword in call.keywords:
        if keyword.arg == name:
            return _literal(keyword.value)
    return default


def _parse_zone(path):
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    data = {
        "text": text,
        "rooms": set(),
        "room_descs": {},
        "exits": [],
        "npcs": set(),
        "spawns": set(),
        "spawn_defs": [],
        "named_mobs": set(),
        "items": set(),
        "quests": [],
        "materials": set(),
        "material_tiers": {},
        "gathering_pools": [],
        "vendor_npcs": set(),
        "vendor_stock": {},
    }

    room_vars = {}
    npc_vars = {}

    for node in ast.walk(tree):
        call = None
        target_name = None
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            call = node.value
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                target_name = node.targets[0].id
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value

        if call is None:
            continue

        if _is_area_call(call, "room"):
            room_id = _literal(call.args[0])
            data["rooms"].add(room_id)
            data["room_descs"][room_id] = _keyword(call, "desc", "")
            if target_name:
                room_vars[target_name] = room_id
            continue

        if _is_area_call(call, "exit"):
            data["exits"].append(
                {
                    "from": room_vars.get(_value_or_name(call.args[0]), _value_or_name(call.args[0])),
                    "to": room_vars.get(_value_or_name(call.args[1]), _value_or_name(call.args[1])),
                    "direction": _literal(call.args[2]),
                    "hidden": _keyword(call, "hidden", False),
                }
            )
            continue

        if _is_area_call(call, "npc"):
            npc_id = _literal(call.args[1])
            data["npcs"].add(npc_id)
            if target_name:
                npc_vars[target_name] = npc_id
            continue

        if _is_area_call(call, "spawn"):
            room_id = room_vars.get(_value_or_name(call.args[0]), _value_or_name(call.args[0]))
            mob_id = _literal(call.args[1])
            data["spawns"].add(mob_id)
            data["spawn_defs"].append(
                {
                    "room": room_id,
                    "mob": mob_id,
                    "count_max": _keyword(call, "count_max", 1),
                }
            )
            continue

        if _is_area_call(call, "named_mob"):
            data["named_mobs"].add(_literal(call.args[0]))
            continue

        if _is_area_call(call, "item"):
            data["items"].add(_literal(call.args[0]))
            continue

        if _is_area_call(call, "material"):
            material_id = _literal(call.args[0])
            data["materials"].add(material_id)
            data["material_tiers"][material_id] = _keyword(call, "tier", 1)
            continue

        if _is_area_call(call, "gathering_pool"):
            rooms_node = call.args[1]
            materials_node = call.args[2]
            data["gathering_pools"].append(
                {
                    "pool_type": _literal(call.args[0]),
                    "rooms": _literal(rooms_node),
                    "materials": _literal(materials_node),
                }
            )
            continue

        if _is_area_call(call, "quest"):
            quest = {"quest_id": _literal(call.args[0])}
            for keyword in call.keywords:
                quest[keyword.arg] = _literal(keyword.value)
            data["quests"].append(quest)
            continue

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.targets[0], ast.Attribute):
            continue
        target = node.targets[0]
        if target.attr != "vendor_item_ids":
            continue
        if not isinstance(target.value, ast.Attribute) or target.value.attr != "db":
            continue
        vendor_var = target.value.value
        if isinstance(vendor_var, ast.Name) and vendor_var.id in npc_vars:
            npc_id = npc_vars[vendor_var.id]
            data["vendor_npcs"].add(npc_id)
            data["vendor_stock"][npc_id] = _literal(node.value)

    return data


class TestKoraheiHub5Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zone_data = {
            zone_name: _parse_zone(path)
            for zone_name, path in ZONE_FILES.items()
            if path.exists()
        }

    def test_area_files_exist(self):
        for zone_name, path in ZONE_FILES.items():
            self.assertTrue(path.exists(), f"{zone_name} area file is missing")

    def test_each_zone_has_at_least_100_rooms(self):
        for zone_name in ZONE_FILES:
            data = self.zone_data[zone_name]
            self.assertGreaterEqual(
                len(data["rooms"]),
                100,
                f"{zone_name} should have at least 100 authored rooms",
            )

    def test_required_room_anchors_exist(self):
        for zone_name, anchors in REQUIRED_ANCHORS.items():
            rooms = self.zone_data[zone_name]["rooms"]
            for room_id in anchors:
                self.assertIn(room_id, rooms, f"{zone_name} missing anchor {room_id}")

    def test_each_zone_has_multiple_rich_subregions(self):
        for zone_name, data in self.zone_data.items():
            counts = defaultdict(int)
            for room_id in data["rooms"]:
                counts[room_id.split("_", 1)[0]] += 1
            self.assertGreaterEqual(
                len(counts),
                5,
                f"{zone_name} should have at least five authored subregions",
            )
            self.assertGreaterEqual(
                min(counts.values()),
                15,
                f"{zone_name} subregions should be substantial, got {dict(counts)}",
            )

    def test_local_room_graph_is_reachable(self):
        for zone_name, data in self.zone_data.items():
            rooms = data["rooms"]
            graph = defaultdict(set)
            for exit_def in data["exits"]:
                if exit_def["to"] in rooms:
                    graph[exit_def["from"]].add(exit_def["to"])

            seen = set()
            queue = deque([START_ROOMS[zone_name]])
            while queue:
                room = queue.popleft()
                if room in seen:
                    continue
                seen.add(room)
                queue.extend(graph[room] - seen)

            self.assertEqual(rooms, seen, f"{zone_name} has unreachable rooms")

    def test_local_exits_are_reciprocal_and_not_duplicate(self):
        opposites = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
            "northeast": "southwest",
            "northwest": "southeast",
            "southeast": "northwest",
            "southwest": "northeast",
            "up": "down",
            "down": "up",
            "in": "out",
            "out": "in",
        }
        for zone_name, data in self.zone_data.items():
            rooms = data["rooms"]
            by_source_direction = {}
            local = set()
            for exit_def in data["exits"]:
                if exit_def["to"] not in rooms:
                    continue
                key = (exit_def["from"], exit_def["direction"])
                self.assertNotIn(key, by_source_direction, f"{zone_name} duplicate exit {key}")
                by_source_direction[key] = exit_def["to"]
                local.add((exit_def["from"], exit_def["direction"], exit_def["to"]))

            for source, direction, target in local:
                if direction in opposites:
                    self.assertIn(
                        (target, opposites[direction], source),
                        local,
                        f"{zone_name} missing reciprocal exit for {source} {direction} {target}",
                    )

    def test_cross_zone_exits_are_authored(self):
        authored = set()
        for zone_name, data in self.zone_data.items():
            for exit_def in data["exits"]:
                if ":" in exit_def["to"]:
                    authored.add((zone_name, exit_def["from"], exit_def["direction"], exit_def["to"]))
        self.assertTrue(EXPECTED_CROSS_ZONE_EXITS.issubset(authored))

    def test_quests_have_real_givers_and_valid_objectives(self):
        from world.action_vocabulary import ACTION_HANDLERS

        all_quests = {}
        global_targets = set()
        for data in self.zone_data.values():
            global_targets |= (
                data["rooms"]
                | data["npcs"]
                | data["spawns"]
                | data["named_mobs"]
                | data["items"]
                | data["materials"]
            )
        for zone_name, data in self.zone_data.items():
            known_targets = (
                data["rooms"]
                | data["npcs"]
                | data["spawns"]
                | data["named_mobs"]
                | data["items"]
                | data["materials"]
            )
            for quest in data["quests"]:
                all_quests[quest["quest_id"]] = quest
                giver = quest.get("quest_giver")
                self.assertIn(giver, data["npcs"], f"{zone_name} quest {quest['quest_id']} has bad giver")
                self.assertTrue(quest.get("description"), f"{quest['quest_id']} needs a description")
                self.assertTrue(quest.get("objectives"), f"{quest['quest_id']} needs objectives")
                self.assertTrue(quest.get("rewards"), f"{quest['quest_id']} needs rewards")
                self.assertIn(
                    quest.get("world_expression", {}),
                    ({}, None),
                    f"{quest['quest_id']} should not make routine shared-world changes",
                )
                for reward in quest["rewards"]:
                    action_type = reward.get("action_type")
                    self.assertIn(
                        action_type,
                        ACTION_HANDLERS,
                        f"{zone_name} quest {quest['quest_id']} has invalid reward action {reward}",
                    )
                for objective in quest["objectives"]:
                    target = objective.get("target")
                    if not target or ":" in target:
                        continue
                    self.assertIn(
                        target,
                        known_targets | global_targets,
                        f"{zone_name} quest {quest['quest_id']} objective points nowhere: {target}",
                    )

        for quest in all_quests.values():
            next_quest_id = quest.get("next_quest_id")
            if not next_quest_id:
                continue
            self.assertIn(next_quest_id, all_quests)
            self.assertIn(
                quest["quest_id"],
                all_quests[next_quest_id].get("prerequisite_quests", []),
                f"{next_quest_id} should require {quest['quest_id']}",
            )

    def test_delivery_quests_route_players_to_meaningful_places(self):
        for zone_name, data in self.zone_data.items():
            room_prefixes = {room_id: room_id.split("_", 1)[0] for room_id in data["rooms"]}
            for quest in data["quests"]:
                delivery_targets = [
                    objective.get("target")
                    for objective in quest.get("objectives", [])
                    if objective.get("type") == "deliver"
                ]
                if not delivery_targets:
                    continue
                route_targets = [
                    objective.get("target")
                    for objective in quest.get("objectives", [])
                    if objective.get("type") in {"visit", "investigate"}
                ]
                self.assertTrue(
                    any(target not in data["npcs"] for target in delivery_targets)
                    or any(
                        room_prefixes.get(target) != room_prefixes.get(START_ROOMS[zone_name])
                        for target in route_targets
                    ),
                    f"{quest['quest_id']} delivery should guide exploration, not just shuffle items",
                )

    def test_every_zone_has_fishing_and_other_gathering_pools(self):
        for zone_name, data in self.zone_data.items():
            pool_types = {pool["pool_type"] for pool in data["gathering_pools"]}
            self.assertIn("fish", pool_types, f"{zone_name} needs a fishing pool")
            self.assertGreaterEqual(
                len(pool_types),
                4,
                f"{zone_name} should support several gathering activities",
            )
            for pool in data["gathering_pools"]:
                for material_id in pool["materials"]:
                    self.assertIn(
                        material_id,
                        data["materials"],
                        f"{zone_name} gathering pool uses undeclared area material {material_id}",
                    )

    def test_declared_material_tiers_match_runtime_registry(self):
        from world.material_definitions import MATERIAL_REGISTRY

        for zone_name, data in self.zone_data.items():
            for material_id, tier in data["material_tiers"].items():
                self.assertEqual(
                    tier,
                    MATERIAL_REGISTRY[material_id]["tier"],
                    f"{zone_name} declares {material_id} as tier {tier}",
                )

    def test_city_has_curated_vendor_stock(self):
        allowed_stock = {
            "trail_rations",
            "spiced_fish",
            "hearty_stew",
            "minor_stamina_potion",
            "minor_healing_potion",
            "bandage",
            "fishing_rod",
            "bait",
            "sickle",
            "hatchet",
            "skinning_knife",
            "pickaxe",
            "iron_dagger",
            "iron_staff",
            "leather_vest",
            "leather_boots",
            "travelers_cloak",
        }
        vendors = self.zone_data["korahei"]["vendor_npcs"]
        self.assertGreaterEqual(len(vendors), 3, "Korahei should have multiple curated vendors")
        for npc_id, stock in self.zone_data["korahei"]["vendor_stock"].items():
            self.assertTrue(stock, f"{npc_id} needs authored stock")
            for item_id in stock:
                self.assertIn(item_id, allowed_stock, f"{npc_id} sells inappropriate stock {item_id}")

    def test_spawned_mobs_have_runtime_templates(self):
        from world.mob_templates import MOB_TEMPLATES

        for zone_name, data in self.zone_data.items():
            for mob_id in data["spawns"]:
                self.assertIn(mob_id, MOB_TEMPLATES, f"{zone_name} spawns missing template {mob_id}")

    def test_zones_have_intentional_combat_loops(self):
        """Combat practice should be available through authored loops, not random sprinkles."""
        for zone_name, expected in COMBAT_LOOP_EXPECTATIONS.items():
            spawn_defs = self.zone_data[zone_name]["spawn_defs"]
            self.assertGreaterEqual(
                len(spawn_defs),
                expected["min_spawn_anchors"],
                f"{zone_name} needs more authored combat anchors",
            )
            self.assertGreaterEqual(
                sum(spawn["count_max"] for spawn in spawn_defs),
                expected["min_max_concurrent"],
                f"{zone_name} needs enough concurrent combat targets for repeatable practice",
            )
            covered_prefixes = {spawn["room"].split("_", 1)[0] for spawn in spawn_defs}
            self.assertTrue(
                expected["prefixes"].issubset(covered_prefixes),
                f"{zone_name} combat loops should cover {expected['prefixes']}, got {covered_prefixes}",
            )

    def test_key_and_combat_rooms_have_hand_polished_prose(self):
        """High-traffic rooms should not retain generated-sounding prose."""
        for zone_name, data in self.zone_data.items():
            key_rooms = set(REQUIRED_ANCHORS[zone_name])
            key_rooms.update(spawn["room"] for spawn in data["spawn_defs"])
            for room_id in key_rooms:
                desc = data["room_descs"][room_id]
                self.assertNotIn(
                    "This part of the",
                    desc,
                    f"{zone_name} {room_id} still has generated prose scaffolding",
                )
                self.assertGreaterEqual(
                    len(desc),
                    120,
                    f"{zone_name} {room_id} needs richer hand-polished prose",
                )

    def test_quest_consequences_are_specific(self):
        seen = set()
        generic = "helped with care instead of haste"
        for zone_name, data in self.zone_data.items():
            for quest in data["quests"]:
                consequence = quest.get("consequence_small") or ""
                self.assertTrue(consequence, f"{zone_name} {quest['quest_id']} needs consequence text")
                self.assertNotIn(
                    generic,
                    consequence,
                    f"{zone_name} {quest['quest_id']} still uses generic consequence text",
                )
                self.assertNotIn(
                    consequence,
                    seen,
                    f"{zone_name} {quest['quest_id']} reuses consequence text",
                )
                seen.add(consequence)

    def test_content_preserves_dragon_mystery_guardrail(self):
        for zone_name, data in self.zone_data.items():
            text = data["text"].lower()
            for phrase in FORBIDDEN_DRAGON_PHRASES:
                self.assertNotIn(phrase, text, f"{zone_name} leaks dragon mystery with '{phrase}'")
