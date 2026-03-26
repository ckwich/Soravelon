---
name: combat-system
description: Combat engine (damage, crits, death, corpses), mob combat AI (ability selection, targeting, scripted sequences), and player combat commands/CmdSet
---

## Activation

This skill triggers when editing these files:
- `world/combat_engine.py`
- `world/combat_ai.py`
- `world/combat_script.py`
- `commands/combat_commands.py`
- `typeclasses/mobs.py`

Keywords: combat, damage, crit, critical hit, death, corpse, combat AI, mob turn, ability selection, targeting, scripted sequence, flee, basic attack, CombatCmdSet, combat command

---

You are working on **soravelon's combat system** — damage resolution in `world/combat_engine.py`, mob turn AI in `world/combat_ai.py`, and player combat commands in `commands/combat_commands.py`.

## Key Files
- `world/combat_engine.py` — Damage math: `resolve_basic_attack`, `resolve_ability_damage`, `resolve_heal`, crit system, elite/boss scaling, death handling, corpse spawning
- `world/combat_ai.py` — Mob turn AI: `process_mob_turn`, `select_mob_action`, `get_mob_target`, `check_scripted_sequence`, `execute_sequence_action`, condition vocabulary
- `world/combat_script.py` — `CombatScript` turn manager: `start_combat()`, turn order, `process_player_action()`, dynamic CombatCmdSet add/remove
- `commands/combat_commands.py` — Player combat commands (`CmdAttack`, `CmdFlee`, `CmdTarget`, `CmdPass`) and `CombatCmdSet`
- `commands/default_cmdsets.py` — `CmdAttack` also registered in `CharacterCmdSet` (initiates combat from outside CombatCmdSet)
- `world/base_attributes.py` — `derive_max_hp`, `record_stat_use` consumed by combat engine
- `world/status_effects.py` — `has_effect`, `get_effect_modifiers`, `apply_effect` consumed by both modules
- `world/zone_scaling.py` — `get_player_damage_to_mob`, `get_mob_damage_for_player`, `apply_resistance`

## Key Concepts
- **Action dicts, not side effects:** `combat_ai.py` returns action dicts for CombatScript to dispatch — it does NOT resolve damage directly. `combat_engine.py` resolves damage and mutates HP.
- **CombatCmdSet:** `mergetype="Replace"`, `priority=10`, `no_exits=True`. Added/removed dynamically by `CombatScript` via `_add_combat_cmdset()`/`_remove_combat_cmdset()`. Includes CmdAttack, CmdFlee, CmdTarget, CmdPass, CmdUseAbility, CmdAbilities, CmdLook.
- **CmdAttack dual role:** In `CharacterCmdSet` it initiates combat (finds mob, calls `start_combat()`). Inside `CombatCmdSet` it performs basic attack via `handler.process_player_action()`.
- **CmdTarget is free:** Does NOT consume an action — only updates `character.ndb.combat_target_id`.
- **Combat handler on ndb:** Active combatants store `character.ndb.combat_handler` pointing to the CombatScript instance. Commands check this to determine in-combat state.
- **Turn validation:** All combat commands check `handler.get_current_combatant()` matches caller before allowing action.
- **DOMAIN_TO_STAT mapping:** Maps 10 domain names to base attribute stat names for ability scaling formula: `ability_base * (1 + primary_stat*0.02 + secondary_stat*0.01)`.
- **Crit system (D-20):** Characters: 5% base + Acuity×0.002. Mobs: `db.crit_chance` or 3% flat. Multiplier 2.0×.
- **Scripted sequences:** Named mob triggers (combat_start, hp_below_X, round_N, target_flees, on_death). Fire-once via `ndb.fired_sequence_triggers` set.
- **Corpse lifecycle:** `spawn_corpse()` → grace period → open → decayed (deleted). Player corpses skip grace. `delay()` drives transitions.

## Critical Rules
1. **Combat AI returns dicts, combat engine mutates state** — never resolve damage in `combat_ai.py`
2. **Minimum 1 damage** — `resolve_basic_attack` and `apply_resistance` enforce `max(1, ...)`
3. **Flee check runs before ability selection** — low-HP mobs escape without wasting an ability
4. **Call-for-help capped at 3 per encounter** — tracked via `combat_handler.ndb.call_for_help_count`
5. **CombatCmdSet lives in `commands/combat_commands.py`** — NOT in `cmd_abilities`. `combat_script.py` imports from there
6. **CmdAttack is in BOTH CharacterCmdSet and CombatCmdSet** — CharacterCmdSet copy initiates combat; CombatCmdSet copy performs in-combat attacks
7. **Lazy imports throughout** — `base_attributes`, `status_effects`, `zone_scaling` imported inside functions to avoid circular deps
8. **Elite/boss scaling applies AFTER resistance** — order matters in damage pipeline

## References
- **Zone Scaling:** `world/zone_scaling.py` — scale factors, resistance
- **Status Effects:** `world/status_effects.py` — effect checks and modifiers
- **Base Attributes:** `world/base_attributes.py` — HP derivation, stat recording
- **Mob Typeclasses:** `typeclasses/mobs.py` — mob attribute schema

---
**Last Updated:** 2026-03-26
