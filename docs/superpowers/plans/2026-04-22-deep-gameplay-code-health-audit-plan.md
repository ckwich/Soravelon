# Soravelon Deep Gameplay and Code Health Audit Plan

**Date:** 2026-04-22
**Scope:** Full-repo audit plan for launch-readiness, gameplay quality, code health, and improvement opportunities.

## Goal
Run a deliberate, section-by-section audit of the entire Soravelon repo that answers four questions at the same time:

- What is broken, incomplete, misleading, or risky?
- What is technically correct but weak, thin, unbalanced, or hard to maintain?
- What is already strong and should be protected with better tests or clearer documentation?
- What should be improved before host/go-live even if it is not strictly a bug?

This is not just a defect hunt. The audit should also surface pacing problems, unclear UX, thin worldbuilding, stale docs, balancing issues, operational blind spots, and places where the codebase makes future iteration harder than it needs to be.

## Audit Principles

- Audit the game as a player experience, not only as Python modules.
- Treat gameplay richness, clarity, and fairness as first-class quality concerns.
- Separate launch blockers from important polish, and separate polish from future nice-to-haves.
- Prefer evidence from actual code paths, authored data, tests, and runtime behavior over old planning assumptions.
- Re-baseline stale planning and concern docs when repo reality has moved on.
- Capture both fixes and follow-on opportunities so the audit can drive multiple work passes.

## Current Scan Summary

The repo already contains substantial live game surface:

- `world/` holds the bulk of runtime engines, registries, area authoring, and system definitions.
- `commands/` exposes a broad custom command surface through `commands/default_cmdsets.py`.
- `typeclasses/` remains thin and delegates heavily into `world/` lifecycle and engine modules.
- `tests/` is large, but coverage symmetry is uneven across commands, helper modules, lifecycle modules, and some registries.
- `.planning/` and older codebase analysis docs contain useful architectural context, but some sections are stale enough that they cannot be treated as ground truth.

This means the audit should begin by re-establishing an accurate current-state baseline before it starts making judgments from older reports.

## Primary Deliverables

- one repo-wide audit report with findings grouped by system
- one launch blocker list
- one improvement opportunity list for non-blocking but meaningful upgrades
- one test-gap matrix showing which systems need stronger automated coverage
- one doc-drift list covering stale or misleading internal docs/help text
- one recommended execution order for remediation

## Audit Output Format

Every audit section should produce findings in four buckets:

- `Blocker`
- `High-value fix`
- `Improvement opportunity`
- `Already strong / protect with regression coverage`

Every finding should include:

- affected files or authored content surface
- player-facing impact
- technical/root-cause notes
- recommended fix direction
- verification needed after the fix

## Audit Sequence

### Wave 0. Reality Baseline and Audit Harness

**Purpose:** Establish current truth before deeper review.

Review:

- top-level repo structure and active runtime entry points
- current command registration
- current world/area inventory
- current tests, smoke scripts, and any content validators
- `.planning/` docs, milestone docs, and codebase analysis docs for drift

Questions:

- Which planning docs are still reliable and which are stale?
- Which systems are shipped in code but underrepresented in docs?
- Which systems are described in docs but still not truly launch-ready?
- What audit scripts/checklists can be reused for later waves?

Outputs:

- current-state inventory
- stale-doc shortlist
- audit checklist skeleton

### Wave 1. Boot, Session, Character Lifecycle, and Persistence Safety

**Purpose:** Make sure the game is safe to host and survive real player usage.

Review:

- login/logout/session lifecycle
- character creation hooks and default state
- movement lifecycle and recovery hooks
- death/respawn edge cases
- persistence boundaries between `db`, `ndb`, and Django models
- reload/restart behavior for combat, quests, statuses, vendors, groups, and cooldowns

Questions:

- Can players get stuck in bad states after disconnects, deaths, or reloads?
- Are there silent data-loss or stale-state hazards?
- Are state transitions consistent across engines?
- Which safety nets are missing tests?

Outputs:

- lifecycle risk list
- persistence/reload test plan
- candidate hardening fixes

### Wave 2. Commands, Help, Onboarding, and Player Legibility

**Purpose:** Ensure players can discover, understand, and use the game without confusion.

Review:

