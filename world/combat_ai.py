"""
Mob combat AI for Soravelon.

Decides what ability a mob uses and who it targets during combat turns.
Supports weight-based ability selection, cooldown/condition filtering,
last-attacker targeting, and named mob scripted sequences at HP thresholds.

Every mob always has a basic attack fallback -- no infinite loops possible.
Call-for-help capped at 3 per encounter (Pitfall 2).

Functions return action dicts for CombatScript to dispatch -- this module
does NOT resolve damage directly.
"""

import random

# ---------------------------------------------------------------------------
# Condition vocabulary (from soravelon-mobs.md)
# ---------------------------------------------------------------------------
# Each entry maps a condition string to a callable(mob, target, combat_handler) -> bool.
# Unknown conditions return False (safe fallback).

CONDITION_CHECKS = {
    "target_below_50hp": lambda mob, target, ch: (
        target is not None
        and hasattr(target, "ndb")
        and getattr(target.ndb, "hp", 0)
        < _derive_target_max_hp(target) * 0.5
    ),
    "target_below_25hp": lambda mob, target, ch: (
        target is not None
        and hasattr(target, "ndb")
        and getattr(target.ndb, "hp", 0)
        < _derive_target_max_hp(target) * 0.25
    ),
    "self_below_50hp": lambda mob, target, ch: (
        getattr(mob.ndb, "hp", 0) < (mob.db.hp_max or 1) * 0.5
    ),
    "self_below_25hp": lambda mob, target, ch: (
        getattr(mob.ndb, "hp", 0) < (mob.db.hp_max or 1) * 0.25
    ),
    "target_has_poison": lambda mob, target, ch: _target_has_effect(target, "poison"),
    "target_has_bleed": lambda mob, target, ch: _target_has_effect(target, "bleed"),
    "target_has_burn": lambda mob, target, ch: _target_has_effect(target, "burn"),
    "no_allies_alive": lambda mob, target, ch: (
        len(_get_mob_combatants(ch, exclude=mob)) == 0
    ),
    "allies_present": lambda mob, target, ch: (
        len(_get_mob_combatants(ch, exclude=mob)) > 0
    ),
}

# Maximum call-for-help spawns per encounter (Pitfall 2)
CALL_FOR_HELP_CAP = 3


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _derive_target_max_hp(target):
    """Get max HP for a target. Players use derive_max_hp, mobs use db.hp_max."""
    if target.tags.get("character_type") == "player_character":
        from world.base_attributes import derive_max_hp
        return derive_max_hp(target)
    return target.db.hp_max or 1


def _target_has_effect(target, effect_type):
    """Check if target has a status effect active."""
    if target is None:
        return False
    from world.status_effects import has_effect
    return has_effect(target, effect_type)


def _get_mob_combatants(combat_handler, exclude=None):
    """Return list of mob combatants from combat handler, excluding one."""
    if combat_handler is None:
        return []
    mob_list = getattr(combat_handler.ndb, "mob_combatants", None) or []
    if exclude is None:
        return [m for m in mob_list if getattr(m.ndb, "hp", 0) > 0]
    return [
        m for m in mob_list
        if m != exclude and getattr(m.ndb, "hp", 0) > 0
    ]


def _get_player_combatants(combat_handler):
    """Return list of alive player combatants from combat handler."""
    if combat_handler is None:
        return []
    player_list = getattr(combat_handler.ndb, "player_combatants", None) or []
    return [p for p in player_list if getattr(p.ndb, "hp", 0) > 0]


def _is_on_cooldown(mob, ability_id):
    """Check if an ability is on cooldown for this mob."""
    cooldowns = getattr(mob.ndb, "ability_cooldowns", None) or {}
    return cooldowns.get(ability_id, 0) > 0


def _target_in_room(target, mob):
    """Check if target is in the same room as mob."""
    if target is None:
        return False
    return target.location == mob.location


def _has_vanish(target):
    """Check if target has vanish effect (untargetable for one round)."""
    from world.status_effects import has_effect
    return has_effect(target, "vanish")


