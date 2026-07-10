"""
Combat engine core for Soravelon.

Damage resolution, critical hit system, ability damage, healing,
elite/boss scaling, death handling, and corpse spawning. All combat
math flows through this module.

resolve_basic_attack() and resolve_ability_damage() integrate zone
scaling from world/zone_scaling.py, elemental resistance, and
Acuity-driven critical hits (2.0x multiplier per D-20).

Exports:
    DOMAIN_TO_STAT, roll_crit, resolve_basic_attack,
    resolve_ability_damage, resolve_heal, apply_elite_boss_scaling,
    check_death, handle_mob_death, handle_player_death, spawn_corpse
"""

import random
import time

from world.equipment_effects import BARE_HANDS_MAX, BARE_HANDS_MIN

# ---------------------------------------------------------------------------
# Domain-to-stat mapping (validated against ability_registry.py)
#
# Maps domain names (used in ability scaling_primary / scaling_secondary)
# to base attribute stat names from STAT_NAMES.
# ---------------------------------------------------------------------------

DOMAIN_TO_STAT = {
    "combat": "strength",
    "subterfuge": "agility",
    "naturalism": "resonance",
    "resonance": "resonance",
    "arcana": "mana",
    "diplomacy": "presence",
    "alchemy": "acuity",
    "tactics": "acuity",
    "engineering": "acuity",
    "remnance": "mana",
}

# Base crit chance for characters
BASE_CRIT_CHANCE = 0.05
# Acuity bonus per point (0.2% = 0.002)
ACUITY_CRIT_BONUS = 0.002
# Default mob crit chance
MOB_CRIT_CHANCE = 0.03
# Base crit multiplier
CRIT_MULTIPLIER = 2.0


# ---------------------------------------------------------------------------
# Critical hit system (D-20)
# ---------------------------------------------------------------------------

def roll_crit(attacker, effective_stats=None):
    """
    Roll for critical hit. Acuity-driven for characters, flat for mobs.

    Characters: base 5% + Acuity * 0.2%.
    Mobs: mob.db.crit_chance if set, else 3% flat.

    Returns:
        (bool, float): (is_crit, multiplier). Multiplier is 2.0 on crit, 1.0 otherwise.
    """
    base_stats = attacker.db.base_stats
    if base_stats:
        # Character: Acuity-based crit
        acuity = _get_modified_stat_value(
            attacker,
            "acuity",
            10,
            effective_stats=effective_stats,
        )
        crit_chance = BASE_CRIT_CHANCE + (acuity * ACUITY_CRIT_BONUS)
    else:
        # Mob: flat crit chance
        crit_chance = attacker.db.crit_chance or MOB_CRIT_CHANCE

    is_crit = random.random() < crit_chance
    multiplier = CRIT_MULTIPLIER if is_crit else 1.0

    if is_crit and base_stats:
        from world.base_attributes import record_stat_use
        record_stat_use(attacker, "critical_hit")

    return is_crit, multiplier


# ---------------------------------------------------------------------------
# Elite/boss scaling (D-21)
# ---------------------------------------------------------------------------

def apply_elite_boss_scaling(damage, mob_rarity, is_incoming=True):
    """
    Apply elite/boss scaling modifiers.

    Args:
        damage: Raw damage value.
        mob_rarity: Mob rarity string ("normal", "magic", "rare", "legendary").
        is_incoming: True if mob attacking player, False if player attacking mob.

    Returns:
        int: Adjusted damage.
    """
    if mob_rarity in ("rare", "elite"):
        if is_incoming:
            return int(damage * 1.40)
        else:
            return max(1, int(damage * 0.75))
    elif mob_rarity == "legendary":
        if is_incoming:
            return int(damage * 1.80)
        else:
            return max(1, int(damage * 0.50))
    return int(damage)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _compute_raw_damage(attacker, weapon, effective_stats=None):
    """Compute base raw damage for character or mob attacker.

    Characters use equipped weapon (or bare hands) + its authored stat.
    Mobs use ref_damage_min/max range.

    Returns:
        (int, str): (raw_damage, element).
    """
    attacker_stats = attacker.db.base_stats
    if attacker_stats:
        from world.equipment_effects import get_weapon_damage_profile

        profile = get_weapon_damage_profile(weapon)
        scaling_value = _get_modified_stat_value(
            attacker,
            profile.scaling_stat,
            10,
            effective_stats=effective_stats,
        )
        raw = random.randint(profile.minimum, profile.maximum) + int(
            scaling_value * 0.5
        )
        element = profile.element
        from world.weapon_skills import weapon_skill_damage_bonus_for_attack
        skill_bonus = weapon_skill_damage_bonus_for_attack(attacker, weapon)
        if skill_bonus:
            raw = max(1, int(raw * (1 + skill_bonus)))
    else:
        raw_min = attacker.db.ref_damage_min or 8
        raw_max = attacker.db.ref_damage_max or 14
        raw = random.randint(raw_min, raw_max)
        element = attacker.db.element or "physical"
    return raw, element


