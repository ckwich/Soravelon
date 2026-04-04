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
        self.db.butcherable = True
        self.db.butchered = False
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

    def can_butcher(self, butcher):
        """
        Check if this corpse can be butchered.

        Returns False if already butchered, decayed, or if the butcher
        cannot access the corpse (respects killer lock / grace period).

        Returns:
            (bool, str): Success and message.
        """
        if self.db.butchered:
            return False, "This corpse has already been butchered."
        if (self.db.loot_phase or "locked") == "decayed":
            return False, "The corpse has decayed beyond salvaging."
        return self.can_loot(butcher)


class SoravelonEquipment(SoravelonItem):
    """An item that can be equipped in a body slot."""

    VALID_SLOTS = {
        "head", "face", "chest", "back", "hands", "wrists",
        "legs", "feet", "main_hand", "off_hand",
        "ring1", "ring2", "amulet"
    }

    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_slot = None
        self.db.stat_bonuses = {}
        self.db.item_type = "equipment"
        self.db.stackable = False
        self.db.two_handed = False
        self.db.armor_value = 0
        self.db.damage_min = 0
        self.db.damage_max = 0
        self.db.material_tier = 0

    def can_equip(self, character):
        from world.models import InventoryItem

        slot = self.db.equipment_slot
        if slot not in self.VALID_SLOTS:
            return False, "That item has an invalid equipment slot."

        # Two-handed weapon check: need both hands free
        if self.db.two_handed and slot == "main_hand":
            off_occupied = InventoryItem.objects.filter(
                character_id=character.id,
                equipment_slot="off_hand",
                is_equipped=True
            ).exists()
            if off_occupied:
                return False, "You need both hands free for that weapon."

        # Off-hand check: can't equip if main_hand has two-handed weapon
        if slot == "off_hand":
            main_items = InventoryItem.objects.filter(
                character_id=character.id,
                equipment_slot="main_hand",
                is_equipped=True
            ).select_related()
            for mi in main_items:
                from evennia.objects.models import ObjectDB
                try:
                    obj = ObjectDB.objects.get(id=mi.item_id)
                    if getattr(obj.db, "two_handed", False):
                        return False, "Your main hand weapon requires both hands."
                except ObjectDB.DoesNotExist:
                    pass

        # Ring auto-fill: if slot is ring1 and occupied, try ring2
        if slot == "ring1":
            r1_occupied = InventoryItem.objects.filter(
                character_id=character.id,
                equipment_slot="ring1",
                is_equipped=True
            ).exists()
            if r1_occupied:
                r2_occupied = InventoryItem.objects.filter(
                    character_id=character.id,
                    equipment_slot="ring2",
                    is_equipped=True
                ).exists()
                if r2_occupied:
                    return False, "Both ring slots are occupied."
                self.db.equipment_slot = "ring2"
                return True, None

        occupied = InventoryItem.objects.filter(
            character_id=character.id,
            equipment_slot=slot,
            is_equipped=True
        ).exists()

        if occupied:
            return False, "You already have something equipped in that slot."

        return True, None


class GatheringNode(SoravelonObject):
    """
    A harvestable resource node in a room. Created by GatheringPoolScript.

    Not an item -- cannot be picked up. Players interact via gathering
    commands (mine, harvest, chop, forage, fish, butcher).
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.node_type = ""          # category from GATHERING_CATEGORIES (ore, herb, wood, etc.)
        self.db.material_id = ""        # key into MATERIAL_REGISTRY
        self.db.gathers_remaining = 4   # randomized 2-6 at spawn per D-03
        self.db.tier = 1                # material tier 1-5
        self.db.zone_id = ""            # zone this node belongs to
        self.db.pool_id = ""            # which pool definition spawned this
        self.db.visibility = "low"      # "low"/"mid"/"high" per D-21
        self.locks.add("get:false()")   # cannot pick up nodes

    def get_display_name(self, looker=None, **kwargs):
        """Skill-gated visibility. Returns None if looker can't see this node."""
        if looker and self.db.visibility != "low":
            from world.material_definitions import VISIBILITY_THRESHOLDS, GATHERING_CATEGORIES
            cat = GATHERING_CATEGORIES.get(self.db.node_type, {})
            skill_name = cat.get("skill", "")
            if skill_name:
                from world.skill_engine import get_skill_value
                skill_val = get_skill_value(looker, skill_name)
                threshold = VISIBILITY_THRESHOLDS.get(self.db.visibility, 0)
                if skill_val < threshold:
                    return None
        return super().get_display_name(looker, **kwargs)

    def return_appearance(self, looker, **kwargs):
        """Show gathers remaining hint."""
        base = super().return_appearance(looker, **kwargs)
        remaining = self.db.gathers_remaining or 0
        if remaining > 4:
            hint = "It looks rich with resources."
        elif remaining > 2:
            hint = "Some resources remain here."
        else:
            hint = "This deposit is nearly exhausted."
        return f"{base}\n{hint}"


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
