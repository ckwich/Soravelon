"""
Gathering node lifecycle engine for Soravelon.

Manages zone-wide gathering pools: stochastic node spawning across
eligible rooms, depletion with respawn-in-different-room scheduling,
and the GatheringPoolScript tick-driven cleanup.

Mirrors the mob_spawner.py pattern: zone-level pool definitions drive
random room placement with configurable limits.
"""

import random

import evennia
from typeclasses.scripts import SoravelonScript
from world.tag_search import search_objects_by_exact_tag


# ---------------------------------------------------------------------------
# GatheringPoolScript
# ---------------------------------------------------------------------------

class _GatheringPoolScript(SoravelonScript):
    """Persistent Evennia script managing one gathering pool."""

    def at_script_creation(self):
        super().at_script_creation()
        self.db.pool_id = ""
        self.db.zone_id = ""
        self.db.eligible_room_ids = []
        self.db.materials = []
        self.db.max_active = 3
        self.db.respawn_minutes = 15
        self.db.respawn_variance = 5
        self.db.tier_floor = 1
        self.db.tier_ceiling = 3
        self.db.active_node_ids = []
        self.db.last_depleted_room_id = None
        self.key = "gathering_pool"
        self.interval = 120
        self.persistent = True

    def at_repeat(self):
        """Prune dead nodes, spawn replacements if under max_active."""
        _prune_and_refill(self)


class GatheringPoolScript:
    """
    Manages one gathering pool's node lifecycle. Attached to zone object.

    Kept as a lightweight compatibility shim. The actual Evennia Script
    subclass must live at module scope because Evennia persists and reloads
    script typeclass paths across restarts.
    """

    @classmethod
    def get_class(cls):
        """Return the persistent Evennia script class."""
        return _GatheringPoolScript


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _prune_and_refill(pool_script):
    """
    Called by at_repeat: remove deleted/missing nodes from active list,
    spawn replacements if under max_active.
    """


    active_ids = list(pool_script.db.active_node_ids or [])
    live_ids = []

    for node_id in active_ids:
        results = evennia.search_object(f"#{node_id}")
        if results and results[0].location:
            live_ids.append(node_id)

    pool_script.db.active_node_ids = live_ids

    deficit = (pool_script.db.max_active or 3) - len(live_ids)
    for _ in range(deficit):
        node = spawn_node_in_pool(pool_script)
        if node is None:
            break  # no eligible rooms


def _pick_eligible_room(pool_script, exclude_room_id=None):
    """
    Pick a random eligible room from the pool, excluding the last
    depleted room (per D-03 / pitfall 5).
    """


    eligible_ids = list(pool_script.db.eligible_room_ids or [])
    if not eligible_ids:
        return None

    # Also exclude the stored last_depleted_room_id
    last_depleted = pool_script.db.last_depleted_room_id
    exclude_ids = set()
    if exclude_room_id is not None:
        exclude_ids.add(exclude_room_id)
    if last_depleted is not None:
        exclude_ids.add(last_depleted)

    candidates = [rid for rid in eligible_ids if rid not in exclude_ids]

    # If all rooms excluded (e.g., only 1-2 eligible rooms), fall back
    if not candidates:
        candidates = eligible_ids

    chosen_id = random.choice(candidates)

    # Resolve dbref to room object
    results = evennia.search_object(f"#{chosen_id}")
    if results:
        return results[0]
    return None


def _pick_material(pool_script):
    """
    Pick a random material from the pool's materials list, filtered by
    the pool's tier range.
    """
    from world.material_definitions import MATERIAL_REGISTRY

    materials = pool_script.db.materials or []
    tier_floor = pool_script.db.tier_floor or 1
    tier_ceiling = pool_script.db.tier_ceiling or 5

    eligible = []
    for mat_id in materials:
        mat_def = MATERIAL_REGISTRY.get(mat_id)
        if mat_def and tier_floor <= mat_def.get("tier", 1) <= tier_ceiling:
            eligible.append((mat_id, mat_def))

    if not eligible:
        # Fallback: pick any from the list
        for mat_id in materials:
            mat_def = MATERIAL_REGISTRY.get(mat_id)
            if mat_def:
                eligible.append((mat_id, mat_def))

    if not eligible:
        return None, None

    return random.choice(eligible)