def _get_modified_stat_value(
    actor,
    stat_name,
    default=10,
    effective_stats=None,
):
    """Return an equipment-aware stat with temporary effects applied."""
    if effective_stats is None:
        from world.equipment_effects import get_effective_stats

        effective_stats = get_effective_stats(actor)
    if not effective_stats:
        return default

    value = effective_stats.get(stat_name, default)

    from world.status_effects import get_effect_modifiers

    boost = get_effect_modifiers(actor).get("stat_multipliers", {}).get(stat_name, 0.0)
    return int(value * (1 + boost))


def _get_echo_scaling_bonus(character):
    """Return a capped damage bonus for lore-heavy echo spenders."""
    resource = getattr(character.ndb, "domain_resource", None) or {}
    current_echoes = resource.get("current", 0) if resource.get("type") == "echoes" else 0
    bonus_data = getattr(character.db, "echoes_investigation_bonus", None)
    stored_bonus = bonus_data.get("amount", 0) if isinstance(bonus_data, dict) else 0
    return 1.0 + min(0.75, (current_echoes + stored_bonus) / 100.0)


def _apply_attack_followups(attacker, target, payload):
    """Apply next-hit rider effects after a successful damaging attack."""
    from world import status_effects

    for effect in payload.get("status_effects", []):
        status_effects.apply_effect(
            target,
            effect["effect_type"],
            effect.get("duration", 3),
            effect.get("magnitude", 1.0),
            attacker.id,
        )


def _apply_incoming_damage(attacker, target, damage, ignore_reduction=False, ignore_absorb=False):
    """Apply damage reduction, absorb pools, and reflect before HP loss."""
    from world.status_effects import get_effect_modifiers, mitigate_incoming_damage

    target_mods = get_effect_modifiers(target)
    final = damage
    absorbed = 0
    reflected = 0

    dmg_reduction = 0.0 if ignore_reduction else target_mods.get("damage_reduction", 0.0)
    if dmg_reduction > 0:
        final = max(1, int(final * (1 - dmg_reduction)))

    if not ignore_reduction and target.db.base_stats:
        from world.equipment_effects import (
            apply_armor_mitigation,
            get_total_equipped_armor,
        )

        final = apply_armor_mitigation(
            final,
            get_total_equipped_armor(target),
        )

    if ignore_absorb:
        absorbed = 0
    else:
        final, absorbed = mitigate_incoming_damage(target, final)

    current_hp = target.ndb.hp or 0
    target.ndb.hp = max(0, current_hp - final)

    reflect_pct = target_mods.get("reflect_percent", 0.0)
    if final > 0 and reflect_pct > 0 and getattr(attacker.ndb, "hp", None) is not None:
        reflected = max(1, int(final * reflect_pct))
        attacker.ndb.hp = max(0, (attacker.ndb.hp or 0) - reflected)

    return final, absorbed, reflected


# ---------------------------------------------------------------------------
# Basic attack resolution (D-19)
# ---------------------------------------------------------------------------

