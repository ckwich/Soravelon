"""
HP/stamina recovery engine for Soravelon.

Three-tier recovery: passive (1%/10s out of combat), rest (3%/10s),
sleep (6%/10s, blind), sleep+bed (10%/10s).

Recovery state stored on character.ndb.recovery_state (volatile).
Regen tick handle on character.ndb.regen_handle (auto-cleared on disconnect).

Medic blessings: Heal, Fortify, Vigor, Purify -- applied by medic NPCs
for Scales with 60-120 second cooldowns.

All public functions return (bool, str) tuples per project convention.
"""

import time

REGEN_RATES = {
    "active": 0.01,        # 1% per 10s (out of combat only)
    "resting": 0.03,       # 3% per 10s
    "sleeping": 0.06,      # 6% per 10s
    "sleeping_bed": 0.10,  # 10% per 10s
}

BLESSINGS = {
    "heal": {
        "name": "Heal",
        "desc": "Restores HP to full.",
        "cost": 20,
        "cooldown": 120,  # 2 minutes
        "effect": "heal_full",
    },
    "fortify": {
        "name": "Fortify",
        "desc": "Temporary defense buff.",
        "cost": 30,
        "cooldown": 120,
        "effect": "fortify_buff",
        "duration": 300,  # 5 minutes (in seconds), converted to rounds in combat
    },
    "vigor": {
        "name": "Vigor",
        "desc": "Temporary offense buff.",
        "cost": 30,
        "cooldown": 120,
        "effect": "vigor_buff",
        "duration": 300,
    },
    "purify": {
        "name": "Purify",
        "desc": "Cleanses all negative status effects.",
        "cost": 40,
        "cooldown": 60,  # 1 minute
        "effect": "purify_cleanse",
    },
}

REGEN_INTERVAL = 10  # seconds between ticks


def _room_has_bed(room):
    """Check if room has an item or flag indicating a bed."""
    if not room:
        return False
    # Check items in room for is_bed attribute
    for obj in room.contents:
        if getattr(obj.db, "is_bed", False):
            return True
    return False


# Lazy import wrappers for testability
def push_stat_update(character):
    """Wrapper around oob_publisher.push_stat_update for mockability."""
    from world.oob_publisher import push_stat_update as _push
    _push(character)


def _regen_tick(character):
    """Periodic regen tick. Called every REGEN_INTERVAL seconds."""
    from world.base_attributes import derive_max_hp, derive_max_stamina

    # Skip if in combat
    if getattr(character.ndb, "combat_handler", None):
        # Re-schedule to check again later (combat may end)
        _schedule_next_tick(character)
        return

    state = getattr(character.ndb, "recovery_state", "active")

    # Check bed bonus for sleeping
    if state == "sleeping":
        has_bed = _room_has_bed(character.location)
        rate = REGEN_RATES["sleeping_bed"] if has_bed else REGEN_RATES["sleeping"]
    else:
        rate = REGEN_RATES.get(state, REGEN_RATES["active"])

    max_hp = derive_max_hp(character)
    max_stamina = derive_max_stamina(character)
    hp_gain = max(1, int(max_hp * rate))
    stamina_gain = max(1, int(max_stamina * rate))

    changed = False
    current_hp = character.ndb.hp or 0
    current_stamina = character.ndb.stamina or 0

    if current_hp < max_hp:
        character.ndb.hp = min(max_hp, current_hp + hp_gain)
        changed = True
    if current_stamina < max_stamina:
        character.ndb.stamina = min(max_stamina, current_stamina + stamina_gain)
        changed = True

    if changed:
        push_stat_update(character)

    # Schedule next tick if not at full
    if (character.ndb.hp or 0) < max_hp or (character.ndb.stamina or 0) < max_stamina:
        _schedule_next_tick(character)


def _schedule_next_tick(character):
    """Schedule next regen tick, canceling any existing handle."""
    from evennia.utils import delay
    old_handle = getattr(character.ndb, "regen_handle", None)
    if old_handle:
        try:
            old_handle.cancel()
        except Exception:
            pass
    character.ndb.regen_handle = delay(REGEN_INTERVAL, _regen_tick, character)


