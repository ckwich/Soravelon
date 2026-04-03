# Phase 10: Node System Player-Ready - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.

**Date:** 2026-04-02
**Phase:** 10-node-system-player-ready
**Areas discussed:** Layer 1 exit topology, Node effect implementation, Stabilization duration, Player transition experience

---

## Layer 1 Exit Topology

| Option | Description | Selected |
|--------|-------------|----------|
| Mirror L0 exactly | Same directions, same connections | ✓ |
| Distorted mirror | Some paths blocked, new shortcuts | |
| Completely different layout | Independent exit graph | |

**User's choice:** Mirror L0 exactly

| Option | Description | Selected |
|--------|-------------|----------|
| Build time | Create in initialize_node(), permanent, editor-friendly | ✓ |
| Activation time | Create dynamically on state change | |

**User's choice:** Build time — explicitly wants game editor to be able to create and edit L1 exits.

---

## Node Effect Implementation

### Thermal
| Option | Description | Selected |
|--------|-------------|----------|
| Damage type modifiers | Fire +30%, water -30% | |
| Status effect interaction | Burn DoT double, wet blocked | |
| Both damage + status | Dual axis: damage AND status | ✓ |

**User's choice:** Both — full dual-axis implementation.

### Cognitive
| Option | Description | Selected |
|--------|-------------|----------|
| Mob target coordination | Mobs focus same target | ✓ |
| Mob ability upgrade | Access higher tier abilities | |
| Pack tactics bonus | +10% damage per additional mob | |

**User's choice:** Mob target coordination

### Temporal
| Option | Description | Selected |
|--------|-------------|----------|
| Random DoT variance | 50%-150% per tick | ✓ |
| Double-tick chance | 30% chance to tick twice | |
| Duration distortion | Durations randomly extend/shorten | |

**User's choice:** Random DoT variance (50%-150%)

---

## Stabilization Duration

| Option | Description | Selected |
|--------|-------------|----------|
| Timed duration | 5 minutes then auto-stop | |
| Stamina drain | Drains stamina over time, stops at 0 | ✓ |
| Action-limited | Breaks on combat/movement/abilities | |

**User's choice:** Stamina drain

| Option | Description | Selected |
|--------|-------------|----------|
| Breaks on combat or movement | Pure focus mechanic | ✓ |
| Breaks on movement only | Can fight while stabilizing | |
| Never breaks automatically | Only stamina depletion stops it | |

**User's choice:** Breaks on combat or movement

---

## Player Transition Experience

| Option | Description | Selected |
|--------|-------------|----------|
| Warning at awakening stage | Atmospheric echoes + direct warning at ~55% | ✓ |
| No warning | Sudden shift, sense/descriptions are the warning | |
| Opt-out window | 30s escape window before teleport | |

**User's choice:** Warning at awakening stage

---

## Claude's Discretion

- Warning message text
- L1 room name format when no override
- Node state tags on L1 rooms
- Stamina drain rate tuning

## Deferred Ideas

- Nodes for zones beyond Cantera Edge
- L1-specific mob spawns
- Distorted exit topology as future feature