# ---------------------------------------------------------------------------
# Core public functions
# ---------------------------------------------------------------------------

def spawn_node_in_pool(pool_script, exclude_room_id=None):
    """
    Spawn a single GatheringNode in a random eligible room.

    Picks a random eligible room (excluding exclude_room_id per D-03),
    picks a random material filtered by tier range, creates a GatheringNode
    with random gathers_remaining (2-6), tags with zone_id and pool_id.

    Args:
        pool_script: GatheringPoolScript instance
        exclude_room_id: dbref int to exclude from room selection

    Returns:
        Created node object, or None if no eligible room/material.
    """

    from typeclasses.objects import GatheringNode

    room = _pick_eligible_room(pool_script, exclude_room_id)
    if not room:
        return None

    mat_id, mat_def = _pick_material(pool_script)
    if not mat_id:
        return None

    display_name = mat_def.get("display_name", mat_id.replace("_", " ").title())
    node = evennia.create_object(
        GatheringNode,
        key=display_name,
        location=room,
    )

    node.db.node_type = mat_def.get("category", "")
    node.db.material_id = mat_id
    node.db.gathers_remaining = random.randint(2, 6)
    node.db.tier = mat_def.get("tier", 1)
    node.db.zone_id = pool_script.db.zone_id or ""
    node.db.pool_id = pool_script.db.pool_id or ""
    node.db.visibility = mat_def.get("visibility", "low")

    # Tag for zone queries
    zone_id = pool_script.db.zone_id or ""
    if zone_id:
        node.tags.add(zone_id, category="zone_id")
    pool_id = pool_script.db.pool_id or ""
    if pool_id:
        node.tags.add(pool_id, category="pool_id")

    # Track in pool script
    active = list(pool_script.db.active_node_ids or [])
    active.append(node.id)
    pool_script.db.active_node_ids = active

    return node


def deplete_node(node, pool_script):
    """
    Remove a depleted node and schedule respawn in a different room.

    Removes node from room, removes from pool_script.db.active_node_ids,
    schedules respawn via evennia.utils.delay() with configurable delay
    plus random variance.

    Args:
        node: GatheringNode instance
        pool_script: GatheringPoolScript managing this node
    """


    depleted_room_id = node.location.id if node.location else None

    # Track last depleted room for anti-repeat spawning
    pool_script.db.last_depleted_room_id = depleted_room_id

    # Remove from active tracking
    active = list(pool_script.db.active_node_ids or [])
    if node.id in active:
        active.remove(node.id)
    pool_script.db.active_node_ids = active

    # Delete the node object
    node.delete()

    # Schedule respawn
    base_seconds = (pool_script.db.respawn_minutes or 15) * 60
    variance_seconds = (pool_script.db.respawn_variance or 5) * 60
    delay = base_seconds + random.uniform(-variance_seconds, variance_seconds)
    delay = max(delay, 30)  # minimum 30s floor

    def _do_respawn():
        if not pool_script or not pool_script.pk:
            return  # Pool script was deleted; skip respawn
        spawn_node_in_pool(pool_script, exclude_room_id=depleted_room_id)

    evennia.utils.delay(delay, _do_respawn)


def gather_from_node(character, node):
    """
    Attempt to gather from a node. Decrements gathers_remaining.

    If depleted (<= 0 remaining), calls deplete_node. Does NOT create
    items -- that is the command's responsibility via item_spawner.

    Args:
        character: Character performing the gather
        node: GatheringNode instance

    Returns:
        (bool, str): (success, material_id)
    """
    material_id = node.db.material_id or ""
    remaining = node.db.gathers_remaining or 0

    if remaining <= 0:
        return (False, "")

    node.db.gathers_remaining = remaining - 1

    if node.db.gathers_remaining <= 0:
        # Find the pool script for this node
        pool_script = _find_pool_script(node)
        if pool_script:
            deplete_node(node, pool_script)

    return (True, material_id)


