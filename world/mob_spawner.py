"""
Mob spawn engine for Soravelon.

Two spawn paths coexist here:

- Legacy room bootstrap helpers used by area loading and older tests:
  spawn_zone() / spawn_room_mobs() / spawn_single_mob() / spawn_named_mob()
- Authoritative runtime respawn flow:
  initialize_spawn_records() / spawn_tick() / schedule_respawn_from_death()

The runtime path uses SpawnRecord rows as the single source of truth for
live slot state. room.db.spawn_definitions remains the authored content
source produced by AreaBuilder.
"""

import random
from datetime import datetime, timedelta

import evennia
from world.tag_search import search_objects_by_exact_tag

try:
    from django.utils import timezone
except Exception:  # pragma: no cover - fallback for pure-logic tests
    class _FallbackTimezone:
        @staticmethod
        def now():
            return datetime.utcnow()

    timezone = _FallbackTimezone()

# Sentinel for detecting explicit vs. missing spawn_def keys
_SENTINEL = object()

# Tag category for identifying named mob instances (used by search_tag for reload detection)
MOB_INSTANCE_TAG_CATEGORY = "mob_instance_id"
SUPPORTED_SPAWN_CONDITIONS = ("node_failure_above_", "node_active")


# ---------------------------------------------------------------------------
# Internal: reactor accessor (allows test patching without module-level import)
# ---------------------------------------------------------------------------

def _get_reactor():
    """Return the Twisted reactor. Import is deferred to avoid module-level Twisted dep."""
    from twisted.internet import reactor
    return reactor


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

    # Unsupported or unknown conditions fail closed. AreaBuilder validation
    # should prevent them from reaching authored production content.
    from evennia.utils import logger
    logger.log_warn(f"[mob_spawner] Unsupported spawn_condition: {condition_str!r}")
    return False


# ---------------------------------------------------------------------------
# Count helpers
# ---------------------------------------------------------------------------

