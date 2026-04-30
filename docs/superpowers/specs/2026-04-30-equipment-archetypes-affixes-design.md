# Equipment Archetypes And Affixes Design

## Goal

Give Soravelon reusable equipment drop foundations without making area authors
copy damage, armor, stat, and affix payloads by hand for every mob.

## Design

Loot tables remain builder-safe literal dictionaries. A drop can keep using the
legacy explicit equipment payload, or it can add:

```python
"equipment_archetype": "agile_blade",
"affix_profile": "bandit_weapon",
"affix_count_by_tier": [0, 0, 1, 1, 1],
```

`world.loot_tables.roll_loot()` still owns drop chance, weighted selection, mob
rarity extra rolls, zone overrides, and skill-based tier selection. When a
selected drop includes `equipment_archetype`, it delegates expansion to
`world.equipment_archetypes.build_equipment_from_archetype()`.

`world.equipment_archetypes` owns:

- `EQUIPMENT_ARCHETYPES`: reusable base gear curves such as agile blades,
  cleaving axes, guarded mail, and beast talismans.
- `EQUIPMENT_AFFIXES`: bounded stat/damage/armor/value modifiers with names
  and description fragments.
- `EQUIPMENT_AFFIX_PROFILES`: weighted pools that make different sources feel
  different without changing the runtime contract.

## Balance Rules

- Drop quality still comes from relevant player skill/domain score, not visible
  level or zone level.
- Affix counts are intentionally small. Basic drops usually get no affix, while
  mid/high tier drops can get one; named/event gear can later use richer
  profiles.
- Dropped gear remains competitive, but the crafting docs' masterwork edge is
  preserved. Masterwork gear should eventually win on intentionality, reliable
  ceiling, naming, and Legacy history.

## Provenance

Generated equipment records lightweight `drop_provenance` data when the drop
comes from a mob. Inspection can show `Recovered From`, and the payload leaves
room for later in-game date, node event, named-mob, and Legacy stamps.

## Builder Notes

Builder tools should expose the new optional loot-drop fields without requiring
them:

- `equipment_archetype`
- `affix_profile`
- `affix_count`
- `affix_count_by_tier`

The builder must continue to support legacy explicit equipment fields:

- `equip_slot`
- `scaling_stat`
- `material_tier_by_tier`
- `damage_min_by_tier`
- `damage_max_by_tier`
- `armor_value_by_tier`
- `stat_bonuses_by_tier`

Both styles are valid. Archetype-backed drops are preferred for new generic
equipment; explicit payloads are still appropriate for hand-tuned named rewards.
