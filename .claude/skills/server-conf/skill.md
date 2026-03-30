---
name: server-conf
description: Server lifecycle hooks, ticker registration, settings overrides, and connection config in server/conf/
---

## Activation

This skill triggers when editing these files:
- `server/conf/settings.py`
- `server/conf/at_server_startstop.py`
- `server/conf/at_initial_setup.py`
- `server/conf/connection_screens.py`
- `server/conf/**/*.py`

Keywords: settings, ticker, server start, server stop, lifecycle, TICKER_HANDLER, connection screen, MSSP, START_LOCATION, spawn

---

You are working on **soravelon's server configuration layer** (`server/conf/`).

## Key Files
- `settings.py` — Minimal overrides: SERVERNAME, INSTALLED_APPS (+world), all 6 BASE_*_TYPECLASS paths, START_LOCATION, imports `secret_settings`
- `at_server_startstop.py` — Registers 4 tickers in `at_server_start()` + initializes node pool
- `connection_screens.py` — Login screen using `settings.SERVERNAME` + Evennia version
- `secret_settings.py` — Server-specific secrets (DB creds, etc.) — **never commit**
- `mssp.py` — MUD listing metadata (still has defaults, not yet customized)

## Ticker Registration (at_server_start)
All background ticks register here via `TICKER_HANDLER.add()` with `persistent=True`:
| idstring | interval | callback |
|---|---|---|
| `world_state_decay` | 86400s (24h) | `world.world_state.world_state_decay_tick` |
| `session_xp_flush` | 600s (10m) | `world.world_state.session_xp_safety_flush` |
| `node_failure_tick` | 30s | `world.node_helpers.node_failure_tick` |
| `banking_payment_tick` | 86400s (24h) | `world.banking.banking_payment_tick` |

After tickers: `initialize_node_pool()` recovers orphaned Layer 1 rooms.

## Spawn & Respawn Location Tags
- **`START_LOCATION = "#2"`** — Evennia-level fallback only. Actual spawn uses tag-based lookup in `Character.at_object_creation()`: `search_tag("greeter_room", category="spawn_point")` sets both `home` and `location`
- **Death respawn** uses `search_tag("respawn_point", category="spawn_point")` in `combat_engine._respawn_player()`
- Tags are set in zone spec files (e.g., `world/areas/vaels_crossing.py`), not in settings

## Critical Rules
1. **All tickers must use `persistent=True`** — otherwise they vanish on reload
2. **Ticker callbacks are string paths** — Evennia resolves them lazily; typos fail silently at tick time
3. **`at_server_start()` runs on EVERY start** (cold start + reload) — put one-time setup in `at_initial_setup()` or `at_server_cold_start()` instead
4. **Settings changes require `evennia reload`** — not just a Python reimport
5. **Don't copy defaults** — only override what you change in `settings.py` to avoid blocking upstream updates
6. **Stub files are inactive** — `cmdparser.py`, `serversession.py`, `at_search.py`, `inlinefuncs.py`, `inputfuncs.py` need explicit settings to activate (e.g., `COMMAND_PARSER = "server.conf.cmdparser.cmdparser"`)
7. **Spawn location is tag-based, not dbref-based** — `START_LOCATION` is a fallback only; the real mechanism is `greeter_room` tag lookup in character creation

## References
- **Evennia Settings Defaults:** `evennia/settings_default.py` (upstream)
- **World State Engine:** `world/world_state.py`
- **Node System:** `world/node_helpers.py`
- **Banking Engine:** `world/banking.py`
- **Character Creation:** `typeclasses/characters.py` — spawn point tag lookup

---
**Last Updated:** 2026-03-30
