---
phase: 08-player-surface-commands
verified: 2026-04-01T21:49:24Z
status: gaps_found
score: 9/10 must-haves verified
gaps:
  - truth: "`use <item>` consumes potions/bandages, applies HP/stamina/effect, destroys consumed item"
    status: partial
    reason: "_consume_item writes to ndb.current_hp and ndb.current_stamina but the entire codebase uses ndb.hp and ndb.stamina -- healing effect is silently lost"
    artifacts:
      - path: "commands/cmd_abilities.py"
        issue: "Line 278 writes ndb.current_hp (should be ndb.hp); line 290 writes ndb.current_stamina (should be ndb.stamina)"
    missing:
      - "Fix ndb.current_hp -> ndb.hp on line 278"
      - "Fix ndb.current_stamina -> ndb.stamina on line 290"
---

# Phase 8: Player Surface Commands Verification Report

**Phase Goal:** Every backend engine with player-facing utility has a working text command -- players can see their stats, manage money, form groups, search for hidden content, use consumables, and manage ability loadouts. Critical equipment schema bugs fixed. OOB inventory wired.
**Verified:** 2026-04-01T21:49:24Z
**Status:** gaps_found
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `status` displays full character sheet: 7 stats, 5 dimensions, HP/stamina, guild, ancestry, domains | VERIFIED | cmd_status.py renders all sections: STAT_NAMES (7 stats), ALL_DIMENSIONS (5), HP/stamina vitals, guild/subclass/rank, ancestry header, domain proficiency labels, economy, loadout |
| 2 | `bank deposit/withdraw/balance` commands call banking engine functions | VERIFIED | cmd_bank.py imports and calls deposit(), withdraw(), get_balance() from world.banking; CmdDeposit/CmdWithdraw flat aliases also present |
| 3 | `group invite/accept/leave/kick/lootmode` commands call group_engine | VERIFIED | cmd_group.py imports send_group_invite, accept_group_invite, leave_group, kick_from_group, set_loot_mode from world.group_engine; all subcmds wired |
| 4 | `search` rolls against hidden exit search_dc and surfaces lore fragments | VERIFIED | cmd_search.py reads room.db.search_dc, rolls investigation skill + d20, reveals hidden_exits, collects lore_fragments with discovery_method="search", has 60s cooldown |
| 5 | `use <item>` consumes potions/bandages, applies HP/stamina/effect, destroys consumed item | FAILED | _consume_item writes ndb.current_hp / ndb.current_stamina but codebase uses ndb.hp / ndb.stamina -- healing is silently discarded |
| 6 | `loadout add/remove/clear` modifies character.db.active_loadout; abilities only usable if in loadout | VERIFIED | cmd_loadout.py: add/remove/clear all write char.db.active_loadout; cmd_abilities.py line 145: loadout gate checks active_loadout before ability use |
| 7 | equip_slot schema drift fixed (item_spawner writes same attr name as objects.py reads) | VERIFIED | item_spawner.py line 65 writes db.equipment_slot from equip_slot input; objects.py reads db.equipment_slot consistently |
| 8 | Starter greatswords use main_hand+two_handed=True | VERIFIED | vaels_crossing.py lines 2165-2170: iron_greatsword and steel_greatsword use equip_slot="main_hand", two_handed=True |
| 9 | OOB push_inventory_update sends real item data | VERIFIED | oob_publisher.py push_inventory_update() calls get_inventory_display_data(character) which queries InventoryItem DB records, builds structured dict with equipped/carried/containers/keyring |
| 10 | `sense` command surfaces SENSE_DISPLAY atmospheric text | VERIFIED | cmd_sense.py imports SENSE_DISPLAY, SENSE_PRIORITY, get_room_flags from room_state; iterates flags in priority order and renders atmospheric text |

