# Testing Patterns

**Analysis Date:** 2026-03-24

## Test Framework

**Runner:**
- Evennia test runner (wraps Django's `unittest` via `evennia test`)
- Base class: `EvenniaTest` from `evennia.utils.test_resources`
- Config: `server/conf/settings.py` (Evennia settings file)

**Assertion Library:**
- Python `unittest` assertions (`assertEqual`, `assertTrue`, `assertAlmostEqual`, etc.)

**Run Commands:**
```bash
evennia test --settings server.conf.settings tests/   # Run all tests
evennia test --settings server.conf.settings tests/test_banking.py  # Single file
```

## Test File Organization

**Location:**
- All tests in `tests/` directory at project root (separate from source)
- One test file per engine module / system

**Naming:**
- `test_<system_name>.py` matching the `world/` module it tests

**Mapping:**

| Test File | Tests | Coverage Area |
|-----------|-------|---------------|
| `tests/test_world_state.py` | 17 | Dimensions, decay, attunement, domain XP, backend level, context packet, faction standing, world events |
| `tests/test_node_system.py` | 20 | Failure slider, state transitions, session cap, stabilization, Layer 1 rooms, layer swap, orphan recovery, node effects, persistence, BFS |
| `tests/test_mob_disposition.py` | 23 | Disposition computation, standing/ancestry/reputation/trust modifiers, behavior translation, edge cases, clamping |
| `tests/test_mob_affixes.py` | 18 | Rarity-based affix counts, forbidden combos, defensive limits, star display, affix reveal, immunity, node pools, pack spawning, loot tier |
| `tests/test_zone_scaling.py` | 21 | Scale factor math, combat scale caching, damage scaling, mob stat initialization, resistance, material tiers, no-zone-level assertions |
| `tests/test_typeclasses.py` | 17 | Item creation defaults, quest item restrictions, container rules, equipment slots, keyring items, locked/hidden/gravity exits, carry state, account preferences |
| `tests/test_banking.py` | 24 | Deposit/withdraw, transaction records, drafts, debt, recurring payments, grace periods, lapsing |
| `tests/test_inventory_engine.py` | 27 | Container weight reduction, pickup/drop, auto-stacking, keyring routing, container operations, equip/unequip, encumbrance, query helpers |
| `tests/test_group_engine.py` | 16 | Invite/accept/decline, group formation, leave/kick, leadership transfer, loot modes, zone proximity, max size, disconnect cleanup |
| `tests/test_area_builder.py` | 17 | Zone creation, room tagging, exit types, cross-zone exits, spawn/NPC/named mob storage, node integration, quest/material/lore storage, build reports, validation, file loading |

**Total: ~200 tests across 10 files**

## Test Structure

**TDD Discipline:**
Every test file has a docstring declaring TDD intent:
```python
"""
Tests for the Soravelon node system (Build Order Step 3).
Tests written FIRST per TDD. These must all fail before production code.
"""
```

**One-test-per-class pattern:**
Most tests use one class per assertion to maximize isolation. Each class has a single `test_*` method:
```python
class TestDepositSuccess(BankingTestBase):
    def test_deposit_success(self):
        from world.banking import deposit, get_balance
        success, msg = deposit(self.char1, 500)
        self.assertTrue(success)
        self.assertEqual(self.char1.db.carried_scales, 500)
        self.assertEqual(get_balance(self.char1), 500)
```

**Exception:** Some base test classes group related tests when they share significant setup (e.g., `ObjectTests` in `tests/test_typeclasses.py`).

**Section comments** group related test classes:
```python
# --- Core computation ---
# --- Ancestry ---
# --- Trust ---
# --- Behavior translation ---
# --- Edge cases ---
```

## Base Test Classes

**Every test file defines a custom base class** extending `EvenniaTest`:

```python
class BankingTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.carried_scales = 1000
```

**`EvenniaTest` provides:**
- `self.char1`, `self.char2` — pre-created Character objects
- A clean database per test
- Evennia server context (typeclasses, scripts, etc.)

**Common base class patterns:**

| Base Class | File | Setup |
|-----------|------|-------|
| `NodeTestBase` | `test_node_system.py` | Zone object, 3 rooms with exits, cross-zone room |
| `DispositionTestBase` | `test_mob_disposition.py` | Room, mob, character with ancestry/reputation, `_set_standing()` helper |
| `BankingTestBase` | `test_banking.py` | Character with 1000 carried_scales |
| `InvTestBase` | `test_inventory_engine.py` | Room, character with strength=10, `_make_item()`, `_make_container()`, `_make_equipment()` helpers |
| `ScalingTestBase` | `test_zone_scaling.py` | Room with zone_id, mob with stat ranges, character with backend_level=10 |
| `GroupTestBase` | `test_group_engine.py` | Room with zone_id, two characters in room, `_make_char()` helper |
| `AffixTestBase` | `test_mob_affixes.py` | Normal room, node room with resonance type and mob_affixes_active tag |
| `AreaBuilderTestBase` | `test_area_builder.py` | Clears registries, `_make_builder()` and `_make_room()` helpers |

## Import Pattern

**Imports inside test methods, not at file level.** This is deliberate — the system under test is imported where used:
```python
class TestDepositSuccess(BankingTestBase):
    def test_deposit_success(self):
        from world.banking import deposit, get_balance  # imported here
        success, msg = deposit(self.char1, 500)
```

This ensures tests fail cleanly if the import target does not exist (important for TDD where tests are written before production code).

## Assertion Patterns

**Boolean success checks:**
```python
success, msg = deposit(self.char1, 500)
self.assertTrue(success)
# or
self.assertFalse(success)
```

**Exact value assertions:**
```python
self.assertEqual(get_balance(self.char1), 500)
self.assertEqual(self.char1.db.carried_scales, 500)
```

**Float comparison with tolerance:**
```python
self.assertAlmostEqual(d, 0.45, places=2)
self.assertAlmostEqual(mod, 0.6, places=5)
```

**Range assertions (boundary testing):**
```python
self.assertLessEqual(script.db.failure, 100.0)
self.assertGreaterEqual(script.db.failure, 0.0)
self.assertGreater(d, 0.0)
self.assertLess(d, 0.5)
```

**Existence assertions:**
```python
self.assertIsNotNone(debt)
self.assertIsNone(self.char1.db.layer0_room_id)
self.assertTrue(
    InventoryItem.objects.filter(character_id=self.char1.id, item_id=item.id).exists()
)
```

**Tag assertions:**
```python
self.assertTrue(room.tags.get("burn_enhanced", category="node_effect"))
self.assertFalse(room.tags.get("action_budget_penalty", category="node_effect"))
```

**Collection membership:**
```python
self.assertIn(self.char1.id, state["members"])
self.assertNotIn(self.room_other_zone, rooms)
```

**String content assertions:**
```python
self.assertTrue(name.startswith("|g★|n"))
self.assertIn("enraged", msg1.lower())
self.assertIn("bog", str(ctx.exception))
```

**Dict key presence (required fields):**
```python
required_keys = {"ancestry", "primary_domain", ...}
self.assertTrue(required_keys.issubset(packet.keys()))
```

## Mocking

**Framework:** `unittest.mock` (`patch`, `MagicMock`)

**Rarity roll mocking** (most common mock usage):
```python
from unittest.mock import patch

with patch("world.mob_affix_roller.roll_rarity", return_value="magic"):
    apply_affixes_to_mob(mob, self.room)
```

**Property mocking** for `is_connected`:
```python
with patch.object(
    type(self.char1), "is_connected",
    new_callable=lambda: property(lambda s: True)
):
    decay_tick_all()
```

**Function call verification:**
```python
with patch("world.zone_object.initialize_node") as mock_init:
    ab.build()
    mock_init.assert_called_once()
    call_kwargs = mock_init.call_args
    self.assertEqual(call_kwargs.kwargs["node_type"], "cognitive")
```

**What to mock:**
- Random number generators (rarity rolls)
- Connection state (`is_connected`)
- External system calls (e.g., `initialize_node` during area building)

**What NOT to mock:**
- Django ORM operations — tests use real database
- Evennia `create_object` / `create_script` — tests create real objects
- The system under test itself

## Fixtures and Factories

**No fixture files.** All test data is created in `setUp()` methods and helper functions.

**Helper methods on base classes:**
```python
# InvTestBase
def _make_item(self, key="item", location=None, **kwargs):
    from typeclasses.objects import SoravelonItem
    loc = location if location is not None else self.room
    item = create_object(SoravelonItem, key=key, location=loc)
    for k, v in kwargs.items():
        setattr(item.db, k, v)
    return item

def _make_container(self, key="bag", location=None, **kwargs):
    from typeclasses.objects import SoravelonContainer
    loc = location if location is not None else self.char1
    bag = create_object(SoravelonContainer, key=key, location=loc)
    for k, v in kwargs.items():
        setattr(bag.db, k, v)
    InventoryItem.objects.create(character_id=self.char1.id, item_id=bag.id)
    return bag
```

**Convention for helper factory methods:**
- Prefix with `_make_`
- Accept `**kwargs` for setting `db` attributes
- Create both Evennia object and Django record when needed
- Return the created object

**Standing helper pattern:**
```python
def _set_standing(self, faction_id, standing, trust=50):
    FactionStanding.objects.update_or_create(
        character=self.char1,
        faction_id=faction_id,
        subfaction_id=None,
        defaults={"standing": standing, "trust": trust},
    )
```

## Statistical Testing

**Looped randomness tests** verify probabilistic constraints hold over many iterations:
```python
class TestForbiddenComboNotRolled(AffixTestBase):
    def test_forbidden_combo_not_rolled(self):
        pool = ["stun_immune", "root_immune", "enraged", "armored", ...]
        for _ in range(200):
            result = roll_affixes(2, pool)
            self.assertFalse(
                {"stun_immune", "root_immune"}.issubset(set(result)),
                f"Forbidden combo rolled: {result}"
            )
```

Used for: forbidden affix combos, defensive limits, container weight reduction ranges.

## Boundary Testing

**Threshold tests use parameterized-style lists** within a single test:
```python
test_cases = [
    (0, "dormant"), (29, "dormant"),
    (30, "awakening"), (59, "awakening"),
    (60, "active"), (89, "active"),
    (90, "critical"), (100, "critical"),
]
for failure, expected_state in test_cases:
    script.db.failure = float(failure)
    # ... assertion with f-string message for debugging
```

**Clamping tests** verify both upper and lower bounds:
```python
class TestDispositionClampedUpper(DispositionTestBase):
    def test_disposition_clamped_upper(self):
        # Stack all positive modifiers
        d = get_mob_disposition(self.mob, self.char1)
        self.assertLessEqual(d, 1.0)

class TestDispositionClampedLower(DispositionTestBase):
    def test_disposition_clamped_lower(self):
        # Stack all negative modifiers
        d = get_mob_disposition(self.mob, self.char1)
        self.assertGreaterEqual(d, -1.0)
```

## Negative Assertion Tests

**"This attribute should NOT exist" tests** enforce design constraints:
```python
class TestNoZoneLevelAttributes(ScalingTestBase):
    def test_no_zone_level_attributes(self):
        """ZoneObject does not have level_floor or level_cap."""
        zone = create_object(Object, key="zone", location=None)
        zone.db.zone_id = "test"
        self.assertIsNone(zone.db.level_floor)
        self.assertIsNone(zone.db.level_cap)

class TestMobHasNoBaseLevel(ScalingTestBase):
    def test_mob_has_no_base_level(self):
        """SoravelonMob should not have db.base_level in new design."""
        fresh_mob = create_object(SoravelonMob, key="fresh", location=self.room)
        self.assertIsNone(fresh_mob.db.base_level)
```

These prevent regression to a previous design (zone-level scaling was removed in favor of per-player scaling).

## Function Signature Tests

```python
class TestMaterialTierNoZoneParam(ScalingTestBase):
    def test_material_tier_function_signature(self):
        """get_material_tier takes only skill_score - no zone parameter."""
        import inspect
        sig = inspect.signature(get_material_tier)
        params = list(sig.parameters.keys())
        self.assertEqual(params, ["skill_score"])
```

## Coverage

**Requirements:** No formal coverage target enforced. No coverage tool configured.

**Coverage gaps:**
- Command layer (`commands/command.py`, `commands/default_cmdsets.py`) — no tests
- Web layer (`web/`) — no tests
- Loot tables (`world/loot_tables.py`) — no tests
- Named mob registry (`world/named_mob_registry.py`) — tested indirectly via area builder
- Zone registry (`world/zone_registry.py`) — tested indirectly via area builder
- Server lifecycle hooks (`server/conf/at_server_startstop.py`) — tested indirectly via `TestServerStartLoadsAreasDir`

## Test Types

**Unit Tests:**
- All current tests are unit tests
- Each test exercises a single function or method
- Real Evennia objects and Django database (not mocked)
- Fast execution — no network calls, no file I/O

**Integration Tests:**
- Area builder tests serve as light integration tests (zone creation + room creation + exit creation + registry)
- Layer swap tests (node system) exercise typeclass + script + room interaction

**E2E Tests:**
- Not used. No command-level or connection-level tests.

## Writing New Tests

**Follow this pattern:**

1. Create a base class extending `EvenniaTest` with shared setup
2. One test class per scenario, named `Test<WhatIsBeingTested>`
3. Import the system under test inside the test method
4. Use `create_object()` to create Evennia objects, set `db` attributes directly
5. Call the function, destructure `(success, msg)` if it uses that pattern
6. Assert on both the return value and any side effects (db changes, Django records)

**Test file template:**
```python
"""
Tests for <system> (Build Order Step N).
Tests written FIRST per TDD.
"""

from evennia.utils.test_resources import EvenniaTest
from evennia import create_object


class MyTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        # shared setup


class TestSpecificScenario(MyTestBase):
    def test_specific_scenario(self):
        from world.my_module import my_function
        result = my_function(self.char1, ...)
        self.assertEqual(result, expected)
```

---

*Testing analysis: 2026-03-24*
