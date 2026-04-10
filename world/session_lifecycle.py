"""
Session lifecycle orchestrator.

Coordinates all system calls for player login and logout.
Typeclasses delegate to on_login / on_logout instead of containing game logic.
All imports are lazy (inside function bodies) per D-04.
"""


def on_login(character):
    """
    Called from Character.at_post_puppet after super().

    Initializes all volatile session state and pushes initial OOB updates.
    """
    from world.world_state import init_session_accumulators
    from world.base_attributes import (
        STAT_NAMES, derive_max_hp, derive_max_stamina,
    )

    init_session_accumulators(character)

    # Stat growth session accumulators (volatile)
    character.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}

    # Combat-relevant ndb state
    character.ndb.combat_handler = None
    character.ndb.combat_target_id = None
    character.ndb.active_effects = []
    character.ndb.actions_remaining = 0
    character.ndb.ability_used_this_turn = False
    character.ndb.hp = derive_max_hp(character)
    character.ndb.stamina = derive_max_stamina(character)
    character.ndb.charged_ability = None

    # Start per-character session script (XP flush + debt countdown).
    # persistent=False on the script means it auto-removes on logout,
    # so we always create fresh on login. Check for existing first
    # to handle reconnect-without-disconnect edge case.
    from evennia import create_script
    from typeclasses.scripts import SessionCommitScript
    if not character.scripts.get("session_commit_script"):
        create_script(SessionCommitScript, obj=character)

    # Initialize OOB debounce dict on (re)connect (Pitfall 1: ndb is None until set)
    character.ndb.oob_debounce = {}
    # Push full initial state to newly connected client (per D-05)
    from world import oob_publisher
    oob_publisher.push_status_update(character)
    oob_publisher.push_stat_update(character)
    oob_publisher.push_map_update(character)
    oob_publisher.push_inventory_update(character)

    # Start passive HP/stamina recovery tick
    from world.recovery_engine import start_regen
    start_regen(character)

    # Ability system volatile state (D-12, D-13)
    character.ndb.ability_cooldowns = {}
    character.ndb.ancestry_ability_used = False
    character.ndb.domain_resource = None  # Default; overwritten below if guild member
    # Initialize domain resource at login for guild members (review feedback:
    # utility/social abilities used outside combat need resources available)
    if character.db.guild_id:
        from world.ability_engine import initialize_domain_resource
        initialize_domain_resource(character)


def on_logout(character):
    """
    Called from Character.at_pre_unpuppet before super().

    Flushes accumulators, disconnects from group, cleans up combat state.
    """
    from world.base_attributes import commit_stat_growth
    from world.world_state import commit_session_xp
    from world.group_engine import on_member_disconnect

    # Flush stat growth accumulators before logout (called exactly once)
    commit_stat_growth(character)

    commit_session_xp(character)
    on_member_disconnect(character)

    # Stop HP/stamina recovery ticks before disconnect
    from world.recovery_engine import stop_regen
    stop_regen(character)

    # Combat cleanup -- remove from active combat on disconnect
    if getattr(character.ndb, "combat_handler", None):
        try:
            character.ndb.combat_handler.remove_combatant(character)
        except (AttributeError, RuntimeError):
            pass  # combat handler may already be cleaned up
        character.ndb.combat_handler = None
