# Wave 11 Audit: Golden-Path Player Journey

Date: 2026-04-22
Scope: First-session player experience from spawn through ancestry choice, early hub onboarding, first quest acquisition, first outbound lead, early combat readiness, and the first guild-discovery expectation.

## Summary

The first-session path is structurally strong but not yet fully honest to the player-facing fantasy.

The good news:

- New players spawn in the correct Vael's Crossing greeter room and receive targeted breadcrumb guidance.
- The early city quest design is purposeful and outward-facing rather than filler-bound.
- The guild-discovery architecture exists and is framed cleanly in UI terms.
- Focused onboarding-adjacent tests and smoke import still pass.

The main issue is that the real golden path currently overpromises in three places:

1. guild progression messaging implies a live domain-practice loop that does not appear to be wired,
2. dialogue-led onboarding promises richer NPC help than the authored city NPCs seem to provide,
3. the starter-equipment flow is too easy to miss for truly new players.

## Golden Path Walkthrough

### 1. Spawn and initial guidance

- New characters arrive in the Harbor Gate arrival room in Vael's Crossing.
- `world/session_lifecycle.py:25` provides contextual login guidance:
  - ancestry selection if none is chosen,
  - guild guidance if no guild is joined,
  - pending quest response guidance when applicable,
  - light breadcrumbing toward `talk`, `ask`, and `quest` for low-level characters with no active lead.

This is a good lightweight alternative to a scripted tutorial and fits the game's exploratory tone.

### 2. Character creation and readiness

- `world/help_entries.py:32` gives a usable new-player overview.
- `world/ancestry_engine.py:280` grants starter items and 50 Scales on ancestry choice.

This gives players enough to start, but the flow does not currently make it obvious that their starter equipment still needs to be equipped manually.

### 3. First quests and first outbound lead

Vael's Crossing's enriched quest set is one of the strongest parts of the current new-player path.

- `vc_q_missing_shipment` teaches city investigation.
- `vc_q_rat_problem` gives a straightforward low-stakes combat loop.
- `vc_q_warden_report` deliberately sends the player outward to Ashreach and chains into that zone's first exterior quest.
- Several city quests route through named districts and reinforce the city's economic and political identity.

This is strong content design and already closer to launch-ready than several surrounding systems.

### 4. First guild expectation

- `world/session_lifecycle.py:67` tells unguilded players to keep practicing fitting domains and watch for a messenger.
- `world/guild_engine.py:1519` sets the guild-eligibility threshold at 30 domain score.
- `world/world_state.py:164` checks for guild eligibility when session XP commits.

This is a good framing model, but it depends on live domain XP accumulation actually happening during play.

## Findings

### 1. Blocker: domain progression for guild discovery does not appear to be wired into live gameplay

Evidence:

- `world/world_state.py:148` defines `accumulate_domain_xp(character, domain, raw_xp)`.
- `world/world_state.py:164` commits session XP into persistent domain scores.
- Search across `world/`, `commands/`, and `typeclasses/` found no live call sites that add domain XP during gameplay.
- A broader search for `domain_xp_` only surfaced the accumulator initializer/reset paths in `world/world_state.py` and `world/banking.py`.
- Meanwhile, `world/session_lifecycle.py:67` explicitly tells players to keep practicing domains, and `world/guild_engine.py:1620` only unlocks guild offers once a domain score reaches the threshold.

Impact:

- The first-session fantasy implies that combat, exploration, gathering, or quests will move a player toward guild discovery.
- In the current code, that progression loop does not appear to exist.
- This makes the `joinguild` breadcrumb functionally misleading and likely blocks normal players from naturally receiving guild invitations.

Recommendation:

- Treat this as the top golden-path launch blocker.
- Wire domain XP into the actual first-session activities that are already being encouraged:
  - combat,
  - investigation/exploration quests,
  - gathering/crafting actions where appropriate,
  - optionally a deliberate practice action if you want a clear fallback path.
- Add at least one integration test that proves a fresh character can gain enough domain score through a realistic early-session loop to trigger a guild invitation.

### 2. High: dialogue-led onboarding is thinner than the onboarding copy suggests

Evidence:

- The guidance in `world/session_lifecycle.py:101` pushes players toward `talk <name>`, `ask <name> about rumors`, and `ask <name> about work`.
- Core early NPCs in `world/areas/vaels_crossing.py` are instantiated plainly:
  - `npc_greeter_maren` at `:356`
  - `npc_broker_carston` at `:1324`
  - `npc_warden_agent_calloway` at `:1603`
  - `npc_barkeep_marta_voss` at `:1868`
