"""
Guild, subclass, and domain fingerprint registries with GTS computation engine.

This module provides:
- FINGERPRINTS: 10 domain mechanical identities (verb, resource, description)
- GUILDS: 10 guild definitions (name, domain, hub cities, resource)
- SUBCLASSES: 90 subclass definitions (name, domains, guild, fantasy, hook)
- GUILD_TIER_LABELS: Guild-specific tier descriptor strings
- DOMAIN_PROFICIENCY_LABELS: Score-to-descriptor mapping for domain display
- GTS computation: calculate_guild_tier_score, get_guild_tier, get_guild_tier_label
- Guild eligibility: check_guild_eligibility

Creative content is from vault sources (soravelon-fingerprints.md,
soravelon-guilds.md, soravelon-abilities.md). Not authored by Claude.
"""

from world.world_state import ALL_DOMAINS

# ---------------------------------------------------------------------------
# Fingerprints — one per domain, defines the mechanical verb and resource
# ---------------------------------------------------------------------------

FINGERPRINTS = {
    "combat": {
        "verb": "press",
        "resource": "Momentum",
        "resource_type": "momentum",
        "description": (
            "Sustained aggression. Momentum builds from hits landed and damage"
            " taken, decays when nothing is happening. A Combat player who stays"
            " in the fight always has resources."
        ),
    },
    "subterfuge": {
        "verb": "read",
        "resource": "Focus",
        "resource_type": "focus",
        "description": (
            "Timing and pattern recognition. Every enemy has a defensive rhythm"
            " -- guard windows that open and close on a timer. Abilities used"
            " within the window chain; abilities used outside break the combo."
        ),
    },
    "naturalism": {
        "verb": "calibrate",
        "resource": "Balance",
        "resource_type": "balance",
        "description": (
            "Managed duality. The Balance spectrum sits at neutral by default."
            " Aggressive abilities push toward Feral, defensive toward Calm."
            " Both extremes weaken you in different ways."
        ),
    },
    "resonance": {
        "verb": "attune",
        "resource": "Resonance",
        "resource_type": "resonance",
        "description": (
            "Environmental sensitivity. Resonance builds toward a threshold,"
            " decays during combat, and spends at 60+ for meaningful effect."
            " Resonance players perceive the world differently."
        ),
    },
    "arcana": {
        "verb": "ration",
        "resource": "Mana",
        "resource_type": "mana",
        "description": (
            "Cross-encounter resource management. Mana regenerates at rest"
            " between fights, not during them. The space between fights is"
            " as strategically interesting as the fight itself."
        ),
    },
    "diplomacy": {
        "verb": "leverage",
        "resource": "Influence",
        "resource_type": "influence",
        "description": (
            "Converting relationships into power. A Diplomacy player who"
            " actively engages the world's political landscape arrives at"
            " combat with more resources than one who ignores it."
        ),
    },
    "alchemy": {
        "verb": "prepare",
        "resource": "Reagents",
        "resource_type": "reagents",
        "description": (
            "Preparation as combat philosophy. Reagents are crafted before"
            " the fight from gathered materials. Running out mid-fight is"
            " a genuine failure state -- insufficient planning, not bad luck."
        ),
    },
    "tactics": {
        "verb": "orchestrate",
        "resource": "Command",
        "resource_type": "command",
        "description": (
            "Group synergy expressed as personal power. Command builds when"
            " allies act. Solo, it builds at half rate. A Tactics player in"
            " a group is a mechanically different class than one playing solo."
        ),
    },
    "engineering": {
        "verb": "construct",
        "resource": "Components",
        "resource_type": "components",
        "description": (
            "Mechanical companion as combat identity. The companion fights"
            " alongside you, fueled by Components. Standard for baseline,"
            " Enhanced Fuel for amplified, Overcharge for risk/reward ceiling."
        ),
    },
    "remnance": {
        "verb": "excavate",
        "resource": "Echoes",
        "resource_type": "echoes",
        "description": (
            "Accumulated knowledge as combat power. Lore fragment decoding"
            " grants starting Echoes for subsequent encounters. The only domain"
            " where intellectual curiosity is directly expressed as combat power."
        ),
    },
}

# ---------------------------------------------------------------------------
# Guilds — 10 guilds, one per domain
# ---------------------------------------------------------------------------

GUILDS = {
    "ironblood": {
        "name": "Guild of Ironblood",
        "primary_domain": "combat",
        "hub_cities": ["caldenmere", "tremen"],
        "hidden": False,
        "motto": "Strength is not a gift. It is a debt you pay every day.",
        "resource_type": "momentum",
    },
    "veilcraft": {
        "name": "Guild of Veilcraft",
        "primary_domain": "subterfuge",
        "hub_cities": ["vaels_crossing"],
        "hidden": False,
        "motto": "What is seen is already lost.",
        "resource_type": "focus",
    },
    "verdance": {
        "name": "Guild of Verdance",
        "primary_domain": "naturalism",
        "hub_cities": ["vaels_crossing", "korahei"],
        "hidden": False,
        "motto": (
            "The forest was here before the Empire. It will be here after."
        ),
        "resource_type": "balance",
    },
    "resonance": {
        "name": "Guild of Resonance",
        "primary_domain": "resonance",
        "hub_cities": ["tremen", "vaels_crossing"],
        "hidden": False,
        "motto": (
            "The patterns were here before us. We are learning to read."
        ),
        "resource_type": "resonance",
    },
    "arcane": {
        "name": "Guild of the Arcane",
        "primary_domain": "arcana",
        "hub_cities": [
            "caldenmere",
            "varath_prime",
            "vaels_crossing",
            "tremen",
        ],
        "hidden": False,
        "motto": "The spell is the question. The effect is the answer.",
        "resource_type": "mana",
    },
    "accord": {
        "name": "Guild of Accord",
        "primary_domain": "diplomacy",
        "hub_cities": ["caldenmere", "varath_prime", "korahei"],
        "hidden": False,
        "motto": (
            "Every door opens from the inside."
            " We know who's standing there."
        ),
        "resource_type": "influence",
    },
    "thornwork": {
        "name": "Guild of Thornwork",
        "primary_domain": "alchemy",
        "hub_cities": ["vaels_crossing"],
        "hidden": False,
        "motto": (
            "Everything that heals can also harm. We chose a side."
        ),
        "resource_type": "reagents",
    },
    "warcraft": {
        "name": "Guild of Warcraft",
        "primary_domain": "tactics",
        "hub_cities": ["caldenmere", "varath_prime", "fort_rennick"],
        "hidden": False,
        "motto": (
            "The battle is won before the first blow."
            " Everything after is ceremony."
        ),
        "resource_type": "command",
    },
    "forge": {
        "name": "Guild of Forge",
        "primary_domain": "engineering",
        "hub_cities": ["caldenmere"],
        "hidden": False,
        "motto": (
            "We don't ask the old magic for permission."
            " We figure it out ourselves."
        ),
        "resource_type": "components",
    },
    "vaelborn": {
        "name": "Guild of Vaelborn",
        "primary_domain": "remnance",
        "hub_cities": [],
        "hidden": True,
        "motto": (
            "The world forgot what it was named after. We remember."
        ),
        "resource_type": "echoes",
    },
}

