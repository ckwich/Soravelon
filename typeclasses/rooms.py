"""
Rooms for Soravelon.

SoravelonRoom is the base room typeclass.
Layer1Room is a pre-pooled room for the node system.
"""

from evennia.objects.objects import DefaultRoom
from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """Default Evennia room — kept for compatibility."""
    pass


class SoravelonRoom(ObjectParent, DefaultRoom):
    """
    Base room for all Soravelon zones.
    Checks node state when generating descriptions.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.zone_id = None
        self.db.layer1_room_id = None
        self.db.layer0_room_id = None
        self.db.is_layer1 = False
        self.db.awakening_desc = None

    def get_display_desc(self, looker, **kwargs):
        """Return description appropriate to current node state."""
        if (self.tags.get("node_awakening", category="node_state")
                and self.db.awakening_desc):
            return self.db.awakening_desc
        return self.db.desc or ""


class Layer1Room(SoravelonRoom):
    """
    A pre-pooled Layer 1 room. Starts tagged inactive.
    Activated by NodeScript._activate_layer1() during layer swap.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_layer1 = True
        self.tags.add("layer_1_pool", category="node_layer")
        self.tags.add("inactive", category="node_layer")
