# Phase 4: Domain Fingerprints and Guild Engine - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Lock the mechanical identity of all 10 domains in a design document and build the guild/GTS computation engine that enforces it. This phase produces: (1) a consolidated design doc in .planning/ from the vault source material, (2) Python constant registries for guilds, subclasses, tier labels, and fingerprints, (3) the GTS computation engine, and (4) a CharacterGuild Django model.

**Out of scope:** Guild discovery trigger wiring, NPC questlines, ability authoring, CharacterAbility model, combat system. Those are Phase 5+.

</domain>

<decisions>
## Implementation Decisions

### Fingerprint Design Document
- **D-01:** All 10 domain fingerprints are authored by the user in vault docs (soravelon-fingerprints.md, soravelon-guilds.md, soravelon-abilities.md). Claude does not author creative content — Claude consolidates vault material into a .planning/ design doc.
- **D-02:** Design doc format is Markdown in `.planning/phases/04-domain-fingerprints-guild-engine/`. Downstream agents read this doc to understand domain identity before authoring abilities in Phase 5.
- **D-03:** The design doc extracts: 10 fingerprint verbs + resources, 90 subclass definitions (name/fantasy/hook), guild tier labels, GTS formula, and data model shapes.

### Guild Discovery Flow
- **D-04:** Guild discovery triggers via post-XP-commit hook. When domain XP commits and a score crosses 30 (Practiced threshold), check if `guild_id` is None. If so, schedule a guild approach event.
- **D-05:** The trigger check is **not wired in Phase 4**. Phase 4 builds the engine; discovery wiring is Phase 5+ content work. The engine exposes a `check_guild_eligibility(character)` function that returns which guild(s) a character qualifies for.

### GTS Tier Labels and Display
- **D-06:** Guild tier labels stored as Python constants in `world/guild_engine.py`. Dict keyed by guild_id → list of 4 label strings. Matches existing ALL_DOMAINS pattern.
- **D-07:** GTS (Guild Tier Score) is always computed on-the-fly: `(primary_domain_score × 0.66) + (secondary_domain_score × 0.33)`. No stored/cached GTS value. Function: `calculate_guild_tier_score(character) → float`.
- **D-08:** Tier thresholds: Tier 1 (0-20), Tier 2 (20-50), Tier 3 (50-85), Tier 4 (85+). Function: `get_guild_tier(character) → int` and `get_guild_tier_label(character) → str`.

### Data Model Boundaries
- **D-09:** GuildDefinition and SubclassDefinition are Python constant dicts in `world/guild_engine.py`, not Django models. Static data that never changes at runtime.
- **D-10:** GUILDS dict structure: `{guild_id: {name, primary_domain, hub_cities, hidden, motto, resource_type}}`.
- **D-11:** SUBCLASSES dict structure: `{subclass_id: {name, primary_domain, secondary_domain, guild_id, fantasy, hook}}`.
- **D-12:** GUILD_TIER_LABELS dict structure: `{guild_id: [tier1_label, tier2_label, tier3_label, tier4_label]}`.
- **D-13:** FINGERPRINTS dict structure: `{domain: {verb, resource, resource_type, description}}`.
- **D-14:** CharacterGuild is a new Django model in `world/models.py`. Fields: character (FK to ObjectDB), guild_id, primary_domain, secondary_domain, subclass_id, joined_at (DateTimeField), induction_complete (BooleanField). One row per character.
- **D-15:** Hybrid storage: CharacterGuild Django model is source of truth. `character.db.guild_id` and `character.db.subclass_id` remain as fast-read caches, updated when the model changes. Avoids DB join on every ability/GTS check.
- **D-16:** CharacterAbility model is **deferred to Phase 5**. Phase 4 only needs to compute which tier a character is at, not track unlocked abilities.

### Claude's Discretion
- Exact Python dict key naming and structure details beyond the shapes above
- Helper function signatures and internal organization of guild_engine.py
- Migration file structure
- Test organization and test case granularity

</decisions>

<specifics>
## Specific Ideas