# ---------------------------------------------------------------------------
# Subclasses — 90 total (10 guilds x 9 secondary domains each)
# ---------------------------------------------------------------------------

SUBCLASSES = {
    # --- Guild of Ironblood (Combat Primary) ---
    "duskblade": {
        "name": "Duskblade",
        "primary_domain": "combat",
        "secondary_domain": "subterfuge",
        "guild_id": "ironblood",
        "fantasy": (
            "A fighter who disappears between strikes"
            " -- combat invisibility not infiltration"
        ),
        "hook": (
            "Momentum spends on mid-combat Vanish;"
            " burst damage on stealth re-entry"
        ),
    },
    "thornguard": {
        "name": "Thornguard",
        "primary_domain": "combat",
        "secondary_domain": "naturalism",
        "guild_id": "ironblood",
        "fantasy": "A warrior whose body is reinforced by living magic",
        "hook": (
            "Nature buffs applied to self;"
            " animal companion assists rather than bonds"
        ),
    },
    "ruinborn": {
        "name": "Ruinborn",
        "primary_domain": "combat",
        "secondary_domain": "resonance",
        "guild_id": "ironblood",
        "fantasy": (
            "Channels old magic through physical strikes"
            " -- hits that leave node-echoes"
        ),
        "hook": (
            "Attacks apply Resonance stacks;"
            " threshold triggers node burst on target"
        ),
    },
    "spellbreaker": {
        "name": "Spellbreaker",
        "primary_domain": "combat",
        "secondary_domain": "arcana",
        "guild_id": "ironblood",
        "fantasy": (
            "Hunts mages -- uses magical vulnerability as a weapon"
        ),
        "hook": "Anti-magic combat abilities; disrupts enemy Mana on hit",
    },
    "ironvoice": {
        "name": "Ironvoice",
        "primary_domain": "combat",
        "secondary_domain": "diplomacy",
        "guild_id": "ironblood",
        "fantasy": (
            "A warrior whose reputation precedes them"
            " -- enemies hesitate, allies rally"
        ),
        "hook": (
            "Presence-scaled intimidation debuffs;"
            " Reputation gains faster in combat"
        ),
    },
    "ashfang": {
        "name": "Ashfang",
        "primary_domain": "combat",
        "secondary_domain": "alchemy",
        "guild_id": "ironblood",
        "fantasy": (
            "Coats everything in blood and poison"
            " -- raw violence as delivery mechanism"
        ),
        "hook": "Melee attacks apply Bleed and Poison simultaneously",
    },
    "vanguard": {
        "name": "Vanguard",
        "primary_domain": "combat",
        "secondary_domain": "tactics",
        "guild_id": "ironblood",
        "fantasy": (
            "The front of every formation"
            " -- absorbs damage, breaks lines"
        ),
        "hook": (
            "Guard mechanics; generates group action budget bonuses"
            " through space control"
        ),
    },
    "ironwright": {
        "name": "Ironwright",
        "primary_domain": "combat",
        "secondary_domain": "engineering",
        "guild_id": "ironblood",
        "fantasy": (
            "A fighter whose companion is built"
            " for close-range combat support"
        ),
        "hook": (
            "Builds weapons mid-battle -- improvised, brutal, adaptive;"
            " no companion -- Engineering knowledge applied to self"
            " and weapons"
        ),
    },
    "dragonblooded": {
        "name": "Dragonblooded",
        "primary_domain": "combat",
        "secondary_domain": "remnance",
        "guild_id": "ironblood",
        "fantasy": (
            "A fighter touched by something ancient"
            " -- physical abilities that shouldn't exist"
        ),
        "hook": (
            "Ancient physical enhancements;"
            " resistances that scale off Resonance stat"
        ),
    },
    # --- Guild of Veilcraft (Subterfuge Primary) ---
    "grimwarden": {
        "name": "Grimwarden",
        "primary_domain": "subterfuge",
        "secondary_domain": "combat",
        "guild_id": "veilcraft",
        "fantasy": (
            "A brutal assassin -- no finesse,"
            " overwhelming force from unexpected angles"
        ),
        "hook": (
            "Focus builds fastest from ambush hits;"
            " stealth re-entry resets cooldowns"
        ),
    },
    "hollowstep": {
        "name": "Hollowstep",
        "primary_domain": "subterfuge",
        "secondary_domain": "naturalism",
        "guild_id": "veilcraft",
        "fantasy": (
            "A wilderness ghost -- tracks, vanishes,"
            " uses terrain as a weapon"
        ),
        "hook": (
            "Outdoor stealth bonuses; terrain-based trap-setting;"
            " creature attunement enhances evasion"
        ),
    },
    "veilreader": {
        "name": "Veilreader",
        "primary_domain": "subterfuge",
        "secondary_domain": "resonance",
        "guild_id": "veilcraft",
        "fantasy": (
            "Reads magical signatures of people and places"
            " -- sees what's coming"
        ),
        "hook": (
            "Node attunement gives combat advantage;"
            " reads enemy ability telegraphs one round ahead"
        ),
    },
    "nullshadow": {
        "name": "Nullshadow",
        "primary_domain": "subterfuge",
        "secondary_domain": "arcana",
        "guild_id": "veilcraft",
        "fantasy": (
            "Wraps magical effects in shadow"
            " -- spells that arrive unseen"
        ),
        "hook": (
            "Magical abilities usable from stealth"
            " without breaking Vanish"
        ),
    },
    "tally_agent": {
        "name": "Tally Agent",
        "primary_domain": "subterfuge",
        "secondary_domain": "diplomacy",
        "guild_id": "veilcraft",
        "fantasy": (
            "Information warfare, double agents, network exploitation"
        ),
        "hook": (
            "Network dimension grows fastest; faction Standing"
            " manipulation; social intel as combat leverage"
        ),
    },
    "blackthorn": {
        "name": "Blackthorn",
        "primary_domain": "subterfuge",
        "secondary_domain": "alchemy",
        "guild_id": "veilcraft",
        "fantasy": (
            "The classic poisoner -- patient, precise, never seen"
        ),
        "hook": (
            "Poison applied during Vanish;"
            " highest single-target poison ceiling in the game"
        ),
    },
    "shadecommand": {
        "name": "Shadecommand",
        "primary_domain": "subterfuge",
        "secondary_domain": "tactics",
        "guild_id": "veilcraft",
        "fantasy": (
            "Special operations -- tactical infiltration,"
            " disruption behind lines"
        ),
        "hook": (
            "Group stealth abilities; disables enemy tactical"
            " advantages; scouts ahead for group"
        ),
    },
    "lockjaw": {
        "name": "Lockjaw",
        "primary_domain": "subterfuge",
        "secondary_domain": "engineering",
        "guild_id": "veilcraft",
        "fantasy": (
            "Built every tool they're using"
            " -- no improvisation, pure preparation"
        ),
        "hook": (
            "Trap-setting master; mechanical devices usable mid-combat"
        ),
    },
    "hollowseen": {
        "name": "Hollowseen",
        "primary_domain": "subterfuge",
        "secondary_domain": "remnance",
        "guild_id": "veilcraft",
        "fantasy": (
            "Sees what others cannot"
            " -- reads ancient patterns in movement"
        ),
        "hook": (
            "Awareness abilities that shouldn't be possible;"
            " lore fragment discovery rate enhanced"
        ),
    },
    # --- Guild of Verdance (Naturalism Primary) ---
    "thornfist": {
        "name": "Thornfist",
        "primary_domain": "naturalism",
        "secondary_domain": "combat",
        "guild_id": "verdance",
        "fantasy": "A nature practitioner who fights with their body",
        "hook": (
            "Shapeshift-adjacent abilities;"
            " physical strikes apply nature DoTs"
        ),
    },
    "rootstalker": {
        "name": "Rootstalker",
        "primary_domain": "naturalism",
        "secondary_domain": "subterfuge",
        "guild_id": "verdance",
        "fantasy": (
            "Moves through wilderness like the wilderness itself"
        ),
        "hook": (
            "Outdoor Vanish with no cooldown;"
            " ambush bonuses from natural cover"
        ),
    },
    "cantera": {
        "name": "Cantera",
        "primary_domain": "naturalism",
        "secondary_domain": "resonance",
        "guild_id": "verdance",
        "fantasy": (
            "Named for the forest"
            " -- nature through old magic specifically"
        ),
        "hook": (
            "Node attunement accelerates in nature zones;"
            " unique Cognitive node interaction"
        ),
    },
    "stormcaller": {
        "name": "Stormcaller",
        "primary_domain": "naturalism",
        "secondary_domain": "arcana",
        "guild_id": "verdance",
        "fantasy": "Calls elemental forces -- rain, lightning, wind",
        "hook": (
            "Area magical effects; Wet application;"
            " weather abilities enhanced in node zones"
        ),
    },
    "greentongue": {
        "name": "Greentongue",
        "primary_domain": "naturalism",
        "secondary_domain": "diplomacy",
        "guild_id": "verdance",
        "fantasy": (
            "Speaks for the natural world in political spaces"
        ),
        "hook": (
            "Faction Standing with Druids and Wardens grows faster;"
            " animal-based social leverage"
        ),
    },
    "rotweald": {
        "name": "Rotweald",
        "primary_domain": "naturalism",
        "secondary_domain": "alchemy",
        "guild_id": "verdance",
        "fantasy": (
            "The dark side of nature -- decay, rot, toxic growth"
        ),
        "hook": (
            "Bleed and Poison through nature abilities;"
            " area DoT effects"
        ),
    },
    "wildcommand": {
        "name": "Wildcommand",
        "primary_domain": "naturalism",
        "secondary_domain": "tactics",
        "guild_id": "verdance",
        "fantasy": (
            "Commands animals as a tactical force"
            " -- the forest is their army"
        ),
        "hook": (
            "Beast companion combat scripting; animal-based group"
            " abilities; zone control through terrain"
        ),
    },
    "growthwright": {
        "name": "Growthwright",
        "primary_domain": "naturalism",
        "secondary_domain": "engineering",
        "guild_id": "verdance",
        "fantasy": (
            "Grows things rather than builds them"
            " -- living structures, organic construction"
        ),
        "hook": (
            "Harvesting bonuses; cultivated material creation;"
            " living trap-setting"
        ),
    },
    "deeproot": {
        "name": "Deeproot",
        "primary_domain": "naturalism",
        "secondary_domain": "remnance",
        "guild_id": "verdance",
        "fantasy": (
            "Touches something beneath nature"
            " -- the world-memory in old growth"
        ),
        "hook": (
            "Ancient forest lore unlocks; unique in Cantera Forest;"
            " dragon-adjacent nature abilities"
        ),
    },
    # --- Guild of Resonance (Resonance Primary) ---
    "runebreaker": {
        "name": "Runebreaker",
        "primary_domain": "resonance",
        "secondary_domain": "combat",
        "guild_id": "resonance",
        "fantasy": (
            "Channels old magic into physical destruction"
            " -- hits that leave reality slightly wrong"
        ),
        "hook": (
            "Resonance stacks on enemies through physical strikes;"
            " node burst damage"
        ),
    },
    "greymantle": {
        "name": "Greymantle",
        "primary_domain": "resonance",
        "secondary_domain": "subterfuge",
        "guild_id": "resonance",
        "fantasy": (
            "Moves through the world's magical blind spots"
        ),
        "hook": (
            "Node proximity grants stealth bonuses;"
            " undetectable to magical detection"
        ),
    },
    "thornweald": {
        "name": "Thornweald",
        "primary_domain": "resonance",
        "secondary_domain": "naturalism",
        "guild_id": "resonance",
        "fantasy": (
            "The nature-magic practitioner"
            " -- DoT focus, terrain manipulation"
        ),
        "hook": (
            "Nature and old magic combined;"
            " terrain manipulation abilities"
        ),
    },
    "sealwright": {
        "name": "Sealwright",
        "primary_domain": "resonance",
        "secondary_domain": "arcana",
        "guild_id": "resonance",
        "fantasy": (
            "Combines ancient patterns with raw magical force"
        ),
        "hook": (
            "Node-powered magical abilities;"
            " highest burst damage of any Resonance subclass"
        ),
    },
    "lorekeeper": {
        "name": "Lorekeeper",
        "primary_domain": "resonance",
        "secondary_domain": "diplomacy",
        "guild_id": "resonance",
        "fantasy": (
            "The Scholar made dangerous"
            " -- ancient knowledge as political leverage"
        ),
        "hook": (
            "Lore fragments grant faction Standing bonuses;"
            " highest Resonance skill ceiling"
        ),
    },
    "corroder": {
        "name": "Corroder",
        "primary_domain": "resonance",
        "secondary_domain": "alchemy",
        "guild_id": "resonance",
        "fantasy": (
            "Applies old magic to chemical effects"
            " -- poisons that interact with node energy"
        ),
        "hook": (
            "Node-enhanced poison effects;"
            " compound effects amplified near active nodes"
        ),
    },
    "nodecaller": {
        "name": "Nodecaller",
        "primary_domain": "resonance",
        "secondary_domain": "tactics",
        "guild_id": "resonance",
        "fantasy": (
            "Uses node events as tactical weapons"
            " -- forces node activation deliberately"
        ),
        "hook": (
            "Can trigger node events; zone control through"
            " magical environmental manipulation"
        ),
    },
    "arcanist": {
        "name": "Arcanist",
        "primary_domain": "resonance",
        "secondary_domain": "engineering",
        "guild_id": "resonance",
        "fantasy": (
            "Understands how old infrastructure was built"
            " -- studies and applies fragments"
        ),
        "hook": (
            "Golem interaction; base-8 decoding;"
            " Scholar Arcanist abilities now Resonance-rooted"
        ),
    },
    "sealreader": {
        "name": "Sealreader",
        "primary_domain": "resonance",
        "secondary_domain": "remnance",
        "guild_id": "resonance",
        "fantasy": "Has gotten uncomfortably close to the truth",
        "hook": (
            "Closest to the dragon secret;"
            " Circle of Wizards actively suppresses this subclass"
        ),
    },
    # --- Guild of the Arcane (Arcana Primary) ---
    "battlemage": {
        "name": "Battlemage",
        "primary_domain": "arcana",
        "secondary_domain": "combat",
        "guild_id": "arcane",
        "fantasy": (
            "A mage who hits things when spells run out"
            " -- and doesn't mind"
        ),
        "hook": (
            "Mana-fueled physical strikes; melee abilities"
            " scale off both Strength and Mana"
        ),
    },
    "mistveil": {
        "name": "Mistveil",
        "primary_domain": "arcana",
        "secondary_domain": "subterfuge",
        "guild_id": "arcane",
        "fantasy": (
            "Disappears behind magical concealment"
            " -- not stealth, something else"
        ),
        "hook": (
            "Magical invisibility distinct from physical stealth;"
            " unique detection bypass"
        ),
    },
    "stormweaver": {
        "name": "Stormweaver",
        "primary_domain": "arcana",
        "secondary_domain": "naturalism",
        "guild_id": "arcane",
        "fantasy": (
            "Weaves elemental forces through nature"
            " -- lightning through trees, frost through roots"
        ),
        "hook": (
            "Nature and arcane combined; area magical effects"
            " enhanced in natural zones"
        ),
    },
    "spellseeker": {
        "name": "Spellseeker",
        "primary_domain": "arcana",
        "secondary_domain": "resonance",
        "guild_id": "arcane",
        "fantasy": (
            "A mage who studies old magic to make new magic better"
        ),
        "hook": (
            "Node study improves Mana pool"
            " and spellcasting effectiveness"
        ),
    },
    "enchantvoice": {
        "name": "Enchantvoice",
        "primary_domain": "arcana",
        "secondary_domain": "diplomacy",
        "guild_id": "arcane",
        "fantasy": "A mage whose words carry literal weight",
        "hook": (
            "Magical persuasion abilities; social-magical hybrids;"
            " Charm spell variants"
        ),
    },
    "fusewright": {
        "name": "Fusewright",
        "primary_domain": "arcana",
        "secondary_domain": "alchemy",
        "guild_id": "arcane",
        "fantasy": (
            "Weaponizes alchemical and magical combinations"
        ),
        "hook": (
            "Potion-powered spell amplification; compound effects"
            " trigger through magical delivery"
        ),
    },
    "wardcaller": {
        "name": "Wardcaller",
        "primary_domain": "arcana",
        "secondary_domain": "tactics",
        "guild_id": "arcane",
        "fantasy": (
            "Directs magical force tactically"
            " -- placement and timing over power"
        ),
        "hook": (
            "Magical area control; ability to define battlefield"
            " zones with lasting effects"
        ),
    },
    "runewright": {
        "name": "Runewright",
        "primary_domain": "arcana",
        "secondary_domain": "engineering",
        "guild_id": "arcane",
        "fantasy": "Encodes magic into constructed objects",
        "hook": (
            "Enchanted device creation; magical trap-setting;"
            " golem empowerment"
        ),
    },
    "voidscribe": {
        "name": "Voidscribe",
        "primary_domain": "arcana",
        "secondary_domain": "remnance",
        "guild_id": "arcane",
        "fantasy": (
            "Studies the space between what magic is and what it was"
        ),
        "hook": (
            "Ancient spellforms inaccessible to other Arcana"
            " subclasses; Circle of Wizards conflict"
        ),
    },
    # --- Guild of Accord (Diplomacy Primary) ---
    "civicguard": {
        "name": "Civicguard",
        "primary_domain": "diplomacy",
        "secondary_domain": "combat",
        "guild_id": "accord",
        "fantasy": (
            "The diplomat with teeth"
            " -- persuasion backed by demonstrated violence"
        ),
        "hook": (
            "Intimidation abilities scale with combat record;"
            " Presence+Strength hybrid scaling"
        ),
    },
    "shadowbroker": {
        "name": "Shadowbroker",
        "primary_domain": "diplomacy",
        "secondary_domain": "subterfuge",
        "guild_id": "accord",
        "fantasy": (
            "Runs information networks from the shadows"
            " -- nobody knows who they work for"
        ),
        "hook": (
            "Network dimension grows fastest;"
            " double faction Standing gains"
        ),
    },
    "wayfinder": {
        "name": "Wayfinder",
        "primary_domain": "diplomacy",
        "secondary_domain": "naturalism",
        "guild_id": "accord",
        "fantasy": (
            "Opens doors through empathy"
            " -- understands what every living thing needs"
        ),
        "hook": (
            "Bond dimension bonuses; animal and NPC warmth"
            " at unprecedented rates"
        ),
    },
    "spiritvoice": {
        "name": "Spiritvoice",
        "primary_domain": "diplomacy",
        "secondary_domain": "resonance",
        "guild_id": "accord",
        "fantasy": (
            "Uses old magic to amplify social power"
            " -- words that carry more weight than they should"
        ),
        "hook": (
            "Presence abilities scale off Resonance;"
            " ability dialogue options unlocked"
        ),
    },
    "highcourt": {
        "name": "Highcourt",
        "primary_domain": "diplomacy",
        "secondary_domain": "arcana",
        "guild_id": "accord",
        "fantasy": (
            "A mage who never had to fight"
            " -- because nobody wanted them to stop talking"
        ),
        "hook": (
            "Social-magical abilities; magical aura affects"
            " NPC disposition passively"
        ),
    },
    "silkpoison": {
        "name": "Silkpoison",
        "primary_domain": "diplomacy",
        "secondary_domain": "alchemy",
        "guild_id": "accord",
        "fantasy": (
            "The subtle threat -- social manipulation backed"
            " by the ability to harm without evidence"
        ),
        "hook": (
            "Poison applied through social encounters;"
            " the most dangerous dinner guest"
        ),
    },
    "bannerspeaker": {
        "name": "Bannerspeaker",
        "primary_domain": "diplomacy",
        "secondary_domain": "tactics",
        "guild_id": "accord",
        "fantasy": (
            "Turns armies with words"
            " -- the voice behind every military campaign"
        ),
        "hook": (
            "Morale mechanics at scale; faction Standing with"
            " military factions grows fastest"
        ),
    },
    "dealwright": {
        "name": "Dealwright",
        "primary_domain": "diplomacy",
        "secondary_domain": "engineering",
        "guild_id": "accord",
        "fantasy": (
            "Makes things that create obligations"
            " -- every gift is an investment"
        ),
        "hook": (
            "Crafted items carry Standing bonuses when gifted;"
            " merchant mechanics"
        ),
    },
    "truthwarden": {
        "name": "Truthwarden",
        "primary_domain": "diplomacy",
        "secondary_domain": "remnance",
        "guild_id": "accord",
        "fantasy": (
            "Knows too much about the world's actual history"
            " -- uses it carefully"
        ),
        "hook": (
            "Hidden faction access; the Resistance questline"
            " starts most naturally here"
        ),
    },
    # --- Guild of Thornwork (Alchemy Primary) ---
    "venomfang": {
        "name": "Venomfang",
        "primary_domain": "alchemy",
        "secondary_domain": "combat",
        "guild_id": "thornwork",
        "fantasy": (
            "Applies poison through sustained physical aggression"
        ),
        "hook": (
            "Highest melee poison application rate;"
            " Bleed+Poison simultaneously"
        ),
    },
    "nightshade": {
        "name": "Nightshade",
        "primary_domain": "alchemy",
        "secondary_domain": "subterfuge",
        "guild_id": "thornwork",
        "fantasy": (
            "Poisons from concealment"
            " -- never seen, only felt later"
        ),
        "hook": (
            "Vanish-applied poison; delayed onset toxins;"
            " highest single-target ceiling"
        ),
    },
    "mireweald": {
        "name": "Mireweald",
        "primary_domain": "alchemy",
        "secondary_domain": "naturalism",
        "guild_id": "thornwork",
        "fantasy": (
            "The Thornwork-primary version"
            " -- decay and organic toxins over living nature"
        ),
        "hook": (
            "Decay-focused nature abilities;"
            " terrain poisoning; rot effects"
        ),
    },
    "voidbrewer": {
        "name": "Voidbrewer",
        "primary_domain": "alchemy",
        "secondary_domain": "resonance",
        "guild_id": "thornwork",
        "fantasy": (
            "Creates alchemical compounds that interact"
            " with old magic"
        ),
        "hook": (
            "Node-enhanced consumables; alchemical effects"
            " amplified in node zones"
        ),
    },
    "fumecaster": {
        "name": "Fumecaster",
        "primary_domain": "alchemy",
        "secondary_domain": "arcana",
        "guild_id": "thornwork",
        "fantasy": (
            "Delivers alchemical compounds"
            " through magical vectors"
        ),
        "hook": (
            "Spell-delivered poisons and compounds;"
            " range on normally melee-only effects"
        ),
    },
    "sweetpoison": {
        "name": "Sweetpoison",
        "primary_domain": "alchemy",
        "secondary_domain": "diplomacy",
        "guild_id": "thornwork",
        "fantasy": (
            "The charming poisoner"
            " -- social access is just a delivery method"
        ),
        "hook": (
            "Poison through social interaction;"
            " Influence builds through successful poisonings"
        ),
    },
    "plaguecommand": {
        "name": "Plaguecommand",
        "primary_domain": "alchemy",
        "secondary_domain": "tactics",
        "guild_id": "thornwork",
        "fantasy": (
            "Tactical toxicology"
            " -- poisons as area-denial weapons"
        ),
        "hook": (
            "Area poison effects; terrain poisoning"
            " for zone control; tactical resource denial"
        ),
    },
    "fumewright": {
        "name": "Fumewright",
        "primary_domain": "alchemy",
        "secondary_domain": "engineering",
        "guild_id": "thornwork",
        "fantasy": (
            "Builds delivery mechanisms -- gas traps,"
            " poison containers, alchemical devices"
        ),
        "hook": (
            "Mechanical poison delivery;"
            " trap-setting with chemical payloads"
        ),
    },
    "firstblight": {
        "name": "Firstblight",
        "primary_domain": "alchemy",
        "secondary_domain": "remnance",
        "guild_id": "thornwork",
        "fantasy": (
            "Something old in the poison"
            " -- toxins that interact with dragon magic"
        ),
        "hook": (
            "Ancient poison effects; dragon-adjacent toxicology;"
            " unique Vaelborn questline interaction"
        ),
    },
    # --- Guild of Warcraft (Tactics Primary) ---
    "warbringer": {
        "name": "Warbringer",
        "primary_domain": "tactics",
        "secondary_domain": "combat",
        "guild_id": "warcraft",
        "fantasy": (
            "The frontline commander who leads by example"
            " -- first in, last out"
        ),
        "hook": (
            "Guard mechanics plus command abilities;"
            " action budget bonuses for nearby allies"
        ),
    },
    "greycommand": {
        "name": "Greycommand",
        "primary_domain": "tactics",
        "secondary_domain": "subterfuge",
        "guild_id": "warcraft",
        "fantasy": (
            "Special operations commander"
            " -- controls information as a tactical weapon"
        ),
        "hook": (
            "Scouting abilities; group stealth;"
            " intel-based combat advantage"
        ),
    },
    "wildtactician": {
        "name": "Wildtactician",
        "primary_domain": "tactics",
        "secondary_domain": "naturalism",
        "guild_id": "warcraft",
        "fantasy": (
            "Commands natural elements as battlefield terrain"
        ),
        "hook": (
            "Zone control through nature;"
            " beast-based tactical abilities"
        ),
    },
    "nodewarden": {
        "name": "Nodewarden",
        "primary_domain": "tactics",
        "secondary_domain": "resonance",
        "guild_id": "warcraft",
        "fantasy": (
            "Uses node events as tactical terrain"
            " -- activates, destabilizes, weaponizes"
        ),
        "hook": (
            "Node manipulation in combat;"
            " Scholar tactical awareness"
        ),
    },
    "siegecaller": {
        "name": "Siegecaller",
        "primary_domain": "tactics",
        "secondary_domain": "arcana",
        "guild_id": "warcraft",
        "fantasy": (
            "Calls magical artillery -- places effects"
            " where they need to be, not where he is"
        ),
        "hook": (
            "Long-range area placement;"
            " magical battlefield geometry"
        ),
    },
    "warlord": {
        "name": "Warlord",
        "primary_domain": "tactics",
        "secondary_domain": "diplomacy",
        "guild_id": "warcraft",
        "fantasy": (
            "Commands through force of personality"
            " -- morale IS the battlefield"
        ),
        "hook": (
            "Presence-scaled command abilities;"
            " faction Standing from combat victories"
        ),
    },
    "siegemaster": {
        "name": "Siegemaster",
        "primary_domain": "tactics",
        "secondary_domain": "alchemy",
        "guild_id": "warcraft",
        "fantasy": (
            "Tactical poison and chemical warfare"
            " -- area denial and attrition"
        ),
        "hook": (
            "Area DoT tactics; siege mechanics"
            " for zone-level content"
        ),
    },
    "fieldwright": {
        "name": "Fieldwright",
        "primary_domain": "tactics",
        "secondary_domain": "engineering",
        "guild_id": "warcraft",
        "fantasy": (
            "Builds battlefield advantages"
            " -- fortifications, devices, mechanical traps"
        ),
        "hook": (
            "Combat construction; field modification abilities"
        ),
    },
    "oathbreaker": {
        "name": "Oathbreaker",
        "primary_domain": "tactics",
        "secondary_domain": "remnance",
        "guild_id": "warcraft",
        "fantasy": (
            "Knows how ancient wars were actually fought"
            " -- tactics nobody else knows"
        ),
        "hook": (
            "Ancient tactical knowledge; abilities referencing"
            " pre-curse battle doctrine"
        ),
    },
    # --- Guild of Forge (Engineering Primary) ---
    "ironsmith": {
        "name": "Ironsmith",
        "primary_domain": "engineering",
        "secondary_domain": "combat",
        "guild_id": "forge",
        "fantasy": (
            "Builds better weapons and wears better armor"
            " -- and uses both"
        ),
        "hook": (
            "Crafted gear has enhanced stats when self-made;"
            " combat bonuses from own crafted equipment"
        ),
    },
    "gearhand": {
        "name": "Gearhand",
        "primary_domain": "engineering",
        "secondary_domain": "subterfuge",
        "guild_id": "forge",
        "fantasy": (
            "A Forge-primary who learned infiltration"
            " through mechanical locks"
        ),
        "hook": (
            "Trap-setting master with infiltration applications;"
            " mechanical lock mastery"
        ),
    },
    "growsmith": {
        "name": "Growsmith",
        "primary_domain": "engineering",
        "secondary_domain": "naturalism",
        "guild_id": "forge",
        "fantasy": (
            "Cultivates living materials and builds with them"
        ),
        "hook": (
            "Living material crafting; unique organic harvesting"
            " mechanics; bridge between grown and constructed"
        ),
    },
    "runewright_forge": {
        "name": "Runewright",
        "primary_domain": "engineering",
        "secondary_domain": "resonance",
        "guild_id": "forge",
        "fantasy": (
            "Studies old infrastructure to understand how it works"
        ),
        "hook": (
            "Ancient construction knowledge; golem repair"
            " and interaction; base-8 pattern application"
        ),
    },
    "sparkshaper": {
        "name": "Sparkshaper",
        "primary_domain": "engineering",
        "secondary_domain": "arcana",
        "guild_id": "forge",
        "fantasy": (
            "Understands that magic and machinery are the same"
            " thing approached differently"
        ),
        "hook": (
            "Magical device crafting;"
            " enchanted component creation"
        ),
    },
    "dealsmith": {
        "name": "Dealsmith",
        "primary_domain": "engineering",
        "secondary_domain": "diplomacy",
        "guild_id": "forge",
        "fantasy": (
            "Makes things people want"
            " -- economic power through craft"
        ),
        "hook": (
            "Merchant mechanics; crafted item Standing bonuses;"
            " Consortium faction integration"
        ),
    },
    "siegewright": {
        "name": "Siegewright",
        "primary_domain": "engineering",
        "secondary_domain": "tactics",
        "guild_id": "forge",
        "fantasy": (
            "Builds what armies need -- siege equipment,"
            " fortifications, field infrastructure"
        ),
        "hook": (
            "Large-scale construction; group-benefiting devices;"
            " siege mechanics"
        ),
    },
    "fumehand": {
        "name": "Fumehand",
        "primary_domain": "engineering",
        "secondary_domain": "alchemy",
        "guild_id": "forge",
        "fantasy": (
            "Chemical engineering meets mechanical construction"
        ),
        "hook": (
            "Alchemical device crafting; gas delivery systems"
        ),
    },
    "bucketborn": {
        "name": "Bucketborn",
        "primary_domain": "engineering",
        "secondary_domain": "remnance",
        "guild_id": "forge",
        "fantasy": (
            "Named for Bucket -- accidentally rediscovered"
            " old magic through mechanical study"
        ),
        "hook": (
            "Unique golem interaction; ancient infrastructure"
            " instinct; the subclass Gidget never meant to create"
        ),
    },
    # --- Guild of Vaelborn (Remnance Primary) — HIDDEN ---
    "dragonkin": {
        "name": "Dragonkin",
        "primary_domain": "remnance",
        "secondary_domain": "combat",
        "guild_id": "vaelborn",
        "fantasy": (
            "A fighter whose body has been changed"
            " by proximity to old power"
        ),
        "hook": (
            "Ancient physical enhancements;"
            " Dragon Rookery interactions unique"
        ),
    },
    "truthshadow": {
        "name": "Truthshadow",
        "primary_domain": "remnance",
        "secondary_domain": "subterfuge",
        "guild_id": "vaelborn",
        "fantasy": (
            "Knows things they shouldn't"
            " and hides that they know them"
        ),
        "hook": (
            "Deepest information access;"
            " unique faction Standing interactions"
        ),
    },
    "worldroot": {
        "name": "Worldroot",
        "primary_domain": "remnance",
        "secondary_domain": "naturalism",
        "guild_id": "vaelborn",
        "fantasy": (
            "Connected to the world's actual foundation"
            " -- the living magic beneath nature"
        ),
        "hook": (
            "Unique Cantera Forest interactions;"
            " dragon lore through nature"
        ),
    },
    "sealbreaker": {
        "name": "Sealbreaker",
        "primary_domain": "remnance",
        "secondary_domain": "resonance",
        "guild_id": "vaelborn",
        "fantasy": (
            "The most dangerous subclass in the game"
            " -- actively working to break the dragon curse"
        ),
        "hook": (
            "Dragon curse questline primary;"
            " Circle of Wizards' primary target"
        ),
    },
    "firstform": {
        "name": "Firstform",
        "primary_domain": "remnance",
        "secondary_domain": "arcana",
        "guild_id": "vaelborn",
        "fantasy": (
            "Casts using spell-forms predating"
            " current magical schools"
        ),
        "hook": (
            "Dragon-origin spellforms; unique effects"
            " unavailable to any other subclass"
        ),
    },
    "ancientvoice": {
        "name": "Ancientvoice",
        "primary_domain": "remnance",
        "secondary_domain": "diplomacy",
        "guild_id": "vaelborn",
        "fantasy": (
            "Speaks with the authority"
            " of the world's true history"
        ),
        "hook": (
            "Political leverage from forbidden knowledge;"
            " unique faction access"
        ),
    },
    "rootpoison": {
        "name": "Rootpoison",
        "primary_domain": "remnance",
        "secondary_domain": "alchemy",
        "guild_id": "vaelborn",
        "fantasy": (
            "Dragon-origin alchemy, not learned alchemy"
        ),
        "hook": (
            "Toxins derived from pre-curse knowledge;"
            " unique compound effects"
        ),
    },
    "firstblade": {
        "name": "Firstblade",
        "primary_domain": "remnance",
        "secondary_domain": "tactics",
        "guild_id": "vaelborn",
        "fantasy": (
            "Fights using pre-curse combat doctrine"
            " -- tactics nobody else has seen"
        ),
        "hook": (
            "Ancient tactical abilities;"
            " unique combat mechanics"
        ),
    },
    "dragonwright": {
        "name": "Dragonwright",
        "primary_domain": "remnance",
        "secondary_domain": "engineering",
        "guild_id": "vaelborn",
        "fantasy": (
            "Builds using fragments of dragon-made"
            " construction knowledge"
        ),
        "hook": (
            "Unique golem construction;"
            " ancient infrastructure understanding"
        ),
    },
}

