---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 03
type: execute
wave: 2
depends_on: ["06b-02"]
files_modified:
  - world/ancestry_engine.py
  - world/world_state.py
  - commands/skill_commands.py
  - commands/default_cmdsets.py
autonomous: true
requirements: [SKL-01, SKL-03]

must_haves:
  truths:
    - "Ancestry skill seeds applied at character creation via set_ancestry()"
    - "Skill accumulators flush alongside domain XP on the existing 600s timer"
    - "Player can view skills filtered by category and practice skills with CmdPractice"
    - "Animal Handling skill exists and is trackable to 100 (Dragon Handling unlock at 100)"
  artifacts:
    - path: "world/ancestry_engine.py"
      provides: "set_ancestry() wired to apply_ancestry_skill_seeds()"
    - path: "world/world_state.py"
      provides: "session_xp_safety_flush calls commit_skill_accumulators"
    - path: "commands/skill_commands.py"
      provides: "CmdSkills, CmdPractice, CmdTrain commands"
      exports: ["CmdSkills", "CmdPractice", "CmdTrain"]
    - path: "commands/default_cmdsets.py"
      provides: "Skill commands registered in CharacterCmdSet"
  key_links:
    - from: "world/ancestry_engine.py"
      to: "world/skill_engine.py"
      via: "set_ancestry() calls apply_ancestry_skill_seeds()"
      pattern: "apply_ancestry_skill_seeds"
    - from: "world/world_state.py"
      to: "world/skill_engine.py"
      via: "session_xp_safety_flush piggybacks commit_skill_accumulators"
      pattern: "commit_skill_accumulators"
    - from: "commands/skill_commands.py"
      to: "world/skill_engine.py"
      via: "CmdPractice calls practice_skill()"
      pattern: "practice_skill"
---

<objective>
Wire skill engine into character creation (ancestry seeds), session flush (accumulator commit), and player-facing commands (skills/practice/train).

Purpose: The skill engine from Plan 02 needs three integration points to be usable: ancestry seeds at character creation (D-20), accumulator flush on the existing 600s timer (research recommendation), and commands for player interaction (D-21). This plan also registers commands in the CharacterCmdSet.

Output: ancestry_engine.py extension, world_state.py flush hook, skill_commands.py, cmdset registration.
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-02-SUMMARY.md

@C:\Obsidian\brain\Soravelon\soravelon-skills.md

@world/ancestry_engine.py
@world/world_state.py
@commands/default_cmdsets.py
</context>

<interfaces>
<!-- From Plan 02 skill_engine.py -->
From world/skill_engine.py (created in Plan 02):
```python
def apply_ancestry_skill_seeds(character, ancestry_id, coat=None): ...
def commit_skill_accumulators(character): ...
def practice_skill(character, skill_id) -> (bool, str): ...
def train_with_trainer(character, skill_id, trainer_id) -> (bool, str): ...
def get_skill_value(character, skill_id) -> float: ...
def get_skills_by_type(character, skill_type) -> list[dict]: ...
```

From world/ancestry_engine.py:
```python
def set_ancestry(character, ancestry_id, coat=None):
    # Returns (bool, str). Currently: sets db.ancestry, applies starting standings.
    # Extension point: add skill seeds call.
```

From world/world_state.py:
```python
def session_xp_safety_flush(*args, **kwargs):
    # Called every 600s by TICKER_HANDLER. Flushes domain XP accumulators.
    # Extension point: add commit_skill_accumulators() call.
```
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: Ancestry seed wiring + session flush integration</name>
  <files>world/ancestry_engine.py, world/world_state.py</files>
  <action>
**Step 1: Extend set_ancestry() in world/ancestry_engine.py** per D-20:

After `_apply_starting_standings(character, ancestry_id)` and before the return statements, add:

```python
# Apply ancestry skill seeds (D-20)
from world.skill_engine import apply_ancestry_skill_seeds
apply_ancestry_skill_seeds(character, ancestry_id, coat=coat)
```

This creates CharacterSkill records with seed values for the chosen ancestry. Human gets no seeds. Selvar uses coat to determine North/South lineage per SELVAR_COAT_TO_LINEAGE mapping in skill_definitions.py.

**Step 2: Extend session_xp_safety_flush() in world/world_state.py:**

Find the existing `session_xp_safety_flush` function. It already iterates online characters and flushes domain XP. Add skill accumulator flush inside the same character loop:

```python
# Flush skill accumulators alongside domain XP
from world.skill_engine import commit_skill_accumulators
commit_skill_accumulators(character)
```

