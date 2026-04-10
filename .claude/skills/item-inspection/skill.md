---
name: item-inspection
description: Item inspection and comparison commands — appraisal skill-gated stat display with rarity/tier DC formula
---

## Activation

This skill triggers when editing these files:
- `commands/cmd_inspect.py`

Keywords: inspect, compare, appraise, appraisal, item stats, RARITY_DC, appraisal DC

---

You are working on **item inspection commands** (`commands/cmd_inspect.py`) — appraisal skill-gated item stat display and side-by-side comparison.

## Key Files
- `commands/cmd_inspect.py` — CmdInspect, CmdCompare, `_get_appraisal_dc()`, `_get_item_stats()`, `_format_stats()`, `RARITY_DC`
- `commands/default_cmdsets.py` — Both commands registered in `CharacterCmdSet`
- `world/skill_engine.py` — `get_skill_value()` for appraisal check, `record_skill_use()` / `accumulate_skill_use()` for passive gain

## Key Concepts
- **Appraisal DC formula:** `RARITY_DC[rarity] + (material_tier * 5)`. Rarity values: common/normal=0, magic=15, rare=30, legendary=45
- **CmdInspect:** Searches inventory + room. If appraisal skill >= DC, shows full stats via `_format_stats()` and records skill use. Otherwise shows desc + "skill too low" message
- **CmdCompare:** Parses `<item1> to <item2>` or `<item1> <item2>`. Requires appraisal >= DC for BOTH items. Shows side-by-side stat table
- **`_get_item_stats()` extracts:** Damage (min-max), Armor, stat_bonuses, Slot, Rarity, Value (Scales), Material Tier — skips zero/empty values
- **CmdInspect aliases:** `appraise_item`, `examine`

## Critical Rules
1. **Stats require appraisal check** — basic desc is always visible via `look`; `inspect` gates mechanical stats behind skill DC
2. **Compare requires BOTH items to pass DC** — if either fails, shows generic rejection
3. **Skill recording on success** — `record_skill_use(character, "appraisal")` called only on successful inspect, enabling passive skill gain
4. **Item search is global** — `self.caller.search()` checks both inventory and room (Evennia default). Not restricted to inventory
5. **Items in `Items` help_category** — `help_category = "Items"` for inspect/compare

## References
- **Item Typeclasses:** `typeclasses/objects.py` — `db.damage_min`, `db.damage_max`, `db.armor_value`, `db.stat_bonuses`, `db.rarity`, `db.material_tier`, `db.equipment_slot`, `db.value_scales`
- **Skill Engine:** `world/skill_engine.py` — `get_skill_value()` and skill use recording

---
**Last Updated:** 2026-04-05
