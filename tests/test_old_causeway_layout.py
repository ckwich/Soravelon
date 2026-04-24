import ast
import pathlib
import unittest
from collections import Counter, defaultdict, deque


ZONE_PATH = pathlib.Path(__file__).resolve().parents[1] / "world" / "areas" / "old_causeway.py"

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
    raise AssertionError(f"Unsupported room reference in old_causeway.py: {ast.dump(node)}")


def _is_cross_zone_ref(ref):
    return isinstance(ref, str) and ":" in ref


def _parse_old_causeway_layout():
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


class TestOldCausewayLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.room_ids, cls.edges = _parse_old_causeway_layout()

    def test_zone_meets_room_budget(self):
        self.assertGreaterEqual(len(self.room_ids), 110)

        region_counts = Counter(room_id.split("_", 1)[0] for room_id in self.room_ids)
        self.assertGreaterEqual(region_counts["bs"], 24)
        self.assertGreaterEqual(region_counts["ar"], 20)
        self.assertGreaterEqual(region_counts["ws"], 18)
        self.assertGreaterEqual(region_counts["br"], 20)
        self.assertGreaterEqual(region_counts["rw"], 18)
        self.assertGreaterEqual(region_counts["sc"], 18)

    def test_anchor_rooms_exist(self):
        required_rooms = {
            "bs_postern_landing",
            "ar_waystation_turn",
            "ws_salvage_square",
            "br_hidden_fork",
            "rw_ward_core",
            "sc_inner_circle",
            "sc_west_edge",
        }
        self.assertTrue(required_rooms.issubset(self.room_ids))

    def test_cross_zone_exit_to_varath_prime_exists(self):
        self.assertIn(
            ("bs_postern_landing", "varath_prime:mw_causeway_postern", "east", False),
            self.edges,
        )

    def test_all_local_rooms_reachable_from_postern_landing(self):
        adjacency = defaultdict(set)
        for source_room, dest_room, _direction, _hidden in self.edges:
            if _is_cross_zone_ref(dest_room):
                continue
            adjacency[source_room].add(dest_room)

        seen = {"bs_postern_landing"}
        queue = deque(["bs_postern_landing"])

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

    def test_all_local_exits_have_reciprocals(self):
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

    def test_no_duplicate_local_exit_directions(self):
        duplicates = defaultdict(list)
        for source_room, dest_room, direction, _hidden in self.edges:
            if _is_cross_zone_ref(dest_room):
                continue
            duplicates[(source_room, direction)].append(dest_room)

        collisions = {
            key: value
            for key, value in duplicates.items()
            if len(value) > 1
        }
        self.assertEqual({}, collisions, f"Duplicate local exit directions: {collisions}")

    def test_hidden_routes_exist(self):
        self.assertIn(
            ("ws_cellar_run", "br_hidden_fork", "south", True),
            self.edges,
        )
        self.assertIn(
            ("ar_hidden_apse", "rw_hidden_conduit", "down", True),
            self.edges,
        )
