---
name: ancestry-engine
description: Four playable ancestries (Human, Kau'roran, Veth, Selvar) with innate traits, starter kits, domain modifiers, and starting faction standings
---

## Activation

This skill triggers when editing these files:
- `world/ancestry_engine.py`
- `typeclasses/characters.py`

Keywords: ancestry, human, kauroran, veth, selvar, coat, set_ancestry, ancestry trait, starting standing, starter kit

---

You are working on **the ancestry engine** (`world/ancestry_engine.py`) — static trait data, starter kits, and character creation logic for four playable ancestries.

## Key Files
- `world/ancestry_engine.py` — Ancestry traits, starting standings, starter kits, `set_ancestry()`, `get_ancestry_trait()`
- `world/mob_disposition.py` — `ANCESTRY_FACTION_MODIFIERS` table consumes ancestry for disposition math
- `world/world_state.py` — `modify_standing()` called by ancestry engine to apply starting faction standings
- `world/item_spawner.py` — `create_item_from_template()` used by `_grant_starter_kit()` to create starter items
- `typeclasses/characters.py` — `_send_new_player_guidance()` sends context-sensitive hints to new players at login

## Key Concepts
- **Pure Python constants, no DB models:** `ANCESTRY_TRAITS` dict holds all trait data. No Django models needed
- **One-time ancestry assignment:** `set_ancestry()` sets `character.db.ancestry` once during character creation. Rejects if already set
- **Selvar coat system:** Selvar ancestry requires a coat choice (`"summer"` or `"winter"`) stored as `character.db.selvar_coat`. Each coat grants different stat bonuses
- **Starting faction standings:** `ANCESTRY_STARTING_STANDING` maps ancestry → faction → standing amount. Applied via `modify_standing()` at creation
- **Selvar special case:** Gets `SELVAR_ALL_FACTIONS_PENALTY` (-5000) to all known factions + `SELVAR_GUILD_OFFSET` (+2500) to guilds
- **Starter kits:** `STARTER_KITS` dict maps ancestry → list of inline item template dicts. `_grant_starter_kit()` creates items via `create_item_from_template()` after standings are applied. Also grants 50 Scales via `character.db.carried_scales`. Per-item error handling so one failure doesn't block the whole kit
- **Starter kit items defined inline:** All item templates (weapons, armor, potions) are plain dicts in `ancestry_engine.py` — no external equipment catalog dependency
- **New player guidance:** `Character._send_new_player_guidance()` sends tiered hints at login: ancestry prompt → guild exploration hint → NPC conversation hint. Skipped for experienced players (backend_level > 1 or 2+ domain_scores)
- **Domain modifiers:** Each ancestry has per-domain modifier flags (combat/naturalism/subterfuge) consumed by future combat/progression systems
- **Trait lookup API:** `get_ancestry_trait(character, trait_name)` provides safe access without importing the full traits dict

## Valid Values
- **Ancestries:** `"human"`, `"kauroran"`, `"veth"`, `"selvar"` (`VALID_ANCESTRIES`)
- **Coats:** `"summer"`, `"winter"` (`VALID_COATS`, selvar only)
- **Known factions at creation:** empire, wardens, kauroran, consortium (resistance excluded — applied later via hidden system)

## Critical Rules
1. **Ancestry is immutable after creation** — `set_ancestry()` rejects if `character.db.ancestry` is already set
2. **All functions return `(bool, str)` tuples** — follows repo-wide convention
3. **Lazy import of `modify_standing`** — avoids circular dependency with `world_state`
4. **Lowercase ancestry IDs everywhere** — keys in `ANCESTRY_TRAITS` are lowercase; callers must match
5. **Coat is required for selvar** — `set_ancestry("selvar")` without coat returns failure
6. **`set_ancestry()` call order:** set `db.ancestry` → `_apply_starting_standings()` → `_grant_starter_kit()` → `apply_ancestry_skill_seeds()`. Starter kit depends on item_spawner being importable
7. **Starter kit uses lazy import of item_spawner** — gracefully skips if unavailable (logs warning)

## References
- **Faction Standings:** `world/world_state.py` — `modify_standing()` used for starting standings
- **Disposition Math:** `world/mob_disposition.py` — `ANCESTRY_FACTION_MODIFIERS` table
- **Item Spawner:** `world/item_spawner.py` — `create_item_from_template()` used by starter kits

---
**Last Updated:** 2026-04-03
