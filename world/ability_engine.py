"""
Ability execution engine.

Dispatches all abilities through effect-type handlers. Manages cooldowns
(ndb, per-encounter) and domain resources (ndb, volatile).

Effect handlers delegate to combat_engine.py for damage/heal resolution
and status_effects.py for buff/debuff/DoT application.

Exports:
    use_ability, clear_encounter_cooldowns, decrement_cooldowns,
    build_domain_resource, spend_domain_resource, get_domain_resource,
    initialize_domain_resource, EFFECT_HANDLERS
"""

import random


# ---------------------------------------------------------------------------
# Effect handlers -- wired to real combat resolution via combat_engine and
# status_effects (lazy imports to avoid circular dependencies)
# ---------------------------------------------------------------------------

def _handle_damage(character, ability, target):
    """Resolve direct damage via combat_engine."""
    from world.combat_engine import resolve_ability_damage
    ok, msg, dmg = resolve_ability_damage(character, ability, target)
    return msg


def _handle_dot(character, ability, target):
    """Apply a damage-over-time status effect to the target."""
    from world import status_effects
    effect_type = ability.get("status_effect", "poison")
    duration = ability.get("effect_duration", 3)
    magnitude = ability.get("effect_magnitude", ability.get("damage_base", 8))
    ok, msg = status_effects.apply_effect(
        target, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    return f"{character.key} applies {ability_name}. {msg}"


def _handle_buff(character, ability, target):
    """Apply a buff to the caster (self-buff)."""
    from world import status_effects
    effect_type = ability.get("buff_type", "haste")
    duration = ability.get("effect_duration", 3)
    magnitude = ability.get("effect_magnitude", 1.0)
    ok, msg = status_effects.apply_effect(
        character, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    return f"{character.key} activates {ability_name}. {msg}"


def _handle_debuff(character, ability, target):
    """Apply a debuff to the target."""
    from world import status_effects
    effect_type = ability.get("debuff_type", "weaken")
    duration = ability.get("effect_duration", 3)
    magnitude = ability.get("effect_magnitude", 1.0)
    ok, msg = status_effects.apply_effect(
        target, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    target_name = target.key if target else "the air"
    return f"{character.key} casts {ability_name} on {target_name}. {msg}"


def _handle_utility(character, ability, target):
    """Context-dependent utility effect."""
    utility_action = ability.get("utility_action")
    if utility_action == "flee_boost":
        from world import status_effects
        status_effects.apply_effect(
            character, "haste", 2, 1.0, character.id
        )
        return f"{character.key} uses {ability['name']} to gain a burst of speed."
    elif utility_action == "reveal":
        # Reveal a mob's affix (if target is a mob)
        if target and hasattr(target, "reveal_affix"):
            affixes = target.db.affix_list or []
            for affix_tag in affixes:
                reveal_msg = target.reveal_affix(character, affix_tag)
                if reveal_msg:
                    return f"{character.key} uses {ability['name']}. {reveal_msg}"
        return f"{character.key} uses {ability['name']} to scan the area."
    return f"{character.key} uses {ability['name']}."


def _handle_social(character, ability, target):
    """Apply charm or social influence to the target."""
    from world import status_effects
    if target and target.db.base_stats is None:
        # Mob target: apply charm effect
        ok, msg = status_effects.apply_effect(
            target, "charm",
            ability.get("effect_duration", 2),
            ability.get("effect_magnitude", 1.0),
            character.id,
        )
    else:
        msg = "Social influence applied."
    from world.base_attributes import record_stat_use
    record_stat_use(character, "social_ability")
    return f"{character.key} invokes {ability['name']}. {msg}"


def _handle_tactical(character, ability, target):
    """Apply tactical buff to group members or self."""
    from world import status_effects
    from world.base_attributes import record_stat_use
    tactical_action = ability.get("tactical_action", "self_buff")
    buff_type = ability.get("buff_type", "haste")
    duration = ability.get("effect_duration", 3)
    magnitude = ability.get("effect_magnitude", 1.0)

    if tactical_action == "group_buff":
        # Try to buff all group members
        leader_id = getattr(character.ndb, "group_leader_id", None)
        if leader_id:
            from world.group_engine import _get_leader, _get_group_members
            leader = _get_leader(character)
            if leader:
                members = _get_group_members(leader)
                for member in members:
                    status_effects.apply_effect(
                        member, buff_type, duration, magnitude, character.id
                    )
                record_stat_use(character, "social_ability")
                return (
                    f"{character.key} rallies the group with {ability['name']}! "
                    f"{len(members)} allies buffed."
                )
    # Fallback: self-buff
    status_effects.apply_effect(
        character, buff_type, duration, magnitude, character.id
    )
    record_stat_use(character, "social_ability")
    return f"{character.key} deploys {ability['name']}."



def _handle_heal(character, ability, target):
    """Resolve healing via combat_engine."""
    from world.combat_engine import resolve_heal
    heal_target = target or character
    ok, msg, healed = resolve_heal(character, ability, heal_target)
    return msg


def _handle_status(character, ability, target):
    """Apply a status effect with application chance roll."""
    from world import status_effects
    effect_type = ability.get("status_effect", "slow")
    chance = ability.get("application_chance", 1.0)
    duration = ability.get("effect_duration", 3)
    magnitude = ability.get("effect_magnitude", 1.0)

    if random.random() > chance:
        return (
            f"{character.key} uses {ability['name']} on "
            f"{target.key if target else 'the air'}, "
            f"but the effect is resisted!"
        )

    ok, msg = status_effects.apply_effect(
        target, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    return f"{character.key} uses {ability_name}. {msg}"


EFFECT_HANDLERS = {
    "damage": _handle_damage,
    "dot": _handle_dot,
    "buff": _handle_buff,
    "debuff": _handle_debuff,
    "utility": _handle_utility,
    "social": _handle_social,
    "tactical": _handle_tactical,
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

    # Mobs use db.abilities list — skip CharacterAbility unlock check
    if character.db.abilities:
        return True, ""

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
