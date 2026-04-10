# Coding Conventions

**Analysis Date:** 2026-03-24

## Naming Patterns

**Files:**
- `snake_case.py` for all modules: `world_state.py`, `mob_disposition.py`, `inventory_engine.py`
- Test files: `test_<module_name>.py` — e.g., `tests/test_banking.py`
- Typeclasses: `<plural_noun>.py` — e.g., `typeclasses/characters.py`, `typeclasses/mobs.py`

**Classes:**
- PascalCase with `Soravelon` prefix for game-specific typeclasses: `SoravelonRoom`, `SoravelonMob`, `SoravelonItem`, `SoravelonExit`
- PascalCase without prefix for Evennia compatibility stubs: `Room`, `Object`, `Character`
- Django models: PascalCase without prefix: `FactionStanding`, `BankTransaction`, `InventoryItem`
- Test classes: one class per test scenario, PascalCase describing the assertion: `TestDepositSuccess`, `TestStandingMaxMapsTo06`

**Functions:**
- `snake_case` for all functions and methods
- Engine functions use verb-first: `deposit()`, `withdraw()`, `pick_up()`, `drop_item()`, `equip_item()`
- Getter functions: `get_balance()`, `get_mob_disposition()`, `get_carry_state()`
- Internal helpers: `_` prefix: `_record_transaction()`, `_get_group_state()`, `_find_existing_stack()`
- Callbacks: `at_` prefix per Evennia convention: `at_object_creation()`, `at_traverse()`, `at_death()`

**Variables:**
- `snake_case` throughout
- Module-level constants: `UPPER_SNAKE_CASE` — `MAX_GROUP_SIZE`, `VALID_LOOT_MODES`, `ALL_DIMENSIONS`
- Data tables: `UPPER_SNAKE_CASE` dicts — `ANCESTRY_FACTION_MODIFIERS`, `CONTAINER_WEIGHT_RANGES`

**Types/Enums:**
- No Python enums used. Constants are tuples or dicts at module level.
- Rarity tiers are string constants: `"normal"`, `"magic"`, `"rare"`, `"legendary"`
- Node states are string constants: `"dormant"`, `"awakening"`, `"active"`, `"critical"`

## Code Style

**Formatting:**
- No formatter configuration detected (no `.prettierrc`, `pyproject.toml`, or `setup.cfg`)
- 4-space indentation (Python standard)
- Lines generally under 100 characters; long lines wrapped with parenthetical continuation
- Single blank line between functions within a module; double blank line between top-level classes

**Linting:**
- No linter configuration detected
- Code follows PEP 8 consistently
- Imports at top of file; lazy imports inside functions when avoiding circular dependencies

**Docstrings:**
- Module-level docstrings on every file describing purpose and key behaviors
- Function docstrings on public functions, one-liners for simple getters
- Performance notes in docstrings where relevant (e.g., `world/mob_disposition.py` line 12: "get_mob_disposition() makes up to 2 DB reads")

## Import Organization

**Order:**
1. Standard library (`random`, `datetime`, `inspect`)
2. Django imports (`django.db.models`, `django.utils.timezone`)
3. Evennia imports (`evennia`, `evennia.utils.test_resources`)
4. Local imports (`world.models`, `typeclasses.rooms`)

**Lazy Imports:**
- Use inside functions to break circular dependencies. This is the standard pattern:
```python
def some_function():
    from typeclasses.objects import SoravelonItem  # lazy to avoid circular
    ...
```
- Examples: `world/banking.py` line 197 (lazy import of `create_object` inside `issue_draft`), `world/inventory_engine.py` line 136 (lazy import of `SoravelonKeyringItem`)

**Path Aliases:**
- None. All imports use full dotted paths.

## The `(bool, str)` Return Tuple Pattern

**This is the primary error-communication pattern.** Nearly every engine function that can fail returns `(success: bool, message: str)`.

