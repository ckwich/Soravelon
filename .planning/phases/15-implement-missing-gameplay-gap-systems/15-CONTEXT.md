# Phase 15: Implement Missing Gameplay Gap Systems - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Make the game fully playable end-to-end. This phase covers:

1. **New systems:** Vendor/shop economy, HP/stamina recovery (rest/sleep/medic blessings), item stat inspection, social systems (who/chat/shout/whisper)
2. **Missing content:** Gathering tools, fish pools, quest items with no source, crafting output item definitions, missing loot tables (rat/bandit)
3. **Combat system fixes:** Ability handler return type normalization (F7), compound status effects (steam/discharge/petrify — F12), custom corpse loot command (3.12), group loot mode distribution logic (3.9)

</domain>

<decisions>
## Implementation Decisions

### Vendor / Shop Economy
- **D-01:** Fixed prices for general vendors. Faction vendors adjust prices based on standing.
- **D-02:** Commands: `buy <item>`, `sell <item>`, `appraise <item>` (shows what vendor will pay), `list` (vendor stock + prices), `view <item>` (item description + full stats).
- **D-03:** Vendors are type-restricted via `db.vendor_accepts` tag list. Weapon shop only buys weapons, alchemy shop only buys potions/ingredients, etc. Quest items blocked from sale.
- **D-04:** Sell-back returns 33% of item value. Sold items then appear in shop stock at full price.
- **D-05:** Unlimited base stock from equipment_catalog. Player-sold items also appear in vendor inventory.

### Vendor Type Mapping (Vaels Crossing)
- mk_weapon_shop (Brenna): accepts `["weapon"]`
- mk_armor_shop (Derik): accepts `["armor"]`
- mk_potion_shop (Ystra): accepts `["consumable", "ingredient"]`
- mk_general_store: accepts `["item", "material"]`
- mk_tanner: accepts `["hide"]`

