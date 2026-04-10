# Phase 1: Patrol, Commands, and Flight Paths - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-24
**Phase:** 01-patrol-commands-and-flight-paths
**Areas discussed:** Patrol behavior, Action vocabulary, Flight path discovery, Command prefix resolution, Flight path topology, Trigger edge cases, Patrol echoes, Custom command discoverability, Flight path API, Patrol mob spawning

---

## Patrol Behavior on Combat

| Option | Description | Selected |
|--------|-------------|----------|
| Instant disposition check | Check immediately on arrival | |
| Arrival emote then check | Emote first, check next tick | |
| Builder-configurable delay | Per-patrol encounter_delay field | ✓ |

**User's choice:** Builder-configurable delay
**Notes:** Some mobs should check instantly (guards), others should emote first (Caldenmere)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Both directions | Mob checks on arrival AND when player enters | ✓ |
| Mob arrival only | Only checks when mob enters new room | |
| Builder choice | Per-patrol flag | |

**User's choice:** Both directions (continuous threat awareness)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Skip disposition entirely | Invulnerable = no combat check | |
| Check but never attack | Disposition computed but never initiates | |
| Configurable per mob | Builder sets combat_enabled flag | ✓ |

**User's choice:** Configurable per mob

---

## Action Vocabulary Completeness

| Option | Description | Selected |
|--------|-------------|----------|
| All stay stubs | Stubs fine for Phase 1 | |
| Implement give_item + take_item | Just items since inventory exists | |
| Implement all that can work | Wire up everything with backing systems | ✓ |

**User's choice:** Implement all that have backing systems (items, standing, events). Stub only quest/dialogue/spawn.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Vocabulary is complete | 11 types sufficient | |
| Add play_sound/music | Audio triggers | |
| Add modify_attunement | Zone attunement from triggers | ✓ |

**User's choice:** Add modify_attunement action type

---

## Flight Path Discovery Model

| Option | Description | Selected |
|--------|-------------|----------|
| Visit room (auto-discover) | Entering room unlocks flight point | |
| Interact with NPC | Must talk to Courier NPC | |
| Both available | Auto-discover on entry, NPC for booking | ✓ |

**User's choice:** Both — discover on entry, NPC interaction to book

---

| Option | Description | Selected |
|--------|-------------|----------|
| Base fare + Standing discount | Flat rate reduced by Consortium Standing | ✓ |
| Standing-tiered pricing | Completely different price tiers | |
| Free for high standing | Free above threshold | |

**User's choice:** Base fare + Standing discount

---

**Flight UX:** User provided custom answer — Multi-leg real-time traversal. Each leg 30+ seconds with timed echo messages describing geography. Player can disembark at any stop. Cost increases per leg.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Locked — flight only | Only disembark or look | |
| Limited actions | Chat, inventory, messages only | |
| Full access minus movement | All commands except movement | ✓ |

**User's choice:** Full access minus movement during flight

---

## Flight Path Network Topology

| Option | Description | Selected |
|--------|-------------|----------|
| Hub-and-spoke from cities | Each hub connects to region | |
| Linear chain | Points form connected path | |
| Graph with explicit edges | Builder defines connections | ✓ |

**User's choice:** Graph with explicit edges defined by builders

---

## Trigger System Edge Cases

| Option | Description | Selected |
|--------|-------------|----------|
| Definition order | Fire in list index order | ✓ |
| All fire, order undefined | No guaranteed order | |
| First match only | Only first matching trigger | |

**User's choice:** Definition order

---

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, natural chaining | Follow normal Evennia hooks | |
| No recursion guard | Block trigger-initiated triggers | |
| Depth-limited (max 3) | Allow but cap at 3 levels | ✓ |

**User's choice:** Depth-limited to 3

---

## Zone-Wide Echoes for Patrol Mobs

| Option | Description | Selected |
|--------|-------------|----------|
| Entire zone | All rooms with zone_id tag | |
| Configurable radius | Per-patrol echo_radius field using BFS | ✓ |
| Adjacent rooms only | Direct exits only | |

**User's choice:** Configurable radius per patrol

---

## Custom Command Discoverability

**User's choice:** Custom answer — Mob/item descriptions hint naturally. Exit/teleport commands have `visible_in_exits` boolean. True = shown in exit list. False = hidden (quest-gated).

---

## Flight Path AreaBuilder API

| Option | Description | Selected |
|--------|-------------|----------|
| flight_point() + flight_route() | Two methods, explicit graph | ✓ |
| flight_point() only | Room marks + separate registry | |
| Tag-based | Tags on rooms + zone metadata | |

**User's choice:** Two explicit methods: area.flight_point() and area.flight_route()

---

## Patrol Mob Spawning

| Option | Description | Selected |
|--------|-------------|----------|
| Manual create_object in tests | Tests create mobs directly | ✓ |
| Builder command @spawnpatrol | Staging command for manual testing | |
| AreaBuilder creates mob on build() | Special case for patrol mobs | |

**User's choice:** Manual create_object in tests, but architecture must cleanly fit future spawn system

---

## Claude's Discretion

- Flight echo text content and timing details
- Exact Standing discount percentages
- PatrolScript tick interval tuning
- Trigger depth-limit error messaging

## Deferred Ideas

- Time of day system (triggers stored, can't fire yet)
- Quest flag system (action stubbed)
- NPC dialogue integration (action stubbed)
- Mob spawn runtime (action stubbed)