**Pattern:**
```python
def deposit(character, amount, description="deposit"):
    if amount <= 0:
        return False, "Amount must be positive."
    # ... success path ...
    return True, f"Deposited {amount} Scales. Banked balance: {account.balance}."
```

**Where used:**
- `world/banking.py`: `deposit()`, `withdraw()`, `deduct_from_bank()`, `credit_to_bank()`, `issue_draft()`, `redeem_draft()`, `create_debt()`, `pay_debt()`
- `world/inventory_engine.py`: `pick_up()`, `drop_item()`, `put_in_container()`, `take_from_container()`, `equip_item()`, `unequip_item()`
- `world/group_engine.py`: `send_group_invite()`, `accept_group_invite()`, `decline_group_invite()`, `leave_group()`, `kick_from_group()`, `set_loot_mode()`
- `typeclasses/objects.py`: `can_drop()`, `can_equip()`, `can_accept()`, `can_be_sold()`

**Convention:** Always destructure at call site:
```python
success, msg = deposit(self.char1, 500)
```

**For the `can_*` methods** on typeclasses, the message is `None` on success:
```python
can, msg = item.can_drop(character)
# can=True, msg=None → allowed
# can=False, msg="You can't drop a quest item." → blocked
```

## The `(bool, str|None)` Reveal Pattern

Used for one-shot reveal messages on mobs:
```python
immune, msg = mob.has_immunity("burn")
# immune=True, msg="The wolf shrugs off the flames." (first time)
# immune=True, msg=None (subsequent times)
```
See `typeclasses/mobs.py` lines 100-119.

## SaverDict Copy Pattern

**Critical performance pattern.** Evennia's `db` attributes backed by `SaverDict` re-pickle the entire dict on every key mutation. When modifying dicts stored in `db`, copy to a plain dict first, mutate, then assign back in a single write.

**Pattern from `world/world_state.py` line 168:**
```python
# Copy to plain dict to avoid SaverDict N+1 repickle.
scores = dict(character.db.domain_scores or {})

for domain in ALL_DOMAINS:
    # ... mutate scores dict ...
    scores[domain] = new_score

# Single DB write for all domain score changes
character.db.domain_scores = scores
```

**When to use:** Any time you modify a dict or list stored on `character.db.*`. Do NOT do:
```python
# BAD — repickles entire dict on every iteration
for domain in domains:
    character.db.domain_scores[domain] = new_val
```

## F() Expression Pattern for Atomic Updates

**Used for all bank balance modifications** to prevent race conditions under concurrent access.

**Pattern from `world/banking.py`:**
```python
from django.db.models import F

# Atomic increment — safe under concurrent modifications
BankAccount.objects.filter(id=account.id).update(balance=F('balance') + amount)
account.refresh_from_db()  # always refresh after F() update

# Atomic check-and-deduct — rows_updated==0 means insufficient balance
rows_updated = BankAccount.objects.filter(
    id=account.id, balance__gte=amount
).update(balance=F('balance') - amount)
if not rows_updated:
    return False, "Insufficient funds."
```

**Also used in `world/world_state.py` line 236** for standing modification with `Greatest`/`Least` clamping:
```python
FactionStanding.objects.filter(id=record.id).update(
    standing=Greatest(-100000, Least(100000, F('standing') + amount))
)
```

**Rule:** Always call `.refresh_from_db()` after any `F()` update to get the new value.

## Lazy Creation Pattern

**Django model records are created only on first use.** No record = default/neutral state.

**Examples:**
- `world/banking.py`: `get_or_create_account()` — bank account created on first deposit
- `world/world_state.py`: `modify_standing()` — `FactionStanding` created on first interaction
- `world/world_state.py`: `update_zone_attunement()` — `ZoneAttunement` via `update_or_create()`
- `world/inventory_engine.py`: `_get_or_create_inventory_record()` — on pickup

**Getter functions return safe defaults when no record exists:**
```python
def get_balance(character):
    try:
        return BankAccount.objects.get(character_id=character.id).balance
    except BankAccount.DoesNotExist:
        return 0

def get_standing(character, faction_id):
    try:
        record = character.faction_standings.get(...)
        return record.standing
    except FactionStanding.DoesNotExist:
        return 0
```

