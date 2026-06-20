# Social Web Memory Engine Design

**Date:** 2026-06-20
**Status:** North-star brainstorm spec, approved for preservation and further
exploration
**Repo:** `/Users/ckwichman/Documents/Projects/soravelon`

## Goal

Make Soravelon feel socially alive through a real social graph: people,
households, shops, factions, guilds, institutions, routes, and settlements pass
knowledge through authored contact paths rather than through generic global
rumor.

The current Vael's Crossing social-memory MVP remains the first proof slice.
This spec defines the larger scaffold that MVP should grow into. Town Memory is
still important, but it is the visible local expression of a deeper Social Web
Engine.

The target fantasy is not "NPCs have dialogue variants." The target fantasy is:

> People know people. Institutions keep records. Rumors travel along roads.
> Secrets survive only while the social web fails to connect them to someone
> dangerous.

## Fable Reference Takeaways

Primary reference:

- Xbox Wire, Dan Greer, "Fable: How We Built the Living Population",
  2026-06-10:
  `https://news.xbox.com/en-us/2026/06/10/fable-living-population-details-explained-xbox-games-showcase-2026/`

Additional reference context:

- Xbox Wire interview overview with Ralph Fulton on the living population:
  `https://news.xbox.com/en-us/2026/01/22/fable-interview-overview-details-developer-direct-2026/`
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
something sharper: make social memory legible through language, rumor, access,
social obligation, route knowledge, faction interpretation, and delayed recall.

The right Soravelon version is a text-native social web:

- what happened
- who saw it
- who repeated it
- who believed it
- who profited from telling it that way
- which social edge carried it
- which contact path failed to carry it
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

The spine is **Social Web Memory**.

Every major social entity should exist in an authored graph. Settlements are
major nodes, but they are not the boundary of truth. Knowledge can travel
between zones when there is a believable contact path: Warden reports, merchant
caravans, guild couriers, family letters, criminal fences, pilgrimage routes,
ship crews, archive copies, gossiping travelers, or node-response teams.

Town Memory remains the first visible surface:

- what Vael's Crossing currently says
- what the Warden network records
- what market people repeat
- what an innkeeper hears first
- what a criminal contact keeps private

But the larger system asks:

> Who could plausibly know this by now, and what would they do with it?

The first player-facing promise:

> If I become known in Vael's Crossing, the town should talk, act, and open or
> close paths like it knows what kind of trouble I bring.

The long-term player-facing promise:

> Every social circle in Soravelon remembers differently, and those memories can
> cross settlement borders through real relationships.

## Soravelon-Native Engram At The Heart

Engram should be central in two related but distinct ways.

First, Engram is the authoring and design brain. It should preserve social-web
decisions, faction logic, NPC relationship rationale, source citations, and
cross-session continuity for the designers and agents building Soravelon.

Second, Soravelon should build its own runtime version of Engram for this social
engine. It should be **Engram-shaped** but domain-specific: graph-first,
evidence-backed, chunkable, queryable, explicit about provenance, and tuned for
MUD runtime constraints. The better path is not to clone every Engram feature
or silently depend on the user's personal Engram Hub. The better path is a
small in-game social knowledge kernel inspired by Engram's model.

Practical split:

- Engram stores design memory, social topology rationale, authored source
  evidence, and agent handoffs.
- Soravelon runtime stores live player social facts, knowledge propagation, and
  relationship state in game-owned persistence.
- Soravelon's runtime knowledge engine should feel like Engram: search known
  facts, retrieve cited evidence, inspect graph edges, compile context packets,
  trace claim provenance, and refuse unsupported claims.

This lets us use Engram as the conceptual heart without making live NPC
interaction brittle or dependent on an external personal-memory service.

The Soravelon-native engine should be narrower than Engram but stricter about
game truth:

- It answers "who knows this?" and "why do they know it?"
- It answers "who could plausibly learn this next?"
- It distinguishes fact, claim, rumor, lie, interpretation, and myth.
- It never mutates durable world truth from LLM output.
- It can explain every NPC social reaction through evidence and edges.
- It can compact old events into local stories without losing auditability.

## Core Pillars

### 1. Soravelon-Native Social Knowledge Graph

The core runtime primitive is a social knowledge graph, not a town reputation
counter.

Suggested primitives:

- `SocialNode`: NPC, player, household, shop, guild, faction, institution,
  route, settlement, zone, caravan, crew, archive, or temporary gathering.
- `SocialEdge`: a contact path between nodes, with type, direction, trust,
  latency, bandwidth, secrecy, distortion, and allowed tags.
- `SocialFact`: an event that actually happened according to game authority.
- `SocialClaim`: an assertion someone makes about a fact, which can be true,
  false, incomplete, biased, or unverifiable.
- `SocialKnowledge`: the record that a node knows or believes a fact or claim.
- `SocialContextPack`: the bounded packet used by dialogue, vendors, quests,
  guards, and optional LLM renderers.
- `SocialTrace`: the audit trail for how a claim reached a node.
- `SocialPolicy`: visibility, privacy, expiry, compaction, and player-safety
  rules.