# ---------------------------------------------------------------------------
# Guild Tier Labels — guild-specific descriptors per tier (1-4)
# ---------------------------------------------------------------------------

GUILD_TIER_LABELS = {
    "ironblood": ["Scrapper", "Ironblood", "Warblade", "Bloodsworn"],
    "veilcraft": ["Shadow", "Veilwalker", "Phantom", "The Unseen"],
    "verdance": ["Wanderer", "Rootbound", "Verdant", "Ancient Voice"],
    "resonance": ["Listener", "Attuned", "Resonant", "Harmonic"],
    "arcane": ["Initiate", "Arcanist", "Adept", "Loremaster"],
    "accord": ["Envoy", "Accord", "Arbiter", "Voice of the Realm"],
    "thornwork": ["Brewer", "Thornworker", "Compound", "Transmuter"],
    "warcraft": ["Conscript", "Tactician", "Commander", "Warchief"],
    "forge": ["Tinkerer", "Forgehand", "Artificer", "Architect"],
    "vaelborn": ["", "Echoing", "Vaelborn", "The Unbroken"],
}

# ---------------------------------------------------------------------------
# Domain Proficiency Labels — score-to-descriptor for display
# ---------------------------------------------------------------------------

DOMAIN_PROFICIENCY_LABELS = [
    (100, "Transcendent"),
    (90, "Virtuosic"),
    (80, "Masterful"),
    (70, "Seasoned"),
    (60, "Expert"),
    (50, "Proficient"),
    (40, "Skilled"),
    (30, "Practiced"),
    (20, "Dabbler"),
    (10, "Novice"),
    (0, "Unaware"),
]

