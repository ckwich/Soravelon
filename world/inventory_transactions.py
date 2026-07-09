"""Atomic ownership mutations for Soravelon's weight-based inventory.

Every public mutation locks the owning character before item and metadata rows.
That lock order serializes first-time pickup, slot assignment, stacking, and
two-character transfers without treating Evennia containment as a second source
of truth. ``ObjectDB.db_location`` and ``InventoryItem`` commit together.
"""

from __future__ import annotations

from contextlib import contextmanager
from numbers import Integral

from django.db import transaction

from world.models import InventoryItem


class InventoryOwnershipError(RuntimeError):
    """A producer attempted to register contradictory ownership state."""


class _MutationRejected(RuntimeError):
    """Expected gameplay rejection used to unwind an in-progress mutation."""


def _after_write(checkpoint: str) -> None:
    """Failure-injection seam for rollback contract tests."""


class _CacheRepairTracker:
    """Repair Evennia's shared model/Attribute caches after DB rollback."""

    def __init__(self):
        self._objects = {}
        self._attributes = {}

    def track(self, obj, *, attributes=()):
        object_id = getattr(obj, "id", None)
        if not isinstance(object_id, Integral) or isinstance(object_id, bool):
            return obj
        self._objects[object_id] = obj
        for name in attributes:
            attribute = obj.attributes.get(name, return_obj=True)
            self._attributes[(object_id, name)] = (
                attribute is not None,
                attribute.value if attribute is not None else None,
            )
        return obj

    def repair(self):
        from django.core.exceptions import ObjectDoesNotExist
        from evennia.objects.models import ObjectDB
        from evennia.utils.dbserialize import to_pickle

        for object_id, obj in self._objects.items():
            try:
                stale_location_id = obj.__dict__.get("db_location_id")
                stored_location_id = ObjectDB.objects.filter(
                    pk=object_id,
                ).values_list("db_location_id", flat=True).get()
                obj.pk = object_id
                obj.__dict__["db_location_id"] = stored_location_id
                obj._state.fields_cache.pop("db_location", None)
                obj.attributes.reset_cache()
                for (tracked_id, name), (existed, value) in self._attributes.items():
                    if tracked_id != object_id or not existed:
                        continue
                    attribute = obj.attributes.get(name, return_obj=True)
                    if attribute is not None:
                        # The database already rolled back. Repair only the
                        # shared in-memory model that Evennia's idmapper retained.
                        attribute.db_value = to_pickle(value)
                for location_id in {stale_location_id, stored_location_id} - {None}:
                    location = ObjectDB.objects.filter(pk=location_id).first()
                    if location:
                        location.contents_cache.init()
            except ObjectDoesNotExist:
                obj.flush_from_cache(force=True)


@contextmanager
def _atomic_inventory_state(*objects):
    tracker = _CacheRepairTracker()
    for obj in objects:
        tracker.track(obj)
    try:
        with transaction.atomic():
            yield tracker
    except Exception:
        tracker.repair()
        raise


def _lock_objects(*object_ids):
    from evennia.objects.models import ObjectDB

    ids = sorted(
        {
            object_id
            for object_id in object_ids
            if isinstance(object_id, Integral)
            and not isinstance(object_id, bool)
            and object_id > 0
        }
    )
    objects = ObjectDB.objects.select_for_update().in_bulk(ids)
    return objects


def _locked_item(item):
    objects = _lock_objects(getattr(item, "id", None))
    return objects.get(getattr(item, "id", None))


def _lock_characters(*characters):
    objects = _lock_objects(*(getattr(character, "id", None) for character in characters))
    if len(objects) != len({character.id for character in characters}):
        raise InventoryOwnershipError("An inventory actor no longer exists.")
    return objects


def _locked_record(character_id, item_id):
    return InventoryItem.objects.select_for_update().filter(
        character_id=character_id,
        item_id=item_id,
    ).first()


def _quantity(value, *, fallback=None):
    if value is None and fallback is not None:
        value = fallback
    if isinstance(value, bool) or not isinstance(value, Integral) or value <= 0:
        return None
    return int(value)


def _is_typeclass(obj, typeclass_path):
    checker = getattr(type(obj), "is_typeclass", None)
    return bool(
        callable(checker)
        and checker(obj, typeclass_path, exact=False)
    )


def _move_or_reject(item, destination, message):
    moved = item.move_to(
        destination,
        quiet=True,
        move_hooks=False,
    )
    if not moved:
        raise _MutationRejected(message)
    _after_write("item_moved")


