# M5 Release Acceptance Playtest

This is the human acceptance gate for Soravelon's launch experience. It is not
an admin verification pass. Run every path through an actual Telnet client and
the actual stock webclient, using ordinary player accounts and only commands a
player can discover in the game. Record failures even when the underlying
automated test is green.

The central question is stronger than "does it work?": does the world make a
player curious enough to stay for hours, form plans, remember people and
places, and want to return?

## Preconditions and evidence

- Use a disposable database initialized through the documented world-content
  command, not a copy of production or a test fixture.
- Start the isolated server with `server.conf.playtest_settings` and preserve
  its logs with the transcript.
- Run `python scripts/smoke_protocols.py --telnet-port <base> --web-port
  <base+1> --websocket-port <base+2>` before human play. All three checks must
  pass.
- Use two fresh accounts for the opening and co-op paths. A later, legitimately
  progressed character may continue into distant crafting regions.
- Record the client, start/end time, character names, commit, content revision,
  first confusion, time to first meaningful choice, failed commands, and every
  point where outside help was needed.

Acceptance requires no admin intervention, no backend level in player-facing
text, and no direct service or database writes. A confusing or dull path is a
failure even if the final state is technically correct.

## Fresh-player opening

Budget 60–90 minutes and do not show the route below to the player until they
are blocked. Create a new character, choose an ancestry through the presented
flow (for the reference route, `ancestry human`), read the arrival room, and
allow normal exploration. Confirm that starting gear is equipped and changes
the player's practical readiness without presenting a class or level screen.

The reference route proves the four one-time Naturalism opportunities that
should lead to Verdance discovery:

1. From the Vael's Crossing arrival, go `west`, then `calm nervous mare`.
2. Return `east`, then go `north`, `northeast`, `east`, `east`, `north`; use
   `cut repair strap` at the tanner.
3. Go `south`, `west`, `west`, `southwest`, `south`, `southeast`, `south`,
   `south`, `south`; use `track wolf sign` on the Ashway.
4. Go `north`, `west`, `south`, `south`, `east`, `south`; use
   `test shelter grass` in the Ashreach grassland.
5. Find the offered Verdance contact through the in-world invitation. The
   reference walk to Elwen is `north`, `west`, `north`, `north`, `east`,
   `north`, `north`, `northwest`, `north`, `northeast`, `northwest`, `north`,
   `north`, `east`. Use `joinguild`, `talk Elwen`, and `accept resonance`.

Record whether the player discovers a reason to act before consulting `help`,
whether the travel reads as a place rather than a corridor, and whether Elwen's
invitation feels earned. Reject the path if replaying an opportunity advances
growth, if another domain unlocks, or if any output exposes numeric progression
or a backend level.

## Co-op combat

Continue with two ordinary players in Vael's Crossing. Find Marta Voss in the
Broken Antler tavern, use `talk Marta`, and accept Cellar Menace through the
offered dialogue.

1. The leader uses `group invite <player>` and the ally uses
   `group accept`.
2. The leader uses `quest share cellar`; the ally inspects `quest offers` and
   uses `quest accept cellar`.
3. From Marta's tavern, go `south`, `southwest`, `down`, `south` to the sewer
   junction; `east` reaches the rat tunnel.
4. Coordinate attacks and abilities against sewer rats. Each player uses
   `loot rewards` after eligible encounters. Continue until the shared quest
   completes through ordinary respawns and room movement.

Both nearby contributors must receive quest credit, each eligible player must
claim an independent personal reward, and the two inventories must not share
or duplicate the same reward object. Record whether cooperation creates real
tactical value, whether waiting for respawns becomes dead time, and whether
group/share/loot language is understandable without a moderator.

## Social consequence

After Cellar Menace, use `talk Marta` again and ask about relevant offered
topics. Her response should recognize the service in authored, local,
non-numeric language. Leave the area, reconnect, and repeat the conversation;
recognition must persist.

