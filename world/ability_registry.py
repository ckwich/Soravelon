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
    # ===================================================================
    # Non-combat / non-tactics domain stubs (kept from Phase 5a)
    # ===================================================================
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
    "deploy_turret": {
        "id": "deploy_turret",
        "name": "Deploy Turret",
        "domain": "engineering",
        "tier": 1,
        "resource_cost": 30,
        "resource_type": "components",
        "cooldown": 5,
        "charge_turns": 1,
        "effect_type": "damage",
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
    # ===================================================================
    # COMBAT DOMAIN POOL (15 abilities) -- resource_type: momentum
    # Fingerprint: PRESS -- sustained aggression, always moving forward
    # Scaling: combat -> strength
    # ===================================================================

    # --- Combat Tier 1 (4 abilities) -- Momentum builders, basic strikes ---
    "crushing_advance": {
        "id": "crushing_advance",
        "name": "Crushing Advance",
        "domain": "combat",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "momentum",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Drive forward with a heavy overhand strike. The simplest"
            " expression of Ironblood doctrine: never stop moving."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 35},
    },
    "break_guard": {
        "id": "break_guard",
        "name": "Break Guard",
        "domain": "combat",
        "tier": 1,
        "resource_cost": 12,
        "resource_type": "momentum",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "A sharp lateral blow aimed at breaking defensive posture."
            " The target's guard falters, leaving them exposed."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'debuff_type': 'weaken', 'duration': 2, 'magnitude': 0.1},
    },
    "press_the_line": {
        "id": "press_the_line",
        "name": "Press the Line",
        "domain": "combat",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "momentum",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Step into the opponent's space with a quick thrust."
            " Momentum builds fastest when you refuse to give ground."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 30},
    },
    "iron_resolve": {
        "id": "iron_resolve",
        "name": "Iron Resolve",
        "domain": "combat",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "momentum",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Steel yourself against the next blow. Endurance born from"
            " discipline, not magic. Reduces incoming damage briefly."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'warding', 'duration': 2, 'magnitude': 0.15},
    },

    # --- Combat Tier 2 (4 abilities) -- Core combat rhythm ---
    "rending_strike": {
        "id": "rending_strike",
        "name": "Rending Strike",
        "domain": "combat",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "momentum",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "A vicious tearing blow that opens wounds. The target"
            " bleeds freely -- pain is the cost of standing in your way."
        ),
        "room_flag_written": "bloodied",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 50, 'status_effect': 'bleed', 'duration': 3, 'magnitude': 1},
    },
    "brutal_charge": {
        "id": "brutal_charge",
        "name": "Brutal Charge",
        "domain": "combat",
        "tier": 2,
        "resource_cost": 18,
        "resource_type": "momentum",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Close distance with sudden violence. The impact carries"
            " your full weight -- hesitation is not an Ironblood virtue."
        ),
        "room_flag_written": "shattered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 60},
    },
    "shatter_bones": {
        "id": "shatter_bones",
        "name": "Shatter Bones",
        "domain": "combat",
        "tier": 2,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": (
            "Target a joint or limb with deliberate force. The target"
            " weakens visibly -- their movements become labored."
        ),
        "room_flag_written": "crushed",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'debuff_type': 'weaken', 'duration': 3, 'magnitude': 0.2},
    },
    "bloodhound_instinct": {
        "id": "bloodhound_instinct",
        "name": "Bloodhound Instinct",
        "domain": "combat",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "momentum",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "The veteran's sense for weakness. Heightened awareness"
            " sharpens your strikes -- the next several attacks find"
            " their mark with greater precision."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'haste', 'duration': 3, 'magnitude': 1.0},
    },

    # --- Combat Tier 3 (4 abilities) -- Advanced strikes, compound effects ---
    "rampage": {
        "id": "rampage",
        "name": "Rampage",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "momentum",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "A relentless sequence of strikes that targets every"
            " enemy in reach. The air fills with the sound of"
            " iron meeting flesh. Applies bleed to all hit."
        ),
        "room_flag_written": "bloodied",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 90, 'status_effect': 'bleed', 'duration': 3, 'magnitude': 1},
    },
    "pressure_break": {
        "id": "pressure_break",
        "name": "Pressure Break",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Channel accumulated momentum into a single devastating"
            " blow. Damage scales with current momentum -- the longer"
            " you have pressed, the harder this lands."
        ),
        "room_flag_written": "shattered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 100},
    },
    "iron_tempest": {
        "id": "iron_tempest",
        "name": "Iron Tempest",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "momentum",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Unleash a storm of steel in all directions. Deals heavy"
            " damage and applies weaken to every target struck. The"
            " ground shakes where you stand."
        ),
        "room_flag_written": "shattered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 100, 'status_effect': 'weaken', 'duration': 2, 'magnitude': 0.15},
    },
    "unyielding_advance": {
        "id": "unyielding_advance",
        "name": "Unyielding Advance",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "momentum",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Enter a state of relentless focus. For several rounds,"
            " incoming damage is reduced and each hit landed builds"
            " additional momentum. The Ironblood ideal made real."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'warding', 'duration': 3, 'magnitude': 0.2},
    },

    # --- Combat Tier 4 (3 abilities) -- Domain capstones ---
    "wrath_of_iron": {
        "id": "wrath_of_iron",
        "name": "Wrath of Iron",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "The Bloodsworn's ultimate expression. A single devastating"
            " strike that carries the weight of every blow landed in the"
            " encounter. Damage scales with total momentum spent this fight."
        ),
        "room_flag_written": "devastated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 200},
    },
    "break_the_world": {
        "id": "break_the_world",
        "name": "Break the World",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "momentum",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Slam weapon into the ground with catastrophic force."
            " Every enemy in the room staggers. Applies weaken and"
            " bleed simultaneously -- the kind of violence that"
            " leaves a mark on the world itself."
        ),
        "room_flag_written": "devastated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 180, 'status_effect': 'weaken', 'duration': 3, 'magnitude': 0.2},
    },
    "ironblood_fury": {
        "id": "ironblood_fury",
        "name": "Ironblood Fury",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Channel the full fury of the Ironblood tradition."
            " For a sustained duration, every attack deals bonus"
            " damage, generates double momentum, and basic strikes"
            " apply bleed. The debt paid in full."
        ),
        "room_flag_written": "bloodied",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'haste', 'duration': 4, 'magnitude': 1.5},
    },

    # ===================================================================
    # COMBAT-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets a Tier 3 enhanced blend + Tier 4 defining ability
    # ===================================================================

    # --- Duskblade (combat + subterfuge) ---
    "duskblade_shadow_strike": {
        "id": "duskblade_shadow_strike",
        "name": "Shadow Strike",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "momentum",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Slip into the target's blind spot and deliver a precise"
            " strike. Deals bonus damage when attacking from concealment."
            " The Duskblade's signature -- violence that arrives unseen."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "duskblade",
        "effect_params": {'damage_base': 90},
    },
    "duskblade_vanishing_edge": {
        "id": "duskblade_vanishing_edge",
        "name": "Vanishing Edge",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "momentum",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Vanish mid-combat and instantly re-enter with a guaranteed"
            " critical strike. The target never sees it coming -- one"
            " moment you are there, the next they are bleeding. The hit"
            " that justifies the name Duskblade."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "duskblade",
        "effect_params": {'damage_base': 200},
    },

    # --- Thornguard (combat + naturalism) ---
    "thornguard_living_armor": {
        "id": "thornguard_living_armor",
        "name": "Living Armor",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": (
            "Call upon the living magic in your blood to reinforce"
            " your body. Bark-like growths harden across your skin,"
            " absorbing incoming damage for several rounds."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "thornguard",
        "effect_params": {'buff_type': 'warding', 'duration': 3, 'magnitude': 0.25},
    },
    "thornguard_ironroot_bastion": {
        "id": "thornguard_ironroot_bastion",
        "name": "Ironroot Bastion",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": (
            "Roots erupt from beneath your feet, anchoring you as"
            " living wood encases your frame. Absorbs massive damage"
            " and reflects a portion back at melee attackers. You"
            " cannot move but you cannot be moved either."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "thornguard",
        "effect_params": {'buff_type': 'warding', 'duration': 4, 'magnitude': 0.4},
    },

    # --- Ruinborn (combat + resonance) ---
    "ruinborn_echostrike": {
        "id": "ruinborn_echostrike",
        "name": "Echostrike",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "resonance",
        "application_chance": 0.90,
        "description": (
            "Each strike leaves a resonance stack on the target."
            " The old magic hums through your weapon -- hits that"
            " shouldn't echo, do. At three stacks, the air crackles."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "ruinborn",
        "effect_params": {'damage_base': 80},
    },
    "ruinborn_node_burst": {
        "id": "ruinborn_node_burst",
        "name": "Node Burst",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "momentum",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "resonance",
        "application_chance": 1.0,
        "description": (
            "Detonate all resonance stacks on the target in a"
            " catastrophic burst. Damage scales with stacks consumed."
            " Every enemy in the room takes splash damage as node"
            " energy rips outward. Leaves the room charged."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "ruinborn",
        "effect_params": {'damage_base': 180},
    },

    # --- Spellbreaker (combat + arcana) ---
    "spellbreaker_mana_rend": {
        "id": "spellbreaker_mana_rend",
        "name": "Mana Rend",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "arcana",
        "application_chance": 0.85,
        "description": (
            "A strike designed to disrupt magical flow. Deals physical"
            " damage and drains the target's mana reserve. Mages learn"
            " to fear the sound of a Spellbreaker's blade."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {},
        "subclass_id": "spellbreaker",
        "effect_params": {'damage_base': 80, 'status_effect': 'silence', 'duration': 2, 'magnitude': 1.0},
    },
    "spellbreaker_null_field": {
        "id": "spellbreaker_null_field",
        "name": "Null Field",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "combat",
        "scaling_secondary": "arcana",
        "application_chance": 0.80,
        "description": (
            "Slam your weapon into the ground and shatter the local"
            " magical field. All enemies in the room are silenced --"
            " magical abilities fail for several rounds. The Circle"
            " of Wizards considers this technique barbaric."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {},
        "subclass_id": "spellbreaker",
        "effect_params": {'debuff_type': 'silence', 'duration': 3, 'magnitude': 1.0},
    },

    # --- Ironvoice (combat + diplomacy) ---
    "ironvoice_dread_presence": {
        "id": "ironvoice_dread_presence",
        "name": "Dread Presence",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "momentum",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "combat",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.80,
        "description": (
            "Your reputation precedes you. A single look accompanied"
            " by a low growl. The target's resolve falters -- weakened"
            " by the weight of your presence alone."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "ironvoice",
        "effect_params": {'debuff_type': 'weaken', 'duration': 2, 'magnitude': 0.15},
    },
    "ironvoice_warcry": {
        "id": "ironvoice_warcry",
        "name": "Warcry of the Ironblood",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "combat",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.85,
        "description": (
            "A shout that shakes the walls. Every enemy in the room"
            " is weakened and slowed. Allies feel their courage surge."
            " Presence scaling amplifies the effect -- the more feared"
            " you are, the louder the world hears you."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": "ironvoice",
        "effect_params": {'debuff_type': 'weaken', 'duration': 3, 'magnitude': 0.25},
    },

    # --- Ashfang (combat + alchemy) ---
    "ashfang_toxic_cleave": {
        "id": "ashfang_toxic_cleave",
        "name": "Toxic Cleave",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "alchemy",
        "application_chance": 0.85,
        "description": (
            "A wide sweeping cut with an envenomed blade. Every target"
            " struck receives both bleed and poison simultaneously."
            " The Ashfang way: coat everything in blood and venom."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "ashfang",
        "effect_params": {'damage_base': 85, 'status_effect': 'poison', 'duration': 3, 'magnitude': 8},
    },
    "ashfang_blood_frenzy": {
        "id": "ashfang_blood_frenzy",
        "name": "Blood Frenzy",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 40,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": "alchemy",
        "application_chance": 1.0,
        "description": (
            "Enter a state of chemical-fueled rage. For the duration,"
            " every melee attack applies double stacks of bleed and"
            " poison. Your weapon drips with something that should"
            " not exist naturally. Raw violence as delivery mechanism."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "ashfang",
        "effect_params": {'buff_type': 'haste', 'duration': 4, 'magnitude': 1.5},
    },

    # --- Vanguard (combat + tactics) ---
    "vanguard_shield_press": {
        "id": "vanguard_shield_press",
        "name": "Shield Press",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "tactical",
        "scaling_primary": "combat",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Step in front of an ally and absorb the next incoming"
            " attack. The absorbed damage converts to momentum."
            " Guard mechanics expressed through aggression -- the"
            " Vanguard protects by being the first target."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": "vanguard",
        "effect_params": {'tactical_action': 'group_buff', 'buff_type': 'warding', 'duration': 2, 'magnitude': 0.2},
    },
    "vanguard_formation_break": {
        "id": "vanguard_formation_break",
        "name": "Formation Break",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "momentum",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "tactics",
        "application_chance": 0.90,
        "description": (
            "Charge through the enemy line with devastating force."
            " Deals heavy AoE damage and grants the entire group"
            " a bonus action this round. The front of every"
            " formation -- the one who breaks lines."
        ),
        "room_flag_written": "shattered",
        "attuned_variants": {},
        "subclass_id": "vanguard",
        "effect_params": {'damage_base': 160, 'status_effect': 'weaken', 'duration': 2, 'magnitude': 0.15},
    },

    # --- Ironwright (combat + engineering) ---
    "ironwright_improvised_weapon": {
        "id": "ironwright_improvised_weapon",
        "name": "Improvised Weapon",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "momentum",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Forge a single-use weapon from battlefield debris in"
            " an instant. The improvised blade strikes with bonus"
            " damage and shatters on impact. Brutal and adaptive."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "ironwright",
        "effect_params": {'damage_base': 95},
    },
    "ironwright_masterwork_edge": {
        "id": "ironwright_masterwork_edge",
        "name": "Field-Forged Masterwork",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "momentum",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Craft a temporary weapon of exceptional quality mid-battle."
            " The masterwork blade persists for several rounds,"
            " granting bonus damage and a unique bleed effect on every"
            " hit. Engineering knowledge applied to pure violence."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "ironwright",
        "effect_params": {'damage_base': 180, 'status_effect': 'bleed', 'duration': 3, 'magnitude': 1},
    },

    # --- Dragonblooded (combat + remnance) ---
    "dragonblooded_ancient_resilience": {
        "id": "dragonblooded_ancient_resilience",
        "name": "Ancient Resilience",
        "domain": "combat",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "momentum",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "combat",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Something ancient stirs in your blood. Resistances"
            " surge beyond what a human body should withstand --"
            " scaling off resonance stat. Physical abilities that"
            " shouldn't exist."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "dragonblooded",
        "effect_params": {'buff_type': 'warding', 'duration': 3, 'magnitude': 0.3},
    },
    "dragonblooded_dragonfire_strike": {
        "id": "dragonblooded_dragonfire_strike",
        "name": "Dragonfire Strike",
        "domain": "combat",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "momentum",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "combat",
        "scaling_secondary": "remnance",
        "application_chance": 0.90,
        "description": (
            "Channel the fire that should have died a thousand years"
            " ago through your weapon. A massive strike wreathed in"
            " ancient flame. Applies burn and deals damage that"
            " scales off your resonance stat. Nobody can explain this."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": "dragonblooded",
        "effect_params": {'damage_base': 200, 'status_effect': 'burn', 'duration': 3, 'magnitude': 12},
    },

    # ===================================================================
    # TACTICS DOMAIN POOL (15 abilities) -- resource_type: command
    # Fingerprint: ORCHESTRATE -- group synergy, conducting the fight
    # Scaling: tactics -> acuity
    # ===================================================================

    # --- Tactics Tier 1 (4 abilities) -- Basic commands, group buffs ---
    "rally_the_line": {
        "id": "rally_the_line",
        "name": "Rally the Line",
        "domain": "tactics",
        "tier": 1,
        "resource_cost": 12,
        "resource_type": "command",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Issue a sharp command that steadies nearby allies."
            " Grants a minor damage bonus to the group for"
            " the next round. Solo, the effect applies to self."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'haste', 'duration': 2, 'magnitude': 1.0},
    },
    "direct_strike": {
        "id": "direct_strike",
        "name": "Direct Strike",
        "domain": "tactics",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "command",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A calculated strike aimed at a weak point identified"
            " through tactical observation. Precision over brute"
            " force -- acuity drives the damage."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 35},
    },
    "battlefield_assessment": {
        "id": "battlefield_assessment",
        "name": "Battlefield Assessment",
        "domain": "tactics",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "utility",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Read the battlefield with a practiced eye. Reveals"
            " enemy weaknesses and threat levels. Information is"
            " the first weapon of every commander."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'utility_action': 'reveal'},
    },
    "ordered_retreat": {
        "id": "ordered_retreat",
        "name": "Ordered Retreat",
        "domain": "tactics",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "tactical",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Command a disciplined withdrawal. All allies may"
            " disengage without provoking opportunity attacks."
            " The battle is won before the first blow -- sometimes"
            " winning means choosing when to leave."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'tactical_action': 'group_disengage'},
    },

    # --- Tactics Tier 2 (4 abilities) -- Core battlefield control ---
    "exploit_weakness": {
        "id": "exploit_weakness",
        "name": "Exploit Weakness",
        "domain": "tactics",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "command",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Identify and call out an enemy's defensive flaw."
            " The target takes increased damage from all sources"
            " for several rounds. Knowledge weaponized."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'debuff_type': 'weaken', 'duration': 3, 'magnitude': 0.15},
    },
    "coordinated_assault": {
        "id": "coordinated_assault",
        "name": "Coordinated Assault",
        "domain": "tactics",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "tactical",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Coordinate the group's next attack against a single"
            " target. Each ally's next action against the marked"
            " target deals bonus damage. Solo: self-buff equivalent."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'tactical_action': 'mark_target', 'duration': 2},
    },
    "suppressive_command": {
        "id": "suppressive_command",
        "name": "Suppressive Command",
        "domain": "tactics",
        "tier": 2,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": (
            "Bark orders that force the enemy into a defensive"
            " posture. The target is slowed, their action budget"
            " reduced by the weight of your tactical authority."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'debuff_type': 'slow', 'duration': 2, 'magnitude': 1.0},
    },
    "strategic_withdrawal": {
        "id": "strategic_withdrawal",
        "name": "Strategic Withdrawal",
        "domain": "tactics",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Reposition the group to a defensible stance. All"
            " allies gain damage reduction for the next round."
            " Sometimes the best offense is choosing your ground."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'warding', 'duration': 2, 'magnitude': 0.15},
    },

    # --- Tactics Tier 3 (4 abilities) -- Advanced coordination ---
    "overwhelming_force": {
        "id": "overwhelming_force",
        "name": "Overwhelming Force",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Direct every ally to strike the same target"
            " simultaneously. Each participant deals bonus damage"
            " and the target is staggered. Group size amplifies"
            " the effect -- the more you orchestrate, the harder"
            " this hits."
        ),
        "room_flag_written": "shattered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 90, 'status_effect': 'weaken', 'duration': 2, 'magnitude': 0.1},
    },
    "defensive_formation": {
        "id": "defensive_formation",
        "name": "Defensive Formation",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "command",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Arrange the group into an optimal defensive posture."
            " All allies gain significant damage reduction and"
            " resistance to status effects for several rounds."
            " The formation holds."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'warding', 'duration': 3, 'magnitude': 0.25},
    },
    "precision_strike_order": {
        "id": "precision_strike_order",
        "name": "Precision Strike Order",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Issue a precise attack command against a critical"
            " weak point. A single heavy strike guided by perfect"
            " tactical awareness. Acuity determines how deep the"
            " blade finds its mark."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'damage_base': 100},
    },
    "deny_ground": {
        "id": "deny_ground",
        "name": "Deny Ground",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Establish tactical dominance over the battlefield."
            " All enemies are rooted in place for a short duration"
            " -- they cannot flee while you hold the field."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'debuff_type': 'root', 'duration': 2, 'magnitude': 1.0},
    },

    # --- Tactics Tier 4 (3 abilities) -- Domain capstones ---
    "grand_stratagem": {
        "id": "grand_stratagem",
        "name": "Grand Stratagem",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Execute a masterwork tactical plan. All allies receive"
            " a bonus action, damage bonus, and damage reduction"
            " for the next two rounds. The Warchief's ultimate"
            " expression: everyone fights better when you are"
            " conducting the battle."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'buff_type': 'haste', 'duration': 2, 'magnitude': 1.5},
    },
    "break_their_will": {
        "id": "break_their_will",
        "name": "Break Their Will",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "command",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Shatter enemy morale through overwhelming tactical"
            " superiority. All enemies are weakened and slowed."
            " Some may break entirely and flee. The battle was"
            " won before the first blow."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'debuff_type': 'weaken', 'duration': 3, 'magnitude': 0.25},
    },
    "commanders_gambit": {
        "id": "commanders_gambit",
        "name": "Commander's Gambit",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "tactical",
        "scaling_primary": "tactics",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Sacrifice your own action budget to grant every ally"
            " two bonus actions this round. The commander who sees"
            " the whole board knows when to step back and let"
            " others deliver the killing blow. Ceremony."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {'tactical_action': 'sacrifice_actions', 'bonus_actions': 2},
    },

    # ===================================================================
    # TACTICS-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # ===================================================================

    # --- Warbringer (tactics + combat) ---
    "warbringer_commanding_charge": {
        "id": "warbringer_commanding_charge",
        "name": "Commanding Charge",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Lead from the front with a charge that builds command"
            " and deals damage. Allies who follow gain a damage"
            " bonus. The Warbringer's paradox: aggression that"
            " creates order."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": "warbringer",
        "effect_params": {'damage_base': 85},
    },
    "warbringer_warfront": {
        "id": "warbringer_warfront",
        "name": "Warfront",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Establish a sustained combat zone. For several rounds,"
            " all allies in the room deal bonus damage, gain damage"
            " reduction, and generate bonus action budget. You"
            " absorb hits meant for others. First in, last out."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": "warbringer",
        "effect_params": {'buff_type': 'warding', 'duration': 4, 'magnitude': 0.25},
    },

    # --- Greycommand (tactics + subterfuge) ---
    "greycommand_intelligence_report": {
        "id": "greycommand_intelligence_report",
        "name": "Intelligence Report",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "utility",
        "scaling_primary": "tactics",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Deploy covert observation to reveal enemy ability"
            " cooldowns, health thresholds, and planned actions."
            " For the next two rounds, the group can see what is"
            " coming. Information warfare at its finest."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "greycommand",
        "effect_params": {'utility_action': 'reveal'},
    },
    "greycommand_shadow_operation": {
        "id": "greycommand_shadow_operation",
        "name": "Shadow Operation",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Cloak the entire group in tactical concealment. All"
            " allies gain stealth for one round and their next"
            " attack is treated as an ambush -- guaranteed critical"
            " strike. The special operation executed flawlessly."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "greycommand",
        "effect_params": {'buff_type': 'haste', 'duration': 1, 'magnitude': 2.0},
    },

    # --- Wildtactician (tactics + naturalism) ---
    "wildtactician_terrain_control": {
        "id": "wildtactician_terrain_control",
        "name": "Terrain Control",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "tactics",
        "scaling_secondary": "naturalism",
        "application_chance": 0.80,
        "description": (
            "Command the natural terrain to impede enemy movement."
            " Roots and undergrowth entangle all enemies, rooting"
            " them in place. The forest is your army when you"
            " know how to give it orders."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "wildtactician",
        "effect_params": {'debuff_type': 'root', 'duration': 2, 'magnitude': 1.0},
    },
    "wildtactician_beast_assault": {
        "id": "wildtactician_beast_assault",
        "name": "Beast Assault",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "command",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": "naturalism",
        "application_chance": 0.90,
        "description": (
            "Call a wave of local predators to assault the enemy."
            " Multiple targets take heavy damage as beasts strike"
            " from every direction. Tactical damage delivered"
            " through the wilderness itself."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": "wildtactician",
        "effect_params": {'damage_base': 160},
    },

    # --- Nodewarden (tactics + resonance) ---
    "nodewarden_resonant_manipulation": {
        "id": "nodewarden_resonant_manipulation",
        "name": "Resonant Manipulation",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "tactical",
        "scaling_primary": "tactics",
        "scaling_secondary": "resonance",
        "application_chance": 0.85,
        "description": (
            "Manipulate local node energy to create a tactical"
            " advantage. Write a resonant flag to the room that"
            " amplifies ally abilities and disrupts enemy casting."
            " Scholar tactical awareness made dangerous."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {},
        "subclass_id": "nodewarden",
        "effect_params": {'tactical_action': 'group_buff', 'buff_type': 'haste', 'duration': 2, 'magnitude': 1.0},
    },
    "nodewarden_node_weaponization": {
        "id": "nodewarden_node_weaponization",
        "name": "Node Weaponization",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": "resonance",
        "application_chance": 0.90,
        "description": (
            "Weaponize the local node infrastructure. Massive area"
            " damage as node energy is discharged through the room."
            " Every enemy is struck and the room becomes charged"
            " with residual energy. Not gentle scholarship."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "nodewarden",
        "effect_params": {'damage_base': 180},
    },

    # --- Siegecaller (tactics + arcana) ---
    "siegecaller_arcane_barrage": {
        "id": "siegecaller_arcane_barrage",
        "name": "Arcane Barrage",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": "arcana",
        "application_chance": 1.0,
        "description": (
            "Direct a barrage of arcane projectiles at a target"
            " area. Ranged damage that bypasses front-line"
            " defenses. Magical artillery placed exactly where"
            " the commander needs it."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": "siegecaller",
        "effect_params": {'damage_base': 90},
    },
    "siegecaller_siege_spell": {
        "id": "siegecaller_siege_spell",
        "name": "Siege Spell",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "tactics",
        "scaling_secondary": "arcana",
        "application_chance": 1.0,
        "description": (
            "Call down a delayed magical bombardment. Two rounds"
            " of channeling, then devastating area damage to all"
            " enemies. The longest charge in the Warcraft guild"
            " -- but when it lands, battlefields end."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": "siegecaller",
        "effect_params": {'damage_base': 250},
    },

    # --- Warlord (tactics + diplomacy) ---
    "warlord_rally_cry": {
        "id": "warlord_rally_cry",
        "name": "Rally Cry",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "diplomacy",
        "application_chance": 1.0,
        "description": (
            "Inspire the group with a commanding shout. All allies"
            " gain a damage bonus and resistance to fear effects."
            " Presence scaling amplifies the buff -- the more"
            " commanding you are, the harder your people fight."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "warlord",
        "effect_params": {'buff_type': 'haste', 'duration': 3, 'magnitude': 1.5},
    },
    "warlord_sovereign_command": {
        "id": "warlord_sovereign_command",
        "name": "Sovereign Command",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "tactics",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.75,
        "description": (
            "Issue a command so absolute that enemies obey. All"
            " enemies in the room are charmed for one round --"
            " they skip their turn, unable to act against the"
            " weight of your authority. Morale IS the battlefield."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": "warlord",
        "effect_params": {'debuff_type': 'charm', 'duration': 1, 'magnitude': 1.0},
    },

    # --- Siegemaster (tactics + alchemy) ---
    "siegemaster_chemical_barrage": {
        "id": "siegemaster_chemical_barrage",
        "name": "Chemical Barrage",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "tactics",
        "scaling_secondary": "alchemy",
        "application_chance": 0.85,
        "description": (
            "Lob chemical compounds across the battlefield. All"
            " enemies receive poison over time. Area denial through"
            " tactical toxicology -- the Siegemaster's bread and butter."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "siegemaster",
        "effect_params": {'status_effect': 'poison', 'duration': 4, 'magnitude': 10},
    },
    "siegemaster_plague_zone": {
        "id": "siegemaster_plague_zone",
        "name": "Plague Zone",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "tactics",
        "scaling_secondary": "alchemy",
        "application_chance": 0.80,
        "description": (
            "Saturate the room with persistent chemical agents."
            " Every enemy receives poison and slow for multiple"
            " rounds. The air itself becomes a weapon -- sustained"
            " area denial that makes the room a killing ground."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "siegemaster",
        "effect_params": {'status_effect': 'poison', 'duration': 5, 'magnitude': 15},
    },

    # --- Fieldwright (tactics + engineering) ---
    "fieldwright_deploy_barricade": {
        "id": "fieldwright_deploy_barricade",
        "name": "Deploy Barricade",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Rapidly construct a field barricade. All allies gain"
            " significant damage reduction from ranged attacks."
            " Combat construction that changes how the group"
            " experiences incoming fire."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": "fieldwright",
        "effect_params": {'buff_type': 'warding', 'duration': 3, 'magnitude': 0.25},
    },
    "fieldwright_field_fortress": {
        "id": "fieldwright_field_fortress",
        "name": "Field Fortress",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Erect a sustained fortification that transforms the"
            " battlefield. Allies gain heavy damage reduction,"
            " enemies are slowed entering the zone, and the"
            " structure persists for multiple rounds. The ultimate"
            " expression of tactical engineering."
        ),
        "room_flag_written": "fortified",
        "attuned_variants": {},
        "subclass_id": "fieldwright",
        "effect_params": {'buff_type': 'warding', 'duration': 4, 'magnitude': 0.35},
    },

    # --- Oathbreaker (tactics + remnance) ---
    "oathbreaker_ancient_formation": {
        "id": "oathbreaker_ancient_formation",
        "name": "Ancient Formation",
        "domain": "tactics",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "command",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Arrange the group according to pre-curse battle"
            " doctrine. Formations nobody else remembers."
            " All allies gain damage bonus and damage reduction"
            " from knowledge a thousand years buried."
        ),
        "room_flag_written": "ancient_ground",
        "attuned_variants": {},
        "subclass_id": "oathbreaker",
        "effect_params": {'buff_type': 'warding', 'duration': 3, 'magnitude': 0.2},
    },
    "oathbreaker_forgotten_doctrine": {
        "id": "oathbreaker_forgotten_doctrine",
        "name": "Forgotten Doctrine",
        "domain": "tactics",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "command",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "tactics",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Execute a tactical maneuver from before the Dragon"
            " Curse. All allies gain haste and a bonus action."
            " All enemies are weakened. The doctrine was forbidden"
            " for a reason -- it works too well. Echoes amplify"
            " the effect."
        ),
        "room_flag_written": "ancient_ground",
        "attuned_variants": {},
        "subclass_id": "oathbreaker",
        "effect_params": {'buff_type': 'haste', 'duration': 3, 'magnitude': 1.5},
    },

    # ===================================================================
    # SUBTERFUGE DOMAIN POOL (15 abilities) -- resource_type: focus
    # Fingerprint: READ -- timing, pattern recognition, patience rewarded
    # Scaling: subterfuge -> agility
    # ===================================================================

    # --- Subterfuge Tier 1 (4 abilities) -- Reads, opening strikes, debuffs ---
    "expose_weakness": {
        "id": "expose_weakness",
        "name": "Expose Weakness",
        "domain": "subterfuge",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "focus",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Read the target's guard and exploit the gap. A precise"
            " strike that leaves the target exposed -- the opening"
            " move of every Veilcraft chain."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 2, "magnitude": 0.1},
    },
    "probing_strike": {
        "id": "probing_strike",
        "name": "Probing Strike",
        "domain": "subterfuge",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "focus",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A quick testing strike that reads the target's rhythm."
            " Deals light damage and builds Focus -- the patient"
            " opening before the chain begins."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 30},
    },
    "shadow_step": {
        "id": "shadow_step",
        "name": "Shadow Step",
        "domain": "subterfuge",
        "tier": 1,
        "resource_cost": 12,
        "resource_type": "focus",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Slip into the target's peripheral vision. Grants a"
            " brief evasion bonus -- you are harder to hit when"
            " you are already reading their next move."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "evasion", "duration": 2, "magnitude": 0.15},
    },
    "nerve_strike": {
        "id": "nerve_strike",
        "name": "Nerve Strike",
        "domain": "subterfuge",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Target a nerve cluster identified through careful"
            " observation. The target's movements slow -- pain"
            " and confusion buy you time."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "slow", "duration": 2, "magnitude": 1.0},
    },

    # --- Subterfuge Tier 2 (4 abilities) -- Core combo abilities ---
    "exploit_opening": {
        "id": "exploit_opening",
        "name": "Exploit Opening",
        "domain": "subterfuge",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "focus",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Strike during the guard window your patience revealed."
            " Deals bonus damage when the target is already debuffed."
            " The reward for reading correctly."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 55},
    },
    "calculated_wound": {
        "id": "calculated_wound",
        "name": "Calculated Wound",
        "domain": "subterfuge",
        "tier": 2,
        "resource_cost": 18,
        "resource_type": "focus",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Place a precise cut that bleeds freely. Not brute force"
            " -- surgical accuracy. The wound worsens as the target"
            " moves, punishing aggression."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 50, "status_effect": "bleed", "duration": 3, "magnitude": 1},
    },
    "feint_and_punish": {
        "id": "feint_and_punish",
        "name": "Feint and Punish",
        "domain": "subterfuge",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "focus",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Draw the target's guard one direction and strike the"
            " other. The feint itself is the weapon -- their"
            " correction exposes them further."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 60},
    },
    "apply_pressure": {
        "id": "apply_pressure",
        "name": "Apply Pressure",
        "domain": "subterfuge",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Stack accumulated reads into sustained pressure. The"
            " target weakens under the weight of knowing you have"
            " seen every opening they offer."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.15},
    },

    # --- Subterfuge Tier 3 (4 abilities) -- Advanced debuffs, chain abilities ---
    "blinding_dust": {
        "id": "blinding_dust",
        "name": "Blinding Dust",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Throw a handful of prepared dust into the target's eyes."
            " Blinded enemies miss more often and cannot read your"
            " movements. The world goes dark for them."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "blind", "duration": 2, "magnitude": 1.0},
    },
    "shadow_chain": {
        "id": "shadow_chain",
        "name": "Shadow Chain",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A rapid sequence of strikes that each build on the"
            " last. Each hit in the chain deals escalating damage."
            " The reward for long, disciplined timing windows."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 90},
    },
    "crippling_poison": {
        "id": "crippling_poison",
        "name": "Crippling Poison",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "focus",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Apply a fast-acting toxin to the target through a"
            " concealed blade. The poison weakens and slows --"
            " two debuffs delivered in a single read."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "poison", "duration": 3, "magnitude": 8},
    },
    "vanishing_strike": {
        "id": "vanishing_strike",
        "name": "Vanishing Strike",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Strike and immediately slip from sight. Deals heavy"
            " damage and grants a brief evasion buff. The target"
            " recoils from a blade they never saw retract."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 100},
    },

    # --- Subterfuge Tier 4 (3 abilities) -- Domain capstones ---
    "death_of_a_thousand_reads": {
        "id": "death_of_a_thousand_reads",
        "name": "Death of a Thousand Reads",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "focus",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Every weakness you have catalogued resolves into a"
            " single devastating chain. Damage scales with debuffs"
            " active on the target. The patient reward -- a kill"
            " built from observation, not brute force."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 180},
    },
    "perfect_read": {
        "id": "perfect_read",
        "name": "Perfect Read",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "You see everything. The target's rhythm, guard, and"
            " intent laid bare. Applies blind and weaken simultaneously"
            " -- the target's confidence collapses as they realize"
            " you have read every move they will ever make."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "blind", "duration": 3, "magnitude": 1.5},
    },
    "phantom_execution": {
        "id": "phantom_execution",
        "name": "Phantom Execution",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "The Unseen's ultimate expression. A single lethal"
            " strike that arrives from nowhere. Guaranteed critical"
            " against blinded or weakened targets. The culmination"
            " of a Veilcraft master's patience."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 220},
    },

    # ===================================================================
    # SUBTERFUGE-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets a Tier 3 enhanced blend + Tier 4 defining ability
    # ===================================================================

    # --- Grimwarden (subterfuge + combat) ---
    "grimwarden_ambush_strike": {
        "id": "grimwarden_ambush_strike",
        "name": "Ambush Strike",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Erupt from concealment with overwhelming force. No"
            " finesse -- raw violence delivered from an unexpected"
            " angle. Deals massive bonus damage from stealth."
            " The Grimwarden method: patience followed by brutality."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "grimwarden",
        "effect_params": {"damage_base": 110},
    },
    "grimwarden_death_from_shadows": {
        "id": "grimwarden_death_from_shadows",
        "name": "Death from Shadows",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "The execution strike. If the target is below 30 percent"
            " health, this is a guaranteed kill. Above that threshold,"
            " it deals devastating damage and applies bleed. Stealth"
            " re-entry resets all cooldowns. The brutal assassin."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "grimwarden",
        "effect_params": {"damage_base": 200, "status_effect": "bleed", "duration": 3, "magnitude": 1},
    },

    # --- Hollowstep (subterfuge + naturalism) ---
    "hollowstep_terrain_trap": {
        "id": "hollowstep_terrain_trap",
        "name": "Terrain Trap",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "naturalism",
        "application_chance": 0.85,
        "description": (
            "Use the natural terrain against the target. Roots erupt"
            " from concealed positions, dealing damage and pinning"
            " the target in place. The wilderness itself is your weapon."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "hollowstep",
        "effect_params": {"damage_base": 80, "status_effect": "root", "duration": 2, "magnitude": 1.0},
    },
    "hollowstep_wilderness_ghost": {
        "id": "hollowstep_wilderness_ghost",
        "name": "Wilderness Ghost",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 40,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": (
            "Become one with the wilderness. Sustained outdoor stealth"
            " with heightened evasion. Attacks from this state deal"
            " bonus damage and do not break concealment. The ghost"
            " that tracks, vanishes, and uses terrain as a weapon."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "hollowstep",
        "effect_params": {"buff_type": "evasion", "duration": 4, "magnitude": 0.3},
    },

    # --- Veilreader (subterfuge + resonance) ---
    "veilreader_read_intent": {
        "id": "veilreader_read_intent",
        "name": "Read Intent",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "resonance",
        "application_chance": 0.90,
        "description": (
            "Read the target's magical signature to predict their"
            " next action. The target's next ability is telegraphed"
            " to all allies. Grants evasion against the predicted"
            " attack. Knowledge is the Veilreader's weapon."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "veilreader",
        "effect_params": {"debuff_type": "weaken", "duration": 2, "magnitude": 0.15},
    },
    "veilreader_precognition_field": {
        "id": "veilreader_precognition_field",
        "name": "Precognition Field",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "resonance",
        "application_chance": 1.0,
        "description": (
            "Extend your ability to read magical signatures to"
            " the entire group. All allies gain enhanced dodge"
            " for several rounds. The Veilreader sees every"
            " blow before it lands -- and shares the vision."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "veilreader",
        "effect_params": {"buff_type": "evasion", "duration": 3, "magnitude": 0.25},
    },

    # --- Nullshadow (subterfuge + arcana) ---
    "nullshadow_shadow_spell": {
        "id": "nullshadow_shadow_spell",
        "name": "Shadow Spell",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "arcana",
        "application_chance": 1.0,
        "description": (
            "Cast a spell wrapped in shadow. Deals magical damage"
            " from stealth without breaking concealment. The target"
            " never sees the source. Magic that arrives unseen."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "nullshadow",
        "effect_params": {"damage_base": 90},
    },
    "nullshadow_void_cloak": {
        "id": "nullshadow_void_cloak",
        "name": "Void Cloak",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "arcana",
        "application_chance": 1.0,
        "description": (
            "Wrap yourself in a cloak of magical shadow. For the"
            " duration, all abilities can be used from stealth"
            " without breaking it. The Nullshadow's defining"
            " power -- invisible spellcasting."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "nullshadow",
        "effect_params": {"buff_type": "stealth", "duration": 4, "magnitude": 1.0},
    },

    # --- Tally Agent (subterfuge + diplomacy) ---
    "tally_agent_intelligence_leak": {
        "id": "tally_agent_intelligence_leak",
        "name": "Intelligence Leak",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.85,
        "description": (
            "Feed false information to the target through social"
            " manipulation. The target's next ability has reduced"
            " effectiveness. Information warfare at its purest --"
            " the fight was lost before it started."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": "tally_agent",
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "tally_agent_double_agent": {
        "id": "tally_agent_double_agent",
        "name": "Double Agent",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.85,
        "description": (
            "Redirect an enemy's buff to your allies through"
            " social infiltration. The target loses their active"
            " buff and your group gains it instead. The Tally"
            " Agent's defining sideways mechanic."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": "tally_agent",
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.0},
    },

    # --- Blackthorn (subterfuge + alchemy) ---
    "blackthorn_concentrated_venom": {
        "id": "blackthorn_concentrated_venom",
        "name": "Concentrated Venom",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "alchemy",
        "application_chance": 0.90,
        "description": (
            "Apply a concentrated toxin during Vanish. The poison"
            " is delivered before the target even knows you are"
            " there. Higher ceiling than standard poison -- the"
            " Blackthorn's patient precision."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "blackthorn",
        "effect_params": {"damage_base": 60, "status_effect": "poison", "duration": 4, "magnitude": 10},
    },
    "blackthorn_lethal_dose": {
        "id": "blackthorn_lethal_dose",
        "name": "Lethal Dose",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "alchemy",
        "application_chance": 0.90,
        "description": (
            "The highest single-target poison ceiling in the game."
            " A precisely measured lethal compound applied from"
            " stealth. Damage scales with existing poison stacks"
            " on the target. Patient. Precise. Never seen."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "blackthorn",
        "effect_params": {"damage_base": 150, "status_effect": "poison", "duration": 4, "magnitude": 12},
    },

    # --- Shadecommand (subterfuge + tactics) ---
    "shadecommand_tactical_shadow": {
        "id": "shadecommand_tactical_shadow",
        "name": "Tactical Shadow",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "focus",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Extend your stealth to the entire group for one round."
            " Special operations doctrine -- the whole team moves"
            " as one shadow. Allies gain evasion."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "shadecommand",
        "effect_params": {"buff_type": "evasion", "duration": 2, "magnitude": 0.2},
    },
    "shadecommand_black_operation": {
        "id": "shadecommand_black_operation",
        "name": "Black Operation",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Execute a coordinated strike from concealment. Group"
            " stealth plus ambush bonus plus all enemy buffs stripped."
            " The defining Shadecommand maneuver -- the operation"
            " that no one saw coming or survived."
        ),
        "room_flag_written": "shadow_marked",
        "attuned_variants": {},
        "subclass_id": "shadecommand",
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.5},
    },

    # --- Lockjaw (subterfuge + engineering) ---
    "lockjaw_mechanical_trap": {
        "id": "lockjaw_mechanical_trap",
        "name": "Mechanical Trap",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "focus",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "engineering",
        "application_chance": 0.85,
        "description": (
            "Deploy a concealed mechanical device that triggers on"
            " the next enemy action. Deals damage and roots the"
            " target. Built with precision, placed with patience."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "lockjaw",
        "effect_params": {"damage_base": 85, "status_effect": "root", "duration": 2, "magnitude": 1.0},
    },
    "lockjaw_killbox": {
        "id": "lockjaw_killbox",
        "name": "Killbox",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "engineering",
        "application_chance": 0.90,
        "description": (
            "Deploy multiple concealed traps in rapid succession."
            " Each enemy that acts triggers a separate device."
            " Deals escalating damage with each trigger. The room"
            " becomes a death sentence for the unprepared."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "lockjaw",
        "effect_params": {"damage_base": 180},
    },

    # --- Hollowseen (subterfuge + remnance) ---
    "hollowseen_echo_sight": {
        "id": "hollowseen_echo_sight",
        "name": "Echo Sight",
        "domain": "subterfuge",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "focus",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "remnance",
        "application_chance": 0.90,
        "description": (
            "See with impossible clarity. Reveal all hidden enemies"
            " and room flags. Hidden targets are weakened by the"
            " shock of being seen. Awareness that should not exist."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "hollowseen",
        "effect_params": {"debuff_type": "weaken", "duration": 2, "magnitude": 0.15},
    },
    "hollowseen_impossible_awareness": {
        "id": "hollowseen_impossible_awareness",
        "name": "Impossible Awareness",
        "domain": "subterfuge",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "focus",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "subterfuge",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Enter a state of preemptive awareness that defies"
            " explanation. Automatically dodge the next several"
            " attacks and counter each one. Echoes of ancient"
            " knowledge fuel perception beyond mortal limits."
        ),
        "room_flag_written": "scouted",
        "attuned_variants": {},
        "subclass_id": "hollowseen",
        "effect_params": {"buff_type": "evasion", "duration": 4, "magnitude": 0.4},
    },

    # ===================================================================
    # DIPLOMACY DOMAIN POOL (15 abilities) -- resource_type: influence
    # Fingerprint: LEVERAGE -- converting relationships into power
    # Scaling: diplomacy -> presence
    # ===================================================================

    # --- Diplomacy Tier 1 (4 abilities) -- Social leverage, basic effects ---
    "compel_attention": {
        "id": "compel_attention",
        "name": "Compel Attention",
        "domain": "diplomacy",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "influence",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Demand the target's attention with a word. Their focus"
            " shifts to you -- weakened resolve makes them slower"
            " to act. The opening play of every Accord negotiation."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 2, "magnitude": 0.1},
    },
    "sharp_rebuke": {
        "id": "sharp_rebuke",
        "name": "Sharp Rebuke",
        "domain": "diplomacy",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "influence",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A cutting remark delivered with authority. Words that"
            " wound. Presence-scaled damage that bypasses armor."
            " Every door opens from the inside."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 30},
    },
    "bolster_resolve": {
        "id": "bolster_resolve",
        "name": "Bolster Resolve",
        "domain": "diplomacy",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Speak a word of encouragement that steadies an ally's"
            " nerve. Grants a brief damage reduction buff. Solo,"
            " the effect applies to self -- conviction is personal."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 2, "magnitude": 0.1},
    },
    "decree_of_hesitation": {
        "id": "decree_of_hesitation",
        "name": "Decree of Hesitation",
        "domain": "diplomacy",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Issue a command that makes the target hesitate. The"
            " authority in your voice creates doubt -- the target"
            " slows, their next action delayed."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "slow", "duration": 2, "magnitude": 1.0},
    },

    # --- Diplomacy Tier 2 (4 abilities) -- Core social combat ---
    "leveraged_demand": {
        "id": "leveraged_demand",
        "name": "Leveraged Demand",
        "domain": "diplomacy",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "influence",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Convert accumulated influence into direct pressure."
            " Words backed by political weight that deal real"
            " damage. Presence amplifies the impact."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 55},
    },
    "inspire_courage": {
        "id": "inspire_courage",
        "name": "Inspire Courage",
        "domain": "diplomacy",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "influence",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Rally an ally with words that ignite courage. Grants"
            " haste for several rounds. In a group, the effect is"
            " amplified. Solo, your own conviction drives you forward."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 2, "magnitude": 1.0},
    },
    "undermine_confidence": {
        "id": "undermine_confidence",
        "name": "Undermine Confidence",
        "domain": "diplomacy",
        "tier": 2,
        "resource_cost": 18,
        "resource_type": "influence",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Identify and exploit the target's insecurities through"
            " calculated speech. Weakens the target's damage output"
            " as self-doubt creeps into their actions."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.15},
    },
    "words_of_authority": {
        "id": "words_of_authority",
        "name": "Words of Authority",
        "domain": "diplomacy",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Deliver a pronouncement that carries the weight of"
            " earned authority. The charged delivery amplifies"
            " impact. Words that leave bruises."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 70},
    },

    # --- Diplomacy Tier 3 (4 abilities) -- Advanced manipulation ---
    "commanding_presence": {
        "id": "commanding_presence",
        "name": "Commanding Presence",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "influence",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Project an aura of undeniable authority. All enemies"
            " in the room are weakened as your presence overwhelms"
            " their resolve. The Arbiter's judgment made manifest."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "charm_offensive": {
        "id": "charm_offensive",
        "name": "Charm Offensive",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "influence",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": (
            "Overwhelm the target with persuasive force. The charmed"
            " target cannot take hostile actions for a brief moment."
            " Not magic -- sheer force of personality."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "charm", "duration": 1, "magnitude": 1.0},
    },
    "rally_the_fallen": {
        "id": "rally_the_fallen",
        "name": "Rally the Fallen",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "influence",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Speak words that lift allies from despair. Grants haste"
            " and damage reduction to the entire group. The effect"
            " scales with party size. The voice that turns a rout"
            " into a rally."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.0},
    },
    "social_execution": {
        "id": "social_execution",
        "name": "Social Execution",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Deliver a devastating verbal assault that strips the"
            " target's morale. Deals heavy presence-scaled damage."
            " Words sharper than any blade."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 95},
    },

    # --- Diplomacy Tier 4 (3 abilities) -- Domain capstones ---
    "voice_of_the_realm": {
        "id": "voice_of_the_realm",
        "name": "Voice of the Realm",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Speak with the full weight of every relationship"
            " you have cultivated. AoE charm that forces all"
            " enemies to hesitate. Damage scales with your"
            " faction Standing. The ultimate leverage."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "charm", "duration": 2, "magnitude": 1.5},
    },
    "absolute_authority": {
        "id": "absolute_authority",
        "name": "Absolute Authority",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A pronouncement that carries the force of absolute"
            " conviction. Charged delivery for maximum impact."
            " Deals devastating presence-scaled damage to all"
            " enemies. The Voice of the Realm made weapon."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 200},
    },
    "morale_collapse": {
        "id": "morale_collapse",
        "name": "Morale Collapse",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Break the enemy's will to fight with a single"
            " declaration. All enemies are weakened and slowed."
            " The Accord's ultimate social weapon -- a fight"
            " ended by words, not blades."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.25},
    },

    # ===================================================================
    # DIPLOMACY-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets a Tier 3 enhanced blend + Tier 4 defining ability
    # ===================================================================

    # --- Civicguard (diplomacy + combat) ---
    "civicguard_iron_diplomacy": {
        "id": "civicguard_iron_diplomacy",
        "name": "Iron Diplomacy",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "influence",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "combat",
        "application_chance": 0.85,
        "description": (
            "Intimidate the target with demonstrated combat prowess."
            " Your strength makes your words heavier. Presence and"
            " strength both scale the debuff. The diplomat with teeth."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": "civicguard",
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "civicguard_violent_persuasion": {
        "id": "civicguard_violent_persuasion",
        "name": "Violent Persuasion",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "combat",
        "application_chance": 0.85,
        "description": (
            "A devastating strike punctuated by a spoken threat."
            " Deals heavy damage and applies charm. The unique"
            " Civicguard hybrid -- violence and persuasion in"
            " the same breath. The target obeys or bleeds."
        ),
        "room_flag_written": "intimidated",
        "attuned_variants": {},
        "subclass_id": "civicguard",
        "effect_params": {"damage_base": 160, "status_effect": "charm", "duration": 1, "magnitude": 1.0},
    },

    # --- Shadowbroker (diplomacy + subterfuge) ---
    "shadowbroker_information_trade": {
        "id": "shadowbroker_information_trade",
        "name": "Information Trade",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Trade intelligence for advantage. Reveals enemy"
            " weaknesses and grants an ally a damage bonus."
            " Information is currency -- and you are the bank."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": "shadowbroker",
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.0},
    },
    "shadowbroker_network_collapse": {
        "id": "shadowbroker_network_collapse",
        "name": "Network Collapse",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "subterfuge",
        "application_chance": 0.90,
        "description": (
            "Burn your accumulated intelligence network for a"
            " devastating social attack. Massive debuff that scales"
            " with your faction Standing. Every relationship you"
            " built becomes a weapon. Nobody knows who you work for."
        ),
        "room_flag_written": "exposed",
        "attuned_variants": {},
        "subclass_id": "shadowbroker",
        "effect_params": {"debuff_type": "weaken", "duration": 4, "magnitude": 0.3},
    },

    # --- Wayfinder (diplomacy + naturalism) ---
    "wayfinder_empathic_bond": {
        "id": "wayfinder_empathic_bond",
        "name": "Empathic Bond",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": (
            "Open an empathic connection with an ally. Heals wounds"
            " and grants a brief damage reduction buff. Presence"
            " and naturalism combine -- empathy made manifest."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": "wayfinder",
        "effect_params": {"damage_base": 80, "buff_type": "warding", "duration": 2, "magnitude": 0.15},
    },
    "wayfinder_heart_of_the_wild": {
        "id": "wayfinder_heart_of_the_wild",
        "name": "Heart of the Wild",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "naturalism",
        "application_chance": 1.0,
        "description": (
            "Channel the empathic bond through nature itself."
            " Group heal that also grants damage reduction."
            " Bond dimension amplifies the effect. The Wayfinder"
            " who understands what every living thing needs."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": "wayfinder",
        "effect_params": {"damage_base": 150, "buff_type": "warding", "duration": 3, "magnitude": 0.2},
    },

    # --- Spiritvoice (diplomacy + resonance) ---
    "spiritvoice_resonant_word": {
        "id": "spiritvoice_resonant_word",
        "name": "Resonant Word",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "resonance",
        "application_chance": 0.85,
        "description": (
            "Speak a word that resonates with old magic. The debuff"
            " is amplified by resonance -- your voice carries weight"
            " that should not be possible. Words that leave echoes."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "spiritvoice",
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "spiritvoice_voice_of_ages": {
        "id": "spiritvoice_voice_of_ages",
        "name": "Voice of Ages",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "resonance",
        "application_chance": 0.80,
        "description": (
            "Channel old magic through your voice. An AoE charm"
            " that affects all enemies. Resonance and presence"
            " both amplify the effect. The Spiritvoice's defining"
            " power -- words that carry more weight than they should."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "spiritvoice",
        "effect_params": {"debuff_type": "charm", "duration": 2, "magnitude": 1.5},
    },

    # --- Highcourt (diplomacy + arcana) ---
    "highcourt_enchant_word": {
        "id": "highcourt_enchant_word",
        "name": "Enchant Word",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "arcana",
        "application_chance": 0.85,
        "description": (
            "Weave a subtle enchantment into your words. The target"
            " is charmed -- not through force of personality alone"
            " but through literal magic carried in speech."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "highcourt",
        "effect_params": {"debuff_type": "charm", "duration": 2, "magnitude": 1.0},
    },
    "highcourt_sovereign_presence": {
        "id": "highcourt_sovereign_presence",
        "name": "Sovereign Presence",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "arcana",
        "application_chance": 0.80,
        "description": (
            "Project an aura of magical authority that passively"
            " weakens all enemies each round. Sustained effect."
            " The mage who never had to fight because nobody"
            " wanted them to stop talking."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "highcourt",
        "effect_params": {"debuff_type": "weaken", "duration": 4, "magnitude": 0.25},
    },

    # --- Silkpoison (diplomacy + alchemy) ---
    "silkpoison_poisoned_word": {
        "id": "silkpoison_poisoned_word",
        "name": "Poisoned Word",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "alchemy",
        "application_chance": 0.85,
        "description": (
            "Deliver poison through social proximity. A handshake,"
            " a whispered word, a shared drink. The target never"
            " sees the delivery mechanism. Subtle threat made real."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "silkpoison",
        "effect_params": {"damage_base": 60, "status_effect": "poison", "duration": 3, "magnitude": 8},
    },
    "silkpoison_fatal_courtesy": {
        "id": "silkpoison_fatal_courtesy",
        "name": "Fatal Courtesy",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "alchemy",
        "application_chance": 0.90,
        "description": (
            "A delayed poison of extraordinary potency applied"
            " through social interaction. The target feels nothing"
            " for two rounds, then the full dose hits. Undetectable"
            " until it is too late. The most dangerous dinner guest."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "silkpoison",
        "effect_params": {"damage_base": 100, "status_effect": "poison", "duration": 4, "magnitude": 12},
    },

    # --- Bannerspeaker (diplomacy + tactics) ---
    "bannerspeaker_rallying_banner": {
        "id": "bannerspeaker_rallying_banner",
        "name": "Rallying Banner",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Raise a rallying standard that inspires the entire"
            " group. Grants haste and damage reduction. Effect"
            " scales with party size. The voice behind every"
            " military campaign."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": "bannerspeaker",
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.0},
    },
    "bannerspeaker_morale_surge": {
        "id": "bannerspeaker_morale_surge",
        "name": "Morale Surge",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Unleash an overwhelming wave of morale. All allies"
            " gain haste plus a significant damage bonus. The"
            " Bannerspeaker's defining power -- turning armies"
            " with words. Military faction Standing amplifies."
        ),
        "room_flag_written": "inspired",
        "attuned_variants": {},
        "subclass_id": "bannerspeaker",
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.5},
    },

    # --- Dealwright (diplomacy + engineering) ---
    "dealwright_contractual_obligation": {
        "id": "dealwright_contractual_obligation",
        "name": "Contractual Obligation",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "engineering",
        "application_chance": 0.85,
        "description": (
            "Impose an obligation the target cannot ignore. The"
            " debuff strengthens each time the target acts --"
            " every action they take tightens the contract."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "dealwright",
        "effect_params": {"debuff_type": "weaken", "duration": 4, "magnitude": 0.15},
    },
    "dealwright_binding_deal": {
        "id": "dealwright_binding_deal",
        "name": "Binding Deal",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "engineering",
        "application_chance": 0.85,
        "description": (
            "Forge a binding contract that constrains the target."
            " Root plus weaken -- the target is held by an"
            " obligation they cannot break. Every gift was an"
            " investment. Every investment comes due."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "dealwright",
        "effect_params": {"debuff_type": "root", "duration": 3, "magnitude": 1.0},
    },

    # --- Truthwarden (diplomacy + remnance) ---
    "truthwarden_forbidden_knowledge": {
        "id": "truthwarden_forbidden_knowledge",
        "name": "Forbidden Knowledge",
        "domain": "diplomacy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "influence",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "remnance",
        "application_chance": 0.85,
        "description": (
            "Speak a truth the target cannot bear. Knowledge of"
            " the world's actual history weaponized. The debuff"
            " is unique -- a psychic wound from forbidden truth."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "truthwarden",
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "truthwarden_truth_revealed": {
        "id": "truthwarden_truth_revealed",
        "name": "Truth Revealed",
        "domain": "diplomacy",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "influence",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "diplomacy",
        "scaling_secondary": "remnance",
        "application_chance": 0.90,
        "description": (
            "Reveal a truth so fundamental it damages the target's"
            " sense of reality. Massive damage plus weaken. Echoes"
            " amplify the effect. The Truthwarden's defining power"
            " -- what you know can destroy."
        ),
        "room_flag_written": "ordered",
        "attuned_variants": {},
        "subclass_id": "truthwarden",
        "effect_params": {"damage_base": 180, "status_effect": "weaken", "duration": 3, "magnitude": 0.2},
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
