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