def resolve_basic_attack(attacker, target, weapon=None):
    """
    Resolve a basic (auto) attack.

    Computes raw damage from weapon or bare hands (characters) or
    ref_damage range (mobs), applies crit, zone scaling, resistance,
    and elite/boss modifiers.

    Args:
        attacker: Character or mob performing the attack.
        target: Character or mob receiving the attack.
        weapon: Optional weapon object with db.damage_min/damage_max.

    Returns:
        (bool, str, int): (success, message, damage_dealt).
    """
    from world.zone_scaling import (
        get_player_damage_to_mob, get_mob_damage_for_player, apply_resistance,
    )
    from world.status_effects import consume_attack_effects, get_effect_modifiers

    # Check miss from blind effect
    target_mods = get_effect_modifiers(target)
    attacker_mods = get_effect_modifiers(attacker)
    next_attack = consume_attack_effects(attacker, consume=False)
    miss_chance = max(
        0.0,
        attacker_mods.get("miss_chance_increase", 0.0) - attacker_mods.get("accuracy_bonus", 0.0),
    )
    if miss_chance > 0 and random.random() < miss_chance:
        return (False, f"{attacker.key}'s attack misses!", 0)
    evasion = target_mods.get("evasion_bonus", 0.0)
    if evasion > 0 and random.random() < evasion:
        return (False, f"{target.key} evades {attacker.key}'s attack!", 0)

    attacker_stats = attacker.db.base_stats
    effective_stats = None
    if attacker_stats:
        from world.equipment_effects import get_effective_stats

        effective_stats = get_effective_stats(attacker)

    raw, element = _compute_raw_damage(
        attacker,
        weapon,
        effective_stats=effective_stats,
    )

    # Critical hit
    if next_attack.get("guaranteed_crit"):
        is_crit, crit_mult = True, CRIT_MULTIPLIER
    else:
        is_crit, crit_mult = roll_crit(
            attacker,
            effective_stats=effective_stats,
        )
    raw = int(raw * crit_mult)
    raw += int(next_attack.get("bonus_damage", 0))
    raw = max(1, int(raw * (1 + attacker_mods.get("damage_bonus", 0.0))))

    # Zone scaling
    target_stats = target.db.base_stats
    if attacker_stats and not target_stats:
        # Character attacking mob
        scaled = get_player_damage_to_mob(raw, target, attacker)
    elif not attacker_stats and target_stats:
        # Mob attacking character -- use scaled range
        scaled_min, scaled_max = get_mob_damage_for_player(attacker, target)
        # raw was from ref range; scale proportionally
        ref_min = attacker.db.ref_damage_min or 8
        ref_max = attacker.db.ref_damage_max or 14
        ref_range = max(1, ref_max - ref_min)
        ratio = (raw / crit_mult - ref_min) / ref_range if ref_range > 0 else 0.5
        ratio = max(0.0, min(1.0, ratio))
        scaled = int(scaled_min + ratio * (scaled_max - scaled_min))
        scaled = int(scaled * crit_mult)
    else:
        scaled = raw

    # Elemental resistance
    final = apply_resistance(scaled, element, target)

    # Elite/boss scaling
    if not attacker_stats and target_stats:
        # Mob attacking player
        mob_rarity = attacker.db.rarity or "normal"
        final = apply_elite_boss_scaling(final, mob_rarity, is_incoming=True)
    elif attacker_stats and not target_stats:
        # Player attacking mob
        mob_rarity = target.db.rarity or "normal"
        final = apply_elite_boss_scaling(final, mob_rarity, is_incoming=False)

    # Defensive mitigation and reflection
    final, absorbed, reflected = _apply_incoming_damage(attacker, target, final)

    # Flag for petrify break-on-damage check
    if final > 0:
        target.ndb.took_damage_this_round = True
        _apply_attack_followups(attacker, target, consume_attack_effects(attacker, consume=True))

    # Record stat use
    if attacker_stats:
        from world.base_attributes import record_stat_use
        from world.weapon_skills import accumulate_weapon_skill_for_attack
        record_stat_use(attacker, "melee_hit")
        accumulate_weapon_skill_for_attack(attacker, weapon)
    if target_stats:
        from world.base_attributes import record_stat_use
        record_stat_use(target, "damage_taken")

    # Build Momentum for attacker on hit and target on damage taken (D-04)
    from world.ability_engine import build_momentum_on_damage
    build_momentum_on_damage(attacker, 10)
    build_momentum_on_damage(target, 5)

    # Build message
    crit_tag = " |y*CRITICAL*|n" if is_crit else ""
    absorb_tag = f" |c({absorbed} absorbed)|n" if absorbed else ""
    reflect_tag = f" |m({reflected} reflected)|n" if reflected else ""
    msg = (
        f"{attacker.key} strikes {target.key} for "
        f"|r{final}|n {element} damage.{crit_tag}{absorb_tag}{reflect_tag}"
    )

    return (True, msg, final)


# ---------------------------------------------------------------------------
# Ability damage resolution (D-08 vault formula)
# ---------------------------------------------------------------------------

