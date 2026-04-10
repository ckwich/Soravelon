---
name: gathering-engine
description: Gathering node lifecycle — zone-wide pool spawning, depletion with respawn scheduling, skill-gated visibility, GatheringPoolScript tick cleanup, and 9 player gathering commands
---

## Activation

This skill triggers when editing these files:
- `world/gathering_engine.py`
- `commands/cmd_gathering.py`
- `commands/cmd_prospect.py`
- `commands/cmd_fishing.py`
- `commands/cmd_tools.py`
- `typeclasses/objects.py`

Keywords: gathering, gather, node, mining, herbalism, woodcutting, foraging, fishing, skinning, harvest, chop, forage, fish, butcher, mine, prospect, survey, repair, GatheringNode, GatheringPoolScript, gathering pool, deplete, respawn node, butcher yields, gathering command, prospect_scan, tool repair, tool slot, equip tool, unequip tool, equipped_tools, catch_fish, complete_gather

---

You are working on **the gathering engine** (`world/gathering_engine.py`) and **gathering commands** (`commands/cmd_gathering.py`, `commands/cmd_prospect.py`, `commands/cmd_fishing.py`, `commands/cmd_tools.py`) — zone-wide gathering pool lifecycle, the `GatheringNode` typeclass, and player-facing gathering commands.

## Key Files
- `world/gathering_engine.py` — Pool script, node spawning, depletion, respawn scheduling, room flag setup, `catch_fish()`, `complete_gather()`, `gather_from_node()`, `BUTCHER_YIELDS`, `get_butcher_yields()`, `prospect_scan()`, `CARDINAL_DIRECTIONS`
- `commands/cmd_gathering.py` — 5 commands: CmdMine, CmdHarvest, CmdChop, CmdForage, CmdButcher + `_BaseGatherCmd` shared base class (thin delegates to engine)
- `commands/cmd_prospect.py` — CmdProspect (prospect/survey) for straight-line node scanning + CmdRepair for tool durability restoration at workbench
- `commands/cmd_fishing.py` — CmdFish (active + idle modes) and CmdReel (thin delegate to engine)
- `commands/cmd_tools.py` — CmdTools: view, equip, and unequip gathering tools from dedicated tool slots
- `typeclasses/objects.py` — `GatheringNode` typeclass (extends `SoravelonObject`, NOT `SoravelonItem` — cannot be picked up), `CorpseContainer` (consumed by CmdButcher)
- `world/material_definitions.py` — `MATERIAL_REGISTRY`, `GATHERING_CATEGORIES`, `VISIBILITY_THRESHOLDS`, `GATHER_DELAY_BY_TIER`, `TOOL_DURABILITY` consumed for node creation, visibility, delay, and repair
- `world/room_state.py` — `add_room_flag()` sets persistent gathering flags on eligible rooms; `SENSE_DISPLAY` already wires gathering hints (mineral_deposits, rich_soil, dense_foliage, water_source)
- `world/skill_engine.py` — `get_skill_value()` used for visibility and delay reduction; `accumulate_skill_use()` for passive skill gain
- `world/area_builder.py` — `gathering_pool()` DSL stores pool defs; `build()` calls `initialize_zone_gathering()`
- `commands/default_cmdsets.py` — All 10 gathering commands registered in `CharacterCmdSet`

