"""
Mob spawn engine for Soravelon.

Stateless functions that read spawn_definitions from rooms and produce
SoravelonMob instances with affixes, combat stats, patrol scripts, and
respawn timers.

Key call chain:
  spawn_zone(zone_obj) → spawn_room_mobs(room) → spawn_single_mob / spawn_named_mob
    → mob.initialize_for_spawn(room)   (affixes + combat stats)
    → _maybe_attach_patrol(mob, ...)   (PatrolScript if patrol def found)

Respawn (SpawnRecord-backed, crash-safe):
  schedule_respawn_from_death(mob) — called from SoravelonMob.at_death()
  spawn_tick() — 60s global ticker processes due SpawnRecords
  initialize_spawn_records() — called on server start after _load_all_zones()

Decision refs: D-01 through D-31 in 03.1-CONTEXT.md, D-01 through D-08 in 06b-CONTEXT.md
"""

import random
from datetime import timedelta

import evennia
from django.utils import timezone


# ---------------------------------------------------------------------------
# Condition evaluation
# ---------------------------------------------------------------------------

def _evaluate_spawn_condition(condition_str, room):
    """
    Evaluate a spawn_condition string against current game state.

    Returns True if the mob should spawn, False if the condition is not met.
    If condition_str is None or empty, always returns True.

    Supported conditions:
      node_failure_above_N  — zone node failure float >= N
      node_active           — node state in ("active", "critical")
      quest_complete:id     — stub; always False until quest system built
      time_of_day:period    — stub; always True until time system built
    """
    if not condition_str:
        return True

    # node_failure_above_N
    if condition_str.startswith("node_failure_above_"):
        threshold = int(condition_str.split("_")[-1])
        from world.node_helpers import get_node_script
        zone_id = room.db.zone_id or ""
        script = get_node_script(zone_id)
        if not script:
            return False
        return (script.db.failure or 0) >= threshold

    # node_active
    if condition_str == "node_active":
        from world.node_helpers import get_node_script
        zone_id = room.db.zone_id or ""
        script = get_node_script(zone_id)
        if not script:
            return False
        state = script.db.state or "dormant"
        return state in ("active", "critical")

    # quest_complete:quest_id — stub until quest system built
    if condition_str.startswith("quest_complete:"):
        return False

    # time_of_day:period — stub until time system built
    if condition_str.startswith("time_of_day:"):
        return True

    # Unknown condition — log warning, spawn anyway
    print(f"[mob_spawner] Unknown spawn_condition: {condition_str!r}")
    return True


# ---------------------------------------------------------------------------
# Count helpers
# ---------------------------------------------------------------------------

def _count_room_mobs(room, spawn_def):
    """
    Count how many mobs matching spawn_def already exist in room.

    For named mobs (is_named=True): uses evennia.search_tag on the mob_id
    category and filters by location == room. This handles reload detection.

    For normal mobs: iterates room.contents, counts SoravelonMob instances
    whose key matches spawn_def["mob"].

    Returns int.
    """
    from typeclasses.mobs import SoravelonMob

    mob_key = spawn_def["mob"]

    if spawn_def.get("is_named"):
        tagged = evennia.search_tag(mob_key, category="mob_id")
        return sum(1 for obj in tagged if obj.location is room)

    return sum(
        1 for obj in room.contents
        if isinstance(obj, SoravelonMob) and obj.key == mob_key
    )


# ---------------------------------------------------------------------------
# Core spawn functions
# ---------------------------------------------------------------------------

