import ast
import pathlib
import unittest
from collections import Counter, defaultdict, deque


ZONE_PATH = pathlib.Path(__file__).resolve().parents[1] / "world" / "areas" / "varath_prime.py"

INVERSE_DIRECTIONS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "northeast": "southwest",
    "southwest": "northeast",
    "northwest": "southeast",
    "southeast": "northwest",
    "up": "down",
    "down": "up",
    "in": "out",
    "out": "in",
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


def _resolve_room_ref(node, room_var_to_id):
    if isinstance(node, ast.Name):
        return room_var_to_id[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    raise AssertionError(f"Unsupported room reference in varath_prime.py: {ast.dump(node)}")


def _is_cross_zone_ref(ref):
    return isinstance(ref, str) and ":" in ref


def _parse_varath_prime_layout():
    source = ZONE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    room_var_to_id = {}
    room_ids = set()
    edges = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        if not _is_area_method(node.value, "room"):
            continue
        if not node.value.args or not isinstance(node.value.args[0], ast.Constant):
            raise AssertionError("area.room() must use a literal room id")
        room_var = node.targets[0].id
        room_id = node.value.args[0].value
        room_var_to_id[room_var] = room_id
        room_ids.add(room_id)

    for node in ast.walk(tree):
        if not _is_area_method(node, "exit"):
            continue
        if len(node.args) < 3:
            raise AssertionError("area.exit() must provide source, destination, and direction")

        source_room = _resolve_room_ref(node.args[0], room_var_to_id)
        dest_room = _resolve_room_ref(node.args[1], room_var_to_id)
        direction_node = node.args[2]
        if not isinstance(direction_node, ast.Constant) or not isinstance(direction_node.value, str):
            raise AssertionError("area.exit() must use a literal direction")

        hidden = any(
            keyword.arg == "hidden"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is True
            for keyword in node.keywords
        )
        edges.append((source_room, dest_room, direction_node.value, hidden))

    return room_ids, edges


class TestVarathPrimeLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.room_ids, cls.edges = _parse_varath_prime_layout()

    def test_city_meets_room_budget(self):
        self.assertGreaterEqual(len(self.room_ids), 150)

        district_counts = Counter(room_id.split("_", 1)[0] for room_id in self.room_ids)
        for district in ("ca", "oc", "mw", "mq", "dc", "cd", "nh", "hw"):
            self.assertGreaterEqual(
                district_counts[district],
                19,
                f"{district} district should have at least 19 rooms",
            )

    def test_anchor_rooms_exist(self):
        required_rooms = {
            "ca_arrival_court",
            "mq_infirmary",
            "dc_courier_platform",
            "ca_crownroad_gate",
            "mw_causeway_postern",
            "mq_escarpment_road",
            "nh_preserve_gate",
        }
        self.assertTrue(required_rooms.issubset(self.room_ids))

    def test_all_rooms_reachable_from_arrival(self):
        adjacency = defaultdict(set)
        for source_room, dest_room, _, _hidden in self.edges:
            if _is_cross_zone_ref(dest_room):
                continue
            adjacency[source_room].add(dest_room)

        seen = {"ca_arrival_court"}
        queue = deque(["ca_arrival_court"])

        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        self.assertEqual(
            self.room_ids,
            seen,
            f"Unreachable rooms: {sorted(self.room_ids - seen)}",
        )

    def test_all_exits_have_reciprocals(self):
        edge_set = {
            (source_room, dest_room, direction)
            for source_room, dest_room, direction, _hidden in self.edges
            if not _is_cross_zone_ref(dest_room)
        }
        missing = []

        for source_room, dest_room, direction, _hidden in self.edges:
            if _is_cross_zone_ref(dest_room):
                continue
            reverse_direction = INVERSE_DIRECTIONS[direction]
            reverse_edge = (dest_room, source_room, reverse_direction)
            if reverse_edge not in edge_set:
                missing.append((source_room, dest_room, direction))

        self.assertEqual([], missing, f"Missing reciprocal exits: {missing}")

    def test_city_has_cross_district_routes(self):
        cross_pairs = set()
        for source_room, dest_room, _direction, _hidden in self.edges:
            if _is_cross_zone_ref(dest_room):
                continue
            source_district = source_room.split("_", 1)[0]
            dest_district = dest_room.split("_", 1)[0]
            if source_district != dest_district:
                cross_pairs.add(frozenset((source_district, dest_district)))

        required_pairs = {
            frozenset(("ca", "oc")),
            frozenset(("ca", "mq")),
            frozenset(("ca", "nh")),
            frozenset(("oc", "mw")),
            frozenset(("oc", "mq")),
            frozenset(("oc", "hw")),
            frozenset(("mw", "cd")),
            frozenset(("mw", "hw")),
            frozenset(("mq", "dc")),
            frozenset(("cd", "hw")),
            frozenset(("cd", "nh")),
            frozenset(("nh", "hw")),
        }
        self.assertTrue(required_pairs.issubset(cross_pairs))

    def test_city_has_crownroad_cross_zone_exit(self):
        self.assertIn(
            ("ca_crownroad_gate", "crownroad_north:om_gate_verge", "south", False),
            self.edges,
        )

    def test_city_has_old_causeway_cross_zone_exit(self):
        self.assertIn(
            ("mw_causeway_postern", "old_causeway:bs_postern_landing", "west", False),
            self.edges,
        )

    def test_city_has_ironvein_cross_zone_exit(self):
        self.assertIn(
            ("mq_escarpment_road", "ironvein_escarpment:sr_gate_grade", "north", False),
            self.edges,
        )

    def test_city_has_stagcrown_cross_zone_exit(self):
        self.assertIn(
            ("nh_preserve_gate", "stagcrown_preserve:fg_charter_gate", "north", False),
            self.edges,
        )
