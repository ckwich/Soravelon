---
name: recovery-engine
description: HP/stamina recovery engine — 4-tier regen (active/rest/sleep/bed), medic NPC blessings with Scales cost and cooldowns, and 4 player commands
---

## Activation

This skill triggers when editing these files:
- `world/recovery_engine.py`
- `commands/cmd_recovery.py`
- `typeclasses/characters.py`
- `tests/test_recovery_engine.py`

Keywords: recovery, regen, rest, sleep, wake, heal, blessing, medic, fortify, vigor, purify, recovery state, regen tick, bed, is_medic, spend stamina

---

You are working on **the recovery engine** (`world/recovery_engine.py`) — HP/stamina regeneration, stamina spending, medic NPC blessings, and player recovery commands.

## Key Files
- `world/recovery_engine.py` — Regen tick loop, recovery state management, `spend_stamina()`, medic blessings
- `commands/cmd_recovery.py` — 4 commands: CmdRest (`rest`/`sit`), CmdSleep (`sleep`), CmdWake (`wake`/`stand`), CmdBlessing (`blessing`/`bless`). Thin dispatchers — no game logic
- `commands/default_cmdsets.py` — All 4 recovery commands registered in `CharacterCmdSet`
- `typeclasses/characters.py` — `start_regen()` called in `at_object_creation()`, `stop_regen()` in `at_pre_unpuppet()`, movement cancels recovery in `at_after_move()`, `at_look()` blocks vision during sleep
- `world/status_effects.py` — `fortify` and `vigor` non-stackable effects (15% damage reduction / bonus) applied by blessings
- `world/base_attributes.py` — `derive_max_hp()`, `derive_max_stamina()` used for regen cap
- `world/oob_publisher.py` — `push_stat_update()` called after HP/stamina changes
- `tests/test_recovery_engine.py` — Pure unittest + MagicMock tests (no Evennia DB)

## Key Concepts
- **Four-tier regen rates:** `active` (1%), `resting` (3%), `sleeping` (6%), `sleeping_bed` (10%) — percentage of max stat per 10s tick
- **Recovery state is volatile:** `character.ndb.recovery_state` (`"active"`, `"resting"`, `"sleeping"`). Lost on disconnect. Defaults to `"active"` via `start_regen()`
- **`spend_stamina(character, amount)` → `(bool, str)`:** Centralized stamina deduction with stat push. Used by `CmdShout` and any system needing stamina cost. Returns failure if insufficient stamina. Automatically calls `push_stat_update()` on success
- **HP/stamina persistence across sessions (F4 fix):** `db._saved_hp` and `db._saved_stamina` are written in `at_pre_unpuppet()` and restored in `at_post_puppet()`. Prevents disconnect exploit where players could F4 to reset HP to max. Values cleared after restore
- **Delay-driven tick loop:** `_schedule_next_tick()` uses `evennia.utils.delay()` with `REGEN_INTERVAL=10s`. Handle stored in `character.ndb.regen_handle`. Stops when HP and stamina both full
- **Combat skips regen:** `_regen_tick()` checks `ndb.combat_handler` — if in combat, re-schedules but does NOT heal
- **Bed detection:** `_room_has_bed()` checks room contents for `obj.db.is_bed`. Upgrades sleeping rate from 6% to 10%
- **Sleep blindness:** `character.ndb.is_sleeping` set True during sleep state. `Character.at_look()` returns a message instead of room description when sleeping
- **Movement cancels recovery:** `Character.at_after_move()` checks `ndb.recovery_state != "active"` and calls `cancel_recovery()` to reset state
- **Character lifecycle wiring:** `start_regen()` at end of `at_object_creation()` (login); `stop_regen()` in `at_pre_unpuppet()` (disconnect); HP/stamina saved before stop, restored on next puppet
- **Four medic blessings:** `heal` (full HP, 20 Scales, 120s CD), `fortify` (defense buff, 30 Scales, 120s CD), `vigor` (offense buff, 30 Scales, 120s CD), `purify` (cleanse all effects, 40 Scales, 60s CD)
- **Medic NPC detection:** `CmdBlessing` scans room contents for `obj.db.is_medic == True`. Medic flag set directly in zone spec (e.g. `_medic.db.is_medic = True` in vaels_crossing.py)
- **Blessing cooldowns:** Per-blessing timestamps in `character.db.blessing_cooldowns` dict. Time-based (wall clock via `time.time()`)
- **Blessing cost:** Deducted from `character.db.carried_scales` (on-person currency, not bank)

## Critical Rules
1. **All public functions return `(bool, str)` tuples** — follows repo-wide convention
2. **Regen handle is volatile** — `ndb.regen_handle` auto-cleared on disconnect. `start_regen()` must be called at login
3. **Never heal during combat** — `_regen_tick()` checks `ndb.combat_handler` and skips HP/stamina changes if present
4. **Blessing effects delegate to `status_effects`** — `fortify` and `vigor` are registered in `NON_STACKABLE_EFFECTS` with `damage_reduction`/`damage_bonus` modifiers
5. **Lazy imports throughout** — `base_attributes`, `oob_publisher`, `status_effects`, `evennia.utils` imported inside functions to avoid circular deps
6. **`set_recovery_state()` blocked in combat** — returns `(False, ...)` if `ndb.combat_handler` exists
7. **Commands are thin dispatchers** — all game logic lives in `world/recovery_engine.py`, not in `commands/cmd_recovery.py`
8. **Medic flag is manual** — `is_medic` is set directly on NPC db attrs in zone spec files, not through AreaBuilder DSL
9. **HP/stamina saved as `db._saved_hp`/`db._saved_stamina`** — written in `at_pre_unpuppet()`, restored in `at_post_puppet()`, then cleared. Never read these outside the login/logout lifecycle
10. **Use `spend_stamina()` for stamina costs** — any system that deducts stamina should call `spend_stamina()` rather than manually reading/writing `ndb.stamina`. It handles the stat push automatically

## References
- **Status Effects:** `world/status_effects.py` — `fortify`, `vigor` effect definitions and `get_effect_modifiers()`
- **Base Attributes:** `world/base_attributes.py` — `derive_max_hp()`, `derive_max_stamina()`
- **OOB Publisher:** `world/oob_publisher.py` — `push_stat_update()` for client notification
- **Character Hooks:** `typeclasses/characters.py` — lifecycle wiring for start/stop regen, movement cancel, and HP/stamina persistence
- **Item Effects:** `world/item_effects.py` — `consume_item()` uses `_apply_hp`/`_apply_stamina` helpers (similar pattern)
- **Tests:** `tests/test_recovery_engine.py`

---
**Last Updated:** 2026-04-05
