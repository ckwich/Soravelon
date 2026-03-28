---
phase: 05c-ability-polish-and-resource-engine
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - world/ability_registry.py
autonomous: true
requirements:
  - ABL-04
must_haves:
  truths:
    - "No ability is strictly worse than another ability at the same or higher tier within its domain"
    - "Every ability brings something unique to an 8-slot loadout"
    - "Fixes use new mechanics (secondary effects, conditions, unique behaviors) not just number bumps"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "18 redesigned abilities with unique mechanics"
      contains: "press_the_line"
  key_links: []
---

<objective>
Fix ~18 redundant/obsolete abilities across 8 domains so every ability is loadout-worthy.

Purpose: Per D-01/D-02, no ability should be strictly worse than another at the same or higher tier. Each fix adds a unique mechanic (secondary effect, condition, or behavior) rather than bumping damage numbers.
Output: Updated ability definitions in ability_registry.py
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/05c-ability-polish-and-resource-engine/5c-CONTEXT.md
@.planning/phases/05c-ability-polish-and-resource-engine/05C-RESEARCH.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Redesign ~18 redundant abilities with unique mechanics</name>
  <files>world/ability_registry.py</files>
  <read_first>
    - world/ability_registry.py (full file -- contains all 330 ability definitions, understand tier-mates before redesigning)
    - .planning/phases/05c-ability-polish-and-resource-engine/5c-CONTEXT.md (specific redundancies listed under D-01/D-02)
    - .planning/phases/05c-ability-polish-and-resource-engine/05C-RESEARCH.md (redesign pattern guidance)
    - world/status_effects.py (available status effect types for secondary effects)
  </read_first>
  <action>
Redesign each of the following ~18 abilities in the ABILITIES dict. For each ability, change effect_params and/or effect_type/description to give it a unique loadout role. Do NOT just increase damage_base numbers. Per D-02, add secondary effects, conditions, or unique mechanics.

**Combat domain:**
- `press_the_line` (T1, damage, 30 dmg) -- currently weaker crushing_advance clone. Redesign: change effect_type to "debuff", add effect_params with debuff_type "slow", duration 2, magnitude 0.8. New description: a quick thrust that hobbles the target's footwork. Now it is the only T1 Combat debuff, making it attractive for control-focused loadouts.

**Subterfuge domain:**
- `death_of_a_thousand_reads` (T4, damage, 180 dmg) -- dominated by phantom_execution (220+crit). Redesign: add effect_params `"is_multi_hit": True, "hit_count": 5, "damage_per_hit": 40` (total 200 in ideal case). New description: five rapid precision strikes exploiting read openings. Multi-hit enables per-hit proc triggers (future) and differentiates from single-hit phantom_execution.

**Arcana domain:**
- `arcane_bolt` (T1, damage, 35 dmg) -- dominated by spark_jolt. Redesign: add effect_params `"piercing": True` (ignores resistance). Lower damage_base to 28. New description: a bolt of pure arcane force that bypasses all elemental defenses. Unique niche: anti-resistance.
- `frost_shard` (T1, damage, 30 dmg) -- dominated by spark_jolt. Redesign: change effect_type to "status", add effect_params `"status_effect": "slow", "duration": 2, "magnitude": 0.7, "damage_base": 20`. New description: a shard of crystallized cold that chills and slows. Unique niche: T1 crowd control.
- `meteor_strike` (T4, damage, 200 dmg) -- dominated by arcane_cataclysm. Redesign: add effect_params `"aoe": True, "aoe_damage_base": 120`. New description: a massive fireball that scorches all enemies in the area. Unique niche: AoE damage.
- `absolute_zero` (T4, damage, 180 dmg) -- dominated by arcane_cataclysm. Redesign: change effect_type to "status", add effect_params `"status_effect": "frozen", "duration": 3, "magnitude": 1.0, "damage_base": 140`. New description: encases the target in absolute cold, freezing them solid. Unique niche: hard CC.

**Resonance domain:**
- `dissonance_wave` (T2, 60 cost) -- niche damage. Redesign: add effect_params `"aoe": True, "debuff_type": "weaken", "debuff_duration": 2`. New description: a discordant pulse that weakens all nearby foes. Unique niche: AoE debuff.
- `echo_mend` (T2, heal, 60 cost) -- niche heal. Redesign: add effect_params `"heal_over_time": True, "hot_duration": 3`. New description: resonant frequencies mend wounds over several rounds. Unique niche: sustained healing (HoT) vs burst.
- `harmonic_shield` (T3, buff, 80 cost) -- rarely chosen over offense. Redesign: add effect_params `"reflect_damage": True, "reflect_percent": 0.25`. New description: a resonant barrier that reflects a quarter of incoming damage back at attackers. Unique niche: damage reflection.

**Naturalism domain:**
- `bramble_burst` (T2) -- superseded by venombloom for poison. Redesign: add effect_params `"aoe": True`. New description: thorny vines erupt around you, lashing all nearby enemies. Unique niche: T2 AoE feral damage.
- `thorn_lash` (T1) -- superseded by higher-tier feral damage. Redesign: add effect_params `"bleed": True, "bleed_duration": 3, "bleed_damage": 8`. New description: barbed thorns tear flesh, leaving a persistent wound. Unique niche: T1 bleed DoT applicator.

