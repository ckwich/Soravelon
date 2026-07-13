"""
Global zone registry. Updated by AreaBuilder.build().
Maps zone_id -> ZoneObject dbref for fast zone lookups.

IMPORTANT: Module-level dict, resets on server restart.
Hydrated read-only from the applied manifest and existing ZoneObjects. Do not persist.
"""

_registry = {}  # zone_id -> zone_obj.id (dbref int)


def register_zone(zone_id, zone_obj):
    _registry[zone_id] = zone_obj.id


def get_zone(zone_id):
    import evennia
    zone_obj_id = _registry.get(zone_id)
    if zone_obj_id is None:
        return None
    objs = evennia.search_object("#" + str(zone_obj_id))
    return objs[0] if objs else None


def get_all_zones():
    return list(_registry.keys())


def unregister_zone(zone_id):
    _registry.pop(zone_id, None)


def clear():
    """Clear the registry. Used in tests."""
    _registry.clear()