def _count_room_mobs(room, spawn_def):
    """
    Count how many mobs matching spawn_def already exist in room.

    For named mobs (is_named=True): uses evennia.search_tag on the mob_instance_id
    category and filters by location == room. This handles reload detection.

    For normal mobs: iterates room.contents, counts SoravelonMob instances
    whose key matches spawn_def["mob"].

    Returns int.
    """
    from typeclasses.mobs import SoravelonMob

    mob_key = spawn_def["mob"]

    if spawn_def.get("is_named"):
        tagged = search_objects_by_exact_tag(mob_key, MOB_INSTANCE_TAG_CATEGORY)
        return sum(1 for obj in tagged if obj.location is room)

    return sum(
        1 for obj in room.contents
        if isinstance(obj, SoravelonMob)
        and getattr(obj.db, "mob_template_key", None) == mob_key
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

    # Create off-room first. Evennia renders the destination room during
    # first-save if location is set, before template/affix state is installed.
    mob = evennia.create_object(SoravelonMob, key=spawn_def["mob"], location=None)

    mob.db.zone_id = room.db.zone_id
    mob.db.base_disposition = spawn_def.get("base_disposition", 0.0)
    mob.db.trust_sensitive = spawn_def.get("trust_sensitive", False)
    mob.db.named_id = spawn_def.get("named_id")
    mob.db.sequence = spawn_def.get("sequence", [])
    mob.db.spawn_record_id = spawn_def.get("_spawn_record_id")

    # Store whether spawn_def explicitly set flee_threshold (sentinel pattern)
    explicit_flee = spawn_def.get("flee_threshold", _SENTINEL)

    # Apply mob template (sets stats, abilities, behavior from template registry)
    from world.mob_templates import apply_mob_template
    apply_mob_template(mob, spawn_def["mob"])

    # If spawn_def explicitly set flee_threshold, override template value
    if explicit_flee is not _SENTINEL:
        mob.db.flee_threshold = explicit_flee
    elif not hasattr(mob.db, "flee_threshold") or mob.db.flee_threshold is None:
        mob.db.flee_threshold = 20

    mob.initialize_for_spawn(room)
    mob.location = room
    _maybe_attach_patrol(mob, spawn_def, room)

    # Tag wandering mobs for efficient lookup by wander_tick (D-27)
    if mob.db.wander:
        mob.tags.add("wanderer", category="mob_behavior")

    return mob


def spawn_named_mob(spawn_def, room, is_respawn=False):
    """
    Create a named (unique/boss) mob from spawn_def.

    Extends spawn_single_mob with:
      - spawn_condition check (returns None if condition not met)
      - prestige_modifier and tome_drop set on mob
      - mob tagged with spawn_def["mob"] in category=MOB_INSTANCE_TAG_CATEGORY for reload detection
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
    mob.tags.add(spawn_def["mob"], category=MOB_INSTANCE_TAG_CATEGORY)

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
    tagged = search_objects_by_exact_tag(zone_id, "zone_id")

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
        rooms = search_objects_by_exact_tag(room_id_tag, "room_id")
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
# Respawn scheduling
# ---------------------------------------------------------------------------

def _schedule_respawn(spawn_def, room):
    """
    Schedule a one-shot respawn via Twisted reactor.callLater.

    Called from SoravelonMob.at_death() — NOT from initial spawn.

    Delay = respawn_minutes*60 ± respawn_variance*60, minimum 30 seconds.
    Callback only spawns if current count < count_max (D-31).

    Twisted import is deferred inside this function to avoid module-level dep.
    """
    base = spawn_def.get("respawn_minutes", 15) * 60
    variance = spawn_def.get("respawn_variance", 5) * 60
    delay = base + random.uniform(-variance, variance)
    delay = max(delay, 30)  # minimum 30s floor

    def _do_respawn():
        if _count_room_mobs(room, spawn_def) < spawn_def.get("count_max", 1):
            if spawn_def.get("is_named"):
                spawn_named_mob(spawn_def, room, is_respawn=True)
            else:
                spawn_single_mob(spawn_def, room)

    reactor = _get_reactor()
    reactor.callLater(delay, _do_respawn)


# ---------------------------------------------------------------------------
# SpawnRecord runtime
# ---------------------------------------------------------------------------

def _is_respawn(record):
    """Return True if the record is being processed as a timed respawn."""
    return record.respawn_at is not None


def _get_spawn_def_for_record(record, room):
    """Resolve the authored spawn definition for a SpawnRecord."""
    spawn_defs = list(getattr(room.db, "spawn_definitions", None) or [])
    if record.spawn_index < 0 or record.spawn_index >= len(spawn_defs):
        return None
    return dict(spawn_defs[record.spawn_index])


def _spawn_from_record(room, spawn_def, record, is_respawn=False):
    """Spawn one mob for a record-backed slot and tag it with the record ID."""
    runtime_def = dict(spawn_def)
    runtime_def["_spawn_record_id"] = record.id
    if runtime_def.get("is_named"):
        return spawn_named_mob(runtime_def, room, is_respawn=is_respawn)
    return spawn_single_mob(runtime_def, room)


def _process_spawn_record(record):
    """
    Attempt to repopulate one SpawnRecord's slot.

    Missing rooms or invalid spawn indexes delete the record. Failed spawn
    conditions are retried in five minutes.
    """
    room_objs = evennia.search_object(f"#{record.room_id}")
    if not room_objs:
        record.delete()
        return

    room = room_objs[0]
    spawn_def = _get_spawn_def_for_record(record, room)
    if not spawn_def:
        record.delete()
        return

    if not _evaluate_spawn_condition(spawn_def.get("spawn_condition"), room):
        record.respawn_at = timezone.now() + timedelta(minutes=5)
        record.save()
        return

    count_min = spawn_def.get("count_min", 1)
    count_max = spawn_def.get("count_max", count_min)
    spawn_count = random.randint(count_min, max(count_min, count_max))
    was_respawn = _is_respawn(record)

    mob_ids = []
    for _ in range(spawn_count):
        mob = _spawn_from_record(room, spawn_def, record, is_respawn=was_respawn)
        if mob is not None:
            mob_ids.append(mob.id)

    record.active_mob_ids = mob_ids
    record.respawn_at = None
    record.save()


def spawn_tick():
    """Process all due SpawnRecord rows."""
    from world.models import SpawnRecord

    due_records = SpawnRecord.objects.filter(
        respawn_at__lte=timezone.now(),
        respawn_at__isnull=False,
    )
    for record in due_records:
        try:
            _process_spawn_record(record)
        except Exception:
            from evennia.utils import logger
            logger.log_trace(
                f"[mob_spawner] spawn_tick error processing record "
                f"room={record.room_id} idx={record.spawn_index}"
            )
            continue


def initialize_spawn_records():
    """
    Ensure every authored spawn definition has a SpawnRecord.

    Newly created records are scheduled for immediate population. Existing
    records preserve their active and respawn state across reloads.
    """
    from world.models import SpawnRecord

    all_rooms = list(search_objects_by_exact_tag("soravelon_room", "room_type"))
    if not all_rooms:
        try:
            from evennia.objects.models import ObjectDB
            all_rooms = [
                obj for obj in ObjectDB.objects.filter(db_typeclass_path__contains="rooms.")
            ]
        except Exception:
            all_rooms = []
    for room in all_rooms:
        if room.tags.get("zone_object", category="object_type"):
            continue
        spawn_defs = list(getattr(room.db, "spawn_definitions", None) or [])
        for idx, spawn_def in enumerate(spawn_defs):
            record, created = SpawnRecord.objects.get_or_create(
                room_id=room.id,
                spawn_index=idx,
                defaults={
                    "mob_template_key": spawn_def.get("mob", ""),
                    "active_mob_ids": [],
                    "respawn_at": None,
                    "is_named": spawn_def.get("is_named", False),
                    "named_id": spawn_def.get("named_id") or spawn_def.get("mob", ""),
                },
            )
            if created:
                record.respawn_at = timezone.now()
                record.save()


def schedule_respawn_from_death(mob):
    """
    Remove a dead mob from its SpawnRecord and schedule slot respawn if empty.
    """
    from world.models import SpawnRecord

    record_id = getattr(mob.db, "spawn_record_id", None)
    if not record_id:
        return

    try:
        record = SpawnRecord.objects.get(id=record_id)
    except Exception:
        return

    remaining_ids = [mid for mid in (record.active_mob_ids or []) if mid != mob.id]
    record.active_mob_ids = remaining_ids

    if remaining_ids:
        record.save()
        return

    room = mob.location
    if room is None:
        room_objs = evennia.search_object(f"#{record.room_id}")
        room = room_objs[0] if room_objs else None

    spawn_def = _get_spawn_def_for_record(record, room) if room else None
    if spawn_def:
        base_minutes = spawn_def.get("respawn_minutes", 15)
        variance_minutes = spawn_def.get("respawn_variance", 5)
        variance_offset = random.uniform(-variance_minutes, variance_minutes)
        delay_minutes = max(1.0, base_minutes + variance_offset)
        record.respawn_at = timezone.now() + timedelta(minutes=delay_minutes)

    record.save()
