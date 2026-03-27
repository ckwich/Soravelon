---
phase: 06c-npc-dialogue-and-crafting
plan: 05
type: execute
wave: 3
depends_on: ["06c-01", "06c-02", "06c-03", "06c-04"]
files_modified:
  - tests/test_dialogue.py
  - tests/test_crafting.py
autonomous: true
requirements: [NPC-01, NPC-02, NPC-03]
must_haves:
  truths:
    - "Standing tier mapping tested for all 8 tiers including betrayal"
    - "Topic priority stack tested for condition ordering"
    - "Keyword extraction tested for all 4 stages"
    - "Context packet interface tested for LLM compatibility"
    - "Crafting quality gradient tested across skill/difficulty ranges"
    - "Recipe discovery model tested for learn/query/default"
  artifacts:
    - path: "tests/test_dialogue.py"
      provides: "NPC dialogue system tests covering NPC-01, NPC-02, NPC-03, D-03, D-04, D-05"
      min_lines: 150
    - path: "tests/test_crafting.py"
      provides: "Crafting system tests covering D-15, D-16, D-17"
      min_lines: 100
  key_links:
    - from: "tests/test_dialogue.py"
      to: "world/dialogue_engine.py"
      via: "direct function calls"
      pattern: "from world.dialogue_engine import"
    - from: "tests/test_crafting.py"
      to: "world/crafting_engine.py"
      via: "direct function calls"
      pattern: "from world.crafting_engine import"
---

<objective>
Comprehensive test suite for NPC dialogue and crafting systems. Tests validate all requirement behaviors: context packet injection (NPC-01), Standing-based response variation (NPC-02), context packet interface stability (NPC-03), crafting quality variance (D-15), recipe discovery (D-16).

Purpose: Verify all systems work correctly before phase completion. Tests serve as regression guard for future changes.
Output: tests/test_dialogue.py, tests/test_crafting.py
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-CONTEXT.md
@.planning/phases/06c-npc-dialogue-and-crafting/06C-RESEARCH.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-01-SUMMARY.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-02-SUMMARY.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-03-SUMMARY.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-04-SUMMARY.md

@tests/test_world_state.py
@tests/test_banking.py

<interfaces>
From world/dialogue_engine.py:
```python
def get_standing_tier(character, npc)
def resolve_greeting(npc, character)
def resolve_topic_response(npc, character, topic_key)
def get_npc_hints(npc, character)
def extract_topic(text, available_topics)
def record_topic_learned(character, npc_id, topic_key, context)
def ambient_npc_tick()
def fire_npc_reactive_echo(room, trigger_type)
```

From world/crafting_engine.py:
```python
def calculate_craft_quality(skill_value, recipe_difficulty, has_station_bonus=False)
def check_station(character, required_station)
def get_known_recipes(character, skill_filter=None)
def learn_recipe(character, recipe_id, learned_from="")
def craft_item(character, recipe_id)
def get_quality_modifier(quality_tier)
```
</interfaces>
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: Dialogue system tests</name>
  <files>tests/test_dialogue.py</files>
  <behavior>
  NPC-01 (Context Packet Injection):
  - Test: Context packet includes ancestry, guild, Standing, Trust, betrayal, dimension scores
  - Test: Dialogue engine reads context packet to select topic responses

  NPC-02 (Standing-Based Responses):
  - Test: High disposition (0.8+) maps to "exalted" tier
  - Test: Low disposition (-0.7) maps to "hostile" tier
  - Test: Betrayal flag overrides disposition to "betrayal" tier
  - Test: Each of 8 tiers gets correct greeting text
  - Test: Topic response priority stack returns quest_complete over honored
  - Test: Topic response returns default when no conditions match

  NPC-03 (Context Packet Interface):
  - Test: Context packet has all required keys for LLM compatibility
  - Test: Context packet has stable key names (regression guard)

  D-04 (Dynamic Hints):
  - Test: Base hints always included
  - Test: Tier hints only included when Standing matches
  - Test: Already-known topics excluded via KnownTopicRecord
  - Test: Hints capped at MAX_HINTS_DISPLAYED (4)

  D-05 (Keyword Extraction):
  - Test: Direct topic match ("wolves" in text matches "wolves" topic)
  - Test: Synonym match ("wolf" matches "wolves" via TOPIC_SYNONYMS)
  - Test: Partial word match ("node" in "what about that node" matches "node_reading")
  - Test: No match returns None
  - Test: Longest match wins (avoid "node" matching before "node_reading")
  </behavior>
  <action>
Create tests/test_dialogue.py using Evennia's EvenniaTestCase base class. Follow existing test patterns from tests/test_world_state.py.

Test class structure:

**TestStandingTierMapping** — Test get_standing_tier() with mocked disposition values:
- Create a mock NPC with db.faction set
- Mock get_mob_disposition to return specific floats
- Verify each tier: hostile (<-0.6), unfriendly (-0.6 to -0.4), neutral (-0.4 to -0.2), acknowledged (-0.2 to 0.2), friendly (0.2 to 0.4), honored (0.4 to 0.6), exalted (0.6 to 0.8), exalted (0.8+)
- Mock betrayal flag True -> returns "betrayal" regardless of disposition

**TestGreetingResolution** — Test resolve_greeting():
- Create NPC with dialogue_greeting_tiers on db
- Verify correct text returned for each tier
- Verify fallback to "neutral" when tier text missing
- Verify generic fallback when no greeting data at all

**TestTopicPriorityStack** — Test resolve_topic_response():
- Create NPC with dialogue_topics having multiple conditions per topic
- Mock context with quest_complete=True -> returns quest_complete text
- Mock context with honored tier + no quest -> returns honored text
- Mock context with nothing special -> returns default text
- Verify "default" always works as fallback

