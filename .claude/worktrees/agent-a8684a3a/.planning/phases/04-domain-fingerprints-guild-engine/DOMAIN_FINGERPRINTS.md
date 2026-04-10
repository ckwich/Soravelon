# Domain Fingerprints: Consolidated Design Document

> Consolidated from vault sources by Claude. Creative content authored by user.
> Do not modify fingerprint verbs, subclass names, or guild lore.
>
> Sources: soravelon-fingerprints.md, soravelon-guilds.md, soravelon-abilities.md
> Consolidated: 2026-03-25

---

## The Ten Fingerprints

Each domain has one mechanical verb that no other domain shares. The resource system
expresses that verb. The abilities reinforce it. When two domains combine into a
subclass, both fingerprints are present -- the primary guild's fingerprint dominates.

---

### Combat -- PRESS
**Guild:** Guild of Ironblood
**Resource:** Momentum (builds from hits landed and damage taken; decays between encounters and on idle rounds)

Sustained aggression. A Combat player who stays in the fight always has resources.
Running away or hesitating bleeds Momentum. The worst thing you can do is nothing.

---

### Subterfuge -- READ
**Guild:** Guild of Veilcraft
**Resource:** Focus (window-based combo timing, not a pool)

Timing and pattern recognition. Every enemy has a defensive rhythm -- guard windows
that open and close on a timer. Abilities used within the window chain, each amplifying
the next. Abilities used outside break the combo entirely. Patience is mechanically
rewarded; aggression without timing is punished.

---

### Naturalism -- CALIBRATE
**Guild:** Guild of Verdance
**Resource:** Balance (spectrum, not a pool)

Managed duality. The Balance spectrum sits at neutral by default. Aggressive abilities
push toward Feral; defensive/healing push toward Calm. Both extremes weaken you in
different ways. The question is never "do I have enough" but "which kind of power
do I need now, and what am I trading to get there."

---

### Resonance -- ATTUNE
**Guild:** Guild of Resonance
**Resource:** Resonance (builder/spender with in-combat decay)

Environmental sensitivity. Resonance builds toward a threshold, decays during combat,
and spends at 60+ for meaningful effect. Resonance players perceive the world differently
-- they detect node activity before anyone else. In node-active zones, their abilities
interact with the environment in ways other domains cannot access.

---

### Arcana -- RATION
**Guild:** Guild of the Arcane
**Resource:** Mana (regenerates between encounters, not during)

Cross-encounter resource management. A fully-rested Arcana player is the most powerful
spellcaster in the game. A depleted one is a liability. This is the only domain where
the space between fights is as strategically interesting as the fight itself.

---

### Diplomacy -- LEVERAGE
**Guild:** Guild of Accord
**Resource:** Influence (builds from social engagement, decays between encounters)

Converting relationships into power. A Diplomacy player who actively engages the world's
political landscape arrives at combat with more resources than one who ignores it. The
game world outside combat directly improves performance inside it.

---

### Alchemy -- PREPARE
**Guild:** Guild of Thornwork
**Resource:** Reagents (pre-crafted consumable stock)

Preparation as combat philosophy. Reagents are crafted before the fight from materials
gathered in the world. Running out mid-fight is a genuine failure state -- not bad luck,
but insufficient planning. The most powerful combinations require advance knowledge of
what you're fighting.

---

### Tactics -- ORCHESTRATE
**Guild:** Guild of Warcraft
**Resource:** Command (builds from ally actions in combat)

Group synergy expressed as personal power. Command builds when allies act -- each ally
action generates Command. Solo, it builds at half rate. This is the only domain where
other players generate your resource for you. A Tactics player in a group is a
mechanically different class than one playing solo.

---

### Engineering -- CONSTRUCT
**Guild:** Guild of Forge
**Resource:** Components (pre-crafted consumable stock)
**Companion:** Mechanical construct, customized per subclass

The Engineering fingerprint is about what you built fighting alongside you. The mechanical
companion is the Engineering identity. Standard Components provide baseline companion
operation; Enhanced Fuel (Alchemist-crafted) amplifies; Overcharge pushes beyond design
limits with risk of shutdown.

---

### Remnance -- EXCAVATE
**Guild:** Guild of Vaelborn
**Resource:** Echoes (builds in combat + investigation bonus)

Accumulated knowledge as combat power. Decoding lore fragments grants +15 starting Echoes
for the next 3 encounters; investigating ancient sites grants +10; stacks to max 40. This
is the only domain where intellectual curiosity about the world's history is directly
expressed as combat capability.