### HP Recovery & Resting
- **D-06:** Three-tier recovery: passive regen (always out-of-combat), rest/sit (accelerated), sleep (fastest but blinds player).
- **D-07:** `rest` command (alias: `sit`) — accelerated regen, interrupted by combat or movement.
- **D-08:** `sleep` command — fastest regen but player is blind (can't see room activity). `is_bed` flag on room items further accelerates sleep regen.
- **D-09:** HP and stamina recover on the same system (same rates, same commands).
- **D-10:** Regen rates: Passive 1% per 10s, Rest/sit 3% per 10s, Sleep 6% per 10s, Sleep+bed 10% per 10s.
- **D-11:** Medic NPCs in towns: heal for Scales + blessings system with 1-2 minute cooldowns between blessings.
- **D-12:** Four blessing types: Heal (restore HP), Fortify (temp defense buff), Vigor (temp offense buff), Purify (cleanse all negative status effects). Blessings last 5-10 minutes for buffs.

### Item Stat Display
- **D-13:** Basic item description always visible on `look`. Full mechanical stats (damage, armor, bonuses, quality, value) require appraisal skill check OR vendor `view` command.
- **D-14:** Dedicated `compare <item1> <item2>` command for side-by-side stat comparison.

### Social Systems
- **D-15:** OOC global channel — server-wide out-of-character chat.
- **D-16:** Zone-wide `shout` command — in-character, heard by everyone in same zone. Costs stamina to prevent spam.
- **D-17:** `whisper <player> <msg>` — in-room private. Others see "X whispers something to Y."
- **D-18:** Domain channel — all members of the same primary domain specialization can chat (e.g., all Subterfuge-domain characters). NOT a player organization system.
- **D-19:** `who` command showing online players with name, ancestry, guild/domain, current zone.

### Claude's Discretion
- Exact blessing Scales cost (should scale with character progression or be flat)
- Appraisal skill DC formula (how hard is it to appraise items of different quality)
- OOC channel implementation (Evennia's built-in channel system vs custom)
- Shout stamina cost amount
- Whether vendor `view` bypasses appraisal requirement (yes — vendors know their own stock)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Economy & Currency
- `world/banking.py` — Atomic F() currency operations; get_balance, deposit, withdraw patterns
- `world/areas/equipment_catalog.py` — 69+ items with value fields; canonical item stock for vendors
- `world/inventory_engine.py` — Authoritative item operations (pickup, drop, equip, transfer)
- `world/models.py` — InventoryItem model, BankAccount model

### Combat & Recovery
- `world/combat_engine.py` — handle_player_death(), handle_mob_death(); HP stored in ndb.hp
- `world/status_effects.py` — apply_effect(), clear_all_effects(); status effect application API
- `world/base_attributes.py` — derive_max_hp(), derive_max_stamina(); stat derivation functions
- `world/ability_engine.py` — Existing consumable use via `_consume_item()` pattern

### Items & Stats
- `typeclasses/objects.py` — SoravelonItem, SoravelonEquipment; return_appearance() hooks
- `world/item_spawner.py` — create_item_from_template(); item definition dict schema
- `world/skill_engine.py` — get_skill_value() for appraisal checks

### Social
- `typeclasses/channels.py` — Existing (empty) channel typeclass extending DefaultChannel
- `commands/cmd_dialogue.py` — Existing say/tell/ask pattern; MAX_DIALOGUE_LENGTH cap
- `commands/default_cmdsets.py` — Where new commands must be registered

### Area Content
- `world/areas/vaels_crossing.py` — Shop rooms (mk_*), medic building (iq_medic_building), merchant NPCs
- `.claude/skills/base/skill.md` — Critical rules (return tuples, atomic updates, OOB through publisher)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/banking.py` deposit/withdraw pattern — reusable for vendor transactions (F() atomicity)
- `world/inventory_engine.py` pick_up/drop — reusable for buy/sell item transfer
- `commands/cmd_bank.py` — command structure pattern for financial operations
- `world/status_effects.py` apply_effect() — reusable for blessing buffs
- `typeclasses/channels.py` Channel class — Evennia's built-in channel system, extends DefaultChannel
- `world/oob_publisher.py` push_stat_update — for pushing HP changes to client during regen

### Established Patterns
- Commands dispatch to world/ engine modules (never contain game logic)
- All engine functions return (bool, str) tuples
- Currency uses atomic F() expressions
- Items tracked in InventoryItem Django model
- NPC detection via SoravelonMob typeclass + db.is_npc flag
- Room-based NPC lookup via _find_npc_in_room() in cmd_dialogue.py

### Integration Points
- New commands register in commands/default_cmdsets.py CharacterCmdSet
- Vendor NPCs already placed in Vaels Crossing shop rooms
- Equipment catalog already defines item prices via `value` field
- Medic building exists (iq_medic_building) with respawn_point tag
- Domain scores on character.db.domain_scores — used for domain channel membership

</code_context>

<specifics>
## Specific Ideas

- Vendor `view` command should show full stats even without appraisal skill — vendors know their own inventory
- Shout costs stamina to prevent spam — thematic (shouting is physically taxing)
- Sleep blinds the player — they literally can't see room descriptions or who enters/exits. Creates vulnerability/risk tradeoff for faster healing
- Beds (`is_bed` items/flags) in rooms like inn rooms and barracks provide the fastest recovery — incentivizes visiting safe locations
- Blessings are NOT purchasable consumables — they're applied directly by the medic NPC via the blessing command/dialogue. 1-2 minute cooldown prevents farming
- Domain channel is conceptually a "guild chat" but the guild system in Soravelon is class-based (domain specialization), not player organizations. Channel membership = characters sharing the same primary domain.

</specifics>

<additional_scope>
## Additional Scope (from Codex Round 2 + Round 3 audits)

### Missing Content (must author)
- **D-20:** Author 5 gathering tools as equippable items (pickaxe, sickle, hatchet, skinning_knife, fishing_rod). Implement a `tools` command (like `gear` but for tool slots). Tools must be equipped in tool slots to function — not just "in inventory." Place basic tools in starter kits and vendor shops. Tool slots are separate from combat equipment slots.
- **D-21:** Add fish gathering pools to coastal zones (stormhaven_coast at minimum). Author fishing_rod and bait items.
- **D-22:** Add missing loot table entries for "rat" and "bandit" mob types.
- **D-23:** Author item definitions for 10 crafting outputs currently falling back to generic objects: basic_healing_draught, cooked_meat, healing_draught, hearty_stew, herb_poultice, iron_chainmail, mountain_tonic, spiced_fish, stamina_tonic, trail_rations.
- **D-24:** Author 8 quest items that have no source: outstanding_debt_token, commissioned_blade, stolen_artifact, rare_herb_bundle, rare_alpine_ingredient, resonance_sample, contraband_package, warden_supplies. Add via give_item triggers, NPC dialogue, or loot tables.

### Combat System Fixes
- **D-25:** Normalize ability effect handlers to return `(bool, str)` tuples instead of bare strings (F7). Thread success flag through `_post_ability_resource_hook`.
- **D-26:** Implement compound status effect behavior: steam burst damage, discharge burst, petrify break-on-damage (F12). Set `took_damage_this_round` flag in combat damage resolution.
- **D-27:** Add custom corpse loot command that respects CorpseContainer.can_loot() phases instead of blanket "get:false()" lock (3.12).
- **D-28:** Implement real group loot distribution logic for at least "personal" and "round_robin" modes (3.9). Wire into corpse/item creation path.

</additional_scope>

<deferred>
## Deferred Ideas

- Player organization/clan system — user explicitly deferred this. Domain channel covers class-based social for now.
- Auction house / player-to-player trading — natural extension of vendor system but separate phase.
- Item enchanting / upgrade system — would interact with vendor economy but separate scope.
- NPC schedules / shop hours — merchants could have working hours, adding life. Future content.

</deferred>

---

*Phase: 15-implement-missing-gameplay-gap-systems*
*Context gathered: 2026-04-04*
