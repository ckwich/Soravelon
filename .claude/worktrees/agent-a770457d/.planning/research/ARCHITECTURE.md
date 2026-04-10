# Architecture Research

**Domain:** Evennia MUD — ability system, desktop client, GUI area builder
**Researched:** 2026-03-24
**Confidence:** HIGH (Evennia protocol verified against official docs; ability system patterns derived from established RPG architecture; client patterns from Tauri 2.0 docs)

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                    DESKTOP CLIENT (separate repo)                     │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────────────────┐ │
│  │  MUD Terminal │  │  Map / Dashboard │  │    GUI Area Builder      │ │
│  │  (text pane)  │  │  (OOB panels)   │  │  (zone authoring tool)   │ │
│  └──────┬────────┘  └────────┬────────┘  └───────────┬──────────────┘ │
│         │                   │                        │               │
│  ┌──────▼───────────────────▼────────────────────────▼──────────────┐ │
│  │              WebSocket Layer (JSON protocol)                      │ │
│  │         ws://host:4008  — Evennia webclient port                  │ │
│  └──────────────────────────┬──────────────────────────────────────┘ │
└─────────────────────────────│────────────────────────────────────────┘
                              │  JSON: ["cmdname", [args], {kwargs}]
┌─────────────────────────────▼────────────────────────────────────────┐
│                    EVENNIA SERVER (soravelon repo)                    │
│                                                                       │
│  Layer 1: Typeclasses (Interface)                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐                 │
│  │  Character   │  │     Mob      │  │    Room     │  ...             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘                 │
│         │                 │                  │                        │
│  Layer 2: World Engines (Business Logic)                              │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Ability  │  │  Skill       │  │  Combat      │  │  Subclass /  │  │
│  │ Engine   │  │  Engine      │  │  Engine      │  │  Guild Eng.  │  │
│  └────┬─────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│       │               │                  │                  │          │
│  ┌────▼───────────────▼──────────────────▼──────────────────▼───────┐ │
│  │                     world/abilities/                               │ │
│  │   (ability definitions — pure data dicts, one file per subclass)  │ │
│  └─────────────────────────────────┬──────────────────────────────── ┘ │
│                                    │                                   │
│  Layer 3: Django Models (Persistence)                                 │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  world/models.py — CharacterAbility, CharacterSkill, SubclassRec  │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│             GUI AREA BUILDER (client-side component)                  │
│  ┌───────────────────┐    ┌──────────────────────────────────────┐   │
│  │  Visual Editor    │    │         .py File Generator            │   │
│  │  (drag-drop UI)   │ -> │  outputs world/areas/{zone_id}.py    │   │
│  └───────────────────┘    └──────────────────────────────────────┘   │
│   reads/writes to local filesystem (soravelon repo working dir)       │
└──────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Location |
|-----------|----------------|----------|
| Ability Engine | Resolve ability activation, apply effects, dispatch result to combat | `world/ability_engine.py` |
| Ability Registry | Static data definitions — all 360+ abilities as plain dicts | `world/abilities/` (one file per subclass or domain) |
| Skill Engine | General proficiency tracking (0-100), profession tracks | `world/skill_engine.py` |
| Subclass Engine | Determine active subclass from primary+secondary domains, gate tier access | `world/subclass_engine.py` |
| Combat Engine | Turn sequencing, damage resolution, ability queue — calls ability engine | `world/combat_engine.py` |
| Ancestry Engine | Apply ancestry stat modifiers and traits at character creation and login | `world/ancestry_engine.py` |
| OOB Publisher | Serialize structured data (map state, node events, health) to client | `world/oob_publisher.py` |
| WebSocket Client | Persistent ws:// connection to Evennia port 4008, renders text + OOB panels | `client/src/` (separate repo) |
| GUI Area Builder | Visual editor producing `world/areas/*.py` AreaBuilder spec files | `client/src/builder/` (separate repo) |

## Recommended Project Structure

### Server side (soravelon repo)

