# Phase 06c: NPC Dialogue & Crafting - Research

**Researched:** 2026-03-26
**Domain:** NPC dialogue system (keyword-based topics, greeting tiers, hints, ambient behavior) + crafting framework (recipe registry, quality variance, crafting commands)
**Confidence:** HIGH

## Summary

This phase builds two complementary systems: NPC dialogue that makes NPCs feel like inhabitants rather than quest kiosks, and a crafting framework that gives players agency in item creation. Both systems are comprehensively specified in vault documents, leaving minimal ambiguity.

The NPC dialogue system is keyword-based with contextual depth: greeting tiers from disposition floats, topic response nodes with a priority stack, dynamic hint filtering, synonym-based keyword extraction, and quest offer integration. The existing `get_mob_disposition()` + `get_standing()` + `get_character_context_packet()` functions provide all the data needed to drive dialogue selection. The AreaBuilder already has an `npc()` method and `npc_definitions` list on rooms, plus `room.db.ambient_echoes` for idle echo support.

The crafting framework implements a recipe registry with skill-based quality variance. Three crafting professions (Cooking, Smithing, Alchemy) produce items on a Flawed-to-Masterwork quality gradient. The existing `world/skill_engine.py` and `world/skill_definitions.py` already define all four crafting skills (cooking, smithing, alchemy, engineering) with thresholds and diminishing returns. Two new Django models (KnownTopicRecord, CharacterRecipe) are needed.

**Primary recommendation:** Build dialogue engine as a pure `world/dialogue_engine.py` module following the thin-typeclass-delegates-to-world pattern. Store NPC dialogue data as `db` attributes on NPC objects (set via AreaBuilder DSL extensions). Crafting engine goes in `world/crafting_engine.py` with a static `RECIPE_REGISTRY` dict and a `CharacterRecipe` Django model for discovery tracking.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Keyword-based topic dialogue per vault spec. Player commands: talk/greet (greeting + hints), ask about <topic> (topic query), say (freeform broadcast, keyword extraction), tell <npc> (directed say). accept/decline for quest offers.
- **D-02:** Standing-tier greetings: hostile, unfriendly, neutral, acknowledged, friendly, honored, exalted, betrayal. Template system selects tier from Standing + Trust. Dialogue system provides text at that tier.
- **D-03:** Topic response nodes with priority stack: quest_complete > quest_failed > quest_active > betrayal > exalted > honored > ... > scholar_present > warden_present > dragon_present > network_high > reputation_high > default. First match wins. Every topic MUST have a default response.
- **D-04:** Dynamic hint system. After every greeting, available hints display in brackets. Hints are dynamic per player (filtered by Standing tier, active quests, world-state dimensions, class/profession). Only non-zero skills shown. Capped at readable number (research determines 3-5).
- **D-05:** Keyword extraction: direct topic match -> synonym matching (TOPIC_SYNONYMS static dict) -> partial match -> generic fallback showing available topics.
- **D-06:** Quest offers appear inline with dialogue. accept/decline commands. Quest offer trigger: NPC has quest available + player doesn't have it active + meets prerequisites + appropriate Standing tier.
- **D-07:** Build exactly as documented in vault. Interesting additions from Claude are welcome.
- **D-08:** Idle echoes: minimum 4 per NPC, fired on timer with variance (base +/- variance seconds). Per vault spec.
- **D-09:** Reactive echoes: fire from zone state change hooks (combat_nearby, node_active, quest_complete, player_enters, etc.).
- **D-10:** Ambient architecture: Claude decides between single global ambient ticker vs per-NPC TickerHandler subscriptions based on performance analysis.
- **D-11:** NPCDialogueDefinition: greeting_tiers dict, topics dict (topic_key -> {condition: text}), base_hints, tier_hints, quest_hints, network_hints, scholar_hints, warden_hints.
- **D-12:** NPCAmbientDefinition: idle_echoes list, idle_interval, idle_variance, reactive_echoes dict.
- **D-13:** KnownTopicRecord: Django model tracking which topics each character has learned from each NPC (for hint suppression).
- **D-14:** TOPIC_SYNONYMS: static Python dict, authored globally (not per NPC). "wolf" maps to "wolves" for every NPC.
- **D-15:** Recipe system with quality variance from skill level. Recipes define required ingredients + skill level + output item. Quality/success based on skill check -- even with the recipe you can still fail ("burn the food").
- **D-16:** Static recipe registry + discovery. Some recipes known by default (basic cooking). Others require finding recipe items in world or learning from trainers. CharacterRecipe model tracks which recipes each character knows.
- **D-17:** Three crafting professions with basic output: Cooking (makes food -- HP regen consumables), Smithing (repairs equipment, basic weapons/armor), Alchemy (craft) (makes potions, reagents).
- **D-18:** Engineering (craft) is SEPARATE from Engineering domain. Craft skill = gear repair, device building. Domain = combat companion, traps. Non-Engineers can repair their own gear.
- **D-19:** Crafting commands: craft <recipe>, cook <recipe>, smith <recipe>, brew <recipe>. Each requires appropriate station/location (campfire for cooking, forge for smithing, etc.).

