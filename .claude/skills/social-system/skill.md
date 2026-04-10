---
name: social-system
description: Social commands (who/shout/whisper), OOC and Domain channel typeclasses, zone-wide and private messaging
---

## Activation

This skill triggers when editing these files:
- `commands/cmd_social.py`
- `typeclasses/channels.py`
- `tests/test_social.py`

Keywords: social, who, shout, whisper, channel, OOC, domain channel, zone chat, private message

---

You are working on **the social system** — player communication commands and channel typeclasses.

## Key Files
- `commands/cmd_social.py` — CmdWho, CmdShout, CmdWhisper + `SHOUT_STAMINA_COST`
- `typeclasses/channels.py` — `OOCChannel` (server-wide OOC), `DomainChannel` (primary domain gated)
- `commands/default_cmdsets.py` — All three social commands registered in `CharacterCmdSet`
- `server/conf/settings.py` — `DEFAULT_CHANNELS` includes OOC channel entry with `typeclasses.channels.OOCChannel`
- `tests/test_social.py` — Unit tests (unittest.TestCase + MagicMock, no Evennia DB)

## Key Concepts
- **CmdWho:** Lists all puppeted characters via `SESSION_HANDLER.get_sessions()`. Shows name, ancestry, guild/primary domain, and zone (from room `zone_id` tag)
- **CmdShout:** Zone-wide in-character broadcast. Finds all rooms via `evennia.search_tag(zone_id, category="zone_id")`, then messages all online characters. Costs `SHOUT_STAMINA_COST` (10) stamina via `recovery_engine.spend_stamina()` — centralized stamina deduction with automatic stat push
- **CmdWhisper:** In-room private message. Target found via `self.caller.search()` in room. Third parties see notification without message content
- **OOCChannel:** Simple channel subclass with `[OOC]` prefix. Auto-created via `DEFAULT_CHANNELS` setting
- **DomainChannel:** Restricts sending to characters whose primary domain (highest score in `db.domain_scores`) matches `db.domain_name` or channel key. Check runs in `at_pre_msg()`
- **Stamina is volatile (`ndb`):** Shout reads/writes `character.ndb.stamina` via `spend_stamina()`. Not persisted across sessions

## Critical Rules
1. **Shout uses zone tags, not BFS** — `search_tag(zone_id, category="zone_id")` finds all zone rooms. Don't use node_helpers BFS
2. **Shout stamina delegates to `recovery_engine.spend_stamina()`** — never manually deduct `ndb.stamina` or call `push_stat_update()` in social commands
3. **Whisper search is room-scoped** — `self.caller.search(name, location=self.caller.location)` restricts to same room
4. **DomainChannel checks at send time** — `at_pre_msg()` rejects non-members. Subscription is not restricted
5. **Sleeping characters skipped** — Shout checks `ndb.is_sleeping` on recipients
6. **All commands in Social help_category** — `help_category = "Social"` for who/shout/whisper

## References
- **Recovery Engine:** `world/recovery_engine.py` — `spend_stamina()` used by CmdShout for stamina cost
- **World State:** `world/world_state.py` — `db.domain_scores` used by DomainChannel membership check
- **Server Conf:** `server/conf/settings.py` — `DEFAULT_CHANNELS` defines OOC channel

---
**Last Updated:** 2026-04-05
