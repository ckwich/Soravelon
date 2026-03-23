"""
Exits for Soravelon.
"""

from evennia.objects.objects import DefaultExit


class SoravelonExit(DefaultExit):
    """Base exit typeclass. Handles node gravity effects."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.hidden = False
        self.db.locked = False
        self.db.lock_tag = None

    def at_traverse(self, traversing_object, target_location, **kwargs):
        if target_location and (target_location.db.action_budget_penalty or 0):
            traversing_object.ndb.gravity_penalty = (
                target_location.db.action_budget_penalty
            )
        else:
            traversing_object.ndb.gravity_penalty = 0

        return super().at_traverse(
            traversing_object, target_location, **kwargs
        )


class LockedExit(SoravelonExit):
    """Requires a keyring item to pass. Auto-checks keyring."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.locked = True
        self.db.lock_tag = None

    def at_traverse(self, traversing_object, target_location, **kwargs):
        lock_tag = self.db.lock_tag
        if not lock_tag:
            return super().at_traverse(
                traversing_object, target_location, **kwargs
            )

        from world.models import InventoryItem
        import evennia

        keyring_records = InventoryItem.objects.filter(
            character_id=traversing_object.id,
            keyring=True
        )

        key_found = False
        for record in keyring_records:
            key_objs = evennia.search_object("#" + str(record.item_id))
            if key_objs:
                key = key_objs[0]
                if getattr(key.db, 'unlocks_exit_tag', None) == lock_tag:
                    key_found = True
                    break

        if not key_found:
            traversing_object.msg(
                "The way is locked. You need the right key."
            )
            return False

        return super().at_traverse(
            traversing_object, target_location, **kwargs
        )


class HiddenExit(SoravelonExit):
    """Invisible until discovered. Discovery persists in db."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.hidden = True
        self.db.search_dc = 30

    def is_visible(self, looker):
        if not self.db.hidden:
            return True
        # Persistent — survives logout and server reload
        discovered = looker.db.discovered_exits
        if not discovered:
            return False
        return self.id in discovered


class NodeGravityExit(SoravelonExit):
    """Always applies gravity penalty regardless of destination."""

    def at_traverse(self, traversing_object, target_location, **kwargs):
        result = super().at_traverse(traversing_object, target_location, **kwargs)
        # Override: NodeGravityExit always applies -1 regardless of destination
        traversing_object.ndb.gravity_penalty = -1
        traversing_object.msg("Every step costs more than it should.")
        return result
