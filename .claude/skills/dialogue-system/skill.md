---
name: dialogue-system
description: NPC dialogue engine — Standing-tier greetings, topic resolution, hint surfacing, keyword extraction, ambient echoes, and 6 player commands
---

## Activation

This skill triggers when editing these files:
- `world/dialogue_engine.py`
- `world/dialogue_definitions.py`
- `commands/cmd_dialogue.py`
- `tests/test_dialogue.py`

Keywords: dialogue, npc, talk, greet, ask, tell, say, hint, topic, greeting, ambient echo, reactive echo, keyword extraction

---

You are working on **soravelon's NPC dialogue system** — Standing-based greetings, topic resolution, and keyword extraction.

## Key Files
- `world/dialogue_engine.py` — Core engine: greetings, topic resolution, hints, keyword extraction, ambient ticks, reactive echoes
- `world/dialogue_definitions.py` — Constants: `STANDING_TIER_THRESHOLDS`, `TOPIC_SYNONYMS`, `RESPONSE_PRIORITY`, hint thresholds
- `commands/cmd_dialogue.py` — 6 commands: CmdTalk, CmdAsk, CmdSay (override), CmdTell, CmdAccept, CmdDecline + `_find_npc_in_room` helper
- `world/models.py` — `KnownTopicRecord` (topic learning + context hash for hint re-surfacing)
- `typeclasses/characters.py` — `ndb.pending_quest_offer` init at login, cleared in `at_after_move`; reactive echo fired on room entry

## Key Concepts
- **Standing tiers:** Disposition float maps to 8 tiers (exalted→hostile + betrayal). Tier drives greeting selection and hint pools
- **NPC data on db attrs:** `dialogue_greeting_tiers`, `dialogue_topics`, `dialogue_base_hints`, `dialogue_tier_hints`, `ambient_idle_echoes`, `ambient_reactive_echoes` — all set by AreaBuilder
- **Context packet interface (NPC-03):** `_build_dialogue_context()` wraps `get_character_context_packet()` with standing tier and quest state from `quest_engine` — same interface future LLM will consume
- **Quest state in dialogue context:** `_build_dialogue_context()` populates `active_quests`, `completed_quests`, and `failed_quests` from `quest_engine.get_active_quests()` and related calls
- **Hint re-surfacing:** `KnownTopicRecord` stores a `context_hash`. When character's standing/reputation/guild changes, hash changes and previously-known topics reappear as hints
- **Keyword extraction:** 4-stage pipeline — direct match → synonym → partial word → None. Used by both CmdAsk and CmdSay
- **CmdSay overrides Evennia default:** Same `key="say"`, `aliases=["'", '"']`. Broadcasts to room, then extracts NPC keywords (cap 2 responders, sorted by Standing tier)
- **Ambient ticks:** `ambient_npc_tick()` registered as server periodic callback. Finds NPCs via `search_tag("npc", category="character_type")`. Fires idle echoes only when players present in room
- **Quest offer lifecycle:** `CmdTalk` sets `ndb.pending_quest_offer` → `CmdAccept`/`CmdDecline` consumes it → cleared on room change

## Critical Rules
1. **NPC lookup is partial-match** — `_find_npc_in_room` uses case-insensitive `startswith` on `npc_name` db attr or key. Exact match takes priority
2. **CmdSay caps NPC responses at 2** — sorted by Standing tier (friendlier first). Don't increase without considering spam
3. **CmdAccept validates NPC still in room** — stale `pending_quest_offer` where NPC has moved is rejected
4. **Quest integration is live** — `_build_dialogue_context()` reads from `quest_engine` (active/completed/failed quests). `open_dialogue` action checks `get_available_quest_for_npc()` and auto-accepts via `accept_quest()`
5. **Lazy imports throughout** — all `world.*` imports inside functions to avoid circular deps
6. **All engine functions return `(bool, str)` or explicit tuples** — follows repo-wide convention
7. **NPC tag category is `character_type`** — `ambient_npc_tick()` uses `search_tag("npc", category="character_type")`, NOT `object_type`

## References
- **Mob Disposition:** `world/mob_disposition.py` — Standing tier computed from disposition float
- **World State:** `world/world_state.py` — `get_character_context_packet()` feeds dialogue context
- **Quest Engine:** `world/quest_engine.py` — `get_active_quests()`, `get_available_quest_for_npc()`, `accept_quest()` feed dialogue and action vocabulary
- **Area Builder:** `world/area_builder.py` — Sets NPC dialogue db attrs during zone initialization

---
**Last Updated:** 2026-04-04