# ---------------------------------------------------------------------------
# GTS Tier Thresholds — descending for first-match iteration
# ---------------------------------------------------------------------------

GTS_TIER_THRESHOLDS = [
    (85, 4),
    (50, 3),
    (20, 2),
    (0, 1),
]

# ---------------------------------------------------------------------------
# Guild Eligibility
# ---------------------------------------------------------------------------

GUILD_ELIGIBILITY_THRESHOLD = 30

GUILD_RECRUITMENT_CONTACTS = {
    "ironblood": ("vaels_crossing", "gq_combat_hall", "npc_guildmaster_combat_haren"),
    "veilcraft": ("vaels_crossing", "gq_subterfuge_den", "npc_guildmaster_subterfuge_dessa"),
    "verdance": ("vaels_crossing", "gq_naturalism_hall", "npc_guildmaster_naturalism_elwen"),
    "resonance": ("vaels_crossing", "gq_resonance_hall", "npc_guildmaster_resonance_kael"),
    "arcane": ("vaels_crossing", "gq_arcana_hall", "npc_guildmaster_arcana_thessa"),
    "accord": ("vaels_crossing", "gq_diplomacy_hall", "npc_guildmaster_diplomacy_aldric"),
    "thornwork": ("vaels_crossing", "gq_alchemy_lab", "npc_guildmaster_alchemy_mirelle"),
    "warcraft": ("vaels_crossing", "gq_tactics_hall", "npc_guildmaster_tactics_brennus"),
    "forge": ("vaels_crossing", "gq_engineering_hall", "npc_guildmaster_engineering_pren"),
}

