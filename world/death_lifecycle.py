"""
Death lifecycle orchestrator.

Coordinates all system calls when a mob dies.
Typeclass delegates to on_mob_death instead of containing game logic.
All imports are lazy (inside function bodies) per D-04.
"""


def on_mob_death(mob, killer=None):
    """
    Called from SoravelonMob.at_death.

    Handles ndb cleanup, trigger firing, loot drops, tome drops,
    room state flags, and respawn scheduling.
    """
    # Clear volatile combat state
    mob.ndb.revealed_affixes = set()
    if hasattr(mob.ndb, 'combat_scales'):
        mob.ndb.combat_scales = {}

    # Fire on_mob_death triggers (existing)
    if mob.db.triggers:
        from world.trigger_engine import fire_triggers
        context = {"mob": mob, "room": mob.location}
        if killer and hasattr(killer, 'account') and killer.account:
            fire_triggers(mob, "on_mob_death", killer, context=context)

    # Drop loot (D-35: roll_loot called from at_death)
    room = mob.location
    if room and killer:
        from world.loot_tables import roll_loot
        from world.item_spawner import create_item_from_template
        drops = roll_loot(mob, killer)
        for item_def in drops:
            create_item_from_template(item_def, location=room)

    # Drop tome if named mob (D-18: tome pre-assigned)
    if mob.db.tome_drop and room:
        from world.item_spawner import create_item_from_template
        tome_def = {
            "item_id": mob.db.tome_drop,
            "key": mob.db.tome_drop.replace("_", " "),
            "item_type": "item",
            "desc": f"A tome recovered from {mob.key}.",
            "rarity": "rare",
            "weight": 0.5,
            "value": 50,
        }
        create_item_from_template(tome_def, location=room)

    # Write room state flags (D-24)
    if room:
        from world.room_state import add_room_flag
        add_room_flag(room, "blood_soaked")

        # Nature-affinity mob death
        if mob.db.faction and mob.db.faction.lower() in (
            "verdance", "wardens", "nature"
        ):
            add_room_flag(room, "fading_life")

        # Named/boss mob death
        from world.mob_spawner import MOB_INSTANCE_TAG_CATEGORY
        is_named = mob.tags.get(category=MOB_INSTANCE_TAG_CATEGORY) is not None
        is_boss = mob.db.rarity == "legendary"
        if is_named or is_boss:
            add_room_flag(room, "power_vacuum")

    # Named mob death: write WorldEventLog entry (D-05)
    from world.mob_spawner import MOB_INSTANCE_TAG_CATEGORY
    is_named = mob.tags.get(category=MOB_INSTANCE_TAG_CATEGORY) is not None
    if is_named and killer:
        from world.models import WorldEventLog
        WorldEventLog.objects.create(
            event_type="named_mob_death",
            zone_id=mob.db.zone_id or "",
            character_id=killer.id if killer else None,
            description=f"{mob.key} was slain by {killer.key}",
            data={"named_id": mob.db.named_id or mob.key, "mob_key": mob.key},
        )

    # Quest progress: kill objectives (D-07, D-19)
    if killer and hasattr(killer, 'account') and killer.account:
        from world.quest_engine import check_kill_objectives
        check_kill_objectives(killer, mob)

    # Schedule respawn via SpawnRecord (replaces callLater)
    from world.mob_spawner import schedule_respawn_from_death
    schedule_respawn_from_death(mob)
