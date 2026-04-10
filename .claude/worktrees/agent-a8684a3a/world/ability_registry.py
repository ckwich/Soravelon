"""
Global data-driven ability registry.

ABILITIES dict keyed by ability_id, same constant-dict pattern as
GUILDS/SUBCLASSES in guild_engine.py. Phase 5a populates ~20 stub entries
for dispatcher validation; Phase 5b fills all 330 entries.

Derived lookups (DOMAIN_ABILITIES, SUBCLASS_SIGNATURES) are built at module
level from the ABILITIES dict -- no manual maintenance required.

Exports:
    EFFECT_TYPES, ABILITY_TIERS, ABILITIES,
    DOMAIN_ABILITIES, SUBCLASS_SIGNATURES, get_ability
"""

# ---------------------------------------------------------------------------
# Effect types -- all valid effect_type values for ability entries
# ---------------------------------------------------------------------------

EFFECT_TYPES = (
    "damage",
    "dot",
    "buff",
    "debuff",
    "utility",
    "social",
    "tactical",
    "compound_trigger",
    "heal",
    "status",
)

# ---------------------------------------------------------------------------
# Ability tiers -- GTS thresholds required to unlock each tier
# ---------------------------------------------------------------------------

ABILITY_TIERS = {
    1: 0,    # Available immediately on guild join
    2: 20,   # GTS >= 20
    3: 50,   # GTS >= 50
    4: 85,   # GTS >= 85
}

# ---------------------------------------------------------------------------
# ABILITIES -- keyed by ability_id string
#
# Each entry has 16 fields per D-09:
#   id, name, domain, tier, resource_cost, resource_type, cooldown,
#   charge_turns, effect_type, scaling_primary, scaling_secondary,
#   application_chance, description, room_flag_written, attuned_variants,
#   subclass_id
#
# Phase 5a: ~20 stub entries covering all 10 domains and all 10 effect types.
# Phase 5b: full 330 entries.
# ---------------------------------------------------------------------------

ABILITIES = {
    # -----------------------------------------------------------------------
    # Domain Tier 1 stubs -- one per domain (10 total)
    # -----------------------------------------------------------------------
    "momentum_strike": {
        "id": "momentum_strike",
        "name": "Momentum Strike",
        "domain": "combat",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "momentum",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Basic combat strike.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "shadow_read": {
        "id": "shadow_read",
        "name": "Shadow Read",
        "domain": "subterfuge",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "focus",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": "[STUB - Phase 5b] Read enemy defenses to expose weakness.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "wild_mend": {
        "id": "wild_mend",
        "name": "Wild Mend",
        "domain": "naturalism",
        "tier": 1,
        "resource_cost": 20,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Draw on natural balance to mend wounds.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "pulse_attune": {
        "id": "pulse_attune",
        "name": "Pulse Attune",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "resonance",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Attune to environmental resonance for combat edge.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "arcane_bolt": {
        "id": "arcane_bolt",
        "name": "Arcane Bolt",
        "domain": "arcana",
        "tier": 1,
        "resource_cost": 25,
        "resource_type": "mana",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Focused arcane energy bolt.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "diplomatic_leverage": {
        "id": "diplomatic_leverage",
        "name": "Diplomatic Leverage",
        "domain": "diplomacy",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "influence",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "social",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.9,
        "description": "[STUB - Phase 5b] Use leverage to shift encounter dynamics.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "reagent_toss": {
        "id": "reagent_toss",
        "name": "Reagent Toss",
        "domain": "alchemy",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "reagents",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.9,
        "description": "[STUB - Phase 5b] Toss a reactive compound that burns over time.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "command_rally": {
        "id": "command_rally",
        "name": "Command Rally",
        "domain": "tactics",
        "tier": 1,
        "resource_cost": 20,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "tactical",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Rally allies with tactical coordination.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "deploy_turret": {
        "id": "deploy_turret",
        "name": "Deploy Turret",
        "domain": "engineering",
        "tier": 1,
        "resource_cost": 30,
        "resource_type": "components",
        "cooldown": 5,
        "charge_turns": 1,
        "effect_type": "compound_trigger",
        "scaling_primary": "engineering",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Deploy a turret construct that fires automatically.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "echo_probe": {
        "id": "echo_probe",
        "name": "Echo Probe",
        "domain": "remnance",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "echoes",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "utility",
        "scaling_primary": "remnance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Probe echoes of past events for tactical insight.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    # -----------------------------------------------------------------------
    # Additional stubs to cover remaining effect types with variety
    # (damage, debuff, heal, buff, social, dot, tactical, compound_trigger,
    #  utility already covered above; need: status)
    # -----------------------------------------------------------------------
    "venom_coat": {
        "id": "venom_coat",
        "name": "Venom Coat",
        "domain": "alchemy",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "status",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": "[STUB - Phase 5b] Coat weapon with venom to apply poison status.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    "resonance_ward": {
        "id": "resonance_ward",
        "name": "Resonance Ward",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 20,
        "resource_type": "resonance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Attune a protective ward against incoming damage.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
    },
    # -----------------------------------------------------------------------
    # Subclass signature stubs -- bladestorm (combat + naturalism secondary)
    # -----------------------------------------------------------------------
    "bladestorm_sig1": {
        "id": "bladestorm_sig1",
        "name": "Tempest Cleave",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 40,
        "resource_type": "momentum",
        "cooldown": 4,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Bladestorm signature: nature-infused sweeping cleave.",
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "bladestorm",
    },
    "bladestorm_sig2": {
        "id": "bladestorm_sig2",
        "name": "Hurricane Stance",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 60,
        "resource_type": "momentum",
        "cooldown": 8,
        "charge_turns": 2,
        "effect_type": "compound_trigger",
        "scaling_primary": "combat",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": "[STUB - Phase 5b] Bladestorm capstone: channel the storm itself.",
        "room_flag_written": "bladestorm_hurricane",
        "attuned_variants": {},
        "subclass_id": "bladestorm",
    },
}

# ---------------------------------------------------------------------------
# Derived lookup: DOMAIN_ABILITIES -- {domain: {tier: [ability_ids]}}
# Built from ABILITIES, excluding subclass signatures.
# ---------------------------------------------------------------------------

DOMAIN_ABILITIES = {}
for _ability_id, _ability in ABILITIES.items():
    if _ability["subclass_id"] is not None:
        continue  # signatures are separate
    _domain = _ability["domain"]
    _tier = _ability["tier"]
    DOMAIN_ABILITIES.setdefault(_domain, {}).setdefault(_tier, []).append(
        _ability_id
    )

# ---------------------------------------------------------------------------
# Derived lookup: SUBCLASS_SIGNATURES -- {subclass_id: [ability_ids]}
# Built from ABILITIES, including only entries with subclass_id set.
# ---------------------------------------------------------------------------

SUBCLASS_SIGNATURES = {}
for _ability_id, _ability in ABILITIES.items():
    if _ability["subclass_id"]:
        _sc = _ability["subclass_id"]
        SUBCLASS_SIGNATURES.setdefault(_sc, []).append(_ability_id)

# Clean up loop variables from module namespace
del _ability_id, _ability, _domain, _tier, _sc


def get_ability(ability_id):
    """Look up an ability definition. Returns dict or None."""
    return ABILITIES.get(ability_id)