### Claude's Discretion
- MAX_HINTS_DISPLAYED value (3-5)
- Known topic persistence strategy (persist vs session-reset)
- Ambient ticker architecture (global vs per-NPC)
- Multi-NPC room response behavior (how many NPCs respond to 'say')
- Recipe quality formula details
- Crafting station implementation (room tag? object in room?)
- Crafting time mechanic (instant? short delay?)

### Deferred Ideas (OUT OF SCOPE)
- LLM-driven NPC responses -- future feature per vault doc
- NPC conversation memory -- future feature (Standing/Trust provides implicit memory)
- NPC-to-NPC dialogue (ambient eavesdropping) -- content phase
- Full recipe list -- content authoring phase
- Advanced crafting (enchanting, upgrading, material quality) -- dedicated crafting expansion
- Merchant buy/sell command set -- separate economy phase or inline
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| NPC-01 | NPC template system injects world-state variables into dialogue | `get_character_context_packet()` already builds the full context dict (Standing, Trust, betrayal, dimensions, ancestry, guild, companion). Dialogue engine consumes this packet for priority stack condition checks. |
| NPC-02 | NPCs respond differently based on character standing, ancestry, and reputation | Disposition float from `get_mob_disposition()` maps to Standing tier. Priority stack checks quest_state > betrayal > standing_tier > class/profession > dimension thresholds > default. All inputs available from existing code. |
| NPC-03 | Context packet feeds NPC templates (same interface as future LLM consumer) | `get_character_context_packet()` in `world/world_state.py` is the canonical packet. Dialogue engine reads it; future LLM system will read the same packet. Interface stability is critical. |
| SKL-03 | Animal Handling skill track (0-100) with Dragon Handling unlock at 100 | Already implemented in `world/skill_definitions.py` (animal_handling entry) and `world/skill_engine.py`. No work needed for this requirement. Crafting skills (cooking, smithing, alchemy, engineering) are also already defined. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia 6.0 | 6.0.0 | MUD engine: commands, typeclasses, TICKER_HANDLER | Project foundation -- locked |
| Django ORM | 6.0.3 | Models for KnownTopicRecord, CharacterRecipe | Existing model layer |
| Python 3.12 | 3.12.10 | All game logic | Project runtime |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Evennia TICKER_HANDLER | built-in | Ambient NPC idle echo timer | Global ambient ticker |
| world/skill_engine.py | existing | Crafting skill checks for quality variance | Every craft attempt |
| world/mob_disposition.py | existing | Standing tier derivation for dialogue | Every greeting |
| world/world_state.py | existing | Context packet, Standing/Trust queries | Every dialogue interaction |
| world/oob_publisher.py | existing | Push quest accept/decline to client | Quest offer flow |
| world/action_vocabulary.py | existing | `open_dialogue` stub already registered | Trigger-driven dialogue |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| db attributes for NPC dialogue | Separate Django model | db attributes are simpler, match existing pattern (spawn_definitions, npc_definitions stored on room.db). No join needed at query time. |
| Global ambient ticker | Per-NPC TickerHandler subscription | See Architecture Patterns -- global wins on performance |
| Static RECIPE_REGISTRY dict | Django model for recipes | Static dict matches SKILL_DEFINITIONS, ABILITIES, ANCESTRY_TRAITS pattern. Recipes are authored content, not player-generated. |

## Architecture Patterns

### Recommended Project Structure
```
world/
  dialogue_engine.py      # Core dialogue logic: greeting, topic query, hint generation, keyword extraction
  dialogue_definitions.py # TOPIC_SYNONYMS dict, RESPONSE_PRIORITY list, Standing tier mapping constants
  crafting_engine.py      # Recipe lookup, quality calculation, craft execution, discovery tracking
  crafting_definitions.py # RECIPE_REGISTRY dict, quality tier constants, station requirements
  models.py               # Add KnownTopicRecord, CharacterRecipe models
  area_builder.py         # Extend npc() with dialogue and ambient kwargs
  oob_publisher.py        # Add push_dialogue_update() for quest offers
  action_vocabulary.py    # Implement open_dialogue handler (currently stub)
commands/
  cmd_dialogue.py         # CmdTalk, CmdAsk, CmdSay (override), CmdTell, CmdAccept, CmdDecline
  cmd_crafting.py         # CmdCraft, CmdCook, CmdSmith, CmdBrew, CmdRecipes
  default_cmdsets.py      # Register new commands
typeclasses/
  characters.py           # Add ndb.pending_quest_offer for accept/decline state
```

