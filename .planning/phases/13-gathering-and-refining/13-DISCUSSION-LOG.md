# Phase 13: Gathering and Refining - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-03
**Phase:** 13-gathering-and-refining
**Areas discussed:** Gathering node design, Processing chains, Material taxonomy, Gathering commands, Tool requirements, Node discovery & visibility, Fishing spots & fish types, Zone material distribution

---

## Gathering Node Design

### What should a gathering node be in the Evennia object model?

| Option | Description | Selected |
|--------|-------------|----------|
| Room-attached data | Gathering sources as data on rooms (like spawn_definitions). No separate DB objects | |
| Typeclass objects in rooms | Each node is a SoravelonGatheringNode object sitting in the room | |
| Tagged rooms | Rooms tagged as gathering locations | |

**User's choice:** Custom — Rooms flagged with possibility of spawning a gathering node. Nodes appear randomly in flagged rooms, zone/area limit on total active nodes. E.g., 5 meadow rooms, max 3 gathering nodes spawn at random times among them. Anti-bot: no predictable farming routes.

### How should gathering nodes deplete and respawn?

| Option | Description | Selected |
|--------|-------------|----------|
| Per-player cooldown | Each player can gather once per cooldown. Node always there for others | |
| Shared depletion pool | Node has X uses before depleting for everyone, respawns on timer | ✓ |
| Infinite with cooldown | Nodes never deplete, just personal cooldown | |

**User's choice:** Shared depletion pool
**Notes:** Creates competition and scarcity.

### How many gathers before a node depletes?

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed count (3-5) | Set number of uses, predictable | |
| Random count per node (2-6) | Variance — some nodes richer than others | ✓ |
| Single use | One gather then moves, maximum unpredictability | |

**User's choice:** Random count per node

### Skill reward axis?

| Option | Description | Selected |
|--------|-------------|----------|
| Quality only | Higher skill = higher quality raw materials | |
| Quantity only | Higher skill = more items per gather | |
| Both | Skill affects both quality AND quantity | ✓ |

**User's choice:** Both

### AreaBuilder integration?

| Option | Description | Selected |
|--------|-------------|----------|
| area.gathering_pool() | Zone-level declaration, pool manages spawns | ✓ |
| Room-level flags only | Each room flagged individually | |
| Separate config file | Gathering pools in separate file per zone | |

**User's choice:** area.gathering_pool()

---

## Processing Chains

### Chain depth?

| Option | Description | Selected |
|--------|-------------|----------|
| Two steps max | Raw -> Processed. Fiber->thread->cloth is deepest | ✓ |
| Variable depth | Some 1 step, some 2, some 3 | |
| Single step only | Everything is one conversion | |

**User's choice:** Two steps max

### System for processing?

| Option | Description | Selected |
|--------|-------------|----------|
| Existing crafting system | Processing recipes in RECIPE_REGISTRY | ✓ |
| Dedicated refine command | New command with own logic | |
| Automatic processing | Auto-process at right station | |

**User's choice:** Existing crafting system

### Quality propagation?

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — quality propagates | Raw quality sets floor/ceiling, skill adjusts | ✓ |
| Processing resets quality | Only processing skill matters | |
| Average of both | Output = average of raw + skill | |

**User's choice:** Quality propagates

### Batch conversion ratio?

| Option | Description | Selected |
|--------|-------------|----------|
| 1:1 ratio | 1 ore = 1 ingot | |
| N:1 conversion | 3 ore = 1 ingot | |
| Skill-based ratio | Ratio improves with skill | ✓ |

**User's choice:** Skill-based — 3:1 at low skill, 2:1 at medium, 1:1 at high skill.

---

## Material Taxonomy

### Material organization?

| Option | Description | Selected |
|--------|-------------|----------|
| MATERIAL_REGISTRY dict | Central Python dict in world/material_definitions.py | ✓ |
| Extend RECIPE_REGISTRY only | No separate registry | |
| Django model | Database definitions | |

**User's choice:** MATERIAL_REGISTRY dict

### Mob loot integration?

| Option | Description | Selected |
|--------|-------------|----------|
| Mobs drop raw materials | Wolf drops wolf_hide, process into leather_strip | ✓ |
| Mob loot stays separate | Gathering nodes only source of raw materials | |
| Hybrid | Some overlap, case-by-case | |

**User's choice:** Mobs drop raw materials

### Material tiers?

| Option | Description | Selected |
|--------|-------------|----------|
| 3 tiers (match equipment) | Iron/leather/common, Steel/hardened/rare, Mithril/shadowsilk/legendary | |
| 5 tiers | More granular, expandable | ✓ |
| Zone-based tiers | Unique materials per zone, no global tiers | |

**User's choice:** 5 tiers — expandable. Current 3-tier equipment is temporary; material system should be future-proof.

### Gathering skill mapping?

| Option | Description | Selected |
|--------|-------------|----------|
| Natural mapping (1 new skill) | Mining new, herbalism/foraging/fishing exist | |
| Foraging covers everything | Single skill for all gathering | |
| Full skill split (6 skills) | Mining, Herbalism, Woodcutting, Foraging, Fishing, Skinning | ✓ |