# ---------------------------------------------------------------------------
# Module-level lookup indexes (built once at import)
# ---------------------------------------------------------------------------

_DOMAIN_TO_GUILD = {g["primary_domain"]: gid for gid, g in GUILDS.items()}

_DOMAIN_PAIR_TO_SUBCLASS = {}
for _sc_id, _sc in SUBCLASSES.items():
    _key = (_sc["primary_domain"], _sc["secondary_domain"])
    _DOMAIN_PAIR_TO_SUBCLASS[_key] = _sc_id

# ---------------------------------------------------------------------------
# Validation assertions — run at import time
# ---------------------------------------------------------------------------

assert set(FINGERPRINTS.keys()) == set(ALL_DOMAINS), (
    "FINGERPRINTS must cover all domains"
)
assert set(_DOMAIN_TO_GUILD.keys()) == set(ALL_DOMAINS), (
    "Every domain must have a guild"
)
assert len(SUBCLASSES) == 90, (
    f"Expected 90 subclasses, got {len(SUBCLASSES)}"
)


# ---------------------------------------------------------------------------
# Computation functions
# ---------------------------------------------------------------------------


def calculate_guild_tier_score(character):
    """
    Compute GTS from primary and secondary domain scores. Always fresh (D-07).

    GTS = (primary_domain_score x 0.66) + (secondary_domain_score x 0.33)
    Max possible: 99 (both domains at 100).
    """
    scores = character.db.domain_scores or {}
    primary = character.db.primary_domain
    secondary = character.db.secondary_domain
    if not primary:
        return 0.0
    p_score = float(scores.get(primary, 0.0))
    s_score = float(scores.get(secondary, 0.0)) if secondary else 0.0
    return (p_score * 0.66) + (s_score * 0.33)


