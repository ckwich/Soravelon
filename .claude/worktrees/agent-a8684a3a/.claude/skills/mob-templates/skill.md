---
name: mob-templates
description: Mob stat template registry — template definitions, stat application, and zone content mob type lookups
---

## Activation

This skill triggers when editing these files:
- `world/mob_templates.py`
- `world/areas/*.py`

Keywords: mob template, mob_templates, template_key, apply_mob_template, sewer_rat, thug, smuggler, pickpocket, mob stats

---

You are working on **the mob template registry** (`world/mob_templates.py`) — pure-data definitions of mob stat blocks consumed by zone content plans.

## Key Files
- `world/mob_templates.py` — `MOB_TEMPLATES` dict, `get_mob_template()`, `apply_mob_template()`
- `world/areas/*.py` — Zone specs reference template keys in `area.spawn()` calls
- `typeclasses/mobs.py` — `SoravelonMob` typeclass receives applied template attrs
- `world/mob_affix_roller.py` — `initialize_for_spawn()` runs after template application

## Key Concepts
- **Pure data registry:** `MOB_TEMPLATES` dict maps `template_key` → stat block dict. No DB models, no Django deps
- **Template fields:** `key`, `mob_type`, `desc`, `base_aggression`, `hp_min/max`, `damage_min/max`, `speed`, `abilities` (list of ability dicts), `faction`, `is_hunter`, `detection_range`, `flee_threshold`, `wander`, `loot_table`
- **`apply_mob_template(mob, key)`** sets all `db.*` attrs from template. Does NOT override `base_disposition` or `trust_sensitive` — those come from spawn definition
- **Ability dicts:** Each ability has `ability_id`, `weight`, `element`, `damage_base`, `cooldown`, `condition`, `status_effect`, `effect_duration`, `effect_magnitude`, `application_chance`
- **Graceful fallback:** Unknown template key logs warning, does not raise — mob keeps defaults

## Critical Rules
1. **Template does NOT set `base_disposition` or `trust_sensitive`** — those are per-spawn, set via `area.spawn()` kwargs
2. **Copy abilities list** — `apply_mob_template` uses `list(template["abilities"])` to avoid shared mutation across mobs
3. **Zone content plans add entries here** — new zones (07-03 through 07-10) extend `MOB_TEMPLATES` with zone-specific mob types
4. **Template key matches spawn key** — `area.spawn(room, "sewer_rat", ...)` must match a `MOB_TEMPLATES["sewer_rat"]` entry
5. **Aggression values are strings** — `"passive"`, `"cautious"`, `"aggressive"`, `"hostile"` — not numeric

## References
- **Combat AI:** `world/combat_ai.py` — reads `db.abilities`, `db.base_aggression`
- **Zone Scaling:** `world/zone_scaling.py` — `initialize_mob_combat_stats()` runs after template
- **Affix Roller:** `world/mob_affix_roller.py` — `initialize_for_spawn()` wraps template + stats

---
**Last Updated:** 2026-03-29
