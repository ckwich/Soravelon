"""
Session lifecycle orchestrator.

Coordinates all system calls for player login and logout.
Typeclasses delegate to on_login / on_logout instead of containing game logic.
All imports are lazy (inside function bodies) per D-04.
"""

import uuid


def _get_active_combat_handler(character):
    """Return the current combat handler only if it still owns the character."""
    handler = getattr(character.ndb, "combat_handler", None)
    if not handler:
        return None
    try:
        if not handler.is_combatant(character):
            return None
    except (AttributeError, RuntimeError):
        return None
    return handler


def get_new_player_guidance(character):
    """
    Return a contextual login breadcrumb for players who still need one.

    Guidance is intentionally light-touch and only shown when it provides a
    concrete next step rather than repeating information the player is likely
    to have already internalized.
    """
    ancestry = getattr(character.db, "ancestry", None)
    if not ancestry:
        return (
            "|y[Before you head out, choose an ancestry with "
            "|wancestry <human|kau'roran|veth>|n or "
            "|wancestry selvar <summer||winter>|n. "
            "Use |whelp ancestry|n for the full breakdown.]|n"
        )

    guild_id = getattr(character.db, "guild_id", None)
    if not guild_id:
        try:
            from world.guild_engine import GUILDS, check_guild_eligibility
            from world.remnance_visibility import guild_is_player_visible

            eligible = check_guild_eligibility(character) or []
            visible = []
            for candidate in eligible:
                guild = GUILDS.get(candidate, {})
                if not guild_is_player_visible(candidate, guild, character):
                    continue
                visible.append(guild.get("name", candidate))
        except Exception:
            visible = []

        if visible:
            return (
                "|y[A guild invitation is waiting for you. Type |wjoinguild|n "
                "to review your offers, then choose your path with "
                "|wjoinguild <guild> <secondary_domain>|n.]|n"
            )

        return (
            "|y[You have not joined a guild yet. Explore guild halls in the "
            "hub city, keep practicing the domains that fit your style, and "
            "watch for a messenger telling you to type |wjoinguild|n.]|n"
        )

    pending_offer = getattr(character.ndb, "pending_quest_offer", None)
    if pending_offer:
        quest = pending_offer.get("quest") or {}
        quest_name = quest.get("name") or quest.get("quest_id")
        if quest_name:
            return (
                f"|y[{quest_name} is waiting on your answer. Type |waccept|n "
                f"to take it or |wdecline|n to turn it down.]|n"
            )
        return (
            "|y[Someone is waiting on your answer. Type |waccept|n to take "
            "the offered quest or |wdecline|n to turn it down.]|n"
        )

    backend_level = int(getattr(character.db, "backend_level", 1) or 1)
    if backend_level > 5:
        return None

    try:
        from world.quest_engine import get_active_quests

        active_quests = get_active_quests(character) or []
    except Exception:
        active_quests = []

    if active_quests:
        return None

    return (
        "|y[You do not have an active lead. Talk to nearby NPCs with "
        "|wtalk <name>|n, dig for work with |wask <name> about rumors|n "
        "or |wask <name> about work|n, and use |wquest|n to review your "
        "journal.]|n"
    )


def send_new_player_guidance(character):
    """Send contextual onboarding guidance if this login still warrants it."""
    guidance = get_new_player_guidance(character)
    if not guidance:
        return False
    character.msg(guidance)
    return True


def on_login(character):
    """
    Called from Character.at_post_puppet after super().

    Restores or initializes volatile session state and pushes initial OOB updates.
    """
    from world.world_state import init_session_accumulators
    from world.base_attributes import (
        STAT_NAMES, derive_max_hp, derive_max_stamina,
    )

    init_session_accumulators(character)
    character.ndb.presence_nonce = str(uuid.uuid4())

    # Stat growth session accumulators (volatile)
    character.ndb.stat_xp_accumulators = {stat: 0.0 for stat in STAT_NAMES}

    active_combat = _get_active_combat_handler(character)

    # Restore existing runtime state on reconnect so logout/login cannot wipe
    # pressure, cooldowns, or combat state mid-session.
    character.ndb.combat_handler = active_combat
    character.ndb.combat_target_id = getattr(
        character.ndb, "combat_target_id", None
    )
    character.ndb.active_effects = list(
        getattr(character.ndb, "active_effects", None) or []
    )
    actions_remaining = getattr(character.ndb, "actions_remaining", None)
    character.ndb.actions_remaining = (
        actions_remaining if actions_remaining is not None else 0
    )
    ability_used = getattr(character.ndb, "ability_used_this_turn", None)
    character.ndb.ability_used_this_turn = (
        bool(ability_used) if ability_used is not None else False
    )
    current_hp = getattr(character.ndb, "hp", None)
    character.ndb.hp = (
        current_hp if current_hp is not None else derive_max_hp(character)
    )
    current_stamina = getattr(character.ndb, "stamina", None)
    character.ndb.stamina = (
        current_stamina
        if current_stamina is not None
        else derive_max_stamina(character)
    )
    character.ndb.charged_ability = getattr(character.ndb, "charged_ability", None)

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
    character.ndb.ability_cooldowns = dict(
        getattr(character.ndb, "ability_cooldowns", None) or {}
    )
    ancestry_used = getattr(character.ndb, "ancestry_ability_used", None)
    character.ndb.ancestry_ability_used = (
        bool(ancestry_used) if ancestry_used is not None else False
    )
    if not character.db.guild_id:
        character.ndb.domain_resource = None
    # Initialize domain resource at login for guild members (review feedback:
    # utility/social abilities used outside combat need resources available)
    elif getattr(character.ndb, "domain_resource", None) is None:
        from world.ability_engine import initialize_domain_resource
        initialize_domain_resource(character)

    from world.ability_engine import sync_character_ability_unlocks
    sync_character_ability_unlocks(character)

    if active_combat:
        from world.combat_script import (
            _add_combat_cmdset, _build_combat_oob, _send_turn_prompt,
        )
        from world.oob_publisher import push_combat_update

        _add_combat_cmdset(character)
        if active_combat.get_current_combatant() == character:
            _send_turn_prompt(character, active_combat)
        push_combat_update(character, _build_combat_oob(character, active_combat))
    else:
        guidance_method = getattr(character, "_send_new_player_guidance", None)
        if callable(guidance_method):
            guidance_method()
        else:
            send_new_player_guidance(character)


def on_logout(character):
    """
    Called from Character.at_pre_unpuppet before super().

    Flushes accumulators, disconnects from group, cleans up combat state.
    """
    from world.base_attributes import commit_stat_growth
    from world.world_state import commit_session_xp
    from world.skill_engine import commit_skill_accumulators
    from world.group_engine import on_member_disconnect

    # Flush ALL accumulators before logout — stat growth, domain XP, skill uses
    commit_stat_growth(character)
    commit_session_xp(character)
    commit_skill_accumulators(character)
    on_member_disconnect(character)

    # Stop HP/stamina recovery ticks before disconnect
    from world.recovery_engine import stop_regen
    stop_regen(character)
    character.ndb.presence_nonce = None

    # Preserve active combat state on disconnect so reconnecting cannot be used
    # to clear pressure or dodge the encounter.
    active_combat = _get_active_combat_handler(character)
    if active_combat:
        stored = dict(active_combat.db.active_effects_db or {})
        effects = list(getattr(character.ndb, "active_effects", None) or [])
        if effects:
            stored[str(character.id)] = effects
        elif str(character.id) in stored:
            del stored[str(character.id)]
        active_combat.db.active_effects_db = stored
    else:
        character.ndb.combat_handler = None
