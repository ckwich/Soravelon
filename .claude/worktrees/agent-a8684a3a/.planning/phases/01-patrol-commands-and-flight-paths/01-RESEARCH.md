# Phase 1: Patrol, Commands, and Flight Paths - Research

**Researched:** 2026-03-24
**Domain:** Evennia scripting, command system extension, BFS pathfinding, trigger/action systems
**Confidence:** HIGH

## Summary

Phase 1 delivers four interconnected server-side systems: PatrolScript (tick-driven BFS mob routing with disposition-aware combat engagement), a shared action vocabulary + trigger system (event-driven world interaction for rooms/mobs/items), command prefix resolution + player aliases (custom CmdSet wrapper with prefix matching and alias expansion), and the Dragon Courier flight network (multi-leg timed traversal with discovery gating and faction pricing).

All four systems are pure server-side Python on top of Evennia 6.0 primitives. The codebase already has the key building blocks: `get_rooms_in_radius()` BFS in `world/node_helpers.py`, `get_mob_behavior()` disposition lookup in `world/mob_disposition.py`, `(bool, str)` return conventions in all engine modules, and the SaverDict copy pattern. PatrolScript follows the NodeScript model (persistent, driven externally, `interval` set for self-tick this time). The trigger system is data-driven on room/mob `db.triggers` lists — the action vocabulary is a dispatch dict. The command system wraps Evennia's default `cmdhandler` prefix matching via a custom `CmdSet` merge policy. Flight paths are managed through a new `FlightRegistry` + `FlightScript` per travelling player.

**Primary recommendation:** Build in this order — (1) action vocabulary as a standalone module with no dependencies, (2) PatrolScript using existing BFS + disposition, (3) trigger system using the vocabulary, (4) AreaBuilder extensions for all three, (5) command prefix + alias system, (6) flight path system last (highest complexity, depends on character state and banking).

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Patrol Behavior**
- D-01: Patrol encounter delay is builder-configurable per patrol definition (`encounter_delay` field). Some mobs check disposition instantly on arrival, others emote first then check.
- D-02: Patrol mobs check disposition in BOTH directions — when mob arrives in a room with players AND when a player enters a room containing a patrol mob. Continuous threat awareness.
- D-03: Combat engagement is configurable per mob via `combat_enabled` flag. Caldenmere and other invulnerable mobs set this to false. Guard patrols set it to true.
- D-04: Patrol echo radius is configurable per patrol definition (`echo_radius` field). Uses BFS from mob's current room.

**Action Vocabulary**
- D-05: Implement all action handlers that have backing systems NOW (give_item, take_item via inventory_engine; modify_standing via world_state; log_world_event via WorldEventLog). Only stub actions whose systems don't exist yet (set_quest_flag, open_dialogue, spawn_mob).
- D-06: Add `modify_attunement` action type — uses existing `update_zone_attunement()`.
- D-07: Total action vocabulary: teleport, teleport_to_mob, echo, give_item, take_item, set_quest_flag (stub), modify_standing, spawn_mob (stub), despawn_self, open_dialogue (stub), log_world_event, modify_attunement.

**Flight Paths**
- D-08: Flight points discovered by visiting the room (auto-discover on enter) AND talking to the Dragon Courier NPC to register. Discovery unlocks the point; NPC interaction is required to book flights.
- D-09: Pricing is base fare per leg + Standing discount (Consortium faction). Higher Standing = cheaper flights. Discount tiers TBD by planner.
- D-10: Flights are MULTI-LEG real-time traversal, NOT instant teleport. Each leg takes 30+ seconds with timed echo messages describing geography passing beneath the player. Cost increases per leg.
- D-11: Player can `disembark` at any stop along the route. They are NOT locked to the final destination.
- D-12: During flight, player has full command access except movement commands. Can chat, check inventory, use abilities, read messages — but cannot walk/move.
- D-13: Flight network is a graph with explicit edges defined by builders via `area.flight_point()` (marks a room as a stop) and `area.flight_route()` (defines connection between stops with cost and leg echoes).

**Command Prefix Resolution**
- D-14: Ambiguous prefixes return an error with the match list: "Did you mean: attack, attune?" Player must type more characters. No silent auto-resolution.
- D-15: Player aliases stored in `character.db.aliases` — persistent across sessions and server restarts.
- D-16: Aliases support chaining up to 3 commands via semicolons (e.g., `buff` = `cast shield; cast haste; cast blessing`).
- D-17: Aliases NEVER override system commands.

**Trigger System**
- D-18: Multiple triggers on the same event fire in definition order (list index in `room.db.triggers`). Builder controls priority.
- D-19: Trigger chaining is depth-limited to 3 levels. A teleport trigger can fire on_enter in the destination, but recursion beyond 3 is blocked.

**Custom Command Discoverability**
- D-20: Mob/item descriptions naturally hint at available interactions (builder writes the hints).
- D-21: Custom commands that act as exits/teleports have a `visible_in_exits` boolean. When true, they appear in the room's exit list. When false, they're hidden (quest-gated or discovery-based).

**Patrol Mob Spawning**
- D-22: Tests use `create_object(SoravelonMob)` + attach PatrolScript directly. Architecture must be clean enough that the future spawn system can adopt the same PatrolScript attachment pattern seamlessly.