This piggybacks on the existing 600s timer -- no new ticker needed per research recommendation. The import should be lazy (inside the function) to avoid circular import issues.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "import ast; tree = ast.parse(open('world/ancestry_engine.py').read()); funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == 'set_ancestry']; body_src = ast.dump(funcs[0]); assert 'apply_ancestry_skill_seeds' in body_src, 'set_ancestry missing skill seeds call'; print('ancestry_engine OK')" && python -c "import ast; src = open('world/world_state.py').read(); assert 'commit_skill_accumulators' in src, 'world_state missing skill flush'; print('world_state OK')"</automated>
  </verify>
  <done>set_ancestry() calls apply_ancestry_skill_seeds() after starting standings. session_xp_safety_flush() commits skill accumulators for all online characters alongside domain XP flush on the existing 600s timer.</done>
</task>

<task type="auto">
  <name>Task 2: Skill commands + CmdSet registration</name>
  <files>commands/skill_commands.py, commands/default_cmdsets.py</files>
  <action>
**Step 1: Create commands/skill_commands.py** with three commands per D-21 and vault spec practice commands:

**CmdSkills** (key="skills", aliases=["skill"]):
- Usage: `skills` (summary), `skills general` (general proficiencies), `skills attunement` (zone/node/creature), `skills <skill_name>` (detailed view)
- No args: Show summary -- count of non-zero skills per category, top 3 highest skills
- `general`: Call `get_skills_by_type(character, "general")`, format as table with Name | Value columns. Only non-zero per D-21.
- `attunement`: Call `get_skills_by_type` for each attunement type (zone_attunement, node_attunement, creature_attunement), group and display
- `<skill_name>`: Look up SKILL_DEFINITIONS, show description, current value, thresholds reached/remaining, last_practiced_at, domain_bonus info
- Use Evennia color codes: `|w` for headers, `|g` for high values (75+), `|y` for mid (25-74), `|n` for reset

**CmdPractice** (key="practice"):
- Usage: `practice <skill_name>`
- Parse skill name from args (match against SKILL_DEFINITIONS keys, use fuzzy matching: check startswith then substring)
- Call `practice_skill(character, skill_id)`
- Display result message (includes old->new value and cooldown info)

**CmdTrain** (key="train"):
- Usage: `train with <npc_name>` or `train <skill_name> with <npc_name>`
- Parse NPC name and optional skill from args
- Find NPC in room by name
- Look up trainer in TRAINER_REGISTRY by NPC's trainer_id tag or db.trainer_id
- Call `train_with_trainer(character, skill_id, trainer_id)`
- Display result message (includes cost and bonus info)
- If TRAINER_REGISTRY is empty (framework only), return "No trainers available yet."

All commands use `from commands.command import Command` as base class per Phase 01 decision.

**Step 2: Register in commands/default_cmdsets.py:**

Add imports and add CmdSkills, CmdPractice, CmdTrain to the CharacterCmdSet. Follow the same pattern as existing command registrations in that file.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "from commands.skill_commands import CmdSkills, CmdPractice, CmdTrain; print('CmdSkills key:', CmdSkills.key); print('CmdPractice key:', CmdPractice.key); print('CmdTrain key:', CmdTrain.key); print('OK')"</automated>
  </verify>
  <done>CmdSkills shows skill summary/detail filtered by category (general, attunement) with only non-zero skills per D-21. CmdPractice calls practice_skill() with 24hr rolling cooldown. CmdTrain framework ready for NPC trainer integration. All three commands registered in CharacterCmdSet.</done>
</task>

</tasks>

<verification>
- set_ancestry("kauroran") creates CharacterSkill records: swimming=30, fishing=25, beast_training=20, persuasion=15
- set_ancestry("selvar", coat="winter") creates: tracking=20, climbing=15, intimidation=10 (North lineage)
- set_ancestry("selvar", coat="summer") creates: lockpicking=15, appraisal=15, persuasion=10, navigation=20 (South lineage)
- session_xp_safety_flush flushes skill accumulators alongside domain XP
- `skills`, `skills general`, `practice lockpicking` commands parse correctly
- Commands are in CharacterCmdSet
</verification>

<success_criteria>
Ancestry skill seeds are applied during character creation. Skill accumulators flush every 10 minutes on the existing timer. Players can view skills, practice them, and (framework-ready) train with NPCs. The animal_handling skill is in the registry and trackable to 100 per SKL-03.
</success_criteria>

<output>
After completion, create `.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-03-SUMMARY.md`
</output>
