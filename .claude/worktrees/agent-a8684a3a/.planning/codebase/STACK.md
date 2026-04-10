# Technology Stack

**Analysis Date:** 2026-03-24

## Languages

**Primary:**
- Python 3.12.10 - All game logic, typeclasses, commands, world engine

**Secondary:**
- HTML/CSS/JavaScript - Web frontend (`web/` directory: admin, webclient, website)

## Runtime

**Environment:**
- Python 3.12.10
- Twisted 24.11.0 (async networking, telnet/websocket server)
- Django 6.0.3 (ORM, web framework, admin)

**Package Manager:**
- pip (system-level install, no virtualenv detected)
- No lockfile (no `requirements.txt`, `pyproject.toml`, or `setup.cfg` present)

## Frameworks

**Core:**
- Evennia 6.0.0 - MUD engine providing typeclass system, command handler, session management, web client
- Django 6.0.3 - ORM, migrations, admin interface, URL routing
- Twisted 24.11.0 - Async event loop, telnet/SSL/websocket protocol handling

**Testing:**
- pytest - Test runner (via `evennia test --settings server.conf.settings tests/`)
- Evennia test utilities (`EvenniaTestCase`, `EvenniaCommandTestMixin`)

**Build/Dev:**
- black 26.3.1 - Code formatter
- isort (bundled with Evennia) - Import sorting

## Key Dependencies

**Critical (Evennia core):**

| Package | Version | Purpose |
|---------|---------|---------|
| evennia | 6.0.0 | MUD engine: typeclasses, commands, sessions, tickers |
| django | 6.0.3 | ORM, migrations, admin, URL routing, templates |
| twisted | 24.11.0 | Async networking: telnet, SSL, websocket protocols |
| autobahn | 20.12.3 | WebSocket protocol implementation (WAMP) |
| djangorestframework | 3.16.1 | REST API framework (Evennia web API) |

**Infrastructure (Evennia dependencies):**

| Package | Version | Purpose |
|---------|---------|---------|
| django-sekizai | 2.0.0 | Django template block management |
| pyyaml | 6.0.3 | YAML parsing (config, data files) |
| lunr | 0.7.0.post1 | Full-text search indexing |
| simpleeval | 1.0.3 | Safe expression evaluation |
| black | 26.3.1 | Code formatting |

## Configuration

**Environment:**
- `server/conf/settings.py` - Main Evennia/Django settings (imports `evennia.settings_default`)
- `server/conf/secret_settings.py` - Secret overrides (exists, not committed - contains sensitive config)
- Server name: `soravelon`
- Custom Django app: `world` registered in `INSTALLED_APPS`

**Typeclass Overrides (in `server/conf/settings.py`):**
- `BASE_OBJECT_TYPECLASS` = `typeclasses.objects.SoravelonObject`
- `BASE_CHARACTER_TYPECLASS` = `typeclasses.characters.Character`
- `BASE_ROOM_TYPECLASS` = `typeclasses.rooms.SoravelonRoom`
- `BASE_EXIT_TYPECLASS` = `typeclasses.exits.SoravelonExit`
- `BASE_SCRIPT_TYPECLASS` = `typeclasses.scripts.SoravelonScript`
- `BASE_ACCOUNT_TYPECLASS` = `typeclasses.accounts.SoravelonAccount`

**Build:**
- No build step required - Python source runs directly
- `evennia start` boots both Server (game logic) and Portal (connection handling)
- `evennia reload` hot-reloads server without dropping player connections

## Database

**Development:**
- SQLite3 - `server/evennia.db3`
- Django ORM with Evennia's built-in models + custom `world` app models

**Production:**
- PostgreSQL (configured via `secret_settings.py`)

## Platform Requirements

**Development:**
- Python 3.12+
- Evennia 6.0.0 installed (`pip install evennia`)
- No containerization (no Dockerfile/docker-compose detected)

**Production:**
- Python 3.12+
- PostgreSQL
- Twisted-compatible OS (Linux recommended)

## Ticker System

Evennia's `TICKER_HANDLER` drives periodic game logic. Registered in `server/conf/at_server_startstop.py`:

| Ticker | Interval | Callback |
|--------|----------|----------|
| World state decay | 86400s (24h) | `world.world_state.world_state_decay_tick` |
| Session XP flush | 600s (10m) | `world.world_state.session_xp_safety_flush` |
| Node failure tick | 30s | `world.node_helpers.node_failure_tick` |
| Banking payments | 86400s (24h) | `world.banking.banking_payment_tick` |

---

*Stack analysis: 2026-03-24*