def _schedule_collect_check(character, item):
    def _check():
        from world.quest_engine import check_collect_objectives

        check_collect_objectives(character, item)

    transaction.on_commit(_check)


def _find_existing_stack_locked(character, item):
    if not bool(item.db.stackable):
        return None, None

    records = list(
        InventoryItem.objects.select_for_update().filter(
            character_id=character.id,
            is_quest_item=False,
            is_equipped=False,
            container_id__isnull=True,
        )
    )
    candidates = _lock_objects(*(record.item_id for record in records))
    for record in records:
        existing = candidates.get(record.item_id)
        if not existing or existing.id == item.id:
            continue
        if (
            existing.key == item.key
            and existing.db.item_type == item.db.item_type
            and bool(existing.db.stackable)
        ):
            return existing, record
    return None, None


def _get_container_contents_weight_locked(character, container):
    records = list(
        InventoryItem.objects.select_for_update().filter(
            character_id=character.id,
            container_id=container.id,
        )
    )
    items = _lock_objects(*(record.item_id for record in records))
    total = 0.0
    for record in records:
        item = items.get(record.item_id)
        if item:
            total += container.get_effective_weight_of(
                item.db.weight or 0.1,
                record.quantity,
            )
    return total


def _get_container_contents_weight(character, container):
    """Read the effective contents weight without mutating ownership."""

    from evennia.objects.models import ObjectDB

    records = list(
        InventoryItem.objects.filter(
            character_id=character.id,
            container_id=container.id,
        )
    )
    items = ObjectDB.objects.in_bulk(record.item_id for record in records)
    return sum(
        container.get_effective_weight_of(
            items[record.item_id].db.weight or 0.1,
            record.quantity,
        )
        for record in records
        if record.item_id in items
    )


def register_item_ownership(
    character,
    item,
    quantity=None,
    container_id=None,
    is_quest_item=None,
    keyring=None,
):
    """Register an already-created direct-to-player item under row locks."""

    requested_quantity = _quantity(
        quantity,
        fallback=_quantity(getattr(item.db, "quantity", None), fallback=1),
    )
    if requested_quantity is None:
        raise ValueError("Inventory quantity must be a positive whole number.")

    with _atomic_inventory_state(item):
        _lock_characters(character)
        locked_item = _locked_item(item)
        if not locked_item:
            raise InventoryOwnershipError("Cannot register a missing item.")
        if locked_item.db_location_id != character.id:
            raise InventoryOwnershipError(
                "Cannot register an item outside the character's possession."
            )

        existing = InventoryItem.objects.select_for_update().filter(
            item_id=locked_item.id,
        ).first()
        if existing and existing.character_id != character.id:
            raise InventoryOwnershipError(
                "The item is already registered to another character."
            )

        values = {
            "quantity": requested_quantity,
            "container_id": container_id,
            "is_quest_item": (
                bool(locked_item.db.is_quest_item)
                if is_quest_item is None
                else bool(is_quest_item)
            ),
            "keyring": (
                bool(getattr(locked_item.db, "keyring", False))
                if keyring is None
                else bool(keyring)
            ),
        }
        if existing:
            for name, value in values.items():
                setattr(existing, name, value)
            existing.save(
                update_fields=[
                    "quantity",
                    "container_id",
                    "is_quest_item",
                    "keyring",
                ]
            )
            record = existing
        else:
            record = InventoryItem.objects.create(
                character_id=character.id,
                item_id=locked_item.id,
                **values,
            )
        _after_write("ownership_registered")
        return record


def unregister_item_ownership(character, item):
    """Low-level metadata removal for a caller's enclosing atomic mutation.

    Prefer ``destroy_owned_item`` or a transfer/drop operation. This function
    remains for composite callers that already own a wider transaction.
    """

    character_id = getattr(character, "id", None)
    item_id = getattr(item, "id", None)
    if (
        isinstance(character_id, bool)
        or isinstance(item_id, bool)
        or not isinstance(character_id, Integral)
        or not isinstance(item_id, Integral)
        or character_id <= 0
        or item_id <= 0
    ):
        return False

    from evennia.objects.models import ObjectDB

    if not ObjectDB.objects.filter(pk=character_id).exists():
        return False
    if not ObjectDB.objects.filter(pk=item_id).exists():
        return False

    with _atomic_inventory_state(item):
        _lock_characters(character)
        locked_item = _locked_item(item)
        if not locked_item:
            return False
        record = _locked_record(character.id, locked_item.id)
        if not record:
            return False
        record.delete()
        _after_write("ownership_unregistered")
        return True


