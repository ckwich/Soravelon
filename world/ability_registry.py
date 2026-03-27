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
    # wild_mend, reagent_toss stubs removed -- replaced by full Naturalism/Alchemy pools below
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
    # venom_coat stub removed -- replaced by full Alchemy pool below
    # resonance_ward stub removed -- replaced by full Resonance pool below
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

    # ===================================================================
    # ARCANA DOMAIN POOL (15 abilities) -- resource_type: mana
    # Fingerprint: RATION -- cross-encounter mana management
    # Scaling: arcana -> mana stat
    # Elements: fire, ice, lightning, arcane. Caster domain: many charged.
    # ===================================================================

    # --- Arcana Tier 1 (4 abilities) -- Basic spells, measured force ---
    "arcane_bolt": {
        "id": "arcane_bolt",
        "name": "Arcane Bolt",
        "domain": "arcana",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "mana",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A focused lance of raw arcane force. The simplest spell"
            " in the Arcane curriculum -- and the one that teaches"
            " mana discipline. Every bolt is a choice to spend."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 35},
    },
    "frost_shard": {
        "id": "frost_shard",
        "name": "Frost Shard",
        "domain": "arcana",
        "tier": 1,
        "resource_cost": 18,
        "resource_type": "mana",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Conjure a spike of crystallized cold and hurl it."
            " Targets struck feel the chill seep into their joints"
            " -- movements slow, reactions dull."
        ),
        "room_flag_written": "frozen",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 30, "status_effect": "slow", "duration": 2, "magnitude": 1.0},
    },
    "mana_shield": {
        "id": "mana_shield",
        "name": "Mana Shield",
        "domain": "arcana",
        "tier": 1,
        "resource_cost": 20,
        "resource_type": "mana",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Weave a thin barrier of condensed mana around yourself."
            " It absorbs incoming damage briefly -- a mage's first"
            " lesson in survival is not to be where the sword lands."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 2, "magnitude": 0.15},
    },
    "spark_jolt": {
        "id": "spark_jolt",
        "name": "Spark Jolt",
        "domain": "arcana",
        "tier": 1,
        "resource_cost": 20,
        "resource_type": "mana",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": (
            "Release a sharp crack of lightning from your fingertips."
            " The jolt disrupts the target's muscles briefly. Cheap"
            " and fast -- the bread and butter of a mage under pressure."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 40, "status_effect": "stun", "duration": 1, "magnitude": 1.0},
    },

    # --- Arcana Tier 2 (4 abilities) -- Core spellcasting, moderate mana ---
    "fireball": {
        "id": "fireball",
        "name": "Fireball",
        "domain": "arcana",
        "tier": 2,
        "resource_cost": 30,
        "resource_type": "mana",
        "cooldown": 2,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Gather mana into a roiling sphere of flame and release"
            " it. The explosion scorches everything nearby. A"
            " channeled classic -- the reason mages earn their keep."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 65, "status_effect": "burn", "duration": 3, "magnitude": 1.0},
    },
    "ice_lance": {
        "id": "ice_lance",
        "name": "Ice Lance",
        "domain": "arcana",
        "tier": 2,
        "resource_cost": 25,
        "resource_type": "mana",
        "cooldown": 1,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Channel cold into a spiraling lance of ice. The impact"
            " pierces and the frost lingers. Slower targets take"
            " the full brunt -- ice rewards patience."
        ),
        "room_flag_written": "frozen",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 60, "status_effect": "slow", "duration": 2, "magnitude": 1.0},
    },
    "arcane_infusion": {
        "id": "arcane_infusion",
        "name": "Arcane Infusion",
        "domain": "arcana",
        "tier": 2,
        "resource_cost": 25,
        "resource_type": "mana",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Infuse yourself with raw magical energy. Your next"
            " several abilities hit harder and cost less -- the"
            " investment pays forward across the encounter."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.0},
    },
    "mana_drain": {
        "id": "mana_drain",
        "name": "Mana Drain",
        "domain": "arcana",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "mana",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Reach into the target's magical reserves and tear away"
            " a portion. What you take you keep. Against mundane"
            " foes, the spell weakens their resistance instead."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "drain", "duration": 3, "magnitude": 1.0},
    },

    # --- Arcana Tier 3 (4 abilities) -- Advanced magic, high mana ---
    "chain_lightning": {
        "id": "chain_lightning",
        "name": "Chain Lightning",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 40,
        "resource_type": "mana",
        "cooldown": 3,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Call down a bolt that leaps from target to target."
            " Each arc carries burn and the air itself becomes"
            " charged. The spell every mage dreams of casting"
            " and every mage fears the cost of."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 90, "status_effect": "burn", "duration": 3, "magnitude": 1.0},
    },
    "glacial_tomb": {
        "id": "glacial_tomb",
        "name": "Glacial Tomb",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 45,
        "resource_type": "mana",
        "cooldown": 4,
        "charge_turns": 1,
        "effect_type": "debuff",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": (
            "Encase a target in a prison of solid ice. The cold"
            " seeps inward, rooting them in place and weakening"
            " their resolve. Breaking free costs them everything."
        ),
        "room_flag_written": "frozen",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "root", "duration": 2, "magnitude": 1.5},
    },
    "conflagration": {
        "id": "conflagration",
        "name": "Conflagration",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 45,
        "resource_type": "mana",
        "cooldown": 3,
        "charge_turns": 1,
        "effect_type": "dot",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Set the air itself alight. A sustained burning that"
            " scorches every enemy in the area. The flames persist"
            " after the spell ends -- mana spent, damage ongoing."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"dot_type": "burn", "duration": 4, "damage_per_tick": 25, "magnitude": 1.5},
    },
    "spellweave_barrier": {
        "id": "spellweave_barrier",
        "name": "Spellweave Barrier",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 40,
        "resource_type": "mana",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Weave a lattice of interlocking spell strands around"
            " yourself or an ally. The barrier absorbs significant"
            " damage before shattering. Expensive -- but survival"
            " has no budget."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.25},
    },

    # --- Arcana Tier 4 (3 abilities) -- Domain capstones, devastating ---
    "meteor_strike": {
        "id": "meteor_strike",
        "name": "Meteor Strike",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 65,
        "resource_type": "mana",
        "cooldown": 6,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Call down a fragment of concentrated elemental force"
            " from the sky. The impact obliterates and the blast"
            " leaves the ground scorched for rounds after. The"
            " spell that ends encounters -- and mana reserves."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 200, "status_effect": "burn", "duration": 3, "magnitude": 2.0},
    },
    "absolute_zero": {
        "id": "absolute_zero",
        "name": "Absolute Zero",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 60,
        "resource_type": "mana",
        "cooldown": 6,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Drain all heat from an area in a single catastrophic"
            " instant. Everything freezes -- movement, thought,"
            " intention. Survivors are rooted and weakened."
            " The coldest expression of magical mastery."
        ),
        "room_flag_written": "frozen",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 180, "status_effect": "root", "duration": 2, "magnitude": 2.0},
    },
    "arcane_cataclysm": {
        "id": "arcane_cataclysm",
        "name": "Arcane Cataclysm",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 70,
        "resource_type": "mana",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Release all elements simultaneously in a single,"
            " devastating convergence. Fire, ice, and lightning"
            " tear through every enemy in the room. The most"
            " expensive spell in the Arcane curriculum. Worth it."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 250, "status_effect": "burn", "duration": 2, "magnitude": 2.0},
    },

    # ===================================================================
    # ARCANA-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets T3 + T4 signature abilities
    # ===================================================================

    # --- Battlemage (arcana + combat) ---
    "battlemage_mana_strike": {
        "id": "battlemage_mana_strike",
        "name": "Mana Strike",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "mana",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Channel mana directly through your weapon arm. The"
            " blow lands with both physical and magical force."
            " Strength and Mana scale the damage equally -- the"
            " Battlemage's answer to running out of spells."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "battlemage",
        "effect_params": {"damage_base": 95},
    },
    "battlemage_arcane_warrior": {
        "id": "battlemage_arcane_warrior",
        "name": "Arcane Warrior",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "mana",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Suffuse your body with mana until flesh and spell are"
            " one. For several rounds every physical strike carries"
            " arcane damage. The Battlemage ideal -- there is no"
            " line between fighter and mage."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "battlemage",
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 1.5},
    },

    # --- Mistveil (arcana + subterfuge) ---
    "mistveil_mist_shroud": {
        "id": "mistveil_mist_shroud",
        "name": "Mist Shroud",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "mana",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Wrap yourself in a cloak of enchanted mist. Unlike"
            " physical stealth this concealment is magical -- it"
            " bends light and muffles sound through spellwork."
            " Detection methods that find Vanish cannot find this."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "mistveil",
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.3},
    },
    "mistveil_phantom_form": {
        "id": "mistveil_phantom_form",
        "name": "Phantom Form",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "mana",
        "cooldown": 7,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Dissolve into a sustained state of magical invisibility."
            " You can cast spells while incorporeal. Enemies strike"
            " through you. The Mistveil's defining gift -- present"
            " but untouchable."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "mistveil",
        "effect_params": {"buff_type": "warding", "duration": 4, "magnitude": 0.4},
    },

    # --- Stormweaver (arcana + naturalism) ---
    "stormweaver_chain_storm": {
        "id": "stormweaver_chain_storm",
        "name": "Chain Storm",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 40,
        "resource_type": "mana",
        "cooldown": 3,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "naturalism",
        "application_chance": 0.85,
        "description": (
            "Weave lightning through natural conduits -- trees,"
            " water, living roots. Each arc chains to the nearest"
            " target. In natural zones the conductivity is perfect"
            " and every enemy feels it."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "stormweaver",
        "effect_params": {"damage_base": 100, "status_effect": "wet", "duration": 2, "magnitude": 1.0},
    },
    "stormweaver_tempest": {
        "id": "stormweaver_tempest",
        "name": "Tempest",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 65,
        "resource_type": "mana",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "naturalism",
        "application_chance": 0.90,
        "description": (
            "Call down a full elemental storm. Wind tears through"
            " the area, lightning strikes indiscriminately, and"
            " rain soaks everything. The Stormweaver's masterwork"
            " -- nature and arcana fused into devastation."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "stormweaver",
        "effect_params": {
            "damage_base": 180, "status_effect": "burn", "duration": 3,
            "magnitude": 1.5,
        },
    },

    # --- Spellseeker (arcana + resonance) ---
    "spellseeker_node_tap": {
        "id": "spellseeker_node_tap",
        "name": "Node Tap",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "mana",
        "cooldown": 4,
        "charge_turns": 1,
        "effect_type": "utility",
        "scaling_primary": "arcana",
        "scaling_secondary": "resonance",
        "application_chance": 1.0,
        "description": (
            "Tap into ambient resonance to restore mana. The old"
            " patterns hold energy the Spellseeker has learned to"
            " siphon. Spend a little, recover more -- the mage who"
            " studies nodes never truly runs dry."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {},
        "subclass_id": "spellseeker",
        "effect_params": {"mana_restored": 40},
    },
    "spellseeker_arcane_resonance": {
        "id": "spellseeker_arcane_resonance",
        "name": "Arcane Resonance",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "mana",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "resonance",
        "application_chance": 1.0,
        "description": (
            "Unleash a blast that harmonizes arcane force with the"
            " room's resonant frequency. In places where old magic"
            " lingers the damage is catastrophic. The Spellseeker's"
            " proof that old and new magic are one thing."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "spellseeker",
        "effect_params": {"damage_base": 200},
    },

    # --- Enchantvoice (arcana + diplomacy) ---
    "enchantvoice_binding_word": {
        "id": "enchantvoice_binding_word",
        "name": "Binding Word",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "mana",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.80,
        "description": (
            "Speak a word charged with magical authority. It strikes"
            " the target's mind and body simultaneously -- damage"
            " from the impact, charm from the compulsion. Words"
            " have weight when an Enchantvoice speaks them."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "enchantvoice",
        "effect_params": {"damage_base": 80, "status_effect": "charm", "duration": 1, "magnitude": 1.0},
    },
    "enchantvoice_voice_of_command": {
        "id": "enchantvoice_voice_of_command",
        "name": "Voice of Command",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "mana",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "debuff",
        "scaling_primary": "arcana",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.75,
        "description": (
            "Release a word of absolute command that reverberates"
            " through every enemy in the room. Presence and mana"
            " weave together into irresistible compulsion. The"
            " Enchantvoice's masterwork -- when you speak, the"
            " world listens."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "enchantvoice",
        "effect_params": {"debuff_type": "charm", "duration": 2, "magnitude": 1.5},
    },

    # --- Fusewright (arcana + alchemy) ---
    "fusewright_volatile_mixture": {
        "id": "fusewright_volatile_mixture",
        "name": "Volatile Mixture",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "mana",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "arcana",
        "scaling_secondary": "alchemy",
        "application_chance": 0.85,
        "description": (
            "Ignite an alchemical compound with magical force."
            " The resulting reaction burns and poisons simultaneously"
            " -- chemistry and spellcraft fused into a persistent"
            " wound the body cannot easily mend."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": "fusewright",
        "effect_params": {"dot_type": "burn", "duration": 4, "damage_per_tick": 20, "magnitude": 1.5},
    },
    "fusewright_transmutation_burst": {
        "id": "fusewright_transmutation_burst",
        "name": "Transmutation Burst",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "mana",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "alchemy",
        "application_chance": 1.0,
        "description": (
            "Convert all active DoT effects on the target into"
            " a single massive burst of transmuted energy. Every"
            " burn, poison, and bleed stack detonates at once."
            " The Fusewright's philosophy: patience creates"
            " the biggest explosion."
        ),
        "room_flag_written": "scorched",
        "attuned_variants": {},
        "subclass_id": "fusewright",
        "effect_params": {"damage_base": 160},
    },

    # --- Wardcaller (arcana + tactics) ---
    "wardcaller_ward_zone": {
        "id": "wardcaller_ward_zone",
        "name": "Ward Zone",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 40,
        "resource_type": "mana",
        "cooldown": 5,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Lay down a ward that reduces damage for all allies"
            " in the room. The ward persists for several rounds"
            " -- precise placement over raw power. The Wardcaller"
            " controls where the fight happens."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "wardcaller",
        "effect_params": {"buff_type": "warding", "duration": 4, "magnitude": 0.2},
    },
    "wardcaller_arcane_fortress": {
        "id": "wardcaller_arcane_fortress",
        "name": "Arcane Fortress",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 60,
        "resource_type": "mana",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Erect a sustained dome of interlocking wards. Allies"
            " inside take reduced damage while enemies inside take"
            " a persistent debuff. The Wardcaller's masterwork --"
            " the battlefield itself becomes your weapon."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "wardcaller",
        "effect_params": {"buff_type": "warding", "duration": 5, "magnitude": 0.3},
    },

    # --- Runewright (arcana + engineering) ---
    "runewright_rune_trap": {
        "id": "runewright_rune_trap",
        "name": "Rune Trap",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 35,
        "resource_type": "mana",
        "cooldown": 4,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "engineering",
        "application_chance": 0.85,
        "description": (
            "Inscribe a rune that detonates when triggered. The"
            " blast applies burn and weaken -- magical engineering"
            " at its finest. Set it and wait. The trap does not"
            " care about patience."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "runewright",
        "effect_params": {"damage_base": 100, "status_effect": "burn", "duration": 3, "magnitude": 1.0},
    },
    "runewright_masterwork_rune": {
        "id": "runewright_masterwork_rune",
        "name": "Masterwork Rune",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "mana",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "buff",
        "scaling_primary": "arcana",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Inscribe a permanent rune of power onto yourself or"
            " an ally. The enchantment persists until dispelled --"
            " not rounds, not minutes, until something breaks it."
            " The Runewright builds things that last."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "runewright",
        "effect_params": {"buff_type": "haste", "duration": 6, "magnitude": 1.5},
    },

    # --- Voidscribe (arcana + remnance) ---
    "voidscribe_void_bolt": {
        "id": "voidscribe_void_bolt",
        "name": "Void Bolt",
        "domain": "arcana",
        "tier": 3,
        "resource_cost": 40,
        "resource_type": "mana",
        "cooldown": 2,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Cast a bolt of pre-cursor energy that bypasses magical"
            " resistance entirely. This spell predates modern"
            " protective wards -- it strikes at something deeper."
            " The Circle of Wizards does not approve."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "voidscribe",
        "effect_params": {"damage_base": 110},
    },
    "voidscribe_firstform_casting": {
        "id": "voidscribe_firstform_casting",
        "name": "Firstform Casting",
        "domain": "arcana",
        "tier": 4,
        "resource_cost": 65,
        "resource_type": "mana",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "arcana",
        "scaling_secondary": "remnance",
        "application_chance": 0.90,
        "description": (
            "Cast using an ancient spellform that predates the"
            " ten schools entirely. The damage is catastrophic"
            " and applies a unique debuff -- the target's magical"
            " resistance inverts. The Voidscribe's forbidden art."
        ),
        "room_flag_written": "arcane_residue",
        "attuned_variants": {},
        "subclass_id": "voidscribe",
        "effect_params": {"damage_base": 220, "status_effect": "weaken", "duration": 3, "magnitude": 0.3},
    },

    # ===================================================================
    # RESONANCE DOMAIN POOL (15 abilities) -- resource_type: resonance
    # Fingerprint: ATTUNE -- builder/spender, in-combat decay, env reading
    # Scaling: resonance -> resonance stat
    # Builder abilities generate +15-20 resonance. Spenders cost 60-100.
    # Decay: -10 per round during combat.
    # ALL resonance abilities have attuned_variants populated.
    # ===================================================================

    # --- Resonance Tier 1 (4 abilities) -- Builders and basic effects ---
    "resonant_strike": {
        "id": "resonant_strike",
        "name": "Resonant Strike",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Strike with old-magic-infused force. The blow deals"
            " damage and builds resonance. The foundation of every"
            " Resonance practitioner's rhythm -- build toward the"
            " moment that matters."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "charged": {"extra_effect": "arc to second target for 50% damage", "extra_cost": 10},
            "resonant": {"extra_effect": "arc to ALL enemies for 30% damage", "extra_cost": 15},
            "fading_life": {"extra_effect": "apply Root for 2 rounds", "extra_cost": 10},
            "ancient_ground": {"extra_effect": "+25% damage", "extra_cost": 5},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 30, "resonance_generated": 15},
    },
    "attunement_pulse": {
        "id": "attunement_pulse",
        "name": "Attunement Pulse",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Send a pulse of resonant energy outward. Deals light"
            " damage and attunes you further to the environment."
            " A builder -- the pulse is the question, the room's"
            " response is the answer."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "charged": {"extra_effect": "pulse stuns for 1 round", "extra_cost": 15},
            "ancient_ground": {"extra_effect": "+20 resonance generated", "extra_cost": 5},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 25, "resonance_generated": 20},
    },
    "echo_ward": {
        "id": "echo_ward",
        "name": "Echo Ward",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Attune a protective echo around yourself. The ward"
            " absorbs incoming damage briefly while building"
            " resonance. Defense and rhythm in a single motion."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "resonant": {"extra_effect": "ward extends to all allies", "extra_cost": 15},
            "ancient_ground": {"extra_effect": "ward duration +2 rounds", "extra_cost": 5},
        },
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 2, "magnitude": 0.15, "resonance_generated": 15},
    },
    "pattern_read": {
        "id": "pattern_read",
        "name": "Pattern Read",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Read the target's defensive patterns through resonant"
            " perception. Weaknesses become visible -- their guard"
            " drops where you predicted it would. Builds resonance"
            " while exposing the enemy."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "corrupted_death": {"extra_effect": "free resonance stack on next ability", "extra_cost": 0},
            "void_touched": {"extra_effect": "debuff duration +2 rounds", "extra_cost": 10},
        },
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 2, "magnitude": 0.1, "resonance_generated": 15},
    },

    # --- Resonance Tier 2 (4 abilities) -- Core attunement, mix of builders/spenders ---
    "harmonic_blast": {
        "id": "harmonic_blast",
        "name": "Harmonic Blast",
        "domain": "resonance",
        "tier": 2,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Spend accumulated resonance in a focused blast of"
            " harmonic energy. The payoff for patient building --"
            " damage scales with how long you held the tension."
            " The spender that defines Resonance combat."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "blast chains to a second target for 75% damage", "extra_cost": 15},
            "resonant": {"extra_effect": "blast hits ALL enemies at 60% damage", "extra_cost": 20},
            "node_critical": {"extra_effect": "spend threshold lowered to 40", "extra_cost": 0},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 70},
    },
    "dissonance_wave": {
        "id": "dissonance_wave",
        "name": "Dissonance Wave",
        "domain": "resonance",
        "tier": 2,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Release a wave of discordant resonance that disrupts"
            " enemy defenses. The disharmony weakens and slows --"
            " their rhythm breaks where yours holds steady."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {
            "resonant": {"extra_effect": "wave hits ALL enemies", "extra_cost": 15},
            "charged": {"extra_effect": "also applies stun for 1 round", "extra_cost": 20},
        },
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.15},
    },
    "resonant_charge": {
        "id": "resonant_charge",
        "name": "Resonant Charge",
        "domain": "resonance",
        "tier": 2,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 1,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Channel resonant energy through a focused charge."
            " The brief cast time builds significant resonance"
            " while dealing moderate damage. The bridge between"
            " T1 builders and T2 spenders."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "ancient_ground": {"extra_effect": "+30% damage and +10 resonance", "extra_cost": 5},
            "fading_life": {"extra_effect": "apply Bleed for 3 rounds", "extra_cost": 10},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 55, "resonance_generated": 20},
    },
    "echo_mend": {
        "id": "echo_mend",
        "name": "Echo Mend",
        "domain": "resonance",
        "tier": 2,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Channel resonance into restorative echoes. The old"
            " patterns remember wholeness -- your body follows."
            " A spender that heals rather than harms. Resonance"
            " practitioners heal by remembering what was intact."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "fading_life": {"extra_effect": "heal also removes 1 DoT effect", "extra_cost": 10},
            "ancient_ground": {"extra_effect": "+50% healing", "extra_cost": 10},
        },
        "subclass_id": None,
        "effect_params": {"heal_amount": 60},
    },

    # --- Resonance Tier 3 (4 abilities) -- Advanced attunement, powerful spenders ---
    "cascade_burst": {
        "id": "cascade_burst",
        "name": "Cascade Burst",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 80,
        "resource_type": "resonance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Release resonance in a cascading detonation that"
            " ripples outward. Each wave hits harder than the"
            " last. Burns everything it touches. The advanced"
            " spender -- raw resonance converted to destruction."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "cascade adds a fourth wave for +40% total damage", "extra_cost": 15},
            "resonant": {"extra_effect": "each wave hits all enemies", "extra_cost": 20},
            "node_critical": {"extra_effect": "spend threshold lowered to 60", "extra_cost": 0},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 110, "status_effect": "burn", "duration": 3, "magnitude": 1.0},
    },
    "harmonic_shield": {
        "id": "harmonic_shield",
        "name": "Harmonic Shield",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 80,
        "resource_type": "resonance",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Attune a powerful harmonic barrier around yourself"
            " and nearby allies. The shield resonates with"
            " incoming damage, reducing it significantly. Spending"
            " a full buildup on protection -- a choice only"
            " discipline can afford."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "resonant": {"extra_effect": "shield reflects 20% damage back to attackers", "extra_cost": 15},
            "ancient_ground": {"extra_effect": "shield duration +3 rounds", "extra_cost": 10},
        },
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.25},
    },
    "deep_attunement": {
        "id": "deep_attunement",
        "name": "Deep Attunement",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 5,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Enter a state of deep environmental attunement."
            " For several rounds all resonance generation is"
            " doubled and decay is halved. The Resonant player's"
            " answer to a long fight -- invest now, dominate later."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "resonant": {"extra_effect": "also grants haste for duration", "extra_cost": 10},
            "ancient_ground": {"extra_effect": "attunement also restores 30 resonance", "extra_cost": 5},
        },
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 1.0, "resonance_generated": 15},
    },
    "disruption_spike": {
        "id": "disruption_spike",
        "name": "Disruption Spike",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 80,
        "resource_type": "resonance",
        "cooldown": 4,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Drive a spike of dissonant energy into the target."
            " The disruption stuns and deals heavy damage. Charged"
            " cast for focused impact -- precision spending."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {
            "charged": {"extra_effect": "stun duration +1 round", "extra_cost": 15},
            "corrupted_death": {"extra_effect": "spike also applies weaken 3 rounds", "extra_cost": 10},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 100, "status_effect": "stun", "duration": 1, "magnitude": 1.5},
    },

    # --- Resonance Tier 4 (3 abilities) -- Domain capstones, full resource spenders ---
    "resonance_detonation": {
        "id": "resonance_detonation",
        "name": "Resonance Detonation",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Detonate your entire resonance pool in one cataclysmic"
            " release. Damage scales with resonance spent -- at"
            " full 100, nothing in the room survives unscathed."
            " The payoff for perfect resource discipline."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "detonation chains to adjacent rooms", "extra_cost": 0},
            "resonant": {"extra_effect": "damage +50% and applies burn 3 rounds", "extra_cost": 0},
            "node_critical": {"extra_effect": "detonation costs only 80 resonance", "extra_cost": 0},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 200},
    },
    "harmonic_convergence": {
        "id": "harmonic_convergence",
        "name": "Harmonic Convergence",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Channel all resonance into a sustained convergence"
            " of harmonic force. The two-round channel amplifies"
            " damage exponentially. Everything in the room takes"
            " massive damage and is stunned. The ultimate expression"
            " of patient power."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "resonant": {"extra_effect": "convergence leaves resonant field for 3 rounds", "extra_cost": 0},
            "ancient_ground": {"extra_effect": "stun duration +1 round", "extra_cost": 0},
            "corrupted_death": {"extra_effect": "enemies take 50% more damage from all sources for 2 rounds", "extra_cost": 0},
        },
        "subclass_id": None,
        "effect_params": {"damage_base": 250, "status_effect": "stun", "duration": 1, "magnitude": 2.0},
    },
    "world_echo": {
        "id": "world_echo",
        "name": "World Echo",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Echo the world's original pattern -- before the curse,"
            " before the breaking. For a brief time everything in"
            " the room reverts toward wholeness. Allies heal, enemies"
            " weaken, and the old magic remembers what it was."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "resonant": {"extra_effect": "echo sustains for +3 additional rounds", "extra_cost": 0},
            "ancient_ground": {"extra_effect": "healing doubled for all allies", "extra_cost": 0},
            "fading_life": {"extra_effect": "also removes all DoT effects from allies", "extra_cost": 0},
        },
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.35},
    },

    # ===================================================================
    # RESONANCE-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets T3 + T4 signature abilities
    # ALL signatures have attuned_variants matching subclass flags
    # ===================================================================

    # --- Runebreaker (resonance + combat) ---
    "runebreaker_resonant_blow": {
        "id": "runebreaker_resonant_blow",
        "name": "Resonant Blow",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Channel old magic through a physical strike that"
            " leaves reality slightly wrong where it lands."
            " Builds resonance AND writes charged to the room."
            " The Runebreaker's signature: hit things until"
            " the world breaks."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "strike deals +50% damage and stuns for 1 round", "extra_cost": 15},
            "resonant": {"extra_effect": "strike arcs to all enemies for 40% damage", "extra_cost": 20},
        },
        "subclass_id": "runebreaker",
        "effect_params": {"damage_base": 85, "resonance_generated": 20},
    },
    "runebreaker_node_burst": {
        "id": "runebreaker_node_burst",
        "name": "Node Burst",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Detonate all accumulated resonance in a physical"
            " shockwave centered on your weapon. Every enemy in"
            " the room takes massive damage. In a charged room"
            " the detonation is catastrophic. The Runebreaker's"
            " answer to everything: hit harder."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "damage +75% in charged rooms", "extra_cost": 0},
            "resonant": {"extra_effect": "burst also applies burn 3 rounds to all targets", "extra_cost": 0},
        },
        "subclass_id": "runebreaker",
        "effect_params": {"damage_base": 220},
    },

    # --- Greymantle (resonance + subterfuge) ---
    "greymantle_shadow_attunement": {
        "id": "greymantle_shadow_attunement",
        "name": "Shadow Attunement",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Attune to the world's blind spots -- places where"
            " old magic creates shadows in perception. You become"
            " undetectable to magical senses while building resonance."
            " The Greymantle moves where the world cannot see."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "shadow_marked": {"extra_effect": "also grants physical stealth for duration", "extra_cost": 10},
            "scouted": {"extra_effect": "next attack from attunement deals +80% damage", "extra_cost": 15},
        },
        "subclass_id": "greymantle",
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.25, "resonance_generated": 20},
    },
    "greymantle_veil_of_silence": {
        "id": "greymantle_veil_of_silence",
        "name": "Veil of Silence",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 1,
        "effect_type": "debuff",
        "scaling_primary": "resonance",
        "scaling_secondary": "subterfuge",
        "application_chance": 0.85,
        "description": (
            "Wrap the area in a veil of resonant silence. Enemies"
            " cannot detect you AND take a persistent debuff aura."
            " You move unseen while they stumble. The Greymantle's"
            " masterwork: the world forgets you exist."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {
            "shadow_marked": {"extra_effect": "veil also applies blind to all enemies", "extra_cost": 0},
            "scouted": {"extra_effect": "first strike from veil auto-crits", "extra_cost": 0},
        },
        "subclass_id": "greymantle",
        "effect_params": {"debuff_type": "slow", "duration": 4, "magnitude": 1.5},
    },

    # --- Thornweald (resonance + naturalism) ---
    "thornweald_nature_echo": {
        "id": "thornweald_nature_echo",
        "name": "Nature Echo",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "resonance",
        "scaling_secondary": "naturalism",
        "application_chance": 0.85,
        "description": (
            "Channel old magic through living roots. The target"
            " takes persistent nature damage while you heal from"
            " the exchange. The Thornweald's duality: every wound"
            " you inflict mends one of your own."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "fading_life": {"extra_effect": "DoT also applies Bleed for duration", "extra_cost": 10},
            "living_wood": {"extra_effect": "self-heal doubled", "extra_cost": 10},
        },
        "subclass_id": "thornweald",
        "effect_params": {"dot_type": "poison", "duration": 4, "damage_per_tick": 18, "magnitude": 1.0, "resonance_generated": 15},
    },
    "thornweald_ancient_growth": {
        "id": "thornweald_ancient_growth",
        "name": "Ancient Growth",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 1,
        "effect_type": "dot",
        "scaling_primary": "resonance",
        "scaling_secondary": "naturalism",
        "application_chance": 0.90,
        "description": (
            "Call forth ancient growth that remembers the world"
            " before the curse. Thorns erupt beneath every enemy,"
            " dealing sustained damage while a healing canopy"
            " shelters allies. The Thornweald's masterwork:"
            " the forest as weapon and sanctuary."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "fading_life": {"extra_effect": "DoT damage +50% and applies Root", "extra_cost": 0},
            "living_wood": {"extra_effect": "healing zone persists 2 extra rounds", "extra_cost": 0},
        },
        "subclass_id": "thornweald",
        "effect_params": {"dot_type": "poison", "duration": 5, "damage_per_tick": 30, "magnitude": 2.0},
    },

    # --- Sealwright (resonance + arcana) ---
    "sealwright_focused_blast": {
        "id": "sealwright_focused_blast",
        "name": "Focused Blast",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "arcana",
        "application_chance": 1.0,
        "description": (
            "Focus resonant and arcane energy into a single"
            " devastating blast. Highest single-target burst"
            " in the Resonance toolkit. In charged rooms the"
            " damage becomes something else entirely."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "damage +60% in charged rooms", "extra_cost": 15},
            "resonant": {"extra_effect": "blast also hits second target for 50% damage", "extra_cost": 15},
        },
        "subclass_id": "sealwright",
        "effect_params": {"damage_base": 120},
    },
    "sealwright_seal_break": {
        "id": "sealwright_seal_break",
        "name": "Seal Break",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "arcana",
        "application_chance": 1.0,
        "description": (
            "Break the seal between old and new magic in a single"
            " cataclysmic release. The highest single-target damage"
            " in the entire Resonance guild. In resonant rooms the"
            " blast tears through resistance entirely. The Sealwright's"
            " proof that power has no limits -- only costs."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {
            "charged": {"extra_effect": "damage +40% and target takes +25% damage for 3 rounds", "extra_cost": 0},
            "resonant": {"extra_effect": "damage +80% -- highest burst in the game", "extra_cost": 0},
        },
        "subclass_id": "sealwright",
        "effect_params": {"damage_base": 250},
    },

    # --- Lorekeeper (resonance + diplomacy) ---
    "lorekeeper_ancient_insight": {
        "id": "lorekeeper_ancient_insight",
        "name": "Ancient Insight",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": "diplomacy",
        "application_chance": 1.0,
        "description": (
            "Channel ancient knowledge into a group buff. Allies"
            " gain combat advantage from lore fragments you have"
            " decoded. The more you know, the more dangerous"
            " everyone around you becomes."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "ancient_ground": {"extra_effect": "buff magnitude doubled on ancient ground", "extra_cost": 10},
            "ancient_presence": {"extra_effect": "also grants faction Standing bonus to group", "extra_cost": 15},
        },
        "subclass_id": "lorekeeper",
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 1.0},
    },
    "lorekeeper_lorewarden": {
        "id": "lorekeeper_lorewarden",
        "name": "Lorewarden",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": "diplomacy",
        "application_chance": 1.0,
        "description": (
            "Become a sustained aura of ancient knowledge. Allies"
            " near you receive continuous combat bonuses and"
            " accelerated Standing gain. The Lorekeeper's defining"
            " power is not destruction -- it is making everyone"
            " around them extraordinary."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "ancient_ground": {"extra_effect": "aura radius expands, duration +3 rounds", "extra_cost": 0},
            "ancient_presence": {"extra_effect": "allies also gain +20% damage for duration", "extra_cost": 0},
        },
        "subclass_id": "lorekeeper",
        "effect_params": {"buff_type": "haste", "duration": 5, "magnitude": 1.5},
    },

    # --- Corroder (resonance + alchemy) ---
    "corroder_resonant_acid": {
        "id": "corroder_resonant_acid",
        "name": "Resonant Acid",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "resonance",
        "scaling_secondary": "alchemy",
        "application_chance": 0.85,
        "description": (
            "Infuse an alchemical acid with resonant energy. The"
            " compound burns through defenses while building your"
            " resonance pool. Old magic makes the chemistry worse"
            " -- worse for them."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "toxic_air": {"extra_effect": "acid also applies poison 3 stacks", "extra_cost": 10},
            "poisoned_air": {"extra_effect": "DoT damage +40% in poisoned rooms", "extra_cost": 10},
        },
        "subclass_id": "corroder",
        "effect_params": {"dot_type": "burn", "duration": 4, "damage_per_tick": 22, "magnitude": 1.0, "resonance_generated": 15},
    },
    "corroder_old_corruption": {
        "id": "corroder_old_corruption",
        "name": "Old Corruption",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "dot",
        "scaling_primary": "resonance",
        "scaling_secondary": "alchemy",
        "application_chance": 0.90,
        "description": (
            "Release a corruption that predates alchemy itself."
            " The toxin interacts with old magic in the air,"
            " amplifying in poisoned rooms to devastating effect."
            " The Corroder's masterwork: chemistry from before"
            " the world forgot what chemistry could do."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {
            "poisoned_air": {"extra_effect": "DoT damage doubled and applies weaken 3 rounds", "extra_cost": 0},
            "toxic_air": {"extra_effect": "corruption spreads to all enemies in room", "extra_cost": 0},
        },
        "subclass_id": "corroder",
        "effect_params": {"dot_type": "poison", "duration": 5, "damage_per_tick": 35, "magnitude": 2.0},
    },

    # --- Nodecaller (resonance + tactics) ---
    "nodecaller_node_pulse": {
        "id": "nodecaller_node_pulse",
        "name": "Node Pulse",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "tactics",
        "application_chance": 0.85,
        "description": (
            "Pulse resonant energy that deliberately writes the"
            " resonant flag to the room. The pulse damages enemies"
            " and creates tactical terrain for your team. The"
            " Nodecaller controls the battlefield's resonant state."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "fortified": {"extra_effect": "pulse also applies weaken to all enemies", "extra_cost": 10},
            "resonant": {"extra_effect": "damage +50% in already resonant rooms", "extra_cost": 10},
        },
        "subclass_id": "nodecaller",
        "effect_params": {"damage_base": 90},
    },
    "nodecaller_node_storm": {
        "id": "nodecaller_node_storm",
        "name": "Node Storm",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "tactics",
        "application_chance": 0.90,
        "description": (
            "Create a sustained node storm that writes resonant"
            " to the room and deals AoE damage each round. The"
            " storm persists for several rounds. The Nodecaller's"
            " masterwork: the node event IS the weapon."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "fortified": {"extra_effect": "allies gain damage reduction for storm duration", "extra_cost": 0},
            "resonant": {"extra_effect": "storm damage +40% per round in resonant rooms", "extra_cost": 0},
        },
        "subclass_id": "nodecaller",
        "effect_params": {"damage_base": 160, "status_effect": "burn", "duration": 4, "magnitude": 1.5},
    },

    # --- Arcanist (resonance + engineering) ---
    "arcanist_pattern_decode": {
        "id": "arcanist_pattern_decode",
        "name": "Pattern Decode",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 0,
        "resource_type": "resonance",
        "cooldown": 4,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Decode the ancient patterns present in the room to"
            " reveal tactical advantage. Grants a significant"
            " combat buff from infrastructure understanding."
            " The Arcanist reads what others walk past."
        ),
        "room_flag_written": None,
        "attuned_variants": {
            "ancient_presence": {"extra_effect": "decode also reveals enemy weaknesses (weaken 3 rounds)", "extra_cost": 10},
        },
        "subclass_id": "arcanist",
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 1.0, "resonance_generated": 20},
    },
    "arcanist_infrastructure_tap": {
        "id": "arcanist_infrastructure_tap",
        "name": "Infrastructure Tap",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "buff",
        "scaling_primary": "resonance",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Tap directly into pre-curse infrastructure buried"
            " beneath the surface. The old systems respond with"
            " power that should not be available. Allies gain"
            " massive buffs, enemies are disrupted. The Arcanist's"
            " defining discovery: the infrastructure still works."
        ),
        "room_flag_written": "resonant",
        "attuned_variants": {
            "ancient_presence": {"extra_effect": "buffs doubled and tap restores 50 resonance", "extra_cost": 0},
        },
        "subclass_id": "arcanist",
        "effect_params": {"buff_type": "haste", "duration": 5, "magnitude": 2.0},
    },

    # --- Sealreader (resonance + remnance) ---
    "sealreader_void_touch": {
        "id": "sealreader_void_touch",
        "name": "Void Touch",
        "domain": "resonance",
        "tier": 3,
        "resource_cost": 60,
        "resource_type": "resonance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "remnance",
        "application_chance": 0.85,
        "description": (
            "Touch the target with resonance drawn from the void"
            " between what is and what was. Damage bypasses"
            " resistance and applies a unique debuff -- reality"
            " itself disagrees with the target's existence."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {
            "void_touched": {"extra_effect": "damage +60% and debuff duration doubled", "extra_cost": 15},
            "corrupted_death": {"extra_effect": "touch also drains 2 stacks per round", "extra_cost": 10},
        },
        "subclass_id": "sealreader",
        "effect_params": {"damage_base": 100, "status_effect": "drain", "duration": 3, "magnitude": 1.0},
    },
    "sealreader_truth_unbound": {
        "id": "sealreader_truth_unbound",
        "name": "Truth Unbound",
        "domain": "resonance",
        "tier": 4,
        "resource_cost": 100,
        "resource_type": "resonance",
        "cooldown": 7,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": "remnance",
        "application_chance": 0.85,
        "description": (
            "Speak a truth the Dragon Curse was designed to hide."
            " Reality convulses. Every enemy in the room takes"
            " catastrophic damage and is stunned. The Circle of"
            " Wizards would kill to suppress this ability. The"
            " Sealreader's most dangerous power: the truth."
        ),
        "room_flag_written": "disrupted",
        "attuned_variants": {
            "corrupted_death": {"extra_effect": "truth resonates -- damage +100% in corrupted rooms", "extra_cost": 0},
            "void_touched": {"extra_effect": "stun duration +2 rounds, enemies cannot be healed", "extra_cost": 0},
        },
        "subclass_id": "sealreader",
        "effect_params": {"damage_base": 230, "status_effect": "stun", "duration": 1, "magnitude": 2.0},
    },

    # ===================================================================
    # NATURALISM DOMAIN POOL (15 abilities) -- resource_type: balance
    # Fingerprint: CALIBRATE -- managed duality, Feral vs Calm spectrum
    # Scaling: naturalism -> resonance
    # Balance is a SPECTRUM: offensive abilities push Feral, defensive
    # abilities push Calm. Both extremes weaken you differently.
    # ===================================================================

    # --- Naturalism Tier 1 (4 abilities) -- Basic nature effects ---
    "thorn_lash": {
        "id": "thorn_lash",
        "name": "Thorn Lash",
        "domain": "naturalism",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "balance",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Lash out with a whip of thorned vine. The simplest"
            " expression of Verdance doctrine: the natural world"
            " answers when you ask. Pushes toward Feral."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 35},
    },
    "wild_mend": {
        "id": "wild_mend",
        "name": "Wild Mend",
        "domain": "naturalism",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Draw upon living energy to close wounds. The forest"
            " gives what it can spare. Healing effectiveness"
            " increases near Calm. Pushes toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"heal_base": 40},
    },
    "feral_strike": {
        "id": "feral_strike",
        "name": "Feral Strike",
        "domain": "naturalism",
        "tier": 1,
        "resource_cost": 10,
        "resource_type": "balance",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Strike with the savagery of a cornered animal. Raw,"
            " unrefined violence drawn from the wild self. Damage"
            " increases near Feral. Pushes toward Feral."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 40},
    },
    "natures_ward": {
        "id": "natures_ward",
        "name": "Nature's Ward",
        "domain": "naturalism",
        "tier": 1,
        "resource_cost": 15,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "A barrier of living energy wraps around you, absorbing"
            " damage briefly. The natural world recognizes its own."
            " Effectiveness increases near Calm. Pushes toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "warding", "duration": 2, "magnitude": 0.12},
    },

    # --- Naturalism Tier 2 (4 abilities) -- Core spectrum management ---
    "bramble_burst": {
        "id": "bramble_burst",
        "name": "Bramble Burst",
        "domain": "naturalism",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "balance",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Thorned vines erupt from the ground, raking everything"
            " nearby. Applies poison on contact -- the natural"
            " world's indifferent cruelty. Pushes toward Feral."
        ),
        "room_flag_written": "overgrown",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 55, "status_effect": "poison", "duration": 3, "magnitude": 8},
    },
    "soothe_the_wild": {
        "id": "soothe_the_wild",
        "name": "Soothe the Wild",
        "domain": "naturalism",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Channel calm into living tissue. A sustained mend"
            " that restores health over several rounds. More"
            " effective near Calm -- the forest heals those who"
            " are at peace. Pushes toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"heal_base": 60},
    },
    "predator_instinct": {
        "id": "predator_instinct",
        "name": "Predator Instinct",
        "domain": "naturalism",
        "tier": 2,
        "resource_cost": 18,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Embrace the predator within. Haste and heightened"
            " reflexes for several rounds. Stronger near Feral."
            " The duality of the Verdance path -- power at a"
            " cost. Pushes toward Feral."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 2, "magnitude": 1.0},
    },
    "entangling_roots": {
        "id": "entangling_roots",
        "name": "Entangling Roots",
        "domain": "naturalism",
        "tier": 2,
        "resource_cost": 20,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Roots surge from beneath the earth to pin the target"
            " in place. The natural world holds what the Verdance"
            " commands. Neutral on the spectrum -- neither Feral"
            " nor Calm, just control."
        ),
        "room_flag_written": "overgrown",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "root", "duration": 2, "magnitude": 1.0},
    },

    # --- Naturalism Tier 3 (4 abilities) -- Advanced nature, DoTs, compounds ---
    "venombloom": {
        "id": "venombloom",
        "name": "Venombloom",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Conjure a bloom of toxic spores that cling to the"
            " target. Sustained poison that worsens each round."
            " The natural world does not distinguish between"
            " healing and harming. Pushes toward Feral."
        ),
        "room_flag_written": "rotting",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 10},
    },
    "lifesurge": {
        "id": "lifesurge",
        "name": "Lifesurge",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "balance",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Flood a target with concentrated life energy. A"
            " powerful burst heal that also grants brief damage"
            " reduction. Dramatically stronger near Calm -- the"
            " forest gives everything when you are at peace."
            " Pushes hard toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"heal_base": 100},
    },
    "rending_thorns": {
        "id": "rending_thorns",
        "name": "Rending Thorns",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Massive thorns erupt through the target, dealing heavy"
            " damage and applying bleed. Nature's violence is not"
            " cruel -- it is indifferent. Pushes toward Feral."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 90, "status_effect": "bleed", "duration": 3, "magnitude": 1},
    },
    "spore_cloud": {
        "id": "spore_cloud",
        "name": "Spore Cloud",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 30,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Release a cloud of choking spores that blankets the"
            " area. All enemies are slowed and weakened as the"
            " spores clog lungs and cloud vision. The forest"
            " does not fight fair. Pushes toward Feral."
        ),
        "room_flag_written": "rotting",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "slow", "duration": 2, "magnitude": 1.0},
    },

    # --- Naturalism Tier 4 (3 abilities) -- Domain capstones ---
    "primal_wrath": {
        "id": "primal_wrath",
        "name": "Primal Wrath",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Unleash the full fury of the wild. Massive damage"
            " to all enemies as thorns, roots, and venom erupt"
            " simultaneously. Applies poison and bleed. Only"
            " available deep in Feral -- the cost of this power"
            " is control. Requires Feral balance."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 180, "status_effect": "poison", "duration": 3, "magnitude": 10},
    },
    "ancient_restoration": {
        "id": "ancient_restoration",
        "name": "Ancient Restoration",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Channel the oldest living energy in the world. A"
            " massive group heal that also removes one negative"
            " status effect per ally. The Ancient Voice speaks"
            " and the wounded rise. Requires Calm balance."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"heal_base": 200},
    },
    "natures_equilibrium": {
        "id": "natures_equilibrium",
        "name": "Nature's Equilibrium",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "balance",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Achieve perfect balance between Feral and Calm."
            " For several rounds, all naturalism abilities deal"
            " full damage AND full healing regardless of spectrum"
            " position. The Verdance ideal: mastery is not"
            " choosing a side. Requires neutral Balance."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.5},
    },

    # ===================================================================
    # NATURALISM-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets a Tier 3 enhanced blend + Tier 4 defining ability
    # ===================================================================

    # --- Thornfist (naturalism + combat) ---
    "thornfist_nature_fist": {
        "id": "thornfist_nature_fist",
        "name": "Nature Fist",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "balance",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": "combat",
        "application_chance": 0.90,
        "description": (
            "Drive a fist wrapped in living thorns into the target."
            " Physical strike that applies poison on contact."
            " Shapeshift-adjacent -- your body IS the weapon."
            " Pushes toward Feral."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": "thornfist",
        "effect_params": {"damage_base": 85, "status_effect": "poison", "duration": 3, "magnitude": 8},
    },
    "thornfist_primal_shift": {
        "id": "thornfist_primal_shift",
        "name": "Primal Shift",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Temporarily transform into something between human"
            " and predator. Massive stat buffs -- strength and"
            " damage amplified, natural armor, every strike"
            " applies nature DoTs. The Thornfist's defining"
            " moment: the body becomes the forest itself."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": "thornfist",
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 2.0},
    },

    # --- Rootstalker (naturalism + subterfuge) ---
    "rootstalker_vine_ambush": {
        "id": "rootstalker_vine_ambush",
        "name": "Vine Ambush",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": "subterfuge",
        "application_chance": 0.85,
        "description": (
            "Vines erupt from concealment to ensnare and damage"
            " the target. Stealth-delivered nature attack that"
            " roots the target. The wilderness ghost strikes"
            " through the terrain itself. Pushes toward Feral."
        ),
        "room_flag_written": "overgrown",
        "attuned_variants": {},
        "subclass_id": "rootstalker",
        "effect_params": {"damage_base": 85, "status_effect": "root", "duration": 2, "magnitude": 1.0},
    },
    "rootstalker_one_with_wilds": {
        "id": "rootstalker_one_with_wilds",
        "name": "One With the Wilds",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "subterfuge",
        "application_chance": 1.0,
        "description": (
            "Merge with the natural environment. Sustained outdoor"
            " stealth with evasion and a poison aura that damages"
            " nearby enemies each round. Attacks do not break"
            " concealment. The Rootstalker's defining state:"
            " the wilderness moves through you."
        ),
        "room_flag_written": "overgrown",
        "attuned_variants": {},
        "subclass_id": "rootstalker",
        "effect_params": {"buff_type": "evasion", "duration": 4, "magnitude": 0.3},
    },

    # --- Cantera (naturalism + resonance) ---
    "cantera_ancient_grove": {
        "id": "cantera_ancient_grove",
        "name": "Ancient Grove",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": "resonance",
        "application_chance": 1.0,
        "description": (
            "Call upon the memory of ancient forests to heal and"
            " strengthen. Node energy accelerates living magic."
            " Heals the group and grants a damage reduction buff."
            " Stronger in nature zones. Pushes toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "cantera",
        "effect_params": {"heal_base": 90},
    },
    "cantera_forest_memory": {
        "id": "cantera_forest_memory",
        "name": "Forest Memory",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": "resonance",
        "application_chance": 1.0,
        "description": (
            "Channel the resonance of every forest that has ever"
            " lived. Massive group heal amplified by the resonance"
            " stat. Grants nature damage resistance and a buff"
            " that persists for multiple rounds. The Cantera's"
            " defining power: nature via old magic."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "cantera",
        "effect_params": {"heal_base": 180},
    },

    # --- Stormcaller (naturalism + arcana) ---
    "stormcaller_lightning_strike": {
        "id": "stormcaller_lightning_strike",
        "name": "Lightning Strike",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": "arcana",
        "application_chance": 0.90,
        "description": (
            "Call a bolt of lightning down on the target. Deals"
            " heavy damage, applies wet status from driving rain,"
            " and writes a charged flag to the room. Elemental"
            " forces bent to will. Pushes toward Feral."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "stormcaller",
        "effect_params": {"damage_base": 95, "status_effect": "wet", "duration": 2, "magnitude": 1.0},
    },
    "stormcaller_storm_call": {
        "id": "stormcaller_storm_call",
        "name": "Storm Call",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 2,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": "arcana",
        "application_chance": 0.85,
        "description": (
            "Summon a devastating storm. Two rounds of gathering"
            " wind, then catastrophic AoE damage. Every enemy"
            " is struck by lightning and drenched. Applies burn"
            " and wet simultaneously. The room becomes charged."
            " The Stormcaller's ultimate: the sky itself answers."
        ),
        "room_flag_written": "charged",
        "attuned_variants": {},
        "subclass_id": "stormcaller",
        "effect_params": {"damage_base": 220, "status_effect": "burn", "duration": 3, "magnitude": 10},
    },

    # --- Greentongue (naturalism + diplomacy) ---
    "greentongue_natures_voice": {
        "id": "greentongue_natures_voice",
        "name": "Nature's Voice",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.85,
        "description": (
            "Speak with the authority of the natural world. The"
            " target's resolve weakens under the weight of something"
            " older than civilization. Presence and nature blend"
            " into a social weapon. Pushes toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "greentongue",
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "greentongue_forest_decree": {
        "id": "greentongue_forest_decree",
        "name": "Forest Decree",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.75,
        "description": (
            "Issue a command that the living world enforces."
            " All nature-aligned creatures and beasts in the room"
            " are charmed. Non-natural enemies are weakened as"
            " the forest itself turns hostile. Presence scaling"
            " amplifies the reach. The Greentongue's voice."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "greentongue",
        "effect_params": {"debuff_type": "charm", "duration": 2, "magnitude": 1.5},
    },

    # --- Rotweald (naturalism + alchemy) ---
    "rotweald_rot_cloud": {
        "id": "rotweald_rot_cloud",
        "name": "Rot Cloud",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "naturalism",
        "scaling_secondary": "alchemy",
        "application_chance": 0.85,
        "description": (
            "Release a cloud of organic decay that clings to"
            " everything it touches. AoE poison and bleed as"
            " flesh rots on contact. The dark side of nature --"
            " decomposition weaponized. Pushes toward Feral."
        ),
        "room_flag_written": "rotting",
        "attuned_variants": {},
        "subclass_id": "rotweald",
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 10},
    },
    "rotweald_consuming_decay": {
        "id": "rotweald_consuming_decay",
        "name": "Consuming Decay",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "naturalism",
        "scaling_secondary": "alchemy",
        "application_chance": 0.80,
        "description": (
            "Transform the room into a zone of sustained organic"
            " decay. Every enemy receives poison and weaken each"
            " round for the duration. The ground itself rots."
            " The Rotweald's defining power: nature does not"
            " always grow -- sometimes it consumes."
        ),
        "room_flag_written": "rotting",
        "attuned_variants": {},
        "subclass_id": "rotweald",
        "effect_params": {"status_effect": "poison", "duration": 5, "magnitude": 15},
    },

    # --- Wildcommand (naturalism + tactics) ---
    "wildcommand_beast_rush": {
        "id": "wildcommand_beast_rush",
        "name": "Beast Rush",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "naturalism",
        "scaling_secondary": "tactics",
        "application_chance": 0.90,
        "description": (
            "Command local predators to assault the target. A"
            " coordinated beast attack that deals heavy damage."
            " Tactical knowledge expressed through animal"
            " direction. Pushes toward Feral."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": "wildcommand",
        "effect_params": {"damage_base": 90},
    },
    "wildcommand_pack_alpha": {
        "id": "wildcommand_pack_alpha",
        "name": "Pack Alpha",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 50,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "tactics",
        "application_chance": 1.0,
        "description": (
            "Summon a sustained beast companion that fights"
            " alongside you with tactical intelligence. The beast"
            " deals damage each round, grants allies a damage"
            " bonus, and obeys complex orders. The Wildcommand's"
            " defining power: the forest is your army."
        ),
        "room_flag_written": "fading_life",
        "attuned_variants": {},
        "subclass_id": "wildcommand",
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 1.5},
    },

    # --- Growthwright (naturalism + engineering) ---
    "growthwright_living_barricade": {
        "id": "growthwright_living_barricade",
        "name": "Living Barricade",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Grow a wall of living wood that shields allies."
            " Significant damage reduction for the group as"
            " organic construction absorbs incoming force."
            " The structure persists and regenerates."
            " Pushes toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "growthwright",
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.25},
    },
    "growthwright_grove_fortress": {
        "id": "growthwright_grove_fortress",
        "name": "Grove Fortress",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "engineering",
        "application_chance": 1.0,
        "description": (
            "Grow a sustained living fortification that transforms"
            " the battlefield. Heavy damage reduction for all"
            " allies, enemies slowed inside the grove, and the"
            " structure heals itself each round. The Growthwright's"
            " defining power: you grow what others build."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "growthwright",
        "effect_params": {"buff_type": "warding", "duration": 4, "magnitude": 0.35},
    },

    # --- Deeproot (naturalism + remnance) ---
    "deeproot_deep_memory": {
        "id": "deeproot_deep_memory",
        "name": "Deep Memory",
        "domain": "naturalism",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "balance",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "naturalism",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Tap into the memory stored in ancient root systems."
            " Grants a damage and defense buff drawn from the"
            " world's oldest living knowledge. Dragon-adjacent"
            " nature power that should not exist. Pushes"
            " toward Calm."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "deeproot",
        "effect_params": {"buff_type": "warding", "duration": 3, "magnitude": 0.2},
    },
    "deeproot_worldroot_pulse": {
        "id": "deeproot_worldroot_pulse",
        "name": "Worldroot Pulse",
        "domain": "naturalism",
        "tier": 4,
        "resource_cost": 55,
        "resource_type": "balance",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "heal",
        "scaling_primary": "naturalism",
        "scaling_secondary": "remnance",
        "application_chance": 1.0,
        "description": (
            "Pulse energy through the deepest root network in"
            " the world. Massive group heal amplified by echoes"
            " of ancient nature. Grants sustained regeneration"
            " and a nature buff that persists for rounds. The"
            " Deeproot's defining power: the world-memory in"
            " old growth, made real."
        ),
        "room_flag_written": "living_wood",
        "attuned_variants": {},
        "subclass_id": "deeproot",
        "effect_params": {"heal_base": 200},
    },

    # ===================================================================
    # ALCHEMY DOMAIN POOL (15 abilities) -- resource_type: reagents
    # Fingerprint: PREPARE -- preparation as combat philosophy
    # Scaling: alchemy -> acuity
    # Reagents are PRE-CRAFTED CONSUMABLES. Costs represent actual stock
    # depletion. Running out mid-fight is a design-intended failure state.
    # ===================================================================

    # --- Alchemy Tier 1 (4 abilities) -- Basic compounds ---
    "reagent_toss": {
        "id": "reagent_toss",
        "name": "Reagent Toss",
        "domain": "alchemy",
        "tier": 1,
        "resource_cost": 5,
        "resource_type": "reagents",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Hurl a basic reactive compound at the target. The"
            " cheapest expenditure in the Thornwork arsenal --"
            " but every reagent spent is a reagent gone. This"
            " is the cost of preparation."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 35},
    },
    "acid_flask": {
        "id": "acid_flask",
        "name": "Acid Flask",
        "domain": "alchemy",
        "tier": 1,
        "resource_cost": 8,
        "resource_type": "reagents",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Lob a flask of concentrated acid. Burns on contact"
            " and weakens armor. A staple of the Thornwork"
            " brewer's kit -- reliable, efficient, finite."
        ),
        "room_flag_written": "caustic",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 40, "status_effect": "burn", "duration": 2, "magnitude": 7},
    },
    "smoke_screen": {
        "id": "smoke_screen",
        "name": "Smoke Screen",
        "domain": "alchemy",
        "tier": 1,
        "resource_cost": 8,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Deploy a chemical smoke compound that blinds enemies"
            " in the area. Visibility drops to nothing -- bought"
            " with preparation, not magic."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "blind", "duration": 2, "magnitude": 1.0},
    },
    "venom_coat": {
        "id": "venom_coat",
        "name": "Venom Coat",
        "domain": "alchemy",
        "tier": 1,
        "resource_cost": 7,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "status",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Coat your weapon with a prepared toxin. The next"
            " several melee strikes apply poison. Pre-crafted"
            " and precise -- the Thornwork way."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"status_effect": "poison", "duration": 3, "magnitude": 8},
    },

    # --- Alchemy Tier 2 (4 abilities) -- Core alchemy ---
    "caustic_compound": {
        "id": "caustic_compound",
        "name": "Caustic Compound",
        "domain": "alchemy",
        "tier": 2,
        "resource_cost": 12,
        "resource_type": "reagents",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Apply a sustained-release chemical burn. The compound"
            " eats through armor and flesh over multiple rounds."
            " Acuity determines how precisely the mixture was"
            " calibrated before the fight."
        ),
        "room_flag_written": "caustic",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"status_effect": "burn", "duration": 3, "magnitude": 8},
    },
    "concentrated_toxin": {
        "id": "concentrated_toxin",
        "name": "Concentrated Toxin",
        "domain": "alchemy",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Deliver a concentrated poison compound. Higher potency"
            " than standard venom -- the result of careful"
            " preparation. Stacks with existing poison effects."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 10},
    },
    "flashpowder": {
        "id": "flashpowder",
        "name": "Flashpowder",
        "domain": "alchemy",
        "tier": 2,
        "resource_cost": 12,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Hurl a prepared flashpowder charge. The burst blinds"
            " and staggers all enemies in the area. A single"
            " handful buys precious seconds -- spend wisely."
        ),
        "room_flag_written": "burning",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "blind", "duration": 2, "magnitude": 1.0},
    },
    "strengthening_draught": {
        "id": "strengthening_draught",
        "name": "Strengthening Draught",
        "domain": "alchemy",
        "tier": 2,
        "resource_cost": 15,
        "resource_type": "reagents",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "Drink a pre-prepared alchemical draught. Haste and"
            " damage resistance for several rounds. The finest"
            " preparation happens before the fight begins."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.0},
    },

    # --- Alchemy Tier 3 (4 abilities) -- Advanced compounds ---
    "blistering_mixture": {
        "id": "blistering_mixture",
        "name": "Blistering Mixture",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.85,
        "description": (
            "Hurl a compound that burns and poisons simultaneously."
            " Two status effects from a single prepared mixture."
            " The Thornworker's craft: maximum effect from"
            " minimum reagent expenditure."
        ),
        "room_flag_written": "burning",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 80, "status_effect": "burn", "duration": 3, "magnitude": 10},
    },
    "weakening_agent": {
        "id": "weakening_agent",
        "name": "Weakening Agent",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.80,
        "description": (
            "Deploy a chemical agent that saps physical strength."
            " The target weakens significantly as the compound"
            " enters their system. Preparation over improvisation."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "weaken", "duration": 3, "magnitude": 0.2},
    },
    "paralytic_compound": {
        "id": "paralytic_compound",
        "name": "Paralytic Compound",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "reagents",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.75,
        "description": (
            "Apply a nerve agent that locks muscles in place."
            " The target is slowed and rooted as the paralytic"
            " takes hold. Expensive to prepare, devastating"
            " when it lands."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"debuff_type": "slow", "duration": 3, "magnitude": 1.0},
    },
    "volatile_concoction": {
        "id": "volatile_concoction",
        "name": "Volatile Concoction",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 25,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Mix a volatile compound mid-combat and hurl it."
            " One round to combine ingredients, then devastating"
            " area damage. The complex mixture requires precision"
            " -- acuity determines the blast radius."
        ),
        "room_flag_written": "burning",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 110},
    },

    # --- Alchemy Tier 4 (3 abilities) -- Domain capstones ---
    "transmuters_masterwork": {
        "id": "transmuters_masterwork",
        "name": "Transmuter's Masterwork",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 35,
        "resource_type": "reagents",
        "cooldown": 5,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 0.90,
        "description": (
            "Deploy the Transmuter's finest creation. A compound"
            " that applies poison, burn, and weaken simultaneously."
            " The ceiling of alchemical craft -- three effects"
            " from one prepared mixture. Devastating and finite."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 150, "status_effect": "poison", "duration": 4, "magnitude": 12},
    },
    "alchemists_perfection": {
        "id": "alchemists_perfection",
        "name": "Alchemist's Perfection",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 40,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "The masterwork compound. One round to combine the"
            " rarest reagents, then a single devastating payload"
            " that deals massive area damage and saturates the"
            " room with persistent toxins. The Transmuter's"
            " ultimate expression: chemistry as annihilation."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"damage_base": 220},
    },
    "reagent_mastery": {
        "id": "reagent_mastery",
        "name": "Reagent Mastery",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 30,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "alchemy",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": (
            "The master alchemist's efficiency. For the duration,"
            " all alchemy abilities cost half reagents and apply"
            " double status effect stacks. The difference between"
            " a brewer and a Transmuter: preparation mastery."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": None,
        "effect_params": {"buff_type": "haste", "duration": 3, "magnitude": 1.5},
    },

    # ===================================================================
    # ALCHEMY-PRIMARY SUBCLASS SIGNATURES (18 abilities = 9 x 2)
    # Each subclass gets a Tier 3 enhanced blend + Tier 4 defining ability
    # ===================================================================

    # --- Venomfang (alchemy + combat) ---
    "venomfang_toxic_bite": {
        "id": "venomfang_toxic_bite",
        "name": "Toxic Bite",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 18,
        "resource_type": "reagents",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "combat",
        "application_chance": 0.90,
        "description": (
            "A melee strike with an envenomed blade that applies"
            " both bleed and poison simultaneously. Highest melee"
            " poison application rate in the game. The Venomfang"
            " bleeds and poisons with every cut."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "venomfang",
        "effect_params": {"damage_base": 80, "status_effect": "poison", "duration": 3, "magnitude": 10},
    },
    "venomfang_apex_predator": {
        "id": "venomfang_apex_predator",
        "name": "Apex Predator",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 30,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "buff",
        "scaling_primary": "alchemy",
        "scaling_secondary": "combat",
        "application_chance": 1.0,
        "description": (
            "Inject yourself with a combat stimulant that pushes"
            " your body beyond its limits. For the duration,"
            " every melee attack applies double poison stacks"
            " and bleed simultaneously. The Venomfang's defining"
            " moment: sustained chemical-fueled aggression."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "venomfang",
        "effect_params": {"buff_type": "haste", "duration": 4, "magnitude": 2.0},
    },

    # --- Nightshade (alchemy + subterfuge) ---
    "nightshade_silent_toxin": {
        "id": "nightshade_silent_toxin",
        "name": "Silent Toxin",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 18,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "subterfuge",
        "application_chance": 0.90,
        "description": (
            "Apply poison from concealment. The target does not"
            " realize they have been dosed until the toxin takes"
            " hold. Delivered from stealth without breaking"
            " Vanish. Patient, precise, never seen."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "nightshade",
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 12},
    },
    "nightshade_midnight_bloom": {
        "id": "nightshade_midnight_bloom",
        "name": "Midnight Bloom",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 35,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "subterfuge",
        "application_chance": 0.85,
        "description": (
            "Apply a delayed-onset toxin of devastating potency."
            " The poison lies dormant for three rounds, then"
            " blooms into massive damage. The target feels nothing"
            " until it is too late. The Nightshade's defining"
            " power: the kill that was decided before the fight."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": "nightshade",
        "effect_params": {"status_effect": "poison", "duration": 5, "magnitude": 15},
    },

    # --- Mireweald (alchemy + naturalism) ---
    "mireweald_swamp_rot": {
        "id": "mireweald_swamp_rot",
        "name": "Swamp Rot",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "naturalism",
        "application_chance": 0.85,
        "description": (
            "Release a compound derived from swamp decay. Area"
            " poison and slow as organic filth clogs and corrodes."
            " The Mireweald approach: where Rotweald grows decay,"
            " you distill and weaponize it."
        ),
        "room_flag_written": "rotting",
        "attuned_variants": {},
        "subclass_id": "mireweald",
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 10},
    },
    "mireweald_mire_zone": {
        "id": "mireweald_mire_zone",
        "name": "Mire Zone",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 40,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "naturalism",
        "application_chance": 0.80,
        "description": (
            "Saturate the terrain with toxic organic compounds."
            " The room becomes a mire -- every enemy takes"
            " poison damage and is slowed each round. Sustained"
            " terrain poisoning. The Mireweald's defining power:"
            " the ground itself rejects your enemies."
        ),
        "room_flag_written": "rotting",
        "attuned_variants": {},
        "subclass_id": "mireweald",
        "effect_params": {"status_effect": "poison", "duration": 5, "magnitude": 15},
    },

    # --- Voidbrewer (alchemy + resonance) ---
    "voidbrewer_resonant_compound": {
        "id": "voidbrewer_resonant_compound",
        "name": "Resonant Compound",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "resonance",
        "application_chance": 0.85,
        "description": (
            "Deploy a compound that interacts with ambient node"
            " energy. Poison amplified when room flags are present."
            " Writes a resonant flag. The Voidbrewer creates"
            " conditions that empower their own future attacks."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {
            "resonant": {"extra_effect": "poison duration +2 rounds", "extra_cost": 5},
        },
        "subclass_id": "voidbrewer",
        "effect_params": {"damage_base": 80, "status_effect": "poison", "duration": 3, "magnitude": 10},
    },
    "voidbrewer_old_world_brew": {
        "id": "voidbrewer_old_world_brew",
        "name": "Old World Brew",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 40,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "resonance",
        "application_chance": 0.85,
        "description": (
            "Combine reagents with old magic resonance. One round"
            " to mix a compound that predates modern alchemy."
            " Room flag amplified -- devastating in charged or"
            " resonant rooms. The Voidbrewer's defining power:"
            " alchemy that touches what the nodes remember."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {
            "resonant": {"extra_effect": "damage +80%, all status durations +2", "extra_cost": 10},
            "charged": {"extra_effect": "burn added, all enemies stunned 1 round", "extra_cost": 8},
        },
        "subclass_id": "voidbrewer",
        "effect_params": {"damage_base": 160, "status_effect": "poison", "duration": 4, "magnitude": 12},
    },

    # --- Fumecaster (alchemy + arcana) ---
    "fumecaster_poison_bolt": {
        "id": "fumecaster_poison_bolt",
        "name": "Poison Bolt",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 18,
        "resource_type": "reagents",
        "cooldown": 1,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "arcana",
        "application_chance": 0.90,
        "description": (
            "Deliver an alchemical payload through a magical"
            " vector. Ranged poison delivery that bypasses"
            " melee range restrictions. Spell-delivered toxin"
            " -- the Fumecaster's signature ranged attack."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": "fumecaster",
        "effect_params": {"damage_base": 80, "status_effect": "poison", "duration": 3, "magnitude": 10},
    },
    "fumecaster_noxious_storm": {
        "id": "fumecaster_noxious_storm",
        "name": "Noxious Storm",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 40,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "arcana",
        "application_chance": 0.85,
        "description": (
            "Conjure a storm of alchemical poison delivered"
            " through arcane force. One round to prepare, then"
            " AoE ranged poison and burn. Every enemy is hit"
            " regardless of position. The Fumecaster's defining"
            " power: melee toxins given devastating range."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "fumecaster",
        "effect_params": {"damage_base": 180, "status_effect": "burn", "duration": 3, "magnitude": 10},
    },

    # --- Sweetpoison (alchemy + diplomacy) ---
    "sweetpoison_honeyed_words": {
        "id": "sweetpoison_honeyed_words",
        "name": "Honeyed Words",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 18,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "debuff",
        "scaling_primary": "alchemy",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.85,
        "description": (
            "Engage the target socially while applying a contact"
            " poison. Charm and poison delivered simultaneously."
            " Social access as delivery mechanism -- the charming"
            " poisoner's opening gambit."
        ),
        "room_flag_written": None,
        "attuned_variants": {},
        "subclass_id": "sweetpoison",
        "effect_params": {"debuff_type": "charm", "duration": 1, "magnitude": 1.0},
    },
    "sweetpoison_killing_kindness": {
        "id": "sweetpoison_killing_kindness",
        "name": "Killing Kindness",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 35,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "diplomacy",
        "application_chance": 0.80,
        "description": (
            "Charm the target into lowering their guard, then"
            " apply a delayed lethal compound. The charmed target"
            " takes no hostile action for one round while the"
            " poison builds to critical levels. The Sweetpoison's"
            " defining power: kindness that kills."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": "sweetpoison",
        "effect_params": {"status_effect": "poison", "duration": 5, "magnitude": 15},
    },

    # --- Plaguecommand (alchemy + tactics) ---
    "plaguecommand_gas_deployment": {
        "id": "plaguecommand_gas_deployment",
        "name": "Gas Deployment",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 3,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "tactics",
        "application_chance": 0.85,
        "description": (
            "Deploy a tactical gas compound across the battlefield."
            " Area poison and weaken as the chemical agent"
            " saturates the space. Tactical toxicology -- area"
            " denial through chemistry."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "plaguecommand",
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 10},
    },
    "plaguecommand_scorched_earth": {
        "id": "plaguecommand_scorched_earth",
        "name": "Scorched Earth",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "tactics",
        "application_chance": 0.80,
        "description": (
            "Saturate the entire room with layered chemical"
            " agents. Poison, burn, and slow applied to all"
            " enemies each round for the duration. Massive area"
            " denial that makes the room uninhabitable. The"
            " Plaguecommand's defining power: tactical"
            " toxicology at its absolute worst."
        ),
        "room_flag_written": "burning",
        "attuned_variants": {},
        "subclass_id": "plaguecommand",
        "effect_params": {"status_effect": "poison", "duration": 5, "magnitude": 15},
    },

    # --- Fumewright (alchemy + engineering) ---
    "fumewright_gas_trap": {
        "id": "fumewright_gas_trap",
        "name": "Gas Trap",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 4,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "engineering",
        "application_chance": 0.85,
        "description": (
            "Place a concealed chemical device that triggers when"
            " an enemy acts. Deals damage and applies poison."
            " Built with precision, armed with patience. The"
            " Fumewright constructs what others merely toss."
        ),
        "room_flag_written": "toxic_air",
        "attuned_variants": {},
        "subclass_id": "fumewright",
        "effect_params": {"damage_base": 85, "status_effect": "poison", "duration": 3, "magnitude": 10},
    },
    "fumewright_chemical_engine": {
        "id": "fumewright_chemical_engine",
        "name": "Chemical Engine",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 1,
        "effect_type": "damage",
        "scaling_primary": "alchemy",
        "scaling_secondary": "engineering",
        "application_chance": 0.90,
        "description": (
            "Construct a sustained chemical delivery device."
            " One round to assemble, then the engine releases"
            " toxins each round -- poison and burn to all"
            " enemies in the room for the duration. The"
            " Fumewright's defining power: a machine that"
            " does the poisoning for you."
        ),
        "room_flag_written": "burning",
        "attuned_variants": {},
        "subclass_id": "fumewright",
        "effect_params": {"damage_base": 160, "status_effect": "poison", "duration": 4, "magnitude": 12},
    },

    # --- Firstblight (alchemy + remnance) ---
    "firstblight_ancient_venom": {
        "id": "firstblight_ancient_venom",
        "name": "Ancient Venom",
        "domain": "alchemy",
        "tier": 3,
        "resource_cost": 20,
        "resource_type": "reagents",
        "cooldown": 2,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "remnance",
        "application_chance": 0.90,
        "description": (
            "Apply a toxin derived from pre-curse knowledge."
            " Higher poison ceiling than standard compounds --"
            " this venom interacts with something the dragon"
            " magic left behind. Ancient poison that modern"
            " alchemy cannot replicate."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": "firstblight",
        "effect_params": {"status_effect": "poison", "duration": 4, "magnitude": 12},
    },
    "firstblight_dragon_blight": {
        "id": "firstblight_dragon_blight",
        "name": "Dragon Blight",
        "domain": "alchemy",
        "tier": 4,
        "resource_cost": 45,
        "resource_type": "reagents",
        "cooldown": 6,
        "charge_turns": 0,
        "effect_type": "dot",
        "scaling_primary": "alchemy",
        "scaling_secondary": "remnance",
        "application_chance": 0.85,
        "description": (
            "Unleash a toxin that should not exist in the modern"
            " world. Dragon-adjacent alchemy that scales with"
            " echoes. Massive sustained poison that worsens each"
            " round. Weakens the target as the ancient compound"
            " unravels their defenses. The Firstblight's defining"
            " power: something old in the poison."
        ),
        "room_flag_written": "poisoned_air",
        "attuned_variants": {},
        "subclass_id": "firstblight",
        "effect_params": {"status_effect": "poison", "duration": 5, "magnitude": 15},
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