def resolve_ability_damage(character, ability, target):
    """
    Resolve ability-based damage.

    Formula: ability_base * (1 + primary_stat*0.02 + secondary_stat*0.01)
    Then crit, zone scaling, resistance, elite/boss modifiers.

    Args:
        character: Character using the ability.
        ability: Ability dict from ABILITIES registry.
        target: Target combatant.

    Returns:
        (bool, str, int): (success, message, damage_dealt).
    """
    from world.zone_scaling import get_player_damage_to_mob, apply_resistance
    from world.status_effects import consume_attack_effects, get_effect_modifiers

    # Check miss from blind/status effects (D-05: Focus resets on miss)
    attacker_mods = get_effect_modifiers(character)
    target_mods = get_effect_modifiers(target)
    params = ability.get("effect_params", {})
    next_attack = (
        {"bonus_damage": 0, "guaranteed_crit": False, "status_effects": []}
        if params.get("ignore_attack_buffs")
        else consume_attack_effects(character, consume=False)
    )
    miss_chance = max(
        0.0,
        attacker_mods.get("miss_chance_increase", 0.0) - attacker_mods.get("accuracy_bonus", 0.0),
    )
    if miss_chance > 0 and random.random() < miss_chance:
        from world.ability_engine import handle_focus_miss
        handle_focus_miss(character)
        ability_name = ability.get("name", "ability")
        return (False, f"{character.key}'s {ability_name} misses!", 0)
    evasion = target_mods.get("evasion_bonus", 0.0)
    if evasion > 0 and random.random() < evasion:
        from world.ability_engine import handle_focus_miss
        handle_focus_miss(character)
        ability_name = ability.get("name", "ability")
        return (False, f"{target.key} evades {character.key}'s {ability_name}!", 0)

    from world.equipment_effects import get_effective_stats

    effective_stats = get_effective_stats(character)

    # Stat lookups via domain-to-stat mapping
    primary_stat_name = DOMAIN_TO_STAT.get(
        ability.get("scaling_primary", "combat"), "strength"
    )
    primary_stat = _get_modified_stat_value(
        character,
        primary_stat_name,
        10,
        effective_stats=effective_stats,
    )

    secondary_domain = ability.get("scaling_secondary")
    if secondary_domain:
        secondary_stat_name = DOMAIN_TO_STAT.get(secondary_domain, "strength")
        secondary_stat = _get_modified_stat_value(
            character,
            secondary_stat_name,
            10,
            effective_stats=effective_stats,
        )
    else:
        secondary_stat = 0

    # Base damage from ability definition (prefer effect_params)
    ability_base = params.get("damage_base") or ability.get("damage_base", 15)
    raw = ability_base * (1 + primary_stat * 0.02 + secondary_stat * 0.01)

    if params.get("echo_scaling"):
        raw = int(raw * _get_echo_scaling_bonus(character))

    # Balance pendulum scaling (D-06)
    balance_type = params.get("balance_type")
    if balance_type:
        from world.ability_engine import get_balance_modifier
        balance_mod = get_balance_modifier(character, balance_type)
        raw = int(raw * balance_mod)

    # Critical hit
    if params.get("guaranteed_crit") or next_attack.get("guaranteed_crit"):
        is_crit, crit_mult = True, CRIT_MULTIPLIER
    else:
        is_crit, crit_mult = roll_crit(
            character,
            effective_stats=effective_stats,
        )
    raw = int(raw * crit_mult)
    raw += int(next_attack.get("bonus_damage", 0))
    raw = max(1, int(raw * (1 + attacker_mods.get("damage_bonus", 0.0))))

    # Zone scaling (player attacking mob)
    target_stats = target.db.base_stats
    if not target_stats:
        scaled = get_player_damage_to_mob(raw, target, character)
    else:
        scaled = raw

    # Element from ability or default physical
    element = ability.get("element", "physical")

    # Elemental resistance
    if params.get("piercing") or params.get("ignores_armor") or params.get("unique_damage_type"):
        final = scaled
    else:
        final = apply_resistance(scaled, element, target)

    # Elite/boss scaling (if target is mob)
    if not target_stats:
        mob_rarity = target.db.rarity or "normal"
        final = apply_elite_boss_scaling(final, mob_rarity, is_incoming=False)

    # Defensive mitigation and reflection
    final, absorbed, reflected = _apply_incoming_damage(
        character,
        target,
        final,
        ignore_reduction=bool(params.get("ignores_armor")),
        ignore_absorb=bool(params.get("ignores_armor")),
    )

    # Flag for petrify break-on-damage check
    if final > 0:
        target.ndb.took_damage_this_round = True
        if not params.get("ignore_attack_buffs"):
            _apply_attack_followups(character, target, consume_attack_effects(character, consume=True))

    # Record stat use
    from world.base_attributes import record_stat_use
    record_stat_use(character, "melee_hit")

    # Build Momentum for target on damage taken (D-04)
    from world.ability_engine import build_momentum_on_damage
    build_momentum_on_damage(target, 5)

    # Apply status effect from ability if specified (prefer effect_params)
    status_effect = params.get("status_effect") or ability.get("status_effect")
    if status_effect:
        from world import status_effects
        status_effects.apply_effect(
            target,
            status_effect,
            params.get("status_duration") or params.get("duration") or ability.get("effect_duration", 3),
            params.get("status_magnitude") or params.get("magnitude") or ability.get("effect_magnitude", 1.0),
            character.id,
        )
    if params.get("bleed"):
        from world import status_effects
        status_effects.apply_effect(
            target,
            "bleed",
            params.get("bleed_duration", 3),
            params.get("bleed_damage", 1.0),
            character.id,
        )
    for extra_effect in params.get("secondary_effects", []) or []:
        from world import status_effects
        status_effects.apply_effect(
            target,
            extra_effect,
            params.get("secondary_duration", params.get("duration") or ability.get("effect_duration", 3)),
            params.get("secondary_magnitude", params.get("magnitude") or ability.get("effect_magnitude", 1.0)),
            character.id,
        )

    # Build message
    crit_tag = " |y*CRITICAL*|n" if is_crit else ""
    absorb_tag = f" |c({absorbed} absorbed)|n" if absorbed else ""
    reflect_tag = f" |m({reflected} reflected)|n" if reflected else ""
    ability_name = ability.get("name", "ability")
    msg = (
        f"{character.key} uses {ability_name} on {target.key} for "
        f"|r{final}|n {element} damage.{crit_tag}{absorb_tag}{reflect_tag}"
    )

    return (True, msg, final)


