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
        # Enforce authored exit requirements (ancestry, standing, quest)
        req_ancestry = self.db.requires_ancestry
        if req_ancestry and getattr(traversing_object.db, "ancestry", None) != req_ancestry:
            traversing_object.msg(
                f"|rOnly those of {req_ancestry} ancestry may pass this way.|n"
            )
            return False

        req_standing = self.db.requires_standing
        if req_standing:
            faction = req_standing.get("faction", "")
            minimum = req_standing.get("minimum", 0)
            if faction:
                from world.world_state import get_standing
                current = get_standing(traversing_object, faction)
                if current < minimum:
                    traversing_object.msg(
                        f"|rYour standing with {faction} is too low to pass.|n"
                    )
                    return False

        req_quest = self.db.requires_quest
        if req_quest:
            from world.models import CharacterQuest
            has_quest = CharacterQuest.objects.filter(
                character=traversing_object, quest_id=req_quest, status="complete"
            ).exists()
            if not has_quest:
                traversing_object.msg(
                    "|rYou have not yet earned passage here.|n"
                )
                return False

        req_access_grant = self.db.requires_access_grant
        if req_access_grant:
            from world.access_grants import has_access_grant

            if not has_access_grant(traversing_object, req_access_grant):
                traversing_object.msg(
                    "|rYou have not yet earned passage here.|n"
                )
                return False

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
