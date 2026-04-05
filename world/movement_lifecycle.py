"""
Movement lifecycle orchestrator.

Coordinates all system calls when a character moves between rooms.
Typeclass delegates to on_move instead of containing game logic.
All imports are lazy (inside function bodies) per D-04.
"""

import time


def on_move(character, source_location, **kwargs):
    """
    Called from Character.at_after_move after super().

    Handles visited room tracking, OOB map push, auto-engage aggressive mobs,
    and Resonance Sense passive detection.
    """
    # Track visited room (for fog-of-war, Pitfall 5)
    if character.location:
        room_id = character.location.tags.get(category="room_id")
        if room_id:
            visited = set(character.db.visited_room_ids or set())
            if room_id not in visited:
                visited.add(room_id)
                character.db.visited_room_ids = visited

    # Skip map_update during Dragon Courier flight -- _arrive_final pushes it instead (Pitfall 6)
    if character.ndb.in_flight:
        return

    from world import oob_publisher
    oob_publisher.push_map_update(character)

    # Update room activity timestamp for still flag logic (review feedback:
    # room_state.py _room_qualifies_as_still reads room.ndb.last_activity)
    if character.location:
        character.location.ndb.last_activity = time.time()

    # Auto-engage: check for aggressive mobs in room (D-13, same-room only)
    # is_hunter BFS aggro deferred to Phase 6b (requires patrol tick integration)
    if character.location and not character.ndb.combat_handler:
        from world.combat_script import start_combat
        aggressive_mobs = []
        for obj in character.location.contents:
            if obj == character:
                continue
            if hasattr(obj, "get_behavior_toward"):
                behavior = obj.get_behavior_toward(character)
                if behavior == "aggressive" and (obj.db.combat_enabled is not False):
                    aggressive_mobs.append(obj)
        if aggressive_mobs:
            # First aggressive mob initiates; others join the same combat
            start_combat(character.location, aggressive_mobs[0], [character])
            for mob in aggressive_mobs[1:]:
                from world.combat_script import join_combat
                handler = character.ndb.combat_handler
                if handler and not handler.is_combatant(mob):
                    join_combat(handler, mob)

    # Resonance Sense passive (D-22)
    if character.db.guild_id and character.location:
        from world.guild_engine import GUILDS
        guild = GUILDS.get(character.db.guild_id, {})
        if guild.get("primary_domain") == "resonance":
            from world.room_state import get_dominant_flag, SENSE_DISPLAY
            flag = get_dominant_flag(character.location)
            if flag:
                text = SENSE_DISPLAY.get(flag, "")
                if text:
                    character.msg(f"|m[Sense] {text}|n")
