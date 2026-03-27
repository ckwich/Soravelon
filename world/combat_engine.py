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

# Bare-hands fallback damage range
BARE_HANDS_MIN = 3
BARE_HANDS_MAX = 6

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

def roll_crit(attacker):
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
        acuity = base_stats.get("acuity", 10)
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
    from world.status_effects import get_effect_modifiers

    # Check miss from blind effect
    target_mods = get_effect_modifiers(target)
    attacker_mods = get_effect_modifiers(attacker)
    miss_chance = attacker_mods.get("miss_chance_increase", 0.0)
    if miss_chance > 0 and random.random() < miss_chance:
        return (False, f"{attacker.key}'s attack misses!", 0)

    attacker_stats = attacker.db.base_stats

    if attacker_stats:
        # Character attacking
        strength = attacker_stats.get("strength", 10)
        if weapon:
            w_min = weapon.db.damage_min or BARE_HANDS_MIN
            w_max = weapon.db.damage_max or BARE_HANDS_MAX
            element = weapon.db.element or "physical"
        else:
            w_min = BARE_HANDS_MIN
            w_max = BARE_HANDS_MAX
            element = "physical"
        raw = random.randint(w_min, w_max) + int(strength * 0.5)
    else:
        # Mob attacking
        raw_min = attacker.db.ref_damage_min or 8
        raw_max = attacker.db.ref_damage_max or 14
        raw = random.randint(raw_min, raw_max)
        element = attacker.db.element or "physical"

    # Critical hit
    is_crit, crit_mult = roll_crit(attacker)
    raw = int(raw * crit_mult)

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

    # Apply weaken damage reduction from status effects
    dmg_reduction = target_mods.get("damage_reduction", 0.0)
    if dmg_reduction > 0:
        final = max(1, int(final * (1 - dmg_reduction)))

    # Reduce target HP
    current_hp = target.ndb.hp or 0
    target.ndb.hp = max(0, current_hp - final)

    # Record stat use
    if attacker_stats:
        from world.base_attributes import record_stat_use
        record_stat_use(attacker, "melee_hit")
    if target_stats:
        from world.base_attributes import record_stat_use
        record_stat_use(target, "damage_taken")

    # Build message
    crit_tag = " |y*CRITICAL*|n" if is_crit else ""
    msg = (
        f"{attacker.key} strikes {target.key} for "
        f"|r{final}|n {element} damage.{crit_tag}"
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

    stats = character.db.base_stats or {}

    # Stat lookups via domain-to-stat mapping
    primary_stat_name = DOMAIN_TO_STAT.get(
        ability.get("scaling_primary", "combat"), "strength"
    )
    primary_stat = stats.get(primary_stat_name, 10)

    secondary_domain = ability.get("scaling_secondary")
    if secondary_domain:
        secondary_stat_name = DOMAIN_TO_STAT.get(secondary_domain, "strength")
        secondary_stat = stats.get(secondary_stat_name, 10)
    else:
        secondary_stat = 0

    # Base damage from ability definition (prefer effect_params)
    params = ability.get("effect_params", {})
    ability_base = params.get("damage_base") or ability.get("damage_base", 15)
    raw = ability_base * (1 + primary_stat * 0.02 + secondary_stat * 0.01)

    # Critical hit
    is_crit, crit_mult = roll_crit(character)
    raw = int(raw * crit_mult)

    # Zone scaling (player attacking mob)
    target_stats = target.db.base_stats
    if not target_stats:
        scaled = get_player_damage_to_mob(raw, target, character)
    else:
        scaled = raw

    # Element from ability or default physical
    element = ability.get("element", "physical")

    # Elemental resistance
    final = apply_resistance(scaled, element, target)

    # Elite/boss scaling (if target is mob)
    if not target_stats:
        mob_rarity = target.db.rarity or "normal"
        final = apply_elite_boss_scaling(final, mob_rarity, is_incoming=False)

    # Apply weaken from status effects
    from world.status_effects import get_effect_modifiers
    target_mods = get_effect_modifiers(target)
    dmg_reduction = target_mods.get("damage_reduction", 0.0)
    if dmg_reduction > 0:
        final = max(1, int(final * (1 - dmg_reduction)))

    # Reduce target HP
    current_hp = target.ndb.hp or 0
    target.ndb.hp = max(0, current_hp - final)

    # Record stat use
    from world.base_attributes import record_stat_use
    record_stat_use(character, "melee_hit")

    # Apply status effect from ability if specified (prefer effect_params)
    status_effect = params.get("status_effect") or ability.get("status_effect")
    if status_effect:
        from world import status_effects
        status_effects.apply_effect(
            target,
            status_effect,
            params.get("duration") or ability.get("effect_duration", 3),
            params.get("magnitude") or ability.get("effect_magnitude", 1.0),
            character.id,
        )

    # Build message
    crit_tag = " |y*CRITICAL*|n" if is_crit else ""
    ability_name = ability.get("name", "ability")
    msg = (
        f"{character.key} uses {ability_name} on {target.key} for "
        f"|r{final}|n {element} damage.{crit_tag}"
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

    stats = character.db.base_stats or {}
    primary_stat_name = DOMAIN_TO_STAT.get(
        ability.get("scaling_primary", "naturalism"), "resonance"
    )
    primary_stat = stats.get(primary_stat_name, 10)

    heal_base = ability.get("heal_base", 20)
    heal_amount = int(heal_base * (1 + primary_stat * 0.015))

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

    # Call existing at_death hook (handles loot drops, triggers, respawn)
    mob.at_death(killer=killer)

    # Spawn corpse container for loot access
    corpse = spawn_corpse(mob, killer)

    # Move any loot dropped to room by at_death into the corpse
    if mob.location and corpse:
        _move_room_loot_to_corpse(mob.location, corpse, mob_name)

    msg = f"|r{mob_name} has been slain!|n"
    return msg


def handle_player_death(character):
    """
    Process player death per D-26: spawn corpse with equipment.

    Actual respawn teleport handled by CombatScript on cleanup.

    Args:
        character: The defeated player character.

    Returns:
        str: Death message.
    """
    room = character.location
    if room:
        corpse = _spawn_player_corpse(character, room)
        # Move all carried items into corpse
        for item in list(character.contents):
            item.move_to(corpse, quiet=True)

    character.ndb.hp = 0
    msg = f"|r{character.key} has fallen!|n"
    return msg


# ---------------------------------------------------------------------------
# Corpse spawning (D-27)
# ---------------------------------------------------------------------------

def spawn_corpse(mob, killer):
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
    corpse.db.mob_key = mob.key
    corpse.db.mob_rarity = mob.db.rarity or "normal"

    # Group leader for group loot access
    group_leader_id = getattr(killer.ndb, "group_leader_id", None)
    corpse.db.killer_group_leader_id = group_leader_id

    # Set decay timestamp for crash-recovery sweep
    grace = CorpseContainer.GRACE_PERIOD
    open_period = CorpseContainer.OPEN_PERIOD
    corpse.db.decay_at = time.time() + grace + open_period

    # Schedule phase transitions using Evennia's delay
    from evennia.utils import delay
    delay(grace, _transition_corpse, corpse.id, "open")
    delay(grace + open_period, _transition_corpse, corpse.id, "decayed")

    return corpse


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


def _move_room_loot_to_corpse(room, corpse, mob_name):
    """
    Move recently spawned loot items from room into corpse.

    Items dropped by at_death land in the room. We move items that
    are SoravelonItem instances (not exits, characters, etc.) that
    were just created (within last 2 seconds).
    """
    from typeclasses.objects import SoravelonItem

    for obj in list(room.contents):
        if isinstance(obj, SoravelonItem) and obj != corpse:
            # Heuristic: move items that aren't characters/rooms
            # Only move items that aren't locked to a specific owner
            obj.move_to(corpse, quiet=True)
