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
    "evasion": {"evasion_bonus": 0.15},  # evasion buff (subterfuge builder)
    "fortify": {"damage_reduction": 0.15},  # 15% damage reduction (medic blessing)
    "vigor": {"damage_bonus": 0.15},  # 15% damage bonus (medic blessing)
    "warding": {"damage_reduction": 0.15},
    "silence": {"silenced": True},
    "frozen": {"skip_turn": True, "prevents_flee": True, "action_budget_penalty": 1},
    "stealth": {"stealthed": True, "evasion_bonus": 0.20},
    "accuracy": {"accuracy_bonus": 0.15},
    "damage_bonus": {"damage_bonus": 0.15},
    "damage_reduction": {"damage_reduction": 0.15},
    "group_damage_bonus": {"damage_bonus": 0.15},
    "group_damage_reduction": {"damage_reduction": 0.15},
    "damage_absorb": {"damage_absorb": 40},
    "damage_redirect": {"damage_absorb": 50},
    "resource_efficiency": {"resource_cost_reduction_pct": 0.25},
    "group_resource_regen": {"resource_regen_per_round": 5},
    "all_stats": {"all_stats": 0.10},
    "stat_boost": {"stat_multipliers": {}},
    "sustained_attack": {"damage_bonus": 0.20},
    "coordinated_strike": {},
    "companion_mode_change": {},
    "regeneration": {"heal_per_round": 15},
    "venom_coat": {},
    "guaranteed_crit": {},
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


def _find_effect(effects, effect_type):
    """Find an effect entry by type.

    Returns:
        (dict or None, int): (entry, index) or (None, -1) if not found.
    """
    for idx, entry in enumerate(effects):
        if entry["type"] == effect_type:
            return entry, idx
    return None, -1


def _copy_effect_data(data):
    """Return a shallow copy of effect metadata for safe storage."""
    if not data:
        return {}
    return dict(data)


def _build_effect_entry(effect_type, duration, magnitude, source_id, max_stacks, data=None, is_compound=False):
    """Build a normalized effect entry dict."""
    return {
        "type": effect_type,
        "stacks": 1,
        "duration": duration,
        "magnitude": magnitude,
        "source_id": source_id,
        "max_stacks": max_stacks,
        "is_compound": is_compound,
        "data": _copy_effect_data(data),
    }


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


def _resolve_effect_source(source_id):
    """Best-effort source object lookup for periodic effects."""
    if not source_id:
        return None
    try:
        import evennia
        results = evennia.search_object("#" + str(source_id))
        return results[0] if results else None
    except Exception:
        return None


def _numeric(value, default=0):
    """Return real numeric values and reject booleans or unsupported objects."""
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return value
    return default


def _get_max_hp(target):
    """Best-effort max HP lookup for players, mobs, and compatible combatants."""
    if getattr(target.db, "base_stats", None):
        try:
            from world.base_attributes import derive_max_hp
            return derive_max_hp(target)
        except Exception:
            pass

    for candidate in (
        getattr(target.ndb, "max_hp", None),
        getattr(target.db, "hp_max", None),
        getattr(target.db, "max_hp", None),
    ):
        resolved = _numeric(candidate, default=None)
        if resolved is not None and resolved > 0:
            return int(resolved)
    current_hp = _numeric(getattr(target.ndb, "hp", None), default=100)
    return max(1, int(current_hp))


def _heal_target(target, amount):
    """Heal a combatant up to their max HP and return the actual amount healed."""
    amount = int(_numeric(amount, 0))
    if amount <= 0:
        return 0

    max_hp = _get_max_hp(target)
    current_hp = int(_numeric(getattr(target.ndb, "hp", 0), 0))
    new_hp = min(max_hp, current_hp + amount)
    target.ndb.hp = new_hp
    return new_hp - current_hp


def _collect_periodic_allies(source):
    """Return same-room allies for periodic healing canopies and support effects."""
    if source is None:
        return []

    if getattr(source.db, "base_stats", None):
        leader_id = getattr(source.ndb, "group_leader_id", None)
        if leader_id:
            try:
                from world.group_engine import _get_group_members, _get_leader

                leader = _get_leader(source)
                if leader:
                    allies = []
                    for member in _get_group_members(leader):
                        if member and getattr(member, "location", None) == getattr(source, "location", None):
                            allies.append(member)
                    if allies:
                        return allies
            except Exception:
                pass
    return [source]