# ---------------------------------------------------------------------------
# Condition checking
# ---------------------------------------------------------------------------

def check_condition(condition_str, mob, target, combat_handler):
    """
    Evaluate a condition string against current combat state.

    Args:
        condition_str: Condition key from CONDITION_CHECKS, or None (always passes).
        mob: The mob evaluating the condition.
        target: The mob's current target (may be None).
        combat_handler: The room's CombatScript.

    Returns:
        bool: True if condition is met, False otherwise.
    """
    if condition_str is None:
        return True
    checker = CONDITION_CHECKS.get(condition_str)
    if checker is None:
        # Unknown condition -- safe fallback per spec
        return False
    return checker(mob, target, combat_handler)


# ---------------------------------------------------------------------------
# Ability selection
# ---------------------------------------------------------------------------

def select_mob_action(mob, target, combat_handler):
    """
    Select an ability for the mob to use this turn.

    Filters mob.db.abilities by cooldown state and condition, then performs
    weighted random selection. Falls back to basic attack if no ability qualifies.

    Args:
        mob: The mob selecting an action.
        target: The mob's current target.
        combat_handler: The room's CombatScript.

    Returns:
        dict: Action dict with "type" field ("ability" or "basic_attack").
    """
    abilities = mob.db.abilities or []
    usable = []

    for ability in abilities:
        ability_id = ability.get("ability_id", "")
        if _is_on_cooldown(mob, ability_id):
            continue
        condition = ability.get("condition")
        if not check_condition(condition, mob, target, combat_handler):
            continue
        usable.append(ability)

    if not usable:
        return _make_basic_attack(mob)

    weights = [a.get("weight", 1) for a in usable]
    selected = random.choices(usable, weights=weights, k=1)[0]

    return {
        "type": "ability",
        "ability_id": selected.get("ability_id"),
        "element": selected.get("element", "physical"),
        "damage_base": selected.get("damage_base", 0),
        "status_effect": selected.get("status_effect"),
        "effect_duration": selected.get("effect_duration", 0),
        "effect_magnitude": selected.get("effect_magnitude", 0),
        "application_chance": selected.get("application_chance", 1.0),
        "cooldown": selected.get("cooldown", 0),
    }


def _make_basic_attack(mob):
    """
    Construct a basic attack action dict from mob's reference damage.

    Every mob always has a basic attack -- this is the fallback per Pitfall 7.
    Uses mob.db.ref_damage_min / ref_damage_max set at spawn by
    initialize_mob_combat_stats().
    """
    return {
        "type": "basic_attack",
        "element": "physical",
        "damage_min": mob.db.ref_damage_min or mob.db.damage_min or 5,
        "damage_max": mob.db.ref_damage_max or mob.db.damage_max or 10,
    }


# ---------------------------------------------------------------------------
# Targeting
# ---------------------------------------------------------------------------

def get_mob_target(mob, combat_handler):
    """
    Determine the mob's target for this turn.

    Priority order per soravelon-mobs.md:
    1. Last attacker (whoever most recently damaged this mob).
    2. Random valid player target in combat.
    3. None (no valid targets -- combat should end).

    Skips targets with "vanish" effect and targets that left the room.

    Args:
        mob: The mob selecting a target.
        combat_handler: The room's CombatScript.

    Returns:
        target or None: The selected target, or None if no valid targets.
    """
    players = _get_player_combatants(combat_handler)

    # Filter out vanished and out-of-room targets
    valid = [
        p for p in players
        if not _has_vanish(p) and _target_in_room(p, mob)
    ]

    if not valid:
        return None

    # Cognitive node: all mobs focus same target
    # Contract: CombatScript must set mob.ndb.current_target_id after get_mob_target() returns
    room = getattr(mob, "location", None)
    if room and hasattr(room, "tags") and room.tags.has("mob_coordination", category="node_effect"):
        mob_combatants = _get_mob_combatants(combat_handler)
        for other_mob in mob_combatants:
            if other_mob.id != mob.id:
                other_target_id = getattr(other_mob.ndb, "current_target_id", None)
                if other_target_id is not None:
                    for p in valid:
                        if p.id == other_target_id:
                            return p
        # If no other mob has a target yet, fall through to normal logic

    # Priority 1: last attacker
    last_attacker_id = getattr(mob.ndb, "last_attacker_id", None)
    if last_attacker_id is not None:
        for p in valid:
            if p.id == last_attacker_id:
                return p

    # Priority 2: random valid target
    return random.choice(valid)