**TestKeywordExtraction** — Test extract_topic():
- Direct match: "wolves" in ["wolves", "node", "work"] -> "wolves"
- Synonym: "wolf" not in topics directly, but "wolf" in TOPIC_SYNONYMS["wolves"] -> "wolves"
- Partial: "I saw a strange node" with topic "node_reading" -> matches via "node" word
- No match: "hello there" with ["wolves", "node"] -> None
- Longest first: "node_reading" and "node" both topics, "node reading" matches "node_reading" first

**TestDynamicHints** — Test get_npc_hints():
- NPC with base_hints=["wolves", "work"], tier_hints={"honored": ["node"]}
- Character with "friendly" tier -> returns ["wolves", "work"] (no "node")
- Character with "honored" tier -> returns ["wolves", "work", "node"]
- After record_topic_learned for "wolves" -> returns ["work"] (or ["work", "node"] if honored)
- With 6 base hints -> only 4 returned (MAX_HINTS_DISPLAYED cap)

**TestContextPacketInterface** — Test _build_dialogue_context():
- Verify returned dict has ALL required keys: ancestry, reputation, network, bond, legacy, attunement, standing, trust, betrayal_flag, companion_present, guild, subclass
- This is the NPC-03 regression guard — if any key is missing, LLM integration breaks

Use `unittest.mock.patch` for mocking get_mob_disposition, get_standing, get_betrayal. Create test NPCs and characters using Evennia's test helpers.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && evennia test --settings server.conf.settings tests/test_dialogue.py -x 2>&1 | tail -5</automated>
  </verify>
  <done>test_dialogue.py has 6+ test classes covering NPC-01, NPC-02, NPC-03, D-04, D-05. All tests pass.</done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: Crafting system tests</name>
  <files>tests/test_crafting.py</files>
  <behavior>
  D-15 (Quality Variance):
  - Test: skill 80 vs difficulty 20 (gap +60) -> superior or masterwork
  - Test: skill 10 vs difficulty 60 (gap -50) -> flawed
  - Test: skill 50 vs difficulty 50 (gap 0) -> standard (mostly)
  - Test: station bonus shifts quality up by 1 tier
  - Test: Quality modifier returns correct multiplier (flawed=0.6, masterwork=2.0)

  D-16 (Recipe Discovery):
  - Test: Default recipes auto-learned on first query
  - Test: learn_recipe creates CharacterRecipe record
  - Test: Duplicate learn_recipe returns (False, "already known")
  - Test: get_known_recipes returns only recipes character knows
  - Test: get_known_recipes with skill_filter narrows to that skill

  D-17 (Three Professions):
  - Test: RECIPE_REGISTRY has at least 2 cooking, 1 smithing, 2 alchemy recipes
  - Test: Each recipe has required fields (name, skill, difficulty, station, ingredients, output)

  Station Check:
  - Test: Room with crafting_campfire tag passes check_station("campfire")
  - Test: Room without tag fails check_station
  </behavior>
  <action>
Create tests/test_crafting.py using Evennia's EvenniaTestCase base class.

Test class structure:

**TestCraftQuality** — Test calculate_craft_quality():
- High skill, low difficulty: gap=60 -> consistently superior/masterwork
- Low skill, high difficulty: gap=-50 -> consistently flawed
- Equal skill and difficulty: gap=0 -> standard (run 20 times, majority standard)
- Station bonus: same inputs with has_station_bonus=True -> one tier higher on average
- Boundary: skill=0, difficulty=100 -> always flawed

**TestQualityModifier** — Test get_quality_modifier():
- "flawed" -> 0.6
- "standard" -> 1.0
- "fine" -> 1.3
- "superior" -> 1.6
- "masterwork" -> 2.0

**TestRecipeDiscovery** — Test learn_recipe() and get_known_recipes():
- learn_recipe for valid recipe -> (True, success message)
- learn_recipe for already-known recipe -> (False, "already know")
- get_known_recipes includes default_known recipes without explicit learn
- get_known_recipes with skill_filter="cooking" only returns cooking recipes
- get_known_recipes for character with no records returns only default_known recipes

**TestRecipeRegistry** — Test RECIPE_REGISTRY data integrity:
- At least 6 recipes total
- Each recipe has all required keys
- Each recipe's skill exists in SKILL_DEFINITIONS
- Each recipe's station exists in STATION_REQUIREMENTS
- At least one default_known=True recipe per profession (cooking, alchemy)

**TestStationCheck** — Test check_station():
- Room with tag ("crafting_campfire", category="crafting_station") -> (True, ...)
- Room without tag -> (False, descriptive error)
- None location -> (False, error)

Use `unittest.mock.patch` where needed. Create test rooms with tags using Evennia's test helpers.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && evennia test --settings server.conf.settings tests/test_crafting.py -x 2>&1 | tail -5</automated>
  </verify>
  <done>test_crafting.py has 5+ test classes covering D-15, D-16, D-17. All tests pass.</done>
</task>

</tasks>

<verification>
- `evennia test --settings server.conf.settings tests/test_dialogue.py -x` passes
- `evennia test --settings server.conf.settings tests/test_crafting.py -x` passes
- `evennia test --settings server.conf.settings tests/ -x` passes (full suite including all existing tests)
</verification>

<success_criteria>
- test_dialogue.py covers NPC-01 (context injection), NPC-02 (Standing variation), NPC-03 (interface stability), D-04 (hints), D-05 (extraction)
- test_crafting.py covers D-15 (quality variance), D-16 (recipe discovery), D-17 (three professions)
- All tests pass individually and as part of the full test suite
- No regressions in existing tests
</success_criteria>

<output>
After completion, create `.planning/phases/06c-npc-dialogue-and-crafting/06c-05-SUMMARY.md`
</output>