def _get_periodic_enemy_target(owner, preferred_id=None):
    """Resolve a live hostile target for autonomous periodic attacks."""
    handler = getattr(owner.ndb, "combat_handler", None)
    if not handler:
        return None

    if getattr(owner.db, "base_stats", None):
        candidates = [enemy for enemy in handler.get_mob_combatants() if enemy]
    else:
        candidates = [enemy for enemy in handler.get_player_combatants() if enemy]

    if preferred_id:
        for candidate in candidates:
            if getattr(candidate, "id", None) == preferred_id and _numeric(getattr(candidate.ndb, "hp", 1), 1) > 0:
                return candidate

    for candidate in candidates:
        if _numeric(getattr(candidate.ndb, "hp", 1), 1) > 0:
            return candidate
    return None


def _apply_periodic_attack(owner, entry):
    """Resolve a periodic autonomous strike from a lingering effect."""
    data = entry.get("data") or {}
    damage = int(_numeric(data.get("damage_per_round"), 0))
    if damage <= 0:
        return None

    target = _get_periodic_enemy_target(owner, preferred_id=data.get("periodic_target_id"))
    if target is None:
        return None

    ability = {
        "name": data.get("ability_name", entry["type"].replace("_", " ").title()),
        "effect_type": "damage",
        "scaling_primary": data.get("scaling_primary", "engineering"),
        "scaling_secondary": data.get("scaling_secondary"),
        "element": data.get("element", "physical"),
        "effect_params": {
            "damage_base": damage,
            "status_effect": data.get("status_effect"),
            "duration": data.get("status_duration", data.get("duration", 3)),
            "magnitude": data.get("status_magnitude", data.get("magnitude", 1.0)),
            "secondary_effects": list(data.get("secondary_effects", []) or []),
            "ignore_attack_buffs": True,
        },
    }

    try:
        from world.combat_engine import resolve_ability_damage

        ok, _, dealt = resolve_ability_damage(owner, ability, target)
        if ok:
            return target, dealt
    except Exception:
        return None
    return None


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def apply_effect(target, effect_type, duration, magnitude=1.0, source_id=None, data=None):
    """
    Apply a status effect to target.

    Args:
        target: Combatant (character or mob) with ndb.active_effects
        effect_type: Key into STACKABLE_EFFECTS or NON_STACKABLE_EFFECTS
        duration: Rounds the effect lasts
        magnitude: Power level (used for non-stackable replacement logic)
        source_id: dbref of the source combatant
        data: Optional effect-specific metadata (value, stats, absorb pool, etc.)

    Returns:
        (bool, str): Success flag and descriptive message.
    """
    if effect_type not in ALL_EFFECT_TYPES and effect_type not in COMPOUND_RESULT_TYPES:
        return (False, f"Unknown effect type: {effect_type}")

    if _has_immunity(target, effect_type):
        return (False, f"Immune to {effect_type}.")

    # Thermal node: wet status blocked in rooms with wet_suppressed tag
    if effect_type == "wet":
        room = getattr(target, "location", None)
        if room and hasattr(room, "tags") and room.tags.has("wet_suppressed", category="node_effect"):
            return (False, "The thermal distortion evaporates the moisture instantly.")

    effects = _get_effects(target)

    if effect_type in STACKABLE_EFFECTS:
        result = _apply_stackable(
            effects, effect_type, duration, magnitude, source_id, data=data
        )
    elif effect_type in NON_STACKABLE_EFFECTS:
        result = _apply_non_stackable(
            effects, effect_type, duration, magnitude, source_id, data=data
        )
    else:
        # Compound result type -- treat as non-stackable
        result = _apply_non_stackable(
            effects, effect_type, duration, magnitude, source_id, data=data
        )

    _save_effects(target, effects)

    # Check for compound triggers after application
    compounds_triggered = check_compound_triggers(target)

    msg = result[1]
    if compounds_triggered:
        msg += " " + ", ".join(f"{c} triggered!" for c in compounds_triggered)

    return (result[0], msg)