### Claude's Discretion
- Flight path echo text content and timing (30s minimum per leg, specific messages are creative work)
- Exact Standing discount percentages for flight pricing
- PatrolScript tick interval optimization (currently 1s per the Session 10 prompt — may tune)
- Trigger depth-limit error messaging

### Deferred Ideas (OUT OF SCOPE)
- Time of day system (on_time_of_day triggers stored but cannot fire until time system exists)
- Quest flag checking in conditions (set_quest_flag action is stubbed)
- NPC dialogue integration (open_dialogue action is stubbed)
- Mob spawn runtime system (spawn_mob action is stubbed; patrol mobs created manually for now)
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| IWA-01 | Patrol system with BFS pathfinding drives mob route-following behavior | PatrolScript uses `get_rooms_in_radius()` BFS pattern; `find_path()` is a shortest-path adaptation of same traversal |
| IWA-02 | Patrol mobs check disposition against players on room arrival and break for combat | `get_mob_behavior()` already returns "aggressive"/"territorial"/"passive"/"friendly"; PatrolScript calls it on arrival + new `at_object_receive()` hook |
| IWA-03 | Patrol interruption modes work correctly (resume / reset_to_start / abandon) | Stored on patrol definition dict; PatrolScript reads after combat-end callback |
| IWA-04 | Custom commands can be attached to rooms, mobs, and items via AreaBuilder | New `area.custom_command()` method; `CmdSet.add()` called on target object at build time |
| IWA-05 | Shared action vocabulary executes teleport, echo, modify_standing, spawn_mob, and other actions | Dispatch dict in `world/action_vocabulary.py` calling existing engine functions |
| IWA-06 | Trigger system fires on room enter, exit, first visit, mob death, and examine events | Hooks: `SoravelonRoom.at_object_receive()`, `at_object_leave()`, `SoravelonMob.at_death()`, `CmdLook` extension |
| IWA-07 | Triggers support once-per-character and cooldown constraints | `character.db.fired_triggers` set for once-per; `character.db.trigger_cooldowns` dict for timed |
| IWA-08 | AreaBuilder exposes patrol(), custom_command(), and trigger() methods | Three new methods added to `AreaBuilder` class |
| FLT-01 | Dragon Courier Service provides transit between discovered flight points | `FlightRegistry` singleton + `CmdFly` + `FlightScript` per-player |
| FLT-02 | Flight points are discovery-gated (must visit the location first) | `character.db.discovered_flight_points` set; auto-populated in `SoravelonRoom.at_object_receive()` |
| FLT-03 | Multi-leg booking supported for indirect routes | Dijkstra/BFS on flight graph; legs stored as ordered list on FlightScript |
| FLT-04 | Standing-based pricing with faction discounts | `get_standing()` from `world.world_state`; discount tiers applied to base fare before `withdraw()` |
| CMD-01 | Command prefix matching resolves shortest unambiguous prefix | Custom `CmdSet` with `key_mergemode` or intercept layer in `at_pre_cmd()` |
| CMD-02 | Context-sensitive CmdSet scope narrows ambiguity automatically | Evennia CmdSet merge priority; room/mob/item CmdSets added/removed at runtime |
| CMD-03 | Player aliases support up to 3 commands per alias with semicolons | `CmdAlias` + preprocessor hook; stored in `character.db.aliases` |
| CMD-04 | Argument tokens ($1, $2, $*, $@) expand correctly in aliases | Token expansion in alias preprocessor before command dispatch |
| CMD-05 | Aliases never override system commands | Alias lookup only proceeds if no system command matches first |
</phase_requirements>

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia | 6.0 | MUD framework — CmdSet, Scripts, TickerHandler, DefaultCharacter hooks | Already in use; all patterns here are Evennia-native |
| Django ORM | (bundled) | Persistent character state, faction standings, bank balances | Already in use; `(bool, str)` returns + F() atomics established |
| Python stdlib `collections.deque` | 3.11 | BFS queue for pathfinding | No deps; deque is O(1) pop/append |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `evennia.utils.utils.delay()` | 6.0 | Twisted-safe deferred callback for encounter_delay and flight leg timers | Use instead of `time.sleep()` — never block the reactor |
| `evennia.scripts.scripts.DefaultScript` | 6.0 | Base for PatrolScript and FlightScript | Both are persistent tick-driven scripts |
| `evennia.TICKER_HANDLER` | 6.0 | Global tick registration | PatrolScript may use self-ticking interval; FlightScript uses `delay()` |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `delay()` for flight leg timers | FlightScript with interval | `delay()` is simpler for one-shot leg transitions; Script interval better if mid-leg state recovery is needed |
| BFS for `find_path()` | A* | BFS is sufficient for MUD-scale graphs (20-50 rooms); A* adds complexity with no material benefit |
| `character.db.aliases` dict | Django model | `db.*` is correct for per-character persistent data that doesn't need relational queries |

**Installation:** No new packages required. All dependencies are already in the Evennia 6.0 environment.

---

## Architecture Patterns

### Recommended Project Structure

New files this phase:

