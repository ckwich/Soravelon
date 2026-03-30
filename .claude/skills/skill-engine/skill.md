---
name: skill-engine
description: Character skill progression — passive accumulation, deliberate practice, trainer sessions, ancestry seeds, and discovery triggers
---

## Activation

This skill triggers when editing these files:
- `world/skill_engine.py`
- `world/skill_definitions.py`
- `world/models.py`

Keywords: skill, practice, trainer, accumulate, discovery, skill engine, skill seed, passive gain, diminishing returns

---

You are working on **the skill engine** (`world/skill_engine.py`) — character skill progression independent of the domain/guild system.

## Key Files
- `world/skill_engine.py` — All skill logic: read, accumulate, practice, train, seeds, discoveries
- `world/skill_definitions.py` — Constants: `SKILL_DEFINITIONS`, `PRACTICE_GAINS`, `DIMINISHING_BRACKETS`, `TRAINER_REGISTRY`, `DISCOVERY_TRIGGERS`, `ANCESTRY_SKILL_SEEDS`
- `world/models.py:77-108` — `CharacterSkill` model (character FK, skill_id, skill_type, value 0-100, last_practiced_at)

## Key Concepts
- **Three improvement methods:** Passive use (ndb accumulators → DB batch), deliberate practice (24hr cooldown, random gain), trainer sessions (NPC, costs Scales, multiplies next practice)
- **Session accumulation pattern:** `accumulate_skill_use()` stores counts in `character.ndb.skill_use_{id}`. `commit_skill_accumulators()` flushes to DB at logout/safety tick — same lifecycle as domain XP
- **Passive threshold:** Every `PASSIVE_ACCUMULATOR_THRESHOLD` (10) uses = one gain tick of `PASSIVE_GAIN_PER_THRESHOLD` × diminishing rate. Remainder preserved in ndb
- **Diminishing returns:** 5 brackets from 100% (0-25) down to ~0% (96-100). Shared by passive and practice paths
- **Trainer bonus is volatile:** Stored as `character.ndb.trainer_bonus_{skill_id}` — consumed on next practice, lost on disconnect
- **trainer_required_above gate:** Above threshold (default 50), practicing without trainer bonus halves gain
- **Trainer registry populated:** `TRAINER_REGISTRY` maps NPC db key (e.g. `"npc_guildmaster_subterfuge_dessa"`) → trainer config with `skills_taught`, `quality_multiplier`, and `cost_per_session`. 10 trainers registered for Vael's Crossing. Quality tiers: apprentice (1.25×), journeyman (1.5×), master (2.0×)
- **Discovery triggers:** Multi-skill threshold conditions checked only on threshold crossings (25/50/75/90/100). Discovered set stored in `character.db.discoveries` using SaverDict copy pattern
- **Ancestry seeds:** `apply_ancestry_skill_seeds()` sets starting values at creation. Selvar coat maps to lineage key. Defensive: only raises value, never lowers
- **Skill types:** `general`, `zone_attunement`, `node_attunement`, `creature_attunement` — stored on `CharacterSkill.skill_type`

## Critical Rules
1. **All functions return `(bool, str)` tuples** — follows repo-wide convention
2. **Lazy record creation** — `get_skill_value()` returns 0.0 for missing records; mutations use `get_or_create`
3. **Skills are independent of domains** — SKL-04: skill_engine does NOT import world_state or domain systems
4. **SaverDict copy pattern for discoveries** — `character.db.discoveries` must be copied to list, mutated, then reassigned
5. **24hr rolling cooldown per skill** — `last_practiced_at` on `CharacterSkill` model, checked in `practice_skill()`
6. **Trainer cost deducts from `carried_scales`** — NOT from bank account. Direct `db.carried_scales` mutation
7. **`commit_skill_accumulators()` iterates ALL skills** — called at session end alongside `commit_session_xp()`. Wire into same lifecycle hooks
8. **Trainer registry keys = NPC db keys** — trainer lookup uses the same string as `area_builder.npc()` second argument. New zone trainers must use matching keys

## References
- **Model:** `world/models.py` — `CharacterSkill` (lines 77-108)
- **Ancestry Engine:** `world/ancestry_engine.py` — calls `apply_ancestry_skill_seeds()` at creation
- **World State:** `world/world_state.py` — parallel accumulation pattern (domain XP)

---
**Last Updated:** 2026-03-30