# ---------------------------------------------------------------------------
# Heal resolution
# ---------------------------------------------------------------------------

def resolve_heal(character, ability, target):
    """
    Resolve a healing ability.

    Formula: heal_base * (1 + primary_stat * 0.015)

    Args:
        character: Character casting the heal.
        ability: Ability dict from ABILITIES registry.
        target: Heal target (often self).

    Returns:
        (bool, str, int): (success, message, heal_amount).
    """
    from world.base_attributes import derive_max_hp

    from world.equipment_effects import get_effective_stats

    effective_stats = get_effective_stats(character)
    primary_stat_name = DOMAIN_TO_STAT.get(
        ability.get("scaling_primary", "naturalism"), "resonance"
    )
    primary_stat = _get_modified_stat_value(
        character,
        primary_stat_name,
        10,
        effective_stats=effective_stats,
    )

    params = ability.get("effect_params", {})
    heal_base = (
        params.get("heal_base")
        or params.get("heal_amount")
        or ability.get("heal_base")
        or ability.get("damage_base", 20)
    )
    heal_amount = int(heal_base * (1 + primary_stat * 0.015))

    # Balance pendulum scaling for heals (D-06: Calm position boosts heals)
    balance_type = params.get("balance_type")
    if balance_type:
        from world.ability_engine import get_balance_modifier
        balance_mod = get_balance_modifier(character, balance_type)
        heal_amount = int(heal_amount * balance_mod)

    max_hp = derive_max_hp(target)
    current_hp = target.ndb.hp or 0
    new_hp = min(max_hp, current_hp + heal_amount)
    actual_healed = new_hp - current_hp
    target.ndb.hp = new_hp

    ability_name = ability.get("name", "heal")
    msg = (
        f"{character.key} heals {target.key} for "
        f"|g{actual_healed}|n HP with {ability_name}."
    )

    return (True, msg, actual_healed)


# ---------------------------------------------------------------------------
# Death checking and handling (D-26, D-27)
# ---------------------------------------------------------------------------

def check_death(combatant):
    """Return True if combatant's HP is at or below 0."""
    hp = combatant.ndb.hp
    if hp is None:
        return False
    return hp <= 0


