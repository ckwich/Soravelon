# Phase 14: All TBD/TODOs Implemented - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement all stub functions, placeholder handlers, and deferred features left behind by Phases 1–13. Wire quest stubs to the existing quest engine, implement death/banking penalties, activate combat affix hooks, fill OOB message payloads, write real Lore help content, give WorldEventScript basic behavior, and clean up stale zone tier references.

</domain>

<decisions>
## Implementation Decisions

### Death & Banking
- **D-01: 20% Scales drop on death** — Player drops 20% of carried Scales when killed. Banked Scales are safe. Creates banking incentive.
- **D-02: Scales appear on corpse** — Dropped Scales placed inside the player's corpse container. Must return to corpse to reclaim. Other players can loot.
- **D-03: Uncommitted session XP loss** — Lose uncommitted session XP (ndb) on death. Committed XP is safe. Punishes recklessness without destroying long-term progress.

### Combat Affix Hooks
- **D-04: Flat rarity damage multiplier** — Normal: 1.0x, Magic: 1.15x, Rare: 1.3x, Legendary: 1.5x. Applied in `check_mob_damage_modifiers()` based on `mob.db.rarity`.
- **D-05: Affixes map to status effects** — Each combat-relevant affix maps to a status effect. 'Venomous' applies Poison on hit, 'Blazing' applies Burn per round. Uses the existing status effect compound system (Burn+Wet=Steam, Poison+Slow=Venom Lag, etc.).

### Quest Stub Wiring
- **D-06: Wire stubs to existing quest engine** — Phase 11 built quest_engine.py with objectives, quest commands, and NPC quest hooks. Phase 14 connects: `set_quest_flag` calls quest_engine, `open_dialogue` triggers NPC quest offers, dialogue hints pull from active quests. Pure wiring, no new quest systems.
- **D-07: NPC quest hook stubs** — Ashreach Plains (2 NPCs) and Reth Foothills (3 NPCs) have quest hook stubs. Wire them to the quest definitions from Phase 11.

### Misc Stubs
- **D-08: Implement WorldEventScript** — Give the stub base class real event tracking behavior (log world events, track state changes).
- **D-09: Write Lore help entry** — Replace placeholder with real lore help content covering Soravelon world lore accessible to players.
- **D-10: Attuned variant text** — Implement D-23 stub in cmd_abilities.py showing informational text about attuned ability variants.
- **D-11: Real OOB payloads** — combat_update is already wired (Phase 6a). quest_update needs a real payload shape for quest progress/completion events pushed to client.

### Cleanup
- **D-12: Remove zone tier references** — Scan and remove/replace all references to "zone tiers" as a concept. Zone tiers have been removed from the game design but stale references remain in code.

### Claude's Discretion
- Exact session XP loss percentage on death
- Specific affix-to-status-effect mapping table
- WorldEventScript event types and storage strategy
- Lore help entry content
- quest_update OOB payload shape
- Which zone tier references to remove vs refactor

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Death/Banking
- `world/banking.py` — Contains `on_character_death()` and `handle_carried_scales_on_death()` stubs (lines 286-291)
- `world/combat_engine.py` — `spawn_corpse()` creates CorpseContainer on death

### Combat Affixes
- `world/mob_affixes.py` — 3 STUB functions: `check_mob_damage_modifiers()`, `check_mob_on_hit_effects()`, `check_mob_per_round_effects()` (lines 242-266)
- `world/combat_engine.py` — Damage resolution that should call affix hooks
- `world/status_effects.py` — Status effect system with compound matrix

### Quest Wiring
- `world/action_vocabulary.py` — `set_quest_flag` and `open_dialogue` mapped to `_stub_handler()` (lines 297-318)
- `world/dialogue_engine.py` — Quest condition stubs (line 144), quest hints commented out (line 232)
- `world/quest_engine.py` — Existing quest system from Phase 11
- `world/areas/ashreach_plains.py` — NPC quest hook stubs (line 1909)
- `world/areas/reth_foothills.py` — NPC quest hook stubs (line 2097)

### Misc
- `typeclasses/scripts.py` — WorldEventScript stub (line 38)
- `world/help_entries.py` — Lore placeholder (line 916)
- `commands/cmd_abilities.py` — Attuned variant text stub (line 171)
- `world/oob_publisher.py` — combat_update and quest_update placeholders (lines 12-13)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Status effect system (status_effects.py):** Full compound matrix already built. Affix hooks just need to call `apply_status_effect()`.
- **Quest engine (quest_engine.py):** Complete quest system from Phase 11. Action vocabulary stubs just need to call into it.
- **CorpseContainer (objects.py):** Already handles mob corpses with loot. Extending for player death currency is straightforward.
- **OOB publisher (oob_publisher.py):** Typed envelope contract with 8 message types. Adding quest_update payload follows existing pattern.

### Established Patterns
- **Action vocabulary dispatch:** Handler functions registered in ACTIONS dict. Replacing `_stub_handler` with real functions follows existing pattern.
- **Help entry format:** Existing 92 help entries in `help_entries.py` provide template for Lore entry.
- **Combat hook calls:** `combat_engine.py` already calls mob methods at damage/hit/round events. Affix hooks wire into these.

### Integration Points
- `world/combat_engine.py` — Where affix hooks get called during damage resolution
- `typeclasses/characters.py` — Where death handling triggers banking functions
- `world/dialogue_engine.py` — Where quest hints get pulled into NPC conversation

</code_context>

<specifics>
## Specific Ideas

- "THERE ARE NO ZONE TIERS" — zone tiers removed as a concept. All stale references must be cleaned up.
- Death penalty (20% Scales + uncommitted XP) creates meaningful risk without being punishing to long-term progress.
- Affix hooks using existing status effect compounds means legendary mobs can trigger compound chains (Burn+Wet=Steam) naturally.
- Quest wiring is pure integration work — no new systems needed.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 14-all-tbd-todos-implemented*
*Context gathered: 2026-04-04*