def spawn_single_mob(spawn_def, room):
    """
    Create one SoravelonMob instance from spawn_def, place it in room.

    Sets: zone_id, base_disposition, trust_sensitive, flee_threshold.
    Calls: mob.initialize_for_spawn(room) → affixes + combat stats.
    Calls: _maybe_attach_patrol(mob, spawn_def, room).

    Returns the created mob object.
    """
    from typeclasses.mobs import SoravelonMob

    mob = evennia.create_object(SoravelonMob, key=spawn_def["mob"], location=room)

    mob.db.zone_id = room.db.zone_id
    mob.db.base_disposition = spawn_def.get("base_disposition", 0.0)
    mob.db.trust_sensitive = spawn_def.get("trust_sensitive", False)
    mob.db.flee_threshold = spawn_def.get("flee_threshold", 20)

    mob.initialize_for_spawn(room)
    _maybe_attach_patrol(mob, spawn_def, room)

    return mob


def spawn_named_mob(spawn_def, room, is_respawn=False):
    """
    Create a named (unique/boss) mob from spawn_def.

    Extends spawn_single_mob with:
      - spawn_condition check (returns None if condition not met)
      - prestige_modifier and tome_drop set on mob
      - mob tagged with spawn_def["mob"] in category="mob_id" for reload detection
      - Room broadcast on respawn (not first spawn)

    Args:
        spawn_def (dict): Spawn definition with is_named=True.
        room: Evennia room object.
        is_respawn (bool): True if this is a timer-driven respawn.

    Returns the mob object, or None if spawn_condition prevents spawn.
    """
    if not _evaluate_spawn_condition(spawn_def.get("spawn_condition"), room):
        return None

    mob = spawn_single_mob(spawn_def, room)
    mob.db.prestige_modifier = spawn_def.get("prestige_modifier", 1.0)
    mob.db.tome_drop = spawn_def.get("tome_drop")
    mob.tags.add(spawn_def["mob"], category="mob_id")

    if is_respawn:
        room.msg_contents(f"|y{spawn_def['mob']} has returned.|n")

    return mob


def spawn_room_mobs(room):
    """
    Spawn mobs for all spawn_definitions on room.

    For each definition:
      1. Check spawn_condition — skip if not met (D-03 preserve intent)
      2. Count existing mobs in room for this def
      3. Spawn up to count_min if existing < count_min

    D-03: On server reload, rooms at or above count_min are NOT re-spawned.

    Returns int: total mobs spawned.
    """
    spawned = 0
    for spawn_def in (room.db.spawn_definitions or []):
        if not _evaluate_spawn_condition(spawn_def.get("spawn_condition"), room):
            continue

        existing = _count_room_mobs(room, spawn_def)
        needed = max(0, spawn_def.get("count_min", 1) - existing)

        for _ in range(needed):
            if spawn_def.get("is_named"):
                mob = spawn_named_mob(spawn_def, room, is_respawn=False)
            else:
                mob = spawn_single_mob(spawn_def, room)
            if mob is not None:
                spawned += 1

    return spawned


def spawn_zone(zone_obj):
    """
    Spawn mobs for all rooms in the zone.

    Finds rooms via evennia.search_tag(zone_id, category="zone_id").
    Filters out the zone_obj itself (tagged "zone_object" in object_type).
    Calls spawn_room_mobs(room) on each qualifying room.

    Returns int: total mobs spawned across the zone.
    """
    zone_id = zone_obj.db.zone_id
    tagged = evennia.search_tag(zone_id, category="zone_id")

    total = 0
    for obj in tagged:
        # Exclude the zone object itself
        if obj.tags.get("zone_object", category="object_type"):
            continue
        # Only process objects that have spawn_definitions (rooms)
        if not hasattr(obj, "db"):
            continue
        total += spawn_room_mobs(obj)

    return total


# ---------------------------------------------------------------------------
# Patrol attachment
# ---------------------------------------------------------------------------

