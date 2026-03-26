---
phase: 06b-spawn-system-skills-and-mob-ai
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - world/models.py
  - world/migrations/0006_spawnrecord.py
  - world/mob_spawner.py
  - typeclasses/mobs.py
  - server/conf/at_server_startstop.py
autonomous: true
requirements: [CMB-04]

must_haves:
  truths:
    - "Mobs respawn on timer after death via SpawnRecord + global ticker"
    - "Named mobs write WorldEventLog on death and announce to zone on respawn"
    - "Server restart preserves spawn state -- existing SpawnRecords not duplicated"
    - "Double-spawn bug eliminated -- callLater respawn replaced with SpawnRecord"
  artifacts:
    - path: "world/models.py"
      provides: "WorldEventLog class body (missing fix) + SpawnRecord model"
      contains: "class WorldEventLog"
    - path: "world/models.py"
      provides: "SpawnRecord model with room_id, spawn_index, active_mob_ids, respawn_at"
      contains: "class SpawnRecord"
    - path: "world/migrations/0006_spawnrecord.py"
      provides: "Django migration for SpawnRecord"
    - path: "world/mob_spawner.py"
      provides: "spawn_tick(), initialize_spawn_records(), schedule_respawn_from_death()"
      exports: ["spawn_tick", "initialize_spawn_records", "schedule_respawn_from_death"]
    - path: "typeclasses/mobs.py"
      provides: "at_death() rewritten to use SpawnRecord instead of callLater"
    - path: "server/conf/at_server_startstop.py"
      provides: "spawn_tick ticker registration + initialize_spawn_records() call"
  key_links:
    - from: "typeclasses/mobs.py"
      to: "world/mob_spawner.py"
      via: "at_death() calls schedule_respawn_from_death()"
      pattern: "schedule_respawn_from_death"
    - from: "server/conf/at_server_startstop.py"
      to: "world/mob_spawner.py"
      via: "TICKER_HANDLER.add + initialize_spawn_records() after _load_all_zones()"
      pattern: "spawn_tick.*initialize_spawn_records"
    - from: "world/mob_spawner.py"
      to: "world/models.py"
      via: "SpawnRecord.objects.filter for due respawns"
      pattern: "SpawnRecord.objects"
---

<objective>
SpawnRecord-backed mob respawn system that replaces Twisted callLater with a crash-safe DB model + global ticker.

Purpose: Current callLater respawn does not survive server restarts. SpawnRecord model makes respawn state persistent and queryable. Named mob deaths write WorldEventLog for respawn announcement tracking. This is the foundation for Phase 7 content zones with reliable mob populations.

Output: WorldEventLog class fix, SpawnRecord model + migration, spawn_tick global ticker, death hook rewrite, server start integration.
</objective>

<execution_context>
@C:\Users\colek\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\colek\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md

@C:\Obsidian\brain\Soravelon\soravelon-spawn-system.md

@world/models.py
@world/mob_spawner.py
@typeclasses/mobs.py
@server/conf/at_server_startstop.py
@world/migrations/0005_characterability.py
</context>

<interfaces>
<!-- Existing interfaces this plan uses and extends -->

From world/models.py:
```python
class CharacterGuild(models.Model):
    # ... last model in file, SpawnRecord goes after
```

From world/mob_spawner.py:
```python
def _evaluate_spawn_condition(condition_str, room): ...
def spawn_single_mob(spawn_def, room): ...
def spawn_named_mob(spawn_def, room, is_respawn=False): ...
def spawn_room_mobs(room): ...
def spawn_zone(zone_obj): ...
def _schedule_respawn(spawn_def, room): ...  # TO BE REPLACED
def _count_room_mobs(room, spawn_def): ...
```

From typeclasses/mobs.py:
```python
class SoravelonMob(DefaultCharacter):
    def at_death(self, killer=None): ...  # TO BE REWRITTEN
```