### Pattern 1: Disposition Float to Standing Tier Mapping
**What:** Map the continuous disposition float (-1.0 to +1.0) to a discrete Standing tier string for greeting selection.
**When to use:** Every `talk`/`greet` command, and as a condition check key in the topic priority stack.
**Rationale:** The vault spec defines 8 tiers. The disposition system already has threshold constants. The mapping must be deterministic and consistent between greeting selection and topic priority checks.

```python
# world/dialogue_definitions.py

STANDING_TIER_THRESHOLDS = [
    # (min_disposition, tier_string)
    # Checked top-down, first match wins
    (0.8, "exalted"),
    (0.6, "honored"),
    (0.4, "friendly"),
    (0.2, "acknowledged"),
    (-0.2, "neutral"),
    (-0.4, "unfriendly"),
    (-0.6, "hostile"),
]

# betrayal is a separate flag, checked before disposition
def get_standing_tier(character, npc):
    """
    Derive standing tier string from disposition + betrayal.
    Returns one of: hostile, unfriendly, neutral, acknowledged,
    friendly, honored, exalted, betrayal.
    """
    from world.world_state import get_betrayal
    faction_id = npc.db.faction
    if faction_id and get_betrayal(character, faction_id):
        return "betrayal"

    from world.mob_disposition import get_mob_disposition
    disposition = get_mob_disposition(npc, character)

    for threshold, tier in STANDING_TIER_THRESHOLDS:
        if disposition >= threshold:
            return tier
    return "hostile"  # below all thresholds
```

### Pattern 2: Topic Priority Stack Resolution
**What:** For a given topic, check conditions in priority order and return the first matching response text.
**When to use:** Every `ask about <topic>` command.

```python
# world/dialogue_engine.py

RESPONSE_PRIORITY = [
    "quest_complete",
    "quest_failed",
    "quest_active",
    "betrayal",
    "exalted",
    "honored",
    "friendly",
    "acknowledged",
    "suspicious",
    "unfriendly",
    "hostile",
    "scholar_present",
    "warden_present",
    "dragon_present",
    "network_high",
    "reputation_high",
    "default",
]

def resolve_topic_response(npc, character, topic_key):
    """
    Given an NPC's topic dict and a character, resolve which
    response text to return using the priority stack.
    Returns (text, condition_matched) or (fallback_text, "default").
    """
    topics = npc.db.dialogue_topics or {}
    topic_data = topics.get(topic_key)
    if not topic_data:
        return None, None

    context = _build_dialogue_context(npc, character)

    for condition in RESPONSE_PRIORITY:
        if condition not in topic_data:
            continue
        if _check_condition(condition, context):
            return topic_data[condition], condition

    # Should never reach here if every topic has "default"
    return topic_data.get("default", "I don't know much about that."), "default"
```

### Pattern 3: Keyword Extraction Pipeline
**What:** Extract topic keys from freeform player text using a 4-stage pipeline.
**When to use:** `say` and `tell` commands.

```python
# world/dialogue_engine.py

def extract_topic(text, available_topics):
    """
    Extract best-matching topic from freeform text.
    Pipeline: direct match -> synonym -> partial word -> None (fallback).
    """
    text_lower = text.lower()

    # Stage 1: Direct topic match (longest match first to avoid "node" matching before "node_reading")
    for topic in sorted(available_topics, key=len, reverse=True):
        if topic.replace("_", " ") in text_lower or topic in text_lower:
            return topic

    # Stage 2: Synonym matching
    from world.dialogue_definitions import TOPIC_SYNONYMS
    for topic, synonyms in TOPIC_SYNONYMS.items():
        if topic in available_topics:
            if any(syn in text_lower for syn in synonyms):
                return topic

    # Stage 3: Partial word match (split on underscores)
    for topic in available_topics:
        words = topic.split("_")
        if any(word in text_lower for word in words if len(word) > 2):
            return topic

    return None  # triggers fallback with topic list
```

### Pattern 4: Global Ambient Ticker (Recommended)
**What:** Single global ticker that iterates all NPC-populated rooms and fires idle echoes for NPCs whose interval has elapsed.
**When to use:** Always. This is the recommended ambient architecture (D-10).

**Performance Analysis:**

Per-NPC TickerHandler subscription:
- Each NPC registers with TICKER_HANDLER at its own interval
- 50 NPCs across 4 starter zones = 50 separate timer entries
- Each fires independently, each callback does a room lookup + echo
- Evennia's TICKER_HANDLER uses a heap-based scheduler -- 50 entries is fine
- BUT: on server reload, all 50 re-register. On zone load, N registrations.
- Scaling concern: 500+ NPCs at content push = 500 timer entries