def _maybe_attach_patrol(mob, spawn_def, room):
    """
    Attach a PatrolScript to mob if a matching patrol definition is found.

    Looks up zone_obj via get_zone_obj_for_room(room), searches
    zone_obj.db.patrol_definitions for an entry where mob_key == spawn_def["mob"].

    If found: resolves route_room_ids → dbref ints via search_tag, attaches
    PatrolScript, and sets db.route_ids and db.patrol_def on the script.

    D-04: Rooms tagged no_mobs (category="room_flag") are excluded from routing —
    this is enforced in patrol_engine.find_path(); mob_spawner trusts the route.
    """
    from world.zone_scaling import get_zone_obj_for_room

    zone_obj = get_zone_obj_for_room(room)
    if not zone_obj:
        return

    patrol_defs = zone_obj.db.patrol_definitions
    if not patrol_defs:
        return

    mob_key = spawn_def["mob"]
    matched_def = None
    for pd in patrol_defs:
        if pd.get("mob_key") == mob_key:
            matched_def = pd
            break

    if not matched_def:
        return

    # Resolve route_room_ids → dbref ints
    zone_id = room.db.zone_id
    resolved_route_ids = []
    for room_id_tag in matched_def.get("route_room_ids", []):
        rooms = evennia.search_tag(room_id_tag, category="room_id")
        for r in rooms:
            # Match by zone to avoid cross-zone collisions
            if getattr(r, "db", None) and r.db.zone_id == zone_id:
                resolved_route_ids.append(r.id)
                break

    from world.scripts.patrol_script import PatrolScript

    mob.scripts.add(PatrolScript)
    script_list = mob.scripts.get(key="patrol_script")
    if not script_list:
        return
    script = script_list[0]
    script.db.route_ids = resolved_route_ids
    script.db.patrol_def = matched_def


# ---------------------------------------------------------------------------
# SpawnRecord-backed respawn system (replaces Twisted callLater)
# ---------------------------------------------------------------------------

def initialize_spawn_records():
    """
    Create SpawnRecord entries for all rooms with spawn_definitions.

    Called after _load_all_zones() on server start. Idempotent — existing
    records are preserved across restarts (D-07).

    New records get respawn_at=now() to trigger immediate first spawn via
    spawn_tick(). Existing records keep their current state.
    """
    from world.models import SpawnRecord

    rooms = evennia.search_tag("zone_id", category="zone_id")
    created = 0
    for room in rooms:
        if room.tags.get("zone_object", category="object_type"):
            continue
        spawn_defs = room.db.spawn_definitions
        if not spawn_defs:
            continue
        for idx, sdef in enumerate(spawn_defs):
            _, was_created = SpawnRecord.objects.get_or_create(
                room_id=room.id,
                spawn_index=idx,
                defaults={
                    "mob_template": sdef.get("mob", "unknown"),
                    "active_mob_ids": [],
                    "respawn_at": timezone.now(),
                    "is_named": sdef.get("is_named", False),
                    "named_id": sdef.get("mob", "") if sdef.get("is_named") else "",
                },
            )
            if was_created:
                created += 1

    if created:
        print(f"[mob_spawner] Created {created} new SpawnRecord(s)")


def spawn_tick(*args, **kwargs):
    """
    Global 60s ticker callback. Processes all SpawnRecords with due respawns.

    Queries SpawnRecord.objects.filter(respawn_at__lte=now, respawn_at__isnull=False)
    and attempts to respawn mobs for each due record (D-02).
    """
    from world.models import SpawnRecord

    now = timezone.now()
    due_records = SpawnRecord.objects.filter(
        respawn_at__lte=now, respawn_at__isnull=False
    )

    for record in due_records:
        try:
            _process_spawn_record(record)
        except Exception as e:
            print(f"[mob_spawner] Error processing SpawnRecord {record.id}: {e}")


