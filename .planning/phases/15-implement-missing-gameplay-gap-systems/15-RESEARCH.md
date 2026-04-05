# Phase 15: Implement Missing Gameplay Gap Systems - Research

**Researched:** 2026-04-04
**Domain:** Gameplay systems (vendor economy, HP recovery, item inspection, social, content gaps, combat fixes)
**Confidence:** HIGH

## Summary

Phase 15 fills the remaining gaps to make Soravelon fully playable end-to-end. The scope splits into four major domains: (1) new gameplay systems (vendor/shop, HP/stamina recovery, item inspection, social channels), (2) missing content authoring (gathering tools, fish pools, quest items, crafting outputs, loot tables), (3) combat system fixes (ability return types, compound effects, corpse loot command, group loot distribution), and (4) social commands (who, shout, whisper, OOC channel, domain channel).

All four domains have strong existing infrastructure to build on. The vendor system reuses banking.py's atomic F() pattern and inventory_engine.py's item transfer. HP recovery builds on the existing ndb.hp/ndb.stamina volatile state with derive_max_hp/derive_max_stamina from base_attributes.py. Social channels leverage Evennia's built-in DefaultChannel with the existing empty Channel typeclass in typeclasses/channels.py. Combat fixes are surgical -- the code is already structured correctly, just missing the (bool, str) return normalization and compound effect behavior implementations.

**Primary recommendation:** Organize into 5-6 plans: (1) vendor engine + commands, (2) HP/stamina recovery + rest/sleep + medic blessings, (3) item inspection + compare, (4) social systems (channels, who, shout, whisper), (5) missing content authoring (tools, fish pools, quest items, crafting outputs, loot tables), (6) combat system fixes (ability returns, compound effects, corpse loot, group loot).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Fixed prices for general vendors. Faction vendors adjust prices based on standing.
- **D-02:** Commands: `buy <item>`, `sell <item>`, `appraise <item>`, `list`, `view <item>`.
- **D-03:** Vendors are type-restricted via `db.vendor_accepts` tag list. Quest items blocked from sale.
- **D-04:** Sell-back returns 33% of item value. Sold items appear in shop stock at full price.
- **D-05:** Unlimited base stock from equipment_catalog. Player-sold items also appear.
- **D-06:** Three-tier recovery: passive regen (always out-of-combat), rest/sit (accelerated), sleep (fastest but blinds).
- **D-07:** `rest` command (alias: `sit`) -- accelerated regen, interrupted by combat or movement.
- **D-08:** `sleep` command -- fastest regen but player blind. `is_bed` flag further accelerates.
- **D-09:** HP and stamina recover on the same system (same rates, same commands).
- **D-10:** Regen rates: Passive 1%/10s, Rest 3%/10s, Sleep 6%/10s, Sleep+bed 10%/10s.
- **D-11:** Medic NPCs: heal for Scales + blessings with 1-2 minute cooldowns.
- **D-12:** Four blessings: Heal (HP), Fortify (defense), Vigor (offense), Purify (cleanse). 5-10 min buffs.
- **D-13:** Basic item desc on `look`. Full stats require appraisal skill check OR vendor `view`.
- **D-14:** `compare <item1> <item2>` for side-by-side stat comparison.
- **D-15:** OOC global channel -- server-wide out-of-character chat.
- **D-16:** Zone-wide `shout` -- in-character, costs stamina.
- **D-17:** `whisper <player> <msg>` -- in-room private, others see notification.
- **D-18:** Domain channel -- same primary domain specialization members can chat.
- **D-19:** `who` command -- online players with name, ancestry, guild/domain, current zone.
- **D-20:** Author 5 gathering tools as equippable items (pickaxe, sickle, hatchet, skinning_knife, fishing_rod). `tools` command. Tool slots separate from combat equipment.
- **D-21:** Fish gathering pools in coastal zones (stormhaven_coast minimum). Fishing rod + bait items.
- **D-22:** Missing loot table entries for "rat" and "bandit" mob types.
- **D-23:** Author 10 crafting output item definitions (basic_healing_draught, cooked_meat, healing_draught, hearty_stew, herb_poultice, iron_chainmail, mountain_tonic, spiced_fish, stamina_tonic, trail_rations).
- **D-24:** Author 8 quest items with sources (outstanding_debt_token, commissioned_blade, stolen_artifact, rare_herb_bundle, rare_alpine_ingredient, resonance_sample, contraband_package, warden_supplies).
- **D-25:** Normalize ability effect handlers to return `(bool, str)` tuples (F7).
- **D-26:** Implement compound status effect behavior: steam burst, discharge burst, petrify break-on-damage (F12).
- **D-27:** Custom corpse loot command respecting CorpseContainer.can_loot() phases (3.12).
- **D-28:** Real group loot distribution for "personal" and "round_robin" modes (3.9).