```
world/
├── ability_engine.py        # Activation logic: gate checks, effect dispatch, cooldowns
├── ability_registry.py      # Registry loader: imports all ability defs, builds lookup dict
├── abilities/               # Ability data definitions (pure data, no logic)
│   ├── __init__.py
│   ├── combat_subterfuge.py     # Duskblade abilities (all 4 tiers)
│   ├── combat_naturalism.py     # Thornguard abilities
│   ├── ...                      # one file per subclass (90 files)
│   └── base_abilities.py        # Shared building blocks (damage, heal, buff patterns)
├── skill_engine.py          # General proficiency 0-100, profession tracks
├── subclass_engine.py       # Domain pair -> subclass lookup, tier unlock thresholds
├── combat_engine.py         # Turn loop, targeting, ability queue, damage math
├── ancestry_engine.py       # Human/Kau'roran/Veth/Selvar trait application
├── oob_publisher.py         # Server -> client structured data (map, node state, HP)
├── npc_template_engine.py   # Variable injection into NPC dialogue/behavior
```

### Client side (separate repo)

```
soravelon-client/
├── src-tauri/               # Rust backend (file I/O, native OS APIs)
│   ├── src/
│   │   └── main.rs          # Tauri app entry, commands for file read/write
│   └── tauri.conf.json      # App configuration, permissions
├── src/                     # Frontend (React/Vue/Svelte)
│   ├── connection/
│   │   └── EventniaSocket.ts    # WebSocket manager, message format encode/decode
│   ├── panels/
│   │   ├── TerminalPane.tsx     # Text output (handles "text" cmd type)
│   │   ├── MapPanel.tsx         # Mini-map (handles "map" OOB cmd type)
│   │   ├── StatusPanel.tsx      # HP/resource bars (handles "status" OOB cmd type)
│   │   └── NodeEventPanel.tsx   # Node failure alerts (handles "node_event" OOB type)
│   ├── builder/
│   │   ├── AreaEditor.tsx       # Visual room/exit editor
│   │   ├── MobEditor.tsx        # Mob spec editor
│   │   ├── ZoneSerializer.ts    # Converts editor state -> AreaBuilder .py text
│   │   └── FileManager.ts       # Read/write world/areas/*.py via Tauri fs API
│   └── App.tsx
```

### Structure Rationale

- **`world/abilities/`:** Separates data from logic. The ability engine imports from here — 90 subclass files stay isolated and independently authored. No file becomes a 5,000-line monolith.
- **`world/ability_registry.py`:** Single import point. At server start, the registry loads all definition files and builds a `dict[ability_key -> AbilityDef]`. The ability engine never does dynamic file lookups.
- **`world/oob_publisher.py`:** Centralizes all structured data sent to the desktop client. Other engines call `oob_publisher.send_status(character)`, not `character.msg(status=...)` directly. Prevents OOB call patterns from scattering across the codebase.
- **`client/src/builder/`:** Area builder lives in the client repo, not the server repo. It writes `.py` files to the working copy of soravelon. The server never knows the builder exists — it just loads whatever `.py` files are in `world/areas/` on restart.

## Architectural Patterns

### Pattern 1: Data-Driven Ability Registry

**What:** Abilities are plain Python dicts with a known schema, grouped into files by subclass. A central registry loads them at server start into a lookup dict. The ability engine is generic code that operates on these dicts.

**When to use:** Always for Soravelon's 360+ abilities. Prevents ability logic from being scattered across 90 command classes.

**Trade-offs:** All ability defs must conform to the same schema. Abilities requiring highly custom logic need an escape hatch (a callable `effect_fn` field).

**Example:**
```python
# world/abilities/combat_subterfuge.py (Duskblade — Combat + Subterfuge)
DUSKBLADE_ABILITIES = {
    "shadow_strike": {
        "key": "shadow_strike",
        "subclass": "duskblade",
        "tier": 1,                    # unlocks at Guild Tier Score 0
        "tier_score_required": 0,
        "cooldown": 8,                # seconds
        "resource_cost": {"stamina": 10},
        "target": "single_enemy",
        "effects": [
            {"type": "damage", "formula": "1.4 * combat_score", "damage_type": "physical"},
            {"type": "debuff", "tag": "off_balance", "duration": 2},
        ],
        "description": "A fast strike from shadow, leaving the target off-balance.",
    },
    "midnight_veil": {
        "key": "midnight_veil",
        "subclass": "duskblade",
        "tier": 3,                    # unlocks at Guild Tier Score 50
        "tier_score_required": 50,
        ...
    },
}
```

