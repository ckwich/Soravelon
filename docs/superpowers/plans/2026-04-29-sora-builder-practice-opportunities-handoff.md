# Sora Builder Handoff: Practice Opportunities

**Date:** 2026-04-29
**Soravelon repo:** `C:\Dev\Evennia\soravelon`
**Builder repo:** `C:\Dev\Sora_builder`

## Summary

Soravelon now supports a builder-safe practice opportunity DSL for meaningful
in-world actions that award hidden skill practice and optional domain XP.

Sora Builder needs parser, data model, validation, and editor UI support so
builders can create and round-trip these opportunities without hand-editing
Python.

## New AreaBuilder DSL

The builder must parse and serialize literal calls shaped like this:

```python
area.practice_opportunity(
    "repair_canal_winch",
    canal_winch_room,
    verb="repair",
    target="canal winch",
    skill_awards={"engineering": 4},
    domain_awards={"engineering": 120},
    success_text=(
        "You reset the slipped gear teeth and learn exactly why the winch "
        "has been chewing its own brake pins."
    ),
    once_per_character=True,
    visible_in_exits=True,
    desc="repair canal winch",
)
```

Strict builder-safe expectations:

- The call must stay as a literal `area.practice_opportunity(...)`.
- Do not introduce helper loops, wrappers, or generated abstractions.
- `room` may be a room variable or room id string, matching existing builder
  parser behavior for other area methods.
- Dicts should round-trip as Python dict literals.
- Multiline strings should be preserved or normalized the same way existing
  room, quest, NPC, and item text is handled.

## Runtime Storage

Soravelon stores each opportunity in:

```python
room.db.practice_opportunities
```

Each entry is a dict:

```python
{
    "opportunity_id": "repair_canal_winch",
    "verb": "repair",
    "target": "canal winch",
    "skill_awards": {"engineering": 4},
    "domain_awards": {"engineering": 120},
    "success_text": "...",
    "failure_text": None,
    "once_per_character": True,
    "cooldown_seconds": None,
}
```

`AreaBuilder.practice_opportunity(...)` also creates a room custom command with:

```python
{
    "action_type": "grant_practice",
    "opportunity_id": "...",
    ...
}
```

The builder UI should show this as a Practice Opportunity, not as a generic
custom command, to avoid duplicate editing surfaces.

## Serialized Zone Support

`world/zone_serializer.py` now accepts a top-level list:

```python
"practice_opportunities": [
    {
        "opportunity_id": "repair_canal_winch",
        "room": "canal_winch_room",
        "verb": "repair",
        "target": "canal winch",
        "skill_awards": {"engineering": 4},
        "domain_awards": {"engineering": 120},
        "success_text": "...",
        "once_per_character": True,
        "visible_in_exits": True,
        "desc": "repair canal winch"
    }
]
```

Builder import/export should treat DSL calls and serialized definitions as the
same concept.

## Required Editor Fields

Recommended room-level panel: `Practice Opportunities`.

Fields:

- `opportunity_id`: required string, unique within the zone.
- `room`: required room reference.
- `verb`: required command verb, for example `repair`, `study`, `tend`,
  `stabilize`, `map`, `calibrate`.
- `target`: optional but strongly recommended command target.
- `skill_awards`: dict of skill id to use-count integer.
- `domain_awards`: dict of domain id to raw XP integer.
- `success_text`: required player-facing prose.
- `failure_text`: optional, currently reserved.
- `once_per_character`: boolean.
- `cooldown_seconds`: optional integer, currently stored for future use.
- `visible_in_exits`: boolean, passed through to the dynamic command and
  displayed to players under the room `Interactions:` heading.
- `aliases`: optional list of command aliases.
- `desc`: optional command/exits hint text.

At least one of `skill_awards` or `domain_awards` should be present for useful
content.

## Validation Rules

Builder-side validation should mirror Soravelon runtime validation:

- `opportunity_id` is required.
- `verb` is required.
- every `skill_awards` key must be in `world.skill_definitions.SKILL_DEFINITIONS`
- every `domain_awards` key must be in `world.world_state.ALL_DOMAINS`
- `skill_awards` counts should be positive integers
- `domain_awards` values should be positive integers
- `success_text` should not mention numeric XP
- `target` should read like something the player can reasonably type after the
  verb

## Remnance Rule

Remnance exists internally for future world-event content, but it must not be
available in current builder UI.

Builder requirements:

- Do not show `remnance` as a selectable domain.
- Do not show Vaelborn as a selectable guild.
- Do not expose Echoes as a current player-facing resource.
- If a parsed file contains `domain_awards={"remnance": ...}`, mark the
  practice opportunity invalid or internal-only and do not save it as normal
  playable content.
- Validation errors shown to normal builders should not teach players or
  content authors about hidden current-era systems. Prefer a message like
  `This hidden current-era domain is not available for practice opportunities.`

This mirrors `world/remnance_visibility.py` and `world/practice_engine.py`.

## Quest Integration

Quest objectives can now watch practice opportunities:

```python
{"type": "practice", "target": "repair_canal_winch", "count": 1}
```

Builder changes recommended:

- In quest objective editors, add `practice` as an objective type.
- When type is `practice`, the `target` picker should list practice opportunity
  IDs authored in the current zone and connected zones if available.
- The objective description should explain the action narratively, not as
  "gain XP".

Example quest objective:

```python
{"type": "practice", "target": "repair_canal_winch", "count": 1,
 "description": "Repair the canal winch so the lock crew can reopen the tow path"}
```

## Parser Tasks For Sora Builder

- Add AST recognition for `area.practice_opportunity(...)`.
- Preserve positional arguments:
  - arg 0: `opportunity_id`
  - arg 1: `room`
- Preserve keyword arguments listed above.
- Link room variable references to room ids in the same way room exits and NPC
  placements are linked.
- Prevent the generated custom command from appearing as an unrelated custom
  command row if it came from `practice_opportunity`.
- Include `practice_opportunities` in any area validation summary.

## Builder UI Tasks

- Add a room-level Practice Opportunities section.
- Add create/edit/delete forms for practice opportunities.
- Show command preview, for example `repair canal winch`.
- Show reward preview as hidden practice, for example `Engineering practice`
  and `Engineering domain progress`, not numeric XP.
- Warn when success text is too generic or describes a reward instead of an
  in-world action.
- Add a quest objective picker for practice opportunity IDs.

## Builder Tests To Add

- Parse a file containing one `area.practice_opportunity(...)`.
- Edit `success_text` and serialize it back to literal DSL.
- Preserve `skill_awards` and `domain_awards` dicts.
- Parse a practice objective inside `area.quest(...)`.
- Reject or block editor save for Remnance domain awards.
- Verify practice-generated dynamic commands do not duplicate as standalone
  custom command rows.
- Round-trip a room with normal exits, NPCs, items, custom commands, and
  practice opportunities without losing any existing content.

## Soravelon Verification Reference

The Soravelon-side focused checks for this slice are:

```powershell
python scripts/run_tests.py tests.test_practice_engine tests.test_action_vocabulary tests.test_quest_engine tests.test_cmd_quest tests.test_dynamic_commands tests.test_remnance_visibility tests.test_help_entries tests.test_help_command tests.test_cmd_guild tests.test_session_lifecycle
python scripts/run_tests.py tests.test_area_builder.TestPracticeOpportunity
python scripts/smoke_start.py
```

The full `tests.test_area_builder` module can be slow in this repo; use the
focused `TestPracticeOpportunity` class for the practice DSL gate unless you
are doing a broader builder compatibility pass.