def destroy_owned_item(character, item):
    """Delete an owned object and its metadata as one durable mutation."""

    with _atomic_inventory_state(item):
        _lock_characters(character)
        locked_item = _locked_item(item)
        if not locked_item:
            return False, "That item no longer exists."
        record = _locked_record(character.id, locked_item.id)
        if not record or locked_item.db_location_id != character.id:
            return False, "You don't have that."
        record.delete()
        _after_write("ownership_unregistered")
        locked_item.delete()
        _after_write("owned_item_deleted")
        return True, ""


def pick_up(character, item, container=None):
    """Atomically claim a visible item, stacking when the direct carry matches."""

    try:
        with _atomic_inventory_state(item):
            characters = _lock_characters(character)
            locked_character = characters[character.id]
            if container:
                objects = _lock_objects(item.id, container.id)
                locked_item = objects.get(item.id)
                locked_container = objects.get(container.id)
                if (
                    not locked_container
                    or locked_container.db_location_id
                    != locked_character.db_location_id
                ):
                    return False, f"{container.key} is not here."
            else:
                locked_item = _locked_item(item)
            if not locked_item:
                return False, "That item is no longer here."

            expected_location_id = (
                container.id if container else locked_character.db_location_id
            )
            if locked_item.db_location_id != expected_location_id:
                if container:
                    return False, f"That's not in {container.key}."
                return False, "You don't see that here."

            quantity = _quantity(getattr(locked_item.db, "quantity", None), fallback=1)
            if quantity is None:
                return False, "That item has an invalid stack quantity."

            existing, existing_record = _find_existing_stack_locked(
                character,
                locked_item,
            )
            if existing:
                existing_record.quantity += quantity
                existing_record.save(update_fields=["quantity"])
                _after_write("stack_incremented")
                item_key = locked_item.key
                locked_item.delete()
                _after_write("source_item_deleted")
                _schedule_collect_check(character, existing)
                return True, (
                    f"You pick up the {item_key}. "
                    f"You now have {existing_record.quantity}."
                )

            if InventoryItem.objects.select_for_update().filter(
                item_id=locked_item.id,
            ).exists():
                return False, "That item is already claimed."

            _move_or_reject(locked_item, character, "That can't be picked up.")
            is_keyring = _is_typeclass(
                locked_item,
                "typeclasses.objects.SoravelonKeyringItem",
            )
            InventoryItem.objects.create(
                character_id=character.id,
                item_id=locked_item.id,
                quantity=quantity,
                is_quest_item=bool(locked_item.db.is_quest_item),
                keyring=is_keyring,
            )
            _after_write("ownership_registered")
            _schedule_collect_check(character, locked_item)
            return True, f"You pick up the {locked_item.key}."
    except _MutationRejected as error:
        return False, str(error)


def move_owned_items_to_world_container(character, items, destination):
    """Move a complete owned-item set to a world container in one commit.

    This is the death/corpse primitive. A missing ownership row is an integrity
    error; silently moving only part of a character's inventory would lose the
    authoritative relationship between containment and metadata.
    """

    items = list(items)
    if not items:
        return 0
    with _atomic_inventory_state(*items, destination):
        _lock_characters(character)
        objects = _lock_objects(*(item.id for item in items), destination.id)
        locked_destination = objects.get(destination.id)
        locked_items = [objects.get(item.id) for item in items]
        if not locked_destination or any(item is None for item in locked_items):
            raise InventoryOwnershipError("A corpse transfer object no longer exists.")

        records = {
            record.item_id: record
            for record in InventoryItem.objects.select_for_update().filter(
                character_id=character.id,
                item_id__in=[item.id for item in locked_items],
            )
        }
        if len(records) != len(locked_items):
            raise InventoryOwnershipError(
                "Cannot transfer a partially registered player inventory."
            )

        for item in locked_items:
            if item.db_location_id != character.id:
                raise InventoryOwnershipError(
                    "Cannot transfer an item outside the character's possession."
                )
            _move_or_reject(
                item,
                locked_destination,
                f"{item.key} could not be moved to the corpse.",
            )
            records[item.id].delete()
            _after_write("ownership_unregistered")
        return len(locked_items)


