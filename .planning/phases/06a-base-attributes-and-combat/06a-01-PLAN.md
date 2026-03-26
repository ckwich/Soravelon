---
phase: 06a-base-attributes-and-combat
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - world/base_attributes.py
  - typeclasses/characters.py
autonomous: true
requirements:
  - CMB-01
must_haves:
  truths:
    - "Base stats stored on character.db.base_stats dict with 7 keys"
    - "get_stat_descriptor returns correct flavor text for all 70 tiers"
    - "Point-buy validates min/max constraints and total budget"
    - "Stat growth accumulates on ndb and commits to db"
    - "HP and stamina derive from Endurance + backend level"
  artifacts:
    - path: "world/base_attributes.py"
      provides: "7-stat system, descriptors, point-buy, growth, HP/stamina derivation"
      exports: ["STAT_NAMES", "STAT_DESCRIPTORS", "POINT_BUY_CONFIG", "get_stat_descriptor", "validate_point_buy", "apply_point_buy", "apply_ancestry_modifiers", "derive_hp", "derive_stamina", "derive_max_hp", "derive_max_stamina", "get_actions_per_turn", "get_initiative", "record_stat_use", "commit_stat_growth", "STAT_GROWTH_ACTIONS"]
    - path: "typeclasses/characters.py"
      provides: "base_stats initialization in at_object_creation and ndb init in at_post_puppet"
  key_links:
    - from: "typeclasses/characters.py"
      to: "world/base_attributes.py"
      via: "at_object_creation calls apply_point_buy; at_post_puppet inits stat accumulators"
      pattern: "base_attributes"
---

<objective>
Build the 7-stat base attribute system with descriptor-based display, point-buy allocation, use-driven growth, and HP/stamina/action-budget derivation formulas.

Purpose: All combat math depends on base stats. Stats must exist before damage formulas, initiative, or action budgets can be computed.
Output: world/base_attributes.py with all stat constants, derivation functions, and descriptor tables. Character typeclass extended with base_stats initialization.
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

@typeclasses/characters.py
@world/zone_scaling.py
@world/world_state.py

<interfaces>
<!-- Executor needs these existing interfaces -->

From typeclasses/characters.py:
```python
class Character(ObjectParent, DefaultCharacter):
    def at_object_creation(self):
        # ... existing init: domain_scores, backend_level, ancestry, etc.
    def at_post_puppet(self, **kwargs):
        # ... existing init: session accumulators, domain resource, oob pushes
```

From world/zone_scaling.py:
```python
def get_scale_factor(backend_level): ...  # logarithmic scale
def get_combat_scale(mob, character): ...  # cached per-player
```

