# Social Web Vael's Crossing Playtest

Use this route to test the full Social Web NPC-interaction vertical without
watching numeric reputation meters. Replace `player:<id>` in admin commands
with the active character's Social Web player node key.

## 1. Complete The Warden Report

Commands:

```text
talk Agent Calloway
accept
talk Commander Harven
```

Expected observation:

Calloway records the Warden report as supported institutional knowledge, and
Harven receives only what the Warden-report route can carry. The completion
should pay the authored quest rewards and create Social Web fact/claim state.

Optional inspection:

```text
socialmemory npc:npc_warden_agent_calloway player:<id>
socialmemory npc:npc_warden_outpost_commander player:<id>
```

## 2. Ask Calloway Why

Commands:

```text
talk Agent Calloway
ask Agent Calloway why
ask Agent Calloway about me
```

Expected observation:

Calloway can explain the supported Warden route from what he plausibly knows.
He should not expose raw fact keys, claim keys, confidence values, hidden trace
internals, or private admin identifiers.

## 3. Check Harven Cross-Zone Knowledge

Commands:

```text
travel to Ashreach Outpost
talk Commander Harven
ask Commander Harven about me
```

Expected observation:

Harven cross-zone knowledge should feel institutional and field-practical, not
omniscient. He knows the player through the Warden-report contact route, not
because every NPC globally shares memory.

## 4. Check Whistle Before And After Rumor Propagation

Commands:

```text
talk Whistle
ask Whistle about me
trigger the inn-traveler rumor route
talk Whistle
ask Whistle about me
socialmemory npc:npc_innkeeper_whistle player:<id>
```

Expected observation:

Whistle should not know the sealed Warden details before a real inn/traveler
route carries a rumor or claim. After propagation, Whistle should talk like an
innkeeper with local road talk, not like a Warden clerk.

## 5. Run The Dynamic Social Quest Lifecycle

Commands:

```text
talk Agent Calloway
accept
talk Whistle
look
talk Raith
talk Agent Calloway
```

Expected observation:

The social follow-up offer should be grounded in the previous Warden report,
not a generic trust gate. It should accept, progress through Whistle, the inn
room, Raith, and Calloway, and then record deterministic Social Web
consequences on completion.

the offer uses deterministic renderer fallback unless a provider is explicitly
enabled for testing.

## 6. Contest A Rumor

Commands:

```text
deny Whistle about me
ask Whistle about me
socialmemory npc:npc_innkeeper_whistle player:<id>
```

Expected observation:

The denial/repair verb should create a new player-spoken contested claim that
Whistle knows through direct witness. It must not erase the old rumor, directly
edit hidden standing numbers, or pretend the player can rewrite world truth.
the original rumor remains intact.

## 7. Renderer And Admin Harness

Commands:

```text
python scripts/playtest_social_web_vertical.py
socialmemory npc:npc_warden_agent_calloway player:<id>
socialmemory npc:npc_warden_outpost_commander player:<id>
socialmemory npc:npc_innkeeper_whistle player:<id>
```

Expected observation:

The route script should print every required beat, including renderer fallback
status and socialmemory inspection. Admin inspection should show who knows the
claim, which channel carried it, and which trace explains the route.
