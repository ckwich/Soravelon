---
phase: 06c-npc-dialogue-and-crafting
plan: 04
type: execute
wave: 2
depends_on: ["06c-01", "06c-02"]
files_modified:
  - commands/cmd_dialogue.py
  - commands/cmd_crafting.py
  - commands/default_cmdsets.py
  - typeclasses/characters.py
autonomous: true
requirements: [NPC-01, NPC-02, NPC-03]
must_haves:
  truths:
    - "Player can talk/greet an NPC and see Standing-tier greeting with dynamic hints"
    - "Player can ask <npc> about <topic> and get priority-stack-resolved response"
    - "Player can say text to room and NPCs with matching topics respond via keyword extraction"
    - "Player can tell <npc> text for directed NPC dialogue"
    - "Player can accept/decline quest offers inline with dialogue"
    - "Player can craft/cook/smith/brew recipes with station and ingredient validation"
    - "Player can list known recipes with the recipes command"
  artifacts:
    - path: "commands/cmd_dialogue.py"
      provides: "CmdTalk, CmdAsk, CmdSay (override), CmdTell, CmdAccept, CmdDecline"
      exports: ["CmdTalk", "CmdAsk", "CmdSay", "CmdTell", "CmdAccept", "CmdDecline"]
    - path: "commands/cmd_crafting.py"
      provides: "CmdCraft, CmdCook, CmdSmith, CmdBrew, CmdRecipes"
      exports: ["CmdCraft", "CmdCook", "CmdSmith", "CmdBrew", "CmdRecipes"]
    - path: "commands/default_cmdsets.py"
      provides: "All new commands registered in CharacterCmdSet"
    - path: "typeclasses/characters.py"
      provides: "ndb.pending_quest_offer initialization and at_after_move clearing"
  key_links:
    - from: "commands/cmd_dialogue.py"
      to: "world/dialogue_engine.py"
      via: "resolve_greeting, resolve_topic_response, get_npc_hints, extract_topic"
      pattern: "from world.dialogue_engine import"
    - from: "commands/cmd_crafting.py"
      to: "world/crafting_engine.py"
      via: "craft_item, get_known_recipes"
      pattern: "from world.crafting_engine import"
    - from: "commands/default_cmdsets.py"
      to: "commands/cmd_dialogue.py"
      via: "import and add to CharacterCmdSet"
      pattern: "from commands.cmd_dialogue import"
---

<objective>
Build all player-facing commands for NPC dialogue and crafting. Register them in the CharacterCmdSet. Wire pending quest offer state on character.

Purpose: Players interact with the dialogue and crafting systems through these commands. This is the user-facing layer that dispatches to the engines built in Plans 01 and 02.
Output: commands/cmd_dialogue.py, commands/cmd_crafting.py, updated default_cmdsets.py and characters.py
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

@commands/default_cmdsets.py
@typeclasses/characters.py

<interfaces>
From world/dialogue_engine.py (Plan 01):
```python
def get_standing_tier(character, npc): ...
def resolve_greeting(npc, character): ...  # returns (greeting_text, tier)
def resolve_topic_response(npc, character, topic_key): ...  # returns (text, condition)
def get_npc_hints(npc, character): ...  # returns list of topic key strings
def extract_topic(text, available_topics): ...  # returns topic_key or None
def record_topic_learned(character, npc_id, topic_key, context): ...
def has_available_quest(npc, character): ...  # stub, returns False
def get_quest_offer(npc, character): ...  # stub, returns None
```

From world/crafting_engine.py (Plan 02):
```python
def craft_item(character, recipe_id): ...  # returns (bool, str)
def get_known_recipes(character, skill_filter=None): ...  # returns list of recipe dicts
def learn_recipe(character, recipe_id, learned_from=""): ...  # returns (bool, str)
```

