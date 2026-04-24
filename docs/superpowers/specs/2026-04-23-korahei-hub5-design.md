# Korahei And Velu'ana Hub 5 Design Start

Date: 2026-04-23

Status: design start, not yet implemented

## Source Basis

This packet is based on the in-repo AGENTS guide, `C:\Obsidian\brain\Soravelon\soravelon-areaspec.md`, `C:\Obsidian\brain\Soravelon\Soravelon_World_Bible.md`, `C:\Obsidian\brain\Soravelon\soravelon.md`, `C:\Obsidian\brain\Soravelon\soravelon-ancestries.md`, `C:\Obsidian\brain\Soravelon\soravelon-companions.md`, and current Engram memories about world expression scope and the ten-zone content scan.

## Binding Guardrails

- Korahei is the largest Kau'roran settlement in Velu'ana: circular, open to the sky, warm, enormous, and politically complex.
- Kau'roran culture should feel communal rather than generic island flavor. The first and best bites of food are shared, people sit and build in circles, and welcome is active rather than ornamental.
- Kiai is sacred because the dragon chooses the bonded human. In current-era launch content, do not imply dragons are secretly intelligent under the curse. Show creature choice, trust, ritual discipline, and awe without revealing the hidden truth.
- The archipelago is where the old foundations are densest. Hub 5 node behavior should feel different, but player-facing text must not casually explain the dragon-body origin of Velu'ana.
- Basic quests must not make big shared-world changes. Routine quest expression should be NPC memory, relationship recognition, and character-scoped acknowledgement.
- Major permanent world changes belong to long, prerequisite-locked special event chains only.
- Dragon Rookeries and true kiai bonding should be handled carefully because companion ownership/access mechanics are still pending.
- Colonization history must be emotionally present without turning every Kau'roran NPC into an exposition terminal.

## Recommended First Hub 5 Pack

Implement Korahei as one city zone, then build four immediately surrounding land/shore zones:

- `korahei`: the hub city proper. This should include the beach markets as a district rather than splitting the city into multiple city files unless a future builder pass requires otherwise.
- `veluana_outer_reefs`: the first exterior approach zone and practical fishing/gathering/tutorial route for archipelago traversal.
- `kiai_grounds`: ritual grounds and old node concentration. This is a respect, witness, and preparation zone at launch, not a free dragon-bond dispenser.
- `veluana_central_isle`: the largest island and strongest "something is physically wrong in an old, beautiful way" exploration zone.
- `colonist_ruins`: the emotionally heavy historical zone, best used as the first long-form justice/memory quest thread for Hub 5.

Defer `dragon_rookeries` until dragon recognition/access rules are ready. Defer `makavelu_sunken_ruins` until diving and underwater traversal expectations are settled.

## Korahei City Feel

Korahei should contrast sharply with Varath Prime. Varath Prime intimidates through architecture and paperwork. Korahei welcomes through scale, sunlight, food, and circles, then slowly reveals the complexity under that warmth.

Primary city districts:

- Arrival Circle: courier landing, guest protocols, map reveals, first Korahei welcome.
- Beach Markets: huge stalls, shared food customs, fish, shellwork, reef tools, practical hospitality.
- Open Hearths: communal kitchens, cooking station, shared meals, family alliances.
- Tide Council Ring: elders, visiting diplomats, social negotiation, political tension.
- Warden Guest House: Dragon Wardens treated as honored allies but still outsiders.
- Listening Terraces: node-watchers, resonance tradition, non-Arcana magical logic.
- Craft Rings: reinforced large-scale tools, shellwork, coral-safe repairs, boatwrights.
- Quiet House: colonization memory kept with dignity; not a tourist memorial.

NPC tone should be warm but not soft. Kau'roran NPCs can be generous, amused by mainland assumptions, formal around kiai, and guarded around Imperial history.

## Initial Quest Shape

Every basic quest should either deepen Korahei relationships, teach a local custom, guide the player outward, or seed a longer chain.

Suggested city quests:

