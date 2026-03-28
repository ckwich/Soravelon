---
phase: 05c-ability-polish-and-resource-engine
plan: 03
type: execute
wave: 2
depends_on:
  - 5c-01
  - 5c-02
files_modified:
  - tests/test_ability_engine.py
autonomous: true
requirements:
  - ABL-04
must_haves:
  truths:
    - "Focus combo lifecycle tested: build on hit, reset on miss, cap at 5, consumes_all_focus scaling"
    - "Balance pendulum tested: shift, clamp 0-100, scaling modifier"
    - "Resonance decay tested: -10 per round"
    - "Influence initialization from Reputation tested"
    - "Momentum build on hit and damage taken tested"
    - "Reagents/Components finite depletion tested"
    - "Command ally-action build and solo rate tested"
    - "Echoes investigation bonus persistence tested"
    - "No obsolete abilities in registry (structural uniqueness validated)"
  artifacts:
    - path: "tests/test_ability_engine.py"
      provides: "Resource system tests + redundancy validation"
      contains: "TestFocusResource"
  key_links:
    - from: "tests/test_ability_engine.py"
      to: "world/ability_engine.py"
      via: "imports and function calls"
      pattern: "from world.ability_engine import"
---

<objective>
Add comprehensive test coverage for all 10 resource systems and ability redundancy validation.

Purpose: Verify that each domain's resource mechanics work correctly per D-04 through D-13, and that the ability redesigns from Plan 01 eliminated all redundancies.
Output: Extended test_ability_engine.py with 10+ new test classes
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
@.planning/phases/05c-ability-polish-and-resource-engine/5c-02-SUMMARY.md
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: Test all 10 resource systems and ability redundancy</name>
  <files>tests/test_ability_engine.py</files>
  <read_first>
    - tests/test_ability_engine.py (existing tests -- preserve all, add new classes after)
    - world/ability_engine.py (after Plan 02 -- verify new function signatures and RESOURCE_HANDLERS)
    - world/ability_registry.py (after Plan 01 -- verify redesigned abilities have new effect_params)
    - .planning/phases/05c-ability-polish-and-resource-engine/05C-RESEARCH.md (test map in Validation Architecture section)
  </read_first>
  <behavior>
    - TestResourceInitialization: all 10 resource types initialize with correct shape (Focus max=5, Balance current=50 max=100, Mana starts at max, Influence from Reputation)
    - TestFocusResource: builder adds 1 point (cap 5), spender costs 1-5, miss resets to 0, consumes_all_focus sets to 0, skip-turn resets to 0
    - TestBalanceResource: shift clamps 0-100, feral shift (negative) toward 0, calm shift (positive) toward 100, get_balance_modifier returns correct scaling (position 0 feral = 1.5, position 50 = 1.0, position 100 calm = 1.5)
    - TestResonanceResource: builder generates resonance, decay_resonance subtracts 10 (floor 0), spender requires threshold
    - TestInfluenceResource: initialize from Reputation (20 base + rep * 0.5), spend depletes, no regen hook
    - TestMomentumResource: build_momentum_on_damage adds to pool (cap 100), on_encounter_end resets to 0
    - TestFiniteResources: Reagents and Components spend normally, no regen on round end or encounter end
    - TestCommandResource: ally action builds Command, solo rate is 5 per round, on_encounter_end resets
    - TestEchoesResource: ability use builds 5 echoes, investigation bonus adds to starting pool, bonus decrements encounters_remaining
    - TestAbilityRedundancy: for each domain, verify no two same-tier abilities have identical effect_params (at minimum, each has a distinguishing key)
    - TestFocusScaling: consumes_all_focus with 5 Focus should produce different result than with 1 Focus
  </behavior>
  <action>
Add new test classes to tests/test_ability_engine.py after the existing TestAbilityTierGating class. Use the existing `_mock_character` helper, extending it if needed to support `echoes_investigation_bonus` on db.

**Update `_mock_character` helper** to accept `echoes_investigation_bonus=None` and `reagent_stock=None` and `component_stock=None` parameters, adding them to `char.db`.

**TestResourceInitialization** (10 tests, one per resource type):
- Patch GUILDS and FINGERPRINTS for each domain
- Call `initialize_domain_resource(char)`
- Assert correct shape: type, current, max

Focus: `{"type": "focus", "current": 0, "max": 5}`
Balance: `{"type": "balance", "current": 50, "max": 100}`
Mana: `{"type": "mana", "current": X, "max": X}` where current == max
Influence: patch `world.world_state.get_dimension_score` to return 60, assert current == int(20 + 60 * 0.5) == 50
Momentum: `{"type": "momentum", "current": 0, "max": 100}`
Resonance: `{"type": "resonance", "current": 0, "max": 100}`
Command: `{"type": "command", "current": 0, "max": 100}`
Echoes with bonus: set `char.db.echoes_investigation_bonus = {"amount": 20, "encounters_remaining": 2}`, assert current starts at 20
Reagents: current from `char.db.reagent_stock` or default 50
Components: current from `char.db.component_stock` or default 50

