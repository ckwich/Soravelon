# External Integrations

**Analysis Date:** 2026-03-24

## APIs & External Services

**No external API integrations detected.** The codebase has no imports for OpenAI, Anthropic, Redis, Celery, or other third-party services. All game logic runs locally within the Evennia server process.

**Note:** `world/models.py` `WorldEventLog` has a docstring mentioning "Fed to LLM as world context when generating custom quests" - this feature is planned but not yet implemented (no LLM SDK imports exist).

| Service | Purpose | Status |
|---------|---------|--------|
| LLM (unspecified) | Custom quest generation from world events | Planned, not implemented |

## Web Framework (Built-in)

Evennia provides a built-in web stack. Configured in `web/urls.py`:

| Endpoint | Purpose | Config |
|----------|---------|--------|
| `/` | Website frontend | `web/website/urls.py` |
| `/webclient/` | Browser-based MUD client | `web/webclient/urls.py` |
| `/admin/` | Django admin interface | `web/admin/urls.py` |
| `/api/` | REST API (Evennia default) | `evennia.web.urls` (default patterns) |

**REST API:** Django REST Framework 3.16.1 is available (Evennia dependency) but `web/api/` contains only `__init__.py` - no custom API endpoints defined.

## Database Connections

**Primary Database:**
- Engine: SQLite3 (development) / PostgreSQL (production)
- Location: `server/evennia.db3` (dev)
- Client: Django ORM
- Connection config: `server/conf/settings.py` (inherits Evennia defaults), production overrides in `server/conf/secret_settings.py`

**Migrations Strategy:**
- Evennia core models: managed by Evennia's migration system
- Custom `world` app models: managed via `evennia migrate`
- Current migrations in `world/migrations/`:
  - `0001_initial.py` - Initial schema
  - `0002_alter_factionstanding_unique_together_and_more.py` - Constraint updates
  - `0003_worldeventlog.py` - World event logging

**Custom Django Models (`world/models.py`):**

| Model | Purpose | Key Relations |
|-------|---------|---------------|
| `FactionStanding` | Character-faction relationships | FK to `ObjectDB` |
| `ZoneAttunement` | Character-zone attunement scores | FK to `ObjectDB` |
| `CharacterSkill` | Character skill values (general, zone, node, creature) | FK to `ObjectDB` |
| `NodeEventLog` | Zone node event history | Standalone |
| `InventoryItem` | Item metadata and equipment state | FK to `ObjectDB` |
| `BankAccount` | Character bank balance | OneToOne to `ObjectDB` |
| `BankTransaction` | Banking transaction ledger | FK to `ObjectDB` |
| `RecurringPayment` | Scheduled recurring payments | FK to `ObjectDB` |
| `DebtRecord` | Character debt tracking | FK to `ObjectDB` |
| `WorldEventLog` | Significant world events (mob kills, faction shifts, node events) | Standalone |

**Data Storage Pattern:** All custom models reference Evennia's `ObjectDB` via foreign keys. Character intrinsic state uses Evennia `db` attributes (key-value on `ObjectDB`). Relational data (faction standings, skills, inventory) uses Django models.

## File System Dependencies

**Configuration Files:**
- `server/conf/settings.py` - Main settings (version controlled)
- `server/conf/secret_settings.py` - Secret overrides (exists, likely gitignored)
- `server/conf/at_server_startstop.py` - Server lifecycle hooks and ticker registration
- `server/conf/connection_screens.py` - Login screen text
- `server/conf/at_initial_setup.py` - First-run setup hooks

**Data Directories:**
- `world/areas/` - Zone definition files (Python modules with `build()` functions, loaded on server start)
- `world/nodes/` - Node effect definitions (`node_effects.py`)
- `world/scripts/` - Tick-driven scripts (`node_script.py`)
- `server/evennia.db3` - SQLite database (dev)
- `server/.static/` - Collected static files (generated)

**Zone Loading System:**
On every server start/reload, `_load_all_zones()` in `server/conf/at_server_startstop.py`:
1. Clears `zone_registry` and `named_mob_registry`
2. Scans `world/areas/` for Python files
3. Imports each module and calls its `build()` function
4. Registries are in-memory only (rebuilt each restart)

**Generated/Runtime Files:**
- `server/evennia.db3` - SQLite database
- `server/.static/` - Django collected static files
- `server/logs/` - Server log files (Evennia default)

## Authentication & Identity

**Auth Provider:** Evennia built-in (custom `typeclasses.accounts.SoravelonAccount`)
- Players authenticate via telnet/websocket with username/password
- Accounts stored in Evennia's `AccountDB` (Django auth backend)
- No external OAuth/SSO integrations

## Monitoring & Observability

**Error Tracking:** None (no Sentry, Datadog, etc.)
**Logs:** Evennia's built-in logging (Twisted logging framework)
**Metrics:** None detected

## CI/CD & Deployment

**Hosting:** Not configured (no Dockerfile, docker-compose, or deployment configs detected)
**CI Pipeline:** None detected (no `.github/workflows/`, `.gitlab-ci.yml`, etc.)

## Webhooks & Callbacks

**Incoming:** None
**Outgoing:** None

## Network Protocols

Evennia provides multiple connection protocols (configured via Evennia defaults):

| Protocol | Port (default) | Purpose |
|----------|---------------|---------|
| Telnet | 4000 | Traditional MUD client connections |
| WebSocket | 4002 | Web client connections (via Autobahn) |
| HTTP | 4001 | Django web interface (admin, website, API) |
| SSH | 4004 | Optional SSH connections |

---

*Integration audit: 2026-03-24*