def _apply_stackable(effects, effect_type, duration, magnitude, source_id, data=None):
    """Apply or stack a stackable effect. Mutates effects list in place."""
    spec = STACKABLE_EFFECTS[effect_type]
    max_stacks = spec["max_stacks"]

    existing, _ = _find_effect(effects, effect_type)

    if existing:
        old_stacks = existing["stacks"]
        new_stacks = min(old_stacks + 1, max_stacks)
        existing["stacks"] = new_stacks
        existing["duration"] = max(existing["duration"], duration)
        existing["magnitude"] = max(existing["magnitude"], magnitude)
        if data:
            merged = dict(existing.get("data") or {})
            merged.update(data)
            existing["data"] = merged
        if new_stacks == old_stacks:
            return (True, f"{effect_type.capitalize()} refreshed ({new_stacks} stacks, max).")
        return (True, f"{effect_type.capitalize()} applied ({new_stacks} stacks).")
    else:
        effects.append(
            _build_effect_entry(
                effect_type,
                duration,
                magnitude,
                source_id,
                max_stacks,
                data=data,
            )
        )
        return (True, f"{effect_type.capitalize()} applied (1 stack).")


def _apply_non_stackable(effects, effect_type, duration, magnitude, source_id, data=None):
    """Apply or replace a non-stackable effect. Mutates effects list in place."""
    existing, existing_idx = _find_effect(effects, effect_type)

    if existing:
        if existing["magnitude"] >= magnitude:
            return (False, f"A stronger {effect_type} is already active.")
        # Replace weaker with stronger
        effects[existing_idx] = _build_effect_entry(
            effect_type,
            duration,
            magnitude,
            source_id,
            1,
            data=data,
        )
        return (True, f"{effect_type.capitalize()} replaced with stronger effect.")
    else:
        effects.append(
            _build_effect_entry(
                effect_type,
                duration,
                magnitude,
                source_id,
                1,
                data=data,
            )
        )
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
                "initial_duration": compound_duration,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": True,
                "data": {},
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
        data = entry.get("data") or {}

        # DoT damage for stackable damage effects
        if etype in ("poison", "bleed", "burn"):
            custom_tick = _numeric(data.get("damage_per_tick"), 0)
            if custom_tick > 0:
                damage = int(custom_tick)
            else:
                spec = STACKABLE_EFFECTS[etype]
                diminishing = spec["diminishing"]
                damage = sum(diminishing[:stacks])

            # Node effect modifiers on DoT damage
            room = getattr(target, "location", None)
            if room and hasattr(room, "tags"):
                # D-06: Thermal node doubles burn DoT
                if etype == "burn" and room.tags.has("burn_enhanced", category="node_effect"):
                    damage = damage * 2
                # D-08: Temporal node adds 50%-150% variance to all DoTs
                if room.tags.has("dot_tick_variance", category="node_effect"):
                    import random
                    variance = random.uniform(0.5, 1.5)
                    damage = int(damage * variance)

            current_hp = target.ndb.hp or 0
            target.ndb.hp = current_hp - damage
            messages.append(
                f"{etype.capitalize()} deals {damage} damage ({stacks} stacks)."
            )

            source = _resolve_effect_source(entry.get("source_id"))
            heal_source = int(_numeric(data.get("heal_source_per_round"), 0))
            if source and heal_source > 0:
                healed = _heal_target(source, heal_source)
                if healed > 0:
                    messages.append(f"{source.key} draws |g{healed}|n health from the lingering effect.")

            heal_allies = int(_numeric(data.get("heal_allies_per_round"), 0))
            if source and heal_allies > 0:
                total_healed = 0
                allies_healed = 0
                for ally in _collect_periodic_allies(source):
                    healed = _heal_target(ally, heal_allies)
                    if healed > 0:
                        allies_healed += 1
                        total_healed += healed
                if total_healed > 0:
                    messages.append(
                        f"{source.key}'s lingering canopy restores |g{total_healed}|n health across {allies_healed} allies."
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
            # Burst damage on first tick only (when duration equals initial_duration)
            initial = entry.get("initial_duration", entry["duration"])
            if entry["duration"] >= initial:
                max_hp = getattr(target.ndb, "max_hp", 100) or 100
                burst = max(1, int(max_hp * 0.15))
                current_hp = target.ndb.hp or 0
                target.ndb.hp = max(0, current_hp - burst)
                messages.append(f"Steam scalds for {burst} damage!")

        elif etype == "discharge":
            # Burst damage is percentage-based, applied once on creation tick
            # Subsequent ticks maintain the action penalty
            initial = entry.get("initial_duration", entry["duration"])
            if entry["duration"] >= initial:
                max_hp = getattr(target.ndb, "max_hp", 100) or 100
                burst = max(1, int(max_hp * 0.20))
                current_hp = target.ndb.hp or 0
                target.ndb.hp = max(0, current_hp - burst)
                messages.append(f"Electrical discharge deals {burst} damage!")

        periodic_heal = int(_numeric(data.get("heal_per_round"), 0))
        if periodic_heal > 0:
            healed = _heal_target(target, periodic_heal)
            if healed > 0:
                messages.append(f"{etype.capitalize()} restores |g{healed}|n health.")

        if etype == "sustained_attack" and _numeric(data.get("damage_per_round"), 0) > 0:
            source = _resolve_effect_source(entry.get("source_id")) or target
            strike = _apply_periodic_attack(source, entry)
            if strike is not None:
                enemy, damage = strike
                messages.append(f"{entry.get('data', {}).get('ability_name', etype.replace('_', ' ').title())} hits {enemy.key} for |r{damage}|n damage.")

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
        "damage_bonus": 0.0,
        "accuracy_bonus": 0.0,
        "evasion_bonus": 0.0,
        "silenced": False,
        "stealthed": False,
        "damage_absorb": 0,
        "reflect_percent": 0.0,
        "resource_cost_reduction_pct": 0.0,
        "resource_regen_per_round": 0,
        "stat_multipliers": {},
        "no_hostile_action": False,
    }

    effects = _get_effects(target)

    for entry in effects:
        etype = entry["type"]
        stacks = entry.get("stacks", 1)
        data = entry.get("data") or {}

        if etype == "slow":
            modifiers["action_budget_penalty"] += data.get("action_budget_penalty", NON_STACKABLE_EFFECTS["slow"]["action_budget_penalty"])
        elif etype == "shocked":
            modifiers["action_budget_penalty"] += data.get("action_budget_penalty", NON_STACKABLE_EFFECTS["shocked"]["action_budget_penalty"])
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
            modifiers["action_budget_bonus"] += int(data.get("action_budget_bonus", NON_STACKABLE_EFFECTS["haste"]["action_budget_bonus"]))
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
        elif etype == "fortify":
            reduction = data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["fortify"]["damage_reduction"]))
            modifiers["damage_reduction"] += reduction
        elif etype == "vigor":
            bonus = data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["vigor"]["damage_bonus"]))
            modifiers["damage_bonus"] += bonus
        elif etype == "warding":
            modifiers["damage_reduction"] += data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["warding"]["damage_reduction"]))
        elif etype in ("damage_reduction", "group_damage_reduction"):
            modifiers["damage_reduction"] += data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS[etype]["damage_reduction"]))
        elif etype in ("damage_bonus", "group_damage_bonus"):
            modifiers["damage_bonus"] += data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS[etype]["damage_bonus"]))
        elif etype == "accuracy":
            modifiers["accuracy_bonus"] += data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["accuracy"]["accuracy_bonus"]))
        elif etype == "evasion":
            modifiers["evasion_bonus"] += data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["evasion"]["evasion_bonus"]))
        elif etype == "silence":
            modifiers["silenced"] = True
        elif etype == "frozen":
            modifiers["skip_turn"] = True
            modifiers["prevents_flee"] = True
            modifiers["action_budget_penalty"] += data.get("action_budget_penalty", NON_STACKABLE_EFFECTS["frozen"]["action_budget_penalty"])
        elif etype == "stealth":
            modifiers["stealthed"] = True
            modifiers["evasion_bonus"] += data.get("evasion_bonus", NON_STACKABLE_EFFECTS["stealth"]["evasion_bonus"])
        elif etype == "damage_absorb":
            remaining = data.get("remaining", data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["damage_absorb"]["damage_absorb"])))
            modifiers["damage_absorb"] += int(remaining)
        elif etype == "damage_redirect":
            remaining = data.get("remaining", data.get("absorb", data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["damage_redirect"]["damage_absorb"]))))
            modifiers["damage_absorb"] += int(remaining)
        elif etype == "resource_efficiency":
            modifiers["resource_cost_reduction_pct"] += data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["resource_efficiency"]["resource_cost_reduction_pct"]))
        elif etype == "group_resource_regen":
            modifiers["resource_regen_per_round"] += int(data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["group_resource_regen"]["resource_regen_per_round"])))
        elif etype == "all_stats":
            boost = data.get("value", entry.get("magnitude", NON_STACKABLE_EFFECTS["all_stats"]["all_stats"]))
            for stat in ("strength", "agility", "endurance", "acuity", "mana", "presence", "resonance"):
                modifiers["stat_multipliers"][stat] = modifiers["stat_multipliers"].get(stat, 0.0) + boost
        elif etype == "stat_boost":
            for stat, boost in (data.get("stats") or {}).items():
                modifiers["stat_multipliers"][stat] = modifiers["stat_multipliers"].get(stat, 0.0) + boost
        elif etype == "sustained_attack":
            modifiers["damage_bonus"] += data.get("damage_bonus", entry.get("magnitude", NON_STACKABLE_EFFECTS["sustained_attack"]["damage_bonus"]))
        if data.get("reflect_percent"):
            modifiers["reflect_percent"] += data["reflect_percent"]

    modifiers["damage_reduction"] = min(modifiers["damage_reduction"], 0.80)
    return modifiers


