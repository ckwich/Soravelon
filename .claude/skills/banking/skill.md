---
name: banking
description: Banking engine — deposits, withdrawals, recurring payments, Consortium Drafts, underworld debt with playtime countdown
---

## Activation

This skill triggers when editing these files:
- `world/banking.py`
- `world/models.py`
- `commands/bank*.py`
- `tests/test_banking.py`

Keywords: banking, bank, deposit, withdraw, scales, draft, debt, recurring payment, death penalty

---

You are working on **Soravelon's banking engine** (`world/banking.py`).

## Key Files
- `world/banking.py` — All banking logic (stateless functions, no classes)
- `world/models.py` — `BankAccount`, `BankTransaction`, `RecurringPayment`, `DebtRecord`
- `typeclasses/scripts.py` — Debt timer decrement via `decrement_debt_timer`
- `typeclasses/characters.py` — `get_balance` used in character display
- `server/conf/at_server_startstop.py` — Registers `banking_payment_tick` as periodic callback
- `tests/test_banking.py` — Comprehensive test suite

## Key Concepts
- **Dual currency locations:** `character.db.carried_scales` (on-person) vs `BankAccount.balance` (banked). Deposit/withdraw moves between them.
- **Per-transaction cap:** `MAX_TRANSACTION = 100000` — both `deposit()` and `withdraw()` reject amounts exceeding this limit to prevent economy exploits.
- **Consortium Drafts:** Physical bearer instruments — `issue_draft` deducts from bank and creates a `SoravelonItem` with tag `consortium_draft`; `redeem_draft` credits bank and destroys the item+InventoryItem record.
- **Recurring payments:** `payment_type` keyed per character. Failed payment enters grace period (1 interval). Second failure sets `lapsed=True, active=False`.
- **Underworld debt:** Playtime-based countdown (`deadline_playtime_seconds`). One active debt per character (app-level check). Timer hits 0 → status becomes `"hunted"`.
- **Transaction log:** Every balance change creates an immutable `BankTransaction` with `balance_after` snapshot.
- **Death penalty:** `on_character_death()` drops 20% of `carried_scales` into the player's corpse (lootable) and wipes all uncommitted session XP (`ndb.session_xp`). Called from `combat_engine.handle_player_death()`. Banked Scales are safe.

## Critical Rules
1. **Always use `F()` expressions** for balance updates — never read-modify-write. Withdrawal uses `filter(balance__gte=amount).update()` for atomic overdraft protection.
2. **All functions return `(bool, str)` tuples** — follow this for any new banking function.
3. **`refresh_from_db()` after every `F()` update** — the in-memory model is stale after `update()`.
4. **Lazy account creation** — `get_balance` returns 0 for missing accounts; `get_or_create_account` for mutations.
5. **Per-transaction cap enforced** — `MAX_TRANSACTION = 100000` checked in both `deposit()` and `withdraw()` before any balance mutation. Do not bypass this limit.
6. **Debt status values:** `"active"`, `"paid"`, `"hunted"`, `"forgiven"` — only one `"active"` debt per character at a time.
7. **Draft lifecycle:** deduct → create object + InventoryItem → on redeem: credit + delete both object and InventoryItem.
8. **`banking_payment_tick`** is registered as a server periodic callback — do not call `process_recurring_payments` from commands directly.
9. **Death penalty only hits carried Scales** — banked balance is untouched. `handle_carried_scales_on_death()` computes `int(carried * 0.20)` and deducts from `db.carried_scales`. Dropped Scales are placed on the corpse object (`obj.db.scales`).

## References
- **Models:** `world/models.py` (lines 171-256)
- **Tests:** `tests/test_banking.py`
- **Server hooks:** `server/conf/at_server_startstop.py`
- **Combat integration:** `world/combat_engine.py` — `handle_player_death()` calls `on_character_death()`

---
**Last Updated:** 2026-04-10
