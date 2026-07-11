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

Keywords: settings, ticker, server start, server stop, lifecycle, TICKER_HANDLER, connection screen, MSSP, START_LOCATION, spawn, DEFAULT_CHANNELS

---

You are working on **soravelon's server configuration layer** (`server/conf/`).

## Key Files
- `settings.py` — Minimal overrides: SERVERNAME, INSTALLED_APPS (+world), all 6 BASE_*_TYPECLASS paths, OOB/help configuration, all default channels, `SOCIAL_RENDERER_ENABLED`, and imports `secret_settings`
- `at_server_startstop.py` — Registers persistent tickers, initializes the node pool, rebuilds authored areas, resolves cross-zone exits, materializes Social Web topology, and initializes spawn records
- `connection_screens.py` — Dark fantasy themed login screen with Soravelon lore excerpt, ANSI colors, and connect/create instructions
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
| `spawn_tick` | 60s | `world.mob_spawner.spawn_tick` |
| `wander_tick` | 60s | `world.wander_system.wander_tick` |
| `npc_ambient_tick` | 15s | `world.dialogue_engine.ambient_npc_tick` |
| `social_propagation_tick` | 60s | `world.social_engine.social_propagation_tick` |

After tickers: `initialize_node_pool()` recovers orphaned Layer 1 rooms.

## Channel Configuration
`DEFAULT_CHANNELS` defines auto-created channels:
- **Public** — default Evennia public discussion channel
- **MudInfo** — admin-only connection log
- **OOC** — server-wide out-of-character chat using `typeclasses.channels.OOCChannel`
- **Combat, Subterfuge, Naturalism, Resonance, Arcana, Diplomacy, Alchemy,
  Tactics, Engineering, Remnance** — default `DomainChannel` instances with a
  `domain_name` attribute

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
8. **OOC and domain channels use custom typeclasses** — update
   `SORAVELON_DOMAIN_CHANNELS` and the matching channel behavior together; all
   listed domains are materialized through `DEFAULT_CHANNELS` at startup.
9. **Do not recreate the retired Telnet override** — Evennia 6.1 owns the
   bytes-safe Telnet protocol. Prefer upstream upgrades plus stock-path tests
   over copied protocol methods.

## References
- **Evennia Settings Defaults:** `evennia/settings_default.py` (upstream)
- **World State Engine:** `world/world_state.py`
- **Node System:** `world/node_helpers.py`
- **Banking Engine:** `world/banking.py`
- **Character Creation:** `typeclasses/characters.py` — spawn point tag lookup
- **Channel Typeclasses:** `typeclasses/channels.py` — OOCChannel, DomainChannel

---
**Last Updated:** 2026-07-11
