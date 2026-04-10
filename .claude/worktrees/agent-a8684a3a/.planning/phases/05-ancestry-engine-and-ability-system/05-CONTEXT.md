# Phase 5: Ancestry Engine and Ability System - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 is SPLIT into two sub-phases:

**Phase 5a (this context):** Build the ancestry engine, ability framework, room state system, CmdUseAbility dispatcher, guild discovery wiring, domains command, and all structural infrastructure. No individual ability definitions yet — that's 5b.

**Phase 5b (separate context):** Author all 330 ability definitions (150 domain + 180 subclass signatures) in a collaborative guild-by-guild review loop. 5b depends on 5a's framework being complete.

**Requirements covered by 5a:**
- ANC-01 through ANC-05 (4 ancestries with mechanical traits, mob disposition integration)
- ABL-01 (global data-driven ability registry — structure, not content)
- ABL-02 (CmdUseAbility dispatcher — handles all abilities through one command)
- ABL-03 (ability tier gating at GTS thresholds 0/20/50/85)
- ABL-05 (ability cooldowns tracked per-encounter on character.ndb)
- ABL-06 (subclass engine derives identity from primary + secondary domain pair)

**Requirements deferred to 5b:**
- ABL-04 (all 90 subclasses have mechanically distinct ability sets — needs ability content)

</domain>

<decisions>
## Implementation Decisions

### Phase Split Strategy
- **D-01:** Phase 5 splits into 5a (engine + framework) and 5b (ability content authoring).
- **D-02:** Phase 5b uses collaborative in-conversation review, domain by domain. Claude proposes abilities for one domain (15 abilities + 9 subclass signatures), user reviews/revises, repeat for all 10 domains.