Global ambient ticker:
- One TICKER_HANDLER entry at 15-second interval
- Callback iterates rooms with NPCs, checks per-NPC last_echo timestamp
- One callback, predictable load, O(rooms_with_NPCs) per tick
- NPC interval variance handled by per-NPC `ndb.next_echo_at` timestamp
- Scales linearly with NPC count but only one timer entry
- Easy to pause/resume (one ticker to manage)

**Recommendation: Global ambient ticker at 15-second interval.** Reasons:
1. Matches existing pattern (node_failure_tick, spawn_tick are global tickers)
2. Single point of control for pause/debug
3. Better scaling behavior at 500+ NPCs
4. Simpler lifecycle management (no per-NPC register/unregister on zone load)
5. 15-second tick with per-NPC jitter achieves the same variance as individual timers

```python
# Registered in at_server_start():
TICKER_HANDLER.add(
    interval=15,
    callback="world.dialogue_engine.ambient_npc_tick",
    idstring="npc_ambient_tick",
    persistent=True,
)
```

### Pattern 5: Crafting Quality Formula
**What:** Compute item quality tier from skill level vs recipe difficulty with random variance.
**When to use:** Every craft attempt.

```python
# world/crafting_engine.py

import random

QUALITY_TIERS = ["flawed", "standard", "fine", "superior", "masterwork"]

def calculate_craft_quality(skill_value, recipe_difficulty, has_station_bonus=False):
    """
    Determine crafted item quality from skill vs difficulty.

    skill_value: 0-100 (from CharacterSkill)
    recipe_difficulty: 0-100 (from recipe definition)
    has_station_bonus: True if crafting at advanced/ancient station

    Returns quality tier string.
    """
    gap = skill_value - recipe_difficulty  # positive = crafter above recipe

    # Base quality index (0-4 mapping to QUALITY_TIERS)
    if gap >= 30:
        base = 3  # superior floor
    elif gap >= 10:
        base = 2  # fine floor
    elif gap >= -10:
        base = 1  # standard floor
    else:
        base = 0  # flawed floor

    # Random variance: +/- 1 tier, weighted toward center
    variance = random.choices([-1, 0, 0, 0, 1], k=1)[0]

    # Station bonus: +1 ceiling
    station_bonus = 1 if has_station_bonus else 0

    final_index = max(0, min(4, base + variance + station_bonus))
    return QUALITY_TIERS[final_index]
```

### Pattern 6: Crafting Station Implementation
**What:** Crafting stations identified by room tag.
**Recommendation:** Room tags. Simpler than placing objects, queryable via `room.tags.has()`.

```python
# Room tag approach:
# room.tags.add("crafting_campfire", category="crafting_station")
# room.tags.add("crafting_forge", category="crafting_station")
# room.tags.add("crafting_alchemy_bench", category="crafting_station")

# In AreaBuilder:
# area.room("room_001", ..., crafting_stations=["campfire", "forge"])

# In crafting_engine:
def check_station(character, required_station):
    room = character.location
    if not room:
        return False, "You need to be somewhere to craft."
    return room.tags.has(f"crafting_{required_station}", category="crafting_station"), \
           f"You need a {required_station} to craft this."
```

### Anti-Patterns to Avoid
- **Storing dialogue in Django models:** NPC dialogue is authored content, not player-generated relational data. Storing it in Django models adds complexity (joins, migrations) with no benefit. Use `db` attributes on NPC objects, set by AreaBuilder. KnownTopicRecord is the exception -- it IS relational (character x NPC x topic).
- **Hardcoding NPC responses in commands:** All dialogue text lives in data (NPC db attributes). Commands call `dialogue_engine` which reads data. No text in command files.
- **Per-NPC TickerHandler for ambient:** Creates lifecycle management burden and scaling issues. Use global ticker.
- **Bypassing context packet for dialogue conditions:** Always use `get_character_context_packet()` as the data source for condition checks. This preserves the LLM interface contract (NPC-03).
- **Direct character.msg() for OOB:** Quest accept/decline state push must go through `oob_publisher.py` per project convention.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Standing tier derivation | Custom Standing query | `get_mob_disposition()` + threshold mapping | Disposition already includes Standing, ancestry, reputation, trust. Re-deriving from raw Standing alone would miss these inputs. |
| Context packet | Custom data gathering per dialogue check | `get_character_context_packet()` | Already exists, tested, and is the LLM interface contract |
| Skill value queries | Direct DB queries | `get_skill_value()` from skill_engine | Handles lazy creation, returns 0.0 for missing |
| Synonym matching | NLP library or regex | Static TOPIC_SYNONYMS dict | Per vault spec. Simple, predictable, authorable |
| Idle echo timing | Custom timer implementation | TICKER_HANDLER + ndb.next_echo_at timestamps | Evennia's built-in scheduling is battle-tested |