**Score:** 9/10 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `commands/cmd_status.py` | Character sheet command | VERIFIED | 149 lines, renders all stat/dimension/domain/vital sections |
| `commands/cmd_sense.py` | Room atmosphere command | VERIFIED | 63 lines, reads SENSE_DISPLAY for active room flags |
| `commands/cmd_bank.py` | Banking commands | VERIFIED | 118 lines, CmdBank + CmdDeposit + CmdWithdraw, calls banking engine |
| `commands/cmd_group.py` | Group management command | VERIFIED | 139 lines, all subcmds wired to group_engine functions |
| `commands/cmd_loadout.py` | Loadout management command | VERIFIED | 210 lines, add/remove/clear/save/load presets |
| `commands/cmd_search.py` | Investigation search command | VERIFIED | 116 lines, skill check + hidden exit + lore fragment discovery |
| `commands/cmd_abilities.py` | Unified use command + abilities display | PARTIAL | 320 lines, CmdUseAbility handles items + abilities with loadout gate; _consume_item has ndb attr name bug |
| `commands/cmd_map.py` | ASCII zone map command | VERIFIED | Exists, renders grid with fog-of-war |
| `commands/default_cmdsets.py` | All commands registered | VERIFIED | Lines 87-102: CmdStatus, CmdSense, CmdBank, CmdDeposit, CmdWithdraw, CmdGroup, CmdLoadout, CmdMap, CmdSearch all registered |
| `world/item_spawner.py` | equip_slot schema fix | VERIFIED | Line 65: writes db.equipment_slot from equip_slot input |
| `world/oob_publisher.py` | Inventory OOB wiring | VERIFIED | push_inventory_update calls get_inventory_display_data with real DB queries |
| `world/skill_definitions.py` | Investigation skill defined | VERIFIED | Lines 336-349: investigation skill with thresholds |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| cmd_status.py | world.base_attributes | STAT_NAMES, derive_max_hp, derive_max_stamina imports | WIRED | All imported and used in func() |
| cmd_status.py | world.world_state | ALL_DIMENSIONS, ALL_DOMAINS imports | WIRED | Iterated for dimension/domain display |
| cmd_status.py | world.banking | get_balance import | WIRED | Called for banked Scales display |
| cmd_bank.py | world.banking | deposit, withdraw, get_balance imports | WIRED | All three called in command handlers |
| cmd_group.py | world.group_engine | 8 function imports | WIRED | send_group_invite, accept_group_invite, etc. all called |
| cmd_search.py | world.skill_engine | get_skill_value, accumulate_skill_use | WIRED | Called for investigation roll and skill progression |
| cmd_loadout.py | world.ability_registry | get_ability, ABILITIES | WIRED | Used for ability lookup and display |
| cmd_abilities.py | world.ability_engine | use_ability, _check_ability_access | WIRED | Routed for ability use; access check for loadout add |
| cmd_sense.py | world.room_state | SENSE_DISPLAY, SENSE_PRIORITY, get_room_flags | WIRED | All imported and used |
| oob_publisher.py | world.inventory_engine | get_inventory_display_data | WIRED | Called in push_inventory_update, returns real DB data |
| item_spawner.py | typeclasses.objects | equipment_slot attr | WIRED | Writes db.equipment_slot matching objects.py reads |
| default_cmdsets.py | all Phase 8 commands | imports + self.add() | WIRED | All 9 command classes imported and added to CharacterCmdSet |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|--------------------|--------|
| cmd_status.py | base_stats, domain_scores | char.db attributes | Yes -- set during character creation and progression | FLOWING |
| cmd_bank.py | balance | world.banking.get_balance | Yes -- reads char.db.banked_scales | FLOWING |
| cmd_group.py | group state | world.group_engine._get_group_state | Yes -- reads leader ndb.group_state | FLOWING |
| oob_publisher.py push_inventory_update | inv_data | get_inventory_display_data | Yes -- queries InventoryItem Django model | FLOWING |
| cmd_abilities.py _consume_item | ndb.current_hp | writes to wrong attr | No -- writes ndb.current_hp but system reads ndb.hp | DISCONNECTED |

### Behavioral Spot-Checks

Step 7b: SKIPPED (no running server; commands require Evennia runtime)

### Requirements Coverage

No explicit requirement IDs were mapped to Phase 8 in plans. All 10 success criteria from ROADMAP.md serve as the contract and are verified above.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| commands/cmd_abilities.py | 278 | `ndb.current_hp` instead of `ndb.hp` | BLOCKER | Healing potions write to wrong attribute; HP restoration silently lost |
| commands/cmd_abilities.py | 290 | `ndb.current_stamina` instead of `ndb.stamina` | BLOCKER | Stamina restoration from consumables silently lost |
| commands/cmd_abilities.py | 171 | "D-23 stub: attuned variant informational text" | INFO | Future feature placeholder; shows hint text but no functional gap |

### Human Verification Required

### 1. Character Sheet Visual Layout
**Test:** Log in, run `status` and confirm the output is readable and properly formatted
**Expected:** Clean columnar display with all sections: vitals, attributes (descriptor labels only, no numbers), dimensions, domains, guild, economy, loadout
**Why human:** Visual formatting quality cannot be verified programmatically

### 2. Search Command Discovery Flow
**Test:** Navigate to a room with search_dc and hidden_exits set, run `search` repeatedly
**Expected:** Successful rolls reveal hidden exits with discovery message; failed rolls show cooldown timer; lore fragments with discovery_method="search" appear
**Why human:** Requires game world state and RNG interaction

### 3. Group Party Flow End-to-End
**Test:** Two characters: invite, accept, check status, change lootmode, kick
**Expected:** All operations succeed with appropriate messages to both parties
**Why human:** Requires two connected player sessions

### Gaps Summary

One gap found blocking full goal achievement:

**Consumable item HP/stamina bug (Success Criterion 5):** The `_consume_item` method in `commands/cmd_abilities.py` writes healing to `ndb.current_hp` and `ndb.current_stamina`, but every other system in the codebase (combat, status display, OOB stat updates, character initialization) reads from `ndb.hp` and `ndb.stamina`. This means potions and bandages appear to work (player sees "restored X HP") but the healing is written to a dead-end attribute that nothing reads. This is a two-line fix: change `ndb.current_hp` to `ndb.hp` on line 278 and `ndb.current_stamina` to `ndb.stamina` on line 290.

---

_Verified: 2026-04-01T21:49:24Z_
_Verifier: Claude (gsd-verifier)_
