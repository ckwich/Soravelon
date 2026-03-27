"""
Status effect system for combat.

Manages stackable and non-stackable effects, compound triggers,
per-round tick processing, and aggregated modifier queries.

All effect state lives on target.ndb.active_effects (volatile list of dicts).
Cleared at encounter end. Ticks down each combat round per D-11.

Effect entry schema:
    {
        "type": str,          # effect name key
        "stacks": int,        # 1 for non-stackable, 1-max for stackable
        "duration": int,      # rounds remaining
        "magnitude": float,   # power level (for non-stackable replacement logic)
        "source_id": int,     # dbref of source combatant
        "max_stacks": int,    # ceiling for stackable effects
        "is_compound": bool,  # True if created by compound trigger
    }

Functions return (bool, str) tuples per project convention where applicable.
SaverDict copy pattern used for all ndb.active_effects mutations.
"""

# ---------------------------------------------------------------------------
# Effect Constants (vault canonical per D-23 / D-25)
# ---------------------------------------------------------------------------

STACKABLE_EFFECTS = {
    "poison": {"max_stacks": 5, "base_damage": 8, "diminishing": [8, 5, 3, 2, 1]},
    "bleed": {"max_stacks": 4, "base_damage": 6, "diminishing": [6, 4, 3, 2]},
    "burn": {"max_stacks": 4, "base_damage": 7, "diminishing": [7, 5, 3, 2]},
    "weaken": {"max_stacks": 3, "reduction_per_stack": 0.08},
    "drain": {"max_stacks": 2, "drain_per_stack": 5},
}

NON_STACKABLE_EFFECTS = {
    "slow": {"action_budget_penalty": 1},
    "root": {"prevents_flee": True},
    "blind": {"miss_chance_increase": 0.25},
    "shocked": {"action_budget_penalty": 1},
    "stun": {"skip_turn": True},
    "charm": {"skip_turn": True, "no_hostile_action": True},
    "haste": {"action_budget_bonus": 1},
    "wet": {
        "burn_chance_reduction": 0.50,
        "burn_magnitude_reduction": 0.25,
        "action_penalty_on_apply": 1,
    },
}

# All known effect types for quick membership checks
ALL_EFFECT_TYPES = set(STACKABLE_EFFECTS) | set(NON_STACKABLE_EFFECTS)

# ---------------------------------------------------------------------------
# Compound Matrix (vault canonical per D-24)
# ---------------------------------------------------------------------------
# Keys stored in both orderings for O(1) lookup.

_BASE_COMPOUNDS = {
    # Additive: both source effects persist, compound effect added
    ("poison", "slow"): {
        "type": "additive",
        "result": "venom_lag",
        "effect": {"bonus_poison_damage": 4},
    },
    ("weaken", "poison"): {
        "type": "additive",
        "result": "corruption",
        "effect": {"poison_stack_ceiling_bonus": 1},
    },
    ("slow", "root"): {
        "type": "additive",
        "result": "petrify",
        "effect": {"extended_duration": 2, "breaks_on_damage": True},
    },
    # Consuming: both source effects removed, replaced by result
    ("burn", "wet"): {
        "type": "consuming",
        "result": "steam",
        "effect": {
            "burst_damage_pct": 0.75,
            "action_budget_penalty": 1,
            "armor_reduction_duration": 2,
        },
    },
    ("wet", "shocked"): {
        "type": "consuming",
        "result": "discharge",
        "effect": {
            "burst_damage_pct": 0.75,
            "action_penalty": -1,
            "action_penalty_duration": 2,
        },
    },
}

# Build bidirectional lookup
COMPOUND_MATRIX = {}
for (a, b), entry in _BASE_COMPOUNDS.items():
    COMPOUND_MATRIX[(a, b)] = entry
    COMPOUND_MATRIX[(b, a)] = entry

# Compound result types (not directly applied by players)
COMPOUND_RESULT_TYPES = {entry["result"] for entry in _BASE_COMPOUNDS.values()}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_effects(target):
    """Return the active effects list, initializing if needed."""
    effects = target.ndb.active_effects
    if effects is None:
        target.ndb.active_effects = []
        return []
    return effects


