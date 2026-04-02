"""
Skill definitions registry for Soravelon.

Pure-data module defining all general proficiency skills, ancestry seed values,
trainer framework, diminishing returns brackets, and discovery triggers.
Skills are independent of the domain/guild system (SKL-04).

Each skill has a 0-100 scale with three improvement methods:
- Passive use: ndb accumulators batched to DB every 10 successful uses
- Deliberate practice: 24hr rolling cooldown per skill, tier-based gains
- Trainer sessions: NPC-driven, costs Scales, enhances next practice
"""

# --- Diminishing Returns (same curve as domain XP per D-19) ---

DIMINISHING_BRACKETS = [
    (0, 25, 1.0),      # full rate
    (26, 50, 0.75),    # 75%
    (51, 75, 0.40),    # 40%
    (76, 90, 0.10),    # 10%
    (91, 100, 0.02),   # 2%
]

# --- Practice Gains by Tier ---

PRACTICE_GAINS = [
    (0, 25, 3.0, 5.0),     # (min_skill, max_skill, min_gain, max_gain)
    (26, 50, 2.0, 4.0),
    (51, 75, 1.0, 3.0),
    (76, 90, 0.5, 1.0),
    (91, 100, 0.1, 0.3),
]

# --- Passive Accumulator Threshold ---
# 10 successful uses = +0.1 skill value (before diminishing rate)
PASSIVE_ACCUMULATOR_THRESHOLD = 10
PASSIVE_GAIN_PER_THRESHOLD = 0.1

# --- Skill Definitions (D-16 through D-25) ---