```python
# world/ability_registry.py
_REGISTRY: dict[str, dict] = {}

def load_all_abilities():
    """Called once at server start from at_server_start()."""
    from world.abilities import combat_subterfuge, combat_naturalism  # etc.
    for module in ALL_ABILITY_MODULES:
        for ability_dict in vars(module).values():
            if isinstance(ability_dict, dict) and "key" in ability_dict:
                _REGISTRY[ability_dict["key"]] = ability_dict

def get_ability(key: str) -> dict | None:
    return _REGISTRY.get(key)
```

### Pattern 2: Subclass Engine as Gating Layer

**What:** The subclass engine is the single place that determines which subclass a character has and what tier they have unlocked. All other systems ask the subclass engine, never compute it themselves.

**When to use:** Any time ability access, ability tier, or subclass identity needs to be checked.

**Trade-offs:** One extra function call in the hot path. Worth it for correctness — subclass logic changes in one place.

**Example:**
```python
# world/subclass_engine.py
def get_active_subclass(character) -> str | None:
    """Returns subclass key from primary+secondary domain pair, or None."""
    primary = character.db.primary_domain
    secondary = character.db.secondary_domain
    if not primary or not secondary:
        return None
    return DOMAIN_PAIR_TO_SUBCLASS.get((primary, secondary))

def get_tier_score(character) -> int:
    """Returns Guild Tier Score (0-100) based on domain mastery."""
    subclass = get_active_subclass(character)
    if not subclass:
        return 0
    primary, secondary = get_domains_for_subclass(subclass)
    primary_score = character.db.domain_scores.get(primary, 0)
    secondary_score = character.db.domain_scores.get(secondary, 0)
    return int((primary_score * 0.7) + (secondary_score * 0.3))

def get_unlocked_tiers(character) -> list[int]:
    """Returns list of unlocked tier indices [1], [1,2], [1,2,3], [1,2,3,4]."""
    ts = get_tier_score(character)
    if ts >= 85: return [1, 2, 3, 4]
    if ts >= 50: return [1, 2, 3]
    if ts >= 20: return [1, 2]
    return [1]
```

### Pattern 3: OOB Push on State Change

**What:** Whenever the server changes state that the client displays (HP, node events, position on map), it pushes structured data to the client using `character.msg(cmdname=data)`. This goes over the existing WebSocket connection as `["cmdname", [args], {kwargs}]`.

**When to use:** Any server event the client needs to reflect without waiting for a player command.

**Trade-offs:** Requires the client to know what OOB command types exist and register handlers for them. Add new types deliberately — too many types makes the client hard to maintain.

**Example:**
```python
# world/oob_publisher.py
def push_status(character):
    """Send health/resource bar update to client."""
    character.msg(status={
        "hp": character.db.hp,
        "hp_max": character.db.hp_max,
        "stamina": character.db.stamina,
        "stamina_max": character.db.stamina_max,
    })

def push_node_event(character, node_type: str, state: str):
    """Notify client of zone node state change."""
    character.msg(node_event={"type": node_type, "state": state})

def push_map_update(character, room):
    """Send mini-map adjacency data."""
    character.msg(map_update={
        "room_id": room.id,
        "zone_id": room.db.zone_id,
        "exits": list(room.exits),
    })
```

### Pattern 4: GUI Builder as File Writer (No Server API)

**What:** The area builder client tool reads and writes `.py` files in `world/areas/` directly via Tauri's filesystem API. It does not talk to the running Evennia server to create rooms. After authoring, the developer runs `evennia reload` and the new area spec is picked up by `_load_all_zones()`.

**When to use:** Always. The alternative (a live HTTP API that creates rooms on-the-fly) requires careful idempotency management and bypasses the build order guarantees of AreaBuilder.

