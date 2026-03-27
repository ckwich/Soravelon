# Phase 5c: Ability Polish & Resource Engine - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Two workstreams: (1) Fix ~18 redundant/obsolete abilities identified in the 5b review audit so every ability is attractive in an 8-slot loadout. (2) Implement all 10 domain resource systems in ability_engine.py so each domain has mechanically distinct combat identity.

</domain>

<decisions>
## Implementation Decisions

### Part 1: Ability Redundancy Fixes

- **D-01:** ~18 abilities across 8 domains need redesign. Each must gain a unique mechanic that makes it attractive alongside its tier-mates. No ability should be strictly worse than another at the same or higher tier.
- **D-02:** Fix approach: redesign the weaker ability with a new secondary effect, condition, or unique mechanic — don't just bump damage numbers. The goal is loadout CHOICES, not power inflation.

**Specific redundancies to fix (from audit):**

Combat:
- `press_the_line` (T1, 30 dmg) — identical to crushing_advance but weaker. Needs unique identity.

Subterfuge:
- `death_of_a_thousand_reads` (T4, 180 dmg) — dominated by phantom_execution (220 dmg + crit). Needs differentiation.

Arcana:
- `arcane_bolt` (T1, 35 dmg) — dominated by spark_jolt (40 dmg + shocked). Needs unique value.
- `frost_shard` (T1, 30 dmg) — same problem, dominated by spark_jolt.
- `meteor_strike` (T4, 200 dmg) — dominated by arcane_cataclysm (250 dmg + multi-element).
- `absolute_zero` (T4, 180 dmg) — same problem.

Resonance:
- `dissonance_wave` (T2, 60 cost) — situational, loses to harmonic_blast for damage loadouts.
- `echo_mend` (T2, 60 cost) — same issue, niche heal.
- `harmonic_shield` (T3, 80 cost) — defensive spender rarely chosen over offense.

Naturalism:
- `bramble_burst` (T2) — superseded by venombloom (T3) for poison.
- `thorn_lash` (T1) — superseded by higher-tier feral damage.
- Calm abilities need more variety (only 1-2 per tier vs 3-4 feral).

Alchemy:
- `venom_coat` (T1) — superseded by concentrated_toxin (T2).
- `smoke_screen` (T1) — superseded by flashpowder (T2).

Engineering:
- `enhanced_fuel_injection` (T2) — superseded by overcharge_protocol (T3).

Remnance:
- `fragment_pulse` (T1) — weaker version of memory_strike.
- `forgotten_impact` (T2) — weaker version of excavate_truth.
- `pre_curse_strike` (T3) — weaker version of void_excavation.
- Weaken debuff at T1/T2/T4 with no differentiation between tiers.

### Part 2: Resource Engine Implementation

- **D-03:** All 10 resource systems implemented as handlers in ability_engine.py. Each resource has distinct build/spend/decay mechanics.

**Resource systems to implement:**

- **D-04: Momentum (Combat)** — Builds on hits landed AND damage taken. Decays between encounters only. Pool-style resource. Vault spec is canonical.
- **D-05: Focus (Subterfuge)** — Combo point system, cap 5. Builders (is_builder: True) generate 1 on hit. Miss = reset to 0. Skip Subterfuge turn = reset to 0. Spenders cost 1-5. consumes_all_focus abilities scale with Focus spent. Persists between turns, not encounters.
- **D-06: Balance (Naturalism)** — Pendulum spectrum 0-100 (0=Feral, 100=Calm, 50=start). NOT a pool. Calm abilities push toward Feral (negative shift), Feral abilities push toward Calm (positive shift). Damage scales with Feral position, heals scale with Calm position. resource_cost always 0.
- **D-07: Resonance** — Builder/spender. Builders (cost 0) generate resonance. Spenders at thresholds 60/80/100. Decay: -10 per round during combat. No decay between encounters. Cap 100.
- **D-08: Mana (Arcana)** — Traditional pool. Persists across encounters. Regenerates slowly between encounters (meditation). Largest pool size.
- **D-09: Influence (Diplomacy)** — Reputation-fueled pool. Starting pool each encounter = f(Reputation dimension score). Does NOT regenerate in-combat. Rationing like mana but encounter-scoped.
- **D-10: Reagents (Alchemy)** — Finite consumable stock. Does NOT regenerate in combat or between encounters. Replenished only through gathering/purchasing. Running out mid-fight is intentional.
- **D-11: Command (Tactics)** — Builds on ally actions in same round. Solo rate: builds at 50% rate without allies. Decays between encounters.
- **D-12: Components (Engineering)** — Finite consumable stock like Reagents. Pre-crafted. Does NOT regenerate.
- **D-13: Echoes (Remnance)** — Builds from abilities used in combat. Investigation bonus: +15 per lore fragment, +10 per ancient site, persists 3 encounters, stacks to 40 starting echoes. Decays between encounters.

### Future Phase (deferred from 5c):
- **Typed resource variants** for Engineering (component types) and Alchemy (reagent types) — the gathering/inventory system and ability variant resolution are deferred. 5c only adds the variant data fields to abilities if practical.

### Claude's Discretion
- Exact redesign of each redundant ability (within the constraint: must be loadout-worthy)
- Resource pool sizes and formulas (within vault-defined parameters)
- Implementation pattern for resource handlers (function dispatch, class hierarchy, or simple if/elif)
- Test coverage granularity for resource systems

</decisions>

<canonical_refs>
## Canonical References

### Vault Resource Specs
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Domain Resources — All 10 resource descriptions with build/decay/feel
- `C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md` — Domain fingerprint verbs that drive ability identity

### Existing Code
- `world/ability_engine.py` — Current resource functions: build_domain_resource, spend_domain_resource, get_domain_resource, initialize_domain_resource. These need to become resource-type-aware.
- `world/ability_registry.py` — 330 abilities with effect_params including is_builder, consumes_all_focus, balance_shift, balance_type, resonance_generated
- `world/status_effects.py` — Status effects including shocked + Discharge compound
- `world/combat_script.py` — Round lifecycle hooks where resource decay/build triggers

### Audit Results
- Redundancy audit performed in conversation (2026-03-27): 18 dead abilities across 8 domains identified with specific IDs and reasons

</canonical_refs>

<code_context>
## Existing Code Insights

### Current Resource System (ability_engine.py)
- `initialize_domain_resource(character)` — sets ndb.domain_resource = {type, current, max}
- `build_domain_resource(character, amount)` — adds to current
- `spend_domain_resource(character, amount)` — subtracts from current
- `get_domain_resource(character)` — returns current value
- These are GENERIC — they don't know about Focus combo points, Balance pendulum, or builder/spender patterns. They need to become resource-type-aware.

### Integration Points
- `combat_script.py:end_round()` — where per-round decay should happen (Resonance -10/round)
- `combat_script.py:end_combat()` — where encounter-end resets happen
- `ability_engine.py:use_ability()` — where resource spend/build logic lives
- `combat_engine.py:resolve_basic_attack()` — where Momentum build-on-hit should trigger
- `world_state.py:get_dimension_score()` — where Influence reads Reputation for pool calculation

</code_context>

<deferred>
## Deferred Ideas

- Typed resource gathering/inventory for Engineering components and Alchemy reagents — requires new item types, gathering commands, salvage system. Separate phase.
- Resource UI display in combat prompt — needs client/OOB integration
- Balance tuning from playtesting — Phase 7+ when content exists

</deferred>

---

*Phase: 05c-ability-polish-and-resource-engine*
*Context gathered: 2026-03-27*
