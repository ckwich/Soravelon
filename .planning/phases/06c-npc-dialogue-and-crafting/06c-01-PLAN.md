---
phase: 06c-npc-dialogue-and-crafting
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - world/models.py
  - world/migrations/0005_knowntopicrecord_characterrecipe.py
  - world/dialogue_definitions.py
  - world/dialogue_engine.py
autonomous: true
requirements: [NPC-01, NPC-02, NPC-03]
must_haves:
  truths:
    - "Standing tier derived from disposition float maps correctly to 8 tier strings"
    - "Topic priority stack resolves first matching condition from quest_complete down to default"
    - "Keyword extraction finds topics via direct match, synonym, partial word, or returns None for fallback"
    - "Dynamic hints filtered by Standing tier, quest state, and world-state dimensions"
    - "Context packet from get_character_context_packet() drives all condition checks"
  artifacts:
    - path: "world/dialogue_definitions.py"
      provides: "TOPIC_SYNONYMS, RESPONSE_PRIORITY, STANDING_TIER_THRESHOLDS, MAX_HINTS_DISPLAYED"
      exports: ["TOPIC_SYNONYMS", "RESPONSE_PRIORITY", "STANDING_TIER_THRESHOLDS", "MAX_HINTS_DISPLAYED"]
    - path: "world/dialogue_engine.py"
      provides: "Core dialogue logic: greetings, topics, hints, keyword extraction, ambient tick"
      exports: ["resolve_greeting", "resolve_topic_response", "get_npc_hints", "extract_topic", "get_standing_tier", "ambient_npc_tick", "fire_npc_reactive_echo"]
    - path: "world/models.py"
      provides: "KnownTopicRecord and CharacterRecipe Django models"
      contains: "class KnownTopicRecord"
    - path: "world/migrations/0005_knowntopicrecord_characterrecipe.py"
      provides: "Django migration for new models"
  key_links:
    - from: "world/dialogue_engine.py"
      to: "world/world_state.py"
      via: "get_character_context_packet() lazy import"
      pattern: "get_character_context_packet"
    - from: "world/dialogue_engine.py"
      to: "world/mob_disposition.py"
      via: "get_mob_disposition() for Standing tier"
      pattern: "get_mob_disposition"
    - from: "world/dialogue_engine.py"
      to: "world/dialogue_definitions.py"
      via: "imports RESPONSE_PRIORITY, TOPIC_SYNONYMS, STANDING_TIER_THRESHOLDS"
      pattern: "from world.dialogue_definitions import"
---

<objective>
Build the NPC dialogue data layer and core engine. This creates the Django models for topic tracking and recipe discovery, the static definitions (synonym dict, priority stack, tier thresholds), and the dialogue engine that resolves greetings, topics, hints, and keyword extraction.

Purpose: All dialogue commands and crafting commands depend on these models and engine functions. This is the foundation layer.
Output: world/dialogue_definitions.py, world/dialogue_engine.py, KnownTopicRecord + CharacterRecipe models with migration
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/06c-npc-dialogue-and-crafting/06c-CONTEXT.md
@.planning/phases/06c-npc-dialogue-and-crafting/06C-RESEARCH.md

@world/models.py
@world/mob_disposition.py
@world/world_state.py
@world/skill_engine.py

<interfaces>
<!-- Key types and contracts the executor needs -->

From world/world_state.py:
```python
def get_character_context_packet(character, npc=None, zone=None):
    """Build the context dict consumed by the NPC template system."""
    # Returns dict with: ancestry, primary_domain, secondary_domain, guild, subclass,
    # reputation, network, bond, legacy, attunement, standing, trust, betrayal_flag,
    # zone_attunement, companion_present, companion_type, companion_tier
```

From world/mob_disposition.py:
```python
def get_mob_disposition(mob, character):
    """Compute mob's disposition toward character. Returns float -1.0 to +1.0."""

def get_mob_behavior(mob, character):
    """Translate disposition to behavior string."""
```

From world/world_state.py:
```python
def get_standing(character, faction_id):
    """Return standing integer for character with faction."""

def get_trust(character, faction_id):
    """Return trust integer for character with faction."""

def get_betrayal(character, faction_id):
    """Get betrayal flag. False if no record."""
```
</interfaces>

Canonical NPC dialogue spec: C:\Obsidian\brain\Soravelon\soravelon-dialogue.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Django models + migration</name>
  <files>world/models.py, world/migrations/0005_knowntopicrecord_characterrecipe.py</files>
  <action>
Add two new Django models to world/models.py per D-13 and D-16:

**KnownTopicRecord** (per research Example 3):
- character: ForeignKey to "objects.ObjectDB", CASCADE, related_name="known_topics"
- npc_id: CharField(max_length=128)
- topic_key: CharField(max_length=128)
- context_hash: CharField(max_length=64, blank=True, default="") — for hint re-surfacing when context changes
- learned_at: DateTimeField(auto_now_add=True)
- Meta: unique_together = ("character", "npc_id", "topic_key"), index on ("character", "npc_id")

