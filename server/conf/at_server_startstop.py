"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_init()
at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""


def at_server_init():
    """
    This is called first as the server is starting up, regardless of how.
    """
    pass


def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    from evennia import TICKER_HANDLER

    # World-state decay — fires every 24 real hours (86400 seconds)
    TICKER_HANDLER.add(
        interval=86400,
        callback="world.world_state.world_state_decay_tick",
        idstring="world_state_decay",
        persistent=True,
    )

    # Session XP safety flush — fires every 10 minutes (600 seconds)
    TICKER_HANDLER.add(
        interval=600,
        callback="world.world_state.session_xp_safety_flush",
        idstring="session_xp_flush",
        persistent=True,
    )

    # Node failure tick — fires every 30 seconds
    TICKER_HANDLER.add(
        interval=30,
        callback="world.node_helpers.node_failure_tick",
        idstring="node_failure_tick",
        persistent=True,
    )

    # Banking recurring payment processing — daily
    TICKER_HANDLER.add(
        interval=86400,
        callback="world.banking.banking_payment_tick",
        idstring="banking_payment_tick",
        persistent=True,
    )

    # Mob spawn ticker — processes due SpawnRecords every 60s (D-02)
    TICKER_HANDLER.add(
        interval=60,
        callback="world.mob_spawner.spawn_tick",
        idstring="spawn_tick",
        persistent=True,
    )

    # NPC ambient idle echoes — fires every 15 seconds (NPC-01)
    TICKER_HANDLER.add(
        interval=15,
        callback="world.dialogue_engine.ambient_npc_tick",
        idstring="npc_ambient_tick",
        persistent=True,
    )

    # Recover any orphaned Layer 1 rooms from crash/restart
    from world.node_helpers import initialize_node_pool
    initialize_node_pool()

    # Load all area files from world/areas/ — rebuilds zone registry
    # and room spawn definitions fresh each restart (idempotent)
    _load_all_zones()

    # Create SpawnRecord entries for all spawn_definitions (idempotent, D-07)
    from world.mob_spawner import initialize_spawn_records
    initialize_spawn_records()


def _load_all_zones():
    """
    Load all area files from world/areas/ on server start.
    Idempotent — safe to call on restart.

    Two-pass loading (BLD-06):
      Pass 1 — all zones build normally; cross-zone exits may fail if
               the target zone hasn't loaded yet.
      Pass 2 — retry all unresolved cross-zone exits now that all zones
               are in DB.
    """
    import os
    import importlib
    import json
    from django.conf import settings
    from world import zone_registry
    from world.area_builder import clear_unresolved_exits, get_unresolved_exits
    import evennia as _evennia

    # Clear registries before rebuild
    zone_registry.clear()
    clear_unresolved_exits()

    areas_dir = os.path.join(settings.GAME_DIR, "world", "areas")
    if not os.path.exists(areas_dir):
        return

    # --- Pass 1: load all zone files (.py and .zone.json) ---
    for filename in sorted(os.listdir(areas_dir)):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = f"world.areas.{filename[:-3]}"
            try:
                if module_name in importlib.sys.modules:
                    importlib.reload(importlib.sys.modules[module_name])
                else:
                    importlib.import_module(module_name)
                module = importlib.sys.modules[module_name]
                if hasattr(module, "build"):
                    report = module.build()
                    warnings = report.get("warnings", [])
                    for w in warnings:
                        if "target zone may not be loaded yet" not in w:
                            print(f"Zone warning [{filename}]: {w}")
                    unresolved = report.get("unresolved_exits", [])
                    if unresolved:
                        print(
                            f"Zone [{filename}]: {len(unresolved)} "
                            f"cross-zone exit(s) deferred to second pass"
                        )
                    zone_id = report.get("zone_id")
                    if zone_id:
                        from world.mob_spawner import spawn_zone
                        zone_objs = _evennia.search_tag("zone_object", category="object_type")
                        zone_obj = next((o for o in zone_objs if o.db.zone_id == zone_id), None)
                        if zone_obj:
                            count = spawn_zone(zone_obj)
                            if count:
                                print(f"Zone [{filename}]: spawned {count} mob(s)")
            except Exception as e:
                import traceback
                print(f"Error loading zone {filename}: {e}")
                traceback.print_exc()
        elif filename.endswith(".zone.json"):
            filepath = os.path.join(areas_dir, filename)
            try:
                from world.zone_serializer import load_zone_from_json
                with open(filepath, "r") as f:
                    zone_data = json.load(f)
                report = load_zone_from_json(zone_data)
                warnings = report.get("warnings", [])
                for w in warnings:
                    if "target zone may not be loaded yet" not in w:
                        print(f"Zone warning [{filename}]: {w}")
                unresolved = report.get("unresolved_exits", [])
                if unresolved:
                    print(
                        f"Zone [{filename}]: {len(unresolved)} "
                        f"cross-zone exit(s) deferred to second pass"
                    )
                zone_id = report.get("zone_id")
                if zone_id:
                    from world.mob_spawner import spawn_zone
                    zone_objs = _evennia.search_tag("zone_object", category="object_type")
                    zone_obj = next((o for o in zone_objs if o.db.zone_id == zone_id), None)
                    if zone_obj:
                        count = spawn_zone(zone_obj)
                        if count:
                            print(f"Zone [{filename}]: spawned {count} mob(s)")
            except ImportError:
                print(
                    f"Skipping {filename}: zone_serializer not available"
                )
            except Exception as e:
                import traceback
                print(f"Error loading zone {filename}: {e}")
                traceback.print_exc()

    # --- Pass 2: retry all unresolved cross-zone exits (BLD-06) ---
    all_unresolved = get_unresolved_exits()
    if not all_unresolved:
        return

    resolved_count = 0
    still_unresolved = 0
    for exit_data in all_unresolved:
        target_str = exit_data["to"]
        target_zone_id, target_room_id = target_str.split(":", 1)

        candidates = _evennia.search_tag(target_room_id, category="room_id")
        target = None
        for room in candidates:
            if (room.db.zone_id or "") == target_zone_id:
                target = room
                break

        if not target:
            print(
                f"Cross-zone exit STILL unresolved after second pass: "
                f"{target_str} (zone not loaded)"
            )
            still_unresolved += 1
            continue

        from_room = exit_data["from_room"]
        direction = exit_data["direction"]
        kwargs = {
            k: v for k, v in exit_data.items()
            if k not in ("from_room", "to", "direction")
        }
        try:
            from world.area_builder import AreaBuilder
            _retry_builder = AreaBuilder.__new__(AreaBuilder)
            _retry_builder._zone_id = from_room.db.zone_id or "unknown"
            _retry_builder._exits_created = 0
            _retry_builder._create_exit_object(
                from_room, target, direction, **kwargs
            )
            resolved_count += 1
        except Exception as e:
            print(f"Error resolving cross-zone exit {target_str}: {e}")
            still_unresolved += 1

    print(
        f"Second pass: resolved {resolved_count} cross-zone exit(s), "
        f"{still_unresolved} still unresolved"
    )


def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