From server/conf/at_server_startstop.py:
```python
def at_server_start():
    # 4 existing TICKER_HANDLER.add calls
    # initialize_node_pool()
    # _load_all_zones()  # spawn_zone() called inline per zone
```
</interfaces>

<tasks>

<task type="auto">
  <name>Task 1: WorldEventLog fix + SpawnRecord model + migration</name>
  <files>world/models.py, world/migrations/0006_spawnrecord.py</files>
  <action>
**Step 1: Add WorldEventLog class body to world/models.py** (per Pitfall 1 in RESEARCH.md).
This model exists in migration 0003 but the class is MISSING from models.py. Add it after CharacterAbility:

```python
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

    def __str__(self):
        return f"{self.event_type}:{self.zone_id or ''}@{self.occurred_at}"
```

IMPORTANT: Match the migration 0003 schema exactly. This is NOT a new model -- just adding the class body that was omitted.

**Step 2: Add SpawnRecord model** after WorldEventLog per D-01:

```python
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

    def __str__(self):
        return f"room={self.room_id}:idx={self.spawn_index}:template={self.mob_template}"
```

**Step 3: Create migration 0006_spawnrecord.py** via `evennia migrate --makemigrations world` or hand-write. Depends on 0005_characterability. Should ONLY create SpawnRecord (WorldEventLog already migrated in 0003). Verify with `evennia migrate` that it applies cleanly.

Note: If makemigrations tries to create a migration for WorldEventLog changes, use `--name spawnrecord` and verify it detects "no changes" for WorldEventLog (since the DB table already exists from 0003).
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "import django; django.setup(); from world.models import WorldEventLog, SpawnRecord; print('WorldEventLog:', WorldEventLog._meta.db_table); print('SpawnRecord:', SpawnRecord._meta.db_table); print('OK')"</automated>
  </verify>
  <done>WorldEventLog class importable from world.models (was missing). SpawnRecord model defined with room_id, spawn_index, active_mob_ids (JSONField), respawn_at (DateTimeField nullable), is_named, named_id. Migration 0006 applies cleanly.</done>
</task>

<task type="auto">
  <name>Task 2: Spawn ticker + death hook rewrite + server start wiring</name>
  <files>world/mob_spawner.py, typeclasses/mobs.py, server/conf/at_server_startstop.py</files>
  <action>
**Step 1: Extend world/mob_spawner.py** with SpawnRecord integration:

Add `spawn_tick(*args, **kwargs)` -- global 60s ticker callback per D-02:
- Query `SpawnRecord.objects.filter(respawn_at__lte=timezone.now(), respawn_at__isnull=False)`
- For each due record: resolve room via `evennia.search_object("#" + str(record.room_id))`, get spawn_def from `room.db.spawn_definitions[record.spawn_index]`, call existing spawn functions
- On successful spawn: set `record.active_mob_ids = [mob.id, ...]`, set `record.respawn_at = None`, save
- On condition not met: reschedule `record.respawn_at = timezone.now() + timedelta(minutes=5)`, save
- On room/def missing: `record.delete()`
- CRITICAL per D-06: Set `mob.db.spawn_record_id = record.id` on every spawned mob for efficient death lookup

Add `initialize_spawn_records()` per D-07:
- Called after `_load_all_zones()` on server start
- For each room with `spawn_definitions`, do `SpawnRecord.objects.get_or_create(room_id=room.id, spawn_index=idx, defaults={...})`
- New records get `respawn_at = timezone.now()` (schedule immediate spawn)
- Existing records preserved (idempotent across restarts)

Add `schedule_respawn_from_death(mob)` per D-04:
- Uses `mob.db.spawn_record_id` for direct SpawnRecord lookup (NOT JSONField __contains per D-06/Pitfall in research)
- Remove mob.id from `record.active_mob_ids` (reassign list, never mutate in place per Pitfall 2)
- If all mobs dead: calculate delay from spawn_def (respawn_minutes +/- respawn_variance, min 1 minute), set `record.respawn_at`
- `record.save()`

