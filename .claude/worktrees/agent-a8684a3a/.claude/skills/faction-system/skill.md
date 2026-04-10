---
name: faction-system
description: Faction standing, trust, betrayal, subfactions, and mob disposition computed from character-faction relationships
---

## Activation

This skill triggers when editing these files:
- `world/world_state.py`
- `world/mob_disposition.py`
- `world/models.py`

Keywords: faction, standing, trust, betrayal, subfaction, disposition, mob behavior

---

You are working on **soravelon's faction system** — character-faction relationships that drive NPC/mob behavior.

## Key Files
- `world/models.py:14-53` — `FactionStanding` model (standing, trust, betrayal_flag, subfaction support)
- `world/world_state.py:219-273` — `modify_standing()`, `get_standing()`, `get_trust()`, `get_betrayal()`
- `world/mob_disposition.py` — Computes disposition float (-1.0 to +1.0) from standing + ancestry + trust + reputation

## Data Model
- **Standing:** integer, -100,000 to +100,000. Default 0 (lazy creation)
- **Trust:** integer, 0-100. Default 50 (lazy creation)
- **Betrayal flag:** boolean, default False
- **Subfaction:** nullable `subfaction_id` on same model. Top-level faction rows have `subfaction_id=None`
- **UniqueConstraint** uses `nulls_distinct=False` to prevent duplicate top-level rows (PostgreSQL NULL handling)

## Key Patterns
- **Atomic standing updates:** `modify_standing()` uses `F()` + `Greatest/Least` for clamped atomic writes — never read-modify-write
- **Lazy records:** `get_or_create` in `modify_standing()`; getters return defaults (0 standing, 50 trust, False betrayal) on `DoesNotExist`
- **Related manager access:** `character.faction_standings` (FK related_name) for queries
- **Disposition is additive:** standing + ancestry + reputation + trust modifiers stack; ancestry never overrides standing
- **Trust only matters for elites:** `trust_sensitive` flag on mob controls whether trust modifier applies

## Disposition → Behavior Thresholds
- `>= 0.6` → friendly | `>= 0.2` → passive | `>= -0.2` → base aggression | `>= -0.6` → territorial/aggressive | `< -0.6` → aggressive
- Standing maps to ±0.6, reputation to +0.2, ancestry to ±0.2, trust to +0.1/penalty

## Critical Rules
1. **Always use `modify_standing()` for changes** — it handles atomic F() updates and clamping
2. **Never expose `backend_level` to players** — it feeds disposition math only
3. **Ancestry modifiers are ADDITIVE with standing** — personal achievement modifies institutional prejudice, never erases it
4. **Cache `get_mob_behavior()` per encounter** in `character.ndb` — `get_mob_disposition()` makes up to 2 DB reads
5. **Context packet interface is frozen** — `get_character_context_packet()` feeds NPC templates and future LLM; do not break its shape

## References
- **Architecture:** `.claude/guidelines/faction-system/patterns.md`
- **World State Engine:** `world/world_state.py` (full 5-dimension system)

---
**Last Updated:** 2026-03-23
