# Phase 14: All TBD/TODOs Implemented - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-04
**Phase:** 14-all-tbd-todos-implemented
**Areas discussed:** Death & banking stubs, Combat affix hooks, Quest-related stubs, Remaining misc stubs

---

## Death & Banking Stubs

### What happens to carried Scales on death?

| Option | Description | Selected |
|--------|-------------|----------|
| Percentage drop | Drop % of carried Scales, appears on corpse/ground | ✓ |
| Fixed amount | Drop flat amount regardless of wealth | |
| No currency loss | Keep all Scales | |
| Full drop | All carried Scales drop | |

**User's choice:** 20% drop (not scaling by zone tier — zone tiers don't exist)
**Notes:** User flagged that zone tiers have been removed as a concept. All zone tier references must be cleaned up.

### Where do dropped Scales go?

| Option | Description | Selected |
|--------|-------------|----------|
| On corpse | Inside player's corpse container | ✓ |
| On ground | Item in room | |
| Lost permanently | Vanish as economic sink | |

### Other death penalties?

| Option | Description | Selected |
|--------|-------------|----------|
| XP loss + currency | Lose uncommitted session XP + Scales | ✓ |
| Currency only | Only lose Scales | |
| Debuff on respawn | Temporary stat debuff | |
| Currency + debuff | Both penalties | |

---

## Combat Affix Hooks

### Damage modifier approach?

| Option | Description | Selected |
|--------|-------------|----------|
| Flat multiplier per rarity | Normal 1.0x, Magic 1.15x, Rare 1.3x, Legendary 1.5x | ✓ |
| Per-affix modifiers | Each affix adds its own modifier | |
| You decide | Claude picks | |

### On-hit and per-round effects?

| Option | Description | Selected |
|--------|-------------|----------|
| Map affixes to status effects | Uses existing compound system | ✓ |
| Custom logic per affix | Unique behavior code | |
| You decide | Claude designs mapping | |

---

## Quest-Related Stubs

### Approach for quest stubs?

| Option | Description | Selected |
|--------|-------------|----------|
| Wire to existing quest system | Pure integration with Phase 11's quest_engine | ✓ |
| Audit Phase 11 first | Check deliverables before deciding | |

### Misc stubs?

| Option | Description | Selected |
|--------|-------------|----------|
| Implement both | Real Lore help + WorldEventScript behavior | ✓ |
| Lore help only | WorldEventScript stays stub | |
| Defer both | Neither needed for v1.0 | |

---

## Cleanup & OOB

### Zone tier reference cleanup?

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — remove zone tier refs | Scan and clean up stale references | ✓ |
| No — separate cleanup | Keep Phase 14 focused on stubs | |

### OOB stub payloads?

| Option | Description | Selected |
|--------|-------------|----------|
| Implement real payloads | quest_update needs real shape | ✓ |
| Leave as-is | Real client integration later | |
| You decide | Claude assesses | |

---

## Claude's Discretion

- Exact session XP loss percentage
- Affix-to-status-effect mapping table
- WorldEventScript event types
- Lore help content
- quest_update payload shape
- Zone tier reference cleanup scope

## Deferred Ideas

None.
