---
phase: 06a-base-attributes-and-combat
plan: 07
type: execute
wave: 4
depends_on: ["06a-05", "06a-06"]
files_modified:
  - tests/test_base_attributes.py
  - tests/test_status_effects.py
  - tests/test_combat_engine.py
  - tests/test_combat_ai.py
  - tests/test_combat_script.py
autonomous: true
requirements:
  - CMB-01
  - CMB-02
  - CMB-03
  - CMB-04
must_haves:
  truths:
    - "All test files pass with evennia test runner"
    - "Each CMB requirement has at least one test covering its core behavior"
    - "Descriptor, point-buy, stat growth, status effects, compound triggers all have unit tests"
  artifacts:
    - path: "tests/test_base_attributes.py"
      provides: "Tests for descriptors, point-buy, stat growth, HP/stamina derivation"
    - path: "tests/test_status_effects.py"
      provides: "Tests for stackable/non-stackable effects, compounds, tick logic"
    - path: "tests/test_combat_engine.py"
      provides: "Tests for damage resolution, zone scaling integration, corpse locking"
    - path: "tests/test_combat_ai.py"
      provides: "Tests for mob ability selection, targeting, condition checks"
    - path: "tests/test_combat_script.py"
      provides: "Tests for turn management, initiative, round progression"
  key_links:
    - from: "tests/"
      to: "world/"
      via: "Unit tests for all combat modules"
      pattern: "from world\\."
---

<objective>
Create the test suite covering all Phase 6a combat modules. Tests validate every CMB requirement and all critical combat behaviors.

Purpose: Combat is the most complex system in the game. Without tests, regressions during Phase 6b and content authoring will be invisible. Each module needs focused unit tests.
Output: 5 test files covering base attributes, status effects, combat engine, combat AI, and combat script.
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/06a-base-attributes-and-combat/06a-CONTEXT.md
@.planning/phases/06a-base-attributes-and-combat/06A-RESEARCH.md

@.planning/phases/06a-base-attributes-and-combat/06a-01-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-02-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-03-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-04-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-05-SUMMARY.md
@.planning/phases/06a-base-attributes-and-combat/06a-06-SUMMARY.md

@tests/test_world_state.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create test_base_attributes.py and test_status_effects.py</name>
  <files>tests/test_base_attributes.py, tests/test_status_effects.py</files>
  <action>
Create tests following existing project test patterns (see tests/test_world_state.py for conventions: EvenniaTestCase, one class per scenario, PascalCase test class names).

**tests/test_base_attributes.py:**

TestStatDescriptors:
- test_strength_feeble: get_stat_descriptor("strength", 5) == "Feeble"
- test_strength_prodigious: get_stat_descriptor("strength", 95) == "Prodigious"
- test_agility_ethereal: get_stat_descriptor("agility", 92) == "Ethereal"
- test_all_stats_have_10_tiers: for each stat in STAT_NAMES, verify 10 descriptor entries
- test_boundary_values: value 9 -> tier 0, value 10 -> tier 1, value 100 -> tier 9

TestPointBuy:
- test_valid_balanced_allocation: 7 stats each at 13 (3 bonus each = 21 points, need to adjust to exactly 20)
- test_valid_focused_allocation: 2 stats at 25, rest at base 10, verify total budget correct
- test_over_budget_rejected: allocate more than 20 bonus points, expect (False, ...)
- test_stat_above_max_rejected: one stat at 30 (above 25 max), expect (False, ...)
- test_stat_below_min_rejected: one stat at 3 (below 5 min), expect (False, ...)
- test_missing_stat_rejected: only 6 of 7 stats, expect (False, ...)

TestStatGrowth:
- test_record_stat_use_accumulates: record_stat_use with "melee_hit" adds to ndb accumulator
- test_diminishing_returns_high_stat: stat at 80 gains much less than stat at 10
- test_commit_updates_db: commit_stat_growth writes accumulated XP to db.base_stats

TestDerivation:
- test_hp_formula: endurance 10, level 1 -> 50+50+10=110
- test_hp_formula_high: endurance 50, level 25 -> 50+250+250=550
- test_stamina_formula: endurance 10 -> 30+20=50
- test_actions_per_turn: agility 10->1, agility 30->2, agility 60->3, agility 90->4
- test_damage_modifier: 1 action->1.0, 2 actions->~0.71, 4 actions->0.5

**tests/test_status_effects.py:**

Use MagicMock for target objects with ndb.active_effects = [] and ndb.hp attribute.

TestApplyStackable:
- test_first_application: apply poison -> stacks=1, duration set
- test_stacking: apply poison twice -> stacks=2
- test_max_stacks: apply poison 6 times -> stacks=5 (capped)
- test_refresh_duration: second application refreshes duration to new value

TestApplyNonStackable:
- test_first_application: apply slow -> entry created
- test_stronger_replaces: apply slow magnitude 5, then magnitude 10 -> magnitude 10 kept
- test_weaker_rejected: apply slow magnitude 10, then magnitude 5 -> (False, "stronger")

TestCompoundTriggers:
- test_burn_wet_steam: apply burn then wet -> check_compound_triggers returns ["steam"], both consumed
- test_poison_slow_venom_lag: apply poison then slow -> both persist + venom_lag added
- test_no_compound_single_effect: apply only poison -> no compound triggered

TestTickEffects:
- test_poison_damage: 2 stacks poison -> tick deals 8+5=13 damage
- test_duration_decrement: effect with duration 3 -> after tick, duration 2
- test_effect_removed_at_zero: duration 1 -> after tick, effect removed
- test_drain_reduces_stamina: drain 1 stack -> stamina reduced by 5