From world/crafting_definitions.py (Plan 02):
```python
RECIPE_REGISTRY = { "trail_rations": {...}, ... }
COMMAND_TO_SKILL = {"cook": "cooking", "smith": "smithing", "brew": "alchemy", "craft": "engineering"}
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Dialogue commands</name>
  <files>commands/cmd_dialogue.py, typeclasses/characters.py</files>
  <action>
Create commands/cmd_dialogue.py with all dialogue commands per D-01. All commands are thin dispatchers to dialogue_engine. No dialogue text in command files (anti-pattern from research).

**CmdTalk** (key="talk", aliases=["greet"]):
- Syntax: `talk <npc>` or `greet <npc>`
- Find NPC in room by name match (search room.contents for objects with `db.is_npc == True`)
- Call `resolve_greeting(npc, character)` to get greeting text and tier
- Display greeting text with NPC name
- Call `get_npc_hints(npc, character)` to get available hints
- Display hints in brackets: `|x[Try: ask about |w{hint1}|n|x, ask about |w{hint2}|n|x]|n`
- Check `has_available_quest(npc, character)` — if True, display quest offer inline (D-06) and set `character.ndb.pending_quest_offer = {"npc": npc, "quest": quest_data}`
- If NPC not found, actionable error: `|rYou don't see anyone by that name here.|n`

**CmdAsk** (key="ask"):
- Syntax: `ask <npc> about <topic>` or `ask <npc> <topic>` (about is optional per vault spec)
- Parse: split on " about " first, then fall back to `<first_word> <rest>`
- Find NPC in room by name
- Call `resolve_topic_response(npc, character, topic_key)`
- If topic found: display response text, call `record_topic_learned()`
- If topic not found: show fallback with available topics list. `|y{npc.key} tilts their head. "I'm not sure what you mean."|n\n|x[Available topics: {topics}]|n`

**CmdSay** (key="say", aliases=["'", '"']):
- IMPORTANT per Pitfall 1: This OVERRIDES Evennia's default CmdSay. Must handle both normal room broadcast AND NPC keyword extraction.
- Syntax: `say <text>` or `'<text>`
- First: broadcast to room as normal say ("`character.key` says, \"{text}\"")
- Then: find all NPCs in room with `db.is_npc == True`
- For each NPC, call `extract_topic(text, available_topics)` where available_topics = list of keys from `npc.db.dialogue_topics or {}`
- If topic match found, call `resolve_topic_response(npc, character, topic_key)` and display response
- Cap at 2 responding NPCs per Claude's discretion recommendation (multi-NPC rooms)
- Prioritize NPCs by Standing tier (friendlier NPCs respond first)

**CmdTell** (key="tell"):
- Syntax: `tell <npc> <text>`
- Find NPC in room by first word
- Extract topic from remaining text using `extract_topic()`
- If topic found: display response (same as CmdAsk flow)
- If no topic: display fallback with available topics

**CmdAccept** (key="accept"):
- Check `character.ndb.pending_quest_offer`
- Validate offering NPC is still in same room (per Pitfall 4)
- If valid: accept quest (stub — set quest flag, send OOB via oob_publisher)
- Clear `pending_quest_offer`
- If no pending offer: `|yThere's nothing to accept right now.|n`

**CmdDecline** (key="decline"):
- Check `character.ndb.pending_quest_offer`
- Clear it, display decline message from NPC
- If no pending offer: `|yThere's nothing to decline right now.|n`

**typeclasses/characters.py changes:**
- In `at_object_creation()`: add `self.ndb.pending_quest_offer = None`
- In `at_after_move()` (or add the method if missing): add `self.ndb.pending_quest_offer = None` to clear stale quest offers on room change (per Pitfall 4)
- Also in `at_after_move()`: call `fire_npc_reactive_echo(destination, "player_enters")` for reactive echo on entry

NPC lookup helper (shared by all commands): Create a helper function `_find_npc_in_room(character, npc_name)` that searches room.contents for objects with `db.is_npc == True` and name matching (case-insensitive, partial match accepted). Return first match or None.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from commands.cmd_dialogue import CmdTalk, CmdAsk, CmdSay, CmdTell, CmdAccept, CmdDecline; print(f'CmdSay key={CmdSay.key}, aliases={CmdSay.aliases}'); assert CmdSay.key == 'say'"</automated>
  </verify>
  <done>All 6 dialogue commands created. CmdSay overrides default with both room broadcast and NPC keyword extraction. Pending quest offer cleared on room change. Reactive echo fires on player_enters.</done>
</task>

