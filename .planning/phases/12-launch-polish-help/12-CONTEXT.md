# Phase 12: Launch Polish and Help System - Context

**Gathered:** 2026-04-03
**Status:** Ready for planning

<domain>
## Phase Boundary

New player experience is smooth from connection to first combat. Comprehensive help covers every command, ability, and system. Lore journal lets players revisit discovered fragments. Connection screen sets the dark fantasy tone. Ancestry-based starter kits equip new characters for their first encounters.

</domain>

<decisions>
## Implementation Decisions

### Connection Screen
- **D-01:** Dark fantasy atmospheric tone. Short lore excerpt setting the world mood ("The old patterns stir beneath the stone..."), followed by clear connect/create instructions. Mysterious but welcoming.
- **D-02:** Replace default Evennia connection screen in `server/conf/connection_screens.py`.

### Help System Coverage
- **D-03:** Ability help auto-generated from ABILITIES registry. `help <ability_name>` dynamically reads: description, tier, domain, resource cost, cooldown, scaling. Zero maintenance, always matches code.
- **D-04:** Comprehensive hand-written help scope: systems (expand 11 existing), commands (~40 custom commands), 4 ancestries, 10 guilds, individual skill descriptions, crafting recipes, faction lore, new-player guide. 100+ entries total.
- **D-05:** Help entries use `world/help_entries.py` HELP_ENTRY_DICTS (already wired via Evennia default FILE_HELP_ENTRY_MODULES). Dynamic ability help requires a custom help command or contrib hook.

### Lore Journal
- **D-06:** `lore` command organized by zone. `lore` shows zones with fragment counts ("Ashreach Plains: 3/5 fragments collected"). `lore <zone>` shows that zone's collected fragments.
- **D-07:** Fragments collected via the existing `search` command (Phase 8). Lore fragments with `discovery_method="search"` found when player searches in rooms containing them.
- **D-08:** Track collected fragments on `character.db.collected_lore` (set of fragment_ids). SaverDict copy pattern applies.

### New Player Funnel
- **D-09:** Guided with prompts after creation. Player gets: "You must first choose your ancestry. Type `ancestry` to begin." Then breadcrumbs to guild, starter quest NPC, etc. No forced tutorial zone.
- **D-10:** Ancestry-based starter kit. Each ancestry gets thematically appropriate gear:
  - Human: iron sword, leather armor, 50 Scales, 2 healing potions
  - Kau'roran: iron bow/spear, hide armor, 50 Scales, 2 healing potions
  - Veth: iron daggers, leather armor, 50 Scales, 2 healing potions, lockpick
  - Selvar: iron staff, cloth robes, 50 Scales, 2 healing potions
- **D-11:** Starter kit placed in inventory during `set_ancestry()` (after ancestry choice, not at character creation — so items match the chosen ancestry).

### Map Command (Already Delivered)
- **D-12:** `map` command already delivered in Phase 8. Remove from Phase 12 scope to avoid duplication.

### Claude's Discretion
- Connection screen lore text content (atmospheric writing)
- Help entry prose and formatting style
- Lore fragment display formatting (how text appears in journal)
- Exact starter gear stat values (balanced with existing iron-tier items from equipment catalog)
- New player prompt timing and message text
- Whether dynamic ability help uses a custom CmdHelp override or Evennia's help contrib hook

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Connection Screen
- `server/conf/connection_screens.py` — Current default screen to replace

### Help System
- `world/help_entries.py` — Existing 11 help entries (HELP_ENTRY_DICTS)
- `world/ability_registry.py` — ABILITIES dict (360+ entries) for auto-generated help
- `world/guild_engine.py` — GUILDS dict (10 guilds) for guild help entries
- `world/ancestry_engine.py` — ANCESTRY_TRAITS dict for ancestry help
- `world/skill_definitions.py` — SKILL_DEFINITIONS for skill help
- `world/crafting_definitions.py` — RECIPE_REGISTRY for recipe help
- `commands/default_cmdsets.py` — Full command list for command help entries

### Lore System
- `world/area_builder.py` — lore_fragment() DSL method
- `commands/cmd_search.py` — Search command (discovery mechanism)
- `world/areas/*.py` — 32 lore fragments across 5 zones

### New Player Flow
- `typeclasses/characters.py` — at_object_creation(), at_post_puppet()
- `world/ancestry_engine.py` — set_ancestry() (starter kit hook point)
- `world/areas/equipment_catalog.py` — Item definitions for starter gear

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/help_entries.py` already has 11 entries with correct HELP_ENTRY_DICTS format
- `world/ability_registry.py:ABILITIES` has all fields needed for auto-help (name, description, tier, domain, resource_cost, cooldown, scaling_primary)
- `commands/cmd_search.py:CmdSearch` already handles lore discovery via investigation skill check
- `world/item_spawner.py:create_item_from_template()` can create starter gear from equipment catalog templates

### Established Patterns
- Help entries: `{"key": "...", "aliases": [...], "category": "...", "locks": "read:all()", "text": "..."}`
- Character state: `character.db.*` for persistent, SaverDict copy pattern
- Commands: `from commands.command import Command`, register in CharacterCmdSet

### Integration Points
- `server/conf/connection_screens.py` — Replace CONNECTION_SCREEN variable
- `world/ancestry_engine.py:set_ancestry()` — Add starter kit creation after ancestry is set
- `typeclasses/characters.py:at_post_puppet()` — Add new player guidance check
- `commands/default_cmdsets.py` — Register CmdLore

</code_context>

<specifics>
## Specific Ideas

- Dynamic ability help: override Evennia's default CmdHelp to intercept `help <ability_name>` and generate text from ABILITIES dict if matched, falling through to standard help for everything else
- New player guidance: check `character.db.ancestry is None` on first login, send ancestry prompt. After ancestry set, check `character.db.guild_id is None` and hint toward exploration.
- Lore fragment collection: search command already surfaces fragments; just needs to add fragment_id to `character.db.collected_lore` set on discovery

</specifics>

<deferred>
## Deferred Ideas

- Web client / webclient customization — separate project
- MSSP metadata customization — post-launch polish
- Character deletion / reroll flow — post-launch
- Achievement system for lore collection — future milestone

</deferred>

---

*Phase: 12-launch-polish-help*
*Context gathered: 2026-04-03*