- command registration and aliases
- command parsing ergonomics and error messaging
- help topic completeness and accuracy
- onboarding flows for new characters
- discoverability of combat, questing, crafting, travel, vendors, groups, and social features

Questions:

- Does every important player action have a clear command and help path?
- Do help files match actual runtime behavior?
- Are beginner pain points caused by missing guidance rather than missing systems?
- Which commands are technically present but feel obscure, awkward, or under-taught?

Outputs:

- command/help gap list
- onboarding friction report
- recommendations for stronger first-session guidance

### Wave 3. Combat, Abilities, Status Effects, and Encounter Loop Quality

**Purpose:** Verify that moment-to-moment combat is truthful, fun, legible, and mechanically sound.

Review:

- combat engine and combat script flow
- ability registry truthfulness versus runtime behavior
- status effect handling and effect interactions
- mob combat behavior and encounter design hooks
- cooldown, resource, death, reflect, AoE, and group-interaction handling

Questions:

- Do abilities do what their text and fantasy imply?
- Are there balance cliffs, dead buttons, or over-centralizing abilities?
- Does combat communicate outcomes clearly enough to feel satisfying?
- Are elite/named encounters mechanically distinct or just stat bumps?

Outputs:

- combat truthfulness findings
- balance and fun-factor tuning targets
- encounter design improvement list
- missing combat regression tests

### Wave 4. Progression, Identity, and Build Expression

**Purpose:** Confirm that character identity feels distinct and rewarding over time.

Review:

- ancestries, domains, guilds, skills, talents, and loadouts
- progression pacing and unlock structure
- synergy between class/guild fantasy and actual buttons
- power curve from early to later content

Questions:

- Do character choices create meaningfully different play experiences?
- Are some tracks clearly richer or flatter than others?
- Are there progression dead zones where players stop receiving interesting incentives?
- Which progression features need clearer surfacing or stronger rewards?

Outputs:

- identity-expression audit
- progression pacing notes
- under-served track list

### Wave 5. Items, Loot, Equipment, Economy, Vendors, and Banking

**Purpose:** Make sure the reward loop is fair, coherent, and worth engaging with.

Review:

- equipment catalog progression
- drop tables and loot quality
- vendor stock curation and pricing
- banking and currency flow
- item effects, consumables, crafting inputs, and sell loops

Questions:

- Does itemization progress cleanly by tier and niche?
- Are players being pushed toward interesting choices or obvious best-in-slot lanes?
- Do vendors support play without collapsing exploration rewards?
- Is the economy generous enough to feel good but tight enough to stay meaningful?

Outputs:

- itemization balance report
- economy pressure-point list
- vendor/payout tuning opportunities

### Wave 6. Gathering, Crafting, Survival Loops, Travel, and Utility Systems

**Purpose:** Evaluate secondary gameplay loops as actual reasons to play, not just feature checkboxes.

Review:

- gathering pools and material definitions
- crafting definitions and recipe usefulness
- fishing, skinning, woodcutting, herbalism, mining, and node interactions
- travel systems including map/movement UX, courier/flight content, and route clarity

Questions:

- Are non-combat systems rewarding and understandable?
- Do crafted goods matter in real play?
- Are gathering loops varied enough across regions?
- Is travel convenient without erasing world scale?

Outputs:

- utility-loop richness report
- crafting/value-chain gaps
- travel friction and travel-content opportunities

### Wave 7. Dialogue, NPC Utility, Quests, and Narrative Reactivity

**Purpose:** Verify that authored interaction content has intent, coherence, and player payoff.

Review:

- dialogue engine and dialogue definitions
- NPC utility roles and interaction density
- quest logic, chains, routing, handoffs, and completion conditions
- delivery/investigate/talk/kill/collect objective quality
- lore distribution and contradiction handling

Questions:

- Does each quest either tell a story, teach the world, or push meaningful exploration?
- Are there NPCs who exist mechanically but feel narratively hollow?
- Are dialogue options doing real worldbuilding work?
- Do quest chains lead players into actual discovery rather than busywork?

Outputs:

- quest quality report
- NPC/dialogue enrichment opportunities
- narrative-cohesion notes

### Wave 8. World Content, Areas, Builder DSL Safety, and Regional Cohesion

**Purpose:** Evaluate the authored world as a connected place and protect builder compatibility.

