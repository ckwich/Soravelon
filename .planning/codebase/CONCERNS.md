# Codebase Concerns

**Analysis Date:** 2026-03-24

## Tech Debt

**Pervasive `getattr(obj.db, ...)` Anti-Pattern:**
- Issue: 22+ instances of `getattr(character.db, 'attr', default)` across the codebase. Evennia's `db` handler already returns `None` for missing attributes, so `getattr` is unnecessary and masks missing attribute initialization. The `or 0` / `or 0.0` fallback pattern (e.g., `getattr(character.db, 'carried_scales', 0) or 0`) conflates `None` with falsy values like `0`.
- Files: `world/inventory_engine.py` (lines 153, 174, 217, 342, 428), `world/banking.py` (lines 32, 57, 213), `world/mob_disposition.py` (lines 67, 117, 128), `world/mob_affix_roller.py` (line 40), `world/world_state.py` (line 65), `world/node_helpers.py` (line 45), `typeclasses/exits.py` (line 58)
- Impact: Hides bugs where attributes are never initialized. If an attribute is genuinely missing, the fallback silently proceeds instead of surfacing the root cause.
- Fix approach: Replace all `getattr(obj.db, 'attr', default)` with direct `obj.db.attr` access. Ensure all attributes are initialized in `at_object_creation()`. Use explicit `None` checks where needed: `val = obj.db.attr; val = val if val is not None else default`.

**`strength` Attribute Never Initialized on Character:**
- Issue: `world/inventory_helpers.py` (line 15-16) and `world/inventory_engine.py` (line 342) read `character.db.strength`, but `typeclasses/characters.py` `at_object_creation()` never sets it. Tests manually set it (`tests/test_typeclasses.py` line 200, `tests/test_inventory_engine.py` line 17).
- Files: `typeclasses/characters.py`, `world/inventory_helpers.py`, `world/inventory_engine.py`
- Impact: Any character created through normal gameplay will have `None` for strength. `inventory_helpers.py` handles this with a `None` check, but `inventory_engine.py` uses the `getattr` anti-pattern. Carry capacity calculation will silently default to 10 instead of failing visibly.
- Fix approach: Add `self.db.strength = 10` (or the intended default) to `Character.at_object_creation()`.

**`is_quest_item` Attribute Never Initialized on SoravelonItem:**
- Issue: `typeclasses/objects.py` `SoravelonItem.at_object_creation()` never sets `self.db.is_quest_item`, but it is read in `can_drop()`, `can_be_sold()`, and referenced during pickup in `inventory_engine.py` (line 176) as `bool(item.db.is_quest_item)`.
- Files: `typeclasses/objects.py`, `world/inventory_engine.py`
- Impact: Works by accident because `None` is falsy, but violates the convention of initializing all attributes in `at_object_creation()`.
- Fix approach: Add `self.db.is_quest_item = False` to `SoravelonItem.at_object_creation()`.

**Stub Functions in Banking System:**
- Issue: `on_character_death()` and `handle_carried_scales_on_death()` are empty stubs with `pass` bodies.
- Files: `world/banking.py` (lines 286-291)
- Impact: Character death has no economic consequence. Carried Scales are not dropped or lost. This is a missing game mechanic, not just a placeholder.
- Fix approach: Implement death penalty logic (e.g., drop percentage of carried Scales, apply debt).

**Quest Modifier Stub:**
- Issue: `get_quest_modifier()` always returns 0.0 with comment "quest system not yet built."
- Files: `world/mob_disposition.py` (lines 96-98)
- Impact: Quest-driven disposition modifiers have no effect. Mob encounters cannot be influenced by active quests.
- Fix approach: Implement when quest system is built. The stub interface is correctly designed.

