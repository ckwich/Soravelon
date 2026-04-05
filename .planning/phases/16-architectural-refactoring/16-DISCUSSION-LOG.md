# Phase 16: Architectural Refactoring - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-05
**Phase:** 16-architectural-refactoring
**Areas discussed:** Typeclass god methods, Command logic extraction, Duplicate logic consolidation, Naming consistency, SaverDict audit, Return type enforcement, Import hygiene

---

## Typeclass God Methods

| Option | Description | Selected |
|--------|-------------|----------|
| Lifecycle orchestrators | Create world/lifecycle.py with on_login(), on_logout(), on_move(), on_mob_death() that typeclasses call as single dispatch points | ✓ |
| Per-system hooks | Each world module registers its own hook. Typeclass calls each one explicitly | |
| You decide | Claude picks the best approach | |

**User's choice:** Lifecycle orchestrators
**Notes:** None

### Follow-up: File structure

| Option | Description | Selected |
|--------|-------------|----------|
| Single world/lifecycle.py | All lifecycle functions in one file | |
| Split by domain | session_lifecycle.py, movement_lifecycle.py, death_lifecycle.py | ✓ |

**User's choice:** Split by domain

---

## Command Logic Extraction

| Option | Description | Selected |
|--------|-------------|----------|
| Extend existing engines | Add catch_fish() to gathering_engine.py, expand gather_from_node() | ✓ |
| New dedicated engines | Create world/fishing_engine.py separately | |
| You decide | Claude picks based on code size | |

**User's choice:** Extend existing engines

---

## Duplicate Logic Consolidation

| Option | Description | Selected |
|--------|-------------|----------|
| Extract clear duplicates only | Only extract identical computation in 2+ places | ✓ |
| Full DRY pass | Extract all repeated patterns including similar ones | |
| You decide | Claude judges each case | |

**User's choice:** Extract clear duplicates only

---

## Naming Consistency

| Option | Description | Selected |
|--------|-------------|----------|
| Standardize on mob_id | Shorter, matches *_id patterns | |
| Standardize on mob_template | More descriptive | |
| Keep both, document boundary | Different concepts, just clarify | |
| Rename to mob_template_key/mob_instance_id | Make distinction explicit in names | ✓ |

**User's choice:** Rename to mob_template_key/mob_instance_id (via Other)
**Notes:** User is building a companion game editor app that reads/writes mob templates. Wants game data in a format easily accessible to companion apps. "Serializable game data format" noted as deferred idea for future phase.

---

## SaverDict Audit

**Mechanical sweep — no design decisions needed.** Included as phase scope with clear rule: every db.* dict/set/list mutation must use copy-mutate-assign pattern.

## Return Type Enforcement

**Mechanical sweep — no design decisions needed.** Every public function in world/*.py returns (bool, str). Private functions exempt.

## Import Hygiene

**Mechanical sweep — no design decisions needed.** Lazy imports for heavy modules, remove unused, verify no circular paths.

---

## Claude's Discretion

- Exact helper function names and signatures for extracted duplicates
- Whether to inline small orchestrator calls vs function references
- Import ordering within files

## Deferred Ideas

- Serializable game data format for companion apps (major data architecture change)
- Equipment query caching (performance optimization, not code quality)
