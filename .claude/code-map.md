## Codebase Structure

**Hub files (most depended-on — prioritize reading these):**
- `commands\command.py` — 11 dependents
- `world\models.py` — 7 dependents
- `world\area_builder.py` — 5 dependents
- `world\area_validator.py` — 3 dependents
- `world\world_state.py` — 3 dependents
- `world\__init__.py` — 3 dependents
- `typeclasses\objects.py` — 2 dependents
- `typeclasses\scripts.py` — 2 dependents
- `world\mob_affixes.py` — 2 dependents
- `world\ability_registry.py` — 1 dependents

**Domain clusters:**
- **commands\cmd_abilities.py** (12 files): `commands\command.py`, `commands\cmd_abilities.py`, `commands\cmd_alias.py`, `commands\cmd_ancestry.py`, `commands\cmd_crafting.py`
- **tests\test_guild_engine.py** (11 files): `world\models.py`, `world\world_state.py`, `world\guild_engine.py`, `world\mob_disposition.py`, `tests\test_guild_engine.py`
- **tests\test_area_builder.py** (9 files): `world\area_builder.py`, `world\__init__.py`, `world\area_validator.py`, `tests\test_area_builder.py`, `tests\test_zone_serializer.py`
- **typeclasses\characters.py** (3 files): `typeclasses\objects.py`, `typeclasses\characters.py`, `typeclasses\rooms.py`
- **typeclasses\mobs.py** (3 files): `world\mob_affixes.py`, `world\mob_affix_roller.py`, `typeclasses\mobs.py`
- **typeclasses\scripts.py** (3 files): `typeclasses\scripts.py`, `world\scripts\flight_script.py`, `world\scripts\patrol_script.py`
- **world\nodes\node_effects.py** (3 files): `world\nodes\node_effects.py`, `world\node_helpers.py`, `world\scripts\node_script.py`
- **tests\test_ability_engine.py** (2 files): `world\ability_registry.py`, `tests\test_ability_engine.py`
- **tests\test_base_attributes.py** (2 files): `world\base_attributes.py`, `tests\test_base_attributes.py`
- **tests\test_room_state.py** (2 files): `world\room_state.py`, `tests\test_room_state.py`
- **tests\test_status_effects.py** (2 files): `world\status_effects.py`, `tests\test_status_effects.py`
- **world\crafting_definitions.py** (2 files): `world\crafting_definitions.py`, `world\crafting_engine.py`
- **world\dialogue_definitions.py** (2 files): `world\dialogue_definitions.py`, `world\dialogue_engine.py`
- **world\skill_definitions.py** (2 files): `world\skill_definitions.py`, `world\skill_engine.py`

*152 files, 50 edges — updated 2026-03-30*
