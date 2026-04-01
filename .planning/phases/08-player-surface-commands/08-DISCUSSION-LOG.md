# Phase 8: Player Surface Commands - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-01
**Phase:** 08-player-surface-commands
**Areas discussed:** Command naming and syntax, Character sheet display, Search/discovery mechanics, Consumable use mechanics

---

## Command Naming and Syntax

| Option | Description | Selected |
|--------|-------------|----------|
| Subcommand pattern | bank deposit 50, group invite cole. One help entry per parent. | |
| Flat commands | deposit 50, invite cole. More commands, shorter to type. | |
| Hybrid | Both work — flat aliases for high-frequency + subcommand canonical. | ✓ |

**User's choice:** Hybrid
**Notes:** High-frequency actions get flat aliases AND subcommand form.

---

| Option | Description | Selected |
|--------|-------------|----------|
| score | Classic MUD convention. Aliases: status, stats, sheet. | |
| status | More modern feel. Aliases: score, stats. | ✓ |
| sheet | Descriptive. Aliases: score, stats, status. | |

**User's choice:** status
**Notes:** Primary command is `status`, with `score`, `stats`, `sheet` as aliases.

---

| Option | Description | Selected |
|--------|-------------|----------|
| loadout add/remove/clear | Standalone command. Clear separation from equip. | ✓ (revised) |
| abilities set/unset | Subcommand of existing abilities. | |
| equip/unequip pattern | Unified verb for gear and abilities. | Initially selected, then revised |

**User's choice:** loadout (standalone) — initially chose equip/unequip pattern but reconsidered due to ambiguity risk between gear and ability names. Also added saved preset support: `loadout save <slot#>`, `loadout <slot#>` to swap.

---

| Option | Description | Selected |
|--------|-------------|----------|
| sense | Thematic, fits Resonance guild passive. Aliases: perceive, feel. | ✓ |
| survey | More grounded/tactical. Alias: assess. | |
| look closely | Extension of look. No new verb. | |

**User's choice:** sense

---

| Option | Description | Selected |
|--------|-------------|----------|
| Text map command | ASCII grid from room coords with fog-of-war. Essential for CLI. | ✓ |
| OOB-only | Map is webclient feature only. | |
| Deferred | Phase 12 polish work. | |

**User's choice:** Text map command

---

## Character Sheet Display

| Option | Description | Selected |
|--------|-------------|----------|
| Full sheet | Everything in organized sections. Dense but complete. | ✓ |
| Compact + detail subcommand | Short default, status full for rest. | |
| Thematic/RP-flavored | Narrative description with embedded mechanics. | |

**User's choice:** Full sheet

---

| Option | Description | Selected |
|--------|-------------|----------|
| Descriptors only | Strength: Imposing. No numbers. | ✓ |
| Descriptor + number | Strength: 24 (Imposing). Both shown. | |
| Descriptor + bar | Strength: Imposing [========--]. Visual hint. | |

**User's choice:** Descriptors only

---

| Option | Description | Selected |
|--------|-------------|----------|
| Proficiency labels only | Combat: Journeyman. No numbers. | ✓ |
| Labels + progress hint | Combat: Journeyman (advancing). Qualitative progress. | |
| Labels + numeric | Combat: 42 (Journeyman). Raw scores shown. | |

**User's choice:** Proficiency labels only

---

## Search/Discovery Mechanics

| Option | Description | Selected |
|--------|-------------|----------|
| Skill check vs DC | Roll investigation + random(1,20) vs search_dc. Can fail. | ✓ |
| Automatic on command | Always succeeds if skill >= DC. Deterministic. | |
| Progressive revelation | Repeated searches find harder things. Time-based. | |

**User's choice:** Skill check vs DC

---

| Option | Description | Selected |
|--------|-------------|----------|
| Acuity stat | Uses existing base attribute. No new skill. | |
| Dedicated investigation skill | New general skill, improves with use. Remnance flavor. | ✓ |
| Domain-contextual | Different domains find different things. | |

**User's choice:** Dedicated investigation skill

---

| Option | Description | Selected |
|--------|-------------|----------|
| Per-room cooldown | 60s cooldown after failed search. Prevents spam. | ✓ |
| No cooldown, diminishing returns | DC increases by 5 per fail. Soft anti-spam. | |
| No restrictions | Search as often as you want. | |

**User's choice:** Per-room cooldown (60 seconds)

---

## Consumable Use Mechanics

| Option | Description | Selected |
|--------|-------------|----------|
| use <item> | Universal verb. Item metadata determines effect. | ✓ |
| Specific verbs | drink potion, apply bandage, eat food. More thematic. | |
| use + specific aliases | use is canonical, drink/quaff/apply are aliases. | |

**User's choice:** use <item>

---

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, costs 1 action | Tactical choice in combat. Bandages may cost 2. | ✓ |
| Yes, free action | No action cost. Potions very powerful. | |
| Out of combat only | Cannot use in combat. Forces pre-fight prep. | |

**User's choice:** Yes, costs 1 action

---

## Claude's Discretion

- Map rendering algorithm (BFS, ASCII layout, symbols)
- Color scheme for status sections
- Investigation skill definition parameters
- Bank NPC proximity validation
- Group command help text and error messages

## Deferred Ideas

- Lore journal / fragment viewer — Phase 12
- Quest log / objectives — Phase 11
- Vendor buy/sell — Phase 9
- Connection screen — Phase 12
