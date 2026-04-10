"""
Objects for Soravelon.

ObjectParent is a mixin for all entities with a location.
SoravelonObject is the base for non-character, non-room objects.
SoravelonItem, SoravelonContainer, SoravelonEquipment,
SoravelonKeyringItem, and CorpseContainer handle the item system.
"""

from evennia.objects.objects import DefaultObject


class ObjectParent:
    """
    Mixin for all entities inheriting from DefaultObject.
    Kept for compatibility with Evennia's scaffolded Character class.
    """
    pass


class Object(ObjectParent, DefaultObject):
    """Default Evennia Object — kept for compatibility."""
    pass


class SoravelonObject(ObjectParent, DefaultObject):
    """Base typeclass for all non-character, non-room Soravelon objects."""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = ""


class SoravelonItem(SoravelonObject):
    """
    Base typeclass for all items that can be picked up, carried,
    equipped, or dropped. Weight and quantity metadata live in
    InventoryItem Django model — not on this object.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.weight = 0.1
        self.db.rarity = "common"
        self.db.item_type = None
        self.db.stackable = False
        self.db.value_scales = 0
        self.db.lore_desc = None

    def get_inventory_record(self, character):
        from world.models import InventoryItem
        try:
            return InventoryItem.objects.get(
                character_id=character.id, item_id=self.id
            )
        except InventoryItem.DoesNotExist:
            return None

    def can_drop(self, character):
        record = self.get_inventory_record(character)
        if record and record.is_quest_item:
            return False, "You can't drop a quest item."
        return True, None

    def can_be_sold(self, character):
        record = self.get_inventory_record(character)
        if record and record.is_quest_item:
            return False, "A vendor wouldn't take that from you."
        return True, None


class SoravelonContainer(SoravelonItem):
    """
    A container with weight reduction. Cannot hold other containers.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.weight_reduction = 0
        self.db.weight_capacity = 10.0
        self.db.stack_capacity = 20
        self.db.item_type = "container"
        self.db.stackable = False
        self.db.absorbed_property = None

    def can_accept(self, item):
        if isinstance(item, SoravelonContainer):
            return False, (
                "A bag inside a bag. You've thought about this "
                "for a moment and decided it's not worth the "
                "philosophical implications."
            )
        return True, None

    def get_effective_weight_of(self, item_weight, quantity=1):
        reduction = self.db.weight_reduction / 100
        return item_weight * quantity * (1 - reduction)


class CorpseContainer(SoravelonContainer):
    """
    A loot container spawned on mob or player death.

    Phases: locked (killer/group only) -> open (anyone) -> decayed (deleted).
    Phase transitions scheduled via delay() in combat_engine.spawn_corpse().

    Lock is enforced by can_loot() -- combat engine and loot commands
    call this to gate access.
    """

    GRACE_PERIOD = 120      # 2 minutes killer-locked
    OPEN_PERIOD = 300       # 5 minutes open to all

    def at_object_creation(self):
        super().at_object_creation()
        self.db.killer_id = None
        self.db.killer_group_leader_id = None
        self.db.loot_phase = "locked"
        self.db.mob_key = ""
        self.db.mob_rarity = "normal"
        self.db.decay_at = None
        self.db.item_type = "corpse"
        self.locks.add("get:false()")

    def can_loot(self, character):
        """
        Check if character can access this corpse's loot.

        locked phase: killer or killer's group members only.
        open phase: anyone.
        decayed phase: nobody.

        Returns:
            (bool, str): Success and message.
        """
        phase = self.db.loot_phase or "locked"

        if phase == "decayed":
            return False, "Nothing remains here."

        if phase == "open":
            return True, ""

        # Locked phase: check killer or group membership
        if character.id == self.db.killer_id:
            return True, ""

        # Check group membership: character's group leader matches killer's group leader
        killer_group_id = self.db.killer_group_leader_id
        if killer_group_id:
            char_group_id = getattr(character.ndb, "group_leader_id", None)
            if char_group_id == killer_group_id:
                return True, ""

        return False, "This corpse's loot is still being claimed by the killer."


class SoravelonEquipment(SoravelonItem):
    """An item that can be equipped in a body slot."""

    VALID_SLOTS = {
        "head", "body", "hands", "feet",
        "right_hand", "left_hand", "accessory"
    }

    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_slot = None
        self.db.stat_bonuses = {}
        self.db.item_type = "equipment"
        self.db.stackable = False

    def can_equip(self, character):
        from world.models import InventoryItem

        slot = self.db.equipment_slot
        if slot not in self.VALID_SLOTS:
            return False, "That item has an invalid equipment slot."

        occupied = InventoryItem.objects.filter(
            character_id=character.id,
            equipment_slot=slot,
            is_equipped=True
        ).exists()

        if occupied:
            return False, "You already have something equipped in that slot."

        return True, None


class SoravelonKeyringItem(SoravelonItem):
    """
    A credential item — key, token, faction badge.
    No weight. Cannot be dropped. Checked on locked exits.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.weight = 0.0
        self.db.stackable = False
        self.db.item_type = "credential"
        self.db.keyring = True
        self.db.unlocks_exit_tag = None

    def can_drop(self, character):
        return False, (
            "That's on your keyring. Use 'discard <item> from keyring' "
            "if you really want to remove it."
        )

    def at_get(self, getter, **kwargs):
        """Ensure InventoryItem record has keyring=True on pickup."""
        from world.models import InventoryItem
        InventoryItem.objects.update_or_create(
            character_id=getter.id,
            item_id=self.id,
            defaults={
                "quantity": 1,
                "keyring": True,
                "is_quest_item": bool(self.db.is_quest_item),
            }
        )