This is the Soravelon version of Engram: a game-owned evidence graph that can
retrieve, explain, and propagate social context.

### 2. Hand-Authored Social Identity

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
hand-shaped. Those anchors should also occupy meaningful graph positions: a
person with no contacts, duties, debts, or routines cannot carry the social web.

### 3. Social Facts, Claims, And Social Knowledge

The existing `SocialMemoryFact` idea records what happened. The scale version
also needs to distinguish what is known, claimed, believed, and repeated.

Suggested split:

- `SocialFact`: what happened, with source, tags, place, subject, weight,
  confidence, and expiration.
- `SocialClaim`: what someone says happened, with speaker, target, intent,
  confidence, bias, and evidence links.
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

### 4. Reputation Clouds, Not Scores

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

### 5. Social Relationships Beyond NPCs

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

### 6. Contact Edges And Propagation Routes

Every social web needs contact infrastructure: people, places, institutions,
and routes where information becomes power.

Contact-route nodes:

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

Edges should be authored or derived from authored data. They should carry
properties like:

- `edge_type`: household, workplace, witness_contact, official_report,
  market_route, guild_line, courier_route, pilgrimage, criminal_whisper,
  patronage, landlord, debt, rivalry, friendship
- `directionality`: one-way, two-way, broadcast, gatekept
- `latency`: immediate, next scene, nightly, weekly, on-courier-arrival
- `trust`: how much the receiver believes this source
- `bandwidth`: how many facts or claims can travel before compression
- `distortion`: whether facts become rumor, slander, euphemism, or myth
- `secrecy`: whether the channel hides, sells, protects, or exposes secrets
- `scope_tags`: which kinds of information this edge can carry
- `blockers`: fear, faction pressure, distance, danger, bribery, shame, debt

NPCs should not all learn everything instantly. A Warden report should travel
differently than a fish-stall rumor or a smuggler warning. A fact should cross
settlement borders only when some contact edge can carry it.

### 7. Local Traits And Network Echoes

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

Local traits should derive from social memory, quest consequences, world-state
dimensions, nodes, and faction pressure. Network echoes should let those traits
matter elsewhere: a Warden outpost may hear that Vael's Crossing is reliable
before a distant market does, while a smuggler route may hear the opposite story
first.

### 8. Social Verbs

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

### 9. Social Consequences As Gameplay

Social Web memory should drive:

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

### 10. Recovery, Repair, And Myth-Making

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

A social circle should not remember every log line forever. It should remember
what people repeat, what institutions record, what families protect, and what
rivals can weaponize.

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

### Cross-Zone Spread Without Omniscience

The user's correction matters: NPC communication should not be trapped inside a
settlement. It should spread beyond local boundaries when the social graph makes
that plausible.

Examples:

- A Warden report from Vael's Crossing reaches another Warden contact before
  ordinary tavern gossip does.
- A market rumor follows a caravan road but skips a remote shrine with no trade
  edge.
- A family letter carries a private mercy story farther than an official notice.
- A criminal whisper crosses zones quickly but loses reliability with each fence.
- A guild courier carries a precise fact but only to people with clearance.
- A pilgrimage route spreads myth faster than evidence.

This lets Soravelon create reputation that travels, but not omnisciently. The
world can feel connected without becoming a global chat room.

### Local Mood And Network Pressure

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
and the types of requests people make. Network pressure should explain why a
local mood changes: a route becomes unsafe, an institution issues a warning, a
market dries up, or a faction quietly suppresses a story.

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

### Local Myth Layer

After enough time or repetition, social circles should stop saying exact facts
and start saying stories.

Example:

- fact: "Player returned Calloway's report."
- rumor: "The new Wanderer carried Warden business cleanly."
- reputation: `reliable`, `warden_aligned`
- myth: "When the road needed a witness, they did not drop the name."

This is where Soravelon can beat visual RPGs: text can make reputation poetic
without exposing numbers.

## Architecture Direction

The social system should be its own service layer, not embedded in dialogue.
Soravelon's existing world models already use Django records for relationships
between entities, so the first implementation should stay boring: relational
tables with graph-shaped APIs and strong indexes. Add a dedicated graph store,
vector index, or LLM summarizer only after deterministic facts, claims, edges,
context packs, and traces are working.

Suggested modules:

- `world/social_taxonomy.py`: approved tags, categories, aliases,
  deprecations, player-safe display text.
- `world/social_graph.py`: social nodes and contact edges, including
  directionality, trust, latency, secrecy, bandwidth, and blockers.
- `world/social_topology.py`: settlement, region, route, faction, institution,
  household, workplace, archive, caravan, and temporary gathering scopes.
- `world/social_knowledge.py`: facts, claims, knowledge records, provenance,
  confidence, expiry, and compaction.
- `world/social_engine.py`: high-level facade for recording facts, spreading
  knowledge, deriving reputation clouds, and building social context.
- `world/social_context.py`: bounded context-pack assembly for dialogue,
  vendors, quests, guards, ambient text, and optional LLM renderers.