def handle_mob_death(mob, killer):
    """
    Process mob death: fire at_death, spawn corpse, return message.

    Args:
        mob: The defeated mob.
        killer: Character who dealt the killing blow.

    Returns:
        str: Death message for combat log.
    """
    mob_name = mob.key

    # Snapshot room contents BEFORE at_death to avoid sweeping unrelated items
    room = mob.location
    pre_death_ids = set(obj.id for obj in room.contents) if room else set()

    # Freeze encounter eligibility before any death hook can mutate combat
    # state. Personal reward and quest-credit decisions share this exact roster.
    from world.encounter_rewards import snapshot_reward_recipients

    recipients = snapshot_reward_recipients(mob, killer)
    corpse = spawn_corpse(
        mob,
        killer,
        authorized_looter_ids=[recipient.id for recipient in recipients],
    )
    mob.ndb.encounter_reward_recipients = recipients
    mob.ndb.encounter_reward_corpse = corpse

    # Call existing at_death hook (handles loot drops, triggers, respawn)
    mob.at_death(killer=killer)

    # Move ONLY newly dropped loot (items that appeared after at_death) into corpse
    if room and corpse:
        _move_room_loot_to_corpse(room, corpse, mob_name, pre_death_ids)

    # Remove defeated mob from the game world
    mob.delete()

    msg = f"|r{mob_name} has been slain!|n"
    return msg


def handle_player_death(character):
    """
    Process player death per D-26: spawn corpse with equipment.
    D-14: Respawn at medic building (respawn_point tag).

    Args:
        character: The defeated player character.

    Returns:
        str: Death message.
    """
    room = character.location
    if room:
        corpse = _spawn_player_corpse(character, room)
        from world.inventory_engine import move_owned_items_to_world_container

        move_owned_items_to_world_container(
            character,
            list(character.contents),
            corpse,
        )

    character.ndb.hp = 0
    msg = f"|r{character.key} has fallen!|n"

    # Death penalty: drop 20% Scales to corpse, wipe uncommitted session XP
    from world.banking import on_character_death
    on_character_death(character, room)

    # D-14: Respawn at medic building via tag lookup
    _respawn_player(character)

    return msg