def _copy_item_for_split(item, destination, quantity, tracker):
    from evennia import create_object

    dropped = create_object(item.__class__, key=item.key, location=destination)
    tracker.track(dropped)
    for attribute in item.attributes.all():
        dropped.attributes.add(
            attribute.key,
            attribute.value,
            category=attribute.category,
        )
    for tag in item.tags.all(return_key_and_category=True):
        if tag and tag[0]:
            dropped.tags.add(tag[0], category=tag[1])
    dropped.db.quantity = quantity
    _after_write("split_item_created")
    return dropped


def drop_item(character, item, quantity=None):
    """Atomically drop a full item or split a positive stack quantity."""

    requested_quantity = None if quantity is None else _quantity(quantity)
    if quantity is not None and requested_quantity is None:
        return False, "Drop quantity must be a positive whole number."

    try:
        with _atomic_inventory_state(item) as tracker:
            tracker.track(item, attributes=("quantity",))
            characters = _lock_characters(character)
            locked_character = characters[character.id]
            locked_item = _locked_item(item)
            if not locked_item:
                return False, "You don't have that."
            record = _locked_record(character.id, locked_item.id)
            if not record or locked_item.db_location_id != character.id:
                return False, "You don't have that."

            can_drop, reason = locked_item.can_drop(character)
            if not can_drop:
                return False, reason
            if record.is_equipped:
                return False, f"Unequip {locked_item.key} before dropping it."
            if record.container_id:
                return False, f"Take {locked_item.key} out before dropping it."

            amount = record.quantity if requested_quantity is None else requested_quantity
            if amount > record.quantity:
                return False, f"You only have {record.quantity}."
            destination = locked_character.location
            if not destination:
                return False, "There is nowhere to drop that."

            if amount < record.quantity:
                _copy_item_for_split(locked_item, destination, amount, tracker)
                record.quantity -= amount
                record.save(update_fields=["quantity"])
                _after_write("stack_decremented")
                return True, f"You drop {amount} {locked_item.key}."

            _move_or_reject(locked_item, destination, "That can't be dropped.")
            locked_item.db.quantity = record.quantity
            _after_write("world_quantity_written")
            record.delete()
            _after_write("ownership_unregistered")
            return True, f"You drop the {locked_item.key}."
    except _MutationRejected as error:
        return False, str(error)


def put_in_container(character, item, container):
    """Atomically assign a directly carried item to an owned container."""

    with _atomic_inventory_state(item, container):
        _lock_characters(character)
        objects = _lock_objects(item.id, container.id)
        locked_item = objects.get(item.id)
        locked_container = objects.get(container.id)
        if not locked_item or not locked_container:
            return False, "You don't have that."
        if not _is_typeclass(
            locked_container,
            "typeclasses.objects.SoravelonContainer",
        ):
            return False, f"{locked_container.key} isn't a container."

        item_record = _locked_record(character.id, locked_item.id)
        container_record = _locked_record(character.id, locked_container.id)
        if (
            not item_record
            or not container_record
            or locked_item.db_location_id != character.id
            or locked_container.db_location_id != character.id
        ):
            return False, "You don't have that."
        if item_record.container_id:
            return False, f"{locked_item.key} is already in a container."
        if item_record.is_equipped:
            return False, f"Unequip {locked_item.key} before packing it."

        can_accept, reason = locked_container.can_accept(locked_item)
        if not can_accept:
            return False, reason
        current_weight = _get_container_contents_weight_locked(
            character,
            locked_container,
        )
        item_weight = locked_container.get_effective_weight_of(
            locked_item.db.weight or 0.1,
            item_record.quantity,
        )
        if current_weight + item_weight > locked_container.db.weight_capacity:
            return False, (
                f"{locked_container.key} is too full. "
                f"Capacity: {locked_container.db.weight_capacity} kg."
            )

        item_record.container_id = locked_container.id
        item_record.save(update_fields=["container_id"])
        _after_write("container_assigned")
        return True, f"You put the {locked_item.key} in {locked_container.key}."


def take_from_container(character, item, container=None):
    """Atomically return a contained item to direct carry."""

    with _atomic_inventory_state(item):
        _lock_characters(character)
        locked_item = _locked_item(item)
        if not locked_item:
            return False, "You don't have that."
        record = _locked_record(character.id, locked_item.id)
        if not record or locked_item.db_location_id != character.id:
            return False, "You don't have that."
        if not record.container_id:
            return False, f"{locked_item.key} isn't in a container."
        if container and record.container_id != container.id:
            return False, f"{locked_item.key} isn't in {container.key}."

        record.container_id = None
        record.save(update_fields=["container_id"])
        _after_write("container_cleared")
        return True, f"You take the {locked_item.key} out."