def _find_pool_script(node):
    """
    Locate the GatheringPoolScript managing this node.
    Searches the zone object's scripts for a matching pool_id.
    """


    zone_id = node.db.zone_id or ""
    pool_id = node.db.pool_id or ""
    if not zone_id:
        return None

    # Find zone object
    zone_objs = search_objects_by_exact_tag(zone_id, "zone_id")
    zone_obj = None
    for obj in zone_objs:
        if obj.tags.get("zone_object", category="object_type"):
            zone_obj = obj
            break

    if not zone_obj:
        return None

    # Search scripts on zone object
    scripts = zone_obj.scripts.all()
    for script in scripts:
        if (script.key == "gathering_pool"
                and (script.db.pool_id or "") == pool_id):
            return script

    return None


def spawn_gathering_pool(zone_obj, pool_def):
    """
    Create or find a GatheringPoolScript on zone_obj for a pool definition.

    Sets pool_script.db attrs from pool_def. Resolves room_ids to dbrefs
    via tag search. Spawns initial nodes up to max_active. Sets gathering
    room state flags on eligible rooms.

    Args:
        zone_obj: Zone Evennia object
        pool_def: dict with keys: pool_type, room_ids, materials,
                  max_active, respawn_minutes, respawn_variance,
                  tier_floor, tier_ceiling
    """


    zone_id = zone_obj.db.zone_id or ""
    pool_type = pool_def.get("pool_type", "")
    pool_id = f"{zone_id}_{pool_type}"

    # Check for existing script with this pool_id
    existing_scripts = zone_obj.scripts.all()
    pool_script = None
    for s in existing_scripts:
        if s.key == "gathering_pool" and (s.db.pool_id or "") == pool_id:
            pool_script = s
            break

    if not pool_script:
        # Create new script
        ScriptClass = GatheringPoolScript.get_class()
        zone_obj.scripts.add(ScriptClass)
        # Retrieve the just-added script
        all_scripts = zone_obj.scripts.all()
        for s in all_scripts:
            if s.key == "gathering_pool" and not s.db.pool_id:
                pool_script = s
                break

    if not pool_script:
        return

    # Resolve room_id strings to dbrefs
    room_ids_str = pool_def.get("room_ids", [])
    eligible_room_ids = []
    for room_id_tag in room_ids_str:
        candidates = search_objects_by_exact_tag(room_id_tag, "room_id")
        for room in candidates:
            if (room.db.zone_id or "") == zone_id:
                eligible_room_ids.append(room.id)
                break

    # Configure the script
    pool_script.db.pool_id = pool_id
    pool_script.db.zone_id = zone_id
    pool_script.db.eligible_room_ids = eligible_room_ids
    pool_script.db.materials = pool_def.get("materials", [])
    pool_script.db.max_active = pool_def.get("max_active", 3)
    pool_script.db.respawn_minutes = pool_def.get("respawn_minutes", 15)
    pool_script.db.respawn_variance = pool_def.get("respawn_variance", 5)
    pool_script.db.tier_floor = pool_def.get("tier_floor", 1)
    pool_script.db.tier_ceiling = pool_def.get("tier_ceiling", 3)
    # Reconcile existing nodes instead of blindly resetting
    existing_ids = list(pool_script.db.active_node_ids or [])
    valid_ids = []
    for nid in existing_ids:
        try:
            results = evennia.search_object("#" + str(nid))
            if results and results[0].pk:
                valid_ids.append(nid)
        except Exception:
            pass
    pool_script.db.active_node_ids = valid_ids
    if not pool_script.db.last_depleted_room_id:
        pool_script.db.last_depleted_room_id = None

    # Spawn nodes only up to max_active minus already-existing valid nodes
    max_active = pool_def.get("max_active", 3)
    to_spawn = max(0, max_active - len(valid_ids))
    for _ in range(to_spawn):
        node = spawn_node_in_pool(pool_script)
        if node is None:
            break

    # Set gathering room state flags on eligible rooms
    _set_room_flags_for_pool(pool_type, eligible_room_ids)


def _set_room_flags_for_pool(pool_type, eligible_room_ids):
    """
    Set persistent room state flags on eligible rooms based on pool type.

    Maps pool_type to flag name per design:
      ore -> mineral_deposits
      herb/forage -> rich_soil
      wood -> dense_foliage
      fish -> water_source
    """

    from world.room_state import add_room_flag

    flag_map = {
        "ore": "mineral_deposits",
        "herb": "rich_soil",
        "forage": "rich_soil",
        "wood": "dense_foliage",
        "fish": "water_source",
    }

    flag_name = flag_map.get(pool_type)
    if not flag_name:
        return

    for room_id in eligible_room_ids:
        results = evennia.search_object(f"#{room_id}")
        if results:
            room = results[0]
            # Use -1 for persistent (never-decaying) flag
            add_room_flag(room, flag_name, duration=-1)