- Vaelborn (Remnance) guild is hidden — `hidden: True` in GUILDS dict. Does not appear in any display until discovered. Tier 1 label is placeholder/empty.
- Guild of the Arcane has two traditions (Imperial/Western) — mechanically identical, culturally distinct. Single guild entry with a note, not two separate guilds.
- Remnance domain accumulates XP silently before discovery. When domain first appears on `domains` display, it shows existing score.
- Each guild has a unique resource type string matching the fingerprint resource (momentum, focus, balance, resonance, mana, influence, reagents, command, components, echoes).

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Domain Fingerprints (creative source — 10 verbs, resources, mechanical identity)
- `C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md` — All 10 domain fingerprints with verbs, resources, mechanical feel, cross-domain interactions, open questions

### Guild and Subclass System (90 subclasses, tier structure, data models)
- `C:\Obsidian\brain\Soravelon\soravelon-guilds.md` — Complete guild/domain/subclass design: 10 guilds, 90 subclass table, tier labels, GTS formula, proposed data model shapes, guild presence by hub city

### Ability and Combat System (GTS formula, domain resources, progression curve)
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` — Domain resources per guild, GTS computation, domain score growth curve (0-100 scale with 10-point descriptor bands), guild discovery flow, domain proficiency descriptors, backend level formula

### Existing Codebase
- `world/world_state.py` — ALL_DOMAINS tuple, domain score tracking (0-100), `calculate_backend_level()`, XP commit pipeline with diminishing returns
- `world/models.py` — Existing Django models (FactionStanding, ZoneAttunement, CharacterSkill, etc.) — CharacterGuild model will be added here
- `typeclasses/characters.py` — Character.at_object_creation() with existing `db.guild_id`, `db.subclass_id`, `db.primary_domain`, `db.secondary_domain` placeholders

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/world_state.py:ALL_DOMAINS` — Tuple of 10 domain strings, already used throughout codebase. Guild engine references this.
- `world/world_state.py:calculate_backend_level()` — Existing weighted domain score calculation. GTS follows the same pattern (read domain_scores dict, apply weights).
- `world/world_state.py:get_domain_score()` / `modify_domain_xp()` — Domain score read/write pipeline. GTS computation calls `get_domain_score()` for primary and secondary.
- `typeclasses/characters.py` — `db.guild_id`, `db.subclass_id`, `db.primary_domain`, `db.secondary_domain` already initialized to None. Phase 4 populates these as caches.

### Established Patterns
- **Python constant dicts** (e.g., `ALL_DOMAINS`, `ANCESTRY_FACTION_MODIFIERS` in mob_disposition.py) — guild/subclass registries follow this pattern
- **(bool, str) return tuples** — guild engine functions that can fail (e.g., `join_guild()`) use this pattern
- **Lazy record creation** — CharacterGuild record created only when character actually joins a guild
- **F() expressions** — Not needed for GTS (computed, not stored), but CharacterGuild model follows existing FK patterns
- **SaverDict copy pattern** — domain_scores is a db dict; any mutations follow copy-mutate-assign

### Integration Points
- `world/world_state.py` — GTS reads domain scores via existing getters. Post-XP-commit is where guild eligibility check stub lives (Phase 5 wiring).
- `world/models.py` — New CharacterGuild model alongside existing FactionStanding, ZoneAttunement, etc.
- `typeclasses/characters.py` — `at_object_creation()` already initializes guild-related db attributes. No changes needed there for Phase 4.
- `server/conf/at_server_startstop.py` — No new tickers needed for Phase 4. Guild engine is reactive (called on demand), not tick-driven.

</code_context>

<deferred>
## Deferred Ideas

- **Guild discovery NPC wiring** — Phase 5+. The trigger hook exists conceptually but is not wired in Phase 4.
- **Guild induction questlines** — Content work, Phase 5+. One questline per guild (10 total).
- **Secondary domain choice UI** — Narrative interaction during induction, Phase 5+.
- **CharacterAbility model + ability definitions** — Phase 5. Phase 4 computes tier, Phase 5 tracks unlocked abilities.
- **AbilityDefinition constant registry** — Phase 5. 360+ abilities need authoring.
- **`domains` command display** — Phase 5+ (command layer). Phase 4 provides the data functions.
- **`guild` command display** — Phase 5+ (command layer).
- **Vaelborn discovery trigger sequence** — Content design pass, well beyond Phase 4.
- **Resource system implementation** (Momentum, Focus, Balance, etc.) — Combat system phase, not Phase 4.

</deferred>

---

*Phase: 04-domain-fingerprints-guild-engine*
*Context gathered: 2026-03-25*