### Claude's Discretion
- Exact blessing Scales cost (should scale with character progression or be flat)
- Appraisal skill DC formula (how hard is it to appraise items of different quality)
- OOC channel implementation (Evennia's built-in channel system vs custom)
- Shout stamina cost amount
- Whether vendor `view` bypasses appraisal requirement (yes -- vendors know their own stock)

### Deferred Ideas (OUT OF SCOPE)
- Player organization/clan system
- Auction house / player-to-player trading
- Item enchanting / upgrade system
- NPC schedules / shop hours
</user_constraints>

## Architecture Patterns

### Recommended Project Structure (new files)
```
world/
  vendor_engine.py       # Vendor economy logic (buy/sell/appraise/list)
  recovery_engine.py     # HP/stamina regen (passive, rest, sleep, blessings)
commands/
  cmd_vendor.py          # CmdBuy, CmdSell, CmdAppraise, CmdList, CmdView
  cmd_recovery.py        # CmdRest, CmdSleep, CmdWake
  cmd_social.py          # CmdWho, CmdShout, CmdWhisper
  cmd_inspect.py         # CmdInspect (appraisal), CmdCompare
  cmd_tools.py           # CmdTools (tool slot management)
  cmd_loot.py            # CmdLoot (corpse looting)
typeclasses/
  channels.py            # OOC + Domain channel subclasses (extend existing)
```

### Pattern 1: Vendor Engine (reuses banking.py atomic pattern)
**What:** Vendor transactions use the same F() atomic pattern as banking for currency safety.
**When to use:** All buy/sell operations.
**Example:**
```python
# world/vendor_engine.py
def buy_item(character, vendor_npc, item_id):
    """Buy item from vendor. Returns (bool, str)."""
    # 1. Resolve item from vendor stock (equipment_catalog or player-sold)
    # 2. Check character has enough carried_scales
    # 3. Atomic: deduct carried_scales, create item via item_spawner
    # 4. Track player-sold items via vendor_npc.db.player_stock
    carried = getattr(character.db, 'carried_scales', 0) or 0
    if carried < price:
        return False, f"You need {price} Scales but only have {carried}."
    character.db.carried_scales = carried - price
    item = create_item_from_template(item_def, location=character)
    return True, f"You purchase {item.key} for {price} Scales."

def sell_item(character, vendor_npc, item):
    """Sell item to vendor. Returns (bool, str)."""
    # 1. Check vendor_accepts type restriction
    # 2. Block quest items (is_quest_item flag)
    # 3. Calculate sell price (33% of item value)
    # 4. Give character Scales, move item to vendor stock
```

### Pattern 2: Recovery Tick System
**What:** A tick-driven regen system using Evennia's delay() for periodic HP/stamina recovery.
**When to use:** Passive regen (always out of combat), accelerated via rest/sleep state.
**Key detail:** Recovery state stored on `character.ndb.recovery_state` (volatile). States: "active" (default/passive), "resting", "sleeping". Combat interrupts all non-passive recovery.
```python
# character.ndb.recovery_state = "active"|"resting"|"sleeping"
# Tick every 10 seconds, check state, apply % of max HP/stamina
REGEN_RATES = {
    "active": 0.01,    # 1% per 10s (out of combat only)
    "resting": 0.03,   # 3% per 10s
    "sleeping": 0.06,  # 6% per 10s
    "sleeping_bed": 0.10,  # 10% per 10s
}
```

### Pattern 3: Evennia Channel System for OOC/Domain
**What:** Use Evennia's built-in DefaultChannel system for OOC and domain channels.
**Why standard:** Evennia already handles channel subscription, nick aliases, message distribution, muting, banning. No need to hand-roll.
**Implementation:**
```python
# In typeclasses/channels.py
class OOCChannel(Channel):
    """Server-wide out-of-character chat."""
    channel_prefix_string = "[|wOOC|n] "

class DomainChannel(Channel):
    """Domain-specific channel. Members share primary domain."""
    channel_prefix_string = "[|c{channelname}|n] "
    
    def at_pre_channel_msg(self, message, **kwargs):
        # Verify sender's primary domain matches channel
        sender = message.senders[0] if message.senders else None
        if sender and not self._check_domain_membership(sender):
            return False
```

### Pattern 4: NPC Vendor Detection
**What:** Vendor NPCs identified by `db.is_vendor = True` and `db.vendor_accepts` list on mob objects.
**When to use:** All vendor commands need to locate the vendor NPC in the room.
**Integration:** Uses same `_find_npc_in_room()` pattern from cmd_dialogue.py.

### Anti-Patterns to Avoid
- **Direct character.msg() for OOB:** Always use oob_publisher for stat pushes (HP/stamina changes during regen must go through push_stat_update).
- **Read-modify-write for currency:** Always use carried_scales direct assignment (not banked balance -- carried_scales is ndb-style on db, no F() needed for single-player carried amount).
- **Game logic in commands:** Commands call into world/ engine modules per established convention.
- **Hardcoded tool checks:** Tools matched via item_tag category, not hardcoded item names.
- **Blocking sleep regen on server restart:** Recovery state is ndb (volatile) -- after restart, characters default to "active" state. This is correct behavior.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Chat channels | Custom message routing | Evennia DefaultChannel | Built-in subscription, muting, banning, nick aliases |
| Currency transactions | Manual balance math | Existing banking.py F() pattern | Race-condition-safe atomicity |
| Item creation | Manual object creation | item_spawner.create_item_from_template() | Handles typeclass selection, db attrs, item_tag |
| Item transfer | Manual location changes | inventory_engine.pick_up/drop | Keeps InventoryItem Django model in sync |
| Status effect buffs | Custom buff tracking | status_effects.apply_effect() | Already handles stacking, duration, modifiers |
| Skill checks | Manual random rolls | skill_engine.get_skill_value() | Handles diminishing returns, passive use tracking |

## Common Pitfalls

### Pitfall 1: Vendor Carried Scales vs Banked Balance
**What goes wrong:** Using banking.py withdraw/deposit for vendor purchases.
**Why it happens:** Banking uses F() for banked balance, but vendors deal in carried_scales (character.db attribute).
**How to avoid:** Vendor buy/sell operates on `character.db.carried_scales` directly. Only use banking.py if the vendor accepts bank drafts (not in scope).
**Warning signs:** Seeing `BankAccount.objects.filter` in vendor code.

### Pitfall 2: Recovery Tick Leak
**What goes wrong:** Regen ticks continue running after character disconnects or enters combat.
**Why it happens:** delay() callbacks persist across state changes.
**How to avoid:** Store the delay handle on ndb (auto-cleared on disconnect). Check combat state at tick time. Cancel tick on combat entry.
**Warning signs:** HP increasing during combat, or errors in logs after disconnect.

### Pitfall 3: Tool Slot vs Equipment Slot Confusion
**What goes wrong:** Tool equip/unequip interfering with combat equipment system.
**Why it happens:** D-20 says tool slots are SEPARATE from combat equipment slots.
**How to avoid:** Tools use a separate `character.db.equipped_tools` dict (not the `character.db.equipped` dict used by combat gear). Tool equip_slot values like "tool_pickaxe" must NOT overlap with SoravelonEquipment.VALID_SLOTS.
**Warning signs:** Equipping a pickaxe unequips a weapon, or vice versa.

### Pitfall 4: Ability Handler Return Type Mismatch
**What goes wrong:** _post_ability_resource_hook treats `result` as boolean, but handlers return bare strings.
**Why it happens:** Handlers were originally stubs returning descriptive text. The hook checks `if result:` which is truthy for non-empty strings -- currently works by accident but is fragile.
**How to avoid:** Each handler in EFFECT_HANDLERS must return `(bool, str)`. Update _post_ability_resource_hook to unpack `ok, msg = result`. Update use_ability to return the msg part.
**Warning signs:** Resource builders not triggering on failed abilities (currently broken silently).

### Pitfall 5: Corpse Lock Bypass via Default `get` Command
**What goes wrong:** Players use Evennia's default `get` command on items inside corpses, bypassing can_loot() phase checks.
**Why it happens:** CorpseContainer has `get:false()` lock which blocks picking up the CORPSE, but items inside it can still be accessed.
**How to avoid:** D-27 requires a custom `loot` command that explicitly calls can_loot(). Lock items inside corpse with `get:false()` too, or override at_pre_get on the corpse to block unauthorized access.
**Warning signs:** Any player able to take items from a locked-phase corpse.

### Pitfall 6: Shout Zone Scope
**What goes wrong:** Shout reaches all players on server, or only players in same room.
**Why it happens:** Need to determine "same zone" from room tags.
**How to avoid:** Use room's zone_id tag to find all rooms in zone, then all characters in those rooms. This is a heavier query -- consider caching zone membership or using Evennia's search_tag.
**Warning signs:** Shout heard across zones, or not heard in adjacent rooms of same zone.

## Code Examples

### Vendor NPC Detection Pattern
```python
# Reuse from cmd_dialogue.py pattern
def _find_vendor_in_room(character):
    """Find a vendor NPC in the character's current room."""
    from typeclasses.mobs import SoravelonMob
    for obj in character.location.contents:
        if isinstance(obj, SoravelonMob) and obj.db.is_vendor:
            return obj
    return None
```

### Vendor Stock Resolution
```python
def get_vendor_stock(vendor_npc):
    """Return combined stock: equipment_catalog base + player-sold items."""
    from world.areas.equipment_catalog import CATALOG  # item_defs dict
    accepts = vendor_npc.db.vendor_accepts or []
    
    # Base stock: filter equipment_catalog by vendor type
    base_stock = {k: v for k, v in CATALOG.items() 
                  if v.get("item_type") in accepts}
    
    # Player-sold items
    player_stock = vendor_npc.db.player_stock or {}
    
    return {**base_stock, **player_stock}
```

### Recovery Regen Tick
```python
def _regen_tick(character):
    """Called every 10 seconds. Apply HP/stamina regen based on state."""
    from world.base_attributes import derive_max_hp, derive_max_stamina
    from world.oob_publisher import push_stat_update
    
    # Skip if in combat
    if getattr(character.ndb, 'combat_handler', None):
        return
    
    state = getattr(character.ndb, 'recovery_state', 'active')
    
    # Check bed bonus for sleeping
    if state == "sleeping":
        room_has_bed = _room_has_bed(character.location)
        rate = REGEN_RATES["sleeping_bed"] if room_has_bed else REGEN_RATES["sleeping"]
    else:
        rate = REGEN_RATES.get(state, REGEN_RATES["active"])
    
    max_hp = derive_max_hp(character)
    max_stamina = derive_max_stamina(character)
    hp_gain = int(max_hp * rate) or 1
    stamina_gain = int(max_stamina * rate) or 1
    
    changed = False
    if (character.ndb.hp or 0) < max_hp:
        character.ndb.hp = min(max_hp, (character.ndb.hp or 0) + hp_gain)
        changed = True
    if (character.ndb.stamina or 0) < max_stamina:
        character.ndb.stamina = min(max_stamina, (character.ndb.stamina or 0) + stamina_gain)
        changed = True
    
    if changed:
        push_stat_update(character)
    
    # Schedule next tick if not at full
    if (character.ndb.hp or 0) < max_hp or (character.ndb.stamina or 0) < max_stamina:
        from evennia.utils import delay
        character.ndb.regen_handle = delay(10, _regen_tick, character)
```

### Ability Handler Return Normalization (D-25)
```python
# BEFORE (current -- returns bare string):
def _handle_damage(character, ability, target):
    ok, msg, dmg = resolve_ability_damage(character, ability, target)
    return msg  # bare string

# AFTER (normalized -- returns (bool, str)):
def _handle_damage(character, ability, target):
    ok, msg, dmg = resolve_ability_damage(character, ability, target)
    return ok, msg  # (bool, str) tuple
```

### Compound Effect Behavior (D-26)
```python
# In status_effects.py tick_effects():
# Steam: burst damage on creation, then armor reduction
elif etype == "steam":
    if entry.get("duration") == entry.get("initial_duration", 3):
        # First tick -- burst damage (15% max HP)
        burst = int((target.ndb.hp or 0) * 0.15)
        target.ndb.hp = max(0, (target.ndb.hp or 0) - burst)
        messages.append(f"Steam scalds for {burst} damage!")

# Discharge: burst damage on creation
elif etype == "discharge":
    if entry.get("duration") == entry.get("initial_duration", 3):
        burst = int((target.ndb.hp or 0) * 0.20)
        target.ndb.hp = max(0, (target.ndb.hp or 0) - burst)
        messages.append(f"Electrical discharge deals {burst} damage!")

# Petrify: break on damage (already partially implemented)
elif etype == "petrify":
    took_damage = getattr(target.ndb, "took_damage_this_round", False)
    if took_damage:
        messages.append("Petrify shatters from damage!")
        continue  # remove from surviving
```

### Custom Corpse Loot Command (D-27)
```python
class CmdLoot(Command):
    """Loot items from a corpse. Respects corpse loot phases."""
    key = "loot"
    locks = "cmd:all()"
    
    def func(self):
        character = self.caller
        # Find corpse in room
        corpse = self._find_corpse(character)
        if not corpse:
            character.msg("There is nothing to loot here.")
            return
        
        # Check loot phase via can_loot()
        ok, msg = corpse.can_loot(character)
        if not ok:
            character.msg(f"|r{msg}|n")
            return
        
        # Transfer all items from corpse to character
        from world.inventory_engine import pick_up
        for item in list(corpse.contents):
            success, result_msg = pick_up(character, item)
            if success:
                character.msg(f"|gYou loot {item.key}.|n")
        
        # Transfer Scales
        corpse_scales = corpse.db.scales or 0
        if corpse_scales > 0:
            character.db.carried_scales = (character.db.carried_scales or 0) + corpse_scales
            corpse.db.scales = 0
            character.msg(f"|gYou loot {corpse_scales} Scales.|n")
```

## Discretion Recommendations

### Blessing Scales Cost
**Recommendation:** Flat cost, scaling mildly with blessing tier. Heal: 20 Scales, Fortify: 30, Vigor: 30, Purify: 40. Rationale: players need predictable costs; scaling with progression creates a moving target that's hard to balance. Flat rates are the MMO standard for NPC healer services.

### Appraisal Skill DC Formula
**Recommendation:** DC = (item_rarity_number * 15) + (material_tier * 5). Normal=0, Magic=15, Rare=30, Legendary=45, plus tier 1-5 adding 5-25. Success = skill_value >= DC. This makes common items trivially easy to appraise and legendary items require high skill.

### OOC Channel Implementation
**Recommendation:** Use Evennia's built-in channel system. Create an OOCChannel subclass in typeclasses/channels.py. Add to DEFAULT_CHANNELS in settings.py so it auto-creates on server start. Accounts auto-subscribe on first login. This is zero custom code for message routing.

### Shout Stamina Cost
**Recommendation:** 10 stamina per shout. High enough to prevent spam (at base 30+ stamina), low enough to not punish legitimate use. Recovery at passive rate means ~100 seconds to recover the cost.

### Vendor `view` Bypasses Appraisal
**Recommendation:** Yes -- vendors know their own stock. `view <item>` in a vendor room shows full stats regardless of appraisal skill. This is explicitly stated in CONTEXT.md specifics.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Ability handlers return bare strings | Must return (bool, str) tuples | Phase 15 fix | All 10 effect handlers need updating |
| Corpse items accessible via default `get` | Custom `loot` command gates access | Phase 15 | Prevents loot theft during grace period |
| No HP recovery system | Tick-based passive + rest + sleep | Phase 15 | Core gameplay loop complete |
| No vendor economy | Vendor buy/sell/appraise/list | Phase 15 | Economy loop closed |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | unittest.TestCase + MagicMock (pure logic), EvenniaTestCase (DB-dependent) |
| Config file | Tests run via `evennia test --settings server.conf.settings tests/` or `pytest` |
| Quick run command | `pytest tests/test_<module>.py -x` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| D-01/D-05 | Vendor buy/sell/stock | unit | `pytest tests/test_vendor_engine.py -x` | Wave 0 |
| D-06/D-10 | HP/stamina regen rates | unit | `pytest tests/test_recovery_engine.py -x` | Wave 0 |
| D-11/D-12 | Medic blessings | unit | `pytest tests/test_recovery_engine.py -x` | Wave 0 |
| D-13/D-14 | Item appraisal + compare | unit | `pytest tests/test_inspect.py -x` | Wave 0 |
| D-15/D-18 | Channel creation + messaging | unit | `pytest tests/test_social.py -x` | Wave 0 |
| D-25 | Ability return normalization | unit | `pytest tests/test_ability_engine.py -x` | Exists (update) |
| D-26 | Compound effect behavior | unit | `pytest tests/test_status_effects.py -x` | Exists (update) |
| D-27 | Corpse loot phases | unit | `pytest tests/test_loot.py -x` | Wave 0 |
| D-28 | Group loot distribution | unit | `pytest tests/test_group_engine.py -x` | Exists (update) |

### Sampling Rate
- **Per task commit:** `pytest tests/test_<changed_module>.py -x`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_vendor_engine.py` -- covers D-01 through D-05
- [ ] `tests/test_recovery_engine.py` -- covers D-06 through D-12
- [ ] `tests/test_inspect.py` -- covers D-13, D-14
- [ ] `tests/test_social.py` -- covers D-15 through D-19
- [ ] `tests/test_loot.py` -- covers D-27

## Open Questions

1. **Equipment Catalog Access Pattern**
   - What we know: equipment_catalog.py defines items via area.item() during build(). Items are stored on zone_obj.db.item_definitions after build runs.
   - What's unclear: How to access item definitions at runtime without rebuilding the zone. May need to extract the item_def dicts into a standalone registry constant or cache.
   - Recommendation: Extract item definitions from equipment_catalog.py into a module-level CATALOG dict that can be imported directly, separate from the AreaBuilder build process.

2. **Regen Tick Lifecycle Management**
   - What we know: ndb is cleared on disconnect. delay() handles persist across some state changes.
   - What's unclear: Whether Evennia's delay() handles survive server reload (hot-reload). If not, regen must be re-started on login.
   - Recommendation: Start regen tick at login (at_post_login) and let ndb cleanup handle disconnect. Check at tick time for combat state.

3. **Domain Channel Membership Tracking**
   - What we know: Primary domain stored on character.db.domain_scores (dict). DefaultChannel handles subscriptions.
   - What's unclear: When a character's primary domain changes (unlikely but possible), should channel membership auto-update?
   - Recommendation: Check domain membership at message send time (at_pre_channel_msg) rather than on subscription. Simpler, no tracking needed.

## Sources

### Primary (HIGH confidence)
- Codebase inspection: world/banking.py, world/inventory_engine.py, world/ability_engine.py, world/status_effects.py, world/combat_engine.py, world/crafting_engine.py, world/gathering_engine.py, world/group_engine.py, world/loot_tables.py, world/item_spawner.py, typeclasses/objects.py, typeclasses/channels.py, commands/default_cmdsets.py, commands/cmd_gathering.py, world/areas/equipment_catalog.py, world/areas/vaels_crossing.py
- [Evennia Channels docs](https://www.evennia.com/docs/latest/Components/Channels.html) -- DefaultChannel API, channel creation, DEFAULT_CHANNELS setting

### Secondary (MEDIUM confidence)
- [Evennia wiki - Customize channels](https://github.com/evennia/evennia/wiki/Customize-channels)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all systems build on existing codebase patterns
- Architecture: HIGH -- patterns verified against existing world/ engine modules
- Pitfalls: HIGH -- identified from actual code inspection (not theoretical)

**Research date:** 2026-04-04
**Valid until:** 2026-05-04 (stable -- no external dependencies changing)
