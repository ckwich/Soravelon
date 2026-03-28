---
phase: 05c-ability-polish-and-resource-engine
plan: 04
type: execute
wave: 1
depends_on: ["5c-02", "5c-03"]
files_modified:
  - world/ability_registry.py
  - world/ability_engine.py
  - tests/test_ability_engine.py
autonomous: true
gap_closure: true
requirements: [ABL-04]

must_haves:
  truths:
    - "Every alchemy ability has a reagent_type field in effect_params classifying its reagent category"
    - "Every engineering ability has a component_type field in effect_params classifying its component category"
    - "_handle_reagents_spend and _handle_components_spend read the variant type from the ability"
  artifacts:
    - path: "world/ability_registry.py"
      provides: "reagent_type on all 33 alchemy abilities, component_type on all 33 engineering abilities"
      contains: "reagent_type"
    - path: "world/ability_engine.py"
      provides: "Variant-aware handler docstrings and field reads"
      contains: "reagent_type"
    - path: "tests/test_ability_engine.py"
      provides: "Tests validating variant fields exist and handlers read them"
      contains: "reagent_type"
  key_links:
    - from: "world/ability_engine.py"
      to: "world/ability_registry.py"
      via: "ability dict effect_params.reagent_type / component_type"
      pattern: "reagent_type|component_type"
---

<objective>
Close the single verification gap from 5c-VERIFICATION.md: add typed resource variant fields (reagent_type, component_type) to all alchemy and engineering abilities, and update the resource handlers to read these fields.

Purpose: Satisfy ROADMAP success criterion 4 — "Typed resource variants for Engineering (component types) and Alchemy (reagent types) have data-layer support (variant fields on abilities)"
Output: All 33 alchemy abilities have reagent_type in effect_params, all 33 engineering abilities have component_type in effect_params, handlers read the fields, tests verify.
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
@.planning/phases/05c-ability-polish-and-resource-engine/5c-VERIFICATION.md
@.planning/phases/05c-ability-polish-and-resource-engine/5c-02-SUMMARY.md
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: Add reagent_type and component_type variant fields to all alchemy and engineering abilities</name>
  <files>world/ability_registry.py, world/ability_engine.py, tests/test_ability_engine.py</files>
  <read_first>
    - world/ability_registry.py (all alchemy abilities lines ~5929-6400, all engineering abilities — search for "ENGINEERING DOMAIN POOL")
    - world/ability_engine.py (lines 280-301 for _handle_reagents_spend and _handle_components_spend)
    - tests/test_ability_engine.py (lines 744-766 for TestFiniteResources)
  </read_first>
  <behavior>
    - Test: Every ability with domain=="alchemy" has effect_params["reagent_type"] in {"volatile", "curative", "toxic"}
    - Test: Every ability with domain=="engineering" has effect_params["component_type"] in {"gear", "conduit", "plating"}
    - Test: _handle_reagents_spend reads ability effect_params["reagent_type"] (logged or stored, even though pool is still single)
    - Test: _handle_components_spend reads ability effect_params["component_type"] (logged or stored, even though pool is still single)
  </behavior>
  <action>
**Step 1: Add test class TestTypedResourceVariants to tests/test_ability_engine.py** (after TestAbilityRedundancy):

```python
class TestTypedResourceVariants(unittest.TestCase):
    """Verify all alchemy/engineering abilities have typed resource variant fields."""

    def test_all_alchemy_have_reagent_type(self):
        from world.ability_registry import ABILITIES
        valid_types = {"volatile", "curative", "toxic"}
        for aid, a in ABILITIES.items():
            if a.get("domain") == "alchemy":
                rt = a.get("effect_params", {}).get("reagent_type")
                self.assertIn(rt, valid_types, f"{aid} missing/invalid reagent_type: {rt}")

    def test_all_engineering_have_component_type(self):
        from world.ability_registry import ABILITIES
        valid_types = {"gear", "conduit", "plating"}
        for aid, a in ABILITIES.items():
            if a.get("domain") == "engineering":
                ct = a.get("effect_params", {}).get("component_type")
                self.assertIn(ct, valid_types, f"{aid} missing/invalid component_type: {ct}")

    def test_reagents_handler_reads_variant(self):
        from world.ability_engine import _handle_reagents_spend
        char = _mock_character(domain_resource={"type": "reagents", "current": 50, "max": 100})
        ability = {"resource_cost": 10, "effect_params": {"reagent_type": "volatile"}}
        ok, msg = _handle_reagents_spend(char, ability)
        self.assertTrue(ok)

    def test_components_handler_reads_variant(self):
        from world.ability_engine import _handle_components_spend
        char = _mock_character(domain_resource={"type": "components", "current": 50, "max": 100})
        ability = {"resource_cost": 10, "effect_params": {"component_type": "conduit"}}
        ok, msg = _handle_components_spend(char, ability)
        self.assertTrue(ok)
```

Run tests — they MUST FAIL (RED phase).

**Step 2: Add reagent_type to every alchemy ability's effect_params in ability_registry.py.**