def get_guild_tier(character):
    """Return tier 1-4 based on GTS thresholds (D-08)."""
    gts = calculate_guild_tier_score(character)
    for threshold, tier in GTS_TIER_THRESHOLDS:
        if gts >= threshold:
            return tier
    return 1


def get_guild_tier_label(character):
    """
    Return guild-specific tier label string (D-04/D-06).

    Returns "Wanderer" for characters with no guild.
    """
    guild_id = character.db.guild_id
    if not guild_id:
        return "Wanderer"
    tier = get_guild_tier(character)
    labels = GUILD_TIER_LABELS.get(guild_id)
    if not labels:
        return "Unknown"
    return labels[tier - 1]


def get_domain_proficiency_label(score):
    """
    Return proficiency descriptor for a domain score (0-100).

    Descriptors: Unaware (0-9), Novice (10-19), Dabbler (20-29),
    Practiced (30-39), Skilled (40-49), Proficient (50-59), Expert (60-69),
    Seasoned (70-79), Masterful (80-89), Virtuosic (90-99), Transcendent (100).
    """
    for threshold, label in DOMAIN_PROFICIENCY_LABELS:
        if score >= threshold:
            return label
    return "Unaware"


def check_guild_eligibility(character):
    """
    Return list of guild_ids the character qualifies for.

    A character qualifies when any domain score >= 30 and they have no guild.
    Includes Vaelborn (hidden filtering is a display concern, not engine).
    """
    if character.db.guild_id:
        return []
    scores = character.db.domain_scores or {}
    eligible = []
    for domain, score in scores.items():
        if float(score) >= GUILD_ELIGIBILITY_THRESHOLD:
            guild_id = _DOMAIN_TO_GUILD.get(domain)
            if guild_id:
                eligible.append(guild_id)
    return eligible


