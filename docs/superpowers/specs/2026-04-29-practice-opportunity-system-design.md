# Practice Opportunity System Design

**Date:** 2026-04-29
**Repo:** `C:\Dev\Evennia\soravelon`

## Purpose

The practice opportunity system gives builders a safe, reusable way to award
hidden skill and domain progression from meaningful in-world actions.

The goal is not to create a generic grind button. A practice opportunity should
represent something the character actually did: repair a stuck winch, read a
weather pattern, stabilize a frightened animal, study a tactical map, clean a
field wound, or perform any other authored action that makes narrative sense.

## Player Experience

- Players use normal in-world verbs such as `repair canal winch` or
  `study signal flags`.
- The result is authored prose, not a numeric XP popup.
- Skill-use counts and domain raw XP are fed into the existing hidden
  progression systems.
- Quest objectives can watch for a named practice opportunity, letting quests
  ask players to do meaningful actions instead of only delivering items or
  killing mobs.
- Practice opportunities may be repeatable or once-per-character.

## Runtime Shape

The core runtime lives in `world/practice_engine.py`.

`resolve_practice_opportunity(payload, context)`:

- validates the authored payload
- checks player command arguments against the authored target
- prevents repeat completion when `once_per_character=True`
- calls `world.skill_engine.accumulate_skill_use`
- calls `world.world_state.accumulate_domain_xp`
- calls `world.quest_engine.check_practice_objectives`
- sends only the authored `success_text` to the player

The shared action dispatcher in `world/action_vocabulary.py` supports:

```python
{"action_type": "grant_practice", "opportunity_id": "...", ...}
```

Dynamic room commands pass raw player arguments through the action context so a
single authored verb can still require a target.

## Builder DSL

Builders author practice opportunities through literal, round-trippable
`AreaBuilder` DSL:

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

The builder stores the payload on `room.db.practice_opportunities` and also
registers a dynamic command with `action_type="grant_practice"`.

`world/zone_serializer.py` also accepts a top-level
`practice_opportunities` list for serialized zone data.

## Quest Objective Shape

Quest objectives can use:

```python
{"type": "practice", "target": "repair_canal_winch", "count": 1}
```

`check_practice_objectives(character, opportunity_id)` increments matching
active quest objectives and caps progress at the authored count.

## Remnance Guardrail

Remnance exists internally for future world-event content, but it is not
player-facing in the current era.

Current behavior:

- generic practice opportunities reject Remnance domain awards
- validation messages do not name Remnance
- public help does not list Remnance or Vaelborn
- command surfaces hide Remnance even if an old `remnance_discovered` flag is
  present
- dynamic ability help hides abilities tied to Remnance, Echoes, or Remnance
  scaling

The current future-event visibility switch is
`character.db.remnance_player_visible`. Nothing in current content sets it.

## Design Rules For Content Authors

- A practice opportunity must be fiction-justified.
- Delivery quests should route players to real places and discoveries, not to
  arbitrary NPC handoffs.
- Practice rewards should encourage exploration, curiosity, or mastery of a
  place.
- Avoid numeric reward language in player-facing success text.
- Do not use practice opportunities to expose Remnance until the future
  dragon-curse story unlocks it.
