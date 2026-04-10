# Soravelon Launch Readiness Report

**Date:** 2026-03-31
**Scope:** Full verification of external Codex audit + independent gap analysis
**Prior work:** 17 bug fixes applied this session (1036/1036 tests green)

---

## Executive Summary

Soravelon has real architecture, real authored content, and real systemic depth. The engines work. The math is correct. The data is authored. What's missing is the **last mile of player surface** — the commands, verbs, and wiring that let players actually interact with the systems that exist.

The Codex audit was largely accurate. Of 14 specific claims verified, **11 confirmed true, 2 partially true, 1 false but with a related real bug**. The two highest-impact findings — `equip_slot` schema drift and `two_hand` slot invalidity — are confirmed real bugs that would break equipment at runtime.

---

## Codex Claim Verification

| # | Claim | Verdict | Notes |
|---|---|---|---|
| 1 | equip_slot vs equipment_slot drift | **TRUE** | item_spawner writes `db.equip_slot`, SoravelonEquipment reads `db.equipment_slot`. Equipment would fail can_equip() validation. |
| 2 | `two_hand` not a valid slot | **TRUE** | Vael's Crossing starter greatswords use `equip_slot="two_hand"` but VALID_SLOTS only has `main_hand`/`off_hand`. Real two-handed uses `two_handed=True` + `equip_slot="main_hand"`. These items are broken. |
| 3 | FILE_HELP_ENTRY_MODULES not in settings | **FALSE** | Evennia 6.0 default already includes `['world.help_entries']`. We verified this directly. Help entries ARE live. |
| 4 | 1 flight point, 0 routes | **TRUE** | Only Vael's Crossing has a courier platform. Zero `flight_route()` calls anywhere. Dragon Courier is a demo stub. |
| 5 | No trainer_id on NPCs | **TRUE** | Zero `trainer_id=` usages in any area file. `train` command exists but has no NPC to train with. |
| 6 | learn_recipe() never called in production | **TRUE** | Called in tests only. Non-default recipes are unlearnable. |
| 7 | 20 quest specs authored | **TRUE** | 8 in Vael's Crossing, 3 each in the four wilderness zones. All stored as data, no quest execution system. |
| 8 | Remnance permanently locked | **TRUE** | `remnance_discovered` initialized False, never set True anywhere. Domain is invisible forever. |
| 9 | No consumable-use mechanism | **TRUE** | 4 consumables defined (potions, bandages), zero eat/drink/quaff/use commands. |
| 10 | Inventory renderer unused by commands | **TRUE** | `get_inventory_display_data()` exists but no command calls it. |
| 11 | OOB inventory items stubbed empty | **TRUE** | `push_inventory_update()` sends `"items": []` hardcoded. |
| 12 | No search/discovery verb | **TRUE** | HiddenExit has `search_dc` and `discovered_exits` mechanism but zero player verbs to trigger discovery. |
| 13 | No loadout management command | **TRUE** | `active_loadout` displayed by CmdAbilities but no way to modify it. |
| 14 | Hidden exit discovery incomplete | **TRUE** | `is_visible()` checks `discovered_exits` but nothing populates it outside tests. |

---

## Content Density

| Zone | Rooms | NPCs | Mob Spawns | Materials | Quests | Lore | Crafting Stations | Flight Points |
|------|-------|------|------------|-----------|--------|------|-------------------|---------------|
| Vael's Crossing | 106 | 54 | 6 | 3 | 8 | 4 | 6 | 1 |
| Ashreach Plains | 102 | 3 | 52 | 4 | 3 | 5 | 2 | 0 |
| Reth Foothills | 102 | 3 | 51 | 3 | 3 | 5 | 0 | 0 |
| Cantera Edge | 101 | 3 | 43 | 10 | 3 | 13 | 1 | 0 |
| Stormhaven Coast | 107 | 3 | 50 | 4 | 3 | 5 | 1 | 0 |
| **Total** | **518** | **66** | **202** | **24** | **20** | **32** | **10** | **1** |

The hub-to-wilderness content gap is real: Vael's Crossing has 82% of all NPCs. Wilderness zones are combat-dense but service-sparse.

---

## Confirmed Bugs (Fix Before Launch)

### Bug 1: equip_slot Schema Drift
- **item_spawner.py:65** writes `item.db.equip_slot`
- **objects.py:182** reads `self.db.equipment_slot`
- **Impact:** Every item spawned by item_spawner fails equipment validation. Can't equip loot.
- **Fix:** Change item_spawner.py to write `db.equipment_slot`, or change objects.py to read `db.equip_slot`. Pick one name, use it everywhere.

