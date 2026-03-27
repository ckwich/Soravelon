# Phase 5b: Ability Content Authoring - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Author all 330 ability definitions (150 domain pool + 180 subclass signatures) to replace the 14 stubs in `world/ability_registry.py`. This is collaborative creative work — Claude proposes based on vault lore and domain fingerprints, user reviews and revises in table format, one domain at a time. Approved domains are committed incrementally.

</domain>

<decisions>
## Implementation Decisions

### Authoring Workflow
- **D-01:** Full domain per session — 15 pool abilities + 18 subclass signatures = 33 abilities per domain. All 10 domains reviewed in one conversation session.
- **D-02:** Table format for review — Claude presents all abilities in a table (name, tier, effect_type, resource_cost, cooldown, charge_turns, description) plus signature table. User scans and marks changes.
- **D-03:** Commit per domain — after each domain is approved, commit its abilities to ability_registry.py. Incremental progress.
- **D-04:** Paired domain order — Combat+Tactics, Subterfuge+Diplomacy, Arcana+Resonance, Naturalism+Alchemy, Engineering+Remnance. Related domains reviewed together for cross-domain awareness.

### Balance Philosophy
- **D-05:** Damage/cost values derived from vault combat system formulas (combat_engine.py). Claude calculates appropriate base values from existing damage pipeline (weapon base + stat scaling + zone scaling).
- **D-06:** Resource costs match effect type, NOT tier. Damage abilities are cheap, CC abilities are moderate, compound triggers are expensive. Cost follows impact regardless of tier.
- **D-07:** Cooldowns are effect-correlated. Damage: 0-1 rounds (spammable), CC: 3-4 rounds, Buffs: 4-6 rounds. Cooldown follows impact type, not tier. A Tier 1 stun still has a long cooldown.
- **D-08:** Charged abilities (cast_time > 0) are common for caster domains (Arcana, Resonance, Remnance) and rare for physical domains (Combat, Subterfuge). Domain identity expressed through casting style.

### Domain Identity
- **D-09:** Strongly distinct playstyles per domain within MUD constraints. No spatial positioning (no "stances"). Differentiation via status effect patterns, buff/debuff stacking, resource manipulation, action economy, and effect type mix.
- **D-10:** Elements are primarily domain-linked (Arcana = fire/ice/lightning, Naturalism = poison/nature, Resonance = arcane) with occasional crossover when lore demands it.
- **D-11:** All domains are solo viable with group bonus. Support-oriented domains (Diplomacy, Alchemy, Engineering) have solo-viable abilities that ALSO work better in groups. No pure support classes.
- **D-12:** Most abilities write temporary room flags as part of their effect. This is universal, not limited to specific domains or tiers.

### Signature Ability Design
- **D-13:** Tier 3 signatures are enhanced domain blends — strong but within existing mechanics. Tier 4 signatures are mechanically unique — the defining ability that makes the subclass special.
- **D-14:** Tier 4 signature power is VARIED across all subclasses — some are big damage, some are unique sideways mechanics, some are situationally dominant. No single pattern for what "defining" means.
- **D-15:** Hybrid subclass signatures (e.g., Warcaller = Combat + Diplomacy) match the blend — one might rally allies (group buff) while the other demoralizes enemies (AoE debuff). Not forced into pure damage.

### Vault & Lore Integration
- **D-16:** Vault docs (soravelon-guilds.md, soravelon-abilities.md) are the canonical source for ability flavor, guild fingerprints, and domain descriptions. User will add additional context during each domain review session.
- **D-17:** Each domain's fingerprint verb (Break, Exploit, Shape, Channel, Weave, Persuade, Distill, Command, Construct, Remember) should dictate its mechanical identity and ability naming conventions.

### Data Model (Carried from Phase 5 CONTEXT)
- **D-18:** 16 fields per ability: id, name, domain, tier, resource_cost, resource_type, cooldown, charge_turns, effect_type, scaling_primary, scaling_secondary, application_chance, description, room_flag_written, attuned_variants, subclass_id.
- **D-19:** Signature abilities have subclass_id set (non-null). Domain pool abilities have subclass_id = None.
- **D-20:** DOMAIN_ABILITIES and SUBCLASS_SIGNATURES derived lookups auto-built from ABILITIES dict at module level.