# ---------------------------------------------------------------------------
# Prospect scan (D-22) — straight-line node discovery
# ---------------------------------------------------------------------------

CARDINAL_DIRECTIONS = ["north", "south", "east", "west"]


def prospect_scan(character, max_range):
    """
    Scan straight lines from character's room for gathering nodes (D-22).

    IMPORTANT: This is straight-line walking, NOT BFS. Each cardinal direction
    is followed through exits until no matching exit is found or max_range reached.

    Args:
        character: The scanning character (skill checked for visibility)
        max_range: Max rooms to scan in each direction

    Returns:
        list of dicts: [{"direction": str, "distance": int, "node": GatheringNode}, ...]
    """
    from typeclasses.objects import GatheringNode

    results = []
    room = character.location

    for direction in CARDINAL_DIRECTIONS:
        current = room
        for distance in range(1, max_range + 1):
            # Find exit in this direction
            exit_obj = None
            for ex in current.exits:
                if ex.key.lower() == direction:
                    exit_obj = ex
                    break

            if not exit_obj or not exit_obj.destination:
                break

            current = exit_obj.destination

            # Check for gathering nodes in this room
            for obj in current.contents:
                if isinstance(obj, GatheringNode):
                    results.append({
                        "direction": direction,
                        "distance": distance,
                        "node": obj,
                    })

    return results


def initialize_zone_gathering(zone_obj):
    """
    Initialize all gathering pools defined on a zone object.

    Reads zone_obj.db.gathering_pools list, calls spawn_gathering_pool
    for each definition. Called during explicit world-content materialization.

    Args:
        zone_obj: Zone Evennia object with db.gathering_pools list
    """
    pools = zone_obj.db.gathering_pools or []
    for pool_def in pools:
        spawn_gathering_pool(zone_obj, pool_def)


# ---------------------------------------------------------------------------
# Tool repair authority
# ---------------------------------------------------------------------------

def _tool_durability_spec(tool):
    """Return the authored durability spec for one canonical tool."""
    from world.material_definitions import TOOL_DURABILITY

    for tool_type, spec in TOOL_DURABILITY.items():
        if tool.tags.has(tool_type, category="item_tag"):
            return tool_type, spec
    return None, None


def _after_tool_repair_write(checkpoint):
    """Failure-injection seam for atomic tool-repair tests."""


def repair_tool(character, tool):
    """Atomically repair one owned canonical tool and charge carried Scales."""
    from numbers import Real

    from evennia.objects.models import ObjectDB

    from world.atomic_state import atomic_evennia_state
    from world.models import InventoryItem
    from world.skill_engine import accumulate_skill_use, get_skill_value

    with atomic_evennia_state(character, tool) as tracker:
        locked = ObjectDB.objects.select_for_update().in_bulk(
            [character.id, tool.id]
        )
        if len(locked) != 2:
            return False, "That repair target no longer exists."
        locked_character = locked[character.id]
        locked_tool = locked[tool.id]
        tracker.track(locked_character, attributes=("carried_scales",))
        tracker.track(locked_tool, attributes=("durability",))

        owned = InventoryItem.objects.select_for_update().filter(
            character_id=locked_character.id,
            item_id=locked_tool.id,
        ).exists()
        if not owned or locked_tool.db_location_id != locked_character.id:
            return False, "You do not own that tool."

        room = locked_character.location
        if not room or not room.tags.has(
            "crafting_workbench",
            category="crafting_station",
        ):
            return False, "You need a workbench to repair tools."

        tool_type, durability_spec = _tool_durability_spec(locked_tool)
        if not durability_spec:
            return False, "That item is not a repairable tool."

        durability = locked_tool.db.durability
        if (
            isinstance(durability, bool)
            or not isinstance(durability, Real)
            or durability < 0
        ):
            return False, "That tool has invalid durability data."

        maximum = durability_spec["max_durability"]
        if durability >= maximum:
            return False, f"{locked_tool.key} is already in good condition."

        cost = durability_spec["repair_cost"]
        carried = locked_character.db.carried_scales or 0
        if carried < cost:
            return False, (
                f"Repairing {locked_tool.key} costs {cost} Scales; "
                f"you only carry {carried}."
            )

        smithing = get_skill_value(locked_character, "smithing")
        repair_amount = int(10 + smithing / 5)
        repaired_to = min(maximum, durability + repair_amount)
        locked_character.db.carried_scales = carried - cost
        _after_tool_repair_write("scales_debited")
        locked_tool.db.durability = repaired_to
        _after_tool_repair_write("durability_restored")

    accumulate_skill_use(character, "smithing")
    return True, (
        f"|gYou repair {tool.key} for {cost} Scales. "
        f"Durability: {repaired_to}/{maximum}.|n"
    )


