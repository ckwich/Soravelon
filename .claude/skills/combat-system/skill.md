---
name: combat-system
description: Combat engine (damage, crits, death, corpses), mob combat AI (ability selection, targeting, scripted sequences), and player combat commands/CmdSet
---

## Activation

This skill triggers when editing these files:
- `world/combat_engine.py`
- `world/combat_ai.py`
- `world/combat_script.py`
- `world/ability_engine.py`
- `world/ability_registry.py`
- `commands/combat_commands.py`
- `typeclasses/mobs.py`

Keywords: combat, damage, crit, critical hit, death, corpse, combat AI, mob turn, ability selection, targeting, scripted sequence, flee, basic attack, CombatCmdSet, combat command, ability, momentum, command resource, effect_params, respawn, death penalty

---

You are working on **soravelon's combat system** — damage resolution in `world/combat_engine.py`, mob turn AI in `world/combat_ai.py`, ability execution in `world/ability_engine.py`, and player combat commands in `commands/combat_commands.py`.

## Key Files
- `world/combat_engine.py` — Damage math: `resolve_basic_attack`, `resolve_ability_damage`, `resolve_heal`, crit system, elite/boss scaling, death handling, corpse spawning, player respawn, `_compute_raw_damage` helper
- `world/combat_ai.py` — Mob turn AI: `process_mob_turn`, `select_mob_action`, `get_mob_target`, `check_scripted_sequence`, `execute_sequence_action`, condition vocabulary
- `world/combat_script.py` — `CombatScript` turn manager: `start_combat()`, turn order, `process_player_action()`, dynamic CombatCmdSet add/remove
- `world/ability_engine.py` — Ability dispatcher: `use_ability()`, cooldown management, domain resource (build/spend/get), effect handlers delegate to `combat_engine` and `status_effects`
- `world/ability_registry.py` — Data-driven ability definitions: `ABILITIES` dict (500+ entries across 10 authored domains), derived lookups `DOMAIN_ABILITIES` and `SUBCLASS_SIGNATURES`, `get_ability()`
- `commands/combat_commands.py` — Player combat commands (`CmdAttack`, `CmdFlee`, `CmdTarget`, `CmdPass`) and `CombatCmdSet`
- `commands/default_cmdsets.py` — `CmdAttack` also registered in `CharacterCmdSet` (initiates combat from outside CombatCmdSet)
- `world/zone_scaling.py` — `get_player_damage_to_mob`, `get_mob_damage_for_player`, `apply_resistance`