TestEffectModifiers:
- test_stun_skips_turn: stun active -> get_effect_modifiers returns skip_turn=True
- test_slow_reduces_actions: slow active -> action_budget_penalty=1
- test_haste_adds_actions: haste active -> action_budget_bonus=1
  </action>
  <verify>
    <automated>evennia test --settings server.conf.settings tests/test_base_attributes.py tests/test_status_effects.py -x</automated>
  </verify>
  <done>test_base_attributes.py covers all 70 descriptors, point-buy validation, stat growth with diminishing returns, and HP/stamina/action-budget derivation. test_status_effects.py covers stackable/non-stackable application, all 4 compound triggers, tick damage, and effect modifier aggregation.</done>
</task>

<task type="auto">
  <name>Task 2: Create test_combat_engine.py, test_combat_ai.py, and test_combat_script.py</name>
  <files>tests/test_combat_engine.py, tests/test_combat_ai.py, tests/test_combat_script.py</files>
  <action>
**tests/test_combat_engine.py:**

TestBasicAttackResolution (CMB-01):
- test_melee_damage_range: resolve_basic_attack with known stats produces damage in expected range
- test_zone_scaling_applied: mock get_player_damage_to_mob, verify it's called (CMB-02)
- test_resistance_applied: target with fire resistance 0.5 takes half fire damage
- test_miss_on_blind: attacker blinded has chance to miss

TestAbilityDamageResolution (CMB-01):
- test_ability_scales_with_primary_stat: higher stat = more damage
- test_status_effect_applied: ability with status_effect field applies it to target

TestEliteBossScaling (CMB-02):
- test_elite_incoming_damage: elite mob deals 1.40x damage to player
- test_elite_damage_reduction: player deals 0.75x damage to elite mob
- test_boss_scaling: boss mob uses 1.80x/0.50x multipliers

TestCorpseLocking (CMB-04):
- test_killer_can_loot: killer can access locked corpse
- test_non_killer_blocked: non-killer blocked from locked corpse
- test_group_member_can_loot: killer's group member can access locked corpse
- test_open_phase_anyone: after grace period, anyone can loot
- test_corpse_decays: corpse deleted after decay timer

TestDeathHandling:
- test_mob_death_spawns_corpse: handle_mob_death creates CorpseContainer in room
- test_player_death_creates_corpse: handle_player_death moves items to corpse

**tests/test_combat_ai.py (CMB-03):**

TestAbilitySelection:
- test_selects_by_weight: higher weight abilities selected more often (statistical test with N=100)
- test_cooldown_filtered: ability on cooldown not selected
- test_condition_checked: "target_below_50hp" only passes when target HP < 50%
- test_fallback_basic_attack: all abilities on cooldown -> returns basic_attack
- test_no_infinite_loop: mob with empty ability list returns basic_attack immediately

TestMobTargeting:
- test_last_attacker_priority: mob targets whoever last hit it
- test_random_fallback: no attacker -> random target from players
- test_vanish_skipped: target with vanish effect not targeted

TestScriptedSequence:
- test_hp_threshold_fires: sequence with hp_below_50 fires when mob at 40% HP
- test_fires_once: same threshold doesn't fire twice
- test_combat_start_fires: round 1 fires combat_start triggers

**tests/test_combat_script.py (CMB-01, CMB-04):**

Use EvenniaTestCase with create_character/create_object for integration testing.

TestInitiativeOrder:
- test_sorted_descending: higher initiative goes first
- test_interleaved: players and mobs alternate based on initiative, not grouped (D-15)

TestTurnManagement:
- test_advance_skips_stunned: stunned combatant's turn is skipped
- test_round_end_ticks_effects: after full round, tick_effects called for all combatants
- test_round_end_decrements_cooldowns: cooldowns go down by 1

TestCombatEnd:
- test_all_enemies_dead: combat ends when last mob dies
- test_all_players_fled: combat ends when all players flee
- test_cleanup_removes_cmdset: CombatCmdSet removed from players at end

TestGroupCombat (CMB-04):
- test_group_timeout_active: is_group_combat=True triggers round timer
- test_solo_no_timeout: solo combat waits indefinitely
  </action>
  <verify>
    <automated>evennia test --settings server.conf.settings tests/test_combat_engine.py tests/test_combat_ai.py tests/test_combat_script.py -x</automated>
  </verify>
  <done>test_combat_engine.py covers damage resolution, zone scaling integration (CMB-02), elite/boss modifiers, and corpse locking (CMB-04). test_combat_ai.py covers weighted ability selection, condition vocabulary, and targeting (CMB-03). test_combat_script.py covers initiative ordering, turn management, round end processing, and combat end cleanup (CMB-01).</done>
</task>

</tasks>

<verification>
Full test suite command:
```
evennia test --settings server.conf.settings tests/test_base_attributes.py tests/test_status_effects.py tests/test_combat_engine.py tests/test_combat_ai.py tests/test_combat_script.py -x
```
All tests pass.
</verification>

<success_criteria>
Every CMB requirement has at least one test. Base attributes: 70 descriptors verified, point-buy constraints enforced, formulas correct. Status effects: stacking, compounds, ticks all tested. Combat engine: damage with scaling + resistance tested. Combat AI: weight selection + condition vocabulary tested. Combat script: initiative ordering + turn flow + cleanup tested. Full suite runs green.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-07-SUMMARY.md`
</output>
