# Phase 8: Player Surface Commands - Context

**Gathered:** 2026-04-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Every backend engine with player-facing utility gets a working text command. Players can see their stats, manage money, form groups, search for hidden content, use consumables, manage ability loadouts, perceive room atmosphere, and view a text map. Two equipment bugs are fixed. OOB inventory is wired to real data.

</domain>

<decisions>
## Implementation Decisions

### Command Naming and Syntax
- **D-01:** Hybrid command pattern — high-frequency actions get flat command aliases AND work as subcommands. `bank deposit 50` is canonical, `deposit 50` also works. Same for group commands.
- **D-02:** Character sheet command is `status` with aliases `score`, `stats`, `sheet`.
- **D-03:** Loadout management is a standalone `loadout` command, NOT part of equip/unequip. Commands: `loadout` (view), `loadout add <ability>`, `loadout remove <ability>`, `loadout clear`, `loadout save <slot#>`, `loadout <slot#>` (swap to saved preset). Multiple saved presets supported.
- **D-04:** Room atmosphere command is `sense` with aliases `perceive`, `feel`. Surfaces SENSE_DISPLAY text for active room state flags.
- **D-05:** Text map command is `map`. Renders ASCII grid from room coordinates with fog-of-war (visited rooms only). Required for telnet/CLI players — not OOB-only.

### Character Sheet Display
- **D-06:** Full sheet display — show everything in organized sections: Vitals (HP/stamina/resource), Stats, Dimensions, Domains, Guild/Ancestry, Economy. One screen, dense but complete.
- **D-07:** Stats show descriptors ONLY — no numeric values. "Strength: Imposing" not "Strength: 24". Consistent with the no-visible-numbers design philosophy.
- **D-08:** Domain scores show proficiency labels ONLY — "Combat: Journeyman" not "Combat: 42". GTS tier label shown for guild primary/secondary domains.
- **D-09:** Economy section shows both carried Scales and banked Scales.

### Search and Discovery Mechanics
- **D-10:** `search` command performs a skill check against room search_dc. Roll: investigation skill + random(1,20) vs search_dc. Failure message varies. Success reveals hidden exits and lore fragments.
- **D-11:** Search is driven by a new `investigation` general proficiency skill. Improves with use (passive accumulation on successful searches). Ties into Remnance excavation flavor.
- **D-12:** 60-second per-room cooldown after failed search. Prevents brute-force spam. Successful searches consume the discoverable (hidden exit added to discovered_exits, lore fragment collected).

### Consumable Use
- **D-13:** Universal `use <item>` command for all consumables. Item metadata determines effect (heal_amount, stamina_amount, cure_effect, etc). Single verb, extensible.
- **D-14:** Consumables work in combat and cost 1 action from the action budget. Tactical choice: use a potion or attack. Bandages may cost 2 actions (builders configure this via item metadata).

### Bug Fixes (Locked)
- **D-15:** Fix equip_slot schema drift — item_spawner.py must write `db.equipment_slot` (not `db.equip_slot`) to match what SoravelonEquipment.can_equip() reads.
- **D-16:** Fix Vael's Crossing starter greatswords — change `equip_slot="two_hand"` to `equip_slot="main_hand", two_handed=True` to match VALID_SLOTS.
- **D-17:** Wire OOB push_inventory_update to real data — replace empty `items: []` stub with actual call to `get_inventory_display_data()`.

### Claude's Discretion
- Map rendering algorithm (BFS from current room, ASCII grid layout, symbol choices)
- Color scheme for status command sections
- Exact investigation skill definition parameters (base value, growth rate, practice gains)
- Bank command NPC proximity validation (whether to require being near a teller)
- Group command help text and error messages

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Backend Engines (source of truth for command wrappers)
- `world/banking.py` — deposit(), withdraw(), get_balance(), get_or_create_account()
- `world/group_engine.py` — send_group_invite(), accept_group_invite(), leave_group(), kick_from_group(), set_loot_mode(), get_group_state()
- `world/room_state.py` — get_dominant_flag(), get_room_flags(), SENSE_DISPLAY, FLAG_VOCABULARY
- `world/inventory_engine.py` — get_inventory_display_data() (line ~345)
- `world/oob_publisher.py` — push_inventory_update() (line ~449, currently stubbed)
- `world/base_attributes.py` — STAT_NAMES, descriptor tiers, derive_max_hp(), derive_max_stamina()
- `world/guild_engine.py` — DOMAIN_PROFICIENCY_LABELS, GUILD_TIER_LABELS, calculate_guild_tier_score()
- `world/skill_definitions.py` — SKILL_DEFINITIONS (add investigation skill here)
- `world/skill_engine.py` — get_skill_value(), accumulate_skill_use()

### Existing Command Patterns (follow these conventions)
- `commands/cmd_crafting.py` — Subcommand pattern example (cook/smith/brew/craft all similar)
- `commands/cmd_equipment.py` — equip/unequip/gear pattern
- `commands/cmd_dialogue.py` — Multi-command registration pattern
- `commands/default_cmdsets.py` — Where all commands register

### Item and Equipment (for bug fixes)
- `world/item_spawner.py` — Line 65: equip_slot schema drift location
- `typeclasses/objects.py` — Lines 161-165: VALID_SLOTS, line 182: can_equip() reads equipment_slot
- `world/areas/vaels_crossing.py` — Lines 2166-2170: two_hand starter weapons
- `world/areas/equipment_catalog.py` — Lines 98-170: correct two_handed=True pattern

### Character State (for status command)
- `typeclasses/characters.py` — at_object_creation() defines all db attributes to display
- `world/world_state.py` — dimension scores, domain scores
- `world/ancestry_engine.py` — ANCESTRY_TRAITS for ancestry display

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `commands/command.py` — Base Command class all custom commands import from
- `world/inventory_engine.py:get_inventory_display_data()` — Already returns structured dict with equipped/carried/keyring/containers
- `world/base_attributes.py` — Has descriptor lookup tables for all 7 stats at 10 tiers each
- `world/guild_engine.py:DOMAIN_PROFICIENCY_LABELS` — 11 proficiency labels ready for display

### Established Patterns
- All commands use `from commands.command import Command`, `locks = "cmd:all()"`
- Commands are thin dispatchers: call engine function, msg the result
- Engine functions return `(bool, str)` tuples
- SaverDict copy pattern for all db.* mutations
- CharacterCmdSet.at_cmdset_creation() registers all commands with lazy imports

### Integration Points
- `commands/default_cmdsets.py` — New commands register here
- `typeclasses/characters.py:at_post_puppet()` — Initialize any new ndb state
- `world/oob_publisher.py:push_inventory_update()` — Wire real data here
- `world/skill_definitions.py:SKILL_DEFINITIONS` — Add investigation skill definition

</code_context>

<specifics>
## Specific Ideas

- Loadout presets (D-03): saved as `character.db.loadout_presets = {1: [...], 2: [...]}`. SaverDict copy pattern applies. Max 3-5 presets.
- Investigation skill (D-11): ties into Remnance excavation flavor. Successful searches accumulate skill use. Higher skill = find harder things.
- Map fog-of-war uses existing `character.db.visited_room_ids` set from characters.py.

</specifics>

<deferred>
## Deferred Ideas

- Lore journal / fragment viewer command — Phase 12 (Launch Polish)
- Quest log / objectives command — Phase 11 (Quest MVP)
- Vendor buy/sell commands — Phase 9 (Content Activation)
- Connection screen theming — Phase 12 (Launch Polish)

</deferred>

---

*Phase: 08-player-surface-commands*
*Context gathered: 2026-04-01*