def start_regen(character):
    """Start regen tick loop. Called at login and after combat ends. Returns (bool, str)."""
    if not getattr(character.ndb, "recovery_state", None):
        character.ndb.recovery_state = "active"
    _schedule_next_tick(character)
    return True, "Recovery started."


def stop_regen(character):
    """Stop regen tick loop. Called on disconnect. Returns (bool, str)."""
    handle = getattr(character.ndb, "regen_handle", None)
    if handle:
        try:
            handle.cancel()
        except Exception:
            pass
        character.ndb.regen_handle = None
    return True, "Recovery stopped."


def set_recovery_state(character, state):
    """Set recovery state. Returns (bool, str)."""
    if state not in ("active", "resting", "sleeping"):
        return False, f"Invalid recovery state: {state}"

    if getattr(character.ndb, "combat_handler", None):
        return False, "You can't rest during combat!"

    character.ndb.recovery_state = state

    if state == "sleeping":
        character.ndb.is_sleeping = True
    else:
        character.ndb.is_sleeping = False

    # Ensure regen tick is running
    _schedule_next_tick(character)

    if state == "resting":
        return True, "You sit down and rest."
    elif state == "sleeping":
        return True, "You lie down and close your eyes. The world fades away."
    else:
        return True, "You stand up."


def cancel_recovery(character):
    """Cancel rest/sleep state, return to active. Returns (bool, str)."""
    was_sleeping = getattr(character.ndb, "is_sleeping", False)
    character.ndb.recovery_state = "active"
    character.ndb.is_sleeping = False
    if was_sleeping:
        return True, "You wake up and look around."
    return True, "You stop resting."


def apply_blessing(character, medic_npc, blessing_id):
    """Apply a medic blessing. Costs Scales. Returns (bool, str)."""
    blessing = BLESSINGS.get(blessing_id)
    if not blessing:
        return False, f"Unknown blessing: {blessing_id}"

    # Check cooldown
    cooldowns = character.db.blessing_cooldowns or {}
    last_used = cooldowns.get(blessing_id, 0)
    now = time.time()
    remaining = blessing["cooldown"] - (now - last_used)
    if remaining > 0:
        return False, f"{blessing['name']} is on cooldown ({int(remaining)}s remaining)."

    # Check cost
    cost = blessing["cost"]
    carried = character.db.carried_scales or 0
    if carried < cost:
        return False, f"The blessing costs {cost} Scales, but you only have {carried}."

    # Deduct Scales
    character.db.carried_scales = carried - cost

    # Record cooldown
    cooldowns = dict(character.db.blessing_cooldowns or {})
    cooldowns[blessing_id] = now
    character.db.blessing_cooldowns = cooldowns

    # Apply effect
    effect = blessing["effect"]
    if effect == "heal_full":
        from world.base_attributes import derive_max_hp
        character.ndb.hp = derive_max_hp(character)
        push_stat_update(character)
        return True, f"The medic's healing light washes over you. HP fully restored. ({cost} Scales)"
    elif effect == "fortify_buff":
        from world import status_effects
        combat_rounds = blessing.get("duration", 300) // 10
        status_effects.apply_effect(character, "fortify", combat_rounds, 1.0, medic_npc.id)
        return True, f"The medic blesses you with Fortify. Defense increased. ({cost} Scales)"
    elif effect == "vigor_buff":
        from world import status_effects
        combat_rounds = blessing.get("duration", 300) // 10
        status_effects.apply_effect(character, "vigor", combat_rounds, 1.0, medic_npc.id)
        return True, f"The medic blesses you with Vigor. Offense increased. ({cost} Scales)"
    elif effect == "purify_cleanse":
        from world import status_effects
        status_effects.clear_all_effects(character)
        return True, f"The medic purifies you. All negative effects cleansed. ({cost} Scales)"

    return False, "Blessing effect not implemented."