**Loot Tables Stub:**
- Issue: `world/loot_tables.py` contains only tier modifier constants and a single getter. No actual drop table logic, item generation, or loot distribution.
- Files: `world/loot_tables.py`
- Impact: Mobs cannot drop loot. The affix/rarity system generates mob difficulty modifiers but has no loot payoff.
- Fix approach: Build full loot table system with drop rates, material tier integration from `zone_scaling.py`, and group loot mode distribution from `group_engine.py`.

**WorldEventScript Stub:**
- Issue: `WorldEventScript` in `typeclasses/scripts.py` (lines 37-46) has creation attributes but no behavior methods.
- Files: `typeclasses/scripts.py`
- Impact: No world events can run. The script type exists but does nothing.
- Fix approach: Implement when world event system is designed.

**No Custom Commands Registered:**
- Issue: `commands/default_cmdsets.py` has empty `at_cmdset_creation()` methods with no custom commands added. All four cmdsets (Character, Account, Unloggedin, Session) use only Evennia defaults.
- Files: `commands/default_cmdsets.py`, `commands/command.py`
- Impact: Players cannot interact with any custom game system (inventory, banking, group, etc.) through commands. All game logic exists as library code with no player-facing interface.
- Fix approach: Create command classes for each system (CmdInventory, CmdBank, CmdGroup, CmdLook override, etc.) and register them in `CharacterCmdSet.at_cmdset_creation()`.

**No Area Spec Files:**
- Issue: `world/areas/` directory contains only `__init__.py`. The `_load_all_zones()` function in `server/conf/at_server_startstop.py` scans this directory but finds nothing to load.
- Files: `world/areas/__init__.py`, `server/conf/at_server_startstop.py`
- Impact: No zones exist in the game. The AreaBuilder system is fully built and tested but has no content to build.
- Fix approach: Create area spec files (e.g., `world/areas/ashenveil.py`) using the AreaBuilder API.

## Known Bugs

**NodeGravityExit Applies Penalty After Movement:**
- Symptoms: `NodeGravityExit.at_traverse()` calls `super().at_traverse()` first, then sets `gravity_penalty = -1`. The base `SoravelonExit.at_traverse()` reads the destination's penalty BEFORE movement. So `NodeGravityExit` overrides the penalty AFTER the parent has already applied the destination-based penalty.
- Files: `typeclasses/exits.py` (lines 91-99)
- Trigger: Any traversal through a NodeGravityExit.
- Workaround: The override happens after `super()` returns, so the final value is correct (-1), but the message from the parent's logic may have used a different value.

**LockedExit Keyring Check Uses search_object per Key:**
- Symptoms: Each keyring item is looked up individually via `evennia.search_object("#" + str(record.item_id))`, creating one DB query per keyring item.
- Files: `typeclasses/exits.py` (lines 48-59)
- Trigger: Any player with keyring items traversing a LockedExit.
- Workaround: Functional but slow for players with many keys.

**Cross-Zone Exit Resolution is Order-Dependent:**
- Symptoms: If zone A references a room in zone B, but zone B loads after zone A, the cross-zone exit is silently skipped with a warning. On next restart it may or may not resolve depending on `sorted()` filename order.
- Files: `world/area_builder.py` (lines 549-574), `server/conf/at_server_startstop.py` (line 96)
- Trigger: Any cross-zone exit where target zone loads after source zone.
- Workaround: Name area files so dependencies load first (alphabetical ordering via `sorted()`). Not robust.

## Security Considerations

**No Input Validation on Banking Amounts:**
- Risk: `deposit()`, `withdraw()`, and related functions validate `amount > 0` but do not check for integer overflow or unreasonably large values. The `amount` parameter type is not enforced.
- Files: `world/banking.py`
- Current mitigation: Django `IntegerField` has DB-level limits. F() expressions prevent negative balances atomically.
- Recommendations: Add explicit type checking and upper bounds on transaction amounts. Validate at command layer before reaching engine functions.

**No Rate Limiting on Banking Operations:**
- Risk: No throttle on deposit/withdraw/draft operations. A scripted client could spam transactions.
- Files: `world/banking.py`
- Current mitigation: None.
- Recommendations: Add cooldown via `ndb` timestamp check or Evennia's built-in throttle utilities.

