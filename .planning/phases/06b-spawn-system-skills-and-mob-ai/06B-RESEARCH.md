# Phase 06b: Spawn System, Skills & Mob AI - Research

**Researched:** 2026-03-26
**Domain:** Mob spawn runtime, general proficiency skills, mob ability AI enhancements
**Confidence:** HIGH

## Summary

This phase has three major subsystems: (1) SpawnRecord-based spawn/respawn runtime that replaces the current Twisted callLater approach with a DB-backed model + global ticker, (2) the full 20+ general proficiency skill system with three improvement methods and ancestry seeds, and (3) mob ability AI enhancements for casting time, conditions, and is_hunter pathfinding. All three domains have comprehensive vault specs and existing code to integrate with.

The existing `world/mob_spawner.py` from Phase 3.1 provides the spawn foundation -- condition evaluation, patrol attachment, zone spawn, single/named mob creation, and callLater respawn. Phase 6b evolves this to SpawnRecord-backed respawn (DB model + 60s ticker) and adds `mob.db.spawn_record_id` for efficient death-to-respawn lookup. The CharacterSkill Django model already exists in `world/models.py` and matches the vault spec closely. The combat_ai.py module from Phase 6a has weight-based selection, condition checking, scripted sequences, and flee behavior -- Phase 6b extends it with casting time mechanics, mob ability cooldown tracking integration, and the is_hunter chase behavior.

