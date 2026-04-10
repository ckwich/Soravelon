---
name: mob-disposition
description: Computed disposition float (-1.0 to +1.0) determining mob behavior toward each player via standing, reputation, ancestry, and trust modifiers
---

## Activation

This skill triggers when editing mob disposition-related files:
- `world/mob_disposition.py`
- `typeclasses/mobs.py`
- `tests/test_mob_disposition.py`

Keywords: disposition, mob behavior, faction standing, trust sensitive, ancestry modifier, aggression

---

You are working on the **mob disposition system**, which computes a per-character disposition float that drives mob behavior.

## Key Files
- `world/mob_disposition.py` — Stateless computation engine: modifier functions + `get_mob_disposition()` + `get_mob_behavior()`
- `typeclasses/mobs.py` — `SoravelonMob` typeclass with `get_disposition()` / `get_behavior_toward()` (lazy-import wrappers)
- `world/world_state.py` — Provides `get_standing()` and `get_trust()` from `FactionStanding` model
- `world/models.py` — `FactionStanding` model (standing + trust per character×faction)
- `tests/test_mob_disposition.py` — 22 test cases covering all modifier paths and edge cases

## Key Concepts
- **Disposition float:** Clamped to `[-1.0, +1.0]`. Sum of: `base_disposition` + standing mod + reputation mod + ancestry mod + trust mod + quest mod (stub)
- **Modifier ordering:** Standing and ancestry are ALWAYS additive — personal achievement modifies institutional prejudice, never erases it
- **Standing modifier:** Maps `[-100,000, +100,000]` → `[-0.6, +0.6]` via linear scale
- **Reputation modifier:** Maps `[0, 100]` → `[0, +0.2]`. Always non-negative (floor at 0)
- **Ancestry × Faction table:** `ANCESTRY_FACTION_MODIFIERS` dict keyed by `(ancestry.lower(), faction_id.lower())`. Unlisted combos return 0.0
- **Trust modifier:** Only for `trust_sensitive=True` (elite) mobs. Trust < 25 proportionally reduces positive disposition. Trust > 75 gives +0.1 bonus. Negative disposition is never touched by trust
- **Behavior thresholds:** `≥0.6` friendly, `≥0.2` passive, `≥-0.2` base_aggression, `≥-0.6` elevated (passive→territorial, else→aggressive), `<-0.6` always aggressive

## Critical Rules
1. **No caching in the engine** — `get_mob_disposition()` computes fresh each call (up to 2 DB reads). Combat system must cache `get_mob_behavior()` per encounter in `character.ndb`
2. **Mob attributes required** — `base_disposition`, `faction`, `base_aggression`, `trust_sensitive`, `quest_modifier` are set in `SoravelonMob.at_object_creation()`
3. **Factionless mobs skip standing/ancestry/trust** — only `base_disposition` + reputation apply
4. **Quest modifier is a stub** — `get_quest_modifier()` always returns 0.0; quest system not yet built
5. **Lazy imports in typeclass** — `get_disposition()` and `get_behavior_toward()` use local imports to avoid circular deps
6. **Lowercase keys** — ancestry and faction_id are `.lower()`'d before table lookup

## References
- **World State API:** `world/world_state.py` — `get_standing()`, `get_trust()` functions
- **Mob Typeclass:** `typeclasses/mobs.py` — full mob attribute schema in `at_object_creation()`
- **Faction Model:** `world/models.py` — `FactionStanding` fields and constraints

---
**Last Updated:** 2026-03-23
