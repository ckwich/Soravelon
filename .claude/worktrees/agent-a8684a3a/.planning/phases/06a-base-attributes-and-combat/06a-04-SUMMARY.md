---
phase: 06a-base-attributes-and-combat
plan: 04
subsystem: combat
tags: [mob-ai, ability-selection, targeting, scripted-sequences, combat-turns]

# Dependency graph
requires:
  - phase: 06a-base-attributes-and-combat
    plan: 02
    provides: "status_effects.has_effect for condition checks"
  - phase: 06a-base-attributes-and-combat
    plan: 01
    provides: "base_attributes.derive_max_hp for HP threshold conditions"
provides:
  - "world/combat_ai.py with select_mob_action, get_mob_target, check_scripted_sequence, process_mob_turn, CONDITION_CHECKS"
  - "9-entry condition vocabulary for mob ability prerequisites"
  - "Named mob scripted sequence execution at HP thresholds and round counts"
affects: [combat-script, ability-engine, mob-typeclasses]

# Tech tracking
tech-stack:
  added: []
  patterns: ["weight-based random.choices for ability selection", "fire-once trigger tracking via ndb set", "action dict protocol for CombatScript dispatch"]

# Key files
key-files:
  created:
    - world/combat_ai.py
  modified: []

# Decisions
decisions:
  - "Condition checks use lambda dict for O(1) lookup; unknown conditions return False for safe fallback"
  - "Scripted sequences use trigger_key for fire-once dedup, allowing multiple entries with same trigger type"
  - "execute_sequence_action returns result dicts rather than executing side effects directly -- CombatScript dispatches"
  - "Flee check runs before ability selection so low-HP mobs escape without wasting an ability"

# Metrics
metrics:
  duration_seconds: 123
  completed: "2026-03-26T18:59:00Z"
---

# Phase 06a Plan 04: Mob Combat AI Summary

Mob turn AI with weight-based ability selection filtered by cooldown/condition state, last-attacker targeting with vanish exclusion, and named mob scripted sequences at HP thresholds and round counts.

## What Was Built

### world/combat_ai.py (new, 330 lines)

**Condition vocabulary:** 9 condition checks mapping string keys to evaluator functions. Covers HP thresholds (target/self at 25% and 50%), status effect presence (poison, bleed, burn), and ally state (no_allies_alive, allies_present). None condition always passes. Unknown conditions return False.

**Ability selection (select_mob_action):** Reads mob.db.abilities list, filters out abilities on cooldown (via mob.ndb.ability_cooldowns dict) and abilities whose condition fails. Performs weighted random selection via random.choices. Falls back to basic attack if no ability qualifies -- every mob always has a basic attack available using mob.db.ref_damage_min/max.

**Targeting (get_mob_target):** Priority 1: last attacker (mob.ndb.last_attacker_id). Priority 2: random valid player from combat handler. Filters out targets with vanish effect and targets that left the room. Returns None when no valid targets exist.

**Scripted sequences (check_scripted_sequence):** Reads mob.db.scripted_sequence list for named mobs. Supports 5 trigger types: combat_start, hp_below_X, round_N, target_flees, on_death. Each trigger fires at most once per encounter, tracked via mob.ndb.fired_sequence_triggers set. Returns list of action dicts or None.

**Sequence execution (execute_sequence_action):** Handles 6 action types: echo (room text), ability (forced use), spawn (mid-combat), call_for_help (capped at 3 per encounter), modify_behavior (change aggression), zone_echo (adjacent rooms). Returns result dicts for CombatScript.

**Main entry (process_mob_turn):** Checks scripted sequences first (combat action overrides normal turn). Checks flee behavior. Gets target. Selects action. Returns list of action dicts for CombatScript to dispatch -- does NOT resolve damage directly.

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

None -- all functions are fully implemented with real logic.

## Self-Check: PASSED