def mitigate_incoming_damage(target, damage):
    """
    Consume absorb/redirect effects before HP loss.

    Returns:
        (int, int): (remaining_damage, absorbed_damage)
    """
    if damage <= 0:
        return 0, 0

    effects = _get_effects(target)
    if not effects:
        return damage, 0

    remaining = damage
    absorbed_total = 0
    changed = False

    for entry in effects:
        if entry["type"] not in ("damage_absorb", "damage_redirect"):
            continue
        data = dict(entry.get("data") or {})
        pool = int(
            data.get(
                "remaining",
                data.get(
                    "absorb",
                    data.get(
                        "value",
                        entry.get("magnitude", 0),
                    ),
                ),
            )
        )
        if pool <= 0:
            continue
        absorbed = min(pool, remaining)
        if absorbed <= 0:
            continue
        pool -= absorbed
        remaining -= absorbed
        absorbed_total += absorbed
        data["remaining"] = pool
        entry["data"] = data
        changed = True
        if pool <= 0:
            entry["duration"] = 0
        if remaining <= 0:
            break

    if changed:
        surviving = [entry for entry in effects if entry.get("duration", 1) > 0]
        _save_effects(target, surviving)

    return remaining, absorbed_total


def cleanse_one_negative_effect(target):
    """Remove one hostile effect from target and return its type, if any."""
    negative_priority = [
        "frozen", "stun", "charm", "silence", "blind", "root", "slow",
        "weaken", "shocked", "poison", "bleed", "burn", "drain",
        "petrify", "steam", "discharge", "corruption", "venom_lag",
    ]
    effects = _get_effects(target)
    for effect_type in negative_priority:
        entry, idx = _find_effect(effects, effect_type)
        if entry is not None:
            del effects[idx]
            _save_effects(target, effects)
            return effect_type
    return None