def _respawn_player(character):
    """
    Teleport player to the nearest reachable respawn point after death.
    Falls back to character home, then any respawn_point tagged room.
    """
    from collections import deque
    from evennia.utils.search import search_tag
    from world.base_attributes import derive_max_hp, derive_max_stamina
    from world import oob_publisher

    def _is_respawn_room(room):
        return bool(
            room
            and hasattr(room, "tags")
            and room.tags.has("respawn_point", category="spawn_point")
        )

    def _find_nearest_respawn(room):
        if _is_respawn_room(room):
            return room
        if not room:
            return None

        queue = deque([room])
        seen = {room.id}
        while queue:
            current = queue.popleft()
            for exit_obj in getattr(current, "exits", []) or []:
                destination = getattr(exit_obj, "destination", None)
                if destination is None or destination.id in seen:
                    continue
                if _is_respawn_room(destination):
                    return destination
                seen.add(destination.id)
                queue.append(destination)
        return None

    destination = _find_nearest_respawn(character.location)
    if destination is None and character.home:
        destination = character.home
    if destination is None:
        respawn_rooms = search_tag("respawn_point", category="spawn_point")
        if respawn_rooms:
            destination = respawn_rooms[0]
    if destination is None:
        return  # nowhere to go

    room_id = destination.tags.get(category="room_id") if hasattr(destination, "tags") else None
    if room_id:
        visited = set(character.db.visited_room_ids or set())
        if room_id not in visited:
            visited.add(room_id)
            character.db.visited_room_ids = visited

    character.move_to(destination, quiet=True, move_hooks=False)
    character.ndb.oob_debounce = {}
    # Restore partial HP on respawn
    character.ndb.hp = max(1, derive_max_hp(character) // 4)
    character.ndb.stamina = derive_max_stamina(character) // 4
    oob_publisher.push_status_update(character)
    oob_publisher.push_stat_update(character)
    oob_publisher.push_map_update(character)
    oob_publisher.push_inventory_update(character)
    character.msg(
        "|yYou awaken on a cot in the medic station, bandaged and "
        "bruised. Your belongings remain where you fell.|n"
    )


# ---------------------------------------------------------------------------
# Corpse spawning (D-27)
# ---------------------------------------------------------------------------

def spawn_corpse(mob, killer, authorized_looter_ids=None):
    """
    Create a CorpseContainer at the mob's location.

    Sets killer lock, group leader ID, loot phase timing.
    Schedules phase transitions: GRACE_PERIOD -> open, then delete.

    Args:
        mob: The defeated mob.
        killer: Character who killed the mob.

    Returns:
        CorpseContainer instance, or None if no location.
    """
    room = mob.location
    if not room:
        return None

    from evennia import create_object
    from typeclasses.objects import CorpseContainer

    corpse_name = f"corpse of {mob.key}"
    corpse = create_object(
        CorpseContainer,
        key=corpse_name,
        location=room,
    )

    corpse.db.killer_id = killer.id
    corpse.db.mob_key = _get_mob_loot_identity(mob)
    corpse.db.mob_rarity = mob.db.rarity or "normal"
    corpse.db.butcherable = True
    corpse.db.butchered = False

    # Snapshot authorized looters at corpse creation so reloads/disconnects
    # cannot rewrite access through ephemeral ndb group state. Encounter entry
    # supplies the authoritative nearby participants; direct callers preserve
    # the old group fallback.
    if authorized_looter_ids is None:
        from world.group_engine import get_group_member_ids

        authorized_ids = get_group_member_ids(killer)
        if not authorized_ids:
            authorized_ids = [killer.id]
    else:
        authorized_ids = list(authorized_looter_ids)
        if not authorized_ids:
            authorized_ids = [killer.id]
    corpse.db.authorized_looter_ids = authorized_ids
    corpse.db.killer_group_leader_id = getattr(
        killer.ndb, "group_leader_id", None
    )

    # Set decay timestamp for crash-recovery sweep
    grace = CorpseContainer.GRACE_PERIOD
    open_period = CorpseContainer.OPEN_PERIOD
    corpse.db.decay_at = time.time() + grace + open_period

    # Schedule phase transitions using Evennia's delay
    from evennia.utils import delay
    delay(grace, _transition_corpse, corpse.id, "open")
    delay(grace + open_period, _transition_corpse, corpse.id, "decayed")

    return corpse


def _get_mob_loot_identity(mob):
    """Return the stable registry key used by loot/gathering systems."""
    for attr_name in ("mob_type", "mob_template_key"):
        value = getattr(mob.db, attr_name, None)
        if isinstance(value, str) and value:
            return value
    return mob.key


def _spawn_player_corpse(character, room):
    """Create a player corpse container at room."""
    from evennia import create_object
    from typeclasses.objects import CorpseContainer

    corpse_name = f"remains of {character.key}"
    corpse = create_object(
        CorpseContainer,
        key=corpse_name,
        location=room,
    )
    corpse.db.killer_id = character.id  # player owns their own corpse
    corpse.db.authorized_looter_ids = [character.id]
    corpse.db.mob_key = character.key
    corpse.db.loot_phase = "open"  # player corpses immediately accessible
    corpse.db.decay_at = time.time() + CorpseContainer.OPEN_PERIOD

    from evennia.utils import delay
    delay(
        CorpseContainer.OPEN_PERIOD,
        _transition_corpse, corpse.id, "decayed",
    )

    return corpse


def _transition_corpse(corpse_id, new_phase):
    """
    Transition a corpse to a new loot phase. Called by delay().

    Args:
        corpse_id: Database ID of the CorpseContainer.
        new_phase: "open" or "decayed".
    """
    import evennia
    results = evennia.search_object("#" + str(corpse_id))
    if not results:
        return
    corpse = results[0]

    if new_phase == "decayed":
        corpse.delete()
    else:
        corpse.db.loot_phase = new_phase


def _move_room_loot_to_corpse(room, corpse, mob_name, pre_death_ids=None):
    """
    Move recently spawned loot items from room into corpse.

    Only moves items that appeared AFTER at_death (not in pre_death_ids).
    This prevents sweeping unrelated items that were already in the room.
    """
    from typeclasses.objects import SoravelonItem

    pre_death_ids = pre_death_ids or set()
    for obj in list(room.contents):
        if (isinstance(obj, SoravelonItem)
                and obj != corpse
                and obj.id not in pre_death_ids):
            obj.move_to(corpse, quiet=True)