**TestFocusResource** (6 tests):
- `test_focus_builder_adds_one`: create char with focus current=2, call `_post_ability_resource_hook` with builder ability, assert current=3
- `test_focus_builder_caps_at_five`: current=5, builder does not exceed 5
- `test_focus_spender_deducts`: current=3, ability cost=2, call `_handle_focus_spend`, assert current=1
- `test_focus_insufficient`: current=1, cost=3, returns (False, "Insufficient Focus")
- `test_focus_miss_resets`: current=4, call `handle_focus_miss`, assert current=0
- `test_focus_skip_turn_resets`: current=3, `ability_used_this_turn=False`, call `on_round_end_resources`, assert current=0

**TestBalanceResource** (5 tests):
- `test_balance_shift_toward_feral`: current=50, shift=-20, assert current=30
- `test_balance_shift_toward_calm`: current=50, shift=+20, assert current=70
- `test_balance_clamp_min`: current=10, shift=-20, assert current=0
- `test_balance_clamp_max`: current=90, shift=+20, assert current=100
- `test_balance_modifier_feral`: position=0, balance_type="feral", assert modifier == 1.5; position=50 assert 1.0; position=100 assert 0.5

**TestResonanceResource** (3 tests):
- `test_resonance_builder_generates`: resonance_generated=20, current=0, after hook current=20
- `test_decay_resonance`: current=30, decay, assert current=20; current=5, decay, assert current=0
- `test_resonance_spender_costs`: current=80, cost=60, assert current=20

**TestInfluenceResource** (2 tests):
- `test_influence_init_from_reputation`: rep=60, pool=50
- `test_influence_spend_no_regen`: spend 20, assert current reduced; no regen hook restores it

**TestMomentumResource** (3 tests):
- `test_momentum_build_on_hit`: current=20, build 10, assert 30
- `test_momentum_cap`: current=95, build 10, assert 100
- `test_momentum_encounter_end_reset`: current=50, call on_encounter_end_resources, assert 0

**TestFiniteResources** (2 tests):
- `test_reagents_deplete`: current=30, cost=15, assert current=15
- `test_components_no_regen`: current=10, call on_round_end_resources, assert current still 10

**TestCommandResource** (2 tests):
- `test_command_build_with_allies`: mock ally_action_count with 2 allies, assert builds 20
- `test_command_solo_rate`: no allies, assert builds 5

**TestEchoesResource** (3 tests):
- `test_echoes_build_on_ability`: current=10, ability use, assert current=15
- `test_echoes_investigation_bonus_init`: bonus={"amount": 30, "encounters_remaining": 2}, init, assert current=30
- `test_echoes_bonus_decrements`: encounters_remaining=2, call on_encounter_end, assert encounters_remaining=1

**TestAbilityRedundancy** (1 test):
- For each domain, group abilities by tier. For each tier group, verify no two abilities have identical (effect_type, effect_params) tuples. Use frozenset of effect_params items for comparison.

All tests use `unittest.TestCase` + `MagicMock` (no DB). Patch lazy imports at source module (`world.world_state`, `world.guild_engine`).
  </action>
  <verify>
    <automated>python -m pytest tests/test_ability_engine.py -x -v 2>&1 | tail -40</automated>
  </verify>
  <acceptance_criteria>
    - tests/test_ability_engine.py contains class `TestResourceInitialization` with tests for all 10 resource types
    - tests/test_ability_engine.py contains class `TestFocusResource` with at least 5 tests
    - tests/test_ability_engine.py contains class `TestBalanceResource` with at least 4 tests including modifier test
    - tests/test_ability_engine.py contains class `TestResonanceResource` with decay test
    - tests/test_ability_engine.py contains class `TestInfluenceResource` with reputation-based init test
    - tests/test_ability_engine.py contains class `TestMomentumResource` with build and reset tests
    - tests/test_ability_engine.py contains class `TestFiniteResources` with reagents/components tests
    - tests/test_ability_engine.py contains class `TestCommandResource` with ally and solo tests
    - tests/test_ability_engine.py contains class `TestEchoesResource` with bonus persistence test
    - tests/test_ability_engine.py contains class `TestAbilityRedundancy`
    - `python -m pytest tests/test_ability_engine.py -x` exits with code 0
    - All existing tests (TestAbilityRegistryStructure, TestUseAbilityDispatch, TestCooldowns, TestResourceManagement, TestAbilityTierGating) still pass
  </acceptance_criteria>
  <done>Comprehensive test coverage for all 10 resource systems. Focus combo lifecycle, Balance pendulum, Resonance decay, Influence from Reputation, Momentum build/reset, finite resources, Command ally-action, Echoes investigation bonus all verified. Redundancy validation confirms no obsolete abilities remain.</done>
</task>

</tasks>

<verification>
- `python -m pytest tests/test_ability_engine.py -x -v` passes all tests
- `python -m pytest tests/ -x` passes full suite (no regressions)
</verification>

<success_criteria>
- All new test classes pass
- All existing test classes still pass
- No regressions in full test suite
- Every resource type has at least 2 tests covering its unique behavior
</success_criteria>

<output>
After completion, create `.planning/phases/05c-ability-polish-and-resource-engine/5c-03-SUMMARY.md`
</output>
