# Soravelon Wave 6 Gathering, Crafting, Fishing, Recovery, and Travel Remediation

**Date:** 2026-04-22
**Depends on:** `docs/superpowers/plans/2026-04-22-wave5-items-loot-economy-remediation.md`

## Scope
Wave 6 audited the secondary-play loops and utility surface:

- crafting and processing
- gathering and fishing integration
- recovery/blessing support
- Dragon Courier travel

The scan found two real integrity gaps and one inventory-consistency issue inside crafting. All three were fixed in this pass.

## Files Changed

- `world/crafting_engine.py`
- `world/flight_engine.py`
- `tests/test_crafting.py`
- `tests/test_flight_engine.py`

## Findings Fixed

### High-value fix: crafting stations were authored but not rewarding real crafting
- `world/crafting_engine.py` already supported `has_station_bonus` in `calculate_craft_quality()`, but `craft_item()` never passed it through.
- Impact: crafting at the correct station worked as a gate, but not as a quality bonus, which made the crafting loop less rewarding than its authored design.
- Fix:
  - standard crafting now passes `has_station_bonus=True` when a valid stationed recipe is crafted
  - processing recipes now also treat the station as part of quality resolution

### High-value fix: processing recipes were ignoring raw-input quality entirely
- `calculate_processing_quality()` existed, but `craft_item()` never used it for `recipe_type == "processing"`.
- Impact: gathered high-quality raw materials did not meaningfully improve refined outputs, which flattened one of the intended gathering-to-crafting reward bridges.
- Fix:
  - processing recipes now use `calculate_processing_quality()`
  - consumed inputs now contribute a best-input raw quality signal
  - the station bonus now flows through that same processing path

### High-value fix: stackable ingredients were counted as one object, not many units
- `_check_ingredients()` previously matched objects, not quantities.
- `_consume_ingredients()` then deleted whole objects rather than decrementing stack counts.
- Impact: stacked ingredients could undercount during validation and overconsume during crafting, which is exactly the kind of hidden friction that makes utility loops feel unreliable.
- Fix:
  - ingredient checks now honor `InventoryItem.quantity`
  - consumption decrements stack quantities when possible instead of always deleting the item

### High-value fix: flight booking engine did not enforce physical departure location
- `commands/cmd_fly.py` correctly required the caller to be at a stop, but `world/flight_engine.book_flight()` itself trusted the supplied origin point id.
- Impact: any future direct caller, script, or accidental misuse could book travel from the wrong room.
- Fix:
  - `book_flight()` now verifies that the character is actually standing at the requested origin stop before it allows booking

## Audit Notes

### Already strong / protect with regression coverage
- The gathering/fishing/recovery surfaces are test-rich and mechanically more mature than many other game subsystems.
- Focused coverage already exercises:
  - node spawning and depletion
  - fishing state transitions
  - recovery state transitions
  - flight fare discounts and booking outcomes
- This made Wave 6 remediation lower-risk and easier to validate.

## Regression Coverage Added

### `tests/test_crafting.py`
- standard crafting passes station bonus into live quality calculation
- processing recipes use processing-quality calculation with raw input quality
- ingredient checks count stack quantity correctly
- ingredient consumption reduces stacks without deleting the whole item

### `tests/test_flight_engine.py`
- booking fails when the character is not physically at the requested departure stop

## Validation

- `python -m py_compile world/crafting_engine.py world/flight_engine.py tests/test_crafting.py tests/test_flight_engine.py`
- `python scripts/run_tests.py tests.test_crafting tests.test_flight_engine tests.test_gathering tests.test_fishing tests.test_recovery_engine`
  - Result: `133` tests passed
- `python scripts/smoke_start.py`
  - Result: passed

## Wave 6 Verdict

- **Wave 6 is materially healthier and more rewarding after remediation.**
- Crafting now actually respects the authored quality systems around stations, processing, and input quality.
- Utility-loop reliability is better because stack-based ingredients now behave sanely.
- Travel booking is safer because the engine itself enforces the departure location, not just the command layer.