**CharacterRecipe** (per research Example 3):
- character: ForeignKey to "objects.ObjectDB", CASCADE, related_name="known_recipes"
- recipe_id: CharField(max_length=128)
- learned_from: CharField(max_length=64, blank=True, default="") — source of recipe (trainer NPC id, recipe item, "default")
- learned_at: DateTimeField(auto_now_add=True)
- Meta: unique_together = ("character", "recipe_id"), index on ("character_id", "recipe_id")

Follow existing model patterns exactly (see FactionStanding, CharacterSkill, CharacterAbility for reference).

Then run `evennia migrate` or `python manage.py makemigrations world` to generate the migration file. Migration number should be 0005 (after 0004 which added SpawnRecord and CharacterAbility).
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.models import KnownTopicRecord, CharacterRecipe; print('Models importable')"</automated>
  </verify>
  <done>Both models exist in world/models.py, migration file generated, models importable without error</done>
</task>

<task type="auto">
  <name>Task 2: Dialogue definitions + dialogue engine</name>
  <files>world/dialogue_definitions.py, world/dialogue_engine.py</files>
  <action>
**world/dialogue_definitions.py** — Static data module (no Django imports, no side effects):

Per D-02, D-03, D-05, D-14 and research patterns:

```python
MAX_HINTS_DISPLAYED = 4  # Claude's discretion: 4 balances info vs clutter

STANDING_TIER_THRESHOLDS = [
    (0.8, "exalted"),
    (0.6, "honored"),
    (0.4, "friendly"),
    (0.2, "acknowledged"),
    (-0.2, "neutral"),
    (-0.4, "unfriendly"),
    (-0.6, "hostile"),
]
# Below -0.6 = "hostile". Betrayal checked separately before disposition.

RESPONSE_PRIORITY = [
    "quest_complete", "quest_failed", "quest_active",
    "betrayal",
    "exalted", "honored", "friendly", "acknowledged",
    "suspicious", "unfriendly", "hostile",
    "scholar_present", "warden_present", "dragon_present",
    "network_high", "reputation_high",
    "default",
]

TOPIC_SYNONYMS = {
    "wolves": ["wolf", "pack", "animals", "beasts", "creatures"],
    "node": ["magic", "ruins", "glow", "strange", "old magic", "failing", "eight"],
    "work": ["job", "quest", "help", "hire", "pay", "coin", "task", "need"],
    "guilds": ["poachers", "children of men", "hunters", "criminals"],
    "empire": ["imperial", "soldiers", "emperor", "throne"],
    "wardens": ["dragon wardens", "protection", "law"],
    "dragons": ["dragon", "beast", "flying", "scaled"],
    "trade": ["buy", "sell", "goods", "wares", "merchant", "shop"],
    "rumors": ["rumor", "news", "gossip", "heard", "word"],
}

# Dimension thresholds for hint/response conditions
NETWORK_HINT_THRESHOLD = 40
REPUTATION_HINT_THRESHOLD = 40
```

**world/dialogue_engine.py** — Core dialogue logic module. All functions use lazy imports to avoid circular dependencies (Pitfall 6). Follow `(bool, str)` return tuple pattern where applicable.

Functions to implement:

1. `get_standing_tier(character, npc)` — Per research Pattern 1. Check betrayal first via `get_betrayal()`, then map `get_mob_disposition()` float to tier string using STANDING_TIER_THRESHOLDS. Returns one of 8 tier strings.

2. `resolve_greeting(npc, character)` — Read `npc.db.dialogue_greeting_tiers or {}`, get standing tier, return greeting text at that tier. Falls back to "neutral" then generic fallback if tier not authored. Returns `(str, str)` = (greeting_text, tier_used).

3. `_build_dialogue_context(npc, character)` — Lazy import `get_character_context_packet` from world_state. Call it with npc and zone args. Add quest state fields (stub: `active_quests=[]`, `completed_quests=[]`). This is the condition check source for NPC-03 — same interface future LLM will consume.

4. `_check_condition(condition, context)` — Map condition strings to context checks:
   - "betrayal" -> context["betrayal_flag"]
   - "exalted"/"honored"/etc -> context standing tier matches
   - "quest_active"/"quest_complete"/"quest_failed" -> check quest state (stub returns False)
   - "scholar_present" -> context["primary_domain"] == "scholar" or context["subclass"] contains "scholar"
   - "warden_present" -> context["guild"] == "wardens" or similar
   - "dragon_present" -> context["companion_type"] == "dragon"
   - "network_high" -> context["network"] > NETWORK_HINT_THRESHOLD
   - "reputation_high" -> context["reputation"] > REPUTATION_HINT_THRESHOLD
   - "default" -> always True