# ---------------------------------------------------------------------------
# Gather completion logic (extracted from cmd_gathering.py per D-06)
# ---------------------------------------------------------------------------

def complete_gather(character, node, tool, skill_name, skill_val):
    """
    Complete a gathering action. Handles node depletion, item creation,
    quality calc, bonus quantity, tool durability, and skill XP.

    Args:
        character: Character performing the gather
        node: GatheringNode instance
        tool: Tool item (or None for no-tool gathering like forage)
        skill_name: Skill name string (e.g., "mining", "herbalism")
        skill_val: Pre-calculated skill value (passed from command delay)

    Returns:
        (bool, str, list[item], bool) -- success, message, created items,
        tool_broken.
        On failure: (False, message, [], False).
    """
    from world.crafting_definitions import QUALITY_DISPLAY
    from world.crafting_engine import calculate_craft_quality
    from world.item_spawner import create_item_from_template
    from world.material_definitions import MATERIAL_REGISTRY
    from world.skill_engine import accumulate_skill_use

    # Perform gather (decrements gathers_remaining)
    success, result = gather_from_node(character, node)
    if not success:
        return (False, "|rThe resource is depleted.|n", [], False)

    material_id = result
    mat = MATERIAL_REGISTRY.get(material_id, {})
    tier_difficulty = (node.db.tier or 1) * 15  # tier 1=15, tier 5=75
    quality = calculate_craft_quality(skill_val, tier_difficulty)

    item_def = {
        "item_id": material_id,
        "key": mat.get("display_name", material_id.replace("_", " ").title()),
        "item_type": "item",
        "weight": 0.5,
        "desc": f"Raw {mat.get('display_name', material_id)}.",
        "value": (node.db.tier or 1) * 5,
        "quality": quality,
    }
    item = create_item_from_template(item_def, location=character)
    items = [item]

    q_display = QUALITY_DISPLAY.get(quality, "")
    msg = f"|gYou gather {q_display} {item.key}.|n"

    # Bonus quantity at high skill (D-04): 25% chance at skill 50+, 50% at skill 80+
    bonus_chance = 0
    if skill_val >= 80:
        bonus_chance = 0.5
    elif skill_val >= 50:
        bonus_chance = 0.25
    if bonus_chance and random.random() < bonus_chance:
        bonus_item = create_item_from_template(item_def, location=character)
        items.append(bonus_item)
        msg += f"\n|gYour skill yields an extra {bonus_item.key}!|n"

    # Tool durability loss (D-20)
    tool_broken = False
    if tool and tool.db.durability is not None:
        tool.db.durability -= 1
        if tool.db.durability <= 0:
            msg += f"\n|y{tool.key} has broken from use!|n"
            tool_broken = True

    # Skill progression
    accumulate_skill_use(character, skill_name)

    return (True, msg, items, tool_broken)


# ---------------------------------------------------------------------------
# Fish catch logic (extracted from cmd_fishing.py per D-05)
# ---------------------------------------------------------------------------