**Trade-offs:** Requires a server reload to see new areas in-game. This is acceptable for content authoring — zones are not hot-swapped. The benefit is simplicity: the builder is pure UI code with no server-side authorization complexity.

**Rationale:** AreaBuilder is already idempotent (it checks for existing rooms before creating). The `.py` file is the source of truth. Writing to the file and reloading respects this contract.

## Data Flow

### Ability Activation Flow

```
Player types "shadow_strike goblin"
    ↓
Command dispatch (commands/default_cmdsets.py)
    ↓
AbilityCommand.func()
    1. calls subclass_engine.get_active_subclass(caller) -> "duskblade"
    2. calls subclass_engine.get_unlocked_tiers(caller) -> [1, 2]
    3. calls ability_registry.get_ability("shadow_strike") -> AbilityDef
    4. checks AbilityDef["tier"] <= max(unlocked_tiers)
    5. checks caller.cooldowns.ready("shadow_strike")
    6. calls ability_engine.activate(caller, target, ability_def)
    ↓
ability_engine.activate()
    1. deducts resource_cost from character.db
    2. calls combat_engine.apply_effects(caster, target, effects_list)
    3. sets caller.cooldowns.add("shadow_strike", cooldown)
    4. calls oob_publisher.push_status(caller) to update client HP bars
    ↓
combat_engine.apply_effects()
    - each effect resolved by type ("damage", "debuff", "heal", etc.)
    - damage: zone_scaling.scale_damage() * ability formula coefficient
    - debuff: adds tag to target.db.status_effects with expiry tick
    ↓
Returns (success: bool, message: str) to AbilityCommand
    ↓
Command sends message to room
```

### OOB Data Flow (Server to Desktop Client)

```
Server event (combat hit, node state change, room move)
    ↓
Engine calls oob_publisher.push_*(character, data)
    ↓
character.msg(cmdname=kwargs)   [Evennia's msg() API]
    ↓
ServerSession -> AMP -> PortalSession
    ↓
WebclientProtocol.send_default()
    serializes: json.dumps(["cmdname", [], {kwargs}])
    ↓
WebSocket frame -> client ws://host:4008
    ↓
EventniaSocket.ts receives JSON array
    dispatches by cmdname:
    - "text"       -> TerminalPane
    - "status"     -> StatusPanel
    - "node_event" -> NodeEventPanel
    - "map_update" -> MapPanel
```

### Area Builder File Flow

```
Author uses GUI builder (Tauri desktop app)
    ↓
AreaEditor.tsx builds zone spec in-memory (rooms, exits, mobs)
    ↓
ZoneSerializer.ts converts to Python source:
    "from world.area_builder import AreaBuilder\n..."
    ↓
FileManager.ts calls Tauri fs.writeTextFile(
    "path/to/soravelon/world/areas/vaels_crossing.py",
    python_source
)
    ↓
Developer runs "evennia reload" (or server restart)
    ↓
at_server_start() -> _load_all_zones()
    imports world/areas/vaels_crossing.py
    calls build() -> AreaBuilder creates Evennia DB objects
```

### Key Data Flows Summary

1. **Ability unlock flow:** Domain XP accumulation -> commit_session_xp() -> domain_scores updated -> subclass_engine.get_tier_score() derives current tier -> no separate unlock record needed.
2. **Skill proficiency flow:** Actions award skill XP -> CharacterSkill model updated (using pattern from existing CharacterSkill model) -> skill checks in crafting/profession commands query model directly.
3. **Ancestry flow:** Character creation selects ancestry -> ancestry_engine.apply() writes modifiers to character.db once -> ancestry_engine.get_traits() reads from db.ancestry key for behavioral gates.
4. **Client reconnect flow:** On WebSocket reconnect, server sends full state push (status, map, active node) — client is stateless between connections and always re-hydrates from server.

## Integration Points

### New Systems Integrating with Existing Architecture

