# Soravelon

Evennia 6.0 MUD — dark-fantasy multiplayer text game with deep progression systems.

## Tech Stack

- **Engine:** Evennia 6.0 (Django + Twisted)
- **Language:** Python 3.11+
- **DB:** Django ORM (SQLite dev / PostgreSQL prod)
- **App:** `world` registered as custom Django app in `INSTALLED_APPS`

## Project Structure

```
typeclasses/     # Characters, rooms, exits, objects, mobs, scripts, accounts
commands/        # Command sets and custom commands
world/           # Game logic — models, engines, helpers, migrations
  scripts/       # Tick-driven scripts (node_script)
  nodes/         # Zone node effects
server/conf/     # Evennia settings, lifecycle hooks, connection screens
tests/           # Pytest test suite
web/             # Django web frontend (admin, API, webclient, website)
```

## Key Commands

```bash
evennia start            # Start server + portal
evennia stop             # Stop server
evennia reload           # Hot-reload without disconnecting players
evennia migrate          # Run Django migrations (world app has custom models)
evennia test --settings server.conf.settings tests/   # Run tests
```

## Custom Typeclasses (settings.py)

| Role       | Class                                  |
|------------|----------------------------------------|
| Object     | `typeclasses.objects.SoravelonObject`  |
| Character  | `typeclasses.characters.Character`     |
| Room       | `typeclasses.rooms.SoravelonRoom`      |
| Exit       | `typeclasses.exits.SoravelonExit`      |
| Script     | `typeclasses.scripts.SoravelonScript`  |
| Account    | `typeclasses.accounts.SoravelonAccount`|

## Skills Reference

Skills document the game's major systems. Invoke via Skill tool when working in that domain.

| Skill | Trigger | Path |
|-------|---------|------|
| **Base** | Any work in this repo | `.claude/skills/base/skill.md` |
| **World State Engine** | Character progression, domain XP, dimensions | `.claude/skills/world-state-engine/skill.md` |
| **Ancestry Engine** | Playable ancestries, traits, starting standings | `.claude/skills/ancestry-engine/skill.md` |
| **Faction System** | Standings, trust, betrayal, subfactions | `.claude/skills/faction-system/skill.md` |
| **Zone Attunement** | Per-zone attunement (0-100), aggregate scores | `.claude/skills/zone-attunement/skill.md` |
| **Node System** | Zone nodes, Layer 0/1 rooms, failure states, ticks | `.claude/skills/node-system/skill.md` |
| **Room State** | Volatile room flags, lazy decay, Sense display | `.claude/skills/room-state/skill.md` |
| **Mob Affix System** | Rarity tiers, weighted pools, forbidden combos | `.claude/skills/mob-affix-system/skill.md` |
| **Mob Disposition** | Computed disposition float, behavior modifiers | `.claude/skills/mob-disposition/skill.md` |
| **Zone Scaling** | Per-player scaling, mob HP, damage math, loot tiers | `.claude/skills/zone-scaling/skill.md` |
| **Combat System** | Damage resolution, crits, mob AI, targeting, corpses | `.claude/skills/combat-system/skill.md` |
| **Banking** | Deposits, withdrawals, drafts, debt, payments | `.claude/skills/banking/skill.md` |
| **Inventory Engine** | Pickup, drop, equip, containers, encumbrance | `.claude/skills/inventory-engine/skill.md` |
| **Item Typeclasses** | SoravelonItem, Container, Equipment, KeyringItem | `.claude/skills/item-typeclasses/skill.md` |
| **Group System** | Party invite, leadership, loot modes, proximity | `.claude/skills/group-system/skill.md` |
| **Loot Tables** | Drop rates, rarity modifiers, material tiers | `.claude/skills/loot-tables/skill.md` |
| **Server Conf** | Lifecycle hooks, tickers, settings, connections | `.claude/skills/server-conf/skill.md` |

## Conventions

- Store game state on `db` attributes (persisted) or `ndb` (volatile). Never raw Django fields on typeclasses.
- Custom Django models go in `world/models.py`; register the `world` app for migrations.
- All game logic lives in `world/` modules; typeclasses call into them.
- Tests use Evennia's `EvenniaTestCase` or `EvenniaCommandTestMixin`.
- Mob behavior is driven by computed disposition — never hardcode friend/foe.
- Node failure uses a state machine (healthy → stressed → failing → collapsed) — respect the tick-driven progression.
- Room state flags must be defined in `FLAG_VOCABULARY` before use — never invent ad-hoc flag names in system code.
