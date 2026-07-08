# Social Quest Grammar Design

This slice adds the first deterministic grammar for Social Web-backed quest
offers.

The goal is not to make an LLM invent quests. Soravelon owns the incident, the
roles, the objective structure, the evidence, the compatibility checks, and the
social consequences. A future provider can only phrase a selected offer from a
bounded packet.

## Runtime Contract

`world.social_quest_grammar` owns two expandable registries:

- `INCIDENT_SEEDS`: what happened, who matters, what evidence exists, which
  social inputs can personalize it, and which archetypes can use it.
- `QUEST_ARCHETYPES`: the playable structure, required roles, objective steps,
  social effects, and LLM render slots.

`build_social_quest_context(seed_id, archetype_id, ...)` compiles those into:

- a deterministic incident packet
- a deterministic archetype packet
- role-aware actor bindings
- a bounded Social Web context packet
- a deterministic objective/social-effect outline
- an LLM context packet with `provider_call_allowed=False`

The function performs no database work and calls no provider.

`compile_quest_spec(seed_id, archetype_id, ...)` turns the same grammar into a
normal `area.quest()`-compatible quest dict. It requires a concrete
`quest_id`, `quest_giver`, social grounding, and objective targets that map each
live objective step to an existing `quest_engine` objective type.

`AreaBuilder.quest()` preserves:

- `incident_seed`
- `quest_archetype`
- `social_quest_context`

## Offer Registry Contract

Live Social Web quest offers should be selected from a data-driven offer
registry, not from one-off control flow inside dialogue or quest commands.

Each offer rule must declare:

- `quest_id`
- `quest_giver`
- `seed_id`
- `archetype_id`
- required Social Web grounding, such as fact tags, fact-key fragments, claim
  status, or trace requirements
- actor bindings and objective targets
- description templates that can include bounded Social Web memory summaries
- player-safe explainability metadata
- future contest/repair hooks where the offer can later be denied, corrected,
  reframed, or socially repaired

The registry is not a new source of truth. It is a selector and binder for
existing Social Web facts, claims, traces, and quest grammar data. Adding a new
offer should primarily mean adding a new rule plus tests. It should not require
branching dialogue commands, duplicating quest lifecycle code, or letting an LLM
choose durable quest structure.

## Explainability And Repair

Every Social Web-gated quest offer should carry a player-safe explanation
packet in `social_quest_context`. This packet exists for future diegetic
surfaces such as `ask <npc> about me`, `ask <npc> why`, or non-numeric
relationship tells. It should answer:

- which known fact or claim made the offer plausible
- which social channel or node is allowed to know it
- what the NPC may safely say to the player
- what the NPC must not imply without an explicit trace

The packet must not expose hidden lore, private unsupported knowledge, numeric
reputation scores, raw prompts, raw model output, or admin-only identifiers
unless those identifiers are already part of a player-safe Social Web summary.

Contest and repair hooks are also metadata only at this layer. They reserve
space for later Social Web gameplay such as `deny`, `confess`, `vouch`, or
`correct a false claim`, but they do not mutate reputation by themselves.
Runtime repair must still be implemented through deterministic facts, claims,
knowledge propagation, and ordinary quest/action effects.

## Expansion Rules

New seeds should add new categories, roles, evidence, and agendas through
validated data. Do not branch quest logic for a one-off social story until the
grammar cannot express it.

New archetypes should describe reusable social structures such as blackmail,
witness protection, corrective testimony, rivalry, patronage, restitution, debt,
or faction mediation.

Political intrigue and coercive NPC behavior are modeled as agendas and
methods, not as alignment labels. A character can exploit, conceal, threaten,
or seek justice without the system needing to flatten them into good or evil.

Seeds that depend on `prior_interactions`, known Social Web facts, known Social
Web claims, or contact traces must not compile into live quest offers from empty
context. The offer needs at least one real grounding source so "personal" quests
do not degrade into disguised generic templates.

## LLM Boundary

The LLM context is a renderer-only packet. It may use prior interactions,
Social Web facts, Social Web claims, and selected objectives to make an offer
sound personal.

It must not:

- create durable facts
- mutate quests
- mutate standing, inventory, access, or world state
- decide who knows a fact
- invent relationships, locations, factions, or consequences
- reveal hidden lore

Provider integration should add a renderer beside this grammar, not replace the
grammar.
