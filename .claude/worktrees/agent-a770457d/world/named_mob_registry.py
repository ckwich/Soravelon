"""
Global named mob registry. Updated by AreaBuilder.build().
Maps mob_id -> {zone_id, room_id, definition}.

Module-level dict, rebuilt on every server start by _load_all_zones().
Do not persist -- treat as a startup cache.
"""

_registry = {}


def register_named_mob(mob_id, zone_id, room_obj, definition):
    _registry[mob_id] = {
        "zone_id": zone_id,
        "room_id": room_obj.id,
        "definition": definition,
    }


def get_named_mob(mob_id):
    return _registry.get(mob_id)


def get_all_named_mobs():
    return dict(_registry)


def unregister_named_mob(mob_id):
    _registry.pop(mob_id, None)


def clear():
    """Clear the registry. Used in tests."""
    _registry.clear()