<task type="auto">
  <name>Task 2: Crafting commands + cmdset registration</name>
  <files>commands/cmd_crafting.py, commands/default_cmdsets.py</files>
  <action>
**commands/cmd_crafting.py** — Create crafting commands per D-19. All dispatch to crafting_engine.

**CmdCook** (key="cook"):
- Syntax: `cook <recipe_name>`
- Validate recipe exists and uses "cooking" skill via COMMAND_TO_SKILL["cook"]
- Display craft_echo flavor text from recipe definition
- Use `evennia.utils.delay(recipe.craft_time, callback)` for the short delay (2-3 sec per Claude's discretion)
- In callback: call `craft_item(character, recipe_id)` and display result
- If character moves during delay, cancel craft

**CmdSmith** (key="smith"):
- Same pattern as CmdCook but for "smithing" skill

**CmdBrew** (key="brew"):
- Same pattern as CmdCook but for "alchemy" skill

**CmdCraft** (key="craft"):
- Same pattern but for "engineering" skill per D-18 (Engineering craft is separate from Engineering domain)

Since all 4 commands follow identical logic with different skill filters, implement a base class `_BaseCraftCmd` that handles the common flow, then subclass for each:

```python
class _BaseCraftCmd(Command):
    """Base for all crafting commands."""
    craft_skill = None  # override in subclass
    craft_verb = None   # override in subclass

    def func(self):
        # ... common crafting logic
```

**CmdRecipes** (key="recipes"):
- Syntax: `recipes` (show all) or `recipes cooking` / `recipes smithing` / `recipes alchemy`
- Call `get_known_recipes(character, skill_filter)`
- Display formatted list with recipe name, difficulty, ingredients, station required
- Group by skill type
- Use Evennia color codes for formatting

**commands/default_cmdsets.py** — Register ALL new commands in CharacterCmdSet.at_cmdset_creation():

```python
# Dialogue commands
from commands.cmd_dialogue import CmdTalk, CmdAsk, CmdSay, CmdTell, CmdAccept, CmdDecline
self.add(CmdTalk())
self.add(CmdAsk())
self.add(CmdSay())  # overrides Evennia default
self.add(CmdTell())
self.add(CmdAccept())
self.add(CmdDecline())

# Crafting commands
from commands.cmd_crafting import CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes
self.add(CmdCook())
self.add(CmdSmith())
self.add(CmdBrew())
self.add(CmdCraft())
self.add(CmdRecipes())
```

IMPORTANT for CmdSay: Evennia's default CmdSay has key="say" and aliases=["'", '"']. The custom CmdSay must use the same key and aliases to properly override it. The custom version in CharacterCmdSet will take priority over the parent class's version because `self.add()` replaces commands with matching keys.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from commands.cmd_crafting import CmdCook, CmdSmith, CmdBrew, CmdCraft, CmdRecipes; from commands.cmd_dialogue import CmdTalk, CmdAsk, CmdSay; from commands.default_cmdsets import CharacterCmdSet; print('All command imports OK')"</automated>
  </verify>
  <done>All crafting commands (cook, smith, brew, craft, recipes) created with shared base class. All dialogue + crafting commands registered in CharacterCmdSet. CmdSay properly overrides Evennia default.</done>
</task>

</tasks>

<verification>
- All 11 commands importable from their modules
- CharacterCmdSet includes all new commands
- CmdSay has key="say" and aliases matching Evennia default
- CmdCook/CmdSmith/CmdBrew/CmdCraft share base class logic
- typeclasses/characters.py clears pending_quest_offer on room change
</verification>

<success_criteria>
- `talk <npc>` shows Standing-tier greeting + dynamic hints per D-01, D-02, D-04
- `ask <npc> about <topic>` returns priority-stack-resolved response per D-03
- `say <text>` broadcasts to room AND triggers NPC keyword extraction per D-05
- `tell <npc> <text>` targets specific NPC per vault spec
- `accept/decline` handle quest offer state per D-06 with Pitfall 4 protection
- `cook/smith/brew/craft <recipe>` validates station + ingredients + skill per D-15, D-19
- `recipes` lists known recipes per D-16
</success_criteria>

<output>
After completion, create `.planning/phases/06c-npc-dialogue-and-crafting/06c-04-SUMMARY.md`
</output>