- `world/social_propagation.py`: deterministic propagation rules, ticks,
  triggers, edge filters, route latency, and rumor distortion.
- `world/social_trace.py`: admin/debug explanation of how a node learned a fact
  or why a reaction fired.
- `world/social_memory.py`: persistence helpers for facts, claims, knowledge,
  graph edges, relationships, and compaction.
- `world/social_effects.py`: maps social context into dialogue, vendors,
  access, quests, ambient text, and future systems.
- `world/social_director.py`: local mood, local traits, network pressure, and
  scheduled updates.

Runtime API shape:

- `record_social_fact(actor, event, scope, evidence, tags)`
- `assert_social_claim(speaker, claim, target, evidence, intent)`
- `propagate_social_knowledge(trigger, budget)`
- `query_social_context(viewer, subject, purpose, scope)`
- `explain_social_claim(viewer, claim_or_fact)`
- `trace_social_route(source_node, target_node, fact_or_claim)`
- `compact_social_memory(scope, policy)`

AreaBuilder should eventually support:

- `social_entity_id=...`
- `social_profile={...}`
- `household_id=...`
- `workplace_id=...`
- `social_edges=[...]`
- `knowledge_routes=[...]`
- `rumor_routes=[...]`
- `institutional_routes=[...]`
- `settlement_trait_hooks=[...]`
- `social_fact_rewards=[...]` or action vocabulary wrappers

The builder DSL must remain literal and round-trippable.

## Scale Guardrails

- Do not author free-form tags forever. Use a taxonomy registry.
- Do not let every NPC know every public fact instantly.
- Do not trap knowledge inside settlements when a believable contact path
  crosses zones.
- Do not build a generic Engram clone first. Build the smallest deterministic
  social knowledge kernel that can retrieve, explain, and propagate game truth.
- Do not introduce vector search, LLM summarization, or probabilistic mutation
  before deterministic facts, claims, edges, and traces work.
- Do not require every NPC to be fully bespoke. Use archetypes plus hand-authored
  anchors.
- Do not expose numeric social state to players by default.
- Do not let LLMs create social facts or mutate durable state.
- Do not store private player data in the external Engram Hub without an
  explicit infrastructure and consent decision.
- Do not mix node topology, social memory, and quest prose in one uncontrolled
  content pass.
- Do not make permanent damage unrecoverable unless the story intentionally
  earns it.

## First North-Star Vertical Slice

The Vael's Crossing MVP should be reframed as:

> Vael's Crossing remembers two public deeds, one private witness, and one
> institutional report; five NPCs interpret those differently; one ordinary
> local repeats a rumor; one Warden relationship changes access to a more direct
> answer; the Warden report can travel to one out-of-settlement contact while
> tavern gossip remains local until a traveler edge carries it.

That slice proves:

- social facts
- social claims
- social knowledge boundaries
- social nodes and contact edges
- cross-zone propagation without omniscience
- local reputation cloud
- NPC worldview interpretation
- relationship state
- traceable explanation
- rumor/recall
- diegetic feedback
- admin inspection
- optional LLM voice as renderer only

## Later Expansion Order

1. Vael's Crossing Social Web proof with local memory as the visible surface.
2. Soravelon-native Engram kernel: facts, claims, knowledge, context packs,
   and traces.
3. Social taxonomy, graph nodes, and contact-edge schema.
4. First cross-zone route: Warden report, caravan market, inn traveler, guild
   courier, or criminal whisper.
5. Non-quest social verbs: gift, apologize, boast, confess, warn.
6. Vendor, inn, guard, and quest-access effects.
7. Household/workplace metadata.
8. Local traits, local mood, and network pressure.
9. Second-zone contrast pass: Korahei, Varath Prime, Cantera, or Ashreach.
10. Node/social crossover.
11. Blackmail, vouching, leverage, and social repair.

## Open Questions For Continued Brainstorming

1. Which launch-critical contact edges should exist first: Warden reports,
   inn/traveler gossip, market caravans, guild couriers, family letters, or
   criminal whispers?
2. What should trigger propagation: quest completion, scheduled ticks, player
   movement, explicit messenger travel, or social verbs?
3. Should Soravelon expose public NPC traits directly on `look`, or keep them
   inferred through prose?
4. Should every settlement have a top-level local mood, or only major hubs?
5. How dangerous should false rumor be?
6. Which social verbs are launch-critical: `gift`, `apologize`, `boast`,
   `confess`, `vouch`, or `warn`?
7. Which second zone should prove contrast after Vael's Crossing: Korahei for
   communal witness culture, Varath Prime for bureaucracy and class, Cantera for
   frontier logistics, or Ashreach for node-adjacent pressure?

## Success Criteria

The feature is working when a player can truthfully say:

- "I did something, and the right people found out."
- "Someone judged me differently than someone else did."
- "A town changed how it talked because of me."
- "A secret stayed secret until a social route exposed it."
- "A fact crossed into another zone because someone had a reason and a route to
  carry it."
- "I could repair damage, but not erase the story."
- "The world did not call me good or evil. People decided what they thought."
