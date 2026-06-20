# Living Settlement Memory Engine Design

**Date:** 2026-06-20
**Status:** North-star brainstorm spec, approved for preservation and further
exploration
**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

## Goal

Make Soravelon's settlements feel socially alive: places where people remember,
misremember, gossip, judge, invite, refuse, protect, exploit, and change their
daily texture because of what the player has done.

The current Vael's Crossing social-memory MVP remains the first proof slice.
This spec defines the larger scaffold that MVP should grow into.

The target fantasy is not "NPCs have dialogue variants." The target fantasy is:

> A town knows you, argues about you, changes around you, and makes you wonder
> what kind of person you are becoming in that place.

## Fable Reference Takeaways

Primary reference:

- Xbox Wire, Dan Greer, "Fable: How We Built the Living Population",
  2026-06-10:
  `https://news.xbox.com/en-us/2026/06/10/fable-living-population-details-explained-xbox-games-showcase-2026/`

Additional reference context:

- GamesRadar interview with Ralph Fulton on persistent NPCs and daily routines:
  `https://www.gamesradar.com/games/rpg/weve-stuck-with-the-ambition-we-had-right-at-the-start-how-fables-open-world-fantasy-lets-you-meddle-in-the-lives-of-over-1000-living-npcs/`
- GamesRadar interview on shades-of-gray morality, witness systems, and
  settlement-specific reputations:
  `https://www.gamesradar.com/games/rpg/fables-shades-of-gray-approach-to-morality-directly-ties-into-the-rpgs-living-population-with-a-reputation-system-i-cant-wait-to-play-with/`
- Fable "Build An Extraordinary Life" gameplay demo:
  `https://www.youtube.com/watch?v=NScIccqYThQ`

Key design lessons to translate, not copy:

- Fable treats its population as the heart of the game, not background crowd
  dressing.
- NPCs are hand-authored individuals with a visible name, role, trait, home,
  job, schedule, and worldview.
- Reputations are settlement-local and can combine in ways different NPCs judge
  differently.
- NPCs react through their own lens. The game does not simply label the player
  good or evil.
- Witnessing matters. Secret actions should remain secret until someone sees,
  hears, reports, or misreports them.
- Memory affects practical systems: jobs, property, wages, rent, house prices,
  shop openings, romance, grudges, blackmail, and settlement traits.
- Consequences should feel real but not permanently ruin a save. Recovery,
  repopulation, apology, bribery, restitution, or social repair can exist.
- The player should be able to poke the system just to see what happens.

## Soravelon Translation

Soravelon should not try to clone Fable's visual life-sim surface. A MUD can do
something sharper: make town memory legible through language, rumor, access,
social obligation, route knowledge, faction interpretation, and delayed recall.

The right Soravelon version is a text-native social ecology:

- what happened
- who saw it
- who repeated it
- who believed it
- who profited from telling it that way
- who changed their behavior because of it
- who offers the player a door, warning, favor, debt, threat, or lie because of
  it

This must remain compatible with Soravelon's existing identity:

- no player-facing level language
- no generic morality meter
- no casual hidden-lore reveal
- no flattening factions into good/evil teams
- no player-visible numeric reputation dashboard as the default surface
- world-state and node systems remain backbone systems, not flavor
- quests should route players toward real places and discoveries

## Design Spine

The spine is **Town Memory**.

Every major settlement should eventually have a local memory made of public
rumors, private witnesses, institutional records, civic mood, favors, debts,
grudges, invitations, refusals, and social roles.

The first player-facing promise:

> If I become known in Vael's Crossing, the town should talk, act, and open or
> close paths like it knows what kind of trouble I bring.

The long-term player-facing promise:

> Every place in Soravelon remembers differently.

## Core Pillars

### 1. Hand-Authored Social Identity

Fable's biggest lesson is that procedural people are not enough. Soravelon
should avoid generic NPC profiles as the final product.

Each important NPC should have:

- `social_role`: witness, broker, patron, skeptic, creditor, protector,
  gossip, gatekeeper, rival, employer, informant, caretaker, magistrate, elder
- `public_trait`: a short player-visible phrase like "careful Warden contact"
  or "salt-dry innkeeper"
- `worldview`: tags this NPC admires, dislikes, fears, exploits, forgives, or
  spreads
- `ties`: optional authored links to factions, jobs, households, workplaces,
  routes, patrons, and rivals
- `memory_style`: what they remember well, exaggerate, ignore, or forgive

Low-importance NPCs can use archetypes, but hubs need named anchors that feel
hand-shaped.

### 2. Social Facts And Social Knowledge

The existing `SocialMemoryFact` idea records what happened. The scale version
also needs to distinguish what is known.

Suggested split:

- `SocialFact`: what happened, with source, tags, place, subject, weight,
  confidence, and expiration.
- `SocialKnowledge`: who knows or claims the fact, how they learned it, how
  reliable it is, and whether they are spreading it.

