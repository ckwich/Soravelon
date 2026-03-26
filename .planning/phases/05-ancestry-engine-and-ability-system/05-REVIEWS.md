---
phase: 5
reviewers: [gemini]
reviewed_at: 2026-03-26
plans_reviewed: [05-01-PLAN.md, 05-02-PLAN.md, 05-03-PLAN.md, 05-04-PLAN.md, 05-05-PLAN.md]
note: Codex CLI failed due to argument length limit on Windows. Claude skipped (current runtime).
---

# Cross-AI Plan Review — Phase 5

## Gemini Review

This review covers the implementation plans for **Phase 5a: Ancestry Engine and Ability System (Infrastructure)**. The plan successfully decomposes a complex architectural shift into five logical, testable waves while strictly adhering to Evennia 6.0 and Soravelon project conventions.

### Summary
The proposed plans provide a robust foundation for the character identity systems that define Soravelon's core value. By leveraging lazy-decay room state (ndb), a centralized ability registry (constant dict), and an effect-type dispatcher (`CmdUseAbility`), the architecture avoids the common MUD pitfalls of ticker-bloat and command-class proliferation. The decoupling of engine logic (Phase 5a) from creative content (Phase 5b) is a strategic move that ensures technical stability before the bulk authoring of 330+ abilities begins.

### Strengths
- **Efficiency via Lazy Decay:** The `room_state.py` implementation avoids global tickers by calculating state decay only when a room is read, which is ideal for performance in a MUD environment.
- **Architectural Scalability:** Using a single `CmdUseAbility` dispatcher with ~10 effect handlers instead of 330+ individual command classes significantly reduces maintenance overhead and memory footprint.
- **Strict build order:** The plans respect the dependency on Phase 4's GTS engine and properly wire into existing hooks like `commit_session_xp` and `at_death`.
- **Atomic Standing Updates:** Plan 01 correctly utilizes the existing `modify_standing` infrastructure with `F()` expressions, ensuring race-condition safety during ancestry initialization.
- **Comprehensive Testing:** Plan 05 provides a clear TDD roadmap with mocks for volatile state (`ndb`) and Django models, ensuring the framework is verified before content is added.

### Concerns
- **Missing Room Activity Update (LOW):** Plan 01 defines a `still` flag that triggers based on `room.ndb.last_activity`, but none of the plans explicitly set this timestamp. Without updating this value during player movement or combat, rooms may incorrectly accumulate the `still` flag or never transition to it.
- **Resource Initialization (MEDIUM):** `initialize_domain_resource` is defined in Plan 03 but only explicitly called "at encounter start". Utility or social abilities used outside of combat will fail if resources aren't also initialized at session start (`at_post_puppet`) for characters who already belong to a guild.
- **Migration Dependency (MEDIUM):** Plan 02 assumes migration `0004` is the latest. If the developer has local uncommitted migrations, the auto-generation of `0005` might cause conflicts. This is a common environment-sync risk.
- **Command Collision (LOW):** Evennia has a default `use` command (often for objects). While Plan 04 correctly handles this by registering in `CharacterCmdSet`, care must be taken to ensure the priority or parsing doesn't break standard Evennia interactions with items.

### Suggestions
- **Track Room Activity:** In `typeclasses/characters.py:at_after_move` (Plan 03), add a line to update the room's activity: `if self.location: self.location.ndb.last_activity = time.time()`. This ensures the `still` flag logic in `room_state.py` functions correctly.
- **Session Resource Sync:** In `typeclasses/characters.py:at_post_puppet`, call `initialize_domain_resource(self)` if `self.db.guild_id` is set. This ensures players can use non-combat abilities immediately upon login.
- **Prefix Matching Logic:** Ensure the prefix matching in `CmdUseAbility` (Plan 04) handles ambiguous names (e.g., "Fire" vs "Fireball") by returning a list of options if multiple matches exist, rather than just choosing the first one.
- **Migration Verification:** Before running Task 2 in Plan 02, verify the current migration state with `evennia migrate --list` to ensure `world:0004` is indeed the correct parent.

### Risk Assessment: LOW
The technical risk is low because the plans rely on proven patterns (constant registries, lazy imports, and ndb storage) already established in earlier phases. The separation of framework and content (5a/5b) further mitigates the risk of "creative stall" during the engineering wave. The primary risk remains the coordination of the 330 stub entries, which Plan 02 manages by limiting the initial wave to ~20 key validation stubs.

**Verdict:** The plans are ready for execution. Proceed with the suggested additions for `last_activity` and session resource initialization.

---

## Codex Review

Codex CLI was unable to process the review prompt — `Argument list too long` error on Windows. The prompt exceeds the shell argument limit when passed as a positional parameter, and Codex does not support piped stdin. Skipped.

---

## Consensus Summary

With only one external reviewer (Gemini), consensus is based on Gemini's feedback cross-referenced with the internal plan-checker's verification.

### Agreed Strengths
- Lazy-decay room state architecture (no global tickers)
- Single CmdUseAbility dispatcher (avoids command-class proliferation)
- Clean dependency chain honoring Phase 4 GTS engine
- Test coverage plan (Wave 3 dedicated to testing)

### Agreed Concerns
1. **Room activity timestamp (LOW):** `room.ndb.last_activity` is read by `still` flag logic but never explicitly written by any plan. Add write to `at_after_move`.
2. **Resource initialization at login (MEDIUM):** `initialize_domain_resource` should also be called in `at_post_puppet` for guild members, not only at encounter start.
3. **Migration numbering (MEDIUM):** Plan 02 assumes migration 0005 follows 0004. Verify migration state before generating.
4. **CmdUseAbility name collision (LOW):** Evennia may have a default `use` command. Verify priority/parsing doesn't conflict.

### Divergent Views
None — only one external reviewer.

### Actionable Items for --reviews Replan
If replanning with `--reviews`, address:
1. Add `self.location.ndb.last_activity = time.time()` to at_after_move in Plan 03
2. Add `initialize_domain_resource(self)` call in at_post_puppet in Plan 03 (conditional on guild_id)
3. Add migration state verification step in Plan 02 Task 2
4. Add ambiguous name handling note to CmdUseAbility in Plan 04
