# Phase 7: Milestone 1 Content - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-29
**Phase:** 07-milestone-1-content
**Areas discussed:** Hub city layout, Starter zone design, Equipment catalog, Node zone mechanics

---

## Hub City Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Compact (8-12 rooms) | Focused hub | |
| Medium (15-25 rooms) | Distinct districts | |
| Large (30+ rooms) | Full city feel | |
| Other: 100+ rooms | True city scale | ✓ |

**User's choice:** 100+ rooms
**Notes:** User wants a genuine city feel, not a compact hub

| Option | Description | Selected |
|--------|-------------|----------|
| You decide | Claude designs districts | ✓ |
| I have specific ideas | User describes districts | |

**User's choice:** Claude designs 6-8 districts

| Option | Description | Selected |
|--------|-------------|----------|
| Service NPCs only | ~15-20 NPCs | |
| Lived-in city | ~30-50 NPCs | |
| Bustling metropolis | 50+ NPCs | |

**User's choice:** Bustling metropolis with quest starters everywhere, rich atmosphere for builder client propagation

| Option | Description | Selected |
|--------|-------------|----------|
| Pure safe zone | No mobs in city | |
| Unsafe edges | Core safe, outskirts dangerous | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Cardinal gates | N/S/E/W exits | |
| Thematic paths | Named roads/trails | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Single flight point | One Dragon Courier | ✓ |
| Full bank | Consortium branch | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| All 10 domains | Every guild has a hall | ✓ |

**Notes:** Temporary — will redistribute across hub cities later

| Option | Description | Selected |
|--------|-------------|----------|
| Hidden underworld district | Mobs + NPCs | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Dark frontier outpost | Gritty, worn | ✓ |
| Start at an NPC | Greeter for onboarding | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Eastern (Varath) | Override vault Hub 1 placement | ✓ |

**Notes:** Vault says "Western continent frontier town" but user overrides to eastern (Varath)

| Option | Description | Selected |
|--------|-------------|----------|
| Vael's Crossing | Final name | ✓ |
| City vendors sell basics | Starter gear available | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| All new content | Invent fresh, but follow vault naming conventions | ✓ |
| One crafting station each | Cooking, forge, alchemy bench | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — populate trainers | Fill TRAINER_REGISTRY | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Empire + Consortium + Wardens | Three faction offices | ✓ |
| Yes — landmarks | 3-5 atmospheric landmarks (Claude designs) | ✓ |
| Medic building | Death respawn point | ✓ |

---

## Starter Zone Design

| Option | Description | Selected |
|--------|-------------|----------|
| Other: 100+ rooms each | Large zones | ✓ |
| You decide | Claude designs 4 biomes from Varath geography | ✓ |
| Moderate density | 1-2 spawns per 2 rooms | ✓ |
| One named mob per zone | Mini-boss with unique loot | ✓ |
| Affix-based rarity | Random modifications on base templates | ✓ |
| A few field NPCs | 1-3 per zone with quest stubs | ✓ |
| Quest stubs only | Must be viewable in builder client | ✓ |
| Both materials and lore | Crafting + Remnance resources | ✓ |
| Connected network | Zones connect to city AND each other | ✓ |
| City flight only | Players walk to zones | ✓ |
| Some wandering mobs | Random movement, not fixed patrols | ✓ |
| 1-2 hunters per zone | Sparingly, BFS chase | ✓ |
| Active attunement | Zone attunement from start | ✓ |
| Mixed flag visibility | Some alter descriptions, some Sense-only | ✓ |

---

## Equipment Catalog

| Option | Description | Selected |
|--------|-------------|----------|
| Large (50+ items) | Ranged weapons flavor only | ✓ |
| Soft stat requirements | Scale better with matching stats | ✓ |
| Vendors + drops + crafting | Three sources | ✓ |
| Material tiers | 2-3 tiers with scaling | ✓ |
| Ignore weight for M1 | No encumbrance | ✓ |
| 13 equipment slots | Head, face, chest, back, hands, wrists, legs, feet, MH, OH, ring×2, amulet | ✓ |
| Two-handed weapons | Greatswords, staves, greataxes | ✓ |
| Passive shield armor | No active block for M1 | ✓ |
| Small stat bonuses | Equipment grants minor bonuses | ✓ |
| Permanent equipment | No durability | ✓ |
| Per vault spec damage | damage_min/max + stat + scaling | ✓ |
| No set bonuses | Future content | ✓ |
| Vendor consumables | Basic healing potions | ✓ |

---

## Node Zone Mechanics

| Option | Description | Selected |
|--------|-------------|----------|
| Claude picks zone | Best theme for corruption | ✓ |
| Complete transformation | L1 rooms fundamentally different | ✓ |
| Partial overlay | Only rooms near node center | ✓ |
| Corrupted L1 mob variants | Unique mobs in collapsed state | ✓ |
| Per existing NodeScript | Tick-driven: healthy→stressed→failing→collapsed | ✓ |
| L1 exclusive lore fragments | Remnance/Echoes rewards | ✓ |
| Interactive stabilization | Players can repair/stabilize node | ✓ |
| Claude picks node type | From VALID_NODE_TYPES | ✓ |

---

## Claude's Discretion

- District layout, names, and room distribution
- Zone biome themes, names, mob rosters
- NPC names, dialogue, quest stubs
- Equipment catalog specifics (names, stats, materials)
- Landmark designs
- Node zone selection and L1 room design
- Wandering mob implementation approach

## Deferred Ideas

- Active shield block mechanic (Engram TODO)
- Equipment durability system (Engram TODO)
- Set bonuses, procedural affixes, cross-room ranged combat
- Full quest system, western continent content, PvP