Knowledge channels:

- direct witness
- official report
- tavern rumor
- market gossip
- guild record
- faction intelligence
- family/household talk
- criminal whisper
- public notice
- bard/song/story

This is how secret actions, blackmail, false rumor, and settlement-specific
reputation become possible.

### 3. Reputation Clouds, Not Scores

Each settlement should maintain a small active reputation cloud rather than a
single moral axis.

Examples:

- `reliable`
- `reckless`
- `generous`
- `profit_minded`
- `warden_aligned`
- `discreet`
- `debtbreaker`
- `node_careless`
- `careful_witness`
- `dangerous_but_useful`

Like the Fable reference, only a bounded number should be active in a settlement
at once. Too many reputations becomes noise. Soravelon's equivalent of Fable's
"up to six active reputations" should be:

- top 3 public reputations
- top 2 institutional reputations
- top 1 private/rumor tension, if relevant

The player should not see this as a spreadsheet. They should hear it in how
people speak.

### 4. Social Relationships Beyond NPCs

The Vael MVP currently names `NpcRelationship`. The scale version should use a
generic social relationship model or an adapter that can become one.

Relationship subjects:

- NPC
- faction
- settlement
- guild
- shop
- household
- institution
- route

Relationship dimensions:

- affinity
- trust
- fear
- respect
- debt owed to player
- debt owed by player
- suspicion
- obligation
- leverage
- grief
- protection

This lets Soravelon represent more than liking and disliking. A Warden might
trust the player but still dislike them. A broker might dislike the player but
find them profitable. A household might fear the player but owe them shelter.

### 5. Social Roles And Rumor Routes

Every town needs social infrastructure: places where information becomes power.

Rumor-route nodes:

- inns and taverns
- markets
- barracks
- shrines
- workshops
- courier platforms
- docks and stables
- guild rooms
- noble houses
- criminal dens
- archive desks

NPCs should not all learn everything instantly. A Warden report should travel
differently than a fish-stall rumor or a smuggler warning.

### 6. Settlement Traits

Fable uses settlement traits to reflect dramatic changes. Soravelon should have
its own version: concise settlement-state phrases that affect room text, NPC
greetings, rumors, prices, and opportunities.

Examples:

- "a road town newly proud of its Wardens"
- "a market where debt collectors speak softly"
- "a harbor settlement short on trust and lamp oil"
- "an underwatched crossroads"
- "a place famous for one corpse no one agrees how to discuss"
- "a village where witnesses have begun naming the dead again"

Settlement traits should derive from social memory, quest consequences,
world-state dimensions, nodes, and faction pressure.

### 7. Social Verbs

The player needs verbs that intentionally touch the social engine.

Candidate commands/actions:

- `thank`
- `apologize`
- `boast`
- `confess`
- `deny`
- `vouch`
- `gift`
- `hire`
- `fire`
- `shelter`
- `bribe`
- `warn`
- `spread`
- `keepquiet`
- `introduce`

These should not all ship early. The important scaffold is that social verbs
create social facts and knowledge records rather than special-cased dialogue.

### 8. Social Consequences As Gameplay

Town Memory should drive:

- dialogue tone and topic access
- quest offers and quest refusal
- vendor prices and special stock
- inn shelter and room access
- Warden warnings or searches
- criminal invitations or threats
- guild notice and induction hints
- courier reliability
- rumors about route safety
- faction suspicion
- crowd barks and ambient echoes
- notices, ledgers, songs, or graffiti
- companion/dragon interaction hooks later

This is where "alive" stops being flavor.

### 9. Recovery, Repair, And Myth-Making

Consequences should persist, but not make the game brittle.

Repair paths:

- apology
- restitution
- public service
- witness correction
- faction mediation
- paying debt
- accepting blame
- exile timer
- social sponsor vouching

Memory transformation:

- exact fact
- rumor
- compressed reputation
- myth
- fading local story

A town should not remember every log line forever. It should remember what
people repeat.

## Feature Constellations

### The Social Panel, MUD Edition

Fable has a UI panel that tells the player why an NPC feels the way they do.
Soravelon should not show a panel by default, but it needs a text-native
equivalent.

Possible surfaces:

- `look <npc>` shows public role, trait, and mood when appropriate.
- `talk <npc>` can include a short relationship tell: "She knows your name from
  the Warden report."
- `ask <npc> about me` gives diegetic self-reputation feedback.
- admin-only `socialmemory` remains numeric/debug-facing.

### The People Toybox, Soravelon Edition

The player should be able to poke social systems to see what happens:

- give a noble a rude gift
- warn a smuggler before a raid
- vouch for a reckless courier
- confess to a Warden before rumors arrive
- overpay an innkeeper during scarcity
- refuse payment in front of a broker
- rescue someone privately and watch the secret stay secret
- let a false rumor spread and later correct it

### Blackmail And Leverage

Fable's blackmail example is a major design clue: social memory becomes story
when secrets create leverage.