---

## Guild Registry

| guild_id | Name | Primary Domain | Hub Cities | Hidden | Resource |
|----------|------|----------------|------------|--------|----------|
| ironblood | Guild of Ironblood | combat | caldenmere, tremen | No | momentum |
| veilcraft | Guild of Veilcraft | subterfuge | vaels_crossing | No | focus |
| verdance | Guild of Verdance | naturalism | vaels_crossing, korahei | No | balance |
| resonance | Guild of Resonance | resonance | tremen, vaels_crossing | No | resonance |
| arcane | Guild of the Arcane | arcana | caldenmere, varath_prime, vaels_crossing, tremen | No | mana |
| accord | Guild of Accord | diplomacy | caldenmere, varath_prime, korahei | No | influence |
| thornwork | Guild of Thornwork | alchemy | vaels_crossing | No | reagents |
| warcraft | Guild of Warcraft | tactics | caldenmere, varath_prime, fort_rennick | No | command |
| forge | Guild of Forge | engineering | caldenmere | No | components |
| vaelborn | Guild of Vaelborn | remnance | (none) | Yes | echoes |

**Guild Mottos:**
- **Ironblood:** "Strength is not a gift. It is a debt you pay every day."
- **Veilcraft:** "What is seen is already lost."
- **Verdance:** "The forest was here before the Empire. It will be here after."
- **Resonance:** "The patterns were here before us. We are learning to read."
- **Arcane:** "The spell is the question. The effect is the answer."
- **Accord:** "Every door opens from the inside. We know who's standing there."
- **Thornwork:** "Everything that heals can also harm. We chose a side."
- **Warcraft:** "The battle is won before the first blow. Everything after is ceremony."
- **Forge:** "We don't ask the old magic for permission. We figure it out ourselves."
- **Vaelborn:** "The world forgot what it was named after. We remember."