**Key insight:** The dialogue system is data-driven, not logic-driven. The engine is thin -- it reads NPC data, checks conditions against the context packet, and returns text. The creative work is in authoring the NPC data, not building the engine.

## Discretion Recommendations

### MAX_HINTS_DISPLAYED: 4
**Rationale:** 3 feels limiting for NPCs with quest + lore + faction content. 5 creates visual clutter. 4 gives room for 1 quest hint + 2 lore hints + 1 contextual hint, which covers most NPC interactions without overwhelming the player.

### Known Topic Persistence: Persist, re-surface on state change
**Rationale:** Per vault suggestion. Persisting known topics (via KnownTopicRecord) prevents hint spam on repeated visits. But when quest state changes (completion, new quest available), related hints should re-appear. Implementation: KnownTopicRecord has a `context_hash` field -- when the context that generated the hint changes, the record is considered stale and the hint re-surfaces.

### Multi-NPC Room Say Response: Max 2 responding NPCs
**Rationale:** Per vault suggestion. When player types `say wolves` in a room with 3 NPCs, only NPCs with "wolves" in their topic tree respond. Cap at 2 responses to prevent spam. Prioritize by: (1) NPC with best Standing tier, (2) first NPC found.

### Crafting Time: Short delay (2-3 seconds)
**Rationale:** Instant feels too game-y for a MUD that values immersion. Long delays are tedious for batch crafting. A 2-3 second delay with a flavor echo ("You work the metal...") provides immersion without frustration. Implemented as a simple `utils.delay()` call, not a script.

### Crafting Station: Room tags (not objects)
**Rationale:** Simpler than placing invisible objects. Room tags are already used extensively (zone_id, room_type, node_layer). Adding `crafting_station` category is consistent. AreaBuilder sets tags in `room()` kwargs.

## Common Pitfalls

### Pitfall 1: Evennia Default `say` Command Conflict
**What goes wrong:** Evennia provides a default `CmdSay` in `evennia.commands.default.general` with key `"say"` and aliases `["'", '"']`. Adding a custom `CmdSay` without proper priority will either shadow the default (losing basic say functionality) or be shadowed by it.
**Why it happens:** The CharacterCmdSet inherits from `default_cmds.CharacterCmdSet` which includes the default say.
**How to avoid:** Override the default say entirely in `CharacterCmdSet`. The custom `CmdSay` should handle both the normal say broadcast AND keyword extraction for NPC dialogue. If no NPC matches, fall back to the standard room broadcast behavior.
**Warning signs:** Players can't say things to the room, or NPCs never respond to `say`.

### Pitfall 2: SaverDict Copy Pattern for NPC db Attribute Mutation
**What goes wrong:** Modifying nested dicts/lists stored on `npc.db.dialogue_topics` without the copy-modify-reassign pattern causes silent data loss.
**Why it happens:** Evennia's SaverDict doesn't detect nested mutations.
**How to avoid:** Never mutate NPC db attributes in-place. For hint suppression updates, use `KnownTopicRecord` model (not db attribute mutation).
**Warning signs:** NPC dialogue data reverts after server restart.

### Pitfall 3: `getattr(obj.db, 'attr', default)` Trap
**What goes wrong:** Using `getattr(character.db, 'some_attr', fallback)` returns the fallback even when the attribute exists but is falsy (0, None, empty string).
**Why it happens:** Evennia `db` is not a real Python object with `__getattr__`. Per CLAUDE.md: always use `obj.db.attr or fallback` pattern.
**How to avoid:** Follow project convention: `npc.db.dialogue_topics or {}`, `npc.db.greeting_tiers or {}`.
**Warning signs:** NPCs with empty-string greetings get the fallback text instead.

### Pitfall 4: Pending Quest Offer State Leak
**What goes wrong:** Player gets a quest offer from NPC A, walks to NPC B, types `accept`, and accepts NPC A's quest at NPC B's location.
**Why it happens:** `character.ndb.pending_quest_offer` persists across rooms.
**How to avoid:** Clear `pending_quest_offer` on room change (`at_after_move`) and on any non-accept/decline command. Also validate that the offering NPC is still in the same room when `accept` fires.
**Warning signs:** Quest accepted message references wrong NPC.

### Pitfall 5: Ambient Ticker Sending to Empty Rooms
**What goes wrong:** Idle echoes fire in rooms with no players, wasting cycles.
**Why it happens:** Global ticker iterates all NPC rooms, not just occupied ones.
**How to avoid:** Check `room.contents` for connected characters before sending echo. Only compute and send if at least one player session is active in the room.
**Warning signs:** Increased server load with zero players online.

