---
phase: 06c-npc-dialogue-and-crafting
plan: 03
type: execute
wave: 2
depends_on: ["06c-01"]
files_modified:
  - world/area_builder.py
  - server/conf/at_server_startstop.py
  - world/action_vocabulary.py
autonomous: true
requirements: [NPC-01, NPC-02]
must_haves:
  truths:
    - "AreaBuilder npc() method accepts dialogue and ambient kwargs and stores them on NPC mob objects"
    - "NPC objects are SoravelonMob instances with is_npc=True created during zone build"
    - "Global ambient ticker fires at 15-second intervals and sends idle echoes to occupied rooms"
    - "Reactive echoes fire from zone state change hooks"
    - "open_dialogue action vocabulary handler is implemented"
  artifacts:
    - path: "world/area_builder.py"
      provides: "Extended npc() method with dialogue and ambient data"
      contains: "dialogue"
    - path: "server/conf/at_server_startstop.py"
      provides: "Global ambient NPC ticker registration"
      contains: "npc_ambient_tick"
    - path: "world/action_vocabulary.py"
      provides: "Implemented open_dialogue handler"
      contains: "open_dialogue"
  key_links:
    - from: "world/area_builder.py"
      to: "typeclasses/mobs.py"
      via: "Creates SoravelonMob with is_npc=True during build()"
      pattern: "is_npc"
    - from: "server/conf/at_server_startstop.py"
      to: "world/dialogue_engine.py"
      via: "TICKER_HANDLER callback to ambient_npc_tick"
      pattern: "ambient_npc_tick"
---

<objective>
Wire NPC dialogue and ambient behavior into the zone loading pipeline. Extend AreaBuilder's npc() method to create actual SoravelonMob objects with dialogue data on db attributes. Register the global ambient ticker. Implement the open_dialogue action vocabulary handler.

Purpose: NPCs need to exist as interactable objects in rooms for dialogue commands to target them. The ambient ticker brings NPCs to life with idle echoes.
Output: Extended area_builder.py, ambient ticker in at_server_startstop.py, open_dialogue handler
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

@world/area_builder.py
@server/conf/at_server_startstop.py
@world/action_vocabulary.py
@typeclasses/mobs.py

<interfaces>
<!-- From Plan 01 outputs -->

From world/dialogue_engine.py:
```python
def ambient_npc_tick():
    """Global ticker callback. Iterates NPC rooms, fires idle echoes for elapsed intervals."""

def fire_npc_reactive_echo(room, trigger_type):
    """Find NPCs in room with matching reactive echo, send to room."""

def get_standing_tier(character, npc):
    """Derive standing tier string from disposition + betrayal."""
```

NPC db attribute naming convention (set by AreaBuilder):
- npc.db.dialogue_greeting_tiers — dict {tier: text}
- npc.db.dialogue_topics — dict {topic_key: {condition: text}}
- npc.db.dialogue_base_hints — list of topic keys
- npc.db.dialogue_tier_hints — dict {tier: [topic_keys]}
- npc.db.dialogue_quest_hints — dict {quest_id: [topic_keys]}
- npc.db.dialogue_network_hints — list of topic keys
- npc.db.dialogue_scholar_hints — list of topic keys
- npc.db.dialogue_warden_hints — list of topic keys
- npc.db.ambient_idle_echoes — list of strings
- npc.db.ambient_idle_interval — int seconds
- npc.db.ambient_idle_variance — int seconds
- npc.db.ambient_reactive_echoes — dict {trigger: text}
- npc.db.is_npc — True
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: AreaBuilder npc() extension + NPC object creation</name>
  <files>world/area_builder.py</files>
  <action>
Extend the existing `npc()` method in AreaBuilder to:

1. Accept `dialogue=dict(...)` and `ambient=dict(...)` keyword arguments per research Example 2.