| New System | Integrates With | Integration Pattern |
|------------|-----------------|---------------------|
| Ability Engine | world_state.py (domain scores for formulas), zone_scaling.py (damage math) | Direct import, same as existing cross-engine calls |
| Ability Engine | combat engine cooldowns | Uses evennia.contrib.cooldowns (attaches CooldownHandler to Character) |
| Subclass Engine | world_state.py (domain scores) | Reads character.db.domain_scores, no write path |
| Skill Engine | world/models.py | CharacterSkill model already exists — extend or reuse |
| Ancestry Engine | typeclasses/characters.py at_object_creation() | Called during character creation, writes to character.db |
| OOB Publisher | Any engine that changes player state | Engines import oob_publisher and call push_* after state changes |
| GUI Builder | world/areas/*.py (file write), AreaBuilder DSL | Client writes Python source; server loads it unchanged |
| Desktop Client | Evennia webclient websocket (port 4008) | JSON protocol: ["cmdname", [args], {kwargs}] |

### Internal Boundaries

| Boundary | Communication | Rule |
|----------|---------------|------|
| Ability Engine -> Combat Engine | Direct function call | ability_engine calls combat_engine.apply_effects(); never reversed |
| Ability Engine -> OOB Publisher | Direct function call | ability_engine calls oob_publisher after state change |
| Subclass Engine -> Ability Engine | One-way read | ability_engine asks subclass_engine for tier; subclass_engine never calls ability_engine |
| Ability Registry -> Ability Engine | Dict lookup | Registry is read-only after server start; engine never writes to registry |
| Combat Engine -> World State | Direct function call | combat_engine calls world_state.accumulate_domain_xp() on kill/event |
| OOB Publisher -> Evennia Protocol | character.msg() | Publisher never touches websocket directly; Evennia handles protocol layer |
| GUI Builder -> Server | Filesystem only (no HTTP) | Builder writes .py files; server reads them at reload time |

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Evennia contrib cooldowns | Import `from evennia.contrib.game_systems.cooldowns import CooldownHandler`; attach to Character via at_object_creation | Cooldown state persists across disconnects — confirm this with evennia.contrib.cooldowns docs during implementation |
| Tauri fs API | `import { writeTextFile, readTextFile } from '@tauri-apps/api/fs'` | Requires `fs` permission in tauri.conf.json; use allowlist scoping to soravelon working dir |
| Evennia webclient websocket | ws://127.0.0.1:4008 (dev) — port from WEBSOCKET_CLIENT_URL setting | Port is configurable; client must read it from config or hardcode per environment |

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-500 concurrent | Current SQLite + single process is fine. Ability engine adds negligible overhead (dict lookup). |
| 500-2000 concurrent | Switch to PostgreSQL (already planned for prod). Consider caching CharacterSkill queries in ndb with TTL invalidation on write. |
| 2000+ concurrent | Evennia's single-server Twisted model hits ceiling. At this scale, evaluate Evennia's portal/server split for horizontal portal scaling. Not a near-term concern. |

### Scaling Priorities

1. **First bottleneck:** Django ORM queries in hot combat loop. Prevention: use `ndb` to cache combat-relevant model data (skill levels, active buffs) per session; flush on logout.
2. **Second bottleneck:** Ability definition lookups. Prevention: already addressed by registry pattern (all defs in memory at server start, O(1) dict lookup).

## Anti-Patterns

### Anti-Pattern 1: Ability Logic in Command Classes

**What people do:** Write combat ability logic directly in `CmdShadowStrike.func()`, one command class per ability.

**Why it's wrong:** 360+ command classes is unmanageable. Logic is scattered, untestable in isolation, and copy-pasted. Changing how damage scales requires touching every ability.

**Do this instead:** One generic `CmdUseAbility.func()` that dispatches to `ability_engine.activate(caller, target, ability_key)`. The ability key is either the command name or an argument. All ability-specific data lives in the registry.

### Anti-Pattern 2: Ability Tier as a Separate Stored Field

**What people do:** Add a `CharacterAbilityTier` Django model, update it when domain scores change.

**Why it's wrong:** Tier is derived from domain scores, not independent state. Storing it creates a sync problem — if domain scores change (decay, debug command), tier must also be updated. Two sources of truth.

**Do this instead:** Compute tier at access time via `subclass_engine.get_unlocked_tiers(character)`. It's a pure function of domain scores already stored on `character.db`. Cache in `ndb` per session if profiling shows it in the hot path.

### Anti-Pattern 3: Client Polling for State Updates

**What people do:** Desktop client polls a REST endpoint (e.g., `/api/character/status`) every second to refresh HP bars and other UI state.

**Why it's wrong:** Evennia is event-driven; polling adds unnecessary HTTP round-trips and introduces lag in a real-time game. The websocket connection is already open.

**Do this instead:** Push-only model. Server calls `oob_publisher.push_status(character)` after any state-changing event (taking damage, using a resource, regenerating). Client updates panels when it receives the OOB message.

### Anti-Pattern 4: Area Builder Communicates Directly with Running Server

**What people do:** Build a live-edit HTTP API so the area builder can create rooms in a running Evennia instance without reloading.

**Why it's wrong:** AreaBuilder is idempotent-by-design on server start. Live editing bypasses this, creates partial-build states, and requires server-side auth for the builder tool. It adds complexity with minimal benefit for a solo developer.

**Do this instead:** Builder writes `.py` files to disk. Developer triggers `evennia reload`. The idempotent `build()` function handles the rest. For future multi-author workflows, a git-based review step between file write and reload is the right gate, not a live API.

### Anti-Pattern 5: OOB Types Proliferating Without a Contract

**What people do:** Every engineer adds new `character.msg(my_new_thing=data)` calls ad-hoc as features are built.

**Why it's wrong:** The client must register a handler for every type. Without a central contract, types accumulate, the client breaks on unknown types, and documentation drifts from reality.

**Do this instead:** All OOB pushes go through `oob_publisher.py`. Every type is documented there. Adding a new type requires adding a `push_*` function — this is the natural documentation and change-tracking point.

## Build Order Implications

The dependency chain for the new systems determines the phase order:

1. **Ancestry Engine first** — no upstream dependencies; gates character creation; required before subclass decisions are meaningful. Writes to `character.db`, no new models.

2. **Subclass + Skill Engine second** — subclass engine is a pure read over existing domain scores (no new models required initially). Skill engine needs CharacterSkill model extension (already partially exists).

3. **Ability Registry + Ability Engine third** — depends on subclass engine (for tier gating), world_state (for domain score formulas), zone_scaling (for damage math). Ability data can be authored incrementally per subclass.

4. **Combat Engine fourth** — depends on ability engine. Cannot build combat without the ability effect dispatch layer. Zone scaling math is already available.

5. **OOB Publisher + Client connection layer fifth** — can be built in parallel with combat once the message protocol is understood. Client shows text from day one; OOB panels are progressive enhancement.

6. **GUI Area Builder last** — depends on nothing server-side. Can be built at any time. Must be complete before zone content authoring begins (per PROJECT.md constraint). Outputs AreaBuilder `.py` files already supported by the existing server.

## Sources

- Evennia Webclient Protocol: https://www.evennia.com/docs/latest/Components/Webclient.html
- Evennia Messagepath: https://www.evennia.com/docs/latest/Concepts/Messagepath.html
- Evennia Godot Websocket Contrib (message format example): https://www.evennia.com/docs/latest/Contribs/Contrib-Godotwebsocket.html
- Evennia Protocols: https://www.evennia.com/docs/latest/Concepts/Protocols.html
- Evennia Traits Contrib: https://www.evennia.com/docs/latest/Contribs/Contrib-Traits.html
- Evennia Contribs Overview: https://www.evennia.com/docs/latest/Contribs/Contribs-Overview.html
- Tauri 2.0 Architecture: https://v2.tauri.app/concept/architecture/
- Tauri WebSocket Plugin: https://v2.tauri.app/plugin/websocket/
- Electron vs Tauri comparison (2025): https://www.dolthub.com/blog/2025-11-13-electron-vs-tauri/
- AnyRPG Ability System Architecture: https://docs.anyrpg.org/architecture/ability-system
- Evennia webclient.py source: https://github.com/evennia/evennia/blob/main/evennia/server/portal/webclient.py

---
*Architecture research for: Soravelon MUD — ability system, desktop client, GUI area builder*
*Researched: 2026-03-24*