**Notes:**
- Guild of the Arcane has two traditions (Imperial in Caldenmere/Varath Prime, Western in Vael's Crossing/Tremen). Mechanically identical, culturally distinct.
- Vaelborn is hidden -- not present in any city. Found through gameplay investigation.

---

## Subclass Matrix

90 total subclasses: 10 guilds x 9 secondary domains. Primary domain is always the guild's
domain. Secondary domain is the complement. Same domain pair in reverse order = different
guild, different emphasis, different identity.

### Guild of Ironblood (Combat Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Subterfuge | duskblade | Duskblade | A fighter who disappears between strikes -- combat invisibility not infiltration | Momentum spends on mid-combat Vanish; burst damage on stealth re-entry |
| Naturalism | thornguard | Thornguard | A warrior whose body is reinforced by living magic | Nature buffs applied to self; animal companion assists rather than bonds |
| Resonance | ruinborn | Ruinborn | Channels old magic through physical strikes -- hits that leave node-echoes | Attacks apply Resonance stacks; threshold triggers node burst on target |
| Arcana | spellbreaker | Spellbreaker | Hunts mages -- uses magical vulnerability as a weapon | Anti-magic combat abilities; disrupts enemy Mana on hit |
| Diplomacy | ironvoice | Ironvoice | A warrior whose reputation precedes them -- enemies hesitate, allies rally | Presence-scaled intimidation debuffs; Reputation gains faster in combat |
| Alchemy | ashfang | Ashfang | Coats everything in blood and poison -- raw violence as delivery mechanism | Melee attacks apply Bleed and Poison simultaneously |
| Tactics | vanguard | Vanguard | The front of every formation -- absorbs damage, breaks lines | Guard mechanics; generates group action budget bonuses through space control |
| Engineering | ironwright | Ironwright | A fighter whose companion is built for close-range combat support | Combat-hardened companion chassis -- shields, weapon assists, disruption; Momentum and companion act in concert |
| Remnance | dragonblooded | Dragonblooded | A fighter touched by something ancient -- physical abilities that shouldn't exist | Ancient physical enhancements; resistances that scale off Resonance stat |

### Guild of Veilcraft (Subterfuge Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | grimwarden | Grimwarden | A brutal assassin -- no finesse, overwhelming force from unexpected angles | Focus builds fastest from ambush hits; stealth re-entry resets cooldowns |
| Naturalism | hollowstep | Hollowstep | A wilderness ghost -- tracks, vanishes, uses terrain as a weapon | Outdoor stealth bonuses; terrain-based trap-setting; creature attunement enhances evasion |
| Resonance | veilreader | Veilreader | Reads magical signatures of people and places -- sees what's coming | Node attunement gives combat advantage; reads enemy ability telegraphs one round ahead |
| Arcana | nullshadow | Nullshadow | Wraps magical effects in shadow -- spells that arrive unseen | Magical abilities usable from stealth without breaking Vanish |
| Diplomacy | tally_agent | Tally Agent | Information warfare, double agents, network exploitation | Network dimension grows fastest; faction Standing manipulation; social intel as combat leverage |
| Alchemy | blackthorn | Blackthorn | The classic poisoner -- patient, precise, never seen | Poison applied during Vanish; highest single-target poison ceiling in the game |
| Tactics | shadecommand | Shadecommand | Special operations -- tactical infiltration, disruption behind lines | Group stealth abilities; disables enemy tactical advantages; scouts ahead for group |
| Engineering | lockjaw | Lockjaw | Built every tool they're using -- no improvisation, pure preparation | Trap-setting master; mechanical devices usable mid-combat |
| Remnance | hollowseen | Hollowseen | Sees what others cannot -- reads ancient patterns in movement | Awareness abilities that shouldn't be possible; lore fragment discovery rate enhanced |

### Guild of Verdance (Naturalism Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | thornfist | Thornfist | A nature practitioner who fights with their body | Shapeshift-adjacent abilities; physical strikes apply nature DoTs |
| Subterfuge | rootstalker | Rootstalker | Moves through wilderness like the wilderness itself | Outdoor Vanish with no cooldown; ambush bonuses from natural cover |
| Resonance | cantera | Cantera | Named for the forest -- nature through old magic specifically | Node attunement accelerates in nature zones; unique Cognitive node interaction |
| Arcana | stormcaller | Stormcaller | Calls elemental forces -- rain, lightning, wind | Area magical effects; Wet application; weather abilities enhanced in node zones |
| Diplomacy | greentongue | Greentongue | Speaks for the natural world in political spaces | Faction Standing with Druids and Wardens grows faster; animal-based social leverage |
| Alchemy | rotweald | Rotweald | The dark side of nature -- decay, rot, toxic growth | Bleed and Poison through nature abilities; area DoT effects |
| Tactics | wildcommand | Wildcommand | Commands animals as a tactical force -- the forest is their army | Beast companion combat scripting; animal-based group abilities; zone control through terrain |
| Engineering | growthwright | Growthwright | Grows things rather than builds them -- living structures, organic construction | Harvesting bonuses; cultivated material creation; living trap-setting |
| Remnance | deeproot | Deeproot | Touches something beneath nature -- the world-memory in old growth | Ancient forest lore unlocks; unique in Cantera Forest; dragon-adjacent nature abilities |

### Guild of Resonance (Resonance Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | runebreaker | Runebreaker | Channels old magic into physical destruction -- hits that leave reality slightly wrong | Resonance stacks on enemies through physical strikes; node burst damage |
| Subterfuge | greymantle | Greymantle | Moves through the world's magical blind spots | Node proximity grants stealth bonuses; undetectable to magical detection |
| Naturalism | thornweald | Thornweald | The nature-magic practitioner -- DoT focus, terrain manipulation | Nature and old magic combined; terrain manipulation abilities |
| Arcana | sealwright | Sealwright | Combines ancient patterns with raw magical force | Node-powered magical abilities; highest burst damage of any Resonance subclass |
| Diplomacy | lorekeeper | Lorekeeper | The Scholar made dangerous -- ancient knowledge as political leverage | Lore fragments grant faction Standing bonuses; highest Resonance skill ceiling |
| Alchemy | corroder | Corroder | Applies old magic to chemical effects -- poisons that interact with node energy | Node-enhanced poison effects; compound effects amplified near active nodes |
| Tactics | nodecaller | Nodecaller | Uses node events as tactical weapons -- forces node activation deliberately | Can trigger node events; zone control through magical environmental manipulation |
| Engineering | arcanist | Arcanist | Understands how old infrastructure was built -- studies and applies fragments | Golem interaction; base-8 decoding; Scholar Arcanist abilities now Resonance-rooted |
| Remnance | sealreader | Sealreader | Has gotten uncomfortably close to the truth | Closest to the dragon secret; Circle of Wizards actively suppresses this subclass |

### Guild of the Arcane (Arcana Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | battlemage | Battlemage | A mage who hits things when spells run out -- and doesn't mind | Mana-fueled physical strikes; melee abilities scale off both Strength and Mana |
| Subterfuge | mistveil | Mistveil | Disappears behind magical concealment -- not stealth, something else | Magical invisibility distinct from physical stealth; unique detection bypass |
| Naturalism | stormweaver | Stormweaver | Weaves elemental forces through nature -- lightning through trees, frost through roots | Nature and arcane combined; area magical effects enhanced in natural zones |
| Resonance | spellseeker | Spellseeker | A mage who studies old magic to make new magic better | Node study improves Mana pool and spellcasting effectiveness |
| Diplomacy | enchantvoice | Enchantvoice | A mage whose words carry literal weight | Magical persuasion abilities; social-magical hybrids; Charm spell variants |
| Alchemy | fusewright | Fusewright | Weaponizes alchemical and magical combinations | Potion-powered spell amplification; compound effects trigger through magical delivery |
| Tactics | wardcaller | Wardcaller | Directs magical force tactically -- placement and timing over power | Magical area control; ability to define battlefield zones with lasting effects |
| Engineering | runewright | Runewright | Encodes magic into constructed objects | Enchanted device creation; magical trap-setting; golem empowerment |
| Remnance | voidscribe | Voidscribe | Studies the space between what magic is and what it was | Ancient spellforms inaccessible to other Arcana subclasses; Circle of Wizards conflict |

### Guild of Accord (Diplomacy Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | civicguard | Civicguard | The diplomat with teeth -- persuasion backed by demonstrated violence | Intimidation abilities scale with combat record; Presence+Strength hybrid scaling |
| Subterfuge | shadowbroker | Shadowbroker | Runs information networks from the shadows -- nobody knows who they work for | Network dimension grows fastest; double faction Standing gains |
| Naturalism | wayfinder | Wayfinder | Opens doors through empathy -- understands what every living thing needs | Bond dimension bonuses; animal and NPC warmth at unprecedented rates |
| Resonance | spiritvoice | Spiritvoice | Uses old magic to amplify social power -- words that carry more weight than they should | Presence abilities scale off Resonance; ability dialogue options unlocked |
| Arcana | highcourt | Highcourt | A mage who never had to fight -- because nobody wanted them to stop talking | Social-magical abilities; magical aura affects NPC disposition passively |
| Alchemy | silkpoison | Silkpoison | The subtle threat -- social manipulation backed by the ability to harm without evidence | Poison applied through social encounters; the most dangerous dinner guest |
| Tactics | bannerspeaker | Bannerspeaker | Turns armies with words -- the voice behind every military campaign | Morale mechanics at scale; faction Standing with military factions grows fastest |
| Engineering | dealwright | Dealwright | Makes things that create obligations -- every gift is an investment | Crafted items carry Standing bonuses when gifted; merchant mechanics |
| Remnance | truthwarden | Truthwarden | Knows too much about the world's actual history -- uses it carefully | Hidden faction access; the Resistance questline starts most naturally here |

### Guild of Thornwork (Alchemy Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | venomfang | Venomfang | Applies poison through sustained physical aggression | Highest melee poison application rate; Bleed+Poison simultaneously |
| Subterfuge | nightshade | Nightshade | Poisons from concealment -- never seen, only felt later | Vanish-applied poison; delayed onset toxins; highest single-target ceiling |
| Naturalism | mireweald | Mireweald | The Thornwork-primary version -- decay and organic toxins over living nature | Decay-focused nature abilities; terrain poisoning; rot effects |
| Resonance | voidbrewer | Voidbrewer | Creates alchemical compounds that interact with old magic | Node-enhanced consumables; alchemical effects amplified in node zones |
| Arcana | fumecaster | Fumecaster | Delivers alchemical compounds through magical vectors | Spell-delivered poisons and compounds; range on normally melee-only effects |
| Diplomacy | sweetpoison | Sweetpoison | The charming poisoner -- social access is just a delivery method | Poison through social interaction; Influence builds through successful poisonings |
| Tactics | plaguecommand | Plaguecommand | Tactical toxicology -- poisons as area-denial weapons | Area poison effects; terrain poisoning for zone control; tactical resource denial |
| Engineering | fumewright | Fumewright | Builds delivery mechanisms -- gas traps, poison containers, alchemical devices | Mechanical poison delivery; trap-setting with chemical payloads |
| Remnance | firstblight | Firstblight | Something old in the poison -- toxins that interact with dragon magic | Ancient poison effects; dragon-adjacent toxicology; unique Vaelborn questline interaction |

### Guild of Warcraft (Tactics Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | warbringer | Warbringer | The frontline commander who leads by example -- first in, last out | Guard mechanics plus command abilities; action budget bonuses for nearby allies |
| Subterfuge | greycommand | Greycommand | Special operations commander -- controls information as a tactical weapon | Scouting abilities; group stealth; intel-based combat advantage |
| Naturalism | wildtactician | Wildtactician | Commands natural elements as battlefield terrain | Zone control through nature; beast-based tactical abilities |
| Resonance | nodewarden | Nodewarden | Uses node events as tactical terrain -- activates, destabilizes, weaponizes | Node manipulation in combat; Scholar tactical awareness |
| Arcana | siegecaller | Siegecaller | Calls magical artillery -- places effects where they need to be, not where he is | Long-range area placement; magical battlefield geometry |
| Diplomacy | warlord | Warlord | Commands through force of personality -- morale IS the battlefield | Presence-scaled command abilities; faction Standing from combat victories |
| Alchemy | siegemaster | Siegemaster | Tactical poison and chemical warfare -- area denial and attrition | Area DoT tactics; siege mechanics for zone-level content |
| Engineering | fieldwright | Fieldwright | Builds battlefield advantages -- fortifications, devices, mechanical traps | Combat construction; field modification abilities |
| Remnance | oathbreaker | Oathbreaker | Knows how ancient wars were actually fought -- tactics nobody else knows | Ancient tactical knowledge; abilities referencing pre-curse battle doctrine |

### Guild of Forge (Engineering Primary)

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | ironsmith | Ironsmith | Builds better weapons and wears better armor -- and uses both | Crafted gear has enhanced stats when self-made; combat bonuses from own crafted equipment |
| Subterfuge | gearhand | Gearhand | A Forge-primary who learned infiltration through mechanical locks | Trap-setting master with infiltration applications; mechanical lock mastery |
| Naturalism | growsmith | Growsmith | Cultivates living materials and builds with them | Living material crafting; unique organic harvesting mechanics; bridge between grown and constructed |
| Resonance | runewright_forge | Runewright | Studies old infrastructure to understand how it works | Ancient construction knowledge; golem repair and interaction; base-8 pattern application |
| Arcana | sparkshaper | Sparkshaper | Understands that magic and machinery are the same thing approached differently | Magical device crafting; enchanted component creation |
| Diplomacy | dealsmith | Dealsmith | Makes things people want -- economic power through craft | Merchant mechanics; crafted item Standing bonuses; Consortium faction integration |
| Tactics | siegewright | Siegewright | Builds what armies need -- siege equipment, fortifications, field infrastructure | Large-scale construction; group-benefiting devices; siege mechanics |
| Alchemy | fumehand | Fumehand | Chemical engineering meets mechanical construction | Alchemical device crafting; gas delivery systems |
| Remnance | bucketborn | Bucketborn | Named for Bucket -- accidentally rediscovered old magic through mechanical study | Unique golem interaction; ancient infrastructure instinct; the subclass Gidget never meant to create |

### Guild of Vaelborn (Remnance Primary) -- HIDDEN

| Secondary | Subclass ID | Name | Fantasy | Hook |
|-----------|-------------|------|---------|------|
| Combat | dragonkin | Dragonkin | A fighter whose body has been changed by proximity to old power | Ancient physical enhancements; Dragon Rookery interactions unique |
| Subterfuge | truthshadow | Truthshadow | Knows things they shouldn't and hides that they know them | Deepest information access; unique faction Standing interactions |
| Naturalism | worldroot | Worldroot | Connected to the world's actual foundation -- the living magic beneath nature | Unique Cantera Forest interactions; dragon lore through nature |
| Resonance | sealbreaker | Sealbreaker | The most dangerous subclass in the game -- actively working to break the dragon curse | Dragon curse questline primary; Circle of Wizards' primary target |
| Arcana | firstform | Firstform | Casts using spell-forms predating current magical schools | Dragon-origin spellforms; unique effects unavailable to any other subclass |
| Diplomacy | ancientvoice | Ancientvoice | Speaks with the authority of the world's true history | Political leverage from forbidden knowledge; unique faction access |
| Alchemy | rootpoison | Rootpoison | Dragon-origin alchemy, not learned alchemy | Toxins derived from pre-curse knowledge; unique compound effects |
| Tactics | firstblade | Firstblade | Fights using pre-curse combat doctrine -- tactics nobody else has seen | Ancient tactical abilities; unique combat mechanics |
| Engineering | dragonwright | Dragonwright | Builds using fragments of dragon-made construction knowledge | Unique golem construction; ancient infrastructure understanding |

---

## Duplicate Name Resolutions

| Domain Pair | Guild A | Name A | Guild B | Name B |
|-------------|---------|--------|---------|--------|
| Arcana+Resonance | Arcane | Spellseeker | Resonance | Sealwright |
| Arcana+Remnance | Arcane | Voidscribe | Vaelborn | Firstform |
| Alchemy+Remnance | Thornwork | Firstblight | Vaelborn | Rootpoison |
| Naturalism+Alchemy | Verdance | Rotweald | Thornwork | Mireweald |
| Subterfuge+Engineering | Veilcraft | Lockjaw | Forge | Gearhand |

---

## Guild Tier Labels

Players see descriptor labels at each Guild Tier Score threshold, not numeric scores.
Each guild has its own vocabulary.

```
Threshold:    0-20        20-50         50-85         85+

Ironblood:    Scrapper    Ironblood     Warblade      Bloodsworn
Veilcraft:    Shadow      Veilwalker    Phantom       The Unseen
Verdance:     Wanderer    Rootbound     Verdant       Ancient Voice
Resonance:    Listener    Attuned       Resonant      Harmonic
Arcane:       Initiate    Arcanist      Adept         Loremaster
Accord:       Envoy       Accord        Arbiter       Voice of the Realm
Thornwork:    Brewer      Thornworker   Compound      Transmuter
Warcraft:     Conscript   Tactician     Commander     Warchief
Forge:        Tinkerer    Forgehand     Artificer     Architect
Vaelborn:     (empty)     Echoing       Vaelborn      The Unbroken
```

Vaelborn tier 1 is empty string -- guild is not visible until discovered. When the
guild surfaces, the label appears retroactively.

---

## GTS Formula and Tier Thresholds

### Guild Tier Score (GTS)

```
GTS = (primary_domain_score x 0.66) + (secondary_domain_score x 0.33)

Max possible with both domains at 100: 99
```

GTS is always computed on-the-fly from current domain scores. Never stored or cached.

### Tier Thresholds

| Tier | GTS Range | Ability Track |
|------|-----------|---------------|
| 1 | 0-20 | Basic passive or utility ability |
| 2 | 20-50 | Core active ability (some A/B choices) |
| 3 | 50-85 | Advanced or situational ability |
| 4 | 85+ | Signature ability -- defining expression of subclass identity |

---

## Domain Proficiency Descriptors

Players see descriptors, never raw scores.

| Score Range | Descriptor |
|-------------|------------|
| 0-9 | Unaware |
| 10-19 | Novice |
| 20-29 | Dabbler |
| 30-39 | Practiced |
| 40-49 | Skilled |
| 50-59 | Proficient |
| 60-69 | Expert |
| 70-79 | Seasoned |
| 80-89 | Masterful |
| 90-99 | Virtuosic |
| 100 | Transcendent |

Guild eligibility threshold: score >= 30 (Practiced).

---

## Data Model Shapes

### CharacterGuild (Django model in world/models.py)

Source of truth for guild/subclass assignment. Lazy creation -- no record means Wanderer.

```python
CharacterGuild:
    character       # OneToOneField to ObjectDB
    guild_id        # CharField, indexed
    primary_domain  # CharField
    secondary_domain # CharField
    subclass_id     # CharField, indexed
    joined_at       # DateTimeField (auto_now_add)
    induction_complete # BooleanField (default=False)
```

### Hybrid Storage Pattern

- **CharacterGuild** model is source of truth
- **character.db.guild_id** and **character.db.subclass_id** are fast-read caches
- Caches updated when model changes (join_guild, etc.)
- GTS computation reads character.db.primary_domain / secondary_domain directly

### GTS Computation (on-the-fly)

```python
def calculate_guild_tier_score(character):
    scores = character.db.domain_scores or {}
    primary = character.db.primary_domain
    secondary = character.db.secondary_domain
    if not primary:
        return 0.0
    p_score = float(scores.get(primary, 0.0))
    s_score = float(scores.get(secondary, 0.0)) if secondary else 0.0
    return (p_score * 0.66) + (s_score * 0.33)
```