def _resolve_subclass(primary_domain, secondary_domain):
    """Return subclass_id for a domain pair, or None."""
    return _DOMAIN_PAIR_TO_SUBCLASS.get((primary_domain, secondary_domain))


def ensure_guild_recruitments(character):
    """Persist each newly earned, player-visible guild invitation."""
    from world.models import GuildRecruitment
    from world.remnance_visibility import guild_is_player_visible

    created_records = []
    for guild_id in check_guild_eligibility(character):
        guild = GUILDS.get(guild_id, {})
        contact = GUILD_RECRUITMENT_CONTACTS.get(guild_id)
        if not contact or not guild_is_player_visible(guild_id, guild, character):
            continue
        zone_id, room_id, npc_id = contact
        recruitment, created = GuildRecruitment.objects.get_or_create(
            character=character,
            guild_id=guild_id,
            defaults={
                "contact_npc_id": npc_id,
                "location_zone_id": zone_id,
                "location_room_id": room_id,
            },
        )
        if created:
            created_records.append(recruitment)
    return created_records


def get_recruitment_for_contact(character, contact):
    """Return an open invitation only at its authored contact and location."""
    from world.models import GuildRecruitment

    npc_id = getattr(contact.db, "npc_id", None)
    location = getattr(contact, "location", None)
    if not npc_id or location != character.location:
        return None
    recruitment = GuildRecruitment.objects.filter(
        character=character,
        contact_npc_id=npc_id,
        status="offered",
    ).first()
    if not recruitment or not location.tags.has(
        recruitment.location_room_id,
        category="room_id",
    ):
        return None
    return recruitment