### Pitfall 6: Circular Import Between dialogue_engine and world_state
**What goes wrong:** `dialogue_engine.py` imports from `world_state.py` which imports from `models.py` at module level, and then a new model that imports something from dialogue creates a cycle.
**Why it happens:** Deep import chains in the `world/` module tree.
**How to avoid:** Use lazy imports inside functions (the established project pattern). `dialogue_engine.py` should import `get_character_context_packet` and `get_mob_disposition` lazily inside the functions that need them.
**Warning signs:** `ImportError` on server start.

### Pitfall 7: Crafting Recipe Discovery Without CharacterRecipe Model
**What goes wrong:** Using character db attributes to track known recipes hits SaverDict performance issues at scale (hundreds of recipes per character).
**Why it happens:** Temptation to avoid a migration by using db attributes.
**How to avoid:** Use `CharacterRecipe` Django model. It's relational data (character x recipe) and follows the same pattern as `CharacterSkill`, `CharacterAbility`, `FactionStanding`.
**Warning signs:** Slow recipe lookups, data corruption on list mutation.

## Code Examples

### Example 1: NPC Dialogue Data on db Attributes (set by AreaBuilder)

```python
# In an area spec file (world/areas/vaels_crossing.py):
def build():
    area = AreaBuilder("vaels_crossing")
    area.zone(name="Vael's Crossing", ...)

    r1 = area.room("town_square", name="Town Square", ...)

    area.npc(r1, "maren_warden",
        faction="wardens",
        # Dialogue definition
        dialogue=dict(
            greeting_tiers={
                "hostile":      "Maren's hand moves to her weapon. 'You need to leave.'",
                "unfriendly":   "Maren eyes you warily but says nothing.",
                "neutral":      "Maren nods briefly. 'Traveler.'",
                "acknowledged": "Maren looks up. 'You again. What brings you out here?'",
                "friendly":     "Maren smiles. 'Good to see a familiar face.'",
                "honored":      "Maren straightens. 'I was hoping you'd come by.'",
                "exalted":      "Maren meets your eyes. 'I'm glad you're here.'",
                "betrayal":     "Maren's expression closes. 'What do you want?'",
            },
            topics={
                "wolves": {
                    "default":        "They've been hitting farms. Too coordinated.",
                    "quest_active":   "How's it going out there?",
                    "quest_complete": "You really came through.",
                    "honored":        "The pack behavior matches a Cognitive node.",
                },
                "work": {
                    "default":        "I could use help with the wolves.",
                    "quest_active":   "You're already on it.",
                    "quest_complete": "You've done more than enough.",
                },
            },
            base_hints=["wolves", "work"],
            tier_hints={"honored": ["node"]},
            quest_hints={},
            network_hints=[],
            scholar_hints=[],
            warden_hints=["patrols"],
        ),
        # Ambient definition
        ambient=dict(
            idle_echoes=[
                "Maren scans the tree line with practiced eyes.",
                "Maren murmurs something to her pack animal.",
                "Maren checks the edge on her blade absently.",
                "Maren pulls her cloak tighter against the chill.",
            ],
            idle_interval=60,
            idle_variance=30,
            reactive_echoes={
                "combat_nearby":  "Maren draws her weapon.",
                "node_active":    "Maren glances toward the glowing ruins.",
            },
        ),
    )
```

### Example 2: AreaBuilder npc() Extension

```python
# world/area_builder.py — extended npc() method

def npc(self, room, npc_id, **kwargs):
    """Place an NPC definition on a room with optional dialogue and ambient data."""
    npc_def = {
        "npc_id": npc_id,
        "wander": kwargs.get("wander", False),
        "quest": kwargs.get("quest"),
        "faction": kwargs.get("faction"),
        "standing_required": kwargs.get("standing_required"),
        # NEW: dialogue and ambient
        "dialogue": kwargs.get("dialogue"),
        "ambient": kwargs.get("ambient"),
    }

    current = list(room.db.npc_definitions or [])
    current.append(npc_def)
    room.db.npc_definitions = current
```

### Example 3: KnownTopicRecord and CharacterRecipe Models

```python
# world/models.py — new models

class KnownTopicRecord(models.Model):
    """
    Tracks which NPC topics a character has already asked about.
    Used for hint suppression (D-13). Re-surfaces hints when context changes.
    """
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="known_topics",
    )
    npc_id = models.CharField(max_length=128)
    topic_key = models.CharField(max_length=128)
    context_hash = models.CharField(max_length=64, blank=True, default="")
    learned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("character", "npc_id", "topic_key")
        indexes = [
            models.Index(fields=["character", "npc_id"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.npc_id}/{self.topic_key}"


class CharacterRecipe(models.Model):
    """
    Tracks which crafting recipes a character has discovered.
    Default recipes are added at character creation or first craft attempt.
    """
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="known_recipes",
    )
    recipe_id = models.CharField(max_length=128)
    learned_from = models.CharField(max_length=64, blank=True, default="")
    learned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("character", "recipe_id")
        indexes = [
            models.Index(fields=["character_id", "recipe_id"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.recipe_id}"
```

