# Soravelon — Quick Repository Map

Read `AGENTS.md` first. It is the authoritative engineering and game-design
contract; this file is the current runtime, command, and domain-skill map.

## Runtime Baseline

- **Engine:** Evennia 6.1.0 (Django + Twisted)
- **Python:** 3.12+
- **Database:** Django ORM; SQLite locally and PostgreSQL in production
- **Custom app:** `world` in `INSTALLED_APPS`
- **Runtime authority:** `requirements.txt`

Activate the virtual environment before calling `evennia`, since it launches
`twistd` from `PATH`:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Canonical Commands

```bash
# Full suite or focused labels; this is the canonical test path.
python scripts/run_tests.py
python scripts/run_tests.py tests.test_social_web_kernel

# Startup/import proof after dependency or area changes.
python scripts/smoke_start.py

# Read-only revision authority; none of these commands mutates world content.
evennia worldcontent validate
evennia worldcontent plan
evennia worldcontent status
evennia worldcontent bootstrap-check

# Game lifecycle.
evennia migrate
evennia start
evennia reload
evennia stop
```

For the Evennia launcher, `--settings` takes a filename relative to
`server/conf`, not a Python module path:

```bash
evennia test --settings settings.py tests.test_telnet_protocol
```

Do **not** use `--settings server.conf.settings`; Evennia would resolve that
incorrectly. For isolated local-port playtests, use a temporary settings file,
validate it, then remove it before committing.

## Layout

```text
commands/        command sets and custom commands
server/conf/     Evennia settings, lifecycle hooks, connection screens
tests/           Django/Evennia test suite
typeclasses/     accounts, characters, rooms, exits, objects, mobs, scripts
web/             Django web frontend, API, and webclient
world/           game logic, engines, models, migrations, authored areas
world/areas/     literal AreaBuilder DSL content
world/scripts/   tick-driven scripts
world/nodes/     zone-node effects
```

## Typeclass Defaults

| Role | Class |
| --- | --- |
| Object | `typeclasses.objects.SoravelonObject` |
| Character | `typeclasses.characters.Character` |
| Room | `typeclasses.rooms.SoravelonRoom` |
| Exit | `typeclasses.exits.SoravelonExit` |
| Script | `typeclasses.scripts.SoravelonScript` |
| Account | `typeclasses.accounts.SoravelonAccount` |

## Runtime Notes

- The Telnet bytes-input bug belongs to upstream Evennia 6.0 and is fixed by
  the 6.1 dependency pin. Do not recreate `server/telnet_protocol.py` or a
  `TELNET_PROTOCOL_CLASS` override without a new, proven upstream gap.
- `scripts/run_tests.py` sets `DJANGO_SETTINGS_MODULE=server.conf.settings`
  and is safer than ad-hoc pytest or a bare Django invocation for routine
  work.
- Historical plans can name old versions. Do not "correct" them during an
  unrelated change; verify current behavior from the pin, source, and tests.
  `AGENTS.md` distinguishes historical vault implementation proposals from the
  planned model-generated-content architecture and its authority boundary.

## Domain Skills

Read `.claude/skills/base/skill.md` for every non-trivial task, then the
matching domain skill. `skill-rules.json` is the routing authority.

| Domain | Skill path |
| --- | --- |
| Ancestry, starting standing | `.claude/skills/ancestry-engine/skill.md` |
| Areas, rooms, exits, spawns, builder validation | `.claude/skills/area-builder/skill.md` |
| Banking, Scales, debt, drafts | `.claude/skills/banking/skill.md` |
| Combat, abilities, targeting, corpses | `.claude/skills/combat-system/skill.md` |
| Crafting and recipes | `.claude/skills/crafting-system/skill.md` |
| Dialogue, topics, hints | `.claude/skills/dialogue-system/skill.md` |
| Equipment archetypes and affixes | `.claude/skills/equipment-archetypes/skill.md` |
| Factions, Standing, Trust | `.claude/skills/faction-system/skill.md` |
| Flights and courier routing | `.claude/skills/flight-system/skill.md` |
| Gathering pools and depletion | `.claude/skills/gathering-engine/skill.md` |
| Groups, proximity, loot modes | `.claude/skills/group-system/skill.md` |
| Help and onboarding | `.claude/skills/help-system/skill.md` |
| Inventory, weight, containers | `.claude/skills/inventory-engine/skill.md` |
| Inspect and compare | `.claude/skills/item-inspection/skill.md` |
| Item typeclasses, keyrings | `.claude/skills/item-typeclasses/skill.md` |
| Loot tables and rarity | `.claude/skills/loot-tables/skill.md` |
| Materials and gathering taxonomy | `.claude/skills/material-registry/skill.md` |
| Mob affixes, templates, disposition | `.claude/skills/mob-affix-system/skill.md`, `.claude/skills/mob-templates/skill.md`, `.claude/skills/mob-disposition/skill.md` |
| Nodes, world state, room state | `.claude/skills/node-system/skill.md`, `.claude/skills/world-state-engine/skill.md`, `.claude/skills/room-state/skill.md` |
| OOB publication and client push | `.claude/skills/oob-publisher/skill.md` |
| Patrols and wandering | `.claude/skills/patrol-system/skill.md`, `.claude/skills/wander-system/skill.md` |
| Practice, skills, trainers | `.claude/skills/practice-engine/skill.md`, `.claude/skills/skill-engine/skill.md` |
| Recovery and rest | `.claude/skills/recovery-engine/skill.md` |
| Current-era Remnance visibility | `.claude/skills/remnance-visibility/skill.md` |
| Server configuration and lifecycle | `.claude/skills/server-conf/skill.md` |
| Social commands and channels | `.claude/skills/social-system/skill.md` |
| Vendors and economy | `.claude/skills/vendor-economy/skill.md` |
| Zone attunement and scaling | `.claude/skills/zone-attunement/skill.md`, `.claude/skills/zone-scaling/skill.md` |

## Local Conventions

- Persistent intrinsic state belongs on `db`; volatile state belongs on `ndb`.
  Relationships and durable histories belong in Django models.
- Keep game logic in `world/`; typeclasses and commands call into it.
- Tests use Evennia/Django test helpers, not bare unit-only substitutes when a
  runtime contract is under test.
- Mob behavior comes from computed disposition. Node failure follows the
  healthy → stressed → failing → collapsed state machine.
- Define room-state flags in `FLAG_VOCABULARY` before use.
- Player-facing commands, help, and dialogue must filter Remnance, Vaelborn,
  and Echoes through `world/remnance_visibility.py`; internal data remains
  complete.