SKILL_DEFINITIONS = {
    "lockpicking": {
        "name": "Lockpicking",
        "skill_type": "general",
        "description": "Pick locks and bypass mechanical security.",
        "domain_bonus": "subterfuge",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Basic locks opened without tools",
            50: "Complex locks, some magical wards",
            75: "Master locks, warded containers",
            90: "Dragon-era locks, ancient mechanisms",
            100: "Any lock in the known world",
        },
    },
    "animal_handling": {
        "name": "Animal Handling",
        "skill_type": "general",
        "description": "Calm, direct, and work with mundane animals.",
        "domain_bonus": "naturalism",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Domestic animals respond to basic commands",
            50: "Wild animals can be calmed or redirected",
            75: "Predators hesitate; pack animals follow willingly",
            90: "Even territorial beasts defer to your presence",
            100: "Any natural creature treats you as kin",
        },
    },
    "beast_training": {
        "name": "Beast Training",
        "skill_type": "general",
        "description": "Train and condition beasts for specific tasks.",
        "domain_bonus": "naturalism",
        "trainer_required_above": 75,
        "thresholds": {
            25: "Simple tricks and obedience",
            50: "Guard, fetch, and patrol behaviors",
            75: "Complex multi-step task chains",
            90: "War-trained beasts obey under duress",
            100: "Dragon-era training techniques recovered",
        },
    },
    "herbalism": {
        "name": "Herbalism",
        "skill_type": "general",
        "description": "Identify, gather, and prepare medicinal plants.",
        "domain_bonus": "alchemy",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Common herbs identified on sight",
            50: "Poultices and basic remedies prepared",
            75: "Rare reagents harvested without damage",
            90: "Node-touched flora handled safely",
            100: "Lost remedies of the Dragon-era reproduced",
        },
    },
    "tracking": {
        "name": "Tracking",
        "skill_type": "general",
        "description": "Follow tracks and signs to locate creatures or people.",
        "domain_bonus": "naturalism",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Fresh tracks in soft ground",
            50: "Day-old tracks, broken branches, disturbed earth",
            75: "Tracks on stone, through water, in dense forest",
            90: "Week-old trails, magical concealment partially pierced",
            100: "No quarry escapes your eye",
        },
    },
    "climbing": {
        "name": "Climbing",
        "skill_type": "general",
        "description": "Scale walls, cliffs, and structures.",
        "domain_bonus": "combat",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Rough walls and low cliffs",
            50: "Smooth stone, rain-slick surfaces",
            75: "Sheer vertical faces, overhangs",
            90: "Dragon-era tower spires, crumbling ruins",
            100: "Any surface, any conditions",
        },
    },
    "persuasion": {
        "name": "Persuasion",
        "skill_type": "general",
        "description": "Convince others through logic, charm, or emotional appeal.",
        "domain_bonus": "diplomacy",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Friendly NPCs sway easily",
            50: "Neutral parties consider your arguments",
            75: "Hostile NPCs pause before acting",
            90: "Faction leaders take your counsel seriously",
            100: "Even sworn enemies hear you out",
        },
    },
    "intimidation": {
        "name": "Intimidation",
        "skill_type": "general",
        "description": "Coerce through threat, presence, or reputation.",
        "domain_bonus": "combat",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Common folk step aside",
            50: "Guards think twice about confrontation",
            75: "Veteran soldiers feel uneasy",
            90: "Named enemies reconsider engagement",
            100: "Your reputation precedes you everywhere",
        },
    },
    "swimming": {
        "name": "Swimming",
        "skill_type": "general",
        "description": "Navigate water, dive, and endure currents.",
        "domain_bonus": "naturalism",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Calm waters, short distances",
            50: "Moderate currents, extended swims",
            75: "Rapids, deep dives, cold water endurance",
            90: "Open sea, underwater exploration",
            100: "Any body of water, any conditions",
        },
    },
    "first_aid": {
        "name": "First Aid",
        "skill_type": "general",
        "description": "Treat wounds, stabilize injuries, and apply field medicine.",
        "domain_bonus": "alchemy",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Stop bleeding, clean wounds",
            50: "Set bones, treat burns, prevent infection",
            75: "Field surgery, antivenom application",
            90: "Stabilize mortal wounds, node-sickness treatment",
            100: "Miraculous recoveries through skill alone",
        },
    },
    "appraisal": {
        "name": "Appraisal",
        "skill_type": "general",
        "description": "Assess the value, quality, and properties of items.",
        "domain_bonus": "diplomacy",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Common goods valued accurately",
            50: "Magical properties detected, rarity assessed",
            75: "Hidden enchantments revealed, forgeries spotted",
            90: "Dragon-era artifact provenance identified",
            100: "No item holds secrets from you",
        },
    },
    "stealth": {
        "name": "Stealth",
        "skill_type": "general",
        "description": "Move unseen and unheard.",
        "domain_bonus": "subterfuge",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Shadows and darkness hide you from casual observation",
            50: "Move silently on most surfaces",
            75: "Pass guards, avoid magical detection zones",
            90: "Near-invisible in any environment",
            100: "Legends speak of your shadow",
        },
    },
    "foraging": {
        "name": "Foraging",
        "skill_type": "general",
        "description": "Find food, water, and useful materials in the wild.",
        "domain_bonus": "naturalism",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Edible plants and clean water found reliably",
            50: "Rare mushrooms, mineral deposits spotted",
            75: "Hidden caches, seasonal rarities located",
            90: "Node-influenced resources identified",
            100: "The land provides whatever you need",
        },
    },
    "node_reading": {
        "name": "Node Reading",
        "skill_type": "general",
        "description": "Sense and interpret magical node energy patterns.",
        "domain_bonus": "resonance",
        "trainer_required_above": 75,
        "thresholds": {
            25: "Active nodes felt at close range",
            50: "Node state assessed (dormant/active/critical)",
            75: "Failure probability estimated, safe paths identified",
            90: "Node behavior predicted minutes ahead",
            100: "Dragon-era node schematics intuited from energy flow",
        },
    },
    "navigation": {
        "name": "Navigation",
        "skill_type": "general",
        "description": "Find your way through unfamiliar territory.",
        "domain_bonus": "tactics",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Trails and marked paths followed reliably",
            50: "Cross-country travel without getting lost",
            75: "Navigate underground, in fog, or at night",
            90: "Dragon-era waypoint networks sensed",
            100: "You always know exactly where you are",
        },
    },
    "fishing": {
        "name": "Fishing",
        "skill_type": "general",
        "description": "Catch fish and aquatic creatures.",
        "domain_bonus": "naturalism",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Common fish in calm waters",
            50: "Deeper waters, bait selection, seasonal patterns",
            75: "Rare species, difficult conditions",
            90: "Node-touched aquatic life safely handled",
            100: "Legendary catches that others only dream of",
        },
    },
    "engineering": {
        "name": "Engineering",
        "skill_type": "general",
        "description": "Design, build, and repair mechanical devices and structures.",
        "domain_bonus": "engineering",
        "trainer_required_above": 75,
        "thresholds": {
            25: "Simple repairs and basic construction",
            50: "Mechanical traps, bridges, fortifications",
            75: "Complex machinery, siege equipment",
            90: "Dragon-era mechanisms partially understood",
            100: "Lost engineering secrets recovered",
        },
    },
    "cooking": {
        "name": "Cooking",
        "skill_type": "general",
        "description": "Prepare meals that provide temporary buffs and restore stamina.",
        "domain_bonus": "alchemy",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Trail rations that don't taste terrible",
            50: "Meals that restore stamina and morale",
            75: "Dishes with temporary stat enhancements",
            90: "Legendary recipes with powerful effects",
            100: "Cuisine that rivals the Dragon-era feasts",
        },
    },
    "smithing": {
        "name": "Smithing",
        "skill_type": "general",
        "description": "Work metal to create and repair weapons and armor.",
        "domain_bonus": "engineering",
        "trainer_required_above": 75,
        "thresholds": {
            25: "Basic repairs, simple tools",
            50: "Standard weapons and armor forged",
            75: "Masterwork quality, alloy techniques",
            90: "Dragon-era metallurgy partially recovered",
            100: "Legendary smith — blades that sing",
        },
    },
    "alchemy": {
        "name": "Alchemy",
        "skill_type": "general",
        "description": "Brew potions, elixirs, and alchemical compounds.",
        "domain_bonus": "alchemy",
        "trainer_required_above": 75,
        "thresholds": {
            25: "Simple healing draughts and antidotes",
            50: "Buff potions, poison neutralizers",
            75: "Transmutation reagents, volatile compounds",
            90: "Node-infused elixirs, rare catalysts",
            100: "Philosopher-level mastery of transformation",
        },
    },
    "reflexes": {
        "name": "Reflexes",
        "skill_type": "general",
        "description": "React quickly to danger, dodge, and counter unexpected attacks.",
        "domain_bonus": "combat",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Flinch reactions improved",
            50: "Dodge telegraphed attacks reliably",
            75: "React to ambushes, counter-strike openings",
            90: "Near-precognitive awareness in combat",
            100: "Nothing catches you off guard",
        },
    },
    "investigation": {
        "name": "Investigation",
        "skill_type": "general",
        "description": "Search rooms for hidden exits, lore fragments, and concealed objects.",
        "domain_bonus": "remnance",
        "trainer_required_above": 50,
        "thresholds": {
            25: "Obvious hidden doors and recent disturbances",
            50: "Concealed passages, buried objects, faded inscriptions",
            75: "Magically obscured exits, ancient caches",
            90: "Dragon-era vaults, node-sealed chambers",
            100: "Nothing stays hidden from your scrutiny",
        },
    },
}

