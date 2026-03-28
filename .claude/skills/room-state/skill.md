---
name: room-state
description: Volatile room flags with lazy decay — elemental, tactical, environmental, and node state flags driving combat and Sense display
---

## Activation

This skill triggers when editing these files:
- `world/room_state.py`
- `typeclasses/rooms.py`

Keywords: room state, room flag, FLAG_VOCABULARY, add_room_flag, get_room_flags, Sense, dominant flag, room decay

---

You are working on **the room state system** (`world/room_state.py`) — volatile per-room flags that represent recent events and drive combat modifiers, Sense display, and NPC reactions.

## Key Files
- `world/room_state.py` — Flag vocabulary, lazy-decay engine, Sense priority/display text
- `typeclasses/rooms.py` — `SoravelonRoom` hosts `ndb.room_state` dict
- `world/ability_registry.py` — Abilities reference `room_flag_written` values that must exist in `FLAG_VOCABULARY`

## Key Concepts
- **Volatile `ndb` storage:** All state lives in `room.ndb.room_state` dict with `flags` (name→rounds_remaining) and `last_updated` timestamp. No DB persistence — flags vanish on server restart
- **Lazy decay:** No global ticker. Flags decay on read — `get_room_flags()` calculates elapsed rounds since `last_updated` and removes expired flags
- **Round-based duration:** `ROUND_DURATION_SECONDS = 3`. Flag durations are in combat rounds, not wall-clock seconds
- **Flag vocabulary is the contract:** `FLAG_VOCABULARY` dict defines all valid flag names with description, typical duration, writers (systems that set it), and readers (systems that respond). **Never invent flags outside this vocabulary**
- **Persistent flags:** Duration `-1` means the flag never decays (e.g., `node_critical`) — must be explicitly removed via `remove_room_flag()`
- **Sense priority:** `SENSE_PRIORITY` list orders flags from most to least significant. `get_dominant_flag()` returns the highest-priority active flag for display
- **Still detection:** Rooms with no active flags and no recent activity (20+ rounds) automatically qualify as `"still"`

## Flag Categories
- **Elemental:** charged, burning, frozen, toxic_air, resonant, void_touched
- **Biological:** fading_life, blood_soaked, living_wood, overgrown, rotting
- **Chemical:** caustic, poisoned_air
- **Tactical:** fortified, scouted, disrupted
- **Environmental:** power_vacuum, unsettled, ancient_presence, still
- **Subterfuge:** shadow_marked, exposed
- **Social/Diplomacy:** intimidated, inspired, ordered
- **Death:** predator_kill, corrupted_death
- **Node:** node_critical (-1 persistent), node_calming
- **Pending (referenced by abilities, need vocabulary entries):** bloodied, shattered, crushed, devastated, scorched, arcane_residue, ancient_ground, excavated, mechanized, trapped

## Critical Rules
1. **Always use `FLAG_VOCABULARY` names** — `add_room_flag()` logs a warning and no-ops for unknown flags
2. **Add new flags to vocabulary FIRST** — document writers and readers before using in system code
3. **Duration refresh takes the max** — `add_room_flag()` keeps the longer of existing vs new duration
4. **No global ticker** — decay is lazy. Don't add a periodic callback for room state cleanup
5. **`SENSE_DISPLAY` must cover all vocabulary entries** — every flag needs player-facing atmospheric text
6. **Ability room flags must be in vocabulary** — `ability_registry.py` `room_flag_written` values are checked against `FLAG_VOCABULARY` at runtime; missing flags are silently dropped

## References
- **Room typeclasses:** `typeclasses/rooms.py`
- **Node system:** `world/scripts/node_script.py` — sets `node_critical` and `node_calming` flags
- **Ability registry:** `world/ability_registry.py` — `room_flag_written` values per ability

---
**Last Updated:** 2026-03-27