# ---------------------------------------------------------------------------
# Scripted sequences (named mobs)
# ---------------------------------------------------------------------------

def check_scripted_sequence(mob, combat_handler):
    """
    Check if any scripted sequence triggers should fire for a named mob.

    Reads mob.db.scripted_sequence (list of dicts) and checks triggers against
    current combat state. Each trigger fires at most once per encounter,
    tracked via mob.ndb.fired_sequence_triggers set.

    Trigger types:
        - "combat_start": fires at round 1
        - "hp_below_X": fires when mob HP% drops below X
        - "round_N": fires on round N
        - "target_flees": fires when current target flees
        - "on_death": fires when mob reaches 0 HP

    Args:
        mob: The named mob with scripted sequences.
        combat_handler: The room's CombatScript.

    Returns:
        list[dict] or None: List of sequence actions to execute, or None.
    """
    sequences = mob.db.scripted_sequence or []
    if not sequences:
        return None

    # Initialize fired triggers set
    if getattr(mob.ndb, "fired_sequence_triggers", None) is None:
        mob.ndb.fired_sequence_triggers = set()
    fired = mob.ndb.fired_sequence_triggers

    current_round = getattr(combat_handler.ndb, "round_number", 1) if combat_handler else 1
    mob_hp = getattr(mob.ndb, "hp", 0)
    mob_hp_max = mob.db.hp_max or 1
    hp_pct = (mob_hp / mob_hp_max) * 100.0

    triggered_actions = []

    for entry in sequences:
        trigger = entry.get("trigger", "")
        trigger_key = entry.get("trigger_key", trigger)  # unique key for fire-once tracking
        actions = entry.get("actions", [])

        if trigger_key in fired:
            continue

        should_fire = False

        if trigger == "combat_start" and current_round == 1:
            should_fire = True
        elif trigger.startswith("hp_below_"):
            try:
                threshold = float(trigger.split("hp_below_")[1])
                if hp_pct < threshold:
                    should_fire = True
            except (ValueError, IndexError):
                pass
        elif trigger.startswith("round_"):
            try:
                target_round = int(trigger.split("round_")[1])
                if current_round == target_round:
                    should_fire = True
            except (ValueError, IndexError):
                pass
        elif trigger == "target_flees":
            # This trigger is checked externally when a player flees;
            # the combat handler sets mob.ndb.target_fled = True before calling
            if getattr(mob.ndb, "target_fled", False):
                should_fire = True
                mob.ndb.target_fled = False
        elif trigger == "on_death":
            if mob_hp <= 0:
                should_fire = True

        if should_fire:
            fired.add(trigger_key)
            triggered_actions.extend(actions)

    # Persist the updated set
    mob.ndb.fired_sequence_triggers = fired

    return triggered_actions if triggered_actions else None