### Bug 2: Starter Greatswords Use Invalid Slot
- **vaels_crossing.py:2166-2170** defines iron_greatsword and iron_greataxe with `equip_slot="two_hand"`
- **objects.py:161** VALID_SLOTS doesn't include `"two_hand"`
- **Real pattern:** `equip_slot="main_hand"` + `two_handed=True` (used correctly in equipment_catalog.py)
- **Fix:** Change the two items in vaels_crossing.py to use `equip_slot="main_hand", two_handed=True`

---

## Systems Assessment: What Works vs What's Missing

### Working End-to-End (player can use today)
- Combat initiation, turn management, damage, death, corpse, respawn
- Ancestry selection (`ancestry` command)
- Guild joining (`joinguild` command)
- Domain score viewing (`domains` command)
- Skill viewing and practice (`skills`, `practice` commands)
- Basic ability use in combat (`use` command)
- Equipment equip/unequip/view (`equip`, `unequip`, `gear` — once schema bug is fixed)
- NPC dialogue and topic system (`talk`, `ask`, `say`, `tell`)
- Crafting at stations (`cook`, `smith`, `brew`, `craft`, `recipes`)
- Node stabilization (`stabilize`)
- Alias system (`alias`, `unalias`)
- Standard Evennia: look, get, drop, inventory, say, emote, who, help

### Backend Complete, No Player Command
| System | What Exists | What's Missing |
|---|---|---|
| **Banking** | Full deposit/withdraw/balance/draft/debt API | No `bank`, `deposit`, `withdraw`, `balance` commands |
| **Groups** | Full invite/accept/kick/loot-mode engine | No `group`, `invite`, `accept invite`, `leave`, `kick` commands |
| **Character sheet** | 7 stats, 5 dimensions, HP/stamina, guild, domains | No `score`, `status`, `stats` command |
| **Search/Discovery** | HiddenExit with search_dc, lore fragments with discovery_method | No `search`, `investigate`, `examine` command |
| **Consumables** | 4 item types defined (potions, bandages) | No `use`, `drink`, `quaff` command |
| **Map** | OOB push with grid coords and fog-of-war | No text `map` command |
| **Lore collection** | 32 lore fragments authored across zones | No `lore`, `journal` command to view collected fragments |
| **Inventory display** | Rich `get_inventory_display_data()` renderer | No command consumes it; OOB items list is `[]` stub |

### Authored Content With No Execution System
| Content | Volume | What's Missing |
|---|---|---|
| **Quests** | 20 specs across 5 zones | Quest acceptance, tracking, completion, reward payout — all stubbed |
| **Ability loadout** | `active_loadout` db attr, display in CmdAbilities | No `loadout set/add/remove` command; no ability unlock command |
| **Remnance domain** | Full ability set authored, discovery flag exists | `remnance_discovered` is never set to True; domain is permanently hidden |
| **Flight routes** | Full engine (BFS routing, fare calc, FlightScript) | 1 flight point, 0 routes. Dragon Courier is non-functional. |
| **Trainer NPCs** | Full trainer system in skill_engine, command exists | Zero NPCs wired with `trainer_id`. `train` command has nothing to bind to. |
| **Recipe learning** | `learn_recipe()` function, CharacterRecipe model | Never called from production code. Non-default recipes can't be learned. |
| **Trigger system** | Full engine with 4 event types, action vocabulary | Zero `area.trigger()` calls in any zone spec. System is unused. |

### Node System (Architecturally Complete, Not Player-Ready)
| Component | Status |
|---|---|
| State machine (dormant→awakening→active→critical) | Working |
| Tick loop (30s global, per-zone actor counting) | Working |
| Player teleport to/from Layer 1 | Working mechanically |
| Stabilization command | Working |
| Crash recovery | Working |
| **Layer 1 exits (players can navigate)** | **MISSING — players trapped in isolated rooms** |
| **Layer 1 description overrides** | **MISSING — data authored, never applied** |
| **3/5 node effect types** | **MISSING — tags set, never checked by combat/AI** |

---

## Recommended Launch Plan

### Tier 0 — Must Fix (Breaks Existing Features)

1. **Fix equip_slot → equipment_slot schema drift** in item_spawner.py
2. **Fix two_hand → main_hand + two_handed=True** for Vael's Crossing starter weapons
3. **Wire OOB inventory** — replace empty `[]` stub with actual `get_inventory_display_data()` call

### Tier 1 — Core Player Commands (Blocks Basic Gameplay Loop)

These are all thin wrappers around existing engines. ~50-80 lines each.