### Claude's Discretion
- Exact damage/cost/cooldown values within the vault-derived framework
- Ability names and descriptions (subject to user review)
- Room flag names for each ability (e.g., "scorched", "frozen", "bloodied")
- Attuned variant design (which abilities get variants, what flags trigger them)
- Scaling stat assignments per ability (primary + optional secondary)
- Application chance values for debuffs/status effects

</decisions>

<specifics>
## Specific Ideas

- "Positioning without custom commands is hard in a MUD" — use status effects, buff/debuff stacking, resource manipulation, and action economy to differentiate domains
- "Cost matches effect type" — a Tier 1 stun costs more than a Tier 1 damage ability
- "Common charges for casters" — Arcana/Resonance/Remnance have many charged abilities; Combat/Subterfuge are mostly instant
- Signature Tier 4 should feel like "this is why I chose this subclass" — the moment that justifies the 85 GTS investment

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before proposing abilities.**

### Ability Framework
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` — Full ability structure, data model, tier distribution, resource types, effect types
- `C:\Obsidian\brain\Soravelon\soravelon-guilds.md` — 10 guilds with fingerprint verbs, hooks, subclass definitions, GTS tiers

### Combat System (for damage/cost calibration)
- `world/combat_engine.py` — Damage resolution pipeline, crit system, zone scaling
- `world/status_effects.py` — 12 status effects, compound matrix, stackable ceilings
- `world/base_attributes.py` — 7 stats, stat-to-domain mapping

### Existing Stubs
- `world/ability_registry.py` — Current 14 stub abilities with correct field shape

### Domain Resources (from vault)
- Combat → Momentum (builds on hits, decays between encounters)
- Subterfuge → Focus (accumulates on successful debuffs, decays on miss)
- Naturalism → Balance (steady regeneration, capped, disrupted by damage)
- Resonance → Echoes (builds on node interaction, fades over time)
- Arcana → Mana (classic pool, slow regen, meditation to restore)
- Diplomacy → Influence (builds through successful persuasion, persists)
- Alchemy → Reagents (pre-crafted consumable stock, not regenerating)
- Tactics → Command (builds on party actions, decays when solo)
- Engineering → Components (pre-built devices, not regenerating)
- Remnance → Echoes (builds on Remnance-specific interactions)

</canonical_refs>

<code_context>
## Existing Code Insights

### Current Registry State
- `world/ability_registry.py` has 14 stub entries with `[STUB - Phase 5b]` in descriptions
- ABILITIES dict structure is correct — Phase 5b replaces stubs with real entries
- DOMAIN_ABILITIES and SUBCLASS_SIGNATURES derived lookups will auto-rebuild
- EFFECT_TYPES tuple defines valid effect types: damage, dot, buff, debuff, utility, social, tactical, compound_trigger, heal, status

### Integration Points (Already Wired)
- `world/ability_engine.py` dispatches by effect_type — 10 handlers exist and are wired to combat_engine/status_effects
- `world/combat_ai.py` selects mob abilities by weight — mob abilities are separate (authored per mob template, not from registry)
- `commands/cmd_abilities.py` CmdAbilities and CmdUseAbility read from ABILITIES dict
- `typeclasses/characters.py` ndb.ability_cooldowns tracks per-ability state

### What Changes in This Phase
- ABILITIES dict grows from 14 entries to 330
- No new code modules needed — just data
- No migrations needed — ability data is in Python constants, not Django models

</code_context>

<deferred>
## Deferred Ideas

- Attuned variant content (which abilities get variants for which room flags) — can be authored alongside or after base abilities
- Ability balance tuning based on playtesting — Phase 7+ when content exists to test against
- PvP ability adjustments — post-launch
- Ability visual effects for desktop client — Milestone 2+

</deferred>

---

*Phase: 5b-ability-content-authoring*
*Context gathered: 2026-03-27*