## Key Concepts
- **Action dicts, not side effects:** `combat_ai.py` returns action dicts for CombatScript to dispatch — it does NOT resolve damage directly. `combat_engine.py` resolves damage and mutates HP.
- **Dead character guard:** `use_ability()` checks `ndb.hp <= 0` at entry and rejects ability use while dead. This prevents dead characters from acting before respawn completes.
- **Turn timer cleanup on combatant removal:** `CombatScript.remove_combatant()` cancels the active turn timer (`ndb.turn_timer_id`) if removing the current combatant, preventing stale timer callbacks from firing after removal.
- **Ability registry is pure data:** 16-field dicts per ability. Derived lookups (`DOMAIN_ABILITIES`, `SUBCLASS_SIGNATURES`) auto-built at module level. Add new abilities to `ABILITIES` dict only.
- **`_compute_raw_damage` helper:** Shared private function for base damage calculation. Characters use weapon + strength modifier; mobs use `ref_damage_min/max`. Called by `resolve_basic_attack` and available for other damage paths.
- **`effect_params` dict pattern:** Effect handlers (`_handle_dot`, `_handle_buff`, `_handle_debuff`, `_handle_utility`, `_handle_social`, `_handle_tactical`, `_handle_status`) and `resolve_ability_damage` read from `ability["effect_params"]` first, falling back to top-level ability keys for backwards compat. New ability definitions should put `damage_base`, `status_effect`, `duration`, `magnitude`, `buff_type`, `debuff_type`, `tactical_action`, `utility_action` inside `effect_params`.
- **Domain resource types:** Combat=`momentum`, Tactics=`command`, Subterfuge=`focus`, Diplomacy=`influence`, Arcana=`mana`, Resonance=`resonance`, Naturalism=`balance`, Alchemy=`reagents`, Engineering=`components`, Remnance=`echoes`. Each domain has a single resource type. Resource is volatile (`ndb`), managed by `ability_engine.py`.
- **Subterfuge Focus combo points:** Focus is a combo point system capped at 0-5. Builders (`is_builder: True` in `effect_params`) have `resource_cost: 0` and generate 1 Focus on hit. Spenders cost 1-5 Focus. Some capstones have `consumes_all_focus: True` — damage scales with Focus spent. Miss resets Focus to 0. Skipping a Subterfuge turn resets Focus to 0.
- **Naturalism Balance pendulum:** Fingerprint CALIBRATE — Balance is a pendulum position (0=Feral, 100=Calm, 50=Neutral). `resource_cost` is always 0 — Balance is never spent, only shifted. All Naturalism abilities have `balance_shift` (integer, positive=toward Calm, negative=toward Feral) and `balance_type` (`"feral"` or `"calm"`) in `effect_params`. Offensive abilities (damage/dot/debuff) are powered by Feral position (`balance_type: "feral"`) and shift toward Calm (`balance_shift > 0`). Defensive abilities (heal/buff) are powered by Calm position (`balance_type: "calm"`) and shift toward Feral (`balance_shift < 0`). The pendulum effect: dealing damage makes your next heal stronger, healing makes your next damage stronger. Nature's Equilibrium capstone requires Balance 40-60. Scaling: naturalism → resonance.
- **Alchemy reagent depletion:** Fingerprint PREPARE — preparation as combat philosophy. Reagent costs represent actual stock depletion. Running out mid-fight is a design-intended failure state. Scaling: alchemy → acuity.
- **Resonance builder/spender pattern:** Resonance T1-T2 builders have `resource_cost: 0` and generate resonance via `effect_params.resonance_generated`. Spenders cost 60-100 resonance. Decay: -10 per round during combat. ALL resonance abilities have `attuned_variants` populated (room-flag-conditional bonus effects).
- **Arcana mana management:** Arcana fingerprint is RATION — cross-encounter mana pool. Many abilities have `charge_turns` (1-2). Elements: fire, ice, lightning, arcane. Room flags written: `scorched`, `frozen`, `charged`, `arcane_residue`.
- **Engineering companion-centric:** Fingerprint CONSTRUCT — companion-centric, fuel decisions matter. Components are pre-crafted consumables. Costs: T1=10-15, T2=15-25, T3=20-35, T4=30-50. Scaling: engineering → acuity. Subclasses each have a different companion chassis type.
- **Remnance excavation-powered:** Fingerprint EXCAVATE — accumulated knowledge as combat power. Echoes build from abilities AND investigation bonus (+15 per lore fragment, +10 per ancient site, persists 3 encounters, stacks to 40). Scaling: remnance → mana. The hidden domain — investigation between fights fuels combat power.
- **Ability tiers:** 1-4, gated by Guild-Tier Score (GTS). Tier thresholds: 0/20/50/85.
- **Subclass signatures:** Tier 3 + Tier 4 abilities with `subclass_id` set and `scaling_secondary` pointing to the blend domain. 9 subclasses per primary domain.
- **CombatCmdSet:** `mergetype="Replace"`, `priority=10`, `no_exits=True`. Added/removed dynamically by `CombatScript`.
- **CmdAttack dual role:** In `CharacterCmdSet` it initiates combat. Inside `CombatCmdSet` it performs basic attack.
- **DOMAIN_TO_STAT mapping:** Maps 10 domain names to base attribute stat names for ability scaling formula: `ability_base * (1 + primary_stat*0.02 + secondary_stat*0.01)`.
- **Crit system (D-20):** Characters: 5% base + Acuity×0.002. Mobs: `db.crit_chance` or 3% flat. Multiplier 2.0×.
- **Scripted sequences:** Named mob triggers (combat_start, hp_below_X, round_N, target_flees, on_death). Fire-once via `ndb.fired_sequence_triggers` set.
- **Mob death flow:** `handle_mob_death()` snapshots room contents (`pre_death_ids`) BEFORE calling `mob.at_death()`, then spawns corpse, moves only newly-dropped loot (items not in `pre_death_ids`) into corpse, and explicitly calls `mob.delete()` to remove the mob from the game world.
- **Player death flow (D-14):** `handle_player_death()` → death penalty via `banking.on_character_death()` (20% carried Scales dropped to corpse, session XP wiped) → items moved to corpse with `InventoryItem` DB rows cleaned up → `_respawn_player()` teleports to `respawn_point` tagged room (with `move_hooks=False` to skip movement triggers) → restores 25% max HP and stamina.
- **Corpse lifecycle:** `spawn_corpse()` → grace period → open → decayed (deleted). Player corpses skip grace. `delay()` drives transitions.

