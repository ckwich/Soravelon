---
name: help-system
description: Custom CmdHelp with dynamic ability lookup from ABILITIES registry, and 92 file-based help entries across 8 categories
---

## Activation

This skill triggers when editing these files:
- `commands/cmd_help.py`
- `world/help_entries.py`

Keywords: help, help system, help entry, CmdHelp, help entries, ability help, help category

---

You are working on **the help system** — a custom `CmdHelp` override with dynamic ability lookup and comprehensive file-based help entries.

## Key Files
- `commands/cmd_help.py` — `CmdHelp` extends Evennia's default; intercepts ability name queries and renders from `ABILITIES` registry
- `world/help_entries.py` — `HELP_ENTRY_DICTS` list with 92 entries across 8 categories, loaded via `settings.FILE_HELP_ENTRY_MODULES`
- `commands/default_cmdsets.py` — `CmdHelp` registered in `CharacterCmdSet`, overrides Evennia default via same `key='help'`
- `world/ability_registry.py` — `ABILITIES` dict consumed read-only for dynamic ability help rendering

## Key Concepts
- **Ability lookup is lazy:** `from world.ability_registry import ABILITIES` happens inside `func()`, not at module level, to avoid import-time Evennia init issues
- **Two-stage matching:** Direct `ability_id` match first, then case-insensitive name match across all ABILITIES values. Falls through to standard Evennia help if no ability found
- **Help entry categories (8):** New Player (5), Systems (15), Commands (40), Ancestries (4), Guilds (10), Skills (8), World Lore (6), General (1 dev-locked)
- **Writing style:** Second person, concise, in-world flavor, Evennia ANSI color codes (`|w`, `|c`, `|x`, `|y`, `|g`, `|r`, `|n`)
- **Dev-locked entry:** "evennia" entry has `locks="read:perm(Developer)"` — hidden from normal players

## Critical Rules
1. **CmdHelp overrides via `add()` replacement** — registered in `CharacterCmdSet` after `super()` call; Evennia's `add()` replaces the default help command with same `key='help'`
2. **Lazy import of ABILITIES** — never move to module level; Evennia's init order makes this unsafe
3. **Fall through to `super().func()`** — if no ability match, always delegate to standard Evennia help. Never swallow queries
4. **Help entries use `read:all()` locks** — unless intentionally restricting visibility (like the dev-only "evennia" entry)
5. **ANSI color convention:** `|w` for commands/emphasis, `|c` for system terms/labels, `|x` for flavor quotes, `|y`/`|g`/`|r` for states

## References
- **Ability Registry:** `world/ability_registry.py` — `ABILITIES` dict consumed for dynamic help
- **Evennia Help:** Evennia's `FILE_HELP_ENTRY_MODULES` setting controls which modules are loaded

---
**Last Updated:** 2026-04-03