## Key Concepts
- **Engine owns all game state mutations (D-07 thin-command pattern):** `catch_fish()` and `complete_gather()` in `gathering_engine.py` handle node depletion, item creation, quality calc, tool durability, and skill XP. Commands only handle validation, UI flow, and fishing state management
- **`catch_fish()` returns 5-tuple:** `(success, msg, item, bait_consumed, tool_broken)` — command reads tuple to decide fishing state (clear bait ref, stop fishing on tool break/depletion)
- **`complete_gather()` returns 4-tuple:** `(success, msg, items_list, tool_broken)` — command reads tuple for UI display only. All mutations already happened in engine
- **`gather_from_node()` is low-level:** Decrements `gathers_remaining`, auto-depletes at 0. Returns `(bool, material_id)`. Called internally by `catch_fish()` and `complete_gather()`
- **10 gathering commands total:** mine, harvest, chop, forage, butcher (cmd_gathering.py), fish, reel (cmd_fishing.py), prospect/survey, repair (cmd_prospect.py), tools (cmd_tools.py) — all registered in CharacterCmdSet
- **Tool slots are SEPARATE from combat equipment slots (D-20):** `character.db.equipped_tools` dict maps slot keys to item IDs. 5 tool slots: `tool_pickaxe`, `tool_sickle`, `tool_hatchet`, `tool_knife`, `tool_rod`. These are independent of combat `VALID_SLOTS` in the inventory engine. CmdTools manages equip/unequip via `VALID_TOOL_SLOTS` and `FRIENDLY_NAME_TO_SLOT` mappings
- **Tool lookup:** `_BaseGatherCmd._find_tool()` searches `character.contents` for items with matching `item_tag` category tag
- **GatheringNode is NOT an item:** Extends `SoravelonObject` (not `SoravelonItem`). Has `locks.add("get:false()")` — cannot be picked up. Players interact via gathering commands
- **Skill-gated visibility:** `get_display_name()` returns `None` if looker's gathering skill is below `VISIBILITY_THRESHOLDS` for the node's visibility level (low/mid/high)
- **GatheringPoolScript pattern:** Dynamic script class created via `_create_script_class()` to avoid import-time typeclass resolution (same pattern as CombatScript). Cached in `_cls_cache`
- **Pool script is self-ticking (120s):** `at_repeat()` prunes dead nodes and spawns replacements up to `max_active`. Attached to zone object, one per pool
- **Anti-repeat spawning:** `last_depleted_room_id` tracks where last node was depleted. New spawns exclude that room (per D-03 / pitfall 5)
- **Depletion → delayed respawn:** `deplete_node()` deletes node, schedules `spawn_node_in_pool()` via `evennia.utils.delay()` with `respawn_minutes ± respawn_variance` (minimum 30s floor)
- **Room state flags:** `_set_room_flags_for_pool()` maps pool_type → persistent flag: ore→mineral_deposits, herb/forage→rich_soil, wood→dense_foliage, fish→water_source. Duration -1 (never decays)
- **_BaseGatherCmd pattern:** Shared base class with `gather_skill`, `gather_verb`, `required_tool`, `target_category` overrides. Handles tool lookup (by `item_tag` category tag in inventory), node finding, skill-based delay (min 40% of base), and `evennia.utils.delay()` callback with move-cancellation guard
- **prospect_scan() — straight-line scanning, NOT BFS:** Walks cardinal directions (N/S/E/W) via `ex.key.lower() == direction` exit matching. Range 2-6 rooms based on highest gathering skill (base 2, +1 per 25 skill). Returns `[{"direction", "distance", "node"}]`
- **CmdRepair — tool durability restoration:** Requires workbench (`crafting_workbench` station tag). Repair amount: `10 + smithing/5`. Looks up max durability from `TOOL_DURABILITY` dict
- **Bonus quantity at high skill:** 25% chance at skill 50+, 50% chance at skill 80+ for an extra gathered item (handled inside `complete_gather()`)
- **Tool durability consumed per gather:** Handled inside `catch_fish()` and `complete_gather()`. Tool breaks at 0 durability
- **Butcher system:** CmdButcher overrides `_find_node()` to find `CorpseContainer` objects only. `_gather_callback()` extracts materials from `BUTCHER_YIELDS`. Mob key → yield list with fallback (exact match → base name → generic meat+bone)

## Critical Rules
1. **GatheringNode extends SoravelonObject, not SoravelonItem** — it is a room fixture, not a pickupable item
2. **Commands are thin delegates (D-07)** — `_catch_fish` delegates to `gathering_engine.catch_fish()`, `_gather_callback` delegates to `gathering_engine.complete_gather()`. Commands handle only validation, move-cancel checks, and fishing state (bait ref, stop fishing). Zero game state mutations in command layer
3. **Pool script uses dynamic class pattern** — `GatheringPoolScript.get_class()` returns cached dynamic subclass. Never instantiate `GatheringPoolScript` directly
4. **Respawn excludes depleted room** — `last_depleted_room_id` prevents node from respawning in the same room it was just depleted from
5. **Room flags are persistent (duration -1)** — gathering room flags never decay; they mark eligible gathering rooms permanently
6. **`initialize_zone_gathering()` is called from `AreaBuilder.build()`** — reads `zone_obj.db.gathering_pools` list, spawns initial nodes for each pool definition
7. **prospect_scan uses straight-line walking, not BFS** — matches exit by `ex.key.lower() == direction`, consistent with area_builder exit creation pattern
8. **Move cancels gathering** — `_BaseGatherCmd` stores `start_room` and compares in callback. Movement invalidates in-progress gather
9. **Butcher yields use fallback chain** — exact `mob_key` → `rsplit("_", 1)[0]` base name → generic (raw_meat + bone_fragment). New mob yields go in `BUTCHER_YIELDS` dict
10. **Lazy imports throughout** — `evennia`, `typeclasses.objects`, `world.material_definitions`, `world.room_state` imported inside functions
11. **Tool slots are separate from combat slots** — `character.db.equipped_tools` dict (tool slot → item ID). CmdTools copies dict before mutation to trigger SaverDict persistence
12. **CmdButcher only targets corpses** — `_find_node()` only finds `CorpseContainer` objects, not hide-type GatheringNodes

## References
- **Material Registry:** `world/material_definitions.py` — material taxonomy, visibility thresholds, gathering categories, delay by tier, tool durability
- **Room State:** `world/room_state.py` — `add_room_flag()` for gathering room flags, `SENSE_DISPLAY` for Sense gathering hints
- **Skill Engine:** `world/skill_engine.py` — `get_skill_value()` for visibility/delay, `accumulate_skill_use()` for progression
- **Crafting Engine:** `world/crafting_engine.py` — `calculate_craft_quality()` used for gathered item quality
- **Area Builder:** `world/area_builder.py` — `gathering_pool()` DSL method and `build()` integration
- **Item Spawner:** `world/item_spawner.py` — `create_item_from_template()` used by engine to create items
- **Equipment Catalog:** `world/areas/equipment_catalog.py` — tool item definitions with `tool_slot` and `tool_tag` fields

---
**Last Updated:** 2026-04-06
