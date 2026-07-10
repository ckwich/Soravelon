"""
AreaBuilder — the Python interface between area spec .py files
and Evennia's internals.

Every zone file imports AreaBuilder and uses it to describe a zone.
When build() is called, the description is translated into Evennia
DB objects (rooms, exits, zone objects).

Usage::

    from world.area_builder import AreaBuilder

    def build():
        area = AreaBuilder("my_zone_id")
        area.zone(name="My Zone", ...)
        r1 = area.room("room_001", name="First Room", ...)
        area.exit(r1, r2, "north")
        ...
        return area.build()
"""

import copy

import evennia
from evennia import create_object

from world import zone_registry


# AreaBuilderValidationError imported from area_validator above


# --- Module-level registry for cross-zone exit second-pass retry (BLD-06) ---

_UNRESOLVED_EXITS_REGISTRY = []


def get_unresolved_exits():
    """Return all unresolved cross-zone exits registered during this load cycle."""
    return list(_UNRESOLVED_EXITS_REGISTRY)


def clear_unresolved_exits():
    """Clear the registry before a new load cycle."""
    global _UNRESOLVED_EXITS_REGISTRY
    _UNRESOLVED_EXITS_REGISTRY = []


# --- Direction offsets for BFS grid auto-layout ---

DIRECTION_OFFSETS = {
    "north":     (0,  1),
    "south":     (0, -1),
    "east":      (1,  0),
    "west":      (-1, 0),
    "northeast": (1,  1),
    "northwest": (-1, 1),
    "southeast": (1, -1),
    "southwest": (-1, -1),
    "up":        (0,  0),
    "down":      (0,  0),
    "in":        (0,  0),
    "out":       (0,  0),
}


def auto_layout_zone(rooms_dict):
    """
    Assign grid_x, grid_y to zone rooms that lack explicit coords.

    Uses BFS traversal from the first room without explicit coords.
    Rooms with existing grid_x are not overwritten. Collision on (0,0)
    exits (up/down/in/out) resolved by nudging nx += 1 until a free cell
    is found.

    Args:
        rooms_dict: dict mapping room_id -> room_obj (self._rooms in AreaBuilder)
    """
    from collections import deque

    room_list = list(rooms_dict.values())
    if not room_list:
        return

    # Find the first room that needs layout
    root = None
    for r in room_list:
        if r.db.grid_x is None:
            root = r
            break
    if root is None:
        return  # All rooms have explicit coords; nothing to do

    occupied = {}   # (x, y) -> room_obj
    root.db.grid_x = 0
    root.db.grid_y = 0
    occupied[(0, 0)] = root

    queue = deque()
    queue.append((root, 0, 0))

    while queue:
        room, cx, cy = queue.popleft()
        for exit_obj in room.exits:
            dest = exit_obj.destination
            if dest is None:
                continue
            if dest.db.grid_x is not None:
                continue  # Already placed (explicit or earlier BFS visit)
            dx, dy = DIRECTION_OFFSETS.get(exit_obj.key, (0, 0))
            nx, ny = cx + dx, cy + dy
            # Collision nudge: shift east until a free cell is found
            while (nx, ny) in occupied:
                nx += 1
            dest.db.grid_x = nx
            dest.db.grid_y = ny
            occupied[(nx, ny)] = dest
            queue.append((dest, nx, ny))


# --- Validation constants (single source of truth: area_validator) ---

from world.area_validator import (
    VALID_ZONE_TYPES,
    VALID_CONTINENTS,
    VALID_NODE_TYPES,
    VALID_FACTION_TERRITORIES,
    VALID_DIRECTIONS,
    VALID_ROOM_TYPES,
    AreaBuilderValidationError,
    validate_spawn_condition,
)