**search_object by dbref String Construction:**
- Risk: Multiple modules construct dbref strings via `"#" + str(id)` for `evennia.search_object()`. If `id` is manipulated (e.g., through a command argument), this could search for unintended objects.
- Files: `world/group_engine.py`, `world/banking.py`, `world/scripts/node_script.py`, `typeclasses/exits.py`, `world/zone_registry.py`
- Current mitigation: All current callers use internally-stored integer IDs, not user input.
- Recommendations: When commands are built, never pass raw user input to `search_object("#" + ...)`. Always resolve objects through Evennia's search infrastructure which respects access controls.

## Performance Risks

**Global Decay Tick Iterates All Characters:**
- Problem: `decay_tick_all()` in `world/world_state.py` (lines 85-104) queries ALL player characters and calls `apply_decay()` on each offline one. Each `apply_decay()` reads and writes up to 4 dimension scores.
- Files: `world/world_state.py`
- Cause: No batch update mechanism. Each character is processed individually with multiple `setattr(character.db, ...)` calls.
- Improvement path: Use Django ORM bulk operations or batch the attribute writes. Consider processing in chunks. At 1000+ characters this tick could take significant time.

**Session XP Safety Flush Iterates All Characters:**
- Problem: `session_xp_safety_flush()` in `world/world_state.py` (lines 369-383) queries ALL player characters and calls `commit_session_xp()` on each online one. Each commit does multiple ndb reads, a dict copy, and a DB write.
- Files: `world/world_state.py`
- Cause: No way to know which characters have accumulated XP without checking all.
- Improvement path: Track characters with dirty accumulators in a module-level set. Only flush those.

**count_zone_actors Scans All Room Contents:**
- Problem: Called every 30 seconds per zone with a node. Searches all rooms tagged with zone_id, then iterates all contents of each room checking for player characters.
- Files: `world/node_helpers.py` (lines 55-76)
- Cause: No indexed lookup for "players in zone". Must scan room contents.
- Improvement path: Acceptable for small zones (<50 rooms). Will degrade with large zones or many zones with nodes active simultaneously.

**group_engine Uses search_object Per Member:**
- Problem: `_get_group_members()` calls `evennia.search_object("#" + str(char_id))` once per member, every time the member list is needed.
- Files: `world/group_engine.py` (lines 34-51)
- Cause: Group state stores member IDs (ints) in ndb, requiring lookup each access.
- Improvement path: Cache member object references in ndb directly. Validate freshness by checking `is_connected`.

**AreaBuilder._get_or_create_zone_object Scans All Zone Objects:**
- Problem: `evennia.search_tag("zone_object", category="object_type")` returns ALL zone objects, then filters linearly by zone_id.
- Files: `world/area_builder.py` (lines 148-162)
- Cause: No tag combining zone_id + object_type for direct lookup.
- Improvement path: Search by zone_id tag directly, then check for zone_object tag. Reverses the filter to narrow first.

## Missing Infrastructure

**No WorldEventLog Retention/Archival:**
- Problem: `WorldEventLog` model docstring specifies "90 days rolling, max 1000 entries" retention policy, but no cleanup mechanism exists.
- Files: `world/models.py` (lines 258-291)
- Blocks: Over time, the table will grow unbounded. When LLM quest generation reads these events, query performance will degrade.

**No Mob Spawn System:**
- Problem: `area_builder.py` `spawn()` and `named_mob()` register spawn definitions on rooms, and `mob_affix_roller.py` has `spawn_mob_with_pack()`, but there is no runtime spawn manager that reads definitions and creates mob instances.
- Files: `world/area_builder.py`, `world/mob_affix_roller.py`
- Blocks: No mobs appear in-game. Combat, loot, and disposition systems have no targets.

