---
name: world-state-engine
description: Five-dimension character progression, domain XP, faction standings, and mob disposition system
---

## Activation

This skill triggers when editing these files:
- `world/world_state.py`
- `world/mob_disposition.py`
- `world/models.py`
- `typeclasses/characters.py`

Keywords: world state, dimension, reputation, attunement, network, bond, legacy, domain xp, faction standing, mob disposition, backend level, decay

---

You are working on the **world-state engine** — the character progression and NPC reaction system.

## Key Files
- `world/world_state.py` — Core engine: dimension scores, domain XP, faction ops, context packet, ticker callbacks
- `world/mob_disposition.py` — Computes mob disposition (-1.0 to +1.0) from standing, ancestry, reputation, trust
- `world/models.py` — Django models: `FactionStanding`, `ZoneAttunement`, `CharacterSkill`
- `typeclasses/characters.py` — `Character.at_object_creation()` initializes all `db.*` attributes; login/logout hooks wire XP lifecycle

## Key Concepts
- **Five dimensions** (`ALL_DIMENSIONS`): reputation, network, bond, legacy, attunement — each 0-100, stored as `character.db.{dim}_score`
- **Ten domains** (`ALL_DOMAINS`): combat, subterfuge, naturalism, resonance, arcana, diplomacy, alchemy, tactics, engineering, remnance — scores in `character.db.domain_scores` dict
- **Session XP lifecycle**: `init_session_accumulators()` on login → `accumulate_domain_xp()` during play (ndb) → `commit_session_xp()` at logout/flush/10m tick. XP is volatile until committed
- **Diminishing returns**: 5 brackets from 100% (score 0-25) down to 2% (score 90-100). Conversion: `raw_xp * 0.001 * bracket_rate`
- **Attunement dual representation**: per-zone in `ZoneAttunement` model, aggregate recalculated as avg on commit
- **Mob disposition**: additive modifiers (standing + ancestry + reputation + trust) → clamped -1.0 to +1.0 → behavior string. Standing and ancestry are ALWAYS additive, never override each other
- **Context packet** (`get_character_context_packet`): stable dict interface consumed by NPC templates and future LLM — do not break its shape

## Critical Rules
1. **Backend level is INTERNAL ONLY** — derived from weighted domain scores (primary×2, secondary×1.5, others×0.5), mapped to 1-50. NEVER expose to players
2. **Faction standing uses F() expressions** — `modify_standing()` does atomic DB updates with `Greatest`/`Least` clamping. Never read-modify-write
3. **SaverDict copy pattern in `commit_session_xp`** — copy `db.domain_scores` to plain dict, mutate, assign once to avoid N+1 repickle
4. **Decay skips online characters** — `decay_tick_all()` only hits offline chars. Legacy never decays. Attunement decays per-zone, not aggregate
5. **Lazy record creation** — missing `FactionStanding`/`ZoneAttunement` = default/neutral (standing=0, trust=50, attunement=0.0)
6. **Trust only matters for elite mobs** — `trust_sensitive` flag gates the trust modifier in disposition calc
7. **Cache `get_mob_behavior()` per encounter** — it makes up to 2 DB reads; combat system should store result in `character.ndb`

## References
- **Models:** `world/models.py`
- **Character Init:** `typeclasses/characters.py` (lines 25-59)
- **Mob Disposition:** `world/mob_disposition.py`

---
**Last Updated:** 2026-03-23