- `kor_q_first_bite`: social/onboarding quest. Share food correctly, learn guest-circle etiquette, and meet market/council/warden contacts.
- `kor_q_reef_runner`: delivery/exploration quest. Carry tide tokens or reef marks to the Outer Reefs, guiding players to the first exterior zone.
- `kor_q_guest_names`: conversation quest using `talk`, `ask`, and `tell` to show NPC memory and local respect.
- `kor_q_warden_guest`: introduce the Dragon Wardens as allies who are respected but not culturally identical to Kau'roran practice.
- `kor_q_quiet_bowl`: carefully introduce colonization memory by asking the player to carry offerings or names to the Quiet House.

Longer chain seeds:

- Kiai preparation should be prerequisite-locked and relationship-heavy. Early steps should teach humility, creature care, and witness etiquette, not grant a bond.
- Colonist Ruins should support a serious, multi-step memory and accountability arc. Any permanent shared-world memorial should be reserved for a later special event chain with player names recorded.
- Outer Reefs should route players to fishing, reef gathering, ferry/boat logistics, and early danger signals before they reach the deeper Hub 5 zones.

## Surrounding Zone Feel

### `veluana_outer_reefs`

Beautiful and dangerous. The reefs connect islands like shallow roads but should never feel like a theme-park beach. Content should support fishing, shellfish, reef kelp, saltfruit, coral-safe harvesting, reef predators, weather, and navigation by tide marks.

Quest role: first outbound route from Korahei; teach reef logistics and danger without hard-gating exploration.

### `kiai_grounds`

Old, quiet, and social rather than combat-first. The space should be built in rings and waiting places. NPCs should care about posture, patience, animal handling, and whether the player treats ordinary creatures well.

Quest role: introduce kiai as witnessed choice. Launch quests can prepare, observe, clean, carry, and learn. They should not make dragons speak or imply hidden intelligence.

### `veluana_central_isle`

The foundation is densest here. The terrain is subtly wrong: tide pools line up in impossible circles, old stone listens to rain, and paths make sense only when walked in loops. This is the strongest node/weirdness zone in the first Hub 5 pack.

Quest role: exploration, node study, resonance tradition, and clues that the archipelago's old infrastructure is unlike Varath or Sorath.

### `colonist_ruins`

Emotionally resonant and restrained. The ruins should show occupation, extraction, resistance, grief, and survival without reducing Kau'roran people to their colonization trauma. Some NPCs speak plainly; some refuse; both are valid.

Quest role: memory, repair, names, missing records, and careful confrontation with Imperial legacy. Big permanent memorialization belongs to a later special event chain.

## Itemization And Gathering Direction

Early Hub 5 materials should emphasize coastal and archipelago identity without invalidating prior tiers:

- Fish: reef silverjack, tide eel, sunscale snapper.
- Forage: saltfruit, reef kelp, shellbean, hearthroot.
- Herbs: sunleaf, kiai blossom, tide-mint.
- Ore/stone: blackglass shard, reefstone, old ring basalt.
- Hide/shell: reefcrawler shell, shore drake hide, braided scale-shed.
- Craft identity: corrosion resistance, water-touch, resonance-safe repairs, large-scale Kau'roran toolwork.

Material registry additions should be added before gathering pools ship, and tests should keep enforcing that authored pools only reference runtime-registered materials.

## Implementation Notes

- Use strict builder-safe AreaBuilder DSL only.
- Do not create helper loops or data-driven abstractions in area files.
- Add contract tests before implementation, following the existing Hub 4 pattern.
- Keep Korahei city services and vendors zone-appropriate: food, reef tools, fishing gear, boat/courier services, craft rings, and respectful visitor supplies.
- No backend level language should appear in player-facing content.
- Korahei should have a flight stop, but dragon transit text must preserve the current-era "dragons as beasts" public understanding.

## Proposed Next Step

Create tests and a first implementation slice for `world/areas/korahei.py`:

1. City metadata, map anchors, and safe service rooms.
2. Core districts and exits.
3. Starter NPCs with rich dialogue.
4. Five meaningful city quests that route players into Outer Reefs, Kiai Grounds, Central Isle, and Colonist Ruins.
5. Vendor and material contract coverage.