**Alchemy domain:**
- `venom_coat` (T1) -- superseded by concentrated_toxin T2. Redesign: add effect_params `"applies_to_next_attack": True, "bonus_poison_damage": 15`. New description: coat your weapon with fast-acting venom that enhances your next strike. Unique niche: attack buff (prep-then-strike).
- `smoke_screen` (T1) -- superseded by flashpowder T2. Redesign: add effect_params `"aoe": True, "miss_chance_increase": 0.3, "duration": 2`. New description: hurl a smoke bomb that blinds all nearby enemies. Unique niche: AoE blind.

**Engineering domain:**
- `enhanced_fuel_injection` (T2) -- superseded by overcharge_protocol T3. Redesign: add effect_params `"resource_refund": True, "refund_percent": 0.5`. New description: recycle waste heat from your companion to partially refund component costs. Unique niche: resource efficiency.

**Remnance domain:**
- `fragment_pulse` (T1, damage) -- weaker memory_strike. Redesign: add effect_params `"echoes_generated": 5`. New description: release a pulse of excavated memories that builds Echoes. Unique niche: T1 echo builder.
- `forgotten_impact` (T2, damage) -- weaker excavate_truth. Redesign: add effect_params `"ignores_armor": True`. New description: channel the weight of forgotten ages through your strike, bypassing all defenses. Unique niche: armor-piercing.
- `pre_curse_strike` (T3, damage) -- weaker void_excavation. Redesign: change effect_type to "damage", add effect_params `"damage_base": 110, "status_effect": "weaken", "status_duration": 2, "status_magnitude": 0.7`. New description: invoke a curse from the age before language, weakening the target's resolve. Unique niche: damage + weaken combo.
- **Remnance weaken debuff differentiation** -- review all Remnance abilities using "weaken" debuff across tiers. Ensure T1 weaken has short duration (1 round), T2 weaken has medium duration (2 rounds), and T3/T4 weaken has longer duration or stronger magnitude, so tier progression is clear.

For each ability: update `effect_params`, `effect_type` (if changed), and `description`. Do NOT change `id`, `name`, `domain`, `tier`, `resource_cost`, `resource_type`, `scaling_primary`, `scaling_secondary`, `subclass_id`, or `attuned_variants` unless the redesign specifically requires it.
  </action>
  <verify>
    <automated>python -c "from world.ability_registry import ABILITIES; ids=['press_the_line','death_of_a_thousand_reads','arcane_bolt','frost_shard','meteor_strike','absolute_zero','dissonance_wave','echo_mend','harmonic_shield','bramble_burst','thorn_lash','venom_coat','smoke_screen','enhanced_fuel_injection','fragment_pulse','forgotten_impact','pre_curse_strike']; [print(f'{i}: {ABILITIES[i][\"effect_params\"]}') for i in ids]"</automated>
  </verify>
  <acceptance_criteria>
    - world/ability_registry.py contains `press_the_line` with effect_params containing `debuff_type`
    - world/ability_registry.py contains `death_of_a_thousand_reads` with effect_params containing `is_multi_hit`
    - world/ability_registry.py contains `arcane_bolt` with effect_params containing `piercing`
    - world/ability_registry.py contains `frost_shard` with effect_params containing `status_effect`
    - world/ability_registry.py contains `meteor_strike` with effect_params containing `aoe`
    - world/ability_registry.py contains `absolute_zero` with effect_params containing `frozen`
    - world/ability_registry.py contains `dissonance_wave` with effect_params containing `aoe`
    - world/ability_registry.py contains `echo_mend` with effect_params containing `heal_over_time`
    - world/ability_registry.py contains `harmonic_shield` with effect_params containing `reflect_damage`
    - world/ability_registry.py contains `fragment_pulse` with effect_params containing `echoes_generated`
    - world/ability_registry.py contains `forgotten_impact` with effect_params containing `ignores_armor`
    - world/ability_registry.py contains `pre_curse_strike` with effect_params containing `weaken`
    - No ability's damage_base was simply increased without adding a new mechanic
    - `python -c "from world.ability_registry import ABILITIES; print(len(ABILITIES))"` prints 330 or more (no abilities removed)
  </acceptance_criteria>
  <done>All ~18 redundant abilities redesigned with unique mechanics. Each brings something different to an 8-slot loadout. No ability is strictly worse than a tier-mate.</done>
</task>

</tasks>

<verification>
- All 330+ abilities still load without import errors
- Each redesigned ability has new effect_params that differentiate it from tier-mates
- No damage_base was simply bumped -- each fix adds a qualitative mechanic
</verification>

<success_criteria>
- Zero import errors from ability_registry.py
- All 18 listed abilities have updated effect_params with unique mechanics
- Total ability count remains >= 330
</success_criteria>

<output>
After completion, create `.planning/phases/05c-ability-polish-and-resource-engine/5c-01-SUMMARY.md`
</output>