**User's choice:** Full skill split — 6 skills. "We're running a deep and rich MUD with 90 subclass combinations, having a large bank of skills makes sense."

---

## Gathering Commands

### Command structure?

| Option | Description | Selected |
|--------|-------------|----------|
| Skill-specific commands | mine, harvest, chop, forage, fish, butcher | ✓ |
| Unified 'gather' command | Single command auto-detects | |
| Hybrid | Both work | |

**User's choice:** Skill-specific commands

### Skinning mechanic?

| Option | Description | Selected |
|--------|-------------|----------|
| Target corpse | 'skin <corpse>' extracts hides/bones | |
| Auto-skin on loot | Automatic based on skill | |
| Butcher command | 'butcher <corpse>' covers skinning + meat | ✓ |

**User's choice:** Butcher command with skinning skill

### Gathering delay?

| Option | Description | Selected |
|--------|-------------|----------|
| Short fixed delay | 2-5 seconds, cancelled by movement | |
| Instant | No delay | |
| Variable by node tier | Low-tier fast, high-tier slow | ✓ |

**User's choice:** Variable by tier, skill reduces delay but never below 40% of original timer.

### Fishing system?

| Option | Description | Selected |
|--------|-------------|----------|
| Simple gather pattern | Same as mining/harvesting | |
| Light mini-game | Cast -> bite -> reel within window | ✓ |
| Idle fishing | Auto-fishing with periodic catches | ✓ |

**User's choice:** Both — active mini-game for full rewards, idle mode with significantly diminished returns.

---

## Tool Requirements

### Tool requirement?

| Option | Description | Selected |
|--------|-------------|----------|
| Required tools per skill | Mining needs pickaxe, etc. No tool = can't gather | ✓ |
| Optional tool bonus | Can gather bare-handed, tools give bonuses | |
| No tools needed | Skills alone determine everything | |

**User's choice:** Required tools per skill

### Tool durability?

| Option | Description | Selected |
|--------|-------------|----------|
| Degradation with repair | Durability points, repairable via smithing | ✓ |
| Permanent tools | Buy once, use forever | |
| Consumable charges | N charges then destroyed | |

**User's choice:** Degradation with repair — creates smith-gatherer economic loop.

---

## Node Discovery & Visibility

### Node visibility?

| Option | Description | Selected |
|--------|-------------|----------|
| Tiered visibility | Low visible, mid requires skill, high hidden | ✓ |
| All visible, skill gates interaction | Everyone sees, skill to gather | |
| All hidden until surveyed | Must actively survey to reveal | |

**User's choice:** Tiered visibility with prospect/survey revealing nodes in straight lines from player. Directional indicators. Skill improves range but not entire zone. Line-of-sight, not around corners.

### Sense integration?

| Option | Description | Selected |
|--------|-------------|----------|
| Sense shows nodes | Vague hints in Sense | |
| Separate prospect/survey | New command specifically for nodes | |
| Both | Sense = vague, prospect = specific | ✓ |

**User's choice:** Both — Sense gives vague environmental hints, prospect/survey gives specifics with directional indicators.

---

## Fishing Spots & Fish Types

### Fishing spot placement?

| Option | Description | Selected |
|--------|-------------|----------|
| Room tags + gathering pools | Water rooms eligible, uses gathering_pool() | ✓ |
| All water rooms fishable | Any water room auto-fishable | |
| Fixed fishing spots only | Specific permanent locations | |

**User's choice:** Room tags + gathering pools, builder-app friendly for configuring fish types per room/zone.

### Bait system?

| Option | Description | Selected |
|--------|-------------|----------|
| Optional bait for bonuses | Can fish without bait, bait improves results | ✓ |
| Required bait | Must have bait to fish | |
| No bait | Skill determines everything | |

**User's choice:** Optional bait for bonuses

---

## Zone Material Distribution

### Zone-tier mapping?

| Option | Description | Selected |
|--------|-------------|----------|
| Zone difficulty drives tier range | Starter zones 1-2, mid 2-3, advanced 3-5 | |
| All tiers everywhere | Skill gates access | |
| Zone-exclusive materials only | Unique materials per zone | |

**User's choice:** Custom — Most common nodes available in most zones. Some zones have exclusive materials in pockets. Variety maximized for both zone identity and player experience.

### Zone-exclusive rare materials?

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — rare exclusives | Each zone 1-2 unique rare materials | ✓ |
| No exclusives | Same pool everywhere | |
| Biome-based grouping | Materials grouped by biome | |

**User's choice:** Yes — rare zone exclusives drive cross-zone travel. Common materials shared across similar biomes.

---

## Claude's Discretion

- Exact gathering delay values per node tier
- Skill threshold breakpoints for tiered visibility
- Prospect/survey max range and scaling formula
- Tool durability values and repair costs
- Fishing bite timer ranges and idle catch intervals
- Bait item definitions and bonus effects
- Processing recipe difficulty values
- Quality propagation formula
- Zone-exclusive material names

## Deferred Ideas

None — discussion stayed within phase scope.
