"""
Ability execution engine.

Dispatches all abilities through effect-type handlers. Manages cooldowns
(ndb, per-encounter) and domain resources (ndb, volatile).

Effect handlers delegate to combat_engine.py for damage/heal resolution
and status_effects.py for buff/debuff/DoT application.

Resource handlers provide type-aware build/spend/decay for all 10 domain
resource systems (Focus, Balance, Resonance, Influence, Momentum, Mana,
Reagents, Command, Components, Echoes).

Exports:
    use_ability, clear_encounter_cooldowns, decrement_cooldowns,
    build_domain_resource, spend_domain_resource, get_domain_resource,
    initialize_domain_resource, EFFECT_HANDLERS, RESOURCE_HANDLERS,
    decay_resonance, on_round_end_resources, on_encounter_end_resources,
    handle_focus_miss, get_balance_modifier, build_momentum_on_damage
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
    params = ability.get("effect_params", {})
    effect_type = params.get("status_effect") or ability.get("status_effect", "poison")
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", ability.get("damage_base", 8))
    ok, msg = status_effects.apply_effect(
        target, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    return f"{character.key} applies {ability_name}. {msg}"


def _handle_buff(character, ability, target):
    """Apply a buff to the caster (self-buff)."""
    from world import status_effects
    params = ability.get("effect_params", {})
    effect_type = params.get("buff_type") or ability.get("buff_type", "haste")
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
    ok, msg = status_effects.apply_effect(
        character, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    return f"{character.key} activates {ability_name}. {msg}"


def _handle_debuff(character, ability, target):
    """Apply a debuff to the target."""
    from world import status_effects
    params = ability.get("effect_params", {})
    effect_type = params.get("debuff_type") or ability.get("debuff_type", "weaken")
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
    ok, msg = status_effects.apply_effect(
        target, effect_type, duration, magnitude, character.id
    )
    ability_name = ability["name"]
    target_name = target.key if target else "the air"
    return f"{character.key} casts {ability_name} on {target_name}. {msg}"


def _handle_utility(character, ability, target):
    """Context-dependent utility effect."""
    params = ability.get("effect_params", {})
    utility_action = params.get("utility_action") or ability.get("utility_action")
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
    params = ability.get("effect_params", {})
    if target and target.db.base_stats is None:
        # Mob target: apply charm effect
        duration = params.get("duration") or ability.get("effect_duration", 2)
        magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)
        ok, msg = status_effects.apply_effect(
            target, "charm",
            duration,
            magnitude,
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
    params = ability.get("effect_params", {})
    tactical_action = params.get("tactical_action") or ability.get("tactical_action", "self_buff")
    buff_type = params.get("buff_type") or ability.get("buff_type", "haste")
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)

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
    params = ability.get("effect_params", {})
    effect_type = params.get("status_effect") or ability.get("status_effect", "slow")
    chance = ability.get("application_chance", 1.0)
    duration = params.get("duration") or ability.get("effect_duration", 3)
    magnitude = params.get("magnitude") or ability.get("effect_magnitude", 1.0)

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
# Resource handlers -- type-aware spend/build per domain (D-03 through D-13)
# ---------------------------------------------------------------------------

def _handle_momentum_spend(character, ability):
    """Momentum: traditional pool spend. Build happens elsewhere."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_focus_spend(character, ability):
    """Focus combo points: builders free, spenders cost 1-5, consumes_all needs >= 1."""
    params = ability.get("effect_params", {})
    if params.get("is_builder"):
        return True, ""  # Builders cost nothing; Focus added after hit
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    if params.get("consumes_all_focus"):
        res = character.ndb.domain_resource
        if not res or res["current"] < 1:
            return False, "No Focus points to spend."
        return True, ""  # Consumed in post-ability hook
    res = character.ndb.domain_resource
    if not res or res["current"] < cost:
        current = res["current"] if res else 0
        return False, f"Insufficient Focus ({current}/{cost} needed)."
    res = dict(res)
    res["current"] -= cost
    character.ndb.domain_resource = res
    return True, ""


def _handle_balance_spend(character, ability):
    """Balance pendulum: shift position, never spend. resource_cost always 0."""
    params = ability.get("effect_params", {})
    shift = params.get("balance_shift", 0)
    if shift == 0:
        return True, ""
    res = character.ndb.domain_resource
    if not res:
        return True, ""
    res = dict(res)
    res["current"] = max(0, min(100, res["current"] + shift))
    character.ndb.domain_resource = res
    return True, ""