```
world/
├── action_vocabulary.py     # Dispatch dict + execute_action() entry point
├── patrol_engine.py         # find_path(), patrol encounter logic helpers
├── flight_registry.py       # FlightRegistry: graph of flight points + routes
├── flight_engine.py         # fare_for_route(), book_flight(), disembark()
  scripts/
  └── patrol_script.py       # PatrolScript (SoravelonScript subclass)
  └── flight_script.py       # FlightScript — per-player in-flight state machine
commands/
├── cmd_alias.py             # CmdAlias, CmdUnalias
├── cmd_fly.py               # CmdFly, CmdDisembark, CmdFlightRoutes
├── cmd_prefix_handler.py    # Prefix resolution interceptor (see pattern below)
typeclasses/
└── rooms.py                 # Extended: at_object_receive(), at_object_leave()
└── mobs.py                  # Extended: at_death() trigger firing
```

### Pattern 1: PatrolScript (Self-Ticking Script on Mob)

**What:** A `SoravelonScript` attached to a patrol mob. On each tick it advances the mob one step along its route using BFS pathfinding. On arrival it checks disposition via `get_mob_behavior()` and optionally initiates combat.

**When to use:** Any mob with a `patrol_definition` dict on `mob.db.patrol`.

**Critical rules:**
- PatrolScript attaches to `mob` object (not a ZoneObject). `self.obj` is the mob.
- Use `self.obj.move_to(next_room, quiet=False)` to move — this fires `at_object_leave` and `at_object_receive` hooks on rooms.
- After `move_to()`, check disposition against all players in new room.
- Use `evennia.utils.utils.delay(encounter_delay, callback)` for delayed disposition checks.
- On combat interrupt: store `mob.db.patrol_interrupted = True` and `mob.db.patrol_interrupt_mode` ("resume"/"reset_to_start"/"abandon"). Combat system calls `PatrolScript.on_combat_end()` when fight resolves.

```python
# Source: project pattern — SoravelonScript + Evennia DefaultScript docs
from typeclasses.scripts import SoravelonScript
from world.node_helpers import get_rooms_in_radius

class PatrolScript(SoravelonScript):
    def at_script_creation(self):
        super().at_script_creation()
        self.key = "patrol_script"
        self.persistent = True
        self.interval = 5   # configurable — 5s default, tunable per D-01 guidance
        self.repeats = 0    # infinite
        self.db.route = []           # list of room dbref ints
        self.db.route_index = 0      # current position in route
        self.db.patrol_def = {}      # full patrol definition dict from AreaBuilder
        self.db.interrupted = False
        self.tags.add("patrol_script", category="script_type")

    def at_repeat(self):
        mob = self.obj
        if not mob or mob.db.patrol_interrupted:
            return
        self._advance_route()

    def _advance_route(self):
        from world.patrol_engine import next_patrol_step
        next_room = next_patrol_step(self.obj, self.db.route, self.db.route_index)
        if next_room:
            self.obj.move_to(next_room, quiet=False)
            # move_to fires at_object_receive on destination — disposition check
            # happens there for player-enters-mob-room case (D-02)

    def on_combat_end(self, outcome):
        mode = self.db.patrol_def.get("interrupt_mode", "resume")
        if mode == "reset_to_start":
            self.db.route_index = 0
        elif mode == "abandon":
            self.stop()
        # "resume" — continue from current position
        self.db.interrupted = False
```

### Pattern 2: Action Vocabulary Dispatch

**What:** A single `execute_action(action_dict, context)` function that dispatches to handler functions. Action dict has `action_type` key. Context provides `character`, `mob`, `room`, `item` as needed.

**When to use:** All trigger actions, custom command actions, and any game event that needs a reusable side effect.

```python
# Source: project pattern — world/action_vocabulary.py
ACTION_HANDLERS = {
    "teleport":         _handle_teleport,
    "teleport_to_mob":  _handle_teleport_to_mob,
    "echo":             _handle_echo,
    "give_item":        _handle_give_item,       # calls inventory_engine
    "take_item":        _handle_take_item,       # calls inventory_engine
    "modify_standing":  _handle_modify_standing, # calls world_state.modify_standing
    "modify_attunement": _handle_modify_attunement, # calls world_state.update_zone_attunement
    "log_world_event":  _handle_log_world_event,  # calls world_state.log_world_event
    "despawn_self":     _handle_despawn_self,
    # Stubs:
    "set_quest_flag":   _stub_handler,
    "open_dialogue":    _stub_handler,
    "spawn_mob":        _stub_handler,
}

def execute_action(action_dict, context, _depth=0):
    """
    Execute one action from the vocabulary.
    context = {"character": ..., "room": ..., "mob": ..., "item": ...}
    _depth tracks trigger chain recursion (D-19 limit of 3).
    Returns (bool, str) per project convention.
    """
    if _depth >= 3:
        return False, "Trigger chain depth limit reached."
    action_type = action_dict.get("action_type")
    handler = ACTION_HANDLERS.get(action_type)
    if not handler:
        return False, f"Unknown action type: {action_type}"
    return handler(action_dict, context, _depth)
```

### Pattern 3: Trigger System

**What:** Triggers stored as list of dicts on `room.db.triggers`, `mob.db.triggers`, `item.db.triggers`. Each dict has: `event`, `conditions`, `actions` (list of action dicts), `once_per_character` (bool), `cooldown_seconds` (int).

**When to use:** Any room/mob/item that needs to respond to player interaction events.

**Event hooks to extend:**
- `SoravelonRoom.at_object_receive(obj, source_location)` — fires `on_enter` and `on_first_visit`
- `SoravelonRoom.at_object_leave(obj, target_location)` — fires `on_exit`
- `SoravelonMob.at_death(killer)` — fires `on_mob_death`
- `CmdLook.func()` or an `examine` command — fires `on_examine`