# --- Ancestry Skill Seeds (D-20) ---
# Applied at character creation. Values represent starting proficiency.

ANCESTRY_SKILL_SEEDS = {
    "human": {},
    "kauroran": {
        "swimming": 30,
        "fishing": 25,
        "beast_training": 20,
        "persuasion": 15,
    },
    "veth": {
        "stealth": 20,
        "navigation": 25,
        "lockpicking": 10,
        "tracking": 25,
    },
    "selvar_north": {
        "tracking": 20,
        "climbing": 15,
        "intimidation": 10,
    },
    "selvar_south": {
        "lockpicking": 15,
        "appraisal": 15,
        "persuasion": 10,
        "navigation": 20,
    },
}

# --- Selvar Coat-to-Lineage Mapping (Pitfall 7) ---
# Selvar coat color determines northern or southern lineage.
# Winter coat = North (mountain/tundra Selvar), Summer coat = South (trade/coastal Selvar).

SELVAR_COAT_TO_LINEAGE = {
    "winter": "selvar_north",
    "summer": "selvar_south",
}

# --- Trainer Registry (framework ready for content phase) ---

TRAINER_REGISTRY = {
    # --- Vael's Crossing Trainers (07-04) ---
    "npc_trainer_combat_sergeant_vale": {
        "name": "Sergeant Vale",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["reflexes", "climbing", "intimidation"],
        "cost_per_session": 80,
    },
    "npc_guildmaster_subterfuge_dessa": {
        "name": "Dessa",
        "trainer_quality": "master",
        "quality_multiplier": 2.0,
        "skills_taught": ["lockpicking", "stealth"],
        "cost_per_session": 150,
    },
    "npc_guildmaster_naturalism_elwen": {
        "name": "Elwen",
        "trainer_quality": "master",
        "quality_multiplier": 2.0,
        "skills_taught": ["animal_handling", "herbalism", "foraging"],
        "cost_per_session": 120,
    },
    "npc_guildmaster_diplomacy_aldric": {
        "name": "Aldric",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["persuasion", "appraisal"],
        "cost_per_session": 100,
    },
    "npc_guildmaster_alchemy_mirelle": {
        "name": "Mirelle",
        "trainer_quality": "master",
        "quality_multiplier": 2.0,
        "skills_taught": ["alchemy", "first_aid"],
        "cost_per_session": 140,
    },
    "npc_guildmaster_tactics_brennus": {
        "name": "Brennus",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["navigation", "tracking"],
        "cost_per_session": 90,
    },
    "npc_guildmaster_engineering_pren": {
        "name": "Pren",
        "trainer_quality": "master",
        "quality_multiplier": 2.0,
        "skills_taught": ["engineering", "smithing"],
        "cost_per_session": 160,
    },
    "npc_guildmaster_resonance_kael": {
        "name": "Kael",
        "trainer_quality": "master",
        "quality_multiplier": 2.0,
        "skills_taught": ["node_reading"],
        "cost_per_session": 200,
    },
    "npc_herbalist_old_ystra": {
        "name": "Old Ystra",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["herbalism", "cooking"],
        "cost_per_session": 60,
    },
    "npc_stablehand_korua": {
        "name": "Korua",
        "trainer_quality": "apprentice",
        "quality_multiplier": 1.25,
        "skills_taught": ["animal_handling", "beast_training", "swimming", "fishing"],
        "cost_per_session": 40,
    },
    # --- Ashreach Plains Trainers (09-01) ---
    "npc_trainer_fishing_ashreach": {
        "name": "Neddra",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["fishing"],
        "cost_per_session": 50,
    },
    "npc_trainer_herbalism_ashreach": {
        "name": "Senna",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["herbalism", "foraging"],
        "cost_per_session": 60,
    },
    # --- Reth Foothills Trainers (09-01) ---
    "npc_trainer_climbing_reth": {
        "name": "Grenn",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["climbing"],
        "cost_per_session": 70,
    },
    "npc_trainer_smithing_reth": {
        "name": "Halvek",
        "trainer_quality": "apprentice",
        "quality_multiplier": 1.25,
        "skills_taught": ["smithing"],
        "cost_per_session": 90,
    },
    # --- Cantera Edge Trainers (09-01) ---
    "npc_trainer_tracking_cantera": {
        "name": "Kaelen",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["tracking"],
        "cost_per_session": 60,
    },
    "npc_trainer_foraging_cantera": {
        "name": "Thaelen",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["foraging", "herbalism"],
        "cost_per_session": 55,
    },
    # --- Stormhaven Coast Trainers (09-01) ---
    "npc_trainer_swimming_stormhaven": {
        "name": "Aldren",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["swimming", "fishing"],
        "cost_per_session": 60,
    },
    "npc_trainer_navigation_stormhaven": {
        "name": "Korrin",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["navigation"],
        "cost_per_session": 65,
    },
}

# --- Trainer Quality Multipliers ---

TRAINER_QUALITY_MULTIPLIER = {
    "apprentice": 1.25,
    "journeyman": 1.5,
    "master": 2.0,
}

# --- Attunement Thresholds (D-23) ---
# Zone/node/creature attunement unlocks at these skill levels.

ATTUNEMENT_THRESHOLDS = {
    25: "sensory_detail",
    50: "hidden_reveal",
    75: "mob_patterns",
    90: "enhanced_magic",
    100: "lore_fragment",
}

# --- Discovery Triggers (D-24) ---
# Framework with one example entry. Content-phase fills these.
# Conditions: dict of {skill_id: min_value} — all must be met.

DISCOVERY_TRIGGERS = [
    {
        "id": "cantera_cognitive_wolves",
        "conditions": {
            "cognitive_node": 90,
            "forest_wolf": 90,
            "cantera_forest_old_path": 75,
        },
        "lore_fragment": "lore_cantera_cognitive_001",
        "message": "You notice something about the wolves near this stone...",
    },
]