### Ability Structure (Corrected Design)
- **D-03:** 15 abilities per domain (3-4 per tier across 4 tiers) × 10 domains = 150 domain abilities. All accessible by primary guild members.
- **D-04:** 2 signature abilities per subclass × 90 subclasses = 180 signature abilities. Unique to specific subclass, not in any domain pool.
- **D-05:** Per character at max GTS: 15 primary domain + 4 secondary picks (1 of 3 per tier, player's choice) + 2 signatures = 21 known abilities. Active loadout: 8 selected from known pool.
- **D-06:** Signature 1 unlocks at Tier 3 (GTS 50+). Signature 2 unlocks at Tier 4 (GTS 85+).
- **D-07:** Secondary domain ability pick is permanent per tier — player chooses 1 of 3 from secondary domain's tier pool. Two characters with same subclass can have different secondary picks.

### Ability Data Model
- **D-08:** AbilityDefinition as Python constants in `world/ability_registry.py`. ABILITIES dict keyed by ability_id. Same pattern as GUILDS/SUBCLASSES in guild_engine.py.
- **D-09:** Full field shape from vault: id, name, domain, tier, resource_cost, resource_type, cooldown, charge_turns, effect_type, scaling_primary, scaling_secondary, application_chance, description, room_flag_written, attuned_variants. Combat-specific values stubbed but not wired until Phase 6.
- **D-10:** CmdUseAbility uses effect-type dispatch. ~10 handlers (damage, dot, buff, debuff, utility, social, tactical, compound_trigger, etc.) cover all 330 abilities. No per-ability callables.
- **D-11:** CharacterAbility Django model in world/models.py. Fields: character FK, ability_id, unlocked_at (timestamp), times_used. Relational data per project convention.

### Cooldown and Resource Tracking
- **D-12:** Ability cooldowns on character.ndb.ability_cooldowns dict. Remaining rounds per ability. Cleared on encounter end. Per-encounter, volatile.
- **D-13:** Domain resource tracking: character.ndb.domain_resource = {type, current, max}. Resource type set from guild fingerprint. Build/decay/spend functions exist in 5a but only called from ability stubs. Combat system (Phase 6) wires real effects.

### Ancestry Engine
- **D-14:** New `world/ancestry_engine.py` module. ANCESTRY_TRAITS dict with trait data for Human, Kau'roran, Veth, Selvar. Starting standing application functions. Starting ability tracking.
- **D-15:** Ancestry starting abilities tracked as character.ndb.ancestry_ability_used (boolean, reset at encounter end). Each ancestry has exactly one starting ability, all once-per-combat.
- **D-16:** Ancestry selection: at_object_creation sets db.ancestry to None. CmdSetAncestry command lets player choose. Starting standings applied via modify_standing() on selection. Ancestry traits apply immediately.

### Guild Discovery Wiring
- **D-17:** Post-XP-commit hook in commit_session_xp(). After domain scores update, call check_guild_eligibility(). If eligible and no guild, send a guild-flavored in-game recruitment message to the character.
- **D-18:** Guild induction: lightweight CmdJoinGuild stub in 5a. Shows NPC dialogue as text prompts (choose from menu). Recommends highest-scoring secondary but offers all qualified options. Replaced by proper NPC interaction in Phase 6.

### Ability Unlock Flow
- **D-19:** When GTS crosses a tier threshold, player receives a guild-flavored notification message. Must visit guild hall and run a claim command to unlock. Manual claim, not auto-add.
- **D-20:** Secondary domain ability selection happens at guild hall claim — player sees 3 options from secondary domain's tier pool, picks 1. Permanent choice.

### Room State System
- **D-21:** Build `world/room_state.py` in Phase 5a. Module implements FLAG_VOCABULARY, lazy decay on ndb, get_room_flags(), add_room_flag(), remove_room_flag(), get_dominant_flag(), SENSE_PRIORITY.
- **D-22:** Resonance Sense passive: after each move and end-of-combat-round, Resonance-primary characters see a one-line atmospheric descriptor from SENSE_DISPLAY. Information only, not a buff.
- **D-23:** Attuned ability variants: ability definitions include attuned_variants dict keyed by room flag. When player uses ability and matching flag is active, present choice (standard vs attuned at extra resource cost). Stub as y/n prompt; auto_attune config deferred.
- **D-24:** Add `add_room_flag` to action vocabulary for builder-authored triggers. Flag writers for mob death (blood_soaked, fading_life, power_vacuum) wire into existing at_death in Phase 5a.

### Commands
- **D-25:** Build `domains` command in Phase 5a. Shows domain scores as descriptors (Practiced, Skilled, etc), guild membership, GTS tier label, subclass name. Remnance hidden until character.db.remnance_discovered flag is True. When discovered, shows existing score retroactively.
- **D-26:** Build `abilities` command stub showing known abilities and active loadout.

### Maintenance Updates
- **D-27:** Update guild_engine.py SUBCLASSES dict — Ironwright hook changed to "Builds weapons mid-battle — improvised, brutal, adaptive; no companion — Engineering knowledge applied to self and weapons".

### Claude's Discretion
- Exact text of guild recruitment messages per guild
- CmdJoinGuild text prompt flow details
- Ability registry Python dict field naming (within the vault-defined shape)
- Test organization and granularity
- Room state integration with existing at_death (mob death flag writers)
- Domain proficiency descriptor display formatting in `domains` command

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Ancestry Design (4 ancestries, traits, starting abilities, standings)
- `C:\Obsidian\brain\Soravelon\soravelon-ancestries.md` — Full ancestry design: Human, Kau'roran, Veth, Selvar traits, starting abilities, domain interactions, cultural knowledge, starting standing, ANCESTRY_TRAITS data model

### Ability and Combat System (ability structure, resources, GTS, progression)
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` — Corrected ability structure (150 domain + 180 signature = 330), domain resources per guild, status effects, ability data model fields, domain progression system, guild discovery flow

### Guild and Subclass System (90 subclasses, tier labels)
- `C:\Obsidian\brain\Soravelon\soravelon-guilds.md` — 10 guilds, 90 subclass table with hooks, ability tier structure, primary domain core abilities, guild tier labels, Ironwright no-companion update

### Domain Fingerprints (10 verbs, resources, mechanical identity)
- `C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md` — 10 fingerprint verbs and resources, Engineering secondary no-companion rule, companion chassis by subclass

### Room State System (flags, Sense, attuned variants)
- `C:\Obsidian\brain\Soravelon\soravelon-room-state.md` — FLAG_VOCABULARY (20 flags), Sense mechanic, attuned ability variants, lazy decay design, non-Resonance domain interactions, flag writers by system, AreaBuilder integration

### Existing Codebase
- `world/guild_engine.py` — GUILDS, SUBCLASSES, FINGERPRINTS, GUILD_TIER_LABELS, GTS computation, join_guild(), check_guild_eligibility()
- `world/world_state.py` — ALL_DOMAINS, domain scores, commit_session_xp() (hook point for guild discovery)
- `world/mob_disposition.py` — ANCESTRY_FACTION_MODIFIERS, get_ancestry_modifier() (already integrates ancestry)
- `world/models.py` — CharacterGuild model (Phase 4), add CharacterAbility model here
- `typeclasses/characters.py` — db.ancestry initialized to None, db.guild_id/subclass_id cached
- `typeclasses/mobs.py` — at_death() (hook point for room flag writers)
- `world/action_vocabulary.py` — add _action_add_room_flag handler

### Phase 4 Design Doc
- `.planning/phases/04-domain-fingerprints-guild-engine/DOMAIN_FINGERPRINTS.md` — Consolidated fingerprints, guild/subclass registry, tier labels

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/guild_engine.py` (1692 lines) — All constant registries, GTS computation, guild mutation functions. Phase 5a adds to this.
- `world/world_state.py:commit_session_xp()` — Natural hook point for guild discovery check. Called at logout, every 10m, and via safety ticker.
- `world/mob_disposition.py:get_ancestry_modifier()` — Already reads character.db.ancestry and applies faction modifiers. Ancestry engine just needs to SET the ancestry.
- `world/world_state.py:modify_standing()` — Used by ancestry engine to apply starting standings on ancestry selection.
- `world/action_vocabulary.py` — Add _action_add_room_flag handler following existing pattern.

### Established Patterns
- Python constant dicts for static data (GUILDS, SUBCLASSES, FINGERPRINTS → ABILITIES, ANCESTRY_TRAITS)
- (bool, str) return tuples for functions that can fail
- character.ndb for volatile per-session/per-encounter state
- Django models for relational data (CharacterGuild → CharacterAbility)
- Lazy import inside functions to avoid circular dependencies
- Tag-based lookups (mob_type, zone_id)

### Integration Points
- `world/world_state.py:commit_session_xp()` → add guild eligibility check after domain scores update
- `typeclasses/characters.py:at_object_creation()` → ancestry already None, add ndb inits for domain_resource and ability_cooldowns
- `typeclasses/mobs.py:at_death()` → add room flag writers (blood_soaked, fading_life, power_vacuum)
- `world/action_vocabulary.py` → add _action_add_room_flag handler
- `commands/` → new CmdUseAbility, CmdSetAncestry, CmdJoinGuild, CmdDomains, CmdAbilities

</code_context>

<specifics>
## Specific Ideas

- Room state uses ndb (ephemeral) with lazy decay — no global ticker scanning rooms. Decay happens on read.
- The `still` flag auto-applies when no other flags present for 20 rounds — passive accumulation handled in get_dominant_flag().
- Sense display is one-line atmospheric text, not mechanical information. Players don't see flag names.
- Attuned variants present a y/n prompt during ability use. `config auto_attune` deferred to later.
- Guild recruitment messages should feel like world events, not system notifications. Each guild has a distinct voice.
- Domain proficiency descriptors (Unaware, Novice, Dabbler, Practiced, Skilled, Proficient, Expert, Seasoned, Masterful, Virtuosic, Transcendent) are 10-point bands on the 0-100 scale.
- Remnance is hidden until character.db.remnance_discovered = True. Domains command shows 9 domains until then.

</specifics>

<deferred>
## Deferred Ideas

- **ABL-04 (360 ability definitions)** → Phase 5b, collaborative guild-by-guild authoring
- **Combat system integration** → Phase 6. Ability effects are stubbed in 5a, wired in 6.
- **NPC template system for guild induction** → Phase 6. 5a uses lightweight command stubs.
- **auto_attune configuration** → later command system pass
- **Sense display for non-Resonance** → future design (Remnance variant TBD)
- **Full attuned variant UI polish** → Phase 6 combat polish
- **Guild induction questlines** → content phase (10 questlines)
- **Vaelborn discovery trigger sequence** → content design pass
- **Companion system integration** → Milestone 2
- **Node script room flag writers** → Phase 5a wires mob death flags; node pulse flags wire in Phase 6

</deferred>

---

*Phase: 05-ancestry-engine-and-ability-system*
*Context gathered: 2026-03-26*
