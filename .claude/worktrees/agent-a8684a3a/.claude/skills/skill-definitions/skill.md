---
name: skill-definitions
description: General proficiency skills (0-100), ancestry seed values, trainer registry, diminishing returns, and discovery triggers
---

## Activation

This skill triggers when editing these files:
- `world/skill_definitions.py`

Keywords: skill definition, proficiency, lockpicking, herbalism, stealth, tracking, trainer, ancestry seed, practice gain, diminishing returns, discovery trigger, skill_definitions

---

You are working on **the skill definitions registry** (`world/skill_definitions.py`) — pure-data module defining all general proficiency skills independent of the domain/guild system.

## Key Files
- `world/skill_definitions.py` — All skill data, ancestry seeds, trainer registry, practice/accumulator constants
- `world/world_state.py` — Domain XP system (separate from general skills)
- `world/ancestry_engine.py` — Ancestry creation calls into seed application

## Key Concepts
- **21 general skills** on 0-100 scale: lockpicking, animal_handling, beast_training, herbalism, tracking, climbing, persuasion, intimidation, swimming, first_aid, appraisal, stealth, foraging, node_reading, navigation, fishing, engineering, cooking, smithing, alchemy, reflexes
- **Three improvement methods:** Passive use (10 successes → +0.1 before diminishing), deliberate practice (24hr cooldown, tier-based gains), trainer sessions (NPC-driven, costs Scales)
- **Diminishing returns:** Same 5-bracket curve as domain XP — 100% (0-25), 75% (26-50), 40% (51-75), 10% (76-90), 2% (91-100)
- **Ancestry skill seeds:** Applied at creation. Human gets none. Kau'roran: swimming/fishing/beast_training/persuasion. Veth: stealth/navigation/lockpicking/tracking. Selvar splits by coat — winter→north (tracking/climbing/intimidation), summer→south (lockpicking/appraisal/persuasion/navigation)
- **Trainer registry:** `TRAINER_REGISTRY` maps NPC keys → quality/multiplier/skills_taught/cost. Three quality tiers: apprentice (1.25×), journeyman (1.5×), master (2.0×)
- **Each skill has `domain_bonus`** — links to one of the 10 domains for cross-system synergy
- **`trainer_required_above`** — skill score above which a trainer is needed to advance

## Critical Rules
1. **Skills are independent of domains** — `skill_definitions.py` is separate from the domain/guild system in `world_state.py`
2. **Selvar coat → lineage mapping** — `SELVAR_COAT_TO_LINEAGE`: winter→`selvar_north`, summer→`selvar_south`. Must use this mapping, not raw coat string
3. **Trainer keys must match NPC keys** — `TRAINER_REGISTRY` keys are the same NPC identifier strings used in `area.npc()` calls
4. **Pure data module** — no Django imports, no Evennia deps. Keep it importable from external tools
5. **Discovery triggers are a framework** — `DISCOVERY_TRIGGERS` has one example entry; content phases fill these

## References
- **Domain XP:** `world/world_state.py` — separate progression system that skills complement
- **Ancestry Engine:** `world/ancestry_engine.py` — applies seed values at character creation
- **Mob Templates:** `world/mob_templates.py` — mob abilities reference skill-adjacent concepts

---
**Last Updated:** 2026-03-29
