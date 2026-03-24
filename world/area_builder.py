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

import evennia
from evennia import create_object

from world import zone_registry, named_mob_registry


class AreaBuilderValidationError(Exception):
    """Raised when an area spec contains invalid values."""
    pass


# --- Validation constants ---

VALID_ZONE_TYPES = {
    "ancient_forest", "plains", "mountain", "coastal",
    "underground", "imperial_city", "frontier", "node_active",
}

VALID_CONTINENTS = {"varath", "sorath", "veluana"}

VALID_NODE_TYPES = {
    "resonance", "thermal", "gravity", "temporal", "cognitive",
}

VALID_FACTION_TERRITORIES = {
    "imperial", "neutral", "warden", "kauroran",
    "contested", "hidden",
}

VALID_DIRECTIONS = {
    "north", "south", "east", "west",
    "northeast", "northwest", "southeast", "southwest",
    "up", "down", "in", "out",
}

VALID_ROOM_TYPES = {
    "path", "clearing", "ruins", "cave", "building",
    "underground", "node_center", "generic",
}


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
        self._deferred_exits = []       # cross-zone exits to resolve later
        self._deferred_patrols = []     # patrol definitions resolved in build()
        self._zone_obj = None           # ZoneObject created in zone()
        self._build_warnings = []       # non-fatal issues
        self._exits_created = 0
        self._node_config = None        # stored by node(), applied in build()

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

        # Initialize list attrs only if not already present
        if not room_obj.db.spawn_definitions:
            room_obj.db.spawn_definitions = []
        if not room_obj.db.npc_definitions:
            room_obj.db.npc_definitions = []
        if not room_obj.db.lore_fragments:
            room_obj.db.lore_fragments = []
        if not room_obj.db.named_mob_definitions:
            room_obj.db.named_mob_definitions = []

        room_obj.tags.add(self._zone_id, category="zone_id")
        room_obj.tags.add(room_id, category="room_id")
        room_obj.tags.add(room_type, category="room_type")

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

        # Set exit attributes
        desc = kwargs.get("desc")
        if desc:
            exit_obj.db.desc = desc
        if locked:
            exit_obj.db.lock_tag = kwargs.get("lock_tag")
        if hidden:
            exit_obj.db.hidden = True

        # Conditional access attributes
        requires_ancestry = kwargs.get("requires_ancestry")
        if requires_ancestry:
            exit_obj.db.requires_ancestry = requires_ancestry
        requires_standing = kwargs.get("requires_standing")
        if requires_standing:
            exit_obj.db.requires_standing = requires_standing
        requires_quest = kwargs.get("requires_quest")
        if requires_quest:
            exit_obj.db.requires_quest = requires_quest

        exit_obj.tags.add(self._zone_id, category="zone_id")

    # ------------------------------------------------------------------
    # spawn()
    # ------------------------------------------------------------------

    def spawn(self, room, mob, **kwargs):
        """
        Register a mob spawn definition on a room.
        Does NOT create mobs — spawning is handled at runtime.
        """
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
        }

        # Copy current list, append, assign back (SaverDict pattern)
        current = list(room.db.spawn_definitions or [])
        current.append(spawn_def)
        room.db.spawn_definitions = current

        # Warn about unverified mob template
        self._build_warnings.append(
            f"spawn in {self._room_id_for(room)} references mob "
            f"'{mob}' — verify template exists before loading to production"
        )

    # ------------------------------------------------------------------
    # named_mob()
    # ------------------------------------------------------------------

    def named_mob(self, mob_id, room, **kwargs):
        """
        Register a named mob definition on a room.
        Named mobs are world-attached with lore.
        """
        named_def = {
            "mob_id": mob_id,
            "behavior": kwargs.get("behavior", []),
            "home_rooms": kwargs.get("home_rooms", []),
            "respawn_minutes": kwargs.get("respawn_minutes", 120),
            "tome_drop": kwargs.get("tome_drop"),
            "spawn_condition": kwargs.get("spawn_condition"),
            "sequence": kwargs.get("sequence", []),
        }

        # Convert any room objects in home_rooms to room IDs
        home_rooms = named_def["home_rooms"]
        resolved = []
        for hr in home_rooms:
            if hasattr(hr, "id"):
                # It's a room object — find its room_id
                rid = self._room_id_for(hr)
                resolved.append(rid)
            else:
                resolved.append(hr)
        named_def["home_rooms"] = resolved

        current = list(room.db.named_mob_definitions or [])
        current.append(named_def)
        room.db.named_mob_definitions = current

        # Store for registry in build()
        if not hasattr(self, "_named_mobs"):
            self._named_mobs = []
        self._named_mobs.append((mob_id, room, named_def))

    # ------------------------------------------------------------------
    # npc()
    # ------------------------------------------------------------------

    def npc(self, room, npc_id, **kwargs):
        """Place an NPC definition on a room."""
        npc_def = {
            "npc_id": npc_id,
            "wander": kwargs.get("wander", False),
            "quest": kwargs.get("quest"),
            "faction": kwargs.get("faction"),
            "standing_required": kwargs.get("standing_required"),
        }

        current = list(room.db.npc_definitions or [])
        current.append(npc_def)
        room.db.npc_definitions = current

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
            mob_obj.location = room

        mob_obj.db.zone_id = self._zone_id
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
            event: "on_enter" | "on_exit" | "on_first_visit" | "on_mob_death" | "on_examine"
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
            visible_in_exits: If True, appears in room exit list (D-21)
            aliases: List of alternative keywords
            desc: Description shown in exit list if visible_in_exits=True
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
        # Store definition on object for later CmdSet injection
        existing = list(target.db.custom_commands or [])
        existing.append(cmd_def)
        target.db.custom_commands = existing
        # Build and attach dynamic CmdSet
        from commands.cmd_dynamic import build_dynamic_cmdset
        target.cmdset.add(build_dynamic_cmdset(cmd_def), persistent=True)
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
        Does NOT implement quest logic — stores the definition.
        """
        if not self._zone_obj:
            raise AreaBuilderValidationError(
                f"zone '{self._zone_id}' — quest() called before zone()"
            )

        quest_def = {
            "quest_id": quest_id,
            "quest_type": kwargs.get("quest_type"),
            "can_share": kwargs.get("can_share", False),
            "share_radius": kwargs.get("share_radius", 1),
            "share_cap": kwargs.get("share_cap", 6),
            "quest_giver": kwargs.get("quest_giver"),
            "objective_type": kwargs.get("objective_type"),
            "objective_target": kwargs.get("objective_target"),
            "objective_count": kwargs.get("objective_count", 1),
            "flagged_drop": kwargs.get("flagged_drop"),
            "reward_tiers": kwargs.get("reward_tiers", {}),
            "world_expression": kwargs.get("world_expression", {}),
            "consequence_small": kwargs.get("consequence_small"),
            "consequence_medium": kwargs.get("consequence_medium"),
        }

        # Silently ignore level_range (legacy field)
        # kwargs.get("level_range") intentionally not stored

        current = list(self._zone_obj.db.quest_definitions or [])
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
        current.append(material_def)
        self._zone_obj.db.material_definitions = current

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
        3. Register named mobs in global registry
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

        # 4. Register named mobs
        for mob_id, room, definition in getattr(self, "_named_mobs", []):
            named_mob_registry.register_named_mob(
                mob_id, self._zone_id, room, definition
            )

        # 5. Register zone
        zone_registry.register_zone(self._zone_id, self._zone_obj)

        # 6. Initialize zone-level list attrs if not present
        if not self._zone_obj.db.quest_definitions:
            self._zone_obj.db.quest_definitions = []
        if not self._zone_obj.db.material_definitions:
            self._zone_obj.db.material_definitions = []

        return {
            "zone_id": self._zone_id,
            "rooms_created": len(self._rooms),
            "exits_created": self._exits_created,
            "warnings": list(self._build_warnings),
        }

    def _resolve_cross_zone_exits(self):
        """Resolve deferred cross-zone exits by tag lookup."""
        for exit_data in self._deferred_exits:
            target_str = exit_data.pop("to")
            target_zone_id, target_room_id = target_str.split(":", 1)

            # Find target room by room_id tag, then filter by zone_id
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
                continue

            from_room = exit_data.pop("from_room")
            direction = exit_data.pop("direction")
            self._create_exit_object(from_room, target, direction, **exit_data)

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