Then begin the Warden route with `talk Calloway` and `accept`. Walk the real
Ashway to Commander Harven and use `talk Harven`. Return later to Calloway and
another locally relevant contact. Record who knows what, whether the direction
of information spread makes sense, and whether different NPC viewpoints make
the world feel socially inhabited rather than globally omniscient.

Reject numeric standing, trust, reputation, or relationship output. Reject a
reaction that appears before its quest consequence, disappears on reconnect,
or spreads to an NPC with no authored knowledge path.

## Crafting and local economy

Use a character that reached a tool-selling settlement through normal play;
Tremen is the reference path. Do not place a tool or raw material into the
inventory externally. At a real tool vendor, use `list`, `view pickaxe`, and
`buy pickaxe`, then `tools equip pickaxe`.

Find an authored ore location through room cues and `prospect`. Use `mine`
until enough ore is gathered, inspect inventory weight and tool wear, then use
a real forge:

1. `recipes smithing`
2. `smith iron ingot` until two ingots exist
3. `smith iron dagger`
4. inspect, equip, and use the crafted dagger in a real encounter

Damage the tool through gathering and use `repair pickaxe` at a real workbench.
Verify that repair costs carried Scales, insufficient funds do not change the
tool, material quality affects only declared mechanics, and the crafted result
is worth using or selling. Record whether sourcing, processing, and trade
create a satisfying plan or only repetitive friction.

## Travel and exploration

Run one long trip with the map hidden and one with normal `map`, `exits`, and
`routes` use. The Calloway-to-Harven delivery is the minimum walking proof; a
discovered Dragon Courier journey adds the logistics proof. Do not reveal
dragon-continent geometry or use out-of-world direction lists during the first
attempt.

Record memorable landmarks, wrong turns, useful spatial cues, danger and
preparation decisions, reasons to leave the fastest route, and whether the
player can explain how to get home. Travel fails if the only workable strategy
is copying a direction macro, if non-node territory feels empty, or if a
destination unlocks without discovery.

## Quest consequence

Inspect `quest Ashway Dispatch` before and after `talk Harven`. The field report
must be delivered exactly once, the quest must complete without a kiosk-style
turn-in command, and subsequent Warden dialogue must acknowledge the outcome.
Confirm that a quest item cannot be sold, discarded, shared as personal loot,
or paid out twice after reconnect/retry.

For Cellar Menace, compare both players' completion, rewards, Marta recognition,
and local world/faction feedback. Record the story learned, relationship
deepened, route revealed, or visible consequence. A quest with none of those
outcomes is not launch-quality content even if its counters update.

## Recovery and return

After a real fight, note qualitative status, use `rest`, wait through at least
one recovery tick, and move to prove that movement interrupts recovery. Take
damage again, use `sleep`, verify that ordinary room chatter is hidden, then use
`wake`. Where a medic is naturally available, compare a paid blessing with
slower self-recovery.

Disconnect during a safe recovery state and reconnect. Confirm that transient
timers do not duplicate, combat does not remain ghost-attached, inventory and
quest consequences persist, and the character returns to a coherent location
and status. Record whether downtime creates a useful social/planning pause or
simply asks the player to wait.

## Living-world acceptance

Each player answers these without being led:

1. What person, place, problem, or mystery do you most want to revisit?
2. What goal would you pursue during another two hours?
3. Which NPC seemed to have a viewpoint rather than a menu?
4. Where did the world visibly remember or react to you?
5. Which journey felt meaningful, and which felt like traversal tax?
6. What was the first moment you felt agency? What was the first confusion?
7. Did progression feel earned and legible without numbers?
8. What is the return pull—the unfinished relationship, route, craft, danger,
   or mystery that would bring you back tomorrow?

M5 passes only when every path completes through both real client surfaces,
the timed opening remains within its target without coaching, no semantic
guardrail fails, and players can name a credible reason to spend hours in
Soravelon. Preserve transcripts and observations; do not average away a severe
confusion, accessibility failure, fairness defect, or lore contradiction.