Soravelon versions:

- a broker knows you helped Wardens and asks for quiet consideration
- a Warden knows you spared a smuggler and demands an explanation
- an innkeeper knows who slept under whose roof during a dangerous night
- a guild contact knows you lied to protect someone
- a criminal uses a true fact with a false interpretation

### Civic Mood

Each settlement can have social mood dimensions:

- safety
- scarcity
- trust
- fear
- pride
- grief
- suspicion
- faction pressure
- node anxiety

Mood should influence ambient text, rumor frequency, guard behavior, prices,
and the types of requests people make.

### Household And Workplace Memory

Fable leans on homes, jobs, landlords, wages, and rent. Soravelon does not need
full property simulation immediately, but households and workplaces are useful
social units.

Scale-friendly version:

- NPCs can belong to a `household_id` and `workplace_id`.
- Social facts can target households and workplaces.
- One member's grief, debt, gratitude, or fear can affect how related NPCs
  receive the player.
- Shops can open, close, discount, refuse, or change stock from social state.

### Settlement Myth Layer

After enough time or repetition, towns should stop saying exact facts and start
saying stories.

Example:

- fact: "Player returned Calloway's report."
- rumor: "The new Wanderer carried Warden business cleanly."
- reputation: `reliable`, `warden_aligned`
- myth: "When the road needed a witness, they did not drop the name."

This is where Soravelon can beat visual RPGs: text can make reputation poetic
without exposing numbers.

## Architecture Direction

The social system should be its own service layer, not embedded in dialogue.

Suggested modules:

- `world/social_taxonomy.py`: approved tags, categories, aliases,
  deprecations, player-safe display text.
- `world/social_topology.py`: settlement, region, route, faction, institution,
  household, and workplace scopes.
- `world/social_engine.py`: high-level facade for recording facts, spreading
  knowledge, deriving reputation clouds, and building social context.
- `world/social_memory.py`: persistence helpers for facts, knowledge, and
  relationships.
- `world/social_effects.py`: maps social context into dialogue, vendors,
  access, quests, ambient text, and future systems.
- `world/social_director.py`: settlement-level mood, traits, and scheduled
  updates.

AreaBuilder should eventually support:

- `social_profile={...}`
- `household_id=...`
- `workplace_id=...`
- `rumor_routes=[...]`
- `settlement_trait_hooks=[...]`
- `social_fact_rewards=[...]` or action vocabulary wrappers

The builder DSL must remain literal and round-trippable.

## Scale Guardrails

- Do not author free-form tags forever. Use a taxonomy registry.
- Do not let every NPC know every public fact instantly.
- Do not require every NPC to be fully bespoke. Use archetypes plus hand-authored
  anchors.
- Do not expose numeric social state to players by default.
- Do not let LLMs create social facts or mutate durable state.
- Do not mix node topology, social memory, and quest prose in one uncontrolled
  content pass.
- Do not make permanent damage unrecoverable unless the story intentionally
  earns it.

## First North-Star Vertical Slice

The Vael's Crossing MVP should be reframed as:

> Vael's Crossing remembers two public deeds, one private witness, and one
> institutional report; five NPCs interpret those differently; one ordinary
> local repeats a rumor; one Warden relationship changes access to a more direct
> answer.

That slice proves:

- social facts
- social knowledge boundaries
- local reputation cloud
- NPC worldview interpretation
- relationship state
- rumor/recall
- diegetic feedback
- admin inspection
- optional LLM voice as renderer only

## Later Expansion Order

1. Vael's Crossing Town Memory proof.
2. Social taxonomy and topology hardening.
3. Non-quest social verbs: gift, apologize, boast, confess, warn.
4. Vendor and inn effects.
5. Rumor-route propagation.
6. Household/workplace metadata.
7. Settlement traits and civic mood.
8. Second settlement contrast pass: Korahei or Varath Prime.
9. Node/social crossover.
10. Blackmail, vouching, and leverage.

## Open Questions For Continued Brainstorming

1. Should Soravelon expose public NPC traits directly on `look`, or keep them
   inferred through prose?
2. Should every settlement have a top-level civic mood, or only major hubs?
3. Should rumor propagation run on timers, quest completion, player movement,
   or explicit social actions?
4. How dangerous should false rumor be?
5. Which social verbs are launch-critical: `gift`, `apologize`, `boast`,
   `confess`, `vouch`, or `warn`?
6. Which settlement should become the first contrast case after Vael's Crossing:
   Korahei for communal witness culture, or Varath Prime for bureaucracy,
   class, and institutional memory?

## Success Criteria

The feature is working when a player can truthfully say:

- "I did something, and the right people found out."
- "Someone judged me differently than someone else did."
- "A town changed how it talked because of me."
- "A secret stayed secret until a social route exposed it."
- "I could repair damage, but not erase the story."
- "The world did not call me good or evil. People decided what they thought."

