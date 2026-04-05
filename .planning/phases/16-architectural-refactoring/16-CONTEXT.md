# Phase 16: Architectural Refactoring - Context

**Gathered:** 2026-04-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Structural code quality improvements identified in the deep audit. No new gameplay features — purely internal refactoring to make the codebase maintainable, consistent, and correct. All existing behavior must be preserved (no functional changes).

</domain>

<decisions>
## Implementation Decisions

### Typeclass God Methods → Lifecycle Orchestrators
- **D-01:** Create domain-split lifecycle orchestrator files: `world/session_lifecycle.py` (login/logout), `world/movement_lifecycle.py` (move), `world/death_lifecycle.py` (mob death).
- **D-02:** Each orchestrator exposes a single entry point (e.g., `on_login(character)`, `on_move(character, source, dest)`) that coordinates all the individual system calls internally.
- **D-03:** Typeclass hooks become thin 3-line delegates: call the orchestrator, nothing else. Example: `at_post_puppet` calls `session_lifecycle.on_login(self)`.
- **D-04:** Orchestrators import world modules lazily (inside functions) to avoid circular imports.

### Command Logic Extraction
- **D-05:** Move `cmd_fishing._catch_fish()` logic (quality calc, bait consumption, tool durability, skill XP) into `world/gathering_engine.py` as a `catch_fish()` function.
- **D-06:** Move `cmd_gathering._gather_callback()` logic (move validation, item creation, quality calc, bonus quantity, tool durability) into `world/gathering_engine.py` as an expanded `gather_from_node()` or new `complete_gather()` function.
- **D-07:** Commands retain only: argument parsing, user messages, calling the engine. No game state mutation.

### Duplicate Logic Consolidation
- **D-08:** Extract only when the SAME computation appears in 2+ places with identical logic. No premature abstractions.
- **D-09:** Specific targets: weapon damage fallback (combat_engine.py two branches), effect list search (status_effects.py two loops), threshold-checking patterns.
- **D-10:** New helpers go in their owning module (e.g., `_find_effect()` in status_effects.py), not a separate utils file.

### Naming Consistency
- **D-11:** Rename `mob_template` → `mob_template_key` and `mob_id` → `mob_instance_id` across all modules to make the distinction explicit. mob_template_key = template registry key, mob_instance_id = spawned instance tag.
- **D-12:** Update all references in world/*.py, typeclasses/*.py, commands/*.py, and tests/*.py. This is a breaking rename — must be done atomically.

### SaverDict Audit
- **D-13:** Systematic sweep of all `db.*` dict/set/list mutations. Every mutation must use copy-mutate-assign pattern. Fix any that mutate in-place.
- **D-14:** Key targets: any `del db.foo[key]`, `db.foo.append()`, `db.foo.add()`, `db.foo[key] = val` without prior `dict(db.foo)` copy.

### Return Type Enforcement
- **D-15:** Every public function in `world/*.py` engine modules must return `(bool, str)` tuples per project convention. Fix any that return None, bare strings, or skip return statements.
- **D-16:** Internal/private functions (prefixed with `_`) are exempt from tuple returns.

### Import Hygiene
- **D-17:** Move heavy top-level imports in typeclasses/ to lazy (inside methods) where they import from world/.
- **D-18:** Remove all unused imports.
- **D-19:** Verify no circular import paths exist between typeclasses/ and world/ modules.

### Claude's Discretion
- Exact helper function names and signatures for extracted duplicates
- Whether to inline small orchestrator calls vs function references
- Import ordering within files

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Typeclasses (refactoring targets)
- `typeclasses/characters.py` — at_post_puppet (lines 97-161), at_pre_unpuppet (200-248), at_after_move (250-331)
- `typeclasses/mobs.py` — at_death (lines 152-223)
- `typeclasses/rooms.py` — at_object_receive (96-148)

### Commands (logic extraction targets)
- `commands/cmd_fishing.py` — _catch_fish (226-303), _idle_catch (195-222), _on_reel (152-165)
- `commands/cmd_gathering.py` — _gather_callback (87-154)

### World engines (consolidation + naming targets)
- `world/combat_engine.py` — weapon damage calc (lines 155-168)
- `world/status_effects.py` — effect lookup loops (196-201, 227-233)
- `world/mob_spawner.py` — mob_template references
- `world/combat_ai.py` — mob_id references
- `world/quest_engine.py` — mixed mob_template/mob_id usage

### Project conventions
- `.claude/skills/base/skill.md` — Critical rules (return tuples, SaverDict pattern, lazy imports)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/item_effects.py` — Recently extracted from cmd_abilities; good reference for the extraction pattern
- `world/recovery_engine.py:spend_stamina()` — Recently extracted from cmd_social; same pattern

### Established Patterns
- Lazy imports inside `func()` in all commands — follow this in new orchestrator modules
- `(bool, str)` return convention across all world/ engines — enforce consistently
- SaverDict copy pattern documented in base skill — scan for violations

### Integration Points
- Typeclass hooks are the only callers of the code being refactored — changes are internal
- Tests mock world module functions, so renames require updating mock paths
- No external API consumers — safe to rename freely

</code_context>

<specifics>
## Specific Ideas

- User is building a companion game editor app that reads/writes mob templates. The mob_template_key/mob_instance_id rename is a step toward making game data more accessible to external tools. A full "serializable game data format" phase should follow this refactoring.
- Lifecycle orchestrators should be thin coordination layers, not new business logic. They call existing functions in the same order the typeclass hooks did — just from a world/ module instead.

</specifics>

<deferred>
## Deferred Ideas

- **Serializable game data format for companion apps** — User wants all game data (mob templates, items, zones, etc.) in a format easily read/written by external tools like the game editor app. This is a major data architecture change, not a rename. Separate phase.
- **Equipment query caching** — can_equip() does 5+ DB queries per call. Could cache equipped items on ndb at login. Performance optimization, not code quality.

</deferred>

---

*Phase: 16-architectural-refactoring*
*Context gathered: 2026-04-05*