def get_open_guild_recruitments(character):
    """Return durable open invitations in delivery order."""
    from world.models import GuildRecruitment

    return list(
        GuildRecruitment.objects.filter(
            character=character,
            status="offered",
        ).order_by("offered_at", "id")
    )


def get_recruitment_secondary_choices(character, recruitment):
    """Return visible secondary domains in authored domain order."""
    from world.remnance_visibility import domain_is_player_visible

    primary = GUILDS[recruitment.guild_id]["primary_domain"]
    return [
        domain
        for domain in ALL_DOMAINS
        if domain != primary and domain_is_player_visible(domain, character)
    ]


def _record_induction_social_fact(character, recruitment, contact):
    from world.social_engine import ensure_social_node, mark_known, record_social_fact

    guild = GUILDS[recruitment.guild_id]
    player = ensure_social_node(
        "player",
        str(character.id),
        display_name=character.key,
    )
    contact_node = ensure_social_node(
        "npc",
        recruitment.contact_npc_id,
        display_name=contact.key,
        zone_id=recruitment.location_zone_id,
    )
    guild_node = ensure_social_node(
        "guild",
        recruitment.guild_id,
        display_name=guild["name"],
        zone_id=recruitment.location_zone_id,
    )
    fact_key = f"fact:guild_induction:{character.id}:{recruitment.guild_id}"
    ok, message, fact = record_social_fact(
        fact_key=fact_key,
        subject_node_key=player.node_key,
        actor_node_key=contact_node.node_key,
        scope_node_key=guild_node.node_key,
        event_type="guild_inducted",
        summary=(
            f"{character.key} completed induction into {guild['name']} "
            f"under {contact.key}."
        ),
        tags=["guild", "induction", recruitment.guild_id],
        visibility="institutional",
        evidence={
            "guild_id": recruitment.guild_id,
            "secondary_domain": recruitment.secondary_domain,
            "contact_npc_id": recruitment.contact_npc_id,
        },
    )
    if not ok:
        raise RuntimeError(message)
    for node in (contact_node, guild_node):
        ok, message, _knowledge = mark_known(
            node_key=node.node_key,
            fact_key=fact.fact_key,
            source_node_key=contact_node.node_key,
            channel="guild_record",
            confidence=1.0,
            spreading=False,
            evidence={"source": "guild_induction"},
        )
        if not ok:
            raise RuntimeError(message)


def complete_recruitment_induction(character, recruitment, secondary_domain, contact):
    """Complete one invitation only at its authored NPC and room."""
    from django.utils import timezone

    from world.models import CharacterGuild, GuildRecruitment
    from world.remnance_visibility import domain_is_player_visible

    if recruitment.character_id != character.id:
        return False, "That invitation does not belong to you."
    if recruitment.status == "completed":
        return True, "Your induction is already complete."
    if character.location != getattr(contact, "location", None):
        return False, "You must meet the guild contact in person."
    if getattr(contact.db, "npc_id", None) != recruitment.contact_npc_id:
        return False, "This is not the contact named in your invitation."
    if not character.location.tags.has(
        recruitment.location_room_id,
        category="room_id",
    ):
        return False, "You must meet the guild contact in person."
    if recruitment.guild_id not in check_guild_eligibility(character):
        return False, "That guild invitation is no longer available."

    guild = GUILDS[recruitment.guild_id]
    primary_domain = guild["primary_domain"]
    if not domain_is_player_visible(secondary_domain, character):
        return False, "That secondary domain is not available for induction."
    subclass_id = _resolve_subclass(primary_domain, secondary_domain)
    if not subclass_id:
        return False, "That secondary path does not fit this guild."

    from world.atomic_state import atomic_evennia_state

    cache_names = ("guild_id", "subclass_id", "primary_domain", "secondary_domain")
    with atomic_evennia_state(character) as cache_tracker:
        cache_tracker.track(character, attributes=cache_names)
        locked = GuildRecruitment.objects.select_for_update().get(pk=recruitment.pk)
        if locked.status == "completed":
            return True, "Your induction is already complete."

        membership, _created = CharacterGuild.objects.update_or_create(
            character=character,
            defaults={
                "guild_id": locked.guild_id,
                "primary_domain": primary_domain,
                "secondary_domain": secondary_domain,
                "subclass_id": subclass_id,
                "induction_complete": True,
            },
        )
        character.db.guild_id = membership.guild_id
        character.db.subclass_id = membership.subclass_id
        character.db.primary_domain = membership.primary_domain
        character.db.secondary_domain = membership.secondary_domain

        locked.status = "completed"
        locked.secondary_domain = secondary_domain
        locked.completed_at = timezone.now()
        locked.save(update_fields=["status", "secondary_domain", "completed_at"])
        _record_induction_social_fact(character, locked, contact)

        from world.ability_engine import sync_character_ability_unlocks

        sync_character_ability_unlocks(character)

    from world.ability_engine import initialize_domain_resource

    initialize_domain_resource(character)
    return True, f"Your induction into {guild['name']} is complete."


# ---------------------------------------------------------------------------
# Mutation functions
# ---------------------------------------------------------------------------


def join_guild(character, guild_id, secondary_domain):
    """
    Fail-closed compatibility boundary for the retired remote join path.

    Membership now exists only after complete_recruitment_induction validates
    the durable invitation, authored contact, and current room.
    """
    if character.db.guild_id:
        existing = GUILDS.get(character.db.guild_id, {})
        existing_name = existing.get("name", character.db.guild_id)
        return False, f"Already a member of {existing_name}."
    return False, (
        "Guild membership requires a durable invitation and an in-person "
        "induction with its named contact."
    )


def complete_induction(character):
    """
    Fail-closed compatibility boundary for detached induction completion.
    """
    return False, (
        "Induction can only be completed in person through the durable "
        "recruitment scene."
    )