class AreaBuilder:
    """
    Translates area spec declarations into Evennia DB objects.

    Instantiated per zone. Methods accumulate definitions.
    build() finalizes everything and returns a report dict.
    """

    def __init__(self, zone_id):
        self._zone_id = zone_id
        self._zone_data = {}
        self._rooms = {}                # room_id -> Evennia room object
        self._mobs = {}                 # mob_key -> Evennia mob object
        self._npc_ids = set()           # npc_ids from npc() calls (reconciliation)
        self._exit_ids = set()          # exit object IDs from exit()/cross-zone (reconciliation)
        self._deferred_exits = []       # cross-zone exits to resolve later
        self._unresolved_exits = []     # exits that failed first-pass resolution
        self._deferred_patrols = []     # patrol definitions resolved in build()
        self._zone_obj = None           # ZoneObject created in zone()
        self._build_warnings = []       # non-fatal issues
        self._exits_created = 0
        self._node_config = None        # stored by node(), applied in build()
        self._social_nodes = {}         # node_key -> literal authored definition
        self._social_edges = {}         # edge_key -> literal authored definition

    # ------------------------------------------------------------------
    # zone()
    # ------------------------------------------------------------------

    def zone(self, **kwargs):
        """
        Register zone metadata. Creates or retrieves the ZoneObject.

        Required kwargs: name, zone_type, continent
        """
        name = kwargs.get("name")
        zone_type = kwargs.get("zone_type")
        continent = kwargs.get("continent")

        if not name:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — name is required"
            )
        if zone_type and zone_type not in VALID_ZONE_TYPES:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — invalid zone_type '{zone_type}'. "
                f"Valid types: {', '.join(sorted(VALID_ZONE_TYPES))}"
            )
        if continent and continent not in VALID_CONTINENTS:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — invalid continent '{continent}'. "
                f"Valid: {', '.join(sorted(VALID_CONTINENTS))}"
            )
        node_type = kwargs.get("node_type")
        if node_type and node_type not in VALID_NODE_TYPES:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — invalid node_type '{node_type}'. "
                f"Valid: {', '.join(sorted(VALID_NODE_TYPES))}"
            )
        faction_territory = kwargs.get("faction_territory", "neutral")
        if faction_territory not in VALID_FACTION_TERRITORIES:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — invalid faction_territory "
                f"'{faction_territory}'. Valid: "
                f"{', '.join(sorted(VALID_FACTION_TERRITORIES))}"
            )

        # Find or create ZoneObject
        zone_obj = self._get_or_create_zone_object()

        # Clear zone-owned definition lists on every load so rebuilds cannot
        # inherit stale definitions from prior source versions.
        zone_obj.db.item_definitions = []
        zone_obj.db.quest_definitions = []
        zone_obj.db.material_definitions = []
        zone_obj.db.gathering_pools = []
        zone_obj.db.loot_table_overrides = {}

        # Set all zone metadata
        zone_obj.db.zone_id = self._zone_id
        zone_obj.db.name = name
        zone_obj.db.tier = kwargs.get("tier", 1)
        zone_obj.db.zone_type = zone_type
        zone_obj.db.continent = continent
        zone_obj.db.region = kwargs.get("region")
        zone_obj.db.hub_city = kwargs.get("hub_city")
        zone_obj.db.has_node = kwargs.get("has_node", False)
        zone_obj.db.node_type = node_type
        zone_obj.db.node_failure_start = kwargs.get("node_failure_start", 0)
        zone_obj.db.faction_territory = faction_territory
        zone_obj.db.faction_presence = kwargs.get("faction_presence", [])
        zone_obj.db.world_x = kwargs.get("world_x")
        zone_obj.db.world_y = kwargs.get("world_y")
        zone_obj.db.world_radius = kwargs.get("world_radius")
        zone_obj.db.fog_of_war = kwargs.get("fog_of_war", False)
        # DO NOT set level_floor or level_cap — removed from design

        # Tag for indexed lookup
        zone_obj.tags.add("zone_object", category="object_type")
        zone_obj.tags.add(self._zone_id, category="zone_id")

        self._zone_data = kwargs
        self._zone_obj = zone_obj

    def _get_or_create_zone_object(self):
        """Find existing ZoneObject for this zone_id, or create one."""
        from typeclasses.objects import SoravelonObject

        existing = evennia.search_tag("zone_object", category="object_type")
        for obj in existing:
            if (obj.db.zone_id or "") == self._zone_id:
                return obj

        zone_obj = create_object(
            SoravelonObject,
            key=f"zone_{self._zone_id}",
            location=None,
        )
        return zone_obj

    # ------------------------------------------------------------------
    # room()
    # ------------------------------------------------------------------

    def room(self, room_id, **kwargs):
        """
        Create or update a SoravelonRoom. Tags it with zone_id.
        Returns the room object for use in exit()/spawn()/etc.
        """
        room_obj = self._get_or_create_room(room_id, **kwargs)
        self._rooms[room_id] = room_obj
        return room_obj

    def _get_or_create_room(self, room_id, **kwargs):
        """
        Return existing room if already loaded, else create new one.
        Existing rooms found by room_id tag + zone_id filter.
        Updates attributes on existing rooms (reload = update in place).
        """
        candidates = evennia.search_tag(room_id, category="room_id")
        for room in candidates:
            if (room.db.zone_id or "") == self._zone_id:
                self._set_room_attrs(room, room_id, **kwargs)
                return room

        from typeclasses.rooms import SoravelonRoom
        room_obj = create_object(
            SoravelonRoom,
            key=kwargs.get("name", room_id),
            location=None,
        )
        self._set_room_attrs(room_obj, room_id, **kwargs)
        return room_obj

    def _set_room_attrs(self, room_obj, room_id, **kwargs):
        """Set all room attributes. Called on both create and update."""
        room_type = kwargs.get("room_type", "generic")

        room_obj.key = kwargs.get("name", room_id)
        room_obj.db.zone_id = self._zone_id
        room_obj.db.desc = kwargs.get("desc", "")
        room_obj.db.room_type = room_type
        room_obj.db.indoor = kwargs.get("indoor", False)
        room_obj.db.terrain = kwargs.get("terrain", "none")
        room_obj.db.flags = kwargs.get("flags", [])
        room_obj.db.ambient_echoes = kwargs.get("ambient_echoes", [])
        room_obj.db.ambient_interval = kwargs.get("ambient_interval", 60)
        room_obj.db.ambient_variance = kwargs.get("ambient_variance", 30)
        room_obj.db.time_echoes = kwargs.get("time_echoes", {})
        room_obj.db.grid_x = kwargs.get("grid_x", None)
        room_obj.db.grid_y = kwargs.get("grid_y", None)

        # Reset authored list attrs on every build to prevent stale data
        room_obj.db.spawn_definitions = []
        room_obj.db.npc_definitions = []
        room_obj.db.lore_fragments = kwargs.get("lore_fragments", [])
        room_obj.db.triggers = []
        room_obj.db.custom_commands = []
        room_obj.db.practice_opportunities = []

        # Crafting station tags — clear stale then re-add (D-05 reconciliation)
        room_obj.tags.clear(category="crafting_station")
        crafting_stations = kwargs.get("crafting_stations", [])
        for station in crafting_stations:
            room_obj.tags.add(f"crafting_{station}", category="crafting_station")

        room_obj.tags.add(self._zone_id, category="zone_id")
        room_obj.tags.add(room_id, category="room_id")
        room_obj.tags.add(room_type, category="room_type")
        room_obj.tags.add("soravelon_room", category="room_type")

    # ------------------------------------------------------------------
    # exit()
    # ------------------------------------------------------------------

    def exit(self, from_room, to_room, direction, **kwargs):
        """
        Create an exit between rooms.

        to_room can be a room object (local) or a string
        "zone_id:room_id" for cross-zone exits.

        Silently ignores requires_level (no level gates in design).
        """
        if direction not in VALID_DIRECTIONS:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — invalid direction '{direction}'. "
                f"Valid: {', '.join(sorted(VALID_DIRECTIONS))}"
            )

        # Strip deprecated requires_level
        kwargs.pop("requires_level", None)

        if isinstance(to_room, str) and ":" in to_room:
            # Cross-zone exit — defer resolution
            self._deferred_exits.append({
                "from_room": from_room,
                "to": to_room,
                "direction": direction,
                **kwargs,
            })
            return

        # Local exit — create immediately
        self._create_exit_object(from_room, to_room, direction, **kwargs)

    def _create_exit_object(self, from_room, to_room, direction, **kwargs):
        """Create the actual exit object between two rooms."""
        from typeclasses.exits import SoravelonExit, LockedExit, HiddenExit

        hidden = kwargs.get("hidden", False)
        locked = kwargs.get("locked", False)

        if hidden:
            typeclass = HiddenExit
        elif locked:
            typeclass = LockedExit
        else:
            typeclass = SoravelonExit

        # Check for existing exit (idempotent)
        existing_exits = [
            ex for ex in from_room.exits
            if ex.key == direction and ex.destination == to_room
        ]
        if existing_exits:
            exit_obj = existing_exits[0]
        else:
            exit_obj = create_object(
                typeclass,
                key=direction,
                location=from_room,
                destination=to_room,
            )
            self._exits_created += 1

        # Reset ALL exit attrs to defaults, then apply from spec (D-06)
        exit_obj.db.desc = kwargs.get("desc", "")
        exit_obj.db.lock_tag = kwargs.get("lock_tag") if locked else None
        exit_obj.db.hidden = kwargs.get("hidden", False)
        exit_obj.db.requires_ancestry = kwargs.get("requires_ancestry")
        exit_obj.db.requires_standing = kwargs.get("requires_standing")
        exit_obj.db.requires_quest = kwargs.get("requires_quest")

        exit_obj.tags.add(self._zone_id, category="zone_id")
        if not hasattr(self, "_exit_ids"):
            self._exit_ids = set()
        self._exit_ids.add(exit_obj.id)

    # ------------------------------------------------------------------
    # spawn()
    # ------------------------------------------------------------------

    def spawn(self, room, mob, **kwargs):
        """
        Register a mob spawn definition on a room.
        Does NOT create mobs — spawning is handled at runtime.
        """
        validate_spawn_condition(kwargs.get("spawn_condition"))
        spawn_def = {
            "mob": mob,
            "behavior": kwargs.get("behavior", []),
            "flee_threshold": kwargs.get("flee_threshold", 20),
            "count_min": kwargs.get("count_min", 1),
            "count_max": kwargs.get("count_max", 1),
            "respawn_minutes": kwargs.get("respawn_minutes", 15),
            "respawn_variance": kwargs.get("respawn_variance", 5),
            "standing_check": kwargs.get("standing_check"),
            "base_disposition": kwargs.get("base_disposition", 0.0),
            "trust_sensitive": kwargs.get("trust_sensitive", False),
            # Named mob fields (D-13)
            "is_named": kwargs.get("is_named", False),
            "prestige_modifier": kwargs.get("prestige_modifier", 1.0),
            "tome_drop": kwargs.get("tome_drop"),
            "spawn_condition": kwargs.get("spawn_condition"),
            "sequence": kwargs.get("sequence", []),
        }

        # Idempotent: update existing definition for same mob template, or append
        current = list(room.db.spawn_definitions or [])
        replaced = False
        for i, existing in enumerate(current):
            if existing.get("mob") == mob:
                current[i] = spawn_def
                replaced = True
                break
        if not replaced:
            current.append(spawn_def)
        room.db.spawn_definitions = current

        from world.mob_templates import get_mob_template

        if get_mob_template(mob) is None:
            self._build_warnings.append(
                f"spawn in {self._room_id_for(room)} references mob "
                f"'{mob}' — verify template exists before loading to production"
            )

    # ------------------------------------------------------------------
    # named_mob()
    # ------------------------------------------------------------------

    def named_mob(self, mob_instance_id, room, **kwargs):
        """
        Register a named mob as a spawn definition.

        Named mobs are spawn definitions with is_named=True. They flow
        through the same spawn_definitions list as regular mobs — no
        separate named_mob_definitions room attr.

        Args:
            mob_instance_id: Unique string ID for this named mob (also the mob template key).
            room: Room object where the named mob spawns.
            **kwargs: respawn_minutes (default 120), respawn_variance (default 30),
                      tome_drop, spawn_condition, sequence, prestige_modifier,
                      behavior, base_disposition, flee_threshold.
        Returns:
            self (for method chaining)
        """
        self.spawn(
            room,
            mob_instance_id,
            is_named=True,
            count_min=1,
            count_max=1,
            respawn_minutes=kwargs.get("respawn_minutes", 120),
            respawn_variance=kwargs.get("respawn_variance", 30),
            prestige_modifier=kwargs.get("prestige_modifier", 1.0),
            tome_drop=kwargs.get("tome_drop"),
            spawn_condition=kwargs.get("spawn_condition"),
            sequence=kwargs.get("sequence", []),
            behavior=kwargs.get("behavior", []),
            base_disposition=kwargs.get("base_disposition", 0.0),
            flee_threshold=kwargs.get("flee_threshold", 20),
        )
        return self

    # ------------------------------------------------------------------
    # npc()
    # ------------------------------------------------------------------

    def npc(self, room, npc_id, **kwargs):
        """
        Place an NPC definition on a room and create/update a SoravelonMob object.

        Accepts optional ``dialogue`` and ``ambient`` dicts to configure NPC
        dialogue and ambient idle/reactive echo data (NPC-01).  The NPC object
        is a SoravelonMob with ``db.is_npc = True`` and ``db.combat_enabled = False``.

        Backward-compatible: ``room.db.npc_definitions`` is always populated.
        """
        # --- 1. Populate room.db.npc_definitions (backward compat) ---------
        npc_def = {
            "npc_id": npc_id,
            "wander": kwargs.get("wander", False),
            "quest": kwargs.get("quest"),
            "faction": kwargs.get("faction"),
            "standing_required": kwargs.get("standing_required"),
            "social_profile": kwargs.get("social_profile", {}),
            "social_edges": kwargs.get("social_edges", []),
        }

        current = list(room.db.npc_definitions or [])
        replaced = False
        for i, existing in enumerate(current):
            if existing.get("npc_id") == npc_id:
                current[i] = npc_def
                replaced = True
                break
        if not replaced:
            current.append(npc_def)
        room.db.npc_definitions = current

        # --- 2. Create or retrieve the NPC SoravelonMob object -------------
        from typeclasses.mobs import SoravelonMob

        # Idempotent: search by npc_id tag within this zone
        candidates = evennia.search_tag(npc_id, category="npc_id")
        npc_obj = None
        for candidate in candidates:
            if (candidate.db.zone_id or "") == self._zone_id:
                npc_obj = candidate
                break

        if not npc_obj:
            npc_obj = create_object(
                SoravelonMob,
                key=kwargs.get("name", npc_id.replace("_", " ").title()),
                location=room,
            )
        else:
            if npc_obj.location != room:
                npc_obj.move_to(room, quiet=True, move_hooks=False)
            npc_obj.key = kwargs.get("name", npc_id.replace("_", " ").title())

        # Core NPC flags
        npc_obj.db.is_npc = True
        npc_obj.db.combat_enabled = False
        npc_obj.db.zone_id = self._zone_id
        npc_obj.db.faction = kwargs.get("faction")
        npc_obj.db.npc_id = npc_id

        # Tags for queryset filtering
        npc_obj.tags.add(npc_id, category="npc_id")
        npc_obj.tags.add(self._zone_id, category="zone_id")
        npc_obj.tags.add("npc", category="character_type")
        self._npc_ids.add(npc_id)
        npc_obj.tags.add("npc", category="mob_type")

        # Trainer binding (SKL-01)
        trainer_id = kwargs.get("trainer_id")
        if trainer_id:
            npc_obj.db.trainer_id = trainer_id
            npc_obj.tags.add(trainer_id, category="trainer_id")

        # --- 3. Dialogue data on db attributes (NPC-01) -------------------
        dialogue = kwargs.get("dialogue", {})
        npc_obj.db.dialogue_greeting_tiers = dialogue.get("greeting_tiers", {})
        npc_obj.db.dialogue_topics = dialogue.get("topics", {})
        npc_obj.db.dialogue_base_hints = dialogue.get("base_hints", [])
        npc_obj.db.dialogue_tier_hints = dialogue.get("tier_hints", {})
        npc_obj.db.dialogue_quest_hints = dialogue.get("quest_hints", {})
        npc_obj.db.dialogue_network_hints = dialogue.get("network_hints", [])
        npc_obj.db.dialogue_scholar_hints = dialogue.get("scholar_hints", [])
        npc_obj.db.dialogue_warden_hints = dialogue.get("warden_hints", [])

        # --- 4. Social Web authoring metadata -----------------------------
        npc_obj.db.social_profile = kwargs.get("social_profile", {})
        npc_obj.db.social_edges = kwargs.get("social_edges", [])

        # --- 5. Ambient data on db attributes (NPC-01) --------------------
        ambient = kwargs.get("ambient", {})
        npc_obj.db.ambient_idle_echoes = ambient.get("idle_echoes", [])
        npc_obj.db.ambient_idle_interval = ambient.get("idle_interval", 60)
        npc_obj.db.ambient_idle_variance = ambient.get("idle_variance", 30)
        npc_obj.db.ambient_reactive_echoes = ambient.get("reactive_echoes", {})

        return npc_obj

    # ------------------------------------------------------------------
    # social_node() / social_edge()
    # ------------------------------------------------------------------

    def social_node(self, node_type, identifier, **kwargs):
        """Author one persistent Social Web node owned by this zone."""
        from world.social_topology import validate_social_node_definition

        try:
            validate_social_node_definition(node_type, identifier, **kwargs)
        except ValueError as exc:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — {exc}"
            ) from exc

        node_key = f"{node_type}:{identifier}"
        self._social_nodes[node_key] = {
            "node_type": node_type,
            "identifier": identifier,
            "display_name": kwargs.get("display_name", ""),
            "zone_id": kwargs.get("zone_id") or self._zone_id,
            "settlement_id": kwargs.get("settlement_id", ""),
            "faction_id": kwargs.get("faction_id", ""),
            "metadata": copy.deepcopy(kwargs.get("metadata") or {}),
        }
        return self

    def social_edge(self, source_node_key, target_node_key, **kwargs):
        """Author one persistent Social Web edge owned by this zone."""
        from world.social_topology import (
            social_edge_key,
            validate_social_edge_definition,
        )

        edge_type = kwargs.get("edge_type")
        edge_kwargs = {key: value for key, value in kwargs.items() if key != "edge_type"}
        try:
            validate_social_edge_definition(
                source_node_key,
                target_node_key,
                edge_type=edge_type,
                **edge_kwargs,
            )
        except ValueError as exc:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — {exc}"
            ) from exc

        edge_key = social_edge_key(source_node_key, target_node_key, edge_type)
        self._social_edges[edge_key] = {
            "source_node_key": source_node_key,
            "target_node_key": target_node_key,
            "edge_type": edge_type,
            "directionality": kwargs.get("directionality", "one_way"),
            "trust": kwargs.get("trust", 0.5),
            "latency_seconds": kwargs.get("latency_seconds", 0),
            "bandwidth": kwargs.get("bandwidth", 3),
            "secrecy": kwargs.get("secrecy", ""),
            "distortion": kwargs.get("distortion", ""),
            "scope_tags": copy.deepcopy(kwargs.get("scope_tags") or []),
            "blockers": copy.deepcopy(kwargs.get("blockers") or []),
            "required_tags": copy.deepcopy(kwargs.get("required_tags")),
            "blocked_tags": copy.deepcopy(kwargs.get("blocked_tags")),
        }
        return self

    # ------------------------------------------------------------------
    # item()
    # ------------------------------------------------------------------

    def item(self, item_id, **kwargs):
        """
        Register an item template definition on this zone.
        Stored on zone_obj.db.item_definitions for use by item_spawner.

        Args:
            item_id: Unique string ID for this item within the zone.
            **kwargs: Item properties — key, item_type, weight, rarity,
                      equip_slot, desc, value, plus any extras.
        Returns:
            self (for method chaining)
        """
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — item() called before zone()"
            )
        item_def = {"item_id": item_id, **kwargs}
        current = list(self._zone_obj.db.item_definitions or [])
        replaced = False
        for i, existing in enumerate(current):
            if existing.get("item_id") == item_id:
                current[i] = item_def
                replaced = True
                break
        if not replaced:
            current.append(item_def)
        self._zone_obj.db.item_definitions = current
        return self

    # ------------------------------------------------------------------
    # loot_table_override()
    # ------------------------------------------------------------------

    def loot_table_override(
        self,
        mob_type,
        *,
        relevant_skill="combat",
        base_drop_chance=0.7,
        drops=None,
    ):
        """
        Register zone-specific random drops for one mob type.

        Stored on zone_obj.db.loot_table_overrides for world.loot_tables.
        """
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — loot_table_override() called before zone()"
            )
        if not isinstance(mob_type, str) or not mob_type:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — loot_table_override() mob_type is required"
            )
        if drops is None:
            drops = []
        if not isinstance(drops, list):
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — loot_table_override('{mob_type}') drops must be a list"
            )

        override = {
            "mob_type": mob_type,
            "relevant_skill": relevant_skill,
            "base_drop_chance": base_drop_chance,
            "drops": copy.deepcopy(drops),
        }
        current = dict(self._zone_obj.db.loot_table_overrides or {})
        current[mob_type] = override
        self._zone_obj.db.loot_table_overrides = current
        return self

    # ------------------------------------------------------------------
    # mob()
    # ------------------------------------------------------------------

    def mob(self, mob_key, room, **kwargs):
        """
        Create or retrieve a named mob object and place it in a room.
        Registers the mob in self._mobs for use by patrol().

        Args:
            mob_key: Unique string identifier for this mob within the zone.
            room: Room object where the mob is placed.
        Returns:
            The mob object.
        """
        from typeclasses.mobs import SoravelonMob

        # Look for existing mob with this key in this zone
        import evennia as _evennia
        candidates = _evennia.search_object(mob_key, typeclass=SoravelonMob)
        mob_obj = None
        for candidate in candidates:
            if (candidate.db.zone_id or "") == self._zone_id:
                mob_obj = candidate
                break

        if not mob_obj:
            mob_obj = create_object(
                SoravelonMob,
                key=mob_key,
                location=room,
            )
        else:
            if mob_obj.location != room:
                mob_obj.move_to(room, quiet=True, move_hooks=False)

        mob_obj.db.zone_id = self._zone_id
        mob_obj.tags.add(self._zone_id, category="zone_id")
        for attr, val in kwargs.items():
            setattr(mob_obj.db, attr, val)

        self._mobs[mob_key] = mob_obj
        return mob_obj

    # ------------------------------------------------------------------
    # patrol()
    # ------------------------------------------------------------------

    def patrol(self, mob_key, route_room_ids, interrupt_mode="resume",
               encounter_delay=0, echo_radius=0, move_echo=None, combat_enabled=True):
        """
        Attach a PatrolScript to a mob and define its walking route.

        Args:
            mob_key: The key of a mob already registered with area.mob()
            route_room_ids: Ordered list of room_id strings (keys in self._rooms)
            interrupt_mode: "resume" | "reset_to_start" | "abandon" (D-01, IWA-03)
            encounter_delay: Seconds before disposition check on arrival (D-01)
            echo_radius: BFS radius for arrival echo messages (D-04)
            move_echo: Message broadcast on each move. Defaults to mob key.
            combat_enabled: False for invulnerable mobs like Caldenmere (D-03)
        Returns:
            self (for method chaining)
        """
        if interrupt_mode not in ("resume", "reset_to_start", "abandon"):
            raise AreaBuilderValidationError(
                f"patrol() interrupt_mode must be 'resume', 'reset_to_start', or 'abandon';"
                f" got '{interrupt_mode}'"
            )
        self._deferred_patrols.append({
            "mob_key": mob_key,
            "route_room_ids": route_room_ids,
            "interrupt_mode": interrupt_mode,
            "encounter_delay": encounter_delay,
            "echo_radius": echo_radius,
            "move_echo": move_echo or f"{mob_key} passes through.",
            "combat_enabled": combat_enabled,
        })
        return self

    # ------------------------------------------------------------------
    # trigger()
    # ------------------------------------------------------------------

    def trigger(self, source_obj_or_id, event, actions,
                trigger_id=None, once_per_character=False, cooldown_seconds=0):
        """
        Attach a trigger to a room, mob, or item.

        Args:
            source_obj_or_id: Room object, room_id string, mob object, or mob key string
            event: "on_enter" | "on_exit" | "on_first_visit" | "on_mob_death"
            actions: List of action dicts, e.g. [{"action_type": "echo", "message": "hello"}]
            trigger_id: Unique string ID for once-per and cooldown tracking. Auto-generated if None.
            once_per_character: Fire at most once per character (D-07)
            cooldown_seconds: Minimum seconds between fires for same character (D-07)
        Returns:
            self (for method chaining)
        """
        VALID_EVENTS = {"on_enter", "on_exit", "on_first_visit", "on_mob_death", "on_examine"}
        if event not in VALID_EVENTS:
            raise AreaBuilderValidationError(
                f"trigger() event must be one of {VALID_EVENTS}; got '{event}'"
            )
        # Resolve source object
        if isinstance(source_obj_or_id, str):
            source_obj = self._rooms.get(source_obj_or_id) or self._mobs.get(source_obj_or_id)
        else:
            source_obj = source_obj_or_id
        if not source_obj:
            self._build_warnings.append(f"trigger(): source '{source_obj_or_id}' not found")
            return self
        auto_id = trigger_id or f"{self._zone_id}_{event}_{len(source_obj.db.triggers or [])}"
        trigger_dict = {
            "trigger_id": auto_id,
            "event": event,
            "actions": list(actions),
            "once_per_character": once_per_character,
            "cooldown_seconds": cooldown_seconds,
        }
        # SaverDict copy pattern
        existing = list(source_obj.db.triggers or [])
        existing.append(trigger_dict)
        source_obj.db.triggers = existing
        return self

    # ------------------------------------------------------------------
    # custom_command()
    # ------------------------------------------------------------------

    def custom_command(self, target_obj_or_id, key, action_dict,
                       visible_in_exits=False, aliases=None, desc=None):
        """
        Attach a custom command to a room, mob, or item.

        Args:
            target_obj_or_id: Target object or room_id/mob_key string
            key: Command keyword players type (e.g., "climb")
            action_dict: Action dict executed when command fires
            visible_in_exits: If True, appears in room Interactions list (D-21)
            aliases: List of alternative keywords
            desc: Description shown in Interactions list if visible_in_exits=True
        Returns:
            self (for method chaining)
        """
        if isinstance(target_obj_or_id, str):
            target = self._rooms.get(target_obj_or_id) or self._mobs.get(target_obj_or_id)
        else:
            target = target_obj_or_id
        if not target:
            self._build_warnings.append(
                f"custom_command(): target '{target_obj_or_id}' not found"
            )
            return self
        cmd_def = {
            "key": key,
            "action_dict": action_dict,
            "visible_in_exits": visible_in_exits,
            "aliases": aliases or [],
            "desc": desc or "",
        }
        # Store definition on object (idempotent — replace by key)
        existing = list(target.db.custom_commands or [])
        replaced = False
        for i, ex in enumerate(existing):
            if ex.get("key") == key:
                existing[i] = cmd_def
                replaced = True
                break
        if not replaced:
            existing.append(cmd_def)
        target.db.custom_commands = existing
        # Rebuild one owned dynamic CmdSet per target to avoid duplicate registrations.
        from commands.cmd_dynamic import build_dynamic_cmdset
        cmdset_key = f"DynamicAreaCmdSet_{target.id}"
        try:
            target.cmdset.remove(cmdset_key)
        except Exception:
            pass
        target.cmdset.add(
            build_dynamic_cmdset(existing, cmdset_key=cmdset_key),
            persistent=True,
        )
        return self

    # ------------------------------------------------------------------
    # practice_opportunity()
    # ------------------------------------------------------------------

    def practice_opportunity(self, opportunity_id, room, **kwargs):
        """
        Register a builder-safe practice opportunity in a room.

        The editable metadata is stored on the room and a dynamic command is
        wired through action_vocabulary so runtime behavior has one path.
        """
        if isinstance(room, str):
            room_obj = self._rooms.get(room)
        else:
            room_obj = room
        if not room_obj:
            self._build_warnings.append(
                f"practice_opportunity(): room '{room}' not found"
            )
            return self

        verb = kwargs.get("verb")
        if not verb:
            raise AreaBuilderValidationError("practice_opportunity() requires a verb")

        practice_def = {
            "opportunity_id": opportunity_id,
            "verb": verb,
            "target": kwargs.get("target", ""),
            "skill_awards": kwargs.get("skill_awards", {}),
            "domain_awards": kwargs.get("domain_awards", {}),
            "success_text": kwargs.get("success_text", ""),
            "failure_text": kwargs.get("failure_text", ""),
            "once_per_character": kwargs.get("once_per_character", True),
            "cooldown_seconds": kwargs.get("cooldown_seconds", 0),
        }

        from world.practice_engine import validate_practice_payload
        valid, validation_msg = validate_practice_payload(practice_def)
        if not valid:
            if validation_msg == "That practice is not available.":
                validation_msg = "practice_opportunity() uses a hidden current-era domain"
            raise AreaBuilderValidationError(validation_msg)

        existing_practice = list(room_obj.db.practice_opportunities or [])
        replaced = False
        for i, existing in enumerate(existing_practice):
            if existing.get("opportunity_id") == opportunity_id:
                existing_practice[i] = practice_def
                replaced = True
                break
        if not replaced:
            existing_practice.append(practice_def)
        room_obj.db.practice_opportunities = existing_practice

        self.custom_command(
            room_obj,
            verb,
            {"action_type": "grant_practice", **practice_def},
            visible_in_exits=kwargs.get("visible_in_exits", kwargs.get("visible", False)),
            aliases=kwargs.get("aliases"),
            desc=kwargs.get("desc"),
        )
        return self

    # ------------------------------------------------------------------
    # flight_point()
    # ------------------------------------------------------------------

    def flight_point(self, room_or_id, point_id, name=None):
        """
        Mark a room as a Dragon Courier flight stop.

        Args:
            room_or_id: Room object or room_id string
            point_id: Unique string ID for this stop (e.g., "vaels_crossing_docks")
            name: Display name shown in flight listings. Defaults to room name.
        Returns:
            self (for method chaining)
        """
        if isinstance(room_or_id, str):
            room = self._rooms.get(room_or_id)
        else:
            room = room_or_id
        if not room:
            self._build_warnings.append(f"flight_point(): room '{room_or_id}' not found")
            return self
        from world.flight_registry import FlightRegistry
        FlightRegistry.register_point(point_id, room, name=name)
        # Tag the room for discovery detection
        room.tags.add("flight_point", category="travel")
        room.db.flight_point_id = point_id
        return self

    # ------------------------------------------------------------------
    # flight_route()
    # ------------------------------------------------------------------

    def flight_route(self, point_a_id, point_b_id, base_fare, leg_duration=30, echoes=None):
        """
        Define a Dragon Courier connection between two flight points.

        Args:
            point_a_id: ID of origin flight point
            point_b_id: ID of destination flight point
            base_fare: Base cost in scales before Standing discount
            leg_duration: Seconds for this leg (D-10: minimum 30)
            echoes: List of {"delay": N, "message": "..."} dicts for in-flight narration
        Returns:
            self (for method chaining)
        """
        if leg_duration < 30:
            raise AreaBuilderValidationError(
                f"flight_route() leg_duration must be >= 30 seconds; got {leg_duration}"
            )
        from world.flight_registry import FlightRegistry
        FlightRegistry.register_route(point_a_id, point_b_id, base_fare, leg_duration, echoes or [])
        return self

    # ------------------------------------------------------------------
    # node()
    # ------------------------------------------------------------------

    def node(self, center_room, radius, **kwargs):
        """
        Configure the node for this zone.
        Defers actual initialization to build() so all rooms exist first.
        """
        self._node_config = {
            "center_room": center_room,
            "radius": radius,
            "lore_fragments": kwargs.get("lore_fragments", []),
            "layer_1_overrides": kwargs.get("layer_1_overrides", {}),
        }

    # ------------------------------------------------------------------
    # quest()
    # ------------------------------------------------------------------

    def quest(self, quest_id, **kwargs):
        """
        Register a quest definition on the zone object.
        Accepts both legacy flat format and new enriched format.
        Per D-21: DSL stores all fields needed by quest_engine.py.
        Per D-22: All fields JSON-serializable for builder app.
        """
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — quest() called before zone()"
            )

        quest_def = {
            "quest_id": quest_id,
            # New enriched fields (D-21, D-22)
            "name": kwargs.get("name", quest_id),
            "description": kwargs.get("description", ""),
            "quest_type": kwargs.get("quest_type"),
            "quest_giver": kwargs.get("quest_giver"),
            "objectives": kwargs.get("objectives", []),
            "rewards": kwargs.get("rewards", []),
            "next_quest_id": kwargs.get("next_quest_id"),
            "prerequisite_quests": kwargs.get("prerequisite_quests", []),
            "one_chance": kwargs.get("one_chance", False),
            # Social Web quest grammar metadata
            "incident_seed": kwargs.get("incident_seed"),
            "quest_archetype": kwargs.get("quest_archetype"),
            "social_quest_context": kwargs.get("social_quest_context"),
            # Sharing (deferred but stored for future use)
            "can_share": kwargs.get("can_share", False),
            "share_radius": kwargs.get("share_radius", 1),
            "share_cap": kwargs.get("share_cap", 6),
            # Legacy flat fields (backward compat — quest_engine normalizes)
            "objective_type": kwargs.get("objective_type"),
            "objective_target": kwargs.get("objective_target"),
            "objective_count": kwargs.get("objective_count", 1),
            "flagged_drop": kwargs.get("flagged_drop"),
            "reward_tiers": kwargs.get("reward_tiers", {}),
            "world_expression": kwargs.get("world_expression", {}),
            "consequence_small": kwargs.get("consequence_small"),
            "consequence_medium": kwargs.get("consequence_medium"),
        }

        # Silently ignore level_range (legacy field, no visible levels)

        current = list(self._zone_obj.db.quest_definitions or [])
        replaced = False
        for i, existing in enumerate(current):
            if existing.get("quest_id") == quest_id:
                current[i] = quest_def
                replaced = True
                break
        if not replaced:
            current.append(quest_def)
        self._zone_obj.db.quest_definitions = current

    # ------------------------------------------------------------------
    # material()
    # ------------------------------------------------------------------

    def material(self, material, **kwargs):
        """Register a harvestable material for this zone."""
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — material() called before zone()"
            )

        material_def = {
            "material": material,
            "tier": kwargs.get("tier", 1),
            "terrain": kwargs.get("terrain"),
            "absorbed_property": kwargs.get("absorbed_property"),
            "profession_bonus": kwargs.get("profession_bonus", {}),
        }

        current = list(self._zone_obj.db.material_definitions or [])
        replaced = False
        for i, existing in enumerate(current):
            if existing.get("material") == material:
                current[i] = material_def
                replaced = True
                break
        if not replaced:
            current.append(material_def)
        self._zone_obj.db.material_definitions = current

    # ------------------------------------------------------------------
    # gathering_pool()
    # ------------------------------------------------------------------

    def gathering_pool(self, pool_type, rooms, materials, **kwargs):
        """
        Register a gathering pool definition on this zone (per D-02).

        Args:
            pool_type: Category string from GATHERING_CATEGORIES (ore, herb, wood, forage, fish, hide)
            rooms: List of room_id strings (must be defined via room() first)
            materials: List of material_id strings from MATERIAL_REGISTRY
            **kwargs: max_active (default 3), respawn_minutes (default 15),
                      respawn_variance (default 5), tier_floor (default 1), tier_ceiling (default 3)

        Returns: self (for chaining)
        """
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' -- gathering_pool() called before zone()"
            )

        pool_def = {
            "pool_type": pool_type,
            "room_ids": rooms,
            "materials": materials,
            "max_active": kwargs.get("max_active", 3),
            "respawn_minutes": kwargs.get("respawn_minutes", 15),
            "respawn_variance": kwargs.get("respawn_variance", 5),
            "tier_floor": kwargs.get("tier_floor", 1),
            "tier_ceiling": kwargs.get("tier_ceiling", 3),
        }
        # SaverDict copy pattern (critical rule #1 from area-builder skill)
        current = list(self._zone_obj.db.gathering_pools or [])
        current.append(pool_def)
        self._zone_obj.db.gathering_pools = current
        return self

    # ------------------------------------------------------------------
    # lore_fragment()
    # ------------------------------------------------------------------

    def lore_fragment(self, fragment_id, room, **kwargs):
        """Place a lore fragment discovery in a room."""
        frag_def = {
            "fragment_id": fragment_id,
            "discovery_method": kwargs.get("discovery_method", "search"),
            "scholar_path": kwargs.get("scholar_path"),
            "text": kwargs.get("text", ""),
            "insight_gain": kwargs.get("insight_gain", 0),
        }

        current = list(room.db.lore_fragments or [])
        replaced = False
        for i, existing in enumerate(current):
            if existing.get("fragment_id") == fragment_id:
                current[i] = frag_def
                replaced = True
                break
        if not replaced:
            current.append(frag_def)
        room.db.lore_fragments = current

    # ------------------------------------------------------------------
    # build()
    # ------------------------------------------------------------------

    def build(self):
        """
        Finalize the build.

        1. Resolve deferred cross-zone exits
        2. Initialize node if has_node=True
        3. Finalize patrol definitions
        3.5 Assign grid coordinates (auto-layout)
        4. Register zone in global zone registry
        5. Return build report
        """
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — build() called before zone()"
            )

        # 1. Resolve cross-zone exits
        self._resolve_cross_zone_exits()

        # 2. Initialize node if configured
        if self._node_config and self._zone_data.get("has_node"):
            self._initialize_node()

        # 3. Finalize patrol definitions
        self._finalize_patrols()

        # 3.5: Assign grid coordinates to rooms without explicit coords (CLI-07)
        auto_layout_zone(self._rooms)

        # 3.55: Register literal Social Web topology. Cross-zone edges resolve
        # after every area file has registered its nodes during server startup.
        from world.social_topology import register_zone_social_topology
        social_topology_report = register_zone_social_topology(
            self._zone_id,
            nodes=self._social_nodes.values(),
            edges=self._social_edges.values(),
        )

        # 3.6: Reconcile stale objects (D-01 through D-04)
        reconcile_report = self._reconcile_stale_objects()

        # 4. Register zone
        zone_registry.register_zone(self._zone_id, self._zone_obj)

        # 6. Zone-owned definition lists are reset in zone() before the file
        # re-registers them through quest()/material()/item()/gathering_pool().

        # 5. Initialize gathering pools
        from world.gathering_engine import initialize_zone_gathering
        initialize_zone_gathering(self._zone_obj)

        return {
            "zone_id": self._zone_id,
            "rooms_created": len(self._rooms),
            "exits_created": self._exits_created,
            "warnings": list(self._build_warnings),
            "unresolved_exits": [
                {"to": e["to"], "direction": e["direction"]}
                for e in self._unresolved_exits
            ],
            "social_topology": social_topology_report,
            "reconciled": reconcile_report,
        }

    def _reconcile_stale_objects(self):
        """
        Post-build sweep: hard-delete zone-owned DB objects not in current spec.

        Order: exits -> NPCs -> mobs -> rooms (rooms last because their
        contents must be cleaned first).

        Per D-04: runtime-spawned mobs (those with mob_instance_id tag)
        are exempt — only builder-authored mob() objects are reconciled.
        """
        from world.mob_spawner import MOB_INSTANCE_TAG_CATEGORY
        from typeclasses.mobs import SoravelonMob
        from typeclasses.characters import Character
        from django.conf import settings as django_settings
        from evennia.utils import logger

        zone_id = self._zone_id
        spec_room_ids = set(self._rooms.keys())
        spec_mob_keys = set(self._mobs.keys())
        spec_npc_ids = set(self._npc_ids)

        report = {"rooms_deleted": 0, "exits_deleted": 0,
                  "npcs_deleted": 0, "mobs_deleted": 0,
                  "players_evicted": 0}

        # --- Eviction target (D-01 fallback chain) ---
        eviction_target = None
        for tag_key in ("respawn_point", "greeter_room"):
            candidates = evennia.search_tag(tag_key, category="spawn_point")
            for room in candidates:
                if (room.db.zone_id or "") == zone_id:
                    eviction_target = room
                    break
            if eviction_target:
                break
        if not eviction_target:
            fallback_id = getattr(django_settings, "DEFAULT_HOME", None)
            if fallback_id:
                from evennia.objects.models import ObjectDB
                # DEFAULT_HOME may be Evennia '#N' format — strip the '#'
                raw = str(fallback_id).lstrip("#")
                try:
                    eviction_target = ObjectDB.objects.get(id=int(raw))
                except (ObjectDB.DoesNotExist, ValueError, TypeError):
                    pass

        # Collect all zone-owned objects once
        all_zone_objects = evennia.search_tag(zone_id, category="zone_id")

        # --- 1. Orphan exits (D-02) ---
        from typeclasses.exits import SoravelonExit
        for obj in all_zone_objects:
            if not obj.pk:
                continue
            try:
                is_exit = isinstance(obj, SoravelonExit) or obj.destination is not None
            except Exception:
                # db_destination access can fail on stale/deleted objects
                is_exit = isinstance(obj, SoravelonExit)
            if is_exit and obj.id not in self._exit_ids:
                obj.delete()
                report["exits_deleted"] += 1

        # --- 2. Orphan NPCs (D-03) ---
        for obj in all_zone_objects:
            if not obj.pk:
                continue
            if getattr(obj.db, 'is_npc', False):
                npc_id_tag = obj.tags.get(category="npc_id")
                if npc_id_tag and npc_id_tag not in spec_npc_ids:
                    obj.delete()
                    report["npcs_deleted"] += 1

        # --- 3. Orphan builder mob() objects (D-03, D-04) ---
        for obj in all_zone_objects:
            if not obj.pk:
                continue
            if not isinstance(obj, SoravelonMob):
                continue
            if getattr(obj.db, 'is_npc', False):
                continue  # NPCs handled above
            # Skip runtime-spawned mobs (D-04)
            if obj.tags.has(category=MOB_INSTANCE_TAG_CATEGORY):
                continue
            # This is a builder mob — check if still in spec
            if obj.key not in spec_mob_keys:
                obj.delete()
                report["mobs_deleted"] += 1

        # --- 4. Orphan rooms (D-01) — last, after contents cleaned ---
        for obj in all_zone_objects:
            if not obj.pk:
                continue
            room_id_tag = obj.tags.get(category="room_id")
            if not room_id_tag:
                continue
            if not hasattr(obj, 'exits'):
                continue  # Not a room
            if room_id_tag not in spec_room_ids:
                # Evict players first
                for content in list(obj.contents):
                    if isinstance(content, Character) and eviction_target:
                        content.msg(
                            "|yYou have been moved — the area you "
                            "were in has been restructured.|n"
                        )
                        content.move_to(
                            eviction_target, quiet=True, move_hooks=False
                        )
                        report["players_evicted"] += 1
                obj.delete()
                report["rooms_deleted"] += 1

        if any(v > 0 for v in report.values()):
            logger.log_info(
                f"[AreaBuilder] Zone '{zone_id}' reconciliation: {report}"
            )

        return report

    def _resolve_cross_zone_exits(self):
        """Resolve deferred cross-zone exits by tag lookup.

        Unresolved exits are saved to both self._unresolved_exits and the
        module-level _UNRESOLVED_EXITS_REGISTRY for second-pass retry by
        _load_all_zones() (BLD-06).
        """
        for exit_data in self._deferred_exits:
            target_str = exit_data["to"]  # peek, don't pop
            target_zone_id, target_room_id = target_str.split(":", 1)

            candidates = evennia.search_tag(
                target_room_id, category="room_id"
            )
            target = None
            for room in candidates:
                if (room.db.zone_id or "") == target_zone_id:
                    target = room
                    break

            if not target:
                self._build_warnings.append(
                    f"Cross-zone exit unresolved: {target_str} "
                    f"(target zone may not be loaded yet)"
                )
                # Save for second-pass retry — keep full dict intact
                unresolved_copy = dict(exit_data)
                self._unresolved_exits.append(unresolved_copy)
                _UNRESOLVED_EXITS_REGISTRY.append(unresolved_copy)
                continue

            # Resolved — build the exit
            resolved = dict(exit_data)
            resolved.pop("to")
            from_room = resolved.pop("from_room")
            direction = resolved.pop("direction")
            self._create_exit_object(from_room, target, direction, **resolved)

    def expose_unresolved_exits(self):
        """
        Return unresolved cross-zone exits from the last build() call.
        Each item: {"from_room": room_obj, "to": "zone_id:room_id",
                     "direction": str, ...kwargs}
        Used by _load_all_zones() for second-pass retry.
        """
        return list(self._unresolved_exits)

    def _initialize_node(self):
        """Call the existing node system to set up this zone's node."""
        from world.zone_object import initialize_node

        config = self._node_config
        center_room = config["center_room"]
        radius = config["radius"]

        # All rooms in this zone are Layer 0 candidates
        layer0_rooms = list(self._rooms.values())

        initialize_node(
            zone_obj=self._zone_obj,
            node_type=self._zone_data.get("node_type", "resonance"),
            center_room=center_room,
            radius=radius,
            layer0_rooms=layer0_rooms,
            failure_start=self._zone_data.get("node_failure_start", 0),
        )

        # Store layer 1 overrides on zone obj for future use
        overrides = config.get("layer_1_overrides", {})
        if overrides:
            self._zone_obj.db.layer_1_overrides = overrides

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _finalize_patrols(self):
        """Attach PatrolScript to each mob registered via patrol()."""
        for patrol_def in self._deferred_patrols:
            mob = self._mobs.get(patrol_def["mob_key"])
            if not mob:
                self._build_warnings.append(
                    f"patrol(): mob '{patrol_def['mob_key']}' not found"
                )
                continue
            route_rooms = []
            for rid in patrol_def["route_room_ids"]:
                room = self._rooms.get(rid)
                if room:
                    route_rooms.append(room.id)
                else:
                    self._build_warnings.append(
                        f"patrol(): room_id '{rid}' not found in zone"
                    )
            if not route_rooms:
                continue
            mob.db.patrol = patrol_def
            mob.db.combat_enabled = patrol_def["combat_enabled"]
            from world.scripts.patrol_script import PatrolScript
            # Check for existing patrol script before creating (F8 idempotency)
            existing_patrols = mob.scripts.get("patrol_script")
            if existing_patrols:
                script = existing_patrols[0]
            else:
                script = mob.scripts.add(PatrolScript, key="patrol_script", persistent=True)
            # SaverDict copy pattern — assign as new list
            script.db.route_ids = list(route_rooms)
            script.db.route_index = 0
            script.db.patrol_def = dict(patrol_def)

    def _room_id_for(self, room_obj):
        """Find the room_id string for a room object."""
        for rid, robj in self._rooms.items():
            if robj.id == room_obj.id:
                return rid
        return f"dbref#{room_obj.id}"