**Primary recommendation:** Build SpawnRecord model + migration first (unblocks spawn_tick and death hook), then skill engine + commands in parallel, then mob AI casting/is_hunter last since combat_ai.py already handles the core loop.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** SpawnRecord Django model tracks live state per spawn slot (room_id, spawn_index, active_mob_ids, respawn_at). Per vault spec in soravelon-spawn-system.md.
- **D-02:** Single global TickerHandler (60s interval) processes all pending respawns in one indexed DB query. NOT per-mob Scripts. Same efficient pattern as existing tickers.
- **D-03:** Spawn condition vocabulary: None (always), node_failure_above_N, node_active, quest_complete:id (stub -> False), time_of_day:period (stub -> True), unknown (log warning, spawn anyway).
- **D-04:** Death hook schedules respawn: mob.at_death() finds SpawnRecord, removes mob from active_mob_ids, schedules respawn_at when all mobs in slot are dead.
- **D-05:** Named mob handling: prestige_modifier (1.5-3.0), long respawn (2-8 hours), zone-wide announcement on respawn (not first spawn), first-engage lore description. Death writes WorldEventLog entry.
- **D-06:** Store mob.db.spawn_record_id at creation time for direct SpawnRecord lookup on death (avoid JSONField __contains query that doesn't work in SQLite).
- **D-07:** Zone initialization on server start: initialize_spawn_records() creates SpawnRecord entries for all spawn definitions. Idempotent -- existing records preserved across restarts.
- **D-08:** Call-for-help cap: max 3 additional mobs per combat encounter. Tracked on room.ndb.call_for_help_count, reset on combat end.
- **D-09:** Weighted priority list for ability selection. Each mob ability has a weight (0.0-1.0) and optional condition. Higher weight = more likely to fire when off cooldown. Abilities authored per-mob template as data dicts (NOT from shared registry).
- **D-10:** ALL mobs have at least 1-2 abilities, not just named/elite mobs. Normal mobs get simple abilities. Magic/Rare/Legendary get progressively more.
- **D-11:** Casting time mechanic: spells with cast_time > 0 telegraph (emote fires at cast start). Resolves on round N+cast_time. Players can interrupt via Stun or Root during cast window.
- **D-12:** Mob ability cooldowns tracked on mob.ndb.ability_cooldowns dict. Cleared on death. Decremented at round end.
- **D-13:** Condition vocabulary for mob abilities: null (no condition), pack_present, hp_below_50, hp_below_25, target_rooted, target_blinded, no_target_dot.
- **D-14:** Named mob scripted sequences: trigger types (combat_start, hp_below_X, round_N, target_flees, on_death). Action types (echo, ability, spawn, call_for_help, modify_behavior, zone_echo).
- **D-15:** is_hunter flag: mobs with this flag use BFS pathfinding to chase players across rooms within detection range. NOT all aggressive mobs -- only explicitly flagged ones.
- **D-16:** Full 20+ general proficiency system. All skills from vault: Lockpicking, Animal Handling, Beast Training, Herbalism, Tracking, Climbing, Persuasion, Intimidation, Swimming, First Aid, Appraisal, Stealth, Foraging, Node Reading, Navigation, Fishing, Engineering (craft), Cooking, Smithing, Alchemy (craft), PLUS new "Reflexes" skill (passive combat speed factor).
- **D-17:** More passive-effect skills welcome (both combat + exploration). Combat passives provide MARGINAL mechanical effects (flavor-level, not competitive). The reason to train is CONTENT ACCESS -- high skill levels unlock quest options and dialogue. Not power.
- **D-18:** Three improvement methods per vault: Passive use (session accumulator in ndb, batch-commit), Deliberate practice (24hr rolling cooldown per skill), Trainer sessions (cost Scales, raise gain ceiling).
- **D-19:** Diminishing returns by tier: 0-25 full rate, 26-50 75%, 51-75 40%, 76-90 10%, 91-100 2%. Same curve as domain XP.
- **D-20:** Ancestry skill seeds wire into ancestry_engine.py's set_ancestry(). Veth (formerly Rodentia): Stealth 20, Navigation 25, Lockpicking 10, Tracking (underground) 25. Kau'roran: Swimming 30, Fishing 25, Beast Training 20, Persuasion 15. Human: no seeds. Selvar North: Tracking 20, Climbing 15, Intimidation 10. Selvar South: Lockpicking 15, Appraisal 15, Persuasion 10, Navigation (coastal) 20.
- **D-21:** Skill display command filtered by category: 'skills' shows summary. 'skills general' shows general proficiencies. 'skills attunement' shows zone/node/creature. Only non-zero skills shown.
- **D-22:** Zone attunement (one per zone, 50 at launch), Node attunement (one per node type, 5), Creature attunement (one per creature type, ~30). Total ~105 skills.
- **D-23:** Attunement threshold unlocks per vault: 25 (sensory detail), 50 (hidden exits/objects), 75 (mob patterns/stabilization), 90 (enhanced magic/early warning), 100 (unique lore fragment).
- **D-24:** Build framework for hidden discovery triggers (skill combo conditions that unlock lore fragments). Framework exists even if no discoveries authored yet. Checks run when skills change thresholds.
- **D-25:** Quest system checks skill values at runtime for skill-gated content. Skills don't know about quests -- clean separation.

### Claude's Discretion
- SpawnRecord migration details
- Ticker registration in at_server_start()
- Skill registry format (Python dicts like ability_registry.py vs YAML)
- Exact passive-effect skill list beyond Reflexes
- Trainer NPC data model details
- is_hunter detection range default value

### Deferred Ideas (OUT OF SCOPE)
- Full crafting system with materials/ingredients -- Phase 6c (basic) or dedicated crafting phase
- Threat engine (taunt, aggro tables) -- post-launch
- Quest spawn system -- quest system not built yet, stub condition evaluator
- Time-of-day spawns -- time system not built, stub returns True
- Full creature attunement list -- depends on complete mob roster from content phase
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CMB-04 | Group combat uses existing group engine for proximity and loot | Already marked complete; group combat was wired in 6a. Spawn system creates mobs that participate in group encounters. No additional work needed for this requirement. |
| SKL-01 | General proficiency skills (0-100) with learn-by-use progression | CharacterSkill model exists, skill_engine.py + SKILL_DEFINITIONS registry + ndb accumulators needed. Vault spec fully defined. |
| SKL-02 | 4 profession tracks: Cooking, Smithing, Alchemy, Scholarly Research | These are general proficiency skills in D-16 list. Skill engine handles them identically to other general skills. No separate profession system -- just skill_type="general" entries. |
| SKL-03 | Animal Handling skill track (0-100) with Dragon Handling unlock at 100 | Part of D-16 skill list. CharacterSkill record with skill_id="animal_handling". Threshold check at 100 unlocks dragon handling content (quest-gated, not mechanical). |
| SKL-04 | Profession progression is independent of domain/guild system | By design -- CharacterSkill model has no FK to CharacterGuild. Skill values read from their own table. Domain scores affect passive gain rate (domain bonus in SKILL_DEFINITIONS) but skills and domains are independent systems. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Django ORM | 6.0.3 | SpawnRecord model, CharacterSkill queries | Already the project's data layer |
| Evennia TICKER_HANDLER | 6.0.0 | spawn_tick 60s global ticker | Same pattern as 4 existing tickers |
| Twisted reactor.callLater | 24.11.0 | is_hunter chase delay (one-shot), NOT spawn respawn | Existing pattern in mob_spawner.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| django.utils.timezone | 6.0.3 | SpawnRecord.respawn_at datetime comparisons | All respawn scheduling |
| evennia.utils.delay | 6.0.0 | Named mob respawn announcements (brief delay) | Zone-wide echo timing |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| SpawnRecord DB model | Twisted callLater (current) | callLater doesn't survive server restarts; DB model is crash-safe |
| Python dict skill registry | YAML files | Python dicts match ability_registry.py pattern, no additional parser needed |
| Per-mob Script for respawn | Global ticker | 1500 scripts vs 1 ticker query -- ticker wins at scale |

## Architecture Patterns

### Recommended Project Structure
```
world/
  mob_spawner.py          # EXTEND: add SpawnRecord integration, spawn_tick(), initialize_spawn_records()
  skill_engine.py         # NEW: skill progression, practice, accumulator, discovery framework
  skill_definitions.py    # NEW: SKILL_DEFINITIONS dict, ANCESTRY_SKILL_SEEDS, TRAINER_REGISTRY
  combat_ai.py            # EXTEND: casting time tracking, is_hunter chase logic
  combat_script.py        # EXTEND: casting time round processing, mid-combat spawn handling
  models.py               # EXTEND: SpawnRecord model, add WorldEventLog to models.py body
  ancestry_engine.py      # EXTEND: set_ancestry() calls _apply_skill_seeds()
commands/
  skill_commands.py       # NEW: CmdSkills, CmdPractice, CmdTrain
tests/
  test_skill_engine.py    # NEW: skill progression, diminishing returns, practice cooldown
  test_spawn_record.py    # NEW: SpawnRecord lifecycle, spawn_tick, death hook
```

### Pattern 1: SpawnRecord Lifecycle
**What:** DB model tracks spawn slot state; global ticker processes due respawns; death hook schedules next respawn.
**When to use:** All mob spawn/respawn flows.
**Example:**
```python
# Death hook (in mob_spawner.py, called from SoravelonMob.at_death)
def schedule_respawn_from_death(mob):
    record_id = mob.db.spawn_record_id
    if not record_id:
        return
    try:
        record = SpawnRecord.objects.get(id=record_id)
    except SpawnRecord.DoesNotExist:
        return
    # Remove this mob from active list
    ids = [mid for mid in record.active_mob_ids if mid != mob.id]
    record.active_mob_ids = ids
    if not ids:
        # All mobs dead -- schedule respawn
        room = _get_room(record.room_id)
        spawn_def = _get_spawn_def(room, record.spawn_index)
        delay_minutes = _roll_respawn_delay(spawn_def)
        record.respawn_at = timezone.now() + timedelta(minutes=delay_minutes)
    record.save()
```

### Pattern 2: Skill ndb Session Accumulator
**What:** Skill use increments ndb counters during gameplay; batch-committed at breakpoints (same as domain XP).
**When to use:** Every passive skill gain event.
**Example:**
```python
# In skill_engine.py
def accumulate_skill_use(character, skill_id, count=1):
    """Add to skill use accumulator. ndb, not persisted until commit."""
    key = f"skill_use_{skill_id}"
    current = getattr(character.ndb, key, 0) or 0
    setattr(character.ndb, key, current + count)

def commit_skill_accumulators(character):
    """Batch-commit all accumulated skill use to DB. Called at breakpoints."""
    from world.skill_definitions import SKILL_DEFINITIONS
    for skill_id in SKILL_DEFINITIONS:
        key = f"skill_use_{skill_id}"
        accumulated = getattr(character.ndb, key, 0) or 0
        if accumulated <= 0:
            continue
        _apply_passive_skill_gain(character, skill_id, accumulated)
        setattr(character.ndb, key, 0)
```

### Pattern 3: Mob Casting Time State
**What:** Mob begins casting on its turn; combat_script tracks pending cast in ndb; resolves N rounds later.
**When to use:** Mob abilities with cast_time > 0.
**Example:**
```python
# In combat_ai.py, when ability has cast_time > 0
def _start_mob_cast(mob, ability, target, combat_handler):
    """Begin a mob cast. Returns echo action for telegraph."""
    pending = dict(combat_handler.ndb.pending_mob_casts or {})
    pending[mob.id] = {
        "ability": ability,
        "target_id": target.id,
        "rounds_left": ability.get("cast_time", 1),
    }
    combat_handler.ndb.pending_mob_casts = pending
    return {"type": "echo", "text": ability.get("emote", "")}
```

### Anti-Patterns to Avoid
- **JSONField __contains for mob-to-SpawnRecord lookup:** SQLite does not support __contains on JSONField. Use mob.db.spawn_record_id (integer FK) for direct lookup instead.
- **Per-use DB writes for skill accumulation:** Dozens of lockpick attempts per session = dozens of DB writes. Use ndb accumulator + batch commit, same as domain XP.
- **Storing skill definitions in DB:** Skill definitions are static game data. Keep as Python dicts (SKILL_DEFINITIONS). Only CharacterSkill records go in DB.
- **Hardcoded skill IDs in game logic:** Use SKILL_DEFINITIONS registry for lookups. Game logic references skill_id strings, not hardcoded behavior.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Respawn timing | Custom timer system | SpawnRecord.respawn_at + TICKER_HANDLER | Crash-safe, single query, proven pattern |
| Diminishing returns curve | Custom math per skill | Reuse DIMINISHING_BRACKETS from world_state.py | Same exact curve (D-19). Import constants. |
| Skill accumulator flush | Custom flush logic | Mirror commit_session_xp() pattern exactly | Same ndb->DB batch pattern. Piggyback on safety flush timer. |
| BFS pathfinding for is_hunter | Custom pathfinding | Reuse patrol_engine.find_path() | Already handles room connectivity, no_mobs exclusion |
| Condition evaluation for spawns | New evaluator | Existing _evaluate_spawn_condition() in mob_spawner.py | Already implemented and tested |

## Common Pitfalls

### Pitfall 1: WorldEventLog Missing from models.py
**What goes wrong:** WorldEventLog exists in migration 0003 and is referenced in world_state.py log_world_event(), but the model class is NOT defined in world/models.py body. Django will error on import.
**Why it happens:** Migration was created but model body was never added to models.py (likely created in a migration-only step).
**How to avoid:** Add WorldEventLog class to models.py BEFORE creating SpawnRecord migration. Verify with `from world.models import WorldEventLog`.
**Warning signs:** ImportError when running `log_world_event()`.

### Pitfall 2: SpawnRecord.active_mob_ids Mutation Safety
**What goes wrong:** JSONField lists on Django models don't auto-detect mutations. Modifying the list in-place won't trigger a save.
**Why it happens:** Django's JSONField stores the value as a Python object; in-place mutations don't mark the field dirty.
**How to avoid:** Always reassign: `record.active_mob_ids = new_list` (never `.append()` or `.remove()` in place). Then call `record.save()`.
**Warning signs:** active_mob_ids appears unchanged after death hook runs.

### Pitfall 3: SaverDict Copy Pattern for Skill Seeds
**What goes wrong:** If ancestry skill seeds are written by iterating and setting db attributes in a loop, each assignment re-pickles the entire SaverDict.
**Why it happens:** Evennia's db attributes use SaverDict which pickles on every __setattr__.
**How to avoid:** For ancestry seeds, create CharacterSkill records via Django ORM (bulk_create or get_or_create), NOT via character.db attributes. Skills live in the CharacterSkill model, not on db.
**Warning signs:** Slow character creation with many seed skills.

### Pitfall 4: Skill Practice Cooldown Rolling 24hr vs Server Reset
**What goes wrong:** If practice cooldown resets at server midnight instead of rolling 24hr from last practice, players can game it by practicing just before midnight.
**Why it happens:** Implementing global reset instead of per-skill rolling timestamp.
**How to avoid:** Store `last_practiced_at` per CharacterSkill record. Check `timezone.now() - last_practiced_at >= timedelta(hours=24)`. Never use a global clock reset.
**Warning signs:** Players practicing twice in quick succession around midnight.

### Pitfall 5: mob_spawner.py at_death() Already Has Respawn Logic
**What goes wrong:** The current SoravelonMob.at_death() already calls `_schedule_respawn()` from mob_spawner.py. Adding SpawnRecord-based respawn without removing the old callLater path creates double-spawn.
**Why it happens:** Two respawn systems running simultaneously.
**How to avoid:** Replace the callLater _schedule_respawn() call in at_death() with SpawnRecord-based schedule_respawn_from_death(). Remove or deprecate _schedule_respawn().
**Warning signs:** Mobs appearing twice after death timer fires.

### Pitfall 6: Casting Time Interrupt Check
**What goes wrong:** Mob starts casting, gets stunned/rooted mid-cast, but cast still resolves because interrupt check happens at wrong time.
**Why it happens:** Interrupt check must happen at resolution time (when rounds_left hits 0), not at cast start.
**How to avoid:** At cast resolution, check if mob has stun/root effect. If so, cancel the cast. The status_effects module has `has_effect(target, "stun")` and `has_effect(target, "root")`.
**Warning signs:** Stunned mobs still completing spells.

### Pitfall 7: Selvar Skill Seeds Differ by Coat (North vs South)
**What goes wrong:** Selvar skill seeds vary by lineage (North/South), but character.db.selvar_coat stores "summer"/"winter" not "north"/"south".
**Why it happens:** Coat and lineage may be the same character creation choice, but the mapping needs to be explicit.
**How to avoid:** Map summer coat -> South lineage, winter coat -> North lineage in ANCESTRY_SKILL_SEEDS. Or add a separate character.db.selvar_lineage field. Confirm with vault spec: CONTEXT.md D-20 lists them separately.
**Warning signs:** All Selvar getting the same seeds regardless of coat.

## Code Examples

### SpawnRecord Model
```python
# world/models.py
class SpawnRecord(models.Model):
    """Tracks live state of each spawn slot. One per spawn_definition per room."""
    room_id = models.IntegerField(db_index=True)
    spawn_index = models.IntegerField()
    mob_template = models.CharField(max_length=64)
    active_mob_ids = models.JSONField(default=list)
    respawn_at = models.DateTimeField(null=True, db_index=True)
    is_named = models.BooleanField(default=False)
    named_id = models.CharField(max_length=128, blank=True, default="")

    class Meta:
        unique_together = [("room_id", "spawn_index")]
        indexes = [
            models.Index(fields=["respawn_at"]),
            models.Index(fields=["is_named"]),
        ]
```

### WorldEventLog Model (Missing from models.py -- add it)
```python
# world/models.py -- this model exists in migration 0003 but NOT in models.py body
class WorldEventLog(models.Model):
    """Significant world events for LLM context and named mob tracking."""
    event_type = models.CharField(max_length=64, db_index=True)
    zone_id = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    faction_id = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    character_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    data = models.JSONField(default=dict)
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["event_type", "occurred_at"]),
            models.Index(fields=["zone_id", "occurred_at"]),
            models.Index(fields=["faction_id", "occurred_at"]),
        ]
```

### spawn_tick() Global Ticker
```python
# world/mob_spawner.py
def spawn_tick(*args, **kwargs):
    """Called every 60s by TickerHandler. Processes all due respawns."""
    from django.utils import timezone
    from world.models import SpawnRecord

    due = SpawnRecord.objects.filter(
        respawn_at__lte=timezone.now(),
        respawn_at__isnull=False,
    )
    for record in due:
        room = _resolve_room(record.room_id)
        if not room:
            record.delete()
            continue
        spawn_defs = room.db.spawn_definitions or []
        if record.spawn_index >= len(spawn_defs):
            record.delete()
            continue
        spawn_def = spawn_defs[record.spawn_index]
        _attempt_spawn(room, spawn_def, record)
```

### Skill Definitions Registry (Claude's Discretion: Python dicts)
```python
# world/skill_definitions.py
SKILL_DEFINITIONS = {
    "lockpicking": {
        "name": "Lockpicking",
        "skill_type": "general",
        "category": "general",
        "description": "Pick locks and bypass mechanical security.",
        "domain_bonus": "subterfuge",  # faster passive gain with this domain
        "thresholds": {
            25: "Basic locks opened without tools",
            50: "Complex locks, some magical wards",
            75: "Master locks, warded containers",
            90: "Dragon-era locks, ancient mechanisms",
            100: "Any lock in the known world",
        },
        "trainer_required_above": 50,
    },
    # ... 20+ entries
}

ANCESTRY_SKILL_SEEDS = {
    "human": {},
    "kauroran": {
        "swimming": 30,
        "fishing": 25,
        "beast_training": 20,
        "persuasion": 15,
    },
    "veth": {
        "stealth": 20,
        "navigation": 25,
        "lockpicking": 10,
        "tracking": 25,
    },
    "selvar_north": {
        "tracking": 20,
        "climbing": 15,
        "intimidation": 10,
    },
    "selvar_south": {
        "lockpicking": 15,
        "appraisal": 15,
        "persuasion": 10,
        "navigation": 20,
    },
}
```

### Deliberate Practice with Rolling Cooldown
```python
# world/skill_engine.py
def practice_skill(character, skill_id):
    """Deliberate practice. 24hr rolling cooldown per skill."""
    from django.utils import timezone
    from datetime import timedelta
    from world.models import CharacterSkill
    from world.skill_definitions import SKILL_DEFINITIONS

    defn = SKILL_DEFINITIONS.get(skill_id)
    if not defn:
        return False, f"Unknown skill: {skill_id}"

    record, _ = CharacterSkill.objects.get_or_create(
        character=character,
        skill_id=skill_id,
        defaults={"skill_type": defn["skill_type"], "value": 0.0},
    )

    # Rolling 24hr cooldown check
    if record.last_practiced_at:
        cooldown_end = record.last_practiced_at + timedelta(hours=24)
        if timezone.now() < cooldown_end:
            remaining = cooldown_end - timezone.now()
            hours = int(remaining.total_seconds() // 3600)
            return False, f"You practiced {defn['name']} recently. Try again in {hours}h."

    # Calculate practice gain using diminishing returns
    gain = _calculate_practice_gain(record.value)
    record.value = min(100.0, record.value + gain)
    record.last_practiced_at = timezone.now()
    record.save()

    return True, f"[{defn['name']}: {record.value - gain:.0f} -> {record.value:.0f}]"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Twisted callLater respawn | SpawnRecord DB model + ticker | Phase 6b | Respawn survives server restart |
| No skill system | CharacterSkill model + skill_engine.py | Phase 6b | 20+ trackable skills with progression |
| Basic mob AI (weight select) | + Casting time, is_hunter chase | Phase 6b | Mobs telegraph spells, hunters chase across rooms |

## Existing Code Gap Analysis

### mob_spawner.py (Phase 3.1) -- What Exists vs What's New

**Already exists:**
- `_evaluate_spawn_condition()` -- full condition vocabulary implemented and tested
- `spawn_single_mob()` -- creates mob, sets attributes, calls initialize_for_spawn
- `spawn_named_mob()` -- condition check, prestige_modifier, mob_id tag, respawn broadcast
- `spawn_room_mobs()` -- iterates spawn_definitions, checks conditions, counts existing
- `spawn_zone()` -- finds rooms by zone tag, calls spawn_room_mobs
- `_maybe_attach_patrol()` -- resolves patrol definitions, attaches PatrolScript
- `_schedule_respawn()` -- Twisted callLater one-shot (TO BE REPLACED)
- `_count_room_mobs()` -- counts by mob key or mob_id tag

**New for Phase 6b:**
- `SpawnRecord` model + migration
- `spawn_tick()` -- global 60s ticker callback
- `initialize_spawn_records()` -- creates SpawnRecord entries on server start
- `_attempt_spawn()` -- spawn_tick helper (condition check + mob creation + record update)
- `schedule_respawn_from_death()` -- replaces _schedule_respawn(), uses SpawnRecord
- Integration: mob.db.spawn_record_id set at spawn time
- Integration: at_server_start() registers spawn_tick and calls initialize_spawn_records()
- Death hook rewrite in SoravelonMob.at_death() to use SpawnRecord instead of callLater

### CharacterSkill Model -- Gap Analysis

**Existing model (world/models.py):**
```python
CharacterSkill:
  character (FK)
  skill_id (CharField 128)
  skill_type (CharField 32, choices: general/zone_attunement/node_attunement/creature_attunement)
  value (FloatField, default 0.0)
  last_practiced_at (DateTimeField, nullable)
  Meta: unique_together (character, skill_id), index on (character, skill_type)
```

**Vault spec requires:**
```python
CharacterSkill:
  character_id
  skill_id
  skill_type
  value (float 0-100)
  last_practiced_at (timestamp, nullable)
  use_accumulator -- NOT in model, stored on ndb during session
```

**Verdict: Model matches vault spec exactly.** The `use_accumulator` is correctly kept on ndb per vault design. No model changes needed for CharacterSkill.

### combat_ai.py (Phase 6a) -- What Exists vs What's New

**Already exists:**
- `CONDITION_CHECKS` dict with target_below_50hp, self_below_50hp, target_has_poison/bleed/burn, no_allies_alive, allies_present
- `check_condition()` -- evaluates condition strings
- `select_mob_action()` -- weight-based selection with cooldown filtering
- `get_mob_target()` -- last-attacker priority, vanish check, room check
- `check_scripted_sequence()` -- trigger types: combat_start, hp_below_X, round_N, target_flees, on_death
- `execute_sequence_action()` -- echo, ability, spawn, call_for_help, modify_behavior, zone_echo
- `process_mob_turn()` -- main entry: sequences -> flee -> target -> action
- `_should_flee()` -- flee_low_hp threshold check
- `CALL_FOR_HELP_CAP = 3` -- already enforced

**New for Phase 6b:**
- Add missing condition keys from D-13: `pack_present`, `target_rooted`, `target_blinded`, `no_target_dot` (partially covered by existing checks but key names differ)
- Casting time tracking: `_start_mob_cast()` in process_mob_turn, pending cast state in combat_handler.ndb
- Cast interrupt check at resolution time (stun/root cancels cast)
- is_hunter chase behavior: BFS pathfinding to chase fleeing players

**Condition mapping (existing -> vault):**
| Vault condition | Existing key | Status |
|-----------------|-------------|--------|
| pack_present | allies_present | Name matches intent, may rename |
| hp_below_50 | self_below_50hp | Different key, same logic |
| hp_below_25 | self_below_25hp | Different key, same logic |
| target_rooted | (missing) | Add: check has_effect(target, "root") |
| target_blinded | (missing) | Add: check has_effect(target, "blind") |
| no_target_dot | (missing) | Add: check no active DoT on target |

### WorldEventLog -- Fix Required
WorldEventLog exists in migration 0003 but is NOT in world/models.py. The `world_state.log_world_event()` function imports it. This must be fixed before SpawnRecord migration or any code that uses WorldEventLog.

### at_server_startstop.py -- Integration Points
Current tickers registered:
1. `world_state_decay_tick` -- 86400s
2. `session_xp_safety_flush` -- 600s
3. `node_failure_tick` -- 30s
4. `banking_payment_tick` -- 86400s

Phase 6b adds:
5. `mob_spawner.spawn_tick` -- 60s (spawn respawn processing)

After `_load_all_zones()` currently calls `spawn_zone()`. Phase 6b adds `initialize_spawn_records()` call after zone loading.

The skill accumulator flush can piggyback on the existing `session_xp_safety_flush` (600s) by adding `commit_skill_accumulators(char)` inside that callback. No new ticker needed.

## Migration Planning

Current migration chain: 0001 -> 0002 -> 0003 (WorldEventLog) -> 0004 (CharacterGuild) -> 0005 (CharacterAbility)

Phase 6b needs:
- **0006**: Add SpawnRecord model

No CharacterSkill migration needed -- model already exists in 0001_initial.

WorldEventLog model class must be added to models.py body (not a migration -- just adding the class definition that's already migrated).

## Trainer NPC Data Model (Claude's Discretion)

**Recommendation: Static Python dict registry, not Django model.**

Rationale:
- Trainers are authored content, not player-generated data
- Number is small (maybe 30-50 trainers at launch)
- Same pattern as SKILL_DEFINITIONS and ability_registry.py
- No need for runtime CRUD

```python
# world/skill_definitions.py
TRAINER_REGISTRY = {
    "marveth_locksmith": {
        "name": "Marveth",
        "trainer_quality": "journeyman",  # apprentice/journeyman/master
        "skills_taught": ["lockpicking", "appraisal"],
        "cost_per_session": 80,  # Scales
        "location_zone": "vaels_crossing",
        "unlock_condition": None,  # or {"standing": {"guild": 10000}}
    },
    # ... more trainers
}
```

## is_hunter Detection Range (Claude's Discretion)

**Recommendation: Default detection range of 3 rooms.** This is the same as call_for_help call_range default. Configurable per-mob via `mob.db.detection_range`. BFS pathfinding uses `patrol_engine.find_path()` capped at detection_range depth.

```python
DEFAULT_HUNTER_DETECTION_RANGE = 3  # rooms via BFS
```

## Discovery Framework Architecture

The discovery framework checks skill combinations when any skill crosses a threshold boundary (25/50/75/90/100). This is a clean hook in `_apply_skill_gain()`.

```python
# world/skill_engine.py
DISCOVERY_TRIGGERS = [
    {
        "id": "cantera_cognitive_wolves",
        "conditions": {
            "cognitive_node": 90,          # node attunement
            "forest_wolf": 90,             # creature attunement
            "cantera_forest_old_path": 75, # any cantera zone attunement
        },
        "lore_fragment": "lore_cantera_cognitive_001",
        "message": "You notice something about the wolves near this stone...",
    },
    # More discoveries added as content is authored
]

def check_discoveries(character, changed_skill_id, new_value):
    """Check if any discovery triggers fire after a skill change."""
    # Only check on threshold crossings
    thresholds = [25, 50, 75, 90, 100]
    crossed = any(new_value >= t > (new_value - 1) for t in thresholds)
    if not crossed:
        return
    for discovery in DISCOVERY_TRIGGERS:
        _check_single_discovery(character, discovery)
```

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (via `evennia test --settings server.conf.settings tests/`) |
| Config file | pytest runs through Evennia's test runner |
| Quick run command | `evennia test --settings server.conf.settings tests/test_skill_engine.py -x` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SKL-01 | General proficiency 0-100 with learn-by-use | unit | `python -m pytest tests/test_skill_engine.py -x` | No - Wave 0 |
| SKL-02 | 4 profession tracks | unit | `python -m pytest tests/test_skill_engine.py::TestProfessionSkills -x` | No - Wave 0 |
| SKL-03 | Animal Handling with Dragon unlock at 100 | unit | `python -m pytest tests/test_skill_engine.py::TestAnimalHandling -x` | No - Wave 0 |
| SKL-04 | Profession independent of domain | unit | `python -m pytest tests/test_skill_engine.py::TestSkillDomainIndependence -x` | No - Wave 0 |
| CMB-04 | Group combat proximity and loot | unit | Already tested in test_combat_script.py | Yes |
| SPAWN | SpawnRecord lifecycle | unit | `python -m pytest tests/test_spawn_record.py -x` | No - Wave 0 |
| MOB-AI | Casting time, is_hunter | unit | `python -m pytest tests/test_combat_ai.py -x` | Yes (extend) |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/test_skill_engine.py tests/test_spawn_record.py tests/test_combat_ai.py -x`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_skill_engine.py` -- covers SKL-01 through SKL-04, practice cooldown, diminishing returns, ancestry seeds
- [ ] `tests/test_spawn_record.py` -- covers SpawnRecord creation, spawn_tick, death hook, named mob WorldEventLog
- [ ] Extend `tests/test_combat_ai.py` -- casting time, is_hunter, new condition keys

## Open Questions

1. **Selvar lineage mapping to coat**
   - What we know: D-20 lists "Selvar North" and "Selvar South" as separate seed profiles. Character creation stores `character.db.selvar_coat` as "summer"/"winter".
   - What's unclear: Is summer=South and winter=North, or is lineage a separate creation choice?
   - Recommendation: Map winter->North, summer->South (cold climate = northern mountains; warm climate = southern coast). Document mapping explicitly in ANCESTRY_SKILL_SEEDS.

2. **Skill accumulator flush integration**
   - What we know: session_xp_safety_flush fires every 600s for all online characters.
   - What's unclear: Should skill accumulators flush on the same timer, or separately?
   - Recommendation: Piggyback on session_xp_safety_flush -- add `commit_skill_accumulators(char)` call inside the existing callback. One fewer ticker, consistent timing.

3. **is_hunter engagement during patrol**
   - What we know: is_hunter mobs chase fleeing players via BFS. Patrol mobs already have PatrolScript.
   - What's unclear: Does is_hunter override patrol behavior, or do they coexist?
   - Recommendation: is_hunter chase suspends patrol (sets ndb.chasing=True). When chase fails (target lost or out of range), patrol resumes. Chase behavior is checked on patrol tick when mob enters a room and detects a player.

4. **Mid-combat spawn from scripted sequences**
   - What we know: execute_sequence_action returns {"type": "spawn", "mob_key": ..., "count": N}. CombatScript handles it.
   - What's unclear: Where do spawned mobs come from? New mob creation mid-combat? Do they use SpawnRecord?
   - Recommendation: Mid-combat spawns are temporary (no SpawnRecord). Use spawn_single_mob() directly. These mobs die when combat ends or are cleaned up if abandoned.

## Sources

### Primary (HIGH confidence)
- Vault spec: `soravelon-spawn-system.md` -- complete SpawnRecord model, spawn_tick, condition evaluator, named mob handling
- Vault spec: `soravelon-skills.md` -- complete skill system: 20 proficiencies, improvement methods, data models, ancestry seeds
- Vault spec: `soravelon-mobs.md` -- mob ability schema, element/status/targeting/condition vocabularies, scripted sequences
- Vault spec: `soravelon-ancestries.md` -- ancestry skill seeds per ancestry
- Codebase: `world/mob_spawner.py` -- existing spawn foundation from Phase 3.1
- Codebase: `world/combat_ai.py` -- existing mob AI from Phase 6a
- Codebase: `world/models.py` -- existing CharacterSkill model
- Codebase: `world/world_state.py` -- session accumulator + batch commit pattern

### Secondary (MEDIUM confidence)
- Codebase: `world/combat_script.py` -- CombatScript integration points for casting time
- Codebase: `server/conf/at_server_startstop.py` -- ticker registration pattern
- Codebase: `world/ancestry_engine.py` -- set_ancestry() extension point

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all tools are already in use in the project
- Architecture: HIGH -- vault specs are comprehensive and prescriptive, existing patterns established
- Pitfalls: HIGH -- identified from direct code reading (WorldEventLog missing, double-spawn risk, JSONField mutation)

**Research date:** 2026-03-26
**Valid until:** 2026-04-25 (stable -- vault specs locked, codebase well understood)