def catch_fish(character, node, tool, bait=None, quality_multiplier=1.0):
    """
    Process a fish catch. Handles node depletion, quality calc, bait
    consumption, tool durability, skill XP, and item creation.

    Args:
        character: Character performing the catch
        node: GatheringNode (fish spot)
        tool: Fishing rod item
        bait: Optional bait item (consumed on use)
        quality_multiplier: 1.0 for active, 0.5 for idle mode

    Returns:
        (bool, str, item_or_None, bool, bool) -- success flag, message,
        created item, bait_consumed, tool_broken.
        On failure: (False, message, None, False, False).
    """
    from world.crafting_definitions import QUALITY_DISPLAY, QUALITY_TIERS
    from world.crafting_engine import calculate_craft_quality
    from world.item_spawner import create_item_from_template
    from world.material_definitions import MATERIAL_REGISTRY
    from world.skill_engine import accumulate_skill_use, get_skill_value

    # Gather from node (decrements gathers_remaining)
    success, result = gather_from_node(character, node)
    if not success:
        return (False, "|rThe fishing spot is depleted.|n", None, False, False)

    material_id = result
    mat = MATERIAL_REGISTRY.get(material_id, {})

    # Quality calculation
    skill_val = get_skill_value(character, "fishing")
    tier_difficulty = node.db.tier * 15
    quality = calculate_craft_quality(skill_val, tier_difficulty)

    # Idle mode quality penalty (D-16: diminished returns)
    if quality_multiplier < 1.0:
        qi = QUALITY_TIERS.index(quality)
        qi = max(0, qi - 1)  # drop one quality tier for idle
        quality = QUALITY_TIERS[qi]

    # Bait quality bonus (D-18)
    bait_consumed = False
    if bait and bait.pk:
        qi = QUALITY_TIERS.index(quality)
        qi = min(len(QUALITY_TIERS) - 1, qi + 1)  # +1 tier with bait
        quality = QUALITY_TIERS[qi]
        # Consume bait
        bait.delete()
        bait_consumed = True

    item_def = {
        "item_id": material_id,
        "key": mat.get("display_name", material_id.replace("_", " ").title()),
        "item_type": "item",
        "weight": 0.3,
        "desc": f"A freshly caught {mat.get('display_name', material_id)}.",
        "value": node.db.tier * 8,
        "quality": quality,
    }
    item = create_item_from_template(item_def, location=character)

    q_display = QUALITY_DISPLAY.get(quality, "")
    msg = f"|gYou catch {q_display} {item.key}!|n"

    # Tool durability (D-20)
    tool_broken = False
    if tool and getattr(tool.db, "durability", None) is not None:
        tool.db.durability -= 1
        if tool.db.durability <= 0:
            msg += f"\n|y{tool.key} has broken from use!|n"
            tool_broken = True

    accumulate_skill_use(character, "fishing")

    return (True, msg, item, bait_consumed, tool_broken)


# ---------------------------------------------------------------------------
# Butcher yields
# ---------------------------------------------------------------------------

BUTCHER_YIELDS = {
    "boar": [
        {"material_id": "boar_hide", "display_name": "Boar Hide", "value": 8},
        {"material_id": "raw_meat", "display_name": "Raw Meat", "value": 3},
    ],
    "ash_wolf": [
        {"material_id": "ash_wolf_pelt", "display_name": "Ash Wolf Pelt", "value": 15},
        {"material_id": "bone_fragment", "display_name": "Bone Fragment", "value": 2},
    ],
    "spider": [
        {"material_id": "spider_silk_thread", "display_name": "Spider Silk Thread", "value": 12},
    ],
    "drake": [
        {"material_id": "drake_scale", "display_name": "Drake Scale", "value": 25},
        {"material_id": "raw_meat", "display_name": "Raw Meat", "value": 3},
    ],
}


def get_butcher_yields(mob_key):
    """
    Get butcherable materials from a mob type.

    Tries exact mob_key match first, then base name (before first underscore).
    Falls back to generic meat + bone if no specific yields defined.

    Args:
        mob_key: The mob's key string (e.g., "boar", "ash_wolf").

    Returns:
        List of yield definition dicts with material_id, display_name, value.
    """
    yields = BUTCHER_YIELDS.get(mob_key)
    if not yields:
        # Try base name (e.g., "ash_wolf_alpha" -> "ash_wolf", then "ash")
        mob_base = mob_key.rsplit("_", 1)[0] if "_" in mob_key else mob_key
        yields = BUTCHER_YIELDS.get(mob_base)
    if not yields:
        yields = [
            {"material_id": "raw_meat", "display_name": "Raw Meat", "value": 3},
            {"material_id": "bone_fragment", "display_name": "Bone Fragment", "value": 2},
        ]
    return yields