4. **`score`/`status` command** — Display stats, dimensions, HP/stamina, guild, ancestry. The data is all on `character.db.*`
5. **`bank deposit <amount>` / `bank withdraw <amount>` / `bank balance`** — Calls `banking.deposit()`, `banking.withdraw()`, `banking.get_balance()`
6. **`group invite <player>` / `group accept` / `group leave` / `group kick <player>`** — Calls group_engine functions
7. **`search`** — Roll against room's hidden exits' `search_dc`, add to `discovered_exits` on success. Also surface lore fragments with `discovery_method="search"`
8. **`use <item>`** — Consume potions/bandages. Apply HP/stamina/effect from item metadata, destroy item
9. **`loadout add <ability>` / `loadout remove <ability>` / `loadout clear`** — Modify `character.db.active_loadout`

### Tier 2 — Content Activation (Unlocks Authored Content)

10. **Wire trainer_id to NPCs** — Add `trainer_id=` to 2-3 NPCs per wilderness zone in area specs
11. **Wire learn_recipe** — Add recipe rewards to quest specs or trainer interactions
12. **Add flight points** — One per wilderness zone (4 new points) + routes connecting them through Vael's Crossing hub
13. **Add Remnance discovery trigger** — Set `remnance_discovered = True` when player interacts with specific lore/node content
14. **Add triggers to zones** — Wire `area.trigger()` calls for on_enter/on_first_visit events (starter quest hooks, flavor text, discovery moments)

### Tier 3 — Node System Player-Ready

15. **Clone L0 exit topology into L1 rooms** — In `initialize_node()`, mirror all exits between Layer 0 rooms as exits between their Layer 1 counterparts
16. **Apply layer_1_overrides** — In `_activate_layer1()`, read `zone_obj.db.layer_1_overrides` and set name/desc on L1 rooms
17. **Wire remaining 3 node effects** — Implement `wet_suppressed`/`burn_enhanced` in combat damage calc, `mob_coordination` in combat_ai target selection, `dot_tick_variance` in status_effects tick

### Tier 4 — Quest MVP (New System)

18. **Quest state model** — CharacterQuest Django model (character, quest_id, status, progress, started_at)
19. **Quest acceptance** — Wire CmdAccept to create CharacterQuest record
20. **Quest tracking** — `quest` / `objectives` commands to view active quests
21. **Quest completion** — Check objective_count against progress, award rewards
22. **Quest log display** — Text-based quest journal

### Tier 5 — Polish

23. **Connection screen** — Themed login screen with game lore and help hints
24. **Text map command** — Render grid from room coordinates with fog-of-war
25. **Lore journal command** — View collected lore fragments per zone
26. **Wilderness NPC density** — Add 2-3 service/flavor NPCs per wilderness zone (camps, wandering merchants, hermits)
27. **Crafting station coverage** — Add engineering bench to Vael's Crossing, basic fire pits to wilderness zones

---

## Effort Estimates

| Tier | Items | Approximate Scope |
|---|---|---|
| **Tier 0** | 3 bug fixes | 30 minutes |
| **Tier 1** | 6 commands | 1-2 days |
| **Tier 2** | 5 content wiring tasks | 1-2 days |
| **Tier 3** | 3 node system completions | 1 day |
| **Tier 4** | 5 quest system items | 2-3 days |
| **Tier 5** | 5 polish items | 1-2 days |

**Minimum viable launch (Tiers 0-1):** ~2 days. Players can fight, progress, see their stats, bank money, form groups, use items, and manage loadouts.

**Full featured launch (Tiers 0-3):** ~5 days. Adds flight network, trainers, recipes, node system, discovery loop.

**Complete v1.0 (Tiers 0-5):** ~8-10 days. Adds quest system, polish, content density.

---

## Design Observations

The Codex audit's core insight is correct: **the team built the bones of a good MUD, but too many loops stop one layer before the player can fully inhabit them.** However, the gap is smaller than it appears — most missing pieces are thin command wrappers over working engines, not new systems to design. The hardest remaining work is the quest MVP (Tier 4), which requires a new Django model and state machine. Everything else is wiring.

The OOB-first design decision is worth preserving. The text commands in Tier 1 are necessary for MUD-client players, but the OOB infrastructure positions Soravelon for a rich webclient that most MUDs can't offer. The recommendation is: build both surfaces, text-first for launch, OOB client as the differentiator.

Content density outside Vael's Crossing is a real gap but not a launch blocker. The wilderness zones are combat-focused by design — adding 2-3 service NPCs per zone (Tier 5) would smooth the experience without requiring architectural changes.
