"""Django transactions that also repair Evennia's shared runtime caches."""

from __future__ import annotations

from contextlib import contextmanager
from numbers import Integral

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


class EvenniaCacheTracker:
    """Snapshot ObjectDB locations/Attributes for rollback cache repair."""

    def __init__(self):
        self._objects = {}
        self._attributes = {}

    def track(self, obj, *, attributes=()):
        object_id = getattr(obj, "id", None)
        if not isinstance(object_id, Integral) or isinstance(object_id, bool):
            return obj
        tracked_objects = self._objects.setdefault(object_id, [])
        if not any(existing is obj for existing in tracked_objects):
            tracked_objects.append(obj)
        for name in attributes:
            attribute = obj.attributes.get(name, return_obj=True)
            self._attributes.setdefault(
                (object_id, name),
                (
                    attribute is not None,
                    attribute.value if attribute is not None else None,
                ),
            )
        return obj

    def repair(self):
        from evennia.objects.models import ObjectDB
        from evennia.utils.dbserialize import to_pickle

        for object_id, objects in self._objects.items():
            for obj in objects:
                try:
                    stale_location_id = obj.__dict__.get("db_location_id")
                    stored_location_id = ObjectDB.objects.filter(
                        pk=object_id,
                    ).values_list("db_location_id", flat=True).get()
                    obj.pk = object_id
                    obj.__dict__["db_location_id"] = stored_location_id
                    obj._state.fields_cache.pop("db_location", None)
                    obj.attributes.reset_cache()
                    for (
                        (tracked_id, name),
                        (existed, value),
                    ) in self._attributes.items():
                        if tracked_id != object_id or not existed:
                            continue
                        attribute = obj.attributes.get(name, return_obj=True)
                        if attribute is not None:
                            # The database already rolled back. Repair only the
                            # idmapper-retained in-memory model value.
                            attribute.db_value = to_pickle(value)
                    for location_id in {
                        stale_location_id,
                        stored_location_id,
                    } - {None}:
                        location = ObjectDB.objects.filter(pk=location_id).first()
                        if location:
                            location.contents_cache.init()
                except ObjectDoesNotExist:
                    obj.flush_from_cache(force=True)


@contextmanager
def atomic_evennia_state(*objects):
    """Open a DB transaction and repair tracked caches if it rolls back."""

    tracker = EvenniaCacheTracker()
    for obj in objects:
        tracker.track(obj)
    try:
        with transaction.atomic():
            yield tracker
    except Exception:
        tracker.repair()
        raise