Review:

- all authored area files
- zone layout readability and traversal clarity
- quest and service distribution by zone
- lore continuity across hubs and connected regions
- builder-safe AreaBuilder usage and round-trip safety
- cross-zone exit discipline and future expansion hooks

Questions:

- Does each zone feel distinct, navigable, and rich enough for its role?
- Are service, quest, and reward densities consistent with intended hub importance?
- Are there thin regions, contradictory history beats, or missed connective tissue?
- Are any authored patterns drifting away from builder-safe conventions?

Outputs:

- zone richness matrix
- continuity issues list
- builder-compatibility findings

### Wave 9. Social, Group, and Cooperative Play Readiness

**Purpose:** Make sure the game supports more than solo progression.

Review:

- group creation and group commands
- party loot and reward behavior
- social commands and RP support
- group-targeted abilities and shared travel/combat loops

Questions:

- Is grouped play meaningfully supported and communicated?
- Are group rewards, heals, and utility loops fair?
- Are there reasons to stay grouped beyond raw combat efficiency?

Outputs:

- co-op readiness findings
- social feature polish list

### Wave 10. Test Architecture, Coverage Gaps, and Verification Strategy

**Purpose:** Identify where the current safety net is strong, weak, misleading, or missing.

Review:

- system test distribution by runtime area
- content contract/layout tests
- smoke coverage
- engine-level versus command-level verification
- cases where tests are structural but not behavioral

Questions:

- Which areas have good coverage but weak assertions?
- Which core systems lack realistic behavior tests?
- Which command surfaces need direct tests instead of relying on engine coverage?
- Which content systems need stronger authored-contract tests?

Outputs:

- coverage-gap matrix
- recommended new test suites
- priority regression list

### Wave 11. Performance, Search Patterns, Admin Safety, and Host Operations

**Purpose:** Catch scalability and hosting issues before live players do.

Review:

- hot paths in combat, ticks, movement, searches, and registries
- object lookup patterns and repeated database access
- admin/debug commands and operational affordances
- deployment scripts, startup scripts, and recovery scripts
- monitoring/logging blind spots

Questions:

- Which paths are acceptable for development scale but risky for live concurrency?
- Are there repeated search or tick loops that need profiling?
- Do operators have enough tooling to diagnose issues during launch?
- What failure modes are recoverable versus opaque?

Outputs:

- performance-risk shortlist
- ops-readiness gaps
- profiling targets

### Wave 12. Final Synthesis and Go-Live Recommendation

**Purpose:** Turn the audit into an actionable execution order.

Deliver:

- one ranked blocker list
- one ranked high-value improvement list
- one launch confidence assessment
- one recommended remediation sequence
- one list of systems that are strong enough to freeze and protect

## Audit Heuristics to Use Throughout

- Prefer player-intent questions: “Why would someone use this?” and “What does this teach or reward?”
- Prefer truthfulness checks: “Does authored text match runtime behavior?”
- Prefer fairness checks: “Is this reward, price, cooldown, or power curve proportionate?”
- Prefer reusability checks: “Will this be easy to extend without regressions?”
- Prefer host-readiness checks: “What breaks under disconnects, reloads, or multiple real players?”

## Known Starting Risks Worth Prioritizing

- stale internal planning/codebase docs creating false confidence or false alarms
- uneven test symmetry across commands, helpers, and lifecycle modules
- likely command/help discoverability issues in systems that exist but are not heavily taught
- potential runtime-versus-authored drift in systems with large registries or rich content payloads
- launch-readiness gaps that only show up under stateful play rather than static import/shape testing

## Suggested Working Order

1. Wave 0 baseline and stale-doc correction
2. Waves 1 and 2 for player-state safety and player legibility
3. Waves 3 through 6 for core loops and reward structure
4. Waves 7 and 8 for authored world/content quality
5. Waves 9 through 11 for multiplayer, verification, and hosting risk
6. Wave 12 synthesis and launch recommendation

## Success Condition

At the end of this audit, we should have a trustworthy answer to three launch questions:

- Can Soravelon be hosted without obvious system integrity risks?
- Will new and returning players consistently understand what to do, why to do it, and how to grow?
- Which remaining issues are true blockers, and which are polish opportunities that can be scheduled after go-live?