2. Create an actual SoravelonMob object for the NPC during `build()` (not just store a definition dict). The NPC should:
   - Be a SoravelonMob with `db.is_npc = True`
   - Have `db.combat_enabled = False` (NPCs don't fight)
   - Be placed in the target room (set `location` to room)
   - Be tagged with `("npc", "character_type")` for queryset filtering
   - Be tagged with `("npc", "mob_type")` for mob filtering
   - Use idempotent creation: search for existing NPC by `room_id` tag + `npc_id` tag before creating new one (same pattern as room idempotency)

3. Set dialogue data as db attributes on the NPC object using the naming convention:
   - `npc.db.dialogue_greeting_tiers = dialogue.get("greeting_tiers", {})`
   - `npc.db.dialogue_topics = dialogue.get("topics", {})`
   - `npc.db.dialogue_base_hints = dialogue.get("base_hints", [])`
   - `npc.db.dialogue_tier_hints = dialogue.get("tier_hints", {})`
   - `npc.db.dialogue_quest_hints = dialogue.get("quest_hints", {})`
   - `npc.db.dialogue_network_hints = dialogue.get("network_hints", [])`
   - `npc.db.dialogue_scholar_hints = dialogue.get("scholar_hints", [])`
   - `npc.db.dialogue_warden_hints = dialogue.get("warden_hints", [])`

4. Set ambient data as db attributes:
   - `npc.db.ambient_idle_echoes = ambient.get("idle_echoes", [])`
   - `npc.db.ambient_idle_interval = ambient.get("idle_interval", 60)`
   - `npc.db.ambient_idle_variance = ambient.get("idle_variance", 30)`
   - `npc.db.ambient_reactive_echoes = ambient.get("reactive_echoes", {})`

5. Set faction from kwargs: `npc.db.faction = kwargs.get("faction")`

6. Also add `crafting_stations` support to the `room()` method. If `crafting_stations=["campfire", "forge"]` is passed, add room tags: `room.tags.add("crafting_campfire", category="crafting_station")` for each station.

7. Keep backward compatibility: if `dialogue` and `ambient` kwargs are not provided, the npc() method still works as before (just stores the npc_definitions dict on room.db). The NPC object creation should happen regardless — even NPCs without dialogue data should exist as objects for `look` targeting.

IMPORTANT: The npc_definitions list on room.db should ALSO still be populated (other systems may read it). The NPC object creation is additive.

Use existing AreaBuilder patterns: check `self._zone_obj`, use `self._current_zone_id` for tags, follow the SaverDict copy pattern for any list mutations on room.db.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.area_builder import AreaBuilder; import inspect; sig = inspect.signature(AreaBuilder.npc); params = list(sig.parameters.keys()); print(f'npc() params: {params}'); assert 'kwargs' in params or 'dialogue' in params, 'npc() must accept dialogue kwarg'"</automated>
  </verify>
  <done>AreaBuilder.npc() creates SoravelonMob objects with is_npc=True, stores dialogue and ambient data on db attributes, adds crafting_station room tags, maintains backward compatibility with npc_definitions list</done>
</task>

<task type="auto">
  <name>Task 2: Ambient ticker registration + open_dialogue handler</name>
  <files>server/conf/at_server_startstop.py, world/action_vocabulary.py</files>
  <action>
**server/conf/at_server_startstop.py:**

Add the global ambient NPC ticker registration to `at_server_start()`. Per research Pattern 4 recommendation: 15-second interval, single global ticker.

```python
# In at_server_start(), after existing ticker registrations:
TICKER_HANDLER.add(
    interval=15,
    callback="world.dialogue_engine.ambient_npc_tick",
    idstring="npc_ambient_tick",
    persistent=True,
)
```

Follow the exact same pattern as the existing ticker registrations (node_failure_tick at 30s, spawn_tick, etc.). Place it after them.

**world/action_vocabulary.py:**

Replace the `_stub_handler` for `"open_dialogue"` in the ACTION_HANDLERS dict with a real handler:

```python
def _handle_open_dialogue(character, room, args, **kwargs):
    """
    Trigger dialogue with a specific NPC. Used by trigger system.
    args: {"npc_id": "maren_warden", "topic": "work"} or just {"npc_id": ...}
    """
    npc_id = args.get("npc_id")
    if not npc_id:
        return

    # Find NPC in room by npc_id tag
    from evennia.utils.search import search_tag
    npcs = [obj for obj in room.contents
            if obj.db.is_npc and (obj.tags.has(npc_id, category="npc_id") or
               obj.key.lower().replace(" ", "_") == npc_id)]
    if not npcs:
        return

    npc = npcs[0]
    topic = args.get("topic")

    if topic:
        # Direct topic query
        from world.dialogue_engine import resolve_topic_response
        text, condition = resolve_topic_response(npc, character, topic)
        if text:
            character.msg(f"\n{npc.key} says: {text}")
    else:
        # Greeting
        from world.dialogue_engine import resolve_greeting, get_npc_hints
        greeting_text, tier = resolve_greeting(npc, character)
        character.msg(f"\n{greeting_text}")
        hints = get_npc_hints(npc, character)
        if hints:
            hint_str = ", ".join(f"ask about |w{h}|n" for h in hints)
            character.msg(f"|x[Try: {hint_str}]|n")
```

Update ACTION_HANDLERS dict to replace `"open_dialogue": _stub_handler` with `"open_dialogue": _handle_open_dialogue`.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from world.action_vocabulary import ACTION_HANDLERS; handler = ACTION_HANDLERS.get('open_dialogue'); print(f'open_dialogue handler: {handler.__name__}'); assert handler.__name__ != '_stub_handler', 'open_dialogue still a stub'"</automated>
  </verify>
  <done>Ambient NPC ticker registered at 15-second interval in at_server_start(). open_dialogue action vocabulary handler implemented with NPC lookup, greeting, and topic support.</done>
</task>

</tasks>

<verification>
- AreaBuilder.npc() accepts dialogue and ambient kwargs
- AreaBuilder room() accepts crafting_stations kwarg
- at_server_startstop.py registers npc_ambient_tick ticker
- ACTION_HANDLERS["open_dialogue"] is not the stub handler
- No import errors in any modified file
</verification>

<success_criteria>
- NPCs created as SoravelonMob objects with is_npc=True during zone build
- Dialogue data stored on NPC db attributes following naming convention
- Crafting station room tags set via AreaBuilder
- Ambient ticker registered and callable
- open_dialogue handler functional for trigger system integration
</success_criteria>

<output>
After completion, create `.planning/phases/06c-npc-dialogue-and-crafting/06c-03-SUMMARY.md`
</output>