### Example 4: Crafting Recipe Registry Entry

```python
# world/crafting_definitions.py

RECIPE_REGISTRY = {
    "trail_rations": {
        "name": "Trail Rations",
        "skill": "cooking",
        "difficulty": 10,
        "station": "campfire",
        "ingredients": [
            {"item_tag": "raw_meat", "quantity": 1},
            {"item_tag": "wild_herb", "quantity": 1},
        ],
        "output": {
            "item_id": "trail_rations",
            "base_item_type": "consumable",
            "effect": {"type": "hp_regen", "amount": 5, "duration": 60},
        },
        "default_known": True,  # all characters know this
        "command": "cook",
    },
    "basic_healing_draught": {
        "name": "Basic Healing Draught",
        "skill": "alchemy",
        "difficulty": 20,
        "station": "alchemy_bench",
        "ingredients": [
            {"item_tag": "thornroot", "quantity": 2},
            {"item_tag": "clean_water", "quantity": 1},
        ],
        "output": {
            "item_id": "healing_draught_basic",
            "base_item_type": "consumable",
            "effect": {"type": "instant_heal", "amount": 25},
        },
        "default_known": False,
        "command": "brew",
    },
}

# Station requirements
STATION_REQUIREMENTS = {
    "campfire": "A campfire or cooking hearth",
    "forge": "A smithing forge",
    "alchemy_bench": "An alchemist's workbench",
    "workbench": "An engineering workbench",
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Menu-driven NPC dialogue | Keyword-based with dynamic hints | Design decision (vault) | More MUD-appropriate, supports future LLM upgrade path |
| Fixed NPC greetings | Disposition-driven tier selection | Phase 4 (disposition system) | NPCs react to relationship, not just presence |
| N/A (no crafting) | Skill-based quality gradient | This phase | First crafting implementation |

**Deprecated/outdated:**
- None -- this is greenfield development on established patterns.

## Open Questions

1. **Quest System Integration**
   - What we know: Quest offer triggers appear in dialogue per D-06. `quest_definitions` are stored on zone objects via AreaBuilder. `action_vocabulary.py` has `set_quest_flag` stub.
   - What's unclear: The quest system itself is not built yet. Quest state tracking (active, complete, failed) needs a model or db attribute pattern. The dialogue system needs to check "does this NPC have an available quest for this player?"
   - Recommendation: Stub quest checking with a simple interface (`has_available_quest(npc, character)` -> bool, `get_quest_offer(npc, character)` -> dict). Implement the stub to return False/None. When quest system is built (content phase), fill in the implementation. This prevents blocking dialogue on quest system completion.

2. **NPC Object Instantiation**
   - What we know: `npc_definitions` are stored as dicts on `room.db`. There are no actual NPC Evennia objects created by the current AreaBuilder `npc()` method -- it just stores the definition.
   - What's unclear: Will NPCs be SoravelonMob objects with `is_npc=True`? Or a separate NPC typeclass? Or virtual (no DB object, just data on the room)?
   - Recommendation: NPCs should be SoravelonMob objects with `npc.db.is_npc = True` and `npc.db.combat_enabled = False`. This lets them appear in room contents (players can `look maren`), carry dialogue data on their `db` attributes, and be targeted by `tell`. The AreaBuilder should create actual NPC objects during `build()`, similar to how it creates rooms. This is the simplest path that supports all dialogue commands.

3. **Reactive Echo Hook Points**
   - What we know: Reactive echoes fire from zone state changes (combat_nearby, node_active, quest_complete, player_enters).
   - What's unclear: Which existing code paths should fire these hooks? Combat system, node tick, trigger engine, `at_after_move`?
   - Recommendation: Define a `fire_npc_reactive_echo(room, trigger_type)` function in `dialogue_engine.py`. Call it from: (a) `at_after_move` for `player_enters`, (b) `combat_script.py` for `combat_nearby`, (c) `node_helpers.py` for `node_active`, (d) trigger engine for `quest_complete`. Each call site adds one line.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest via evennia test runner |
| Config file | none -- `evennia test --settings server.conf.settings tests/` |
| Quick run command | `evennia test --settings server.conf.settings tests/test_dialogue.py -x` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| NPC-01 | Context packet injects world-state variables into dialogue | unit | `evennia test --settings server.conf.settings tests/test_dialogue.py::TestContextPacketInjection -x` | Wave 0 |
| NPC-02 | NPCs respond differently by standing/ancestry/reputation | unit | `evennia test --settings server.conf.settings tests/test_dialogue.py::TestStandingTierResponses -x` | Wave 0 |
| NPC-03 | Context packet interface stable for LLM consumer | unit | `evennia test --settings server.conf.settings tests/test_dialogue.py::TestContextPacketInterface -x` | Wave 0 |
| SKL-03 | Animal Handling skill track | unit | Already exists in tests/test_skills.py | Exists |
| D-05 | Keyword extraction pipeline (direct/synonym/partial/fallback) | unit | `evennia test --settings server.conf.settings tests/test_dialogue.py::TestKeywordExtraction -x` | Wave 0 |
| D-15 | Crafting quality variance from skill level | unit | `evennia test --settings server.conf.settings tests/test_crafting.py::TestCraftQuality -x` | Wave 0 |
| D-16 | Recipe discovery tracking (CharacterRecipe model) | unit | `evennia test --settings server.conf.settings tests/test_crafting.py::TestRecipeDiscovery -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `evennia test --settings server.conf.settings tests/test_dialogue.py tests/test_crafting.py -x`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_dialogue.py` -- covers NPC-01, NPC-02, NPC-03, D-03, D-04, D-05
- [ ] `tests/test_crafting.py` -- covers D-15, D-16, D-17
- [ ] Django migration for KnownTopicRecord and CharacterRecipe models

## Project Constraints (from CLAUDE.md)

- **Thin typeclasses:** All game logic in `world/` modules; typeclasses delegate. Dialogue and crafting engines go in `world/`, commands go in `commands/`.
- **`(bool, str)` return tuples:** All engine functions that can fail follow this pattern. `craft()`, `learn_recipe()`, `resolve_greeting()` should all return `(bool, str)`.
- **SaverDict copy pattern:** Any mutation of db attributes on rooms or NPCs must copy-modify-reassign.
- **F() expressions:** Not applicable to dialogue (no concurrent balance updates), but CharacterRecipe creation should use `get_or_create` for idempotency.
- **Lazy imports:** Use inside functions for cross-module imports to break circular dependencies.
- **No getattr(obj.db, ...):** Always `obj.db.attr or fallback`.
- **OOB through publisher:** Quest accept/decline state must go through `oob_publisher.py`.
- **Tags for classification:** NPCs should get tags for queryset filtering (e.g., `npc` category on character_type tag).
- **Color codes:** Player-facing messages use Evennia color codes: `|g`, `|y`, `|r`, `|w`, `|m`, `|n`.
- **Error messages:** Descriptive and actionable per project convention.
- **Evennia TickerHandler:** Ambient ticker registered in `at_server_startstop.py`.
- **Module naming:** `snake_case.py` for all modules. `dialogue_engine.py`, not `dialogueEngine.py`.
- **Function naming:** Verb-first for engine functions: `resolve_greeting()`, `extract_topic()`, `craft_item()`, `learn_recipe()`.

## Sources

### Primary (HIGH confidence)
- `C:\Obsidian\brain\Soravelon\soravelon-dialogue.md` -- Complete NPC dialogue spec (commands, greeting tiers, topic nodes, priority stack, hints, keyword extraction, quest offers, ambient behavior, data models)
- `C:\Obsidian\brain\Soravelon\soravelon-crafting.md` -- Crafting system spec (quality gradient, material system, recipe framework, stations, breakdown, XP)
- `C:\Obsidian\brain\Soravelon\soravelon-skills.md` -- Skill system spec (crafting proficiencies, attunement, practice mechanics)
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` -- Mob disposition system, faction territory expression, ambient echo context
- Existing codebase: `world/mob_disposition.py`, `world/world_state.py`, `world/skill_engine.py`, `world/skill_definitions.py`, `world/oob_publisher.py`, `world/models.py`, `world/area_builder.py`, `world/action_vocabulary.py`, `commands/default_cmdsets.py`, `typeclasses/characters.py`

### Secondary (MEDIUM confidence)
- [Evennia default CmdSay documentation](https://www.evennia.com/docs/latest/_modules/evennia/commands/default/general.html) -- Default say command class structure (key, aliases, behavior)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries are existing project dependencies, no new packages
- Architecture: HIGH -- follows established patterns (thin typeclass, world/ engine, static registry, Django model)
- Pitfalls: HIGH -- identified from direct codebase analysis and existing project pitfall documentation
- Dialogue system: HIGH -- vault spec is comprehensive and unambiguous
- Crafting system: HIGH for framework, MEDIUM for quality formula tuning (needs playtesting)

**Research date:** 2026-03-26
**Valid until:** 2026-04-26 (stable -- no external dependency changes expected)