def execute_sequence_action(action, mob, combat_handler):
    """
    Execute a single scripted sequence action.

    Action types:
        - "echo": Return text for room display.
        - "ability": Force mob to use a specific ability (bypass weight selection).
        - "spawn": Placeholder for mid-combat mob spawn.
        - "call_for_help": Find same-type mobs nearby and add to combat.
        - "modify_behavior": Change mob.db.base_aggression mid-combat.
        - "zone_echo": Send message to adjacent rooms.

    Args:
        action: Action dict with "type" and type-specific fields.
        mob: The mob executing the action.
        combat_handler: The room's CombatScript.

    Returns:
        dict: Result dict describing what happened, for CombatScript to process.
    """
    action_type = action.get("type", "echo")

    if action_type == "echo":
        return {
            "type": "echo",
            "text": action.get("text", ""),
        }

    elif action_type == "ability":
        # Force a specific ability, bypassing normal selection
        return {
            "type": "ability",
            "ability_id": action.get("ability_id"),
            "element": action.get("element", "physical"),
            "damage_base": action.get("damage_base", 0),
            "status_effect": action.get("status_effect"),
            "effect_duration": action.get("effect_duration", 0),
            "effect_magnitude": action.get("effect_magnitude", 0),
            "application_chance": action.get("application_chance", 1.0),
            "cooldown": action.get("cooldown", 0),
            "forced": True,
        }

    elif action_type == "spawn":
        # Placeholder -- CombatScript handles actual mob creation
        return {
            "type": "spawn",
            "mob_key": action.get("mob_key"),
            "count": action.get("count", 1),
        }

    elif action_type == "call_for_help":
        # Capped at CALL_FOR_HELP_CAP per encounter (Pitfall 2)
        help_count = getattr(combat_handler.ndb, "call_for_help_count", 0) if combat_handler else 0
        if help_count >= CALL_FOR_HELP_CAP:
            return {
                "type": "echo",
                "text": action.get("fail_text", ""),
            }
        # Increment counter
        if combat_handler:
            combat_handler.ndb.call_for_help_count = help_count + 1
        return {
            "type": "call_for_help",
            "mob_type": action.get("mob_type", mob.db.mob_type),
            "search_radius": action.get("search_radius", 3),
        }

    elif action_type == "modify_behavior":
        new_aggression = action.get("base_aggression")
        if new_aggression is not None:
            mob.db.base_aggression = new_aggression
        return {
            "type": "modify_behavior",
            "base_aggression": new_aggression,
        }

    elif action_type == "zone_echo":
        return {
            "type": "zone_echo",
            "text": action.get("text", ""),
            "radius": action.get("radius", 1),
        }

    # Unknown action type -- return echo with empty text
    return {"type": "echo", "text": ""}


# ---------------------------------------------------------------------------
# Flee behavior
# ---------------------------------------------------------------------------

def _should_flee(mob):
    """
    Check if mob should attempt to flee based on flee_low_hp behavior.

    Returns True if mob has flee behavior and HP is below threshold.
    """
    flee_config = mob.db.flee_low_hp or None
    if flee_config is None:
        return False
    threshold = flee_config if isinstance(flee_config, (int, float)) else 0.2
    mob_hp = getattr(mob.ndb, "hp", 0)
    mob_hp_max = mob.db.hp_max or 1
    hp_pct = mob_hp / mob_hp_max
    return hp_pct < threshold


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def process_mob_turn(mob, combat_handler):
    """
    Process a mob's full combat turn. Returns action list for CombatScript.

    Order:
    1. Check scripted sequences (may override normal action).
    2. Check flee behavior.
    3. Get target.
    4. Select action via weight-based ability selection.
    5. Return list of action dicts for CombatScript to dispatch.

    Does NOT resolve damage -- returns instruction dicts only.

    Args:
        mob: The mob taking a turn.
        combat_handler: The room's CombatScript managing this encounter.

    Returns:
        list[dict]: Action dicts for CombatScript to resolve.
    """
    actions = []

    # 1. Scripted sequences (named mobs)
    sequence_actions = check_scripted_sequence(mob, combat_handler)
    if sequence_actions:
        for seq_action in sequence_actions:
            result = execute_sequence_action(seq_action, mob, combat_handler)
            actions.append(result)
        # If any sequence action is an ability or spawn, that overrides normal turn
        has_combat_action = any(
            a.get("type") in ("ability", "spawn", "call_for_help")
            for a in actions
        )
        if has_combat_action:
            return actions

    # 2. Flee check
    if _should_flee(mob):
        actions.append({
            "type": "flee",
            "mob_id": mob.id,
        })
        return actions

    # 3. Targeting
    target = get_mob_target(mob, combat_handler)
    if target is None:
        # No valid targets -- combat should end
        return actions

    # 4. Action selection
    action = select_mob_action(mob, target, combat_handler)
    action["target_id"] = target.id
    actions.append(action)

    return actions
