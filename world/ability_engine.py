"""
Ability execution engine.

Dispatches all abilities through effect-type handlers. Manages cooldowns
(ndb, per-encounter) and domain resources (ndb, volatile). Combat wiring
deferred to Phase 6.

Exports:
    use_ability, clear_encounter_cooldowns, decrement_cooldowns,
    build_domain_resource, spend_domain_resource, get_domain_resource,
    initialize_domain_resource
"""


# ---------------------------------------------------------------------------
# Effect handlers -- stubs returning descriptive text (Phase 6 wires real
# combat effects)
# ---------------------------------------------------------------------------

def _handle_damage(character, ability, target):
    return (
        f"You use {ability['name']} against "
        f"{target.key if target else 'the air'}. [Combat stub]"
    )


def _handle_dot(character, ability, target):
    return f"You apply {ability['name']}. [DoT stub]"


def _handle_buff(character, ability, target):
    return f"You activate {ability['name']}. [Buff stub]"


def _handle_debuff(character, ability, target):
    return (
        f"You cast {ability['name']} on "
        f"{target.key if target else 'nothing'}. [Debuff stub]"
    )


def _handle_utility(character, ability, target):
    return f"You use {ability['name']}. [Utility stub]"


def _handle_social(character, ability, target):
    return f"You invoke {ability['name']}. [Social stub]"


def _handle_tactical(character, ability, target):
    return f"You deploy {ability['name']}. [Tactical stub]"


def _handle_compound_trigger(character, ability, target):
    return f"You trigger {ability['name']}. [Compound stub]"


def _handle_heal(character, ability, target):
    return f"You channel {ability['name']}. [Heal stub]"


def _handle_status(character, ability, target):
    return f"You apply {ability['name']}. [Status stub]"


EFFECT_HANDLERS = {
    "damage": _handle_damage,
    "dot": _handle_dot,
    "buff": _handle_buff,
    "debuff": _handle_debuff,
    "utility": _handle_utility,
    "social": _handle_social,
    "tactical": _handle_tactical,
    "compound_trigger": _handle_compound_trigger,
    "heal": _handle_heal,
    "status": _handle_status,
}


# ---------------------------------------------------------------------------
# Resource management (D-13)
# ---------------------------------------------------------------------------

def get_domain_resource(character):
    """Return current domain resource dict or None if no guild."""
    return character.ndb.domain_resource


def build_domain_resource(character, amount):
    """Add resource (capped at max). Returns new current value."""
    res = character.ndb.domain_resource
    if not res:
        return 0
    res = dict(res)
    res["current"] = min(res["max"], res["current"] + amount)
    character.ndb.domain_resource = res
    return res["current"]


def spend_domain_resource(character, amount):
    """Spend resource. Returns (bool, str). Fails if insufficient."""
    res = character.ndb.domain_resource
    if not res:
        return False, "No domain resource available."
    if res["current"] < amount:
        return False, (
            f"Insufficient {res['type']} "
            f"({res['current']}/{amount} needed)."
        )
    res = dict(res)
    res["current"] = res["current"] - amount
    character.ndb.domain_resource = res
    return True, ""


def initialize_domain_resource(character):
    """
    Set up domain resource from guild fingerprint.
    Called at encounter start or session start for guild members.
    """
    guild_id = character.db.guild_id
    if not guild_id:
        character.ndb.domain_resource = None
        return
    from world.guild_engine import GUILDS, FINGERPRINTS
    guild = GUILDS.get(guild_id, {})
    domain = guild.get("primary_domain")
    fp = FINGERPRINTS.get(domain, {})
    resource_type = fp.get("resource", domain)
    resource_max = fp.get("resource_max", 100)
    character.ndb.domain_resource = {
        "type": resource_type,
        "current": 0,
        "max": resource_max,
    }


# ---------------------------------------------------------------------------
# Cooldown management (D-12)
# ---------------------------------------------------------------------------

def decrement_cooldowns(character):
    """Decrement all ability cooldowns by 1 round. Called each combat round."""
    cooldowns = dict(character.ndb.ability_cooldowns or {})
    expired = []
    for ability_id, remaining in cooldowns.items():
        cooldowns[ability_id] = remaining - 1
        if cooldowns[ability_id] <= 0:
            expired.append(ability_id)
    for ability_id in expired:
        del cooldowns[ability_id]
    character.ndb.ability_cooldowns = cooldowns


def clear_encounter_cooldowns(character):
    """Clear all cooldowns and reset ancestry ability. Called at encounter end."""
    character.ndb.ability_cooldowns = {}
    character.ndb.ancestry_ability_used = False


# ---------------------------------------------------------------------------
# Access check
# ---------------------------------------------------------------------------

def _check_ability_access(character, ability_id):
    """Check if character knows and can use this ability. Returns (bool, str)."""
    from world.ability_registry import ABILITIES
    ability = ABILITIES.get(ability_id)
    if not ability:
        return False, "Unknown ability."

    # Check CharacterAbility model for unlock (ABL-03)
    from world.models import CharacterAbility
    if not CharacterAbility.objects.filter(
        character=character, ability_id=ability_id
    ).exists():
        return False, f"You have not unlocked {ability['name']}."

    return True, ""


# ---------------------------------------------------------------------------
# Resource check helper
# ---------------------------------------------------------------------------

def _check_and_spend_resource(character, ability):
    """Check and deduct resource cost. Returns (bool, str)."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


# ---------------------------------------------------------------------------
# Main dispatch (D-10)
# ---------------------------------------------------------------------------

def use_ability(character, ability_id, target=None):
    """
    Execute an ability. Returns (bool, str).

    Checks: known, cooldown, resource, then dispatches to effect handler.
    Per D-10: effect-type dispatch, no per-ability callables.
    """
    from world.ability_registry import ABILITIES
    ability = ABILITIES.get(ability_id)
    if not ability:
        return False, "Unknown ability."

    # Check character has unlocked this ability
    ok, msg = _check_ability_access(character, ability_id)
    if not ok:
        return False, msg

    # Check cooldown (D-12)
    cooldowns = character.ndb.ability_cooldowns or {}
    remaining = cooldowns.get(ability_id, 0)
    if remaining > 0:
        return False, (
            f"{ability['name']} is on cooldown "
            f"({remaining} rounds remaining)."
        )

    # Check and spend resource (D-13)
    ok, msg = _check_and_spend_resource(character, ability)
    if not ok:
        return False, msg

    # Dispatch to effect handler (D-10)
    handler = EFFECT_HANDLERS.get(ability["effect_type"])
    if not handler:
        return False, f"Unhandled effect type: {ability['effect_type']}"

    result = handler(character, ability, target)

    # Set cooldown (D-12)
    if ability.get("cooldown", 0) > 0:
        cooldowns = dict(character.ndb.ability_cooldowns or {})
        cooldowns[ability_id] = ability["cooldown"]
        character.ndb.ability_cooldowns = cooldowns

    # Write room flag if specified (D-24)
    if ability.get("room_flag_written") and character.location:
        from world.room_state import add_room_flag
        add_room_flag(character.location, ability["room_flag_written"])

    # Increment times_used
    try:
        from django.db.models import F
        from world.models import CharacterAbility as CA
        CA.objects.filter(
            character=character, ability_id=ability_id
        ).update(times_used=F("times_used") + 1)
    except Exception:
        pass  # Non-fatal -- counter is informational

    return True, result