def _handle_resonance_spend(character, ability):
    """Resonance: builders free (generate after), spenders cost from pool."""
    params = ability.get("effect_params", {})
    if params.get("resonance_generated"):
        return True, ""  # Builder; resonance added in post-ability hook
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_mana_spend(character, ability):
    """Mana: traditional pool spend. Persists across encounters."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_influence_spend(character, ability):
    """Influence: encounter-scoped pool, no regen. Standard spend."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_reagents_spend(character, ability):
    """Reagents: finite stock, standard spend. Reads reagent_type variant."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    reagent_type = ability.get("effect_params", {}).get("reagent_type", "generic")
    return spend_domain_resource(character, cost)


def _handle_command_spend(character, ability):
    """Command: pool spend. Builds from ally actions."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


def _handle_components_spend(character, ability):
    """Components: finite stock like reagents. Reads component_type variant."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    component_type = ability.get("effect_params", {}).get("component_type", "generic")
    return spend_domain_resource(character, cost)


def _handle_echoes_spend(character, ability):
    """Echoes: pool spend. Builds from abilities and investigation bonus."""
    cost = ability.get("resource_cost", 0)
    if cost <= 0:
        return True, ""
    return spend_domain_resource(character, cost)


RESOURCE_HANDLERS = {
    "momentum": _handle_momentum_spend,
    "focus": _handle_focus_spend,
    "balance": _handle_balance_spend,
    "resonance": _handle_resonance_spend,
    "mana": _handle_mana_spend,
    "influence": _handle_influence_spend,
    "reagents": _handle_reagents_spend,
    "command": _handle_command_spend,
    "components": _handle_components_spend,
    "echoes": _handle_echoes_spend,
}


# ---------------------------------------------------------------------------
# Post-ability resource hooks
# ---------------------------------------------------------------------------

def _post_ability_resource_hook(character, ability, result):
    """Apply post-ability resource effects (builders, consumers)."""
    res = character.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    params = ability.get("effect_params", {})

    if rtype == "focus":
        if params.get("is_builder") and result:
            # Focus builder: add 1 combo point on successful ability (cap at max 5)
            res = dict(res)
            res["current"] = min(res["max"], res["current"] + 1)
            character.ndb.domain_resource = res
        elif params.get("consumes_all_focus"):
            # Consume all Focus points (damage already scaled by caller)
            res = dict(res)
            res["current"] = 0
            character.ndb.domain_resource = res
    elif rtype == "resonance" and params.get("resonance_generated"):
        # Resonance builder: add generated amount
        amount = params["resonance_generated"]
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + amount)
        character.ndb.domain_resource = res
    elif rtype == "momentum" and result:
        # Momentum: build 10 on successful ability use
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + 10)
        character.ndb.domain_resource = res
    elif rtype == "echoes" and result:
        # Echoes: build 5 on each ability use
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + 5)
        character.ndb.domain_resource = res
    elif rtype == "command" and result:
        # Command: build 5 on successful ability (solo rate)
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + 5)
        character.ndb.domain_resource = res


# ---------------------------------------------------------------------------
# Focus miss handler (exported)
# ---------------------------------------------------------------------------

def handle_focus_miss(character):
    """Reset Focus to 0 on miss. Called from combat_engine on ability miss."""
    res = character.ndb.domain_resource
    if res and res["type"] == "focus":
        res = dict(res)
        res["current"] = 0
        character.ndb.domain_resource = res


# ---------------------------------------------------------------------------
# Balance scaling helper (exported)
# ---------------------------------------------------------------------------

def get_balance_modifier(character, balance_type):
    """Return damage/heal modifier based on Balance pendulum position.
    position 0 (Feral) = 1.5x damage, position 100 (Calm) = 1.5x heal,
    position 50 = 1.0x both. Linear interpolation."""
    res = character.ndb.domain_resource
    if not res or res["type"] != "balance":
        return 1.0
    position = res["current"]
    if balance_type == "feral":
        return 1.0 + (50 - position) * 0.01
    elif balance_type == "calm":
        return 1.0 + (position - 50) * 0.01
    return 1.0


# ---------------------------------------------------------------------------
# Decay and lifecycle functions (exported)
# ---------------------------------------------------------------------------

def decay_resonance(combatant):
    """Decay Resonance by 10 per round. Called from combat_script.end_round."""
    res = combatant.ndb.domain_resource
    if res and res["type"] == "resonance":
        res = dict(res)
        res["current"] = max(0, res["current"] - 10)
        combatant.ndb.domain_resource = res


def on_round_end_resources(combatant, combat_handler):
    """Per-round resource hooks. Called from combat_script.end_round for each combatant."""
    res = combatant.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    if rtype == "resonance":
        decay_resonance(combatant)
    elif rtype == "focus":
        # Reset Focus if subterfuge character skipped their turn this round
        if not getattr(combatant.ndb, "ability_used_this_turn", False):
            res = dict(res)
            res["current"] = 0
            combatant.ndb.domain_resource = res
    elif rtype == "command":
        # Build Command from ally actions (group combat)
        _build_command_from_allies(combatant, combat_handler)


def _build_command_from_allies(combatant, combat_handler):
    """Build Command resource based on ally actions this round."""
    res = combatant.ndb.domain_resource
    if not res or res["type"] != "command":
        return
    # Count allies who acted this round
    ally_action_count = getattr(combat_handler.ndb, "ally_action_count", None) or {}
    my_allies = ally_action_count.get(str(combatant.id), 0)
    if my_allies > 0:
        amount = my_allies * 10  # 10 Command per ally action
    else:
        amount = 5  # Solo rate: 50% of 10
    res = dict(res)
    res["current"] = min(res["max"], res["current"] + amount)
    combatant.ndb.domain_resource = res


def on_encounter_end_resources(combatant):
    """Encounter-end resource lifecycle. Called from combat_script.end_combat."""
    res = combatant.ndb.domain_resource
    if not res:
        return
    rtype = res["type"]
    if rtype == "mana":
        # Mana recovers 15% at encounter end, persists
        res = dict(res)
        recovery = int(res["max"] * 0.15)
        res["current"] = min(res["max"], res["current"] + recovery)
        combatant.ndb.domain_resource = res
    elif rtype in ("focus", "influence", "command"):
        # Reset encounter-scoped resources
        res = dict(res)
        res["current"] = 0
        combatant.ndb.domain_resource = res
    elif rtype == "momentum":
        # Momentum decays between encounters
        res = dict(res)
        res["current"] = 0
        combatant.ndb.domain_resource = res
    elif rtype == "echoes":
        # Decrement investigation bonus persistence
        bonus = combatant.db.echoes_investigation_bonus
        if bonus and bonus.get("encounters_remaining", 0) > 0:
            bonus = dict(bonus)
            bonus["encounters_remaining"] -= 1
            if bonus["encounters_remaining"] <= 0:
                bonus["amount"] = 0
            combatant.db.echoes_investigation_bonus = bonus
    # resonance: no decay between encounters (persists)
    # reagents/components: persist as-is (finite stock, no regen)


def build_momentum_on_damage(character, amount=10):
    """Build Momentum when character lands a hit or takes damage.
    Called from combat_engine. Only applies if resource type is momentum."""
    res = character.ndb.domain_resource
    if res and res["type"] == "momentum":
        res = dict(res)
        res["current"] = min(res["max"], res["current"] + amount)
        character.ndb.domain_resource = res


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
    Type-aware: each domain starts with different pool values.
    """
    guild_id = character.db.guild_id
    if not guild_id:
        character.ndb.domain_resource = None
        return
    from world.guild_engine import GUILDS, FINGERPRINTS
    guild = GUILDS.get(guild_id, {})
    domain = guild.get("primary_domain")
    fp = FINGERPRINTS.get(domain, {})
    resource_type = fp.get("resource_type", fp.get("resource", domain))

    # Type-aware initialization
    if resource_type == "focus":
        current, pool_max = 0, 5
    elif resource_type == "balance":
        current, pool_max = 50, 100
    elif resource_type == "mana":
        pool_max = fp.get("resource_max", 100)
        current = pool_max  # Mana starts full, persists across encounters
    elif resource_type == "influence":
        from world.world_state import get_dimension_score
        pool_max = int(20 + get_dimension_score(character, "reputation") * 0.5)
        pool_max = max(20, pool_max)
        current = pool_max  # Full pool each encounter
    elif resource_type == "reagents":
        current = character.db.reagent_stock or 50
        pool_max = 100
    elif resource_type == "components":
        current = character.db.component_stock or 50
        pool_max = 100
    elif resource_type == "echoes":
        bonus = character.db.echoes_investigation_bonus
        investigation_bonus = bonus.get("amount", 0) if bonus else 0
        current = investigation_bonus
        pool_max = 100
    elif resource_type == "momentum":
        current, pool_max = 0, 100
    elif resource_type == "resonance":
        current, pool_max = 0, 100
    elif resource_type == "command":
        current, pool_max = 0, 100
    else:
        # Generic fallback
        pool_max = fp.get("resource_max", 100)
        current = 0

    character.ndb.domain_resource = {
        "type": resource_type,
        "current": current,
        "max": pool_max,
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
    """Check and deduct resource cost. Returns (bool, str).
    Uses type-aware dispatch via RESOURCE_HANDLERS."""
    res = character.ndb.domain_resource
    if not res:
        cost = ability.get("resource_cost", 0)
        if cost <= 0:
            return True, ""
        return False, "No domain resource available."
    handler = RESOURCE_HANDLERS.get(res["type"])
    if handler:
        return handler(character, ability)
    # Fallback to generic spend
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

    # Post-ability resource hooks
    _post_ability_resource_hook(character, ability, result)

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