**No Combat System:**
- Problem: Zone scaling (`world/zone_scaling.py`), mob affixes (`world/mob_affixes.py`), and mob disposition (`world/mob_disposition.py`) all reference a combat system that does not exist. Affix hooks are marked "STUB -- called by combat system."
- Files: `world/zone_scaling.py`, `world/mob_affixes.py`, `world/mob_disposition.py`
- Blocks: Core gameplay loop (encounter -> fight -> loot -> progress) is not functional.

**No NPC System:**
- Problem: `area_builder.py` `npc()` stores NPC definitions on rooms, and `world_state.py` `get_character_context_packet()` builds a context dict for NPC interaction, but no NPC typeclass, dialogue system, or interaction handler exists.
- Files: `world/area_builder.py`, `world/world_state.py`
- Blocks: Quest givers, vendors, and faction representatives cannot function.

**No Quest System:**
- Problem: `area_builder.py` `quest()` stores quest definitions. Characters have `questline_choices` and `active_llm_quest_id` attributes. But no quest tracking, objective checking, or completion logic exists.
- Files: `world/area_builder.py`, `typeclasses/characters.py`
- Blocks: No structured objectives for players.

## Scaling Limits

**In-Memory Registries (zone_registry, named_mob_registry):**
- Current capacity: Module-level Python dicts rebuilt on every server restart.
- Limit: Memory-bound. With hundreds of zones and thousands of named mobs, startup time increases linearly as each area file is imported and `build()` called.
- Scaling path: Acceptable for foreseeable content volume. If startup becomes slow, add lazy loading or parallel area builds.

**SQLite in Development:**
- Current capacity: Single-writer, file-based database.
- Limit: Concurrent writes block. Banking F() atomic operations work but may serialize under load.
- Scaling path: Migrate to PostgreSQL for production (already noted in CLAUDE.md).

## Dependencies at Risk

**Evennia 6.0 Upgrade Path:**
- Risk: Evennia 6.0 may still be in development/early release. API changes between minor versions could break typeclass hooks, TickerHandler interface, or tag search behavior.
- Impact: All typeclasses, scripts, and world logic depend on Evennia's internal API.
- Migration plan: Pin Evennia version. Monitor changelog. The codebase correctly uses documented APIs (DefaultCharacter, DefaultScript, search_tag, create_object).

## Test Coverage Gaps

**No Tests for AreaBuilder:**
- What's not tested: `tests/test_area_builder.py` exists but should be verified for coverage of cross-zone exits, node initialization, named mob registration, and idempotent rebuilds.
- Files: `tests/test_area_builder.py`, `world/area_builder.py`
- Risk: Area spec loading could silently break on server restart.
- Priority: Medium

**No Tests for Node Script State Transitions:**
- What's not tested: `tests/test_node_system.py` exists but NodeScript's `_on_state_transition()`, Layer 1 activation/deactivation, and player teleportation between layers need thorough coverage.
- Files: `tests/test_node_system.py`, `world/scripts/node_script.py`
- Risk: Node state machine bugs could strand players in Layer 1 rooms.
- Priority: High

**No Tests for Session Lifecycle:**
- What's not tested: `Character.at_post_puppet()` creating SessionCommitScript, `at_pre_unpuppet()` flushing XP and leaving groups. No integration test for login->accumulate->logout->verify persistence.
- Files: `typeclasses/characters.py`
- Risk: XP loss on disconnect, orphaned group state.
- Priority: Medium

**No Tests for Exits:**
- What's not tested: LockedExit keyring checking, HiddenExit discovery persistence, NodeGravityExit penalty application.
- Files: `typeclasses/exits.py`
- Risk: Players could pass locked exits without keys, or hidden exits could be visible to all.
- Priority: Medium

**No Tests for zone_object.initialize_node():**
- What's not tested: Layer 1 room creation, NodeScript attachment, failure_start propagation.
- Files: `world/zone_object.py`
- Risk: Node initialization from area specs could create broken node configurations.
- Priority: Medium

---

*Concerns audit: 2026-03-24*