**Cooldown state on character (D-07):**
- `character.db.fired_triggers` — set of `trigger_id` strings for once-per-character
- `character.db.trigger_cooldowns` — dict of `trigger_id: datetime` for cooldown tracking

```python
# Source: project pattern — world/trigger_engine.py
def fire_triggers(source_obj, event_name, character, context=None, _depth=0):
    """
    Fire all triggers on source_obj matching event_name for character.
    Respects once-per-character (D-07) and cooldown (D-07) constraints.
    Enforces depth limit of 3 (D-19).
    """
    triggers = list(source_obj.db.triggers or [])
    ctx = context or {}
    ctx.update({"character": character, "room": character.location})

    for trigger in triggers:
        if trigger.get("event") != event_name:
            continue
        trigger_id = trigger.get("trigger_id")
        if _check_once_per(character, trigger_id, trigger):
            continue
        if _check_cooldown(character, trigger_id, trigger):
            continue
        for action in trigger.get("actions", []):
            from world.action_vocabulary import execute_action
            execute_action(action, ctx, _depth=_depth)
        _record_fired(character, trigger_id, trigger)
```

### Pattern 4: Command Prefix Resolution

**What:** A preprocessing hook that intercepts input before Evennia's cmdhandler. Finds all commands matching the typed prefix. If exactly one match: substitute with full key. If multiple: return error listing matches. If none: pass through unchanged (let Evennia report "command not found").

**Architecture decision:** Implement as an override of `CmdSet.get_cmd()` or as an input preprocessor on the session/character. The cleanest approach in Evennia 6 is to override `CmdSet.get_cmd_exact()` — or more practically, to override `Character.at_pre_cmd_handler()` (if available) or to subclass `Command` with a `parse()` that resolves prefixes.

**Better approach for Evennia 6.0:** Override `cmdhandler` input via a custom `InputFunc` or override `Character.execute_cmd()` to pre-process the input string before passing to the Evennia cmdhandler.

```python
# In typeclasses/characters.py — add to Character class
def execute_cmd(self, raw_string, session=None, **kwargs):
    """Pre-process input for prefix expansion and alias substitution."""
    from world.command_preprocessor import preprocess_input
    processed = preprocess_input(self, raw_string)
    # processed is either the original string, expanded alias commands,
    # or None if an ambiguity error was already sent to the player
    if processed is None:
        return  # Error already sent in preprocess_input
    # Handle semicolon-chained alias expansion (D-16)
    if isinstance(processed, list):
        for cmd_str in processed:
            super().execute_cmd(cmd_str, session=session, **kwargs)
        return
    super().execute_cmd(processed, session=session, **kwargs)
```

**Alias expansion with argument tokens (CMD-04):**

```python
# world/command_preprocessor.py
def expand_alias(character, alias_key, raw_args):
    """
    Expand alias. Supports $1, $2, $*, $@ token substitution.
    Returns list of expanded command strings (max 3 for D-16).
    """
    aliases = character.db.aliases or {}
    if alias_key not in aliases:
        return None
    expansion = aliases[alias_key]
    parts = raw_args.strip().split()
    def _substitute(cmd):
        cmd = cmd.replace("$*", raw_args.strip())
        cmd = cmd.replace("$@", raw_args.strip())
        for i, part in enumerate(parts, 1):
            cmd = cmd.replace(f"${i}", part)
        return cmd
    commands = [c.strip() for c in expansion.split(";")][:3]  # D-16 cap
    return [_substitute(c) for c in commands]
```

### Pattern 5: Flight Path System

**What:** `FlightRegistry` is a module-level singleton dict of `{zone_id: {room_id: FlightPoint}}` and `{(point_a, point_b): FlightRoute}`. Built from AreaBuilder data on server start (same pattern as zone_registry). A `FlightScript` is a per-player script that manages the in-progress journey.

**FlightScript lifecycle:**
1. Player books flight via `CmdFly` — fare deducted atomically, `FlightScript` created with leg list.
2. Each leg: script fires `delay(leg_duration, _advance_leg)`.
3. At each stop: player notified, can `disembark` (stops script, moves to stop room).
4. Final stop: script ends naturally, player arrives.
5. During flight: `in_flight` flag on `character.ndb.in_flight = True` blocks movement commands.

```python
# typeclasses/scripts.py — add FlightScript
class FlightScript(SoravelonScript):
    def at_script_creation(self):
        super().at_script_creation()
        self.key = "flight_script"
        self.persistent = True
        self.interval = 0   # NOT self-ticking; uses delay()
        self.db.legs = []         # list of {from_point, to_point, duration, echoes}
        self.db.current_leg = 0
        self.db.in_transit = True
        self.tags.add("flight_script", category="script_type")

    def start_journey(self):
        self.obj.ndb.in_flight = True
        self._begin_leg()

    def _begin_leg(self):
        if self.db.current_leg >= len(self.db.legs):
            self._arrive_final()
            return
        leg = self.db.legs[self.db.current_leg]
        # Send departure echoes, then schedule arrival
        from evennia.utils.utils import delay
        delay(leg["duration"], self._arrive_at_stop)

    def _arrive_at_stop(self):
        # Move player to stop room, send arrival echoes
        # Player can disembark here
        self.db.current_leg += 1
        if self.db.current_leg < len(self.db.legs):
            self._begin_leg()
        else:
            self._arrive_final()

    def _arrive_final(self):
        self.obj.ndb.in_flight = False
        self.stop()
```

