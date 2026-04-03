"""
File-based help entries for Soravelon.

Comprehensive help covering new player guides, game systems, commands,
ancestries, guilds, and skills. Loaded by Evennia via
settings.FILE_HELP_ENTRY_MODULES.

Each entry in HELP_ENTRY_DICTS is a dict with keys:
  key, text, category (optional), aliases (optional), locks (optional)
"""

HELP_ENTRY_DICTS = [
    # =========================================================================
    # DEVELOPER (1 entry, locked)
    # =========================================================================
    {
        "key": "evennia",
        "aliases": ["ev"],
        "category": "General",
        "locks": "read:perm(Developer)",
        "text": (
            "Evennia is the MU-game server and framework powering Soravelon. "
            "You can read more on https://www.evennia.com."
        ),
    },
    # =========================================================================
    # NEW PLAYER (5 entries)
    # =========================================================================
    {
        "key": "getting started",
        "aliases": ["new player", "newbie", "beginner"],
        "category": "New Player",
        "locks": "read:all()",
        "text": (
            "Welcome to |wSoravelon|n, a world where ancient dragon-built "
            "infrastructure crumbles and mortals inherit power they barely "
            "understand.\n\n"
            "|wFirst steps:|n\n"
            "  1. Choose your |cancestry|n -- type |wancestry|n to see options\n"
            "  2. Explore the world -- |wlook|n, |wsearch|n, |wmap|n\n"
            "  3. Discover |cguilds|n by visiting guild halls -- type |wjoinguild|n\n"
            "  4. Learn |cabilities|n as you advance -- type |wabilities|n\n"
            "  5. Fight creatures with |wattack|n and |wuse <ability>|n\n\n"
            "Type |whelp <topic>|n for more on any system. "
            "Type |whelp|n alone to see all help categories."
        ),
    },
    {
        "key": "character creation",
        "aliases": ["chargen", "create character"],
        "category": "New Player",
        "locks": "read:all()",
        "text": (
            "Your journey begins with choosing an |wancestry|n. Each of the "
            "four ancestries -- Human, Kau'roran, Veth, and Selvar -- grants "
            "unique traits that shape how you interact with the world.\n\n"
            "Type |wancestry <name>|n to choose. Selvar characters also choose "
            "a seasonal coat (|wancestry selvar summer|n or |wancestry selvar winter|n).\n\n"
            "After choosing, you start with basic equipment and a starting "
            "ability tied to your ancestry. Explore your surroundings to find "
            "guild halls where you can begin developing domain mastery."
        ),
    },
    {
        "key": "combat basics",
        "aliases": ["fighting"],
        "category": "New Player",
        "locks": "read:all()",
        "text": (
            "Combat in Soravelon is |wturn-based|n with an action budget.\n\n"
            "|wStarting a fight:|n\n"
            "  |wattack <target>|n -- Engage a hostile creature\n\n"
            "|wDuring combat:|n\n"
            "  |wuse <ability>|n -- Use one of your abilities\n"
            "  |wattack|n -- Basic attack against your target\n"
            "  |wflee|n -- Attempt to escape combat\n\n"
            "Your |caction budget|n determines how many actions you get per "
            "round. Using multiple actions in a round reduces each action's "
            "damage. Status effects like poison, bleed, or stun can change "
            "the flow of battle.\n\n"
            "Type |whelp combat|n for the full combat system reference."
        ),
    },
    {
        "key": "exploration",
        "aliases": ["exploring"],
        "category": "New Player",
        "locks": "read:all()",
        "text": (
            "The world of Soravelon rewards the curious.\n\n"
            "|wMovement:|n Use compass directions (|wnorth|n, |wsouth|n, etc.) "
            "or named exits to move between rooms.\n\n"
            "|wDiscovery:|n\n"
            "  |wsearch|n -- Reveal hidden exits, items, and lore fragments\n"
            "  |wmap|n -- View your zone map\n"
            "  |wsense|n -- Read the ambient state of your surroundings\n\n"
            "Some exits are |chidden|n and only appear after searching. "
            "Others are |clocked|n and require a key. Zones contain nodes "
            "of ancient magic in various states of decay -- from healthy "
            "to collapsed -- that affect the environment around them."
        ),
    },
    {
        "key": "currency",
        "aliases": ["scales", "money", "gold"],
        "category": "New Player",
        "locks": "read:all()",
        "text": (
            "The currency of Soravelon is |wScales|n -- thin iridescent "
            "coins originally minted by dragon civilization.\n\n"
            "|wEarning Scales:|n Defeating creatures, completing quests, "
            "selling crafted goods, and trading with NPCs.\n\n"
            "|wCarried vs Banked:|n You carry Scales on your person (lost on "
            "death) or store them safely at a bank branch. Use |wbank|n, "
            "|wdeposit|n, and |wwithdraw|n to manage your finances.\n\n"
            "The Consortium issues |cDrafts|n -- transferable notes of credit "
            "used for large transactions."
        ),
    },
    # =========================================================================
    # SYSTEMS (11 entries)
    # =========================================================================
    {
        "key": "combat",
        "aliases": ["combat system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wCombat System|n\n\n"
            "Combat is turn-based with initiative determining action order.\n\n"
            "|cAction Budget:|n Each round you have a number of actions based "
            "on your agility. Using more actions reduces damage per action.\n\n"
            "|cAbilities:|n Your primary combat tools. Each costs a domain "
            "resource and may have cooldowns. Type |wuse <ability>|n.\n\n"
            "|cStatus Effects:|n Abilities can inflict conditions like poison, "
            "bleed, stun, or root. Some effects compound -- applying bleed "
            "to a poisoned target creates hemorrhage.\n\n"
            "|cTargeting:|n |wattack <target>|n to engage. |wtarget <name>|n "
            "to switch targets mid-combat.\n\n"
            "|cFleeing:|n Type |wflee|n to attempt escape. Success depends "
            "on your speed relative to enemies.\n\n"
            "Defeated enemies drop loot scaled to your progression. Group "
            "combat distributes loot according to the party's loot mode."
        ),
    },
    {
        "key": "guilds",
        "aliases": ["guild system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wGuild System|n\n\n"
            "Soravelon has 10 guilds, each tied to a domain of mastery. "
            "Discover guilds by visiting their halls in hub cities, then "
            "type |wjoinguild <guild>|n.\n\n"
            "|cGuild Tier Score (GTS):|n Your advancement within a guild is "
            "measured by GTS, computed from your domain scores. Higher GTS "
            "unlocks more powerful abilities.\n\n"
            "|cTier thresholds:|n 0 (join), 20, 50, 85\n\n"
            "|cSubclasses:|n When you develop a secondary domain alongside "
            "your guild's primary, you unlock a unique subclass identity. "
            "There are 90 possible subclasses across all guilds.\n\n"
            "|w10 Guilds:|n Ironblood (Combat), Veilcraft (Subterfuge), "
            "Verdance (Naturalism), Resonance (Resonance), Arcane (Arcana), "
            "Accord (Diplomacy), Thornwork (Alchemy), Warcraft (Tactics), "
            "Forge (Engineering), Vaelborn (Remnance)"
        ),
    },
    {
        "key": "domains",
        "aliases": ["domain system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wDomain System|n\n\n"
            "There are 10 domains of mastery in Soravelon. Your domain "
            "scores determine your Guild Tier Score and which abilities "
            "you unlock.\n\n"
            "|c10 Domains:|n\n"
            "  |wCombat|n -- Sustained aggression (Momentum)\n"
            "  |wSubterfuge|n -- Timing and precision (Focus)\n"
            "  |wNaturalism|n -- Managed duality (Balance)\n"
            "  |wResonance|n -- Environmental sensitivity (Resonance)\n"
            "  |wArcana|n -- Cross-encounter management (Mana)\n"
            "  |wDiplomacy|n -- Relationships as power (Influence)\n"
            "  |wAlchemy|n -- Preparation philosophy (Reagents)\n"
            "  |wTactics|n -- Group synergy (Command)\n"
            "  |wEngineering|n -- Mechanical companions (Components)\n"
            "  |wRemnance|n -- Knowledge as power (Echoes)\n\n"
            "Each domain has a unique resource that fuels its abilities. "
            "Type |wdomains|n to see your current domain scores."
        ),
    },
    {
        "key": "abilities",
        "aliases": ["ability system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wAbility System|n\n\n"
            "Abilities are your primary tools in combat and beyond. Each "
            "ability belongs to a domain and costs a domain resource.\n\n"
            "|cTiers:|n Abilities unlock at GTS thresholds:\n"
            "  Tier 1: GTS 0 (immediate)  |  Tier 2: GTS 20\n"
            "  Tier 3: GTS 50             |  Tier 4: GTS 85\n\n"
            "|cUsing abilities:|n |wuse <ability name>|n\n"
            "|cViewing abilities:|n |wabilities|n to see what you know\n"
            "|cAbility details:|n |whelp <ability name>|n for full info\n\n"
            "|cCooldowns:|n After using an ability, it may go on cooldown "
            "for a number of rounds before it can be used again.\n\n"
            "|cScaling:|n Ability power scales with your domain scores. "
            "Some abilities scale with two domains."
        ),
    },
    {
        "key": "ancestry",
        "aliases": ["ancestries", "races"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wAncestry System|n\n\n"
            "Your ancestry defines who you are in the world of Soravelon. "
            "Each of the four ancestries grants unique mechanical traits "
            "that influence combat, exploration, and social interactions.\n\n"
            "|wHuman|n -- Adaptable, diplomatic. Bonus to all attributes, "
            "faster reputation gain, reduced status durations.\n\n"
            "|wKau'roran|n -- Towering, resilient. +30%% HP, enhanced "
            "strength, faster trust building with factions.\n\n"
            "|wVeth|n -- Quick, cunning. Enhanced agility, faster movement, "
            "warren sense reveals hidden passages underground.\n\n"
            "|wSelvar|n -- Fierce, seasonal. Reckless momentum in combat, "
            "summer/winter coat grants different bonuses.\n\n"
            "Type |whelp <ancestry name>|n for detailed info on each."
        ),
    },
    {
        "key": "crafting",
        "aliases": ["crafting system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wCrafting System|n\n\n"
            "Create equipment, consumables, and reagents at crafting stations.\n\n"
            "|cStations:|n Different crafts require specific stations:\n"
            "  Forge -- |wsmith|n weapons and armor\n"
            "  Kitchen -- |wcook|n food and provisions\n"
            "  Alchemy Bench -- |wbrew|n potions and reagents\n"
            "  Workbench -- |wcraft|n general items\n\n"
            "|cRecipes:|n Type |wrecipes|n to see known recipes. New recipes "
            "are discovered through exploration and skill advancement.\n\n"
            "|cQuality:|n Output quality depends on your skill level, "
            "material tier, and recipe difficulty. Higher quality items "
            "provide stronger effects."
        ),
    },
    {
        "key": "banking",
        "aliases": ["bank system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wBanking System|n\n\n"
            "The Consortium operates bank branches throughout Soravelon.\n\n"
            "|cBasic operations:|n\n"
            "  |wbank|n -- Check your balance\n"
            "  |wdeposit <amount>|n -- Store Scales safely\n"
            "  |wwithdraw <amount>|n -- Retrieve stored Scales\n\n"
            "|cDrafts:|n Consortium Drafts are transferable notes of credit "
            "for large transactions. Useful when carrying large sums is risky.\n\n"
            "|cDebt:|n Borrowing against your account incurs debt. "
            "Unpaid debt accrues interest and may affect your standing with "
            "the Consortium faction."
        ),
    },
    {
        "key": "equipment",
        "aliases": ["gear system", "equip system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wEquipment System|n\n\n"
            "Equip weapons and armor to improve your combat effectiveness.\n\n"
            "|cCommands:|n\n"
            "  |wequip <item>|n -- Equip an item from your inventory\n"
            "  |wunequip <item>|n -- Remove an equipped item\n"
            "  |wgear|n -- View your current equipment\n\n"
            "|cSlots:|n Each piece of equipment fits a specific slot. You "
            "cannot equip two items in the same slot.\n\n"
            "|cMaterial tiers:|n Equipment quality follows material tiers "
            "that affect base stats. Higher-tier materials are found in "
            "more dangerous zones.\n\n"
            "|cScaling:|n Weapon damage and armor protection scale with "
            "your attributes and domain scores."
        ),
    },
    {
        "key": "skills",
        "aliases": ["skill system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wSkill System|n\n\n"
            "Skills represent general proficiencies that improve through use.\n\n"
            "|cViewing skills:|n Type |wskills|n to see your current skill levels.\n"
            "|cPracticing:|n |wpractice <skill>|n to actively train a skill.\n"
            "|cTrainers:|n |wtrain <skill>|n at a trainer NPC for faster gains.\n\n"
            "Skills range from 0 to 100. Higher skill levels improve your "
            "effectiveness at related tasks and may unlock new recipes, "
            "dialogue options, or interactions.\n\n"
            "Skill categories include investigation, lockpicking, cooking, "
            "smithing, alchemy, herbalism, and more."
        ),
    },
    {
        "key": "quests",
        "aliases": ["quest system", "journal"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wQuest System|n\n\n"
            "Quests track your objectives and story progress.\n\n"
            "|cCommands:|n\n"
            "  |wquest|n -- View your quest journal\n"
            "  |wquest <name>|n -- View details for a specific quest\n\n"
            "Quests are offered by NPCs, discovered through exploration, "
            "or triggered by world events. Each quest lists objectives "
            "and rewards. Completed quests may affect faction standings "
            "and unlock new areas."
        ),
    },
    {
        "key": "factions",
        "aliases": ["standings", "reputation", "faction system"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wFaction System|n\n\n"
            "Your reputation with the world's factions shapes how NPCs "
            "treat you and what opportunities open.\n\n"
            "|cStanding:|n Ranges from deeply hostile to revered. Actions "
            "in the world -- combat kills, quest choices, dialogue -- "
            "shift your standing.\n\n"
            "|cTrust:|n A separate measure (0-100) that tracks how much "
            "a faction trusts you personally. Trust unlocks special "
            "services, quests, and dialogue options.\n\n"
            "|cBetrayal:|n Major actions against a faction may trigger a "
            "permanent betrayal flag, dramatically altering your "
            "relationship. Choose carefully.\n\n"
            "Your ancestry affects starting standings with various factions."
        ),
    },
    # =========================================================================
    # COMMANDS (~40 entries)
    # =========================================================================
    # -- Exploration --
    {
        "key": "search",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n search\n\n"
            "Search your current room for hidden exits, concealed items, "
            "and lore fragments. Some hidden passages only reveal themselves "
            "to those who look carefully.\n\n"
            "|wExample:|n\n"
            "  > search\n"
            "  You notice a faint draft from behind the bookshelf..."
        ),
    },
    {
        "key": "map",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n map\n\n"
            "Display a map of your current zone, showing rooms you have "
            "visited and their connections.\n\n"
            "|wExample:|n\n"
            "  > map"
        ),
    },
    # -- Ancestry & Guilds --
    {
        "key": "ancestry command",
        "aliases": ["setancestry"],
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n ancestry <name> [coat]\n\n"
            "Choose your character's ancestry during creation. This is "
            "a permanent choice that grants unique traits and abilities.\n\n"
            "Available ancestries: Human, Kau'roran, Veth, Selvar\n"
            "Selvar characters also choose a coat: |wancestry selvar summer|n "
            "or |wancestry selvar winter|n\n\n"
            "|wExample:|n\n"
            "  > ancestry human\n"
            "  > ancestry selvar winter"
        ),
    },
    {
        "key": "joinguild",
        "aliases": ["join guild"],
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n joinguild <guild name>\n\n"
            "Join a guild after discovering its hall. You must be in a "
            "room where the guild can be joined. Joining grants access to "
            "the guild's tier 1 abilities.\n\n"
            "|wExample:|n\n"
            "  > joinguild ironblood"
        ),
    },
    {
        "key": "domains command",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n domains\n\n"
            "Display your current domain scores across all 10 domains. "
            "Shows your primary and secondary domains, GTS progress, "
            "and current subclass if applicable.\n\n"
            "|wExample:|n\n"
            "  > domains"
        ),
    },
    {
        "key": "abilities command",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n abilities\n\n"
            "List all abilities you currently have access to, organized "
            "by domain. Shows ability name, tier, cooldown status, and "
            "resource cost.\n\n"
            "|wExample:|n\n"
            "  > abilities"
        ),
    },
    {
        "key": "use",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n use <ability name>\n\n"
            "Activate one of your abilities. In combat, consumes an action "
            "and spends the ability's domain resource cost. Outside combat, "
            "social and utility abilities can be used freely.\n\n"
            "Ability names support progressive word matching -- you only "
            "need to type enough of the name to be unique.\n\n"
            "|wExamples:|n\n"
            "  > use momentum strike\n"
            "  > use wild mend\n"
            "  > use mom   (matches 'Momentum Strike' if unique)"
        ),
    },
    # -- Combat --
    {
        "key": "attack",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n attack <target>\n\n"
            "Initiate combat with a target or perform a basic attack "
            "against your current target. Basic attacks cost no resources "
            "but deal less damage than abilities.\n\n"
            "|wExamples:|n\n"
            "  > attack wolf\n"
            "  > attack"
        ),
    },
    {
        "key": "flee",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n flee\n\n"
            "Attempt to escape from combat. Success depends on your speed "
            "relative to your enemies. A failed flee attempt wastes your "
            "action for the round.\n\n"
            "|wExample:|n\n"
            "  > flee"
        ),
    },
    {
        "key": "target",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n target <name>\n\n"
            "Switch your combat target to a different enemy. Your abilities "
            "and basic attacks will be directed at the new target.\n\n"
            "|wExample:|n\n"
            "  > target dire wolf"
        ),
    },
    {
        "key": "pass",
        "aliases": ["skip turn"],
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n pass\n\n"
            "Skip your remaining actions this round. Useful when conserving "
            "resources or waiting for cooldowns to expire.\n\n"
            "|wExample:|n\n"
            "  > pass"
        ),
    },
    # -- Skills --
    {
        "key": "skills command",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n skills\n\n"
            "Display your current skill levels and progress. Skills are "
            "organized by category and show your proficiency (0-100).\n\n"
            "|wExample:|n\n"
            "  > skills"
        ),
    },
    {
        "key": "practice",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n practice <skill name>\n\n"
            "Practice a skill to improve your proficiency. Practice is "
            "slower than training with an NPC but can be done anywhere.\n\n"
            "|wExample:|n\n"
            "  > practice lockpicking"
        ),
    },
    {
        "key": "train",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n train <skill name>\n\n"
            "Train a skill with a trainer NPC. You must be near a trainer "
            "who teaches the skill. Training provides faster advancement "
            "than solo practice.\n\n"
            "|wExample:|n\n"
            "  > train smithing"
        ),
    },
    # -- Dialogue --
    {
        "key": "talk",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n talk <npc>\n\n"
            "Begin a conversation with an NPC. The NPC will greet you and "
            "may present topics you can ask about.\n\n"
            "|wExample:|n\n"
            "  > talk merchant"
        ),
    },
    {
        "key": "ask",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n ask <npc> about <topic>\n\n"
            "Ask an NPC about a specific topic. Available topics are "
            "revealed through conversation and exploration.\n\n"
            "|wExample:|n\n"
            "  > ask merchant about rumors"
        ),
    },
    {
        "key": "say",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n say <message>\n\n"
            "Speak aloud in your current room. Everyone present, "
            "including NPCs, can hear you. Some NPCs respond to "
            "keywords in your speech.\n\n"
            "|wExample:|n\n"
            "  > say Hello, is anyone here?"
        ),
    },
    {
        "key": "tell",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n tell <player> <message>\n\n"
            "Send a private message to another player. The message is "
            "only visible to you and the recipient.\n\n"
            "|wExample:|n\n"
            "  > tell Arden Watch your back in the ruins."
        ),
    },
    {
        "key": "accept",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n accept\n\n"
            "Accept a pending offer, quest, or invitation from an NPC "
            "or another player.\n\n"
            "|wExample:|n\n"
            "  > accept"
        ),
    },
    {
        "key": "decline",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n decline\n\n"
            "Decline a pending offer, quest, or invitation.\n\n"
            "|wExample:|n\n"
            "  > decline"
        ),
    },
    # -- Crafting --
    {
        "key": "cook",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n cook <recipe>\n\n"
            "Cook a recipe at a kitchen station. You must have the required "
            "ingredients in your inventory and be near a cooking station.\n\n"
            "|wExample:|n\n"
            "  > cook hearty stew"
        ),
    },
    {
        "key": "smith",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n smith <recipe>\n\n"
            "Forge a weapon or armor at a smithing station. Requires "
            "appropriate materials and proximity to a forge.\n\n"
            "|wExample:|n\n"
            "  > smith iron longsword"
        ),
    },
    {
        "key": "brew",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n brew <recipe>\n\n"
            "Brew a potion or reagent at an alchemy bench. Requires "
            "ingredients and proximity to an alchemy station.\n\n"
            "|wExample:|n\n"
            "  > brew healing draught"
        ),
    },
    {
        "key": "craft",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n craft <recipe>\n\n"
            "Craft a general item at a workbench. Used for miscellaneous "
            "items that do not fall under cooking, smithing, or alchemy.\n\n"
            "|wExample:|n\n"
            "  > craft rope ladder"
        ),
    },
    {
        "key": "recipes",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n recipes [category]\n\n"
            "List all recipes you have discovered. Optionally filter by "
            "category (cooking, smithing, alchemy, general).\n\n"
            "|wExamples:|n\n"
            "  > recipes\n"
            "  > recipes cooking"
        ),
    },
    # -- Equipment --
    {
        "key": "equip",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n equip <item>\n\n"
            "Equip an item from your inventory to the appropriate slot. "
            "If the slot is occupied, you must unequip first.\n\n"
            "|wExample:|n\n"
            "  > equip iron longsword"
        ),
    },
    {
        "key": "unequip",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n unequip <item>\n\n"
            "Remove an equipped item and return it to your inventory.\n\n"
            "|wExample:|n\n"
            "  > unequip iron longsword"
        ),
    },
    {
        "key": "gear",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n gear\n\n"
            "Display all your currently equipped items, organized by slot. "
            "Shows item name, material tier, and key stats.\n\n"
            "|wExample:|n\n"
            "  > gear"
        ),
    },
    # -- Node Interaction --
    {
        "key": "stabilize",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n stabilize\n\n"
            "Attempt to stabilize a stressed or failing magical node in "
            "your current room. Requires resonance attunement and may "
            "consume resources. Successful stabilization can reverse "
            "node decay and restore the area.\n\n"
            "|wExample:|n\n"
            "  > stabilize"
        ),
    },
    # -- Player Surface --
    {
        "key": "status",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n status\n\n"
            "Display your character's current status including health, "
            "stamina, active effects, domain resources, and combat state.\n\n"
            "|wExample:|n\n"
            "  > status"
        ),
    },
    {
        "key": "sense",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n sense\n\n"
            "Read the ambient state of your surroundings. Reveals room "
            "state flags, node influence, environmental effects, and "
            "lingering magical traces. The depth of information depends "
            "on your resonance attunement.\n\n"
            "|wExample:|n\n"
            "  > sense\n"
            "  The air hums with residual node energy. You sense decay..."
        ),
    },
    {
        "key": "bank",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n bank\n\n"
            "Check your bank balance. Shows carried Scales, banked Scales, "
            "outstanding drafts, and any debt.\n\n"
            "|wExample:|n\n"
            "  > bank"
        ),
    },
    {
        "key": "deposit",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n deposit <amount>\n\n"
            "Deposit Scales from your carried currency into your bank "
            "account. You must be at a bank branch.\n\n"
            "|wExample:|n\n"
            "  > deposit 500"
        ),
    },
    {
        "key": "withdraw",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n withdraw <amount>\n\n"
            "Withdraw Scales from your bank account to carried currency. "
            "You must be at a bank branch.\n\n"
            "|wExample:|n\n"
            "  > withdraw 200"
        ),
    },
    # -- Group --
    {
        "key": "group",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n\n"
            "  group -- View your current group\n"
            "  group invite <player> -- Invite a player\n"
            "  group leave -- Leave your group\n"
            "  group kick <player> -- Remove a member (leader only)\n"
            "  group loot <mode> -- Set loot distribution mode\n"
            "  group leader <player> -- Transfer leadership\n\n"
            "Groups (parties) support up to 6 members. Four loot modes "
            "are available: round-robin, need/greed, leader-assigns, and "
            "free-for-all. Groups are session-only and disband on logout.\n\n"
            "|wExample:|n\n"
            "  > group invite Arden"
        ),
    },
    # -- Loadout --
    {
        "key": "loadout",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n\n"
            "  loadout -- View your current ability loadout\n"
            "  loadout set <slot> <ability> -- Assign an ability to a slot\n"
            "  loadout clear <slot> -- Clear a slot\n\n"
            "Your loadout determines which abilities are readily available "
            "in combat. Organize your abilities for quick access.\n\n"
            "|wExample:|n\n"
            "  > loadout set 1 momentum strike"
        ),
    },
    # -- Flight --
    {
        "key": "fly",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n fly <destination>\n\n"
            "Board the Dragon Courier Service for instant transit to "
            "a discovered destination. You must be at a courier station. "
            "Fare varies by distance and your faction standing.\n\n"
            "|wExample:|n\n"
            "  > fly caldenmere"
        ),
    },
    {
        "key": "disembark",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n disembark\n\n"
            "Leave the Dragon Courier at the next intermediate stop. "
            "Useful if you want to explore a waypoint rather than "
            "continuing to your final destination.\n\n"
            "|wExample:|n\n"
            "  > disembark"
        ),
    },
    {
        "key": "routes",
        "aliases": ["flight routes", "flights"],
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n routes\n\n"
            "Display available Dragon Courier routes from your current "
            "location, including destinations, fares, and travel times.\n\n"
            "|wExample:|n\n"
            "  > routes"
        ),
    },
    # -- Alias --
    {
        "key": "alias",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n alias <name> <command>\n\n"
            "Create a personal command alias. The alias expands tokens: "
            "$1, $2 for positional arguments, $* for all arguments.\n\n"
            "|wExamples:|n\n"
            "  > alias ms use momentum strike\n"
            "  > alias heal use wild mend\n"
            "  > alias t target $1"
        ),
    },
    {
        "key": "unalias",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n unalias <name>\n\n"
            "Remove a personal command alias.\n\n"
            "|wExample:|n\n"
            "  > unalias ms"
        ),
    },
    # -- Quest --
    {
        "key": "quest command",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n\n"
            "  quest -- View your quest journal\n"
            "  quest <name> -- View details of a specific quest\n\n"
            "Your quest journal tracks active, completed, and failed "
            "quests. Each quest shows objectives, progress, and rewards.\n\n"
            "|wExample:|n\n"
            "  > quest\n"
            "  > quest the sunken ward"
        ),
    },
    # -- Lore (placeholder for Plan 03) --
    {
        "key": "lore",
        "category": "Commands",
        "locks": "read:all()",
        "text": (
            "|wUsage:|n lore\n\n"
            "Review lore fragments you have collected through exploration. "
            "Lore fragments provide insight into the world's history, "
            "the Dragon Curse, and the factions vying for power.\n\n"
            "|yThis system is being expanded.|n"
        ),
    },
    # =========================================================================
    # ANCESTRIES (4 entries)
    # =========================================================================
    {
        "key": "human",
        "category": "Ancestries",
        "locks": "read:all()",
        "text": (
            "|wHuman|n\n\n"
            "Humans are the most numerous people in Soravelon, inheritors "
            "of an empire built on dragon infrastructure they only partially "
            "understand. Adaptable and politically connected, Humans thrive "
            "in every environment through sheer resourcefulness.\n\n"
            "|cMechanical Traits:|n\n"
            "  |wAttribute Bonus:|n +1 to all base attributes\n"
            "  |wReputation Generation:|n 15%% faster reputation gain\n"
            "  |wStatus Resist:|n 10%% reduced status effect duration\n"
            "  |wStarting Ability:|n Second Wind\n\n"
            "|cDomain Interactions:|n\n"
            "  Combat: Bonus reputation from kills\n"
            "  Naturalism: Zone attunement gains in any environment\n"
            "  Subterfuge: Bonus network gains from jobs\n\n"
            "|cStarting Standing:|n Favorable with the Empire"
        ),
    },
    {
        "key": "kauroran",
        "aliases": ["kau'roran"],
        "category": "Ancestries",
        "locks": "read:all()",
        "text": (
            "|wKau'roran|n\n\n"
            "The Kau'roran are towering, resilient people descended from "
            "highland clans who once served as wardens of dragon-built "
            "fortifications. They value honor, community, and endurance "
            "above all else.\n\n"
            "|cMechanical Traits:|n\n"
            "  |wHP Bonus:|n +30%% maximum health\n"
            "  |wStrength Scaling:|n +20%% strength effectiveness\n"
            "  |wTrust Build Rate:|n +20%% faster trust with factions\n"
            "  |wStarting Ability:|n Immovable\n\n"
            "|cDomain Interactions:|n\n"
            "  Combat: Additional strength scaling\n"
            "  Naturalism: Bonus AoE magnitude\n"
            "  Subterfuge: Focus generated on melee hits\n\n"
            "|cStarting Standing:|n Favorable with Kau'roran clans and "
            "Wardens; distrusted by the Empire"
        ),
    },
    {
        "key": "veth",
        "category": "Ancestries",
        "locks": "read:all()",
        "text": (
            "|wVeth|n\n\n"
            "The Veth are a lithe, quick people who dwell in underground "
            "warrens beneath Soravelon's cities and wilds. Masters of "
            "stealth and cunning, they see paths others miss.\n\n"
            "|cMechanical Traits:|n\n"
            "  |wAgility Scaling:|n +25%% agility effectiveness\n"
            "  |wSpeed Bonus:|n +15%% movement speed\n"
            "  |wWarren Sense:|n Automatically detect hidden underground passages\n"
            "  |wGuard Threshold:|n 30%% higher threshold before guards turn hostile\n"
            "  |wStarting Ability:|n Vanish\n\n"
            "|cDomain Interactions:|n\n"
            "  Combat: Momentum gained from enemy misses\n"
            "  Naturalism: Double attunement in underground zones\n"
            "  Subterfuge: Double network gains\n\n"
            "|cStarting Standing:|n Favorable with the Consortium"
        ),
    },
    {
        "key": "selvar",
        "category": "Ancestries",
        "locks": "read:all()",
        "text": (
            "|wSelvar|n\n\n"
            "The Selvar are fierce, mercurial people whose physiology "
            "shifts with the seasons. Summer Selvar are quick and sharp; "
            "winter Selvar are tough and resilient. They are distrusted "
            "by most factions but respected for their raw power.\n\n"
            "|cMechanical Traits:|n\n"
            "  |wReckless Momentum:|n +20%% bonus momentum in combat\n"
            "  |wStarting Ability:|n Audacity\n\n"
            "|cSeasonal Coat:|n Choose at character creation.\n"
            "  |ySummer:|n +10%% agility, +5%% focus generation\n"
            "  |ySummer:|n +10%% endurance, +5%% status resistance\n\n"
            "|cDomain Interactions:|n\n"
            "  Combat: Momentum does not decay between rounds\n"
            "  Naturalism: Mana regeneration on applying status effects\n"
            "  Subterfuge: Focus generated when status effects land\n\n"
            "|cStarting Standing:|n Penalty with all factions; offset "
            "partially by guild membership"
        ),
    },
    # =========================================================================
    # GUILDS (10 entries)
    # =========================================================================
    {
        "key": "ironblood",
        "aliases": ["guild of ironblood"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Ironblood|n\n"
            "|x\"Strength is not a gift. It is a debt you pay every day.\"|n\n\n"
            "|cPrimary Domain:|n Combat\n"
            "|cResource:|n Momentum -- builds from hits landed and damage taken\n"
            "|cHub Cities:|n Caldenmere, Tremen\n\n"
            "The Ironblood guild trains warriors in the art of sustained "
            "aggression. Momentum builds as you fight and decays when you "
            "stop. An Ironblood member who stays in the fight always has "
            "resources.\n\n"
            "|cSubclasses:|n Duskblade, Thornguard, Ruinborn, Spellbreaker, "
            "Ironvoice, Bloodwright, Warlord, Ironwright, Ashwalker"
        ),
    },
    {
        "key": "veilcraft",
        "aliases": ["guild of veilcraft"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Veilcraft|n\n"
            "|x\"What is seen is already lost.\"|n\n\n"
            "|cPrimary Domain:|n Subterfuge\n"
            "|cResource:|n Focus -- built through timing and pattern reading\n"
            "|cHub Cities:|n Vael's Crossing\n\n"
            "The Veilcraft guild teaches the art of reading enemies -- "
            "finding guard windows that open and close on a timer. "
            "Abilities used within the window chain; abilities used "
            "outside break the combo.\n\n"
            "|cSubclasses:|n Shadowranger, Mistweaver, Echowalker, "
            "Spellthief, Silvertongue, Venomhand, Phantomblade, "
            "Gearshade, Gravewhisper"
        ),
    },
    {
        "key": "verdance",
        "aliases": ["guild of verdance"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Verdance|n\n"
            "|x\"The forest was here before the Empire. It will be here after.\"|n\n\n"
            "|cPrimary Domain:|n Naturalism\n"
            "|cResource:|n Balance -- a spectrum between Feral and Calm\n"
            "|cHub Cities:|n Vael's Crossing, Korahei\n\n"
            "The Verdance guild teaches mastery of natural duality. "
            "Aggressive abilities push toward Feral, defensive toward "
            "Calm. Both extremes weaken you. The skilled naturalist "
            "manages their balance carefully.\n\n"
            "|cSubclasses:|n Bladestorm, Thornshade, Resonant Warden, "
            "Sporeweaver, Wildvoice, Venombark, Beastwarden, "
            "Rootwright, Ashbloom"
        ),
    },
    {
        "key": "resonance guild",
        "aliases": ["guild of resonance"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Resonance|n\n"
            "|x\"The patterns were here before us. We are learning to read.\"|n\n\n"
            "|cPrimary Domain:|n Resonance\n"
            "|cResource:|n Resonance -- builds toward threshold, decays in combat\n"
            "|cHub Cities:|n Tremen, Vael's Crossing\n\n"
            "The Resonance guild teaches sensitivity to the ambient magical "
            "energy left by the dragon civilization. Resonance builds toward "
            "a threshold and spends at 60+ for meaningful effect. Resonance "
            "members perceive the world differently.\n\n"
            "|cSubclasses:|n Ruinborn, Echowalker, Resonant Warden, "
            "Resonant Sage, Harmonist, Resonant Smith, Warshaper, "
            "Resonwright, Nodewalker"
        ),
    },
    {
        "key": "arcane",
        "aliases": ["guild of the arcane", "guild of arcane"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of the Arcane|n\n"
            "|x\"The spell is the question. The effect is the answer.\"|n\n\n"
            "|cPrimary Domain:|n Arcana\n"
            "|cResource:|n Mana -- regenerates at rest, not during combat\n"
            "|cHub Cities:|n Caldenmere, Varath Prime, Vael's Crossing, Tremen\n\n"
            "The Arcane guild teaches cross-encounter resource management. "
            "Mana regenerates between fights, not during them. The space "
            "between fights is as strategically interesting as the fight itself.\n\n"
            "|cSubclasses:|n Spellbreaker, Spellthief, Sporeweaver, "
            "Resonant Sage, Accordant Mage, Elixirmage, Battlemage, "
            "Runewright, Voidscribe"
        ),
    },
    {
        "key": "accord",
        "aliases": ["guild of accord"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Accord|n\n"
            "|x\"Every door opens from the inside. We know who's standing there.\"|n\n\n"
            "|cPrimary Domain:|n Diplomacy\n"
            "|cResource:|n Influence -- built from faction relationships\n"
            "|cHub Cities:|n Caldenmere, Varath Prime, Korahei\n\n"
            "The Accord guild converts relationships into power. A Diplomacy "
            "member who actively engages the world's political landscape "
            "arrives at combat with more resources than one who ignores it.\n\n"
            "|cSubclasses:|n Ironvoice, Silvertongue, Wildvoice, Harmonist, "
            "Accordant Mage, Apothecary, Bannerlord, Forgepact, Lorewarden"
        ),
    },
    {
        "key": "thornwork",
        "aliases": ["guild of thornwork"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Thornwork|n\n"
            "|x\"Everything that heals can also harm. We chose a side.\"|n\n\n"
            "|cPrimary Domain:|n Alchemy\n"
            "|cResource:|n Reagents -- crafted before combat from gathered materials\n"
            "|cHub Cities:|n Vael's Crossing\n\n"
            "The Thornwork guild embodies preparation as combat philosophy. "
            "Reagents are crafted before the fight. Running out mid-fight is "
            "a genuine failure state -- insufficient planning, not bad luck.\n\n"
            "|cSubclasses:|n Bloodwright, Venomhand, Venombark, Resonant Smith, "
            "Elixirmage, Apothecary, Siegewright, Alchemist, Hollowbrewer"
        ),
    },
    {
        "key": "warcraft",
        "aliases": ["guild of warcraft"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Warcraft|n\n"
            "|x\"The battle is won before the first blow. Everything after is ceremony.\"|n\n\n"
            "|cPrimary Domain:|n Tactics\n"
            "|cResource:|n Command -- builds when allies act, half rate solo\n"
            "|cHub Cities:|n Caldenmere, Varath Prime, Fort Rennick\n\n"
            "The Warcraft guild teaches group synergy as personal power. "
            "Command builds when allies act. Solo, it builds at half rate. "
            "A Tactics member in a group is mechanically a different class "
            "than one playing solo.\n\n"
            "|cSubclasses:|n Warlord, Phantomblade, Beastwarden, Warshaper, "
            "Battlemage, Bannerlord, Siegewright, Warchief, Dreadmarshal"
        ),
    },
    {
        "key": "forge",
        "aliases": ["guild of forge"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Forge|n\n"
            "|x\"We don't ask the old magic for permission. We figure it out ourselves.\"|n\n\n"
            "|cPrimary Domain:|n Engineering\n"
            "|cResource:|n Components -- fuel for mechanical companions\n"
            "|cHub Cities:|n Caldenmere\n\n"
            "The Forge guild teaches mechanical companion construction as "
            "combat identity. The companion fights alongside you, fueled "
            "by Components. Standard for baseline, Enhanced Fuel for "
            "amplified, Overcharge for risk/reward ceiling.\n\n"
            "|cSubclasses:|n Ironwright, Gearshade, Rootwright, Resonwright, "
            "Runewright, Forgepact, Alchemist, Warchief, Relicwright"
        ),
    },
    {
        "key": "vaelborn",
        "aliases": ["guild of vaelborn"],
        "category": "Guilds",
        "locks": "read:all()",
        "text": (
            "|wGuild of Vaelborn|n\n"
            "|x\"The world forgot what it was named after. We remember.\"|n\n\n"
            "|cPrimary Domain:|n Remnance\n"
            "|cResource:|n Echoes -- accumulated knowledge as combat power\n"
            "|cHub Cities:|n Hidden -- must be discovered\n\n"
            "The Vaelborn are a hidden guild devoted to excavating the "
            "secrets of the dragon civilization. Lore fragment decoding "
            "grants starting Echoes for subsequent encounters. The only "
            "domain where intellectual curiosity is directly expressed "
            "as combat power.\n\n"
            "|cSubclasses:|n Ashwalker, Gravewhisper, Ashbloom, Nodewalker, "
            "Voidscribe, Lorewarden, Hollowbrewer, Dreadmarshal, Relicwright"
        ),
    },
    # =========================================================================
    # SKILLS (8 entries for major skill categories)
    # =========================================================================
    {
        "key": "investigation",
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wInvestigation|n\n\n"
            "Your ability to find hidden things and piece together clues. "
            "Higher investigation improves search results, reveals more "
            "details when examining objects, and unlocks special dialogue "
            "options with NPCs.\n\n"
            "Improved through: searching rooms, examining objects, "
            "solving puzzles."
        ),
    },
    {
        "key": "lockpicking",
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wLockpicking|n\n\n"
            "The art of opening locked doors and containers without a key. "
            "Higher skill improves success chance on difficult locks and "
            "reduces the risk of breaking your tools.\n\n"
            "Improved through: picking locks, practicing on training locks."
        ),
    },
    {
        "key": "cooking skill",
        "aliases": ["cooking"],
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wCooking|n\n\n"
            "Preparing food and provisions from gathered ingredients. "
            "Higher cooking skill unlocks better recipes and improves "
            "the quality of food produced. Quality food provides stronger "
            "and longer-lasting buffs.\n\n"
            "Improved through: cooking recipes, practicing at kitchen stations."
        ),
    },
    {
        "key": "smithing skill",
        "aliases": ["smithing"],
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wSmithing|n\n\n"
            "Forging weapons and armor from raw materials. Higher smithing "
            "skill unlocks advanced recipes, improves output quality, and "
            "allows working with higher-tier materials.\n\n"
            "Improved through: forging items, training with master smiths."
        ),
    },
    {
        "key": "alchemy skill",
        "aliases": ["alchemy"],
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wAlchemy|n\n\n"
            "Brewing potions, reagents, and compounds from gathered herbs "
            "and minerals. Higher skill produces more potent results and "
            "unlocks complex multi-ingredient recipes.\n\n"
            "Improved through: brewing potions, experimenting at alchemy benches."
        ),
    },
    {
        "key": "herbalism",
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wHerbalism|n\n\n"
            "The knowledge of plants and where they grow. Higher herbalism "
            "improves the yield and quality of gathered herbs and reveals "
            "rare gathering nodes in the world.\n\n"
            "Improved through: gathering herbs, identifying plants."
        ),
    },
    {
        "key": "mining",
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wMining|n\n\n"
            "Extracting ore and minerals from deposits. Higher mining skill "
            "improves yield, reveals richer veins, and allows extraction "
            "from more difficult deposits.\n\n"
            "Improved through: mining ore, prospecting deposits."
        ),
    },
    {
        "key": "survival",
        "category": "Skills",
        "locks": "read:all()",
        "text": (
            "|wSurvival|n\n\n"
            "General wilderness competence. Higher survival improves your "
            "ability to track creatures, find safe rest spots, resist "
            "environmental hazards, and navigate unfamiliar terrain.\n\n"
            "Improved through: exploring wilderness zones, camping, tracking."
        ),
    },
    # =========================================================================
    # WORLD LORE (6 entries)
    # =========================================================================
    {
        "key": "dragon curse",
        "aliases": ["the dragon curse", "curse"],
        "category": "World Lore",
        "locks": "read:all()",
        "text": (
            "|wThe Dragon Curse|n\n\n"
            "One thousand years ago, a catastrophic magical event reduced "
            "the dragons of Soravelon from sentient architects to feral "
            "beasts. The infrastructure they built -- nodes of power, "
            "great cities, transit networks -- still functions but decays "
            "without maintenance.\n\n"
            "The mortal civilizations that inherited this infrastructure "
            "understand only fragments of how it works. As nodes fail "
            "and collapse, the world grows more dangerous."
        ),
    },
    {
        "key": "nodes",
        "aliases": ["magical nodes", "node system"],
        "category": "World Lore",
        "locks": "read:all()",
        "text": (
            "|wMagical Nodes|n\n\n"
            "Nodes are ancient dragon-built magical infrastructure scattered "
            "throughout the world. Each node sustains an area of influence, "
            "maintaining environmental stability and powering old magic.\n\n"
            "Nodes degrade through a state machine:\n"
            "  |gHealthy|n -> |yStressed|n -> |rFailing|n -> |xCollapsed|n\n\n"
            "As nodes degrade, the environment changes. Rooms shift from "
            "their normal (Layer 0) state to degraded (Layer 1) versions. "
            "Collapsed nodes spawn dangerous anomalies.\n\n"
            "Players with resonance attunement can |wstabilize|n stressed "
            "or failing nodes to reverse the decay."
        ),
    },
    {
        "key": "dragon courier",
        "aliases": ["dragon courier service", "courier service", "flight system"],
        "category": "World Lore",
        "locks": "read:all()",
        "text": (
            "|wDragon Courier Service|n\n\n"
            "One of the few dragon-era systems still fully operational. "
            "Domesticated courier dragons (not affected by the Curse in "
            "the same way) carry passengers between hub cities and "
            "waystations.\n\n"
            "Use |wfly <destination>|n at a courier station to travel. "
            "Fares are discounted based on your standing with the local "
            "faction. Type |wroutes|n to see available destinations."
        ),
    },
    {
        "key": "empire",
        "aliases": ["the empire"],
        "category": "World Lore",
        "locks": "read:all()",
        "text": (
            "|wThe Empire|n\n\n"
            "The dominant political power in Soravelon, ruling from the "
            "great city of Varath Prime. The Empire inherited the largest "
            "share of dragon infrastructure and guards it jealously. "
            "Humans form the majority of its citizens, though all "
            "ancestries live within its borders.\n\n"
            "The Empire's relationship with the Kau'roran is strained, "
            "and Selvar face open discrimination in Imperial territories."
        ),
    },
    {
        "key": "consortium",
        "aliases": ["the consortium"],
        "category": "World Lore",
        "locks": "read:all()",
        "text": (
            "|wThe Consortium|n\n\n"
            "A powerful trade network that operates across political "
            "boundaries. The Consortium controls banking, issues Drafts, "
            "and facilitates commerce between cities. They are pragmatic "
            "and profit-driven, maintaining neutrality in most conflicts.\n\n"
            "The Veth have historical ties to the Consortium through "
            "their underground trade routes."
        ),
    },
    {
        "key": "wardens",
        "aliases": ["the wardens"],
        "category": "World Lore",
        "locks": "read:all()",
        "text": (
            "|wThe Wardens|n\n\n"
            "An order dedicated to maintaining the world's failing magical "
            "infrastructure. The Wardens study node mechanics, stabilize "
            "degrading nodes, and protect communities from the effects "
            "of node collapse. The Kau'roran have a long tradition of "
            "service among the Wardens."
        ),
    },
    # =========================================================================
    # MISCELLANEOUS (4 entries)
    # =========================================================================
    {
        "key": "encumbrance",
        "aliases": ["weight", "carrying capacity"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wEncumbrance|n\n\n"
            "Your carrying capacity is based on your attributes. As you "
            "carry more weight, you become encumbered:\n\n"
            "  |gLight|n -- No penalties\n"
            "  |yModerate|n -- Reduced movement speed\n"
            "  |rHeavy|n -- Reduced speed and combat effectiveness\n"
            "  |xOverloaded|n -- Cannot move\n\n"
            "Containers with weight reduction can help manage your load. "
            "Deposit excess items at a bank vault or drop them."
        ),
    },
    {
        "key": "death",
        "aliases": ["dying", "defeat"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wDeath & Defeat|n\n\n"
            "When your health reaches zero, you are defeated. You lose "
            "carried Scales (banked Scales are safe) and respawn at the "
            "nearest safe waypoint. Your equipment is not lost.\n\n"
            "Defeat is a setback, not an ending. Prepare better, choose "
            "fights wisely, and bank your wealth regularly."
        ),
    },
    {
        "key": "attunement",
        "aliases": ["zone attunement"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wZone Attunement|n\n\n"
            "As you spend time in a zone, your attunement to it grows "
            "(0-100). Higher attunement provides benefits:\n\n"
            "  Increased loot quality from zone creatures\n"
            "  Better resource node yields\n"
            "  Enhanced ability effectiveness in the zone\n"
            "  Deeper sense readings of the environment\n\n"
            "Attunement grows through exploration, combat, and "
            "interacting with the zone's node system."
        ),
    },
    {
        "key": "scaling",
        "aliases": ["zone scaling", "level scaling"],
        "category": "Systems",
        "locks": "read:all()",
        "text": (
            "|wZone Scaling|n\n\n"
            "Soravelon uses per-player logarithmic scaling. Every zone "
            "is playable at any stage of your journey -- there are no "
            "level-locked areas or content gates based on progression.\n\n"
            "Creatures scale to present a meaningful challenge regardless "
            "of your domain scores. What changes with progression is "
            "your toolkit -- more abilities, better equipment, deeper "
            "understanding of combat mechanics."
        ),
    },
]