From world/world_state.py:
```python
def init_session_accumulators(character): ...
def commit_session_xp(character): ...
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create world/base_attributes.py with stat system, descriptors, and derivation formulas</name>
  <files>world/base_attributes.py</files>
  <action>
Create world/base_attributes.py implementing the full base attribute system per D-01 through D-08.

**Constants (per D-01):**
- STAT_NAMES = ("strength", "agility", "endurance", "mana", "acuity", "presence", "resonance")
- STAT_GOVERNS dict mapping each stat to its description (from vault: Strength governs melee damage/carry/physical power, Agility governs speed/dodge/stealth, etc.)

**Descriptor tables (per D-03, all 70 from research):**
- STAT_DESCRIPTORS dict: {stat_name: [(0, "Feeble"), (10, "Frail"), ...]} for all 7 stats
  - Strength: Feeble/Frail/Average/Sturdy/Strong/Powerful/Mighty/Formidable/Colossal/Prodigious
  - Agility: Sluggish/Clumsy/Steady/Nimble/Quick/Deft/Swift/Fleet/Blinding/Ethereal
  - Endurance: Fragile/Delicate/Hardy/Tough/Resilient/Stout/Stalwart/Unyielding/Ironforged/Indomitable
  - Mana: Inert/Dim/Flickering/Luminous/Radiant/Brilliant/Blazing/Incandescent/Resplendent/Transcendent
  - Acuity: Dull/Unfocused/Attentive/Sharp/Keen/Precise/Insightful/Piercing/Prescient/Omniscient
  - Presence: Invisible/Meek/Noticeable/Engaging/Commanding/Imposing/Magnetic/Sovereign/Overwhelming/Legendary
  - Resonance: Deaf/Faint/Attuned/Receptive/Sensitive/Harmonic/Resonant/Reverberant/Symphonic/Primordial
- get_stat_descriptor(stat_name, value) -> str: Return the descriptor word for a stat value (0-100). Tiers at 0-9, 10-19, ..., 90-100.

**Point-buy (per D-02, Claude's discretion on numbers):**
- POINT_BUY_CONFIG = {"base": 10, "bonus_points": 20, "per_stat_max": 25, "per_stat_min": 5}
- validate_point_buy(allocations: dict) -> (bool, str): Verify all 7 stats present, each within min/max, total points spent = bonus_points + points freed from reductions below base
- apply_point_buy(character, allocations: dict) -> (bool, str): Validate then set character.db.base_stats
- apply_ancestry_modifiers(character) -> None: Read character.db.ancestry, apply additive modifiers to base_stats. Use ANCESTRY_STAT_MODIFIERS dict. Human: +2 presence, +1 acuity. Kau'roran: +3 strength, +2 endurance, -2 acuity. Veth: +2 acuity, +2 agility, -1 strength. Selvar: +2 resonance, +1 presence, +1 agility, -1 endurance.

**HP/Stamina derivation (per D-05, D-06, research formulas):**
- derive_max_hp(character) -> int: base_hp(50) + endurance*5 + backend_level*10
- derive_max_stamina(character) -> int: base_stamina(30) + endurance*2
- derive_hp(character) -> int: Return current hp (from ndb or compute max)
- derive_stamina(character) -> int: Return current stamina

**Action budget (per D-08):**
- get_actions_per_turn(character) -> int: floor(1 + agility / 30). Min 1, practical max 4.
- get_damage_modifier(actions_per_turn) -> float: 1.0 / sqrt(actions_per_turn). Reduces per-action damage for multi-action builds.

**Initiative (per D-07):**
- get_initiative(combatant) -> int: For characters: agility_stat + randint(1, 20). For mobs: (mob.db.speed or 1.0) * 10 + randint(1, 20). Fixed for entire encounter.

**Stat growth through use (per D-04):**
- STAT_GROWTH_ACTIONS dict mapping action strings to stat names: {"melee_hit": "strength", "dodge_success": "agility", "damage_taken": "endurance", "spell_cast": "mana", "cooldown_reduced": "acuity", "social_ability": "presence", "resonance_ability": "resonance"}
- STAT_GROWTH_RATES: diminishing returns curve. 0-25: 1.0x, 25-50: 0.75x, 50-75: 0.40x, 75-90: 0.10x, 90-100: 0.02x
- record_stat_use(character, action_type, amount=1) -> None: Accumulate stat XP on ndb.stat_xp_accumulators[stat_name]. Apply diminishing returns based on current stat value.
- commit_stat_growth(character) -> None: Read ndb accumulators, convert XP to stat points, update character.db.base_stats (SaverDict copy pattern). Called by SessionCommitScript alongside domain XP flush.

All functions return (bool, str) tuples where they can fail. Pure getters return values directly.
  </action>
  <verify>
    <automated>python -c "from world.base_attributes import STAT_NAMES, STAT_DESCRIPTORS, get_stat_descriptor, validate_point_buy, derive_max_hp, get_actions_per_turn, get_initiative, STAT_GROWTH_ACTIONS; print('OK:', len(STAT_NAMES), 'stats,', sum(len(v) for v in STAT_DESCRIPTORS.values()), 'descriptors')"</automated>
  </verify>
  <done>world/base_attributes.py exists with all 7 stats, 70 descriptors, point-buy validation, HP/stamina derivation, action budget, initiative, and stat growth functions. All constants and functions are importable.</done>
</task>

<task type="auto">
  <name>Task 2: Wire base stats into Character typeclass</name>
  <files>typeclasses/characters.py</files>
  <action>
Extend Character typeclass to initialize and manage base stats.

**In at_object_creation() — add after existing domain_scores init:**
- self.db.base_stats = {stat: 10 for stat in STAT_NAMES}  # default base, overwritten by point-buy
- self.db.stat_xp = {stat: 0.0 for stat in STAT_NAMES}  # persistent stat growth XP

**In at_post_puppet() — add after existing domain resource init:**
- self.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}  # session volatile
- Initialize combat-relevant ndb state that combat system will use:
  - self.ndb.combat_handler = None
  - self.ndb.combat_target_id = None
  - self.ndb.active_effects = []
  - self.ndb.actions_remaining = 0
  - self.ndb.ability_used_this_turn = False
  - self.ndb.hp = derive_max_hp(self)  # full HP on login
  - self.ndb.stamina = derive_max_stamina(self)  # full stamina on login
  - self.ndb.charged_ability = None  # for charged ability tracking per D-10

**In at_pre_unpuppet() — add before existing commit_session_xp call:**
- from world.base_attributes import commit_stat_growth
- commit_stat_growth(self)  # flush stat XP accumulators on logout

Also add to at_pre_unpuppet: combat cleanup — if self.ndb.combat_handler, remove self from combat (clean disconnect).

Import lazily inside methods to avoid circular imports (standard pattern).
  </action>
  <verify>
    <automated>python -c "from typeclasses.characters import Character; print('Character typeclass importable')"</automated>
  </verify>
  <done>Character.at_object_creation sets base_stats dict. at_post_puppet initializes hp, stamina, stat accumulators, and combat ndb slots. at_pre_unpuppet flushes stat growth and cleans up combat state.</done>
</task>

</tasks>

<verification>
- `python -c "from world.base_attributes import *"` imports without error
- get_stat_descriptor("strength", 45) returns "Strong"
- get_stat_descriptor("agility", 92) returns "Ethereal"
- validate_point_buy with valid allocation returns (True, ...)
- validate_point_buy with over-budget returns (False, ...)
- derive_max_hp for endurance=10, backend_level=1 returns 110 (50+50+10)
- get_actions_per_turn for agility=60 returns 3
</verification>

<success_criteria>
All 7 base stats defined with 70 unique descriptors. Point-buy allocation validates correctly. HP/stamina derivation formulas match research spec. Action budget and initiative formulas implemented. Stat growth through use accumulates with diminishing returns. Character typeclass initializes all base stat state at creation and login.
</success_criteria>

<output>
After completion, create `.planning/phases/06a-base-attributes-and-combat/06a-01-SUMMARY.md`
</output>