Also update existing `spawn_single_mob()` and `spawn_named_mob()`:
- After mob creation, if a `record` parameter is passed, set `mob.db.spawn_record_id = record.id`
- The spawn_tick path passes the record; the initial zone spawn path (spawn_room_mobs) does NOT have records yet (they're created by initialize_spawn_records)

Remove or mark `_schedule_respawn()` as deprecated (keep the function but have it log a warning and no-op, or remove entirely since at_death will call the new function).

**Step 2: Rewrite SoravelonMob.at_death()** in typeclasses/mobs.py:

Replace the old `_schedule_respawn()` call at the bottom of at_death() with:
```python
# Schedule respawn via SpawnRecord (replaces callLater)
from world.mob_spawner import schedule_respawn_from_death
schedule_respawn_from_death(self)
```

Add named mob WorldEventLog writing per D-05:
```python
# Named mob death: write WorldEventLog entry
is_named = self.tags.get("mob_id", category="mob_id") is not None
if is_named and killer:
    from world.models import WorldEventLog
    WorldEventLog.objects.create(
        event_type="named_mob_death",
        zone_id=self.db.zone_id or "",
        character_id=killer.id if killer else None,
        description=f"{self.key} was slain by {killer.key}",
        data={"named_id": self.db.named_id or self.key, "mob_key": self.key},
    )
```

Also add `self.db.spawn_record_id = None` in `at_object_creation()` for the db attribute convention.

**Step 3: Wire at_server_startstop.py:**

In `at_server_start()`, add spawn_tick TICKER_HANDLER registration (60s interval per D-02):
```python
TICKER_HANDLER.add(
    interval=60,
    callback="world.mob_spawner.spawn_tick",
    idstring="spawn_tick",
    persistent=True,
)
```

After `_load_all_zones()`, add:
```python
from world.mob_spawner import initialize_spawn_records
initialize_spawn_records()
```

Update the named mob respawn announcement in spawn_tick: when `record.is_named` and the spawn succeeds, use `_announce_named_mob_respawn()` which checks WorldEventLog for previous deaths (not first spawn). The vault spec says announcement is a zone-wide echo to all rooms tagged with the zone_id. Use vague text: "Something stirs in the distance." per vault spec.
  </action>
  <verify>
    <automated>cd /c/Dev/Evennia/soravelon && python -c "import django; django.setup(); from world.mob_spawner import spawn_tick, initialize_spawn_records, schedule_respawn_from_death; print('spawn_tick:', callable(spawn_tick)); print('initialize_spawn_records:', callable(initialize_spawn_records)); print('schedule_respawn_from_death:', callable(schedule_respawn_from_death)); print('OK')"</automated>
  </verify>
  <done>spawn_tick() processes due SpawnRecords every 60s. schedule_respawn_from_death() replaces _schedule_respawn() using mob.db.spawn_record_id for direct lookup. initialize_spawn_records() creates idempotent records on server start. SoravelonMob.at_death() uses SpawnRecord path and writes WorldEventLog for named mobs. Ticker registered in at_server_start(). No callLater respawn path remains.</done>
</task>

</tasks>

<verification>
- `from world.models import WorldEventLog, SpawnRecord` succeeds
- `from world.mob_spawner import spawn_tick, initialize_spawn_records, schedule_respawn_from_death` succeeds
- `_schedule_respawn` is removed or deprecated in mob_spawner.py
- SoravelonMob.at_death() no longer calls `_schedule_respawn()`
- at_server_start() has 5 TICKER_HANDLER entries (4 existing + spawn_tick)
- Migration 0006 applies: `evennia migrate`
</verification>

<success_criteria>
SpawnRecord model tracks mob spawn slot state in the DB. Global 60s ticker processes due respawns. Death hook schedules respawn via SpawnRecord (not callLater). Named mob deaths create WorldEventLog entries. Server restart preserves spawn state.
</success_criteria>

<output>
After completion, create `.planning/phases/06b-spawn-system-skills-and-mob-ai/06b-01-SUMMARY.md`
</output>