**Movement blocking for D-12:**

```python
# typeclasses/characters.py — extend at_before_move()
def at_before_move(self, destination, **kwargs):
    if getattr(self.ndb, 'in_flight', False):
        self.msg("You cannot move while aboard the Dragon Courier.")
        return False
    # ... existing overload check
```

### Anti-Patterns to Avoid

- **Never call `time.sleep()` in Twisted callbacks.** Use `evennia.utils.utils.delay()` for all deferred execution (flight leg timers, encounter delays).
- **Never query all scripts for a patrol script by scanning `ScriptDB.objects.all()`.** Use tag search: `ScriptDB.objects.get_by_tag("patrol_script", category="script_type")`. Mirror the NodeScript lookup pattern.
- **Never mutate `mob.db.route` in-place** — always copy list, mutate, assign back (SaverDict copy pattern).
- **Never implement prefix matching by subclassing every Command.** Implement once in `execute_cmd()` preprocessor. One entry point.
- **Never build `find_path()` from scratch.** Reuse `get_rooms_in_radius()` BFS in `node_helpers.py`; `find_path()` is the same BFS with a target termination condition and parent-pointer backtracking.
- **Never fire triggers recursively without checking depth.** `_depth` counter must propagate through `execute_action` → trigger handler chain (D-19).
- **Never deduct flight fare with read-modify-write.** Use `banking.withdraw()` which already uses atomic `F()` expression.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Mob movement between rooms | Custom teleport logic | `mob.move_to(room, quiet=False)` | Fires all Evennia room hooks correctly |
| Delayed callbacks (timers) | `threading.Timer` or `time.sleep` | `evennia.utils.utils.delay()` | Thread-safe on Twisted reactor; cancellable |
| Script persistence | Raw Django object storage | `DefaultScript` with `persistent=True` | Automatically survives reload/restart |
| Atomic balance deduction | Read-modify-write on balance | `banking.withdraw()` | Already has `F()` atomic update + overdraft guard |
| Standing lookup | Direct FactionStanding query | `world_state.get_standing()` | Handles lazy record creation (missing = neutral) |
| Zone BFS traversal | New graph traversal | `node_helpers.get_rooms_in_radius()` | Already zone-boundary-aware, tested |
| CmdSet injection at runtime | Direct script manipulation | `obj.cmdset.add(SomeCmdSet)` / `obj.cmdset.remove()` | Evennia's built-in mechanism for dynamic commands |
| Per-player in-flight state | Django model | `character.ndb.in_flight` (volatile) + `FlightScript.db.*` (persistent) | ndb is sufficient for volatile runtime flag; Script `db.*` survives reload |

**Key insight:** Evennia's object hooks (`move_to`, `at_object_receive`, `at_object_leave`, `at_death`) are the canonical integration points. Triggering side effects by overriding these hooks keeps the trigger system decoupled from any specific command.

---

## Common Pitfalls

### Pitfall 1: SaverDict List Mutation
**What goes wrong:** `mob.db.route.append(room_id)` silently fails — Evennia's SaverDict does not propagate in-place mutations on nested lists.
**Why it happens:** `db.*` attributes are pickled; mutating the unpickled copy doesn't trigger re-save.
**How to avoid:** Always: `route = list(mob.db.route or []); route.append(room_id); mob.db.route = route`
**Warning signs:** State changes are lost on the next tick with no exception raised.

### Pitfall 2: Script Tick Fires on Dead/Deleted Mob
**What goes wrong:** PatrolScript fires `at_repeat()` after mob has been deleted or moved to `None` location.
**Why it happens:** Scripts outlive their objects briefly during deletion.
**How to avoid:** Guard every `at_repeat()`: `mob = self.obj; if not mob or not mob.pk: self.stop(); return`
**Warning signs:** AttributeError on `self.obj.location` during patrol tick.

### Pitfall 3: Circular Import in World Modules
**What goes wrong:** `world/action_vocabulary.py` imports from `world/inventory_engine.py` which imports from `typeclasses/objects.py` which imports from `world/...` — ImportError on server start.
**Why it happens:** All `world/` modules are loaded together; circular chains fail at import time.
**How to avoid:** Use lazy imports inside functions (established project pattern): `def _handle_give_item(...): from world.inventory_engine import pick_up; ...`
**Warning signs:** `ImportError` or `cannot import name` on `evennia start`.

### Pitfall 4: Trigger Infinite Recursion
**What goes wrong:** A `teleport` action fires `on_enter` in the destination room, which has another `teleport` trigger — stack overflow.
**Why it happens:** Trigger handlers call `execute_action()`, which calls trigger handlers again.
**How to avoid:** Pass `_depth` counter through all calls; `execute_action()` returns `(False, "depth limit")` at depth >= 3 (D-19).
**Warning signs:** RecursionError in trigger firing code.