## Authored Domain Pools
All 10 domains are fully authored (15 base + 18 subclass signatures each):
- **Combat** (momentum) — PRESS fingerprint, sustained aggression
- **Tactics** (command) — tactical positioning, group coordination
- **Subterfuge** (focus) — READ fingerprint, combo point system (0-5 cap). Builders generate 1 Focus on hit (`is_builder: True`), spenders consume 1-5. Capstones use `consumes_all_focus: True` for scaling damage. Miss or skipped turn resets to 0. Scaling: subterfuge → agility
- **Diplomacy** (influence) — LEVERAGE fingerprint, converting relationships into power. Scaling: diplomacy → presence
- **Arcana** (mana) — RATION fingerprint, cross-encounter mana management. Scaling: arcana → mana
- **Resonance** (resonance) — ATTUNE fingerprint, builder/spender with decay and env reading. Scaling: resonance → resonance
- **Naturalism** (balance) — CALIBRATE fingerprint, pendulum position (0-100). `resource_cost: 0` always; `balance_shift`/`balance_type` in effect_params drive the swing. Scaling: naturalism → resonance
- **Alchemy** (reagents) — PREPARE fingerprint, finite reagent stock. Scaling: alchemy → acuity
- **Engineering** (components) — CONSTRUCT fingerprint, companion-centric fuel decisions. Scaling: engineering → acuity. Subclasses: ironsmith, gearhand, growsmith, runewright_forge, sparkshaper, dealsmith, siegewright, fumehand, bucketborn
- **Remnance** (echoes) — EXCAVATE fingerprint, investigation-fueled combat. Scaling: remnance → mana. Subclasses: dragonkin, truthshadow, worldroot, sealbreaker, firstform, ancientvoice, rootpoison, firstblade, dragonwright

## Critical Rules
1. **Combat AI returns dicts, combat engine mutates state** — never resolve damage in `combat_ai.py`
2. **Minimum 1 damage** — `resolve_basic_attack` and `apply_resistance` enforce `max(1, ...)`
3. **Flee check runs before ability selection** — low-HP mobs escape without wasting an ability
4. **Call-for-help capped at 3 per encounter** — tracked via `combat_handler.ndb.call_for_help_count`
5. **CmdAttack is in BOTH CharacterCmdSet and CombatCmdSet** — CharacterCmdSet copy initiates combat; CombatCmdSet copy performs in-combat attacks
6. **Lazy imports throughout** — `base_attributes`, `status_effects`, `zone_scaling`, `banking` imported inside functions to avoid circular deps
7. **Elite/boss scaling applies AFTER resistance** — order matters in damage pipeline
8. **Ability `room_flag_written` must be in `FLAG_VOCABULARY`** — abilities set room flags on use; flags not in vocabulary are silently ignored with a warning
9. **Effect params use fallback pattern** — always `params.get("key") or ability.get("key", default)`. This preserves backwards compat with old top-level keys while preferring `effect_params`
10. **Subterfuge `is_builder` and `consumes_all_focus` flags live in `effect_params`** — builders have `resource_cost: 0` with `"is_builder": True`; capstone spenders have `"consumes_all_focus": True` for Focus-scaled damage
11. **Naturalism `balance_shift` and `balance_type` live in `effect_params`** — `resource_cost` is always 0; `balance_shift` (int, positive=toward Calm, negative=toward Feral) and `balance_type` (`"feral"` or `"calm"`) control the pendulum
12. **Respawn uses tag lookup + move_hooks=False** — `_respawn_player()` finds destination via `search_tag("respawn_point", category="spawn_point")`. Falls back to `character.home`, then no-ops. Uses `move_hooks=False` to skip movement triggers (e.g. room enter effects). Never hardcode room dbrefs
13. **Death penalty order matters** — `on_character_death()` runs BEFORE `_respawn_player()` so corpse receives dropped Scales at death location, not respawn location
14. **Pre-death snapshot for mob loot** — `handle_mob_death()` captures `pre_death_ids` before `at_death()` runs, so `_move_room_loot_to_corpse()` only sweeps newly-dropped items. Never use time-based heuristics for loot identification
15. **Player death cleans up InventoryItem rows** — `handle_player_death()` deletes `InventoryItem` records for items transferred to corpse, keeping Django model in sync with Evennia object locations
16. **`handle_mob_death()` explicitly deletes the mob** — `mob.delete()` is called after loot is moved to corpse. Do not rely on `at_death()` to remove the mob object
17. **Dead characters cannot use abilities** — `use_ability()` checks `ndb.hp <= 0` at entry and returns failure. This prevents dead characters from acting before respawn
18. **Turn timer cancelled on combatant removal** — `remove_combatant()` cancels `ndb.turn_timer_id` if removing the active combatant, preventing stale timer callbacks

## References
- **Ability Registry:** `world/ability_registry.py` — all ability definitions and derived lookups
- **Ability Engine:** `world/ability_engine.py` — dispatcher and resource management
- **Zone Scaling:** `world/zone_scaling.py` — scale factors, resistance
- **Status Effects:** `world/status_effects.py` — effect checks and modifiers
- **Base Attributes:** `world/base_attributes.py` — HP derivation, stat recording
- **Mob Typeclasses:** `typeclasses/mobs.py` — mob attribute schema
- **Banking:** `world/banking.py` — `on_character_death()` for death penalty (Scales drop + XP wipe)
- **Inventory Model:** `world/models.py` — `InventoryItem` records cleaned up during player death

---
**Last Updated:** 2026-04-10