5. `resolve_topic_response(npc, character, topic_key)` — Per research Pattern 2 and D-03. Read `npc.db.dialogue_topics or {}`, get topic data, iterate RESPONSE_PRIORITY checking conditions. Returns `(text, condition_key)` or `(None, None)` if topic not found.

6. `get_npc_hints(npc, character)` — Per vault spec hint selection logic and D-04. Collect base_hints, tier_hints, quest_hints, network_hints, scholar_hints, warden_hints from NPC db attributes. Filter already-known topics via KnownTopicRecord. Cap at MAX_HINTS_DISPLAYED (4). Returns list of topic key strings.

7. `record_topic_learned(character, npc_id, topic_key, context)` — Create or update KnownTopicRecord. Store a context_hash derived from relevant context fields so hints re-surface when context changes (per research discretion recommendation).

8. `extract_topic(text, available_topics)` — Per research Pattern 3 and D-05. 4-stage pipeline: direct match (longest first, handle underscores as spaces) -> synonym match via TOPIC_SYNONYMS -> partial word match (words > 2 chars from underscore-split) -> None.

9. `has_available_quest(npc, character)` — Stub that returns False. Interface ready for quest system.

10. `get_quest_offer(npc, character)` — Stub that returns None. Interface ready for quest system.

11. `ambient_npc_tick()` — Global ambient ticker callback per research Pattern 4. Iterate all rooms that have NPC objects with ambient data. For each NPC, check `npc.ndb.next_echo_at` timestamp. If elapsed, pick random idle echo from `npc.db.ambient_idle_echoes`, send to room (only if room has connected characters per Pitfall 5), set next_echo_at = now + interval +/- variance. Skip NPCs in rooms with no players.

12. `fire_npc_reactive_echo(room, trigger_type)` — Find NPCs in room, check their `npc.db.ambient_reactive_echoes` dict for the trigger_type key, send echo to room if found.

NPC db attribute naming convention (set by AreaBuilder):
- `npc.db.dialogue_greeting_tiers` — dict {tier: text}
- `npc.db.dialogue_topics` — dict {topic_key: {condition: text}}
- `npc.db.dialogue_base_hints` — list of topic keys
- `npc.db.dialogue_tier_hints` — dict {tier: [topic_keys]}
- `npc.db.dialogue_quest_hints` — dict {quest_id: [topic_keys]}
- `npc.db.dialogue_network_hints` — list of topic keys
- `npc.db.dialogue_scholar_hints` — list of topic keys
- `npc.db.dialogue_warden_hints` — list of topic keys
- `npc.db.ambient_idle_echoes` — list of strings
- `npc.db.ambient_idle_interval` — int seconds
- `npc.db.ambient_idle_variance` — int seconds
- `npc.db.ambient_reactive_echoes` — dict {trigger: text}
- `npc.db.is_npc` — True
- `npc.db.faction` — already exists on mobs

Use `obj.db.attr or fallback` pattern everywhere (no getattr trap).
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.dialogue_definitions import TOPIC_SYNONYMS, RESPONSE_PRIORITY, STANDING_TIER_THRESHOLDS, MAX_HINTS_DISPLAYED; from world.dialogue_engine import resolve_greeting, resolve_topic_response, get_npc_hints, extract_topic, get_standing_tier, ambient_npc_tick, fire_npc_reactive_echo; print('All imports OK')"</automated>
  </verify>
  <done>dialogue_definitions.py exports all constants. dialogue_engine.py exports all 12 functions. All use lazy imports, follow (bool, str) pattern where applicable, consume context packet per NPC-03, and handle the full vault spec priority stack per D-03.</done>
</task>

</tasks>

<verification>
- `from world.models import KnownTopicRecord, CharacterRecipe` succeeds
- `from world.dialogue_definitions import TOPIC_SYNONYMS, RESPONSE_PRIORITY` succeeds
- `from world.dialogue_engine import resolve_greeting, extract_topic, get_standing_tier` succeeds
- Migration file exists and is syntactically valid
- No circular import errors on any import
</verification>

<success_criteria>
- KnownTopicRecord and CharacterRecipe models exist with correct fields, constraints, and indexes
- Migration generated and applies cleanly
- dialogue_definitions.py contains TOPIC_SYNONYMS, RESPONSE_PRIORITY, STANDING_TIER_THRESHOLDS, MAX_HINTS_DISPLAYED
- dialogue_engine.py contains all 12 functions with correct signatures
- Standing tier mapping produces correct tier string for each disposition range
- extract_topic pipeline handles all 4 stages (direct, synonym, partial, None)
- All imports use lazy pattern inside functions
</success_criteria>

<output>
After completion, create `.planning/phases/06c-npc-dialogue-and-crafting/06c-01-SUMMARY.md`
</output>
