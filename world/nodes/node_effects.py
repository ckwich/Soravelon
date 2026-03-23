"""
Node type mechanical effects.
Tags rooms so combat, mob, and status effect systems can check them.
These tags are the interface contract.
"""

NODE_TYPE_TAGS = {
    "resonance": ["mob_affixes_active"],
    "thermal": ["wet_suppressed", "burn_enhanced"],
    "cognitive": ["mob_coordination"],
    "gravity": ["action_budget_penalty"],
    "temporal": ["dot_tick_variance"],
}


def apply_node_effects(room, node_type, state):
    """Apply node type effect tags to a room."""
    if state not in ("active", "critical"):
        return
    for tag in NODE_TYPE_TAGS.get(node_type, []):
        room.tags.add(tag, category="node_effect")
    if node_type == "gravity":
        room.db.action_budget_penalty = -1


def remove_node_effects(room):
    """Remove all node effect tags from a room."""
    for tag_list in NODE_TYPE_TAGS.values():
        for tag in tag_list:
            room.tags.remove(tag, category="node_effect")
    room.db.action_budget_penalty = 0