Classification rules (based on ability effect_type and theme):
- **"volatile"** — damage-dealing abilities (effect_type=damage, dot, or has damage_base): reagent_toss, acid_flask, caustic_compound, concentrated_toxin, blistering_mixture, volatile_concoction, alchemists_perfection, transmuters_masterwork, fumecaster_poison_bolt, fumecaster_noxious_storm, fumewright_gas_trap, fumewright_chemical_engine, venomfang_toxic_bite, firstblight_ancient_venom, firstblight_dragon_blight, plaguecommand_gas_deployment, plaguecommand_scorched_earth, mireweald_swamp_rot, mireweald_mire_zone, voidbrewer_resonant_compound, voidbrewer_old_world_brew
- **"toxic"** — poison/debuff abilities (effect_type=debuff or status with debilitating theme): venom_coat, smoke_screen, flashpowder, paralytic_compound, weakening_agent, nightshade_silent_toxin, nightshade_midnight_bloom, sweetpoison_honeyed_words, sweetpoison_killing_kindness
- **"curative"** — buff/utility abilities (effect_type=buff): strengthening_draught, reagent_mastery, venomfang_apex_predator

For each ability, add `"reagent_type": "<type>"` inside the existing `effect_params` dict.

**Step 3: Add component_type to every engineering ability's effect_params in ability_registry.py.**

Classification rules:
- **"gear"** — companion/mechanical damage abilities: deploy_sentry, rivet_burst, deploy_shock_mine, fragmentation_charge, companion_overdrive, masterwork_assembly, ironsmith_assault_protocol, ironsmith_ironforged_protocol, gearhand_scout_strike, gearhand_ghost_protocol, bucketborn_anomalous_function, bucketborn_base8_resonance, sparkshaper_arcane_payload, sparkshaper_overload_device
- **"plating"** — defensive/buff abilities: reinforce_chassis, companion_intercept, deploy_barrier_wall, overcharge_protocol, fortification_engine, growsmith_bark_shield, growsmith_living_fortress, siegewright_siege_stance, siegewright_fortress_protocol, total_recall_refit
- **"conduit"** — utility/debuff/tactical abilities: construct_snare, field_calibration, enhanced_fuel_injection, dealsmith_trade_advantage, dealsmith_consortium_protocol, fumehand_chemical_spray, fumehand_overcharge_protocol, runewright_forge_rune_swap, runewright_forge_full_rune_activation

**Step 4: Update _handle_reagents_spend and _handle_components_spend in ability_engine.py** to read the variant field from the ability. Since the pool remains a single undifferentiated pool for now, the handler reads the variant type and includes it in logging/messaging but does not change spend logic:

```python
def _handle_reagents_spend(character, ability):
    """Reagents: finite stock, standard spend. Reads reagent_type variant."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    reagent_type = ability.get("effect_params", {}).get("reagent_type", "generic")
    return spend_domain_resource(character, cost)


def _handle_components_spend(character, ability):
    """Components: finite stock like reagents. Reads component_type variant."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    component_type = ability.get("effect_params", {}).get("component_type", "generic")
    return spend_domain_resource(character, cost)
```

**Step 5: Run tests — they MUST PASS (GREEN phase).**
  </action>
  <verify>
    <automated>cd C:/Dev/Evennia/soravelon && python -m pytest tests/test_ability_engine.py -x -q 2>&1 | tail -5</automated>
  </verify>
  <acceptance_criteria>
    - grep -c "reagent_type" world/ability_registry.py returns 33 (one per alchemy ability)
    - grep -c "component_type" world/ability_registry.py returns 33 (one per engineering ability)
    - grep "reagent_type" world/ability_engine.py shows the field being read in _handle_reagents_spend
    - grep "component_type" world/ability_engine.py shows the field being read in _handle_components_spend
    - grep "TestTypedResourceVariants" tests/test_ability_engine.py returns a match
    - python -m pytest tests/test_ability_engine.py -x passes with 0 failures
  </acceptance_criteria>
  <done>All 33 alchemy abilities have reagent_type in effect_params (volatile/curative/toxic), all 33 engineering abilities have component_type in effect_params (gear/conduit/plating), handlers read variant fields, 4 new tests pass alongside all existing 61 tests.</done>
</task>

</tasks>

<verification>
1. `python -c "from world.ability_registry import ABILITIES; alc=[a for a in ABILITIES.values() if a.get('domain')=='alchemy']; assert all('reagent_type' in a.get('effect_params',{}) for a in alc), 'Missing reagent_type'; print(f'All {len(alc)} alchemy abilities have reagent_type')"` — prints "All 33 alchemy abilities have reagent_type"
2. `python -c "from world.ability_registry import ABILITIES; eng=[a for a in ABILITIES.values() if a.get('domain')=='engineering']; assert all('component_type' in a.get('effect_params',{}) for a in eng), 'Missing component_type'; print(f'All {len(eng)} engineering abilities have component_type')"` — prints "All 33 engineering abilities have component_type"
3. `python -m pytest tests/test_ability_engine.py -x` — all tests pass (65 total: 61 existing + 4 new)
</verification>

<success_criteria>
- ROADMAP success criterion 4 is satisfied: typed resource variants have data-layer support
- All 33 alchemy abilities classified as volatile/curative/toxic
- All 33 engineering abilities classified as gear/conduit/plating
- Resource handlers read variant fields from ability effect_params
- Full test suite passes with no regressions
</success_criteria>

<output>
After completion, create `.planning/phases/05c-ability-polish-and-resource-engine/5c-04-SUMMARY.md`
</output>