def _process_spawn_record(record):
    """Process a single due SpawnRecord: resolve room, spawn mob, update record."""
    # Resolve room
    results = evennia.search_object(f"#{record.room_id}")
    if not results:
        print(f"[mob_spawner] Room #{record.room_id} not found, deleting SpawnRecord {record.id}")
        record.delete()
        return

    room = results[0]
    spawn_defs = room.db.spawn_definitions
    if not spawn_defs or record.spawn_index >= len(spawn_defs):
        print(f"[mob_spawner] spawn_definitions missing for record {record.id}, deleting")
        record.delete()
        return

    spawn_def = spawn_defs[record.spawn_index]

    # Check spawn condition
    if not _evaluate_spawn_condition(spawn_def.get("spawn_condition"), room):
        # Condition not met — reschedule for 5 minutes from now
        record.respawn_at = timezone.now() + timedelta(minutes=5)
        record.save()
        return

    # Spawn the mob(s)
    is_named = spawn_def.get("is_named", False)
    is_respawn = _is_respawn(record)

    if is_named:
        mob = spawn_named_mob(spawn_def, room, is_respawn=is_respawn)
    else:
        mob = spawn_single_mob(spawn_def, room)

    if mob is None:
        # Spawn failed (condition in spawn_named_mob)
        record.respawn_at = timezone.now() + timedelta(minutes=5)
        record.save()
        return

    # Link mob to SpawnRecord (D-06)
    mob.db.spawn_record_id = record.id

    # Update record
    active_ids = list(record.active_mob_ids or [])
    active_ids.append(mob.id)
    record.active_mob_ids = active_ids
    record.respawn_at = None
    record.save()

    # Named mob respawn announcement (D-05)
    if is_named and is_respawn:
        _announce_named_mob_respawn(record, room, spawn_def)


def _is_respawn(record):
    """Check if this is a respawn (not first spawn) by looking for prior deaths."""
    from world.models import WorldEventLog

    if not record.is_named:
        return False

    # For named mobs, check WorldEventLog for prior death
    return WorldEventLog.objects.filter(
        event_type="named_mob_death",
        data__named_id=record.named_id,
    ).exists()


def _announce_named_mob_respawn(record, room, spawn_def):
    """
    Zone-wide echo when a named mob respawns (D-05).

    Only fires if WorldEventLog has a prior death for this named mob.
    Uses vague text per vault spec.
    """
    zone_id = room.db.zone_id
    if not zone_id:
        return

    zone_rooms = evennia.search_tag(zone_id, category="zone_id")
    for r in zone_rooms:
        if r.tags.get("zone_object", category="object_type"):
            continue
        r.msg_contents("|ySomething stirs in the distance.|n")


def schedule_respawn_from_death(mob):
    """
    Schedule a respawn via SpawnRecord after mob death (D-04).

    Uses mob.db.spawn_record_id for direct lookup (D-06, avoids JSONField
    __contains query that doesn't work in SQLite).

    Removes mob.id from active_mob_ids. When all mobs in the slot are dead,
    calculates delay and sets respawn_at.
    """
    from world.models import SpawnRecord

    record_id = mob.db.spawn_record_id
    if not record_id:
        return

    try:
        record = SpawnRecord.objects.get(id=record_id)
    except SpawnRecord.DoesNotExist:
        return

    # Remove this mob from active list (reassign, never mutate in place)
    active_ids = [mid for mid in (record.active_mob_ids or []) if mid != mob.id]
    record.active_mob_ids = active_ids

    if not active_ids:
        # All mobs in this slot are dead — schedule respawn
        room = mob.location
        if room and room.db.spawn_definitions:
            spawn_defs = room.db.spawn_definitions
            if record.spawn_index < len(spawn_defs):
                spawn_def = spawn_defs[record.spawn_index]
                base = spawn_def.get("respawn_minutes", 15)
                variance = spawn_def.get("respawn_variance", 5)
                delay_minutes = base + random.uniform(-variance, variance)
                delay_minutes = max(delay_minutes, 1)  # minimum 1 minute
                record.respawn_at = timezone.now() + timedelta(minutes=delay_minutes)
            else:
                record.respawn_at = timezone.now() + timedelta(minutes=15)
        else:
            record.respawn_at = timezone.now() + timedelta(minutes=15)

    record.save()