def _save_effects(target, effects):
    """Write back the effects list using SaverDict copy pattern."""
    target.ndb.active_effects = list(effects)


def _has_immunity(target, effect_type):
    """Check if target is immune to an effect type (mob immunity support)."""
    immunities = target.ndb.immunities if hasattr(target.ndb, "immunities") else None
    if immunities and effect_type in immunities:
        return True
    # Also check db.immunities for persistent mob config
    db_immunities = target.db.immunities or []
    if effect_type in db_immunities:
        return True
    return False


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def apply_effect(target, effect_type, duration, magnitude=1.0, source_id=None):
    """
    Apply a status effect to target.

    Args:
        target: Combatant (character or mob) with ndb.active_effects
        effect_type: Key into STACKABLE_EFFECTS or NON_STACKABLE_EFFECTS
        duration: Rounds the effect lasts
        magnitude: Power level (used for non-stackable replacement logic)
        source_id: dbref of the source combatant

    Returns:
        (bool, str): Success flag and descriptive message.
    """
    if effect_type not in ALL_EFFECT_TYPES and effect_type not in COMPOUND_RESULT_TYPES:
        return (False, f"Unknown effect type: {effect_type}")

    if _has_immunity(target, effect_type):
        return (False, f"Immune to {effect_type}.")

    effects = _get_effects(target)

    if effect_type in STACKABLE_EFFECTS:
        result = _apply_stackable(effects, effect_type, duration, magnitude, source_id)
    elif effect_type in NON_STACKABLE_EFFECTS:
        result = _apply_non_stackable(effects, effect_type, duration, magnitude, source_id)
    else:
        # Compound result type -- treat as non-stackable
        result = _apply_non_stackable(effects, effect_type, duration, magnitude, source_id)

    _save_effects(target, effects)

    # Check for compound triggers after application
    compounds_triggered = check_compound_triggers(target)

    msg = result[1]
    if compounds_triggered:
        msg += " " + ", ".join(f"{c} triggered!" for c in compounds_triggered)

    return (result[0], msg)


def _apply_stackable(effects, effect_type, duration, magnitude, source_id):
    """Apply or stack a stackable effect. Mutates effects list in place."""
    spec = STACKABLE_EFFECTS[effect_type]
    max_stacks = spec["max_stacks"]

    existing = None
    for entry in effects:
        if entry["type"] == effect_type:
            existing = entry
            break

    if existing:
        old_stacks = existing["stacks"]
        new_stacks = min(old_stacks + 1, max_stacks)
        existing["stacks"] = new_stacks
        existing["duration"] = max(existing["duration"], duration)
        existing["magnitude"] = max(existing["magnitude"], magnitude)
        if new_stacks == old_stacks:
            return (True, f"{effect_type.capitalize()} refreshed ({new_stacks} stacks, max).")
        return (True, f"{effect_type.capitalize()} applied ({new_stacks} stacks).")
    else:
        effects.append({
            "type": effect_type,
            "stacks": 1,
            "duration": duration,
            "magnitude": magnitude,
            "source_id": source_id,
            "max_stacks": max_stacks,
            "is_compound": False,
        })
        return (True, f"{effect_type.capitalize()} applied (1 stack).")


def _apply_non_stackable(effects, effect_type, duration, magnitude, source_id):
    """Apply or replace a non-stackable effect. Mutates effects list in place."""
    existing = None
    existing_idx = None
    for idx, entry in enumerate(effects):
        if entry["type"] == effect_type:
            existing = entry
            existing_idx = idx
            break

    if existing:
        if existing["magnitude"] >= magnitude:
            return (False, f"A stronger {effect_type} is already active.")
        # Replace weaker with stronger
        effects[existing_idx] = {
            "type": effect_type,
            "stacks": 1,
            "duration": duration,
            "magnitude": magnitude,
            "source_id": source_id,
            "max_stacks": 1,
            "is_compound": False,
        }
        return (True, f"{effect_type.capitalize()} replaced with stronger effect.")
    else:
        effects.append({
            "type": effect_type,
            "stacks": 1,
            "duration": duration,
            "magnitude": magnitude,
            "source_id": source_id,
            "max_stacks": 1,
            "is_compound": False,
        })
        return (True, f"{effect_type.capitalize()} applied.")


