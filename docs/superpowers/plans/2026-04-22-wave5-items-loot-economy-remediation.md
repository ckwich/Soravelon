# Soravelon Wave 5 Items, Loot, Vendors, and Economy Remediation

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-wave4-progression-identity-remediation.md`

## Scope
Wave 5 audited the reward loop and fixed the highest-impact integrity issues in:

- loot payload truthfulness
- vendor stock persistence and resale behavior
- bank draft economy limits

## Files Changed

- `world/loot_tables.py`
- `world/vendor_engine.py`
- `world/banking.py`
- `tests/test_loot_tables.py`
- `tests/test_vendor_engine.py`
- `tests/test_banking.py`

## Findings Fixed

### Blocker: some loot-authored equipment was mechanically hollow
- Several loot tables authored drops as `item_type: "equipment"` but did not provide the fields needed to make those items function as real gear.
- Before this pass, drops like:
  - `raider_cutlass`
  - `iron_shortsword`
  - `alpha_fang_necklace`
  - `raider_boarding_axe`
  would spawn with the equipment typeclass but without a proper slot or meaningful combat/stat payload.
- `world/loot_tables.py` now supports tiered equipment authoring fields:
  - `material_tier_by_tier`
  - `damage_min_by_tier`
  - `damage_max_by_tier`
  - `armor_value_by_tier`
  - `stat_bonuses_by_tier`
- The authored drops above now include real slot/stat/damage metadata, so looted gear is actually worth equipping.

### High-value fix: player-sold vendor stock could overwrite itself or hide authored stock
- `world/vendor_engine.py` previously keyed player-sold items only by `item_id` / name-derived ids.
- Impact:
  - selling identical items could overwrite prior stock instead of stacking quantity
  - selling something with the same id as authored catalog stock could replace the base vendor item in merged stock views
- The vendor engine now:
  - stacks truly identical player-sold items with `stock_quantity`
  - avoids collisions with authored catalog ids by minting stable `used_*` stock ids when needed
  - decrements quantity correctly on purchase
  - surfaces stock count in `view`

### High-value fix: bank drafts bypassed the transaction cap
- `world/banking.py` enforced `MAX_TRANSACTION` for deposit/withdraw, but `issue_draft()` could still create larger drafts.
- This undercut the intended per-transaction economy guardrail.
- `issue_draft()` now enforces the same cap.

### Improvement folded into the fix: resale templates are more faithful
- Player-sold vendor entries now preserve richer item metadata, including non-weapon payloads like `use_effect`, instead of only a narrow combat-focused subset.
- Vendor bookkeeping fields such as `stock_quantity` are stripped before a purchased item is spawned back into the world.

## Regression Coverage Added

### `tests/test_loot_tables.py`
- equipment loot preserves authored slot/stat/damage metadata
- all authored equipment drops must carry real equipment payload fields

### `tests/test_vendor_engine.py`
- buying from player stock decrements quantity instead of deleting the whole entry
- identical sold items stack correctly
- player-sold stock no longer overwrites authored catalog ids
- consumable resale payloads stay intact
- stock quantity is shown in `view`

### `tests/test_banking.py`
- draft issuance rejects amounts over `MAX_TRANSACTION`

## Validation

- `python -m py_compile world/vendor_engine.py world/banking.py world/loot_tables.py tests/test_vendor_engine.py tests/test_banking.py tests/test_loot_tables.py`
- `python scripts/run_tests.py tests.test_vendor_engine tests.test_banking tests.test_loot_tables tests.test_item_spawner tests.test_inventory_engine tests.test_content_authoring`
  - Result: `142` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

## Wave 5 Verdict

- **Wave 5 is materially safer for launch.**
- Looted gear now matches its authored fantasy, vendor resale no longer destroys or hides stock, and draft issuance honors the same economy cap as the rest of the bank surface.
- The reward loop is more trustworthy both mechanically and economically than it was before this pass.