## The `getattr` Trap on `db` Attributes

**Evennia's `db` handler returns `None` for unset attributes** — it does not raise `AttributeError`. This means `getattr(obj.db, 'foo', default)` does NOT work as expected because `obj.db.foo` returns `None` (not missing).

**Safe access pattern used throughout:**
```python
# Correct — handles both None and missing
carried = getattr(character.db, 'carried_scales', 0) or 0

# Also correct
reputation = float(getattr(character.db, 'reputation_score', 0.0) or 0.0)
```

**The `or 0` / `or 0.0` suffix is essential** because `getattr` may return `None` for an attribute that exists but was set to `None`.

## Data Storage Patterns

**When to use `db.*` (Evennia attributes):**
- Intrinsic character state: `db.ancestry`, `db.carried_scales`, `db.reputation_score`
- Mob configuration: `db.rarity`, `db.base_disposition`, `db.faction`
- Room metadata: `db.zone_id`, `db.awakening_desc`
- All typeclass state initialized in `at_object_creation()`

**When to use `ndb.*` (volatile, not persisted):**
- Session accumulators: `ndb.domain_xp_combat` (batch-committed periodically)
- Group state: `ndb.group_state`, `ndb.group_leader_id` (groups dissolve on disconnect)
- Combat caches: `ndb.combat_scales` (per-encounter, cleared on death)
- One-shot reveals: `ndb.revealed_affixes` (reset on mob death)
- Pending invites: `ndb.pending_group_invite`

**When to use Django models (`world/models.py`):**
- Relational data between entities: `FactionStanding`, `ZoneAttunement`
- Transaction logs (immutable): `BankTransaction`, `NodeEventLog`, `WorldEventLog`
- Inventory metadata: `InventoryItem` (links Evennia objects to character inventory)
- Financial state: `BankAccount`, `RecurringPayment`, `DebtRecord`

**Rule from CLAUDE.md:** "All game logic lives in `world/` modules; typeclasses call into them." Typeclasses are thin wrappers; the engines do the work.

## Tags Pattern

**Evennia tags are used extensively for categorized flags:**
```python
# Setting tags
room.tags.add("test_zone", category="zone_id")
room.tags.add("clearing", category="room_type")
mob.tags.add("enraged", category="mob_affix")

# Checking tags
room.tags.get("burn_enhanced", category="node_effect")

# Querying by tag
ScriptDB.objects.get_by_tag("node_script", category="script_type")
```

**Tag categories in use:**
- `zone_id` — zone membership for rooms
- `room_type` — room classification
- `room_id` — idempotent room lookup
- `node_layer` — `"active"` / `"inactive"` for Layer 1 rooms
- `node_effect` — active node effects on rooms
- `node_state` — current node phase on rooms
- `mob_affix` — active affixes on mobs
- `item_type` — item classification
- `script_type` — script classification
- `character_type` — `"player_character"` for queryset filtering
- `object_type` — `"zone_object"` for zone objects

## Module Organization

**Each `world/` engine module follows this layout:**
1. Module docstring
2. Imports
3. Constants / data tables
4. Internal helper functions (prefixed with `_`)
5. Public API functions grouped by feature (with comment headers)
6. TickerHandler callbacks at the bottom

**Section separators** use comment blocks:
```python
# ---------------------------------------------------------------------------
# Container operations
# ---------------------------------------------------------------------------
```

## Error Messages

- Player-facing messages use Evennia color codes: `|g` green, `|y` yellow, `|r` red, `|w` white, `|n` reset
- Error messages are descriptive and actionable: `"Unequip sword before dropping it."`, `"The way is locked. You need the right key."`
- Internal error returns use f-strings with context: `f"Insufficient funds. Banked balance: {account.balance} Scales."`

---

*Convention analysis: 2026-03-24*