### Pitfall 5: Prefix Matching Against Aliases Before System Commands
**What goes wrong:** A player aliases `"n"` to `"go north"` — but `"n"` is also a standard Evennia direction command. Alias fires first, double-movement occurs.
**Why it happens:** Alias expansion happens before system command lookup.
**How to avoid:** In `preprocess_input()`, check if the raw string matches any system command key first (exact match). Only proceed to alias lookup if no system command matched (D-17). Prefix expansion happens on the full merged CmdSet AFTER alias substitution.
**Warning signs:** Movement commands misbehave; `look` cannot be aliased to `l` (it's already a system alias).

### Pitfall 6: Flight Fare Double-Deduction on Script Restart
**What goes wrong:** Server reloads mid-flight. `FlightScript` restarts from `at_script_creation()`, re-deducts the fare.
**Why it happens:** `at_script_creation()` is called on every script instantiation.
**How to avoid:** Deduct fare in `start_journey()`, NOT in `at_script_creation()`. Check `self.db.fare_paid` flag before deducting. `start_journey()` is called once by `CmdFly`, not by the script restart path.
**Warning signs:** Player balance goes negative after server reload mid-flight.

### Pitfall 7: `at_object_receive` fires for non-Character objects
**What goes wrong:** Trigger system fires `on_enter` when an item or mob moves into a room, not just players.
**Why it happens:** `at_object_receive` fires for any object entering the room.
**How to avoid:** In the trigger-firing hook, guard: `if not (hasattr(obj, 'account') and obj.account): return` for player-only triggers. Patrol mobs moving through rooms should NOT fire player-only triggers.
**Warning signs:** Triggers fire spuriously, standing modifiers applied to mobs.

---

## Code Examples

Verified patterns from existing codebase:

### BFS find_path() from existing get_rooms_in_radius()

```python
# Source: world/node_helpers.py — adapted for pathfinding
def find_path(start_room, target_room, max_depth=20):
    """
    BFS shortest path from start_room to target_room.
    Returns list of rooms [start, ..., target] or [] if unreachable.
    Zone-boundary-aware: respects zone_id like get_rooms_in_radius().
    """
    if start_room == target_room:
        return [start_room]
    zone_id = start_room.db.zone_id
    visited = {start_room: None}   # room -> parent
    frontier = [start_room]
    for _ in range(max_depth):
        next_frontier = []
        for room in frontier:
            for exit_obj in room.exits:
                dest = exit_obj.destination
                if (dest and dest not in visited
                        and getattr(dest.db, 'zone_id', None) == zone_id):
                    visited[dest] = room
                    if dest == target_room:
                        # Backtrack
                        path = [dest]
                        cur = room
                        while cur is not None:
                            path.append(cur)
                            cur = visited[cur]
                        return list(reversed(path))
                    next_frontier.append(dest)
        frontier = next_frontier
        if not frontier:
            break
    return []
```

### Script creation + tag pattern (mirrors NodeScript)

```python
# Source: world/scripts/node_script.py — established pattern
class PatrolScript(SoravelonScript):
    def at_script_creation(self):
        super().at_script_creation()
        self.key = "patrol_script"
        self.persistent = True
        self.interval = 5
        self.repeats = 0
        self.tags.add("patrol_script", category="script_type")
```

### Disposition check for patrol encounter (uses existing mob method)

```python
# Source: typeclasses/mobs.py — get_behavior_toward() wraps mob_disposition.py
for obj in destination_room.contents:
    if hasattr(obj, 'account') and obj.account:
        behavior = mob.get_behavior_toward(obj)
        if behavior == "aggressive" and mob.db.combat_enabled:
            # initiate combat
            pass
```

### AreaBuilder idempotent pattern for flight_point()

```python
# Source: world/area_builder.py — mirrors spawn(), named_mob() pattern
def flight_point(self, room, point_id, **kwargs):
    """Mark a room as a Dragon Courier stop."""
    point_def = {
        "point_id": point_id,
        "display_name": kwargs.get("display_name", room.key),
    }
    room.db.flight_point = point_def
    room.tags.add("flight_point", category="travel")
    room.tags.add(point_id, category="flight_point_id")
    # Register in zone-level flight point list
    if not hasattr(self, "_flight_points"):
        self._flight_points = []
    self._flight_points.append((point_id, room, point_def))
```

### withdraw() for flight fare (existing banking pattern)

```python
# Source: world/banking.py — use directly, don't replicate
from world.banking import withdraw
from world.world_state import get_standing

def calculate_fare(base_fare, character):
    standing = get_standing(character, "consortium")
    # Standing -100k to +100k maps to 0% to 30% discount
    discount_pct = max(0.0, min(0.30, (standing / 100_000) * 0.30))
    return int(base_fare * (1.0 - discount_pct))

ok, msg = withdraw(character, fare, description="Dragon Courier fare")
if not ok:
    character.msg(f"Insufficient funds. {msg}")
    return
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Self-ticking scripts with arbitrary intervals | Externally-ticked scripts (interval=0) for zone-wide effects, self-ticking for per-mob effects | NodeScript precedent in this codebase | PatrolScript CAN be self-ticking (per-mob is fine); FlightScript uses delay() |
| Per-command Cmd subclasses for each ability/action | Single dispatcher with action vocabulary | Project decision (research, pre-Phase 1) | All 12 action types go in one module |
| Hardcoded faction checks | `get_mob_behavior()` returning behavior string | mob_disposition.py already written | PatrolScript just calls the existing function |

**Deprecated/outdated:**
- `spawn_with_affixes()` on SoravelonMob: replaced by `initialize_for_spawn()` (backward compat wrapper kept). Patrol test code should use `initialize_for_spawn()`.

---

## Open Questions

1. **PatrolScript tick interval vs. Twisted performance**
   - What we know: CONTEXT.md references "1s" as original discussion target; Claude's Discretion allows tuning.
   - What's unclear: With 20+ patrol mobs in a city zone, 1s interval = 20 DB writes/second minimum.
   - Recommendation: Default to 5s interval. Builder can override via `patrol_def["tick_interval"]`. PatrolScript reads it at creation. Document the performance tradeoff in code comments.

2. **`CmdFly` route discovery — BFS on flight graph vs. precomputed**
   - What we know: Flight graph edges are explicit (D-13). Graph size is small (< 20 points per continent).
   - What's unclear: Whether shortest path needs to account for leg cost or just hop count.
   - Recommendation: BFS on hop count for routing; multiply base_fare per leg for total cost. No precomputed matrix needed at this scale.

3. **Trigger `trigger_id` uniqueness**
   - What we know: Triggers stored as dicts in a list. No explicit ID generation described.
   - What's unclear: How to generate stable trigger IDs for once-per-character tracking across server restarts.
   - Recommendation: Builder assigns explicit `trigger_id` strings (e.g., `"vaels_crossing.east_gate.on_first_visit"`). If not provided, auto-generate from `zone_id:room_id:event:index`. Store as field in trigger dict.

4. **Custom commands on mobs — CmdSet attachment at build time vs. runtime**
   - What we know: `obj.cmdset.add(SomeCmdSet)` is Evennia's runtime API (HIGH confidence).
   - What's unclear: Whether CmdSets attached at build time survive server reload without re-attachment.
   - Recommendation: Re-attach all mob/item/room CmdSets on server start in `_load_all_zones()`. AreaBuilder `custom_command()` stores the definition in `obj.db.custom_commands`; startup hook re-hydrates. This mirrors how zone objects are rebuilt on every start.

---

## Environment Availability

Step 2.6: SKIPPED — This phase is pure server-side Python with no external tool dependencies beyond the existing Evennia 6.0 environment. All required runtimes (Python 3.11, Django, Twisted) are already operational.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Evennia EvenniaTest (unittest-based) |
| Config file | `server/conf/settings.py` via `--settings server.conf.settings` |
| Quick run command | `evennia test --settings server.conf.settings tests/test_patrol_engine.py` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| IWA-01 | `find_path()` returns correct BFS route | unit | `evennia test --settings server.conf.settings tests/test_patrol_engine.py` | Wave 0 |
| IWA-01 | PatrolScript advances mob along route on tick | unit | `evennia test --settings server.conf.settings tests/test_patrol_engine.py` | Wave 0 |
| IWA-02 | Patrol mob triggers disposition check on player in room | unit | `evennia test --settings server.conf.settings tests/test_patrol_engine.py` | Wave 0 |
| IWA-03 | resume/reset_to_start/abandon modes handle post-combat correctly | unit | `evennia test --settings server.conf.settings tests/test_patrol_engine.py` | Wave 0 |
| IWA-04 | custom_command() attaches CmdSet to room/mob/item | unit | `evennia test --settings server.conf.settings tests/test_area_builder.py` | Extends existing |
| IWA-05 | execute_action() dispatches all 12 action types | unit | `evennia test --settings server.conf.settings tests/test_action_vocabulary.py` | Wave 0 |
| IWA-05 | stub actions return (False, stub_message) without error | unit | `evennia test --settings server.conf.settings tests/test_action_vocabulary.py` | Wave 0 |
| IWA-06 | Trigger fires on_enter when player enters room | unit | `evennia test --settings server.conf.settings tests/test_trigger_engine.py` | Wave 0 |
| IWA-06 | Trigger fires on_exit, on_first_visit, on_mob_death, on_examine | unit | `evennia test --settings server.conf.settings tests/test_trigger_engine.py` | Wave 0 |
| IWA-07 | Once-per-character trigger does not fire twice | unit | `evennia test --settings server.conf.settings tests/test_trigger_engine.py` | Wave 0 |
| IWA-07 | Cooldown trigger respects timer | unit | `evennia test --settings server.conf.settings tests/test_trigger_engine.py` | Wave 0 |
| IWA-08 | AreaBuilder patrol(), custom_command(), trigger() methods exist and store correctly | unit | `evennia test --settings server.conf.settings tests/test_area_builder.py` | Extends existing |
| FLT-01 | CmdFly creates FlightScript and debits fare | unit | `evennia test --settings server.conf.settings tests/test_flight_system.py` | Wave 0 |
| FLT-02 | Visiting a flight_point room adds it to discovered_flight_points | unit | `evennia test --settings server.conf.settings tests/test_flight_system.py` | Wave 0 |
| FLT-03 | Multi-leg route calculated correctly by BFS on flight graph | unit | `evennia test --settings server.conf.settings tests/test_flight_system.py` | Wave 0 |
| FLT-04 | Higher Consortium Standing reduces fare | unit | `evennia test --settings server.conf.settings tests/test_flight_system.py` | Wave 0 |
| CMD-01 | Unique prefix resolves to full command | unit | `evennia test --settings server.conf.settings tests/test_command_system.py` | Wave 0 |
| CMD-01 | Ambiguous prefix returns error with match list | unit | `evennia test --settings server.conf.settings tests/test_command_system.py` | Wave 0 |
| CMD-02 | Context CmdSet narrows ambiguity (room-attached cmd takes priority) | unit | `evennia test --settings server.conf.settings tests/test_command_system.py` | Wave 0 |
| CMD-03 | Alias with semicolons expands to 3 commands max | unit | `evennia test --settings server.conf.settings tests/test_command_system.py` | Wave 0 |
| CMD-04 | $1, $2, $*, $@ tokens substitute correctly | unit | `evennia test --settings server.conf.settings tests/test_command_system.py` | Wave 0 |
| CMD-05 | Alias named same as system command does not override system command | unit | `evennia test --settings server.conf.settings tests/test_command_system.py` | Wave 0 |

### Sampling Rate
- **Per task commit:** Run the relevant test file for that task's system
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_patrol_engine.py` — covers IWA-01, IWA-02, IWA-03
- [ ] `tests/test_action_vocabulary.py` — covers IWA-05
- [ ] `tests/test_trigger_engine.py` — covers IWA-06, IWA-07
- [ ] `tests/test_flight_system.py` — covers FLT-01, FLT-02, FLT-03, FLT-04
- [ ] `tests/test_command_system.py` — covers CMD-01, CMD-02, CMD-03, CMD-04, CMD-05
- IWA-04 and IWA-08 extend `tests/test_area_builder.py` (file exists)

---

## Project Constraints (from CLAUDE.md)

All directives from `CLAUDE.md` that apply to Phase 1 implementation:

| Directive | Applies To |
|-----------|-----------|
| Store game state on `db` attributes (persisted) or `ndb` (volatile). Never raw Django fields on typeclasses. | `character.db.aliases`, `character.db.fired_triggers`, `character.ndb.in_flight`, patrol state |
| All game logic lives in `world/` modules; typeclasses call into them. | `world/patrol_engine.py`, `world/action_vocabulary.py`, `world/trigger_engine.py`, `world/flight_engine.py` |
| Custom Django models go in `world/models.py`; register the `world` app for migrations. | FlightPoint/FlightRoute if stored relationally — but preference is `db.*` on ZoneObject per existing pattern |
| Mob behavior is driven by computed disposition — never hardcode friend/foe. | PatrolScript calls `get_mob_behavior()`, never checks `mob.db.faction == "guards"` directly |
| Node failure uses a state machine — respect the tick-driven progression. | PatrolScript must NOT interfere with NodeScript or TICKER_HANDLER node tick |
| Return `(bool, str)` tuples from all engine functions. | `execute_action()`, `book_flight()`, `fire_triggers()`, `find_path()` |
| SaverDict copy pattern for list attribute mutations. | Patrol route index updates, trigger list mutations, alias dict updates |
| Tag-based lookups for zone/room/mob identification. | PatrolScript found via `get_by_tag("patrol_script", ...)` |
| Lazy imports inside methods to avoid circular dependencies. | All cross-module calls in `world/` |
| Tests use Evennia's `EvenniaTestCase` or `EvenniaCommandTestMixin`. | All 5 new test files |

---

## Sources

### Primary (HIGH confidence)
- Existing codebase (`world/node_helpers.py`) — BFS pattern, zone-boundary traversal, get_rooms_in_radius()
- Existing codebase (`world/mob_disposition.py`) — get_mob_behavior() return values, disposition float range
- Existing codebase (`world/area_builder.py`) — idempotent build pattern, SaverDict copy convention
- Existing codebase (`world/banking.py`) — withdraw() atomic F() pattern
- Existing codebase (`world/world_state.py`) — modify_standing(), update_zone_attunement(), log_world_event() signatures
- Existing codebase (`world/scripts/node_script.py`) — Script tag pattern, persistent=True, at_script_creation structure
- Existing codebase (`server/conf/at_server_startstop.py`) — TICKER_HANDLER.add() pattern, zone loading on start
- Existing codebase (`typeclasses/characters.py`) — at_before_move(), at_post_puppet() hook patterns
- Existing codebase (`typeclasses/mobs.py`) — at_death(), get_behavior_toward() wrapping

### Secondary (MEDIUM confidence)
- Evennia 6.0 documentation on `DefaultScript` (interval, persistent, repeats, at_repeat) — confirmed via codebase usage in node_script.py
- Evennia `evennia.utils.utils.delay()` — confirmed usage in existing Evennia contrib patterns; Twisted-safe
- Evennia `obj.cmdset.add()` / `obj.cmdset.remove()` — standard Evennia CmdSet API; used in default contrib packages

### Tertiary (LOW confidence)
- `Character.execute_cmd()` override as prefix interception point — this is the cleanest known approach but needs verification against Evennia 6.0 source before implementation. Alternative: `at_pre_cmd()` hook or session-level `inputfunc` override.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries already in use, no new dependencies
- Architecture patterns: HIGH — all patterns derived from existing codebase conventions
- Pitfalls: HIGH — SaverDict, circular imports, script lifecycle are documented project patterns
- Command prefix architecture: MEDIUM — `execute_cmd()` interception approach is conventional but not yet validated against Evennia 6.0 source
- Flight leg timer (delay() vs interval): MEDIUM — `delay()` confirmed for one-shot; recovery semantics on server reload need verification

**Research date:** 2026-03-24
**Valid until:** 2026-06-24 (stable Evennia 6.0; project conventions are stable)