def consume_attack_effects(attacker, target=None, consume=True):
    """Return one-shot attack enhancers and optionally remove them from the attacker."""
    effects = _get_effects(attacker)
    payload = {
        "bonus_damage": 0,
        "damage_multiplier": 0.0,
        "guaranteed_crit": False,
        "status_effects": [],
    }
    surviving = []

    for entry in effects:
        etype = entry["type"]
        data = entry.get("data") or {}
        if etype == "venom_coat":
            payload["bonus_damage"] += int(_numeric(data.get("bonus_poison_damage"), 0))
            status_effect = data.get("status_effect")
            if status_effect:
                payload["status_effects"].append(
                    {
                        "effect_type": status_effect,
                        "duration": int(_numeric(data.get("duration"), 3)),
                        "magnitude": _numeric(data.get("magnitude"), 1.0),
                    }
                )
            if not consume:
                surviving.append(entry)
            continue
        if etype == "guaranteed_crit":
            payload["guaranteed_crit"] = True
            if not consume:
                surviving.append(entry)
            continue
        if etype == "coordinated_strike":
            if target and data.get("target_id") == target.id:
                payload["damage_multiplier"] += _numeric(
                    data.get("damage_bonus", entry.get("magnitude", 0.0))
                )
                if not consume:
                    surviving.append(entry)
                continue
        surviving.append(entry)

    if consume:
        _save_effects(attacker, surviving)
    return payload