def equip_item(character, item):
    """Atomically claim one valid equipment slot."""

    with _atomic_inventory_state(item):
        _lock_characters(character)
        locked_item = _locked_item(item)
        if not locked_item:
            return False, "You don't have that."
        list(
            InventoryItem.objects.select_for_update().filter(
                character_id=character.id,
                is_equipped=True,
            )
        )
        record = _locked_record(character.id, locked_item.id)
        if not record or locked_item.db_location_id != character.id:
            return False, "You don't have that."
        if record.container_id:
            return False, f"Take {locked_item.key} out of your container first."

        can_equip, slot_override = locked_item.can_equip(character)
        if not can_equip:
            return False, slot_override
        slot = slot_override or locked_item.db.equipment_slot
        record.is_equipped = True
        record.equipment_slot = slot
        record.save(update_fields=["is_equipped", "equipment_slot"])
        _after_write("equipment_updated")

    from world.equipment_effects import clamp_current_resources_to_effective_caps

    clamp_current_resources_to_effective_caps(character)
    return True, f"You equip the {item.key}."


def unequip_item(character, item):
    """Atomically release an occupied equipment slot."""

    with _atomic_inventory_state(item):
        _lock_characters(character)
        locked_item = _locked_item(item)
        if not locked_item:
            return False, "You don't have that."
        record = _locked_record(character.id, locked_item.id)
        if not record or locked_item.db_location_id != character.id:
            return False, "You don't have that."
        if not record.is_equipped:
            return False, f"{locked_item.key} isn't equipped."

        record.is_equipped = False
        record.equipment_slot = None
        record.save(update_fields=["is_equipped", "equipment_slot"])
        _after_write("equipment_updated")

    from world.equipment_effects import clamp_current_resources_to_effective_caps

    clamp_current_resources_to_effective_caps(character)
    return True, f"You unequip the {item.key}."


def transfer_item(giver, receiver, item):
    """Atomically transfer one uncontained, unequipped item between players."""

    if giver.id == receiver.id:
        return False, "You keep that to yourself."
    if not _is_typeclass(receiver, "typeclasses.characters.Character"):
        return False, "You can only give carried items to another player."
    if giver.location != receiver.location:
        return False, "They are not here."

    try:
        with _atomic_inventory_state(item):
            characters = _lock_characters(giver, receiver)
            locked_giver = characters[giver.id]
            locked_receiver = characters[receiver.id]
            if locked_giver.db_location_id != locked_receiver.db_location_id:
                return False, "They are not here."
            locked_item = _locked_item(item)
            if not locked_item:
                return False, "You don't have that."
            record = _locked_record(giver.id, locked_item.id)
            if not record or locked_item.db_location_id != giver.id:
                return False, "You don't have that."
            can_transfer, reason = locked_item.can_drop(giver)
            if not can_transfer:
                return False, reason
            if record.is_equipped:
                return False, f"Unequip {locked_item.key} before giving it away."
            if record.container_id:
                return False, f"Take {locked_item.key} out before giving it away."

            existing, existing_record = _find_existing_stack_locked(
                receiver,
                locked_item,
            )
            if existing:
                existing_record.quantity += record.quantity
                existing_record.save(update_fields=["quantity"])
                _after_write("stack_incremented")
                item_key = locked_item.key
                record.delete()
                _after_write("ownership_unregistered")
                locked_item.delete()
                _after_write("source_item_deleted")
                _schedule_collect_check(receiver, existing)
                return True, f"You give {item_key} to {receiver.key}."

            _move_or_reject(locked_item, receiver, "That item cannot be transferred.")
            record.character_id = receiver.id
            record.container_id = None
            record.is_equipped = False
            record.equipment_slot = None
            record.save(
                update_fields=[
                    "character",
                    "container_id",
                    "is_equipped",
                    "equipment_slot",
                ]
            )
            _after_write("ownership_transferred")
            _schedule_collect_check(receiver, locked_item)
            return True, f"You give {locked_item.key} to {receiver.key}."
    except _MutationRejected as error:
        return False, str(error)