- `world/area_builder.py:563-566` shows that NPC dialogue data comes from literal `dialogue=` kwargs and otherwise defaults to empty greeting tiers, topics, and hints.
- These onboarding-critical NPC ids are not being sourced from `world.mob_templates.MOB_TEMPLATES` either, so there is no visible fallback template-based dialogue source in this path.

Impact:

- Quest offers can still work, because the quest engine can independently offer quests from NPC ids.
- But the human-facing discovery layer is much flatter than the game tells players it will be.
- A new player following the recommended verbs may get generic or silent-feeling responses from the exact NPCs meant to anchor their first hour.

Recommendation:

- Author literal builder-safe dialogue payloads directly on the critical Vael's Crossing onboarding NPCs.
- At minimum, make sure the greeter, barkeep, broker, warden contact, and first guild-facing NPCs each have:
  - one clear greeting,
  - at least `work` and `rumors` topics where appropriate,
  - one or more `base_hints` nudging the player toward the next useful verb or place.
- Add an authored-contract test that critical golden-path NPCs expose non-empty dialogue guidance.

### 3. Medium: `help tell` describes the wrong command behavior

Evidence:

- `commands/cmd_dialogue.py:325-345` implements `tell` as NPC-directed dialogue.
- `world/help_entries.py:549-558` documents `tell <player> <message>` as a private player message.

Impact:

- This is exactly the kind of contradiction that confuses a new player at the moment they are trying to learn the dialogue system.
- It also undermines confidence in the help corpus more broadly.

Recommendation:

- Fix the help entry immediately so it reflects the live command surface.
- If remote private messaging is a desired future social feature, give it its own explicit command rather than overloading `tell`.

### 4. Medium: starter equipment is easy to miss in the first hour

Evidence:

- `world/ancestry_engine.py:280-303` creates starter items directly in inventory and grants 50 Scales.
- `world/help_entries.py:61-63` says players start with basic equipment and a starting ability.
- `world/session_lifecycle.py:33-106` does not instruct players to check or equip their starter kit after ancestry selection.
- `world/help_entries.py:40-45` similarly omits an explicit gear-up step from the first-steps sequence even though `world/help_entries.py:283-296` and `:647-655` clearly explain the equipment system elsewhere.

Impact:

- Experienced MUD players may infer the next step.
- Truly new players can enter their first fight without realizing they are still unequipped.

Recommendation:

- Improve the first-session funnel in one of two ways:
  - add an explicit early nudge to run `gear` and `equip`,
  - or auto-equip ancestry starter items when their slots are empty.
- The lower-risk near-term fix is the guidance update; the stronger long-term fix is safe auto-equipping on ancestry selection.

## Improvement Opportunities

These are not blockers, but they would noticeably improve the feel of the first hour.

### 1. Make the first lead feel more curated

The current lightweight guidance is good, but it could feel more intentional if the first breadcrumb referenced a named NPC in the current room when available, rather than generic `talk <name>` language.

### 2. Surface outward travel intent sooner

Vael's Crossing already contains good outbound quest routing. The onboarding layer could capitalize on that by hinting that the city's first jobs are meant to push players toward the roads, not keep them circling the square forever.

### 3. Add a true golden-path integration test

Current tests prove many parts in isolation, but they do not yet validate the first-hour player promise as a continuous journey. A launch-facing verification should cover:

- fresh spawn,
- ancestry selection,
- starter kit presence/readiness,
- first quest offer,
- first quest acceptance,
- first outbound quest completion,
- domain progression,
- guild invitation surfacing.

## Validation

Focused verification run on 2026-04-22:

- `python scripts/run_tests.py tests.test_session_lifecycle tests.test_help_entries tests.test_guild_engine tests.test_content_integration`
- `python scripts/smoke_start.py`

Results:

- 87 tests passed
- smoke import passed

## Recommended Next Fix Order

1. Wire live domain XP progression into real first-session activities.
2. Enrich the critical Vael's Crossing onboarding NPCs with authored dialogue payloads.
3. Correct `help tell`.
4. Tighten starter-equipment onboarding, preferably with explicit `gear` / `equip` guidance and optionally safe auto-equip behavior.