def remove_effect(target, effect_type):
    """
    Remove all entries of effect_type from target's active effects.

    Args:
        target: Combatant with ndb.active_effects
        effect_type: Effect key to remove
    """
    effects = _get_effects(target)
    new_effects = [e for e in effects if e["type"] != effect_type]
    _save_effects(target, new_effects)


def has_effect(target, effect_type):
    """
    Check if target has at least one active entry of the given effect type.

    Returns:
        bool: True if effect is present.
    """
    effects = _get_effects(target)
    return any(e["type"] == effect_type for e in effects)


def get_effect_stacks(target, effect_type):
    """
    Return current stack count for an effect.

    Returns:
        int: Stack count for stackable, 1 for non-stackable if present, 0 if absent.
    """
    effects = _get_effects(target)
    for e in effects:
        if e["type"] == effect_type:
            return e["stacks"]
    return 0


def check_compound_triggers(target):
    """
    Scan active effects for compound trigger pairs from COMPOUND_MATRIX.

    For additive compounds: keep both source effects, add compound effect.
    For consuming compounds: remove both sources, add compound result.

    Only triggers each compound once per call (tracked via set).

    Args:
        target: Combatant with ndb.active_effects

    Returns:
        list[str]: Names of compound results that triggered.
    """
    effects = _get_effects(target)
    active_types = {e["type"] for e in effects}
    triggered = []
    already_processed = set()

    for (a, b), compound in COMPOUND_MATRIX.items():
        # Normalize key to avoid double-processing (a,b) and (b,a)
        pair_key = tuple(sorted((a, b)))
        if pair_key in already_processed:
            continue

        if a in active_types and b in active_types:
            result_name = compound["result"]
            # Don't re-trigger if compound result already present
            if result_name in active_types:
                already_processed.add(pair_key)
                continue

            already_processed.add(pair_key)

            if compound["type"] == "consuming":
                # Remove both source effects
                effects = [e for e in effects if e["type"] not in (a, b)]
                active_types.discard(a)
                active_types.discard(b)

            # Add compound result entry
            compound_duration = 3  # default compound duration
            # Petrify gets extended duration from spec
            if "extended_duration" in compound["effect"]:
                compound_duration += compound["effect"]["extended_duration"]

            effects.append({
                "type": result_name,
                "stacks": 1,
                "duration": compound_duration,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": True,
            })
            active_types.add(result_name)
            triggered.append(result_name)

    _save_effects(target, effects)
    return triggered


def tick_effects(target):
    """
    Process all active effects for one combat round (called at round end per D-11).

    - DoT effects (poison, bleed, burn): deal diminishing damage based on stacks.
    - Drain: reduce stamina by drain_per_stack * stacks.
    - All effects: reduce duration by 1. Remove expired effects.
    - Petrify with breaks_on_damage: remove if target took damage this round.

    Args:
        target: Combatant with ndb.active_effects and ndb.hp / ndb.stamina

    Returns:
        list[str]: Combat log messages describing what happened.
    """
    effects = _get_effects(target)
    messages = []
    surviving = []

    for entry in effects:
        etype = entry["type"]
        stacks = entry.get("stacks", 1)

        # DoT damage for stackable damage effects
        if etype in ("poison", "bleed", "burn"):
            spec = STACKABLE_EFFECTS[etype]
            diminishing = spec["diminishing"]
            damage = sum(diminishing[:stacks])
            current_hp = target.ndb.hp or 0
            target.ndb.hp = current_hp - damage
            messages.append(
                f"{etype.capitalize()} deals {damage} damage ({stacks} stacks)."
            )

        # Drain reduces stamina
        elif etype == "drain":
            spec = STACKABLE_EFFECTS["drain"]
            drain_amount = spec["drain_per_stack"] * stacks
            current_stamina = target.ndb.stamina or 0
            target.ndb.stamina = max(0, current_stamina - drain_amount)
            messages.append(
                f"Drain saps {drain_amount} stamina ({stacks} stacks)."
            )

        # Petrify breaks on damage check
        elif etype == "petrify":
            took_damage = getattr(target.ndb, "took_damage_this_round", False)
            if took_damage:
                messages.append("Petrify shatters from damage!")
                continue  # skip adding to surviving -- effectively removed

        # Steam burst damage (consuming compound result)
        elif etype == "steam":
            # Burst damage is percentage-based, applied once on creation tick
            # Subsequent ticks just maintain the armor reduction / action penalty
            pass

        # Discharge burst damage (consuming compound: wet + shocked)
        elif etype == "discharge":
            # Burst damage is percentage-based, applied once on creation tick
            # Subsequent ticks maintain the action penalty
            pass

        # Decrement duration
        entry["duration"] -= 1
        if entry["duration"] <= 0:
            messages.append(f"{etype.capitalize()} fades.")
        else:
            surviving.append(entry)

    _save_effects(target, surviving)
    return messages


def clear_all_effects(target):
    """
    Remove all active effects from target. Called at encounter end per D-23.

    Args:
        target: Combatant with ndb.active_effects
    """
    target.ndb.active_effects = []


def get_effect_modifiers(target):
    """
    Return aggregated combat modifiers from all active effects.

    Called by combat engine when computing action budgets and checks.

    Args:
        target: Combatant with ndb.active_effects

    Returns:
        dict: Aggregated modifiers with keys:
            action_budget_penalty (int), action_budget_bonus (int),
            miss_chance_increase (float), skip_turn (bool),
            prevents_flee (bool), damage_reduction (float from weaken),
            no_hostile_action (bool)
    """
    modifiers = {
        "action_budget_penalty": 0,
        "action_budget_bonus": 0,
        "miss_chance_increase": 0.0,
        "skip_turn": False,
        "prevents_flee": False,
        "damage_reduction": 0.0,
        "no_hostile_action": False,
    }

    effects = _get_effects(target)

    for entry in effects:
        etype = entry["type"]
        stacks = entry.get("stacks", 1)

        if etype == "slow":
            modifiers["action_budget_penalty"] += NON_STACKABLE_EFFECTS["slow"]["action_budget_penalty"]
        elif etype == "shocked":
            modifiers["action_budget_penalty"] += NON_STACKABLE_EFFECTS["shocked"]["action_budget_penalty"]
        elif etype == "root":
            modifiers["prevents_flee"] = True
        elif etype == "blind":
            modifiers["miss_chance_increase"] += NON_STACKABLE_EFFECTS["blind"]["miss_chance_increase"]
        elif etype == "stun":
            modifiers["skip_turn"] = True
        elif etype == "charm":
            modifiers["skip_turn"] = True
            modifiers["no_hostile_action"] = True
        elif etype == "haste":
            modifiers["action_budget_bonus"] += NON_STACKABLE_EFFECTS["haste"]["action_budget_bonus"]
        elif etype == "weaken":
            spec = STACKABLE_EFFECTS["weaken"]
            modifiers["damage_reduction"] += spec["reduction_per_stack"] * stacks
        elif etype == "venom_lag":
            # Compound: adds bonus poison damage (handled in damage calc)
            pass
        elif etype == "petrify":
            # Compound: prevents flee + skip turn
            modifiers["prevents_flee"] = True
            modifiers["skip_turn"] = True
        elif etype == "steam":
            # Compound: action penalty
            modifiers["action_budget_penalty"] += 1
        elif etype == "discharge":
            # Compound: action penalty (wet + shocked)
            modifiers["action_budget_penalty"] += 1

    return modifiers
