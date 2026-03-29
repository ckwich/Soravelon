# Phase 7: Milestone 1 Content - Research

**Researched:** 2026-03-29
**Domain:** Content authoring via AreaBuilder DSL, mob templates, equipment catalog, node system integration
**Confidence:** HIGH

## Summary

Phase 7 is a massive content-authoring phase: ~500+ rooms across 5 zones (Vael's Crossing hub + 4 starter zones), 50+ equipment items, mob templates with loot tables, NPC dialogue, and one node zone with Layer 1 rooms. All content is authored as Python zone spec files in `world/areas/` using the existing AreaBuilder DSL. The DSL, spawner, dialogue engine, combat AI, ability registry, crafting system, and node system are all built and tested from prior phases.

The primary technical risk is not the DSL (which is solid) but three infrastructure gaps that must be closed before bulk content authoring begins: (1) a mob template registry to map mob keys to full stat blocks (abilities, HP ranges, damage, aggression, mob_type, etc.) since `spawn_single_mob` currently only sets a few attributes from spawn_def, (2) expansion of the equipment slot system from the current 7 slots to the 13 required by D-37, and (3) a wandering mob system (D-27) since only the `wander` flag on NPC defs exists with no implementation. Once these three gaps are closed, the rest is creative content authoring using well-established patterns.

**Primary recommendation:** Structure the phase as infrastructure-first (mob templates, equipment slots, wander system), then content waves (hub city first, then zones in parallel), then integration (node zone, loot tables, trainer registry, character spawn location).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Vael's Crossing is 100+ rooms on Varath (eastern continent). Dark frontier outpost aesthetic. User override of vault World Bible Hub 1 location.
- **D-02:** "Vael's Crossing" is the final name.
- **D-03:** Bustling metropolis feel with 50+ NPCs and quest stub threads everywhere.
- **D-04:** 6-8 districts (~15-25 rooms each) covering all services. Must include guild quarter, market, residential, dock/gate area.
- **D-05:** Unsafe edges -- core city safe, outskirts/sewers/back alleys have low-level threats. Hidden underworld district with mob spawns.
- **D-06:** Thematic named paths connect to starter zones (e.g., "The Ashway", "Harbor Road").
- **D-07:** Single Dragon Courier flight point. Full Consortium bank branch.
- **D-08:** All 10 guild halls present.
- **D-09:** Empire + Consortium + Wardens faction presence with formal offices. Other factions via NPCs.
- **D-10:** 3-5 atmospheric landmarks.
- **D-11:** New player onboarding: arrive at specific room with greeter NPC.
- **D-12:** One crafting station of each type.
- **D-13:** Skill trainer NPCs for TRAINER_REGISTRY.
- **D-14:** Medic building as death respawn point.
- **D-15:** City vendors sell basic starter weapons/armor AND basic consumable potions.
- **D-16:** All content invented fresh, but scan ALL vault files for naming/geography/faction conventions.
- **D-17:** 4 starter zones, 100+ rooms each. 4 distinct biomes using Varath geography.
- **D-18:** NO LEVELS -- zone scaling makes all content appropriate for all players.
- **D-19:** Moderate mob density: 1-2 spawns per 2 rooms.
- **D-20:** One named mob (mini-boss) per zone with unique loot and zone-wide respawn announcement.
- **D-21:** Mob rarity through affix system, not separate spawn definitions.
- **D-22:** 1-3 field NPCs per zone with dialogue and quest hook stubs.
- **D-23:** Quest stubs only -- NPCs reference quests but system stays stubbed.
- **D-24:** Both crafting materials AND lore fragments in each zone.
- **D-25:** Connected network -- zones connect to city AND to each other.
- **D-26:** Flight points in city only for M1.
- **D-27:** Some mobs wander (random movement). If system doesn't exist, implement it.
- **D-28:** 1-2 is_hunter mobs per zone (BFS chase within detection range).
- **D-29:** Zone attunement active from start.
- **D-30:** Some room state flags alter descriptions (visible), others discoverable by Sense.
- **D-31:** 3-5 base mob types per zone, themed to biome.
- **D-32:** 50+ item equipment catalog. Ranged weapons flavor only.
- **D-33:** Soft stat requirements -- weapons work for anyone but scale better with matching stats.
- **D-34:** Three sources: city vendors, mob drops, crafting.
- **D-35:** 2-3 material tiers with scaling stats (iron -> steel -> mithril or similar).
- **D-36:** Ignore equipment weight for M1.
- **D-37:** 13 equipment slots: head, face, chest, back, hands, wrists, legs, feet, main hand, off hand, ring x2, amulet.
- **D-38:** Two-handed weapons use both hand slots, higher damage.
- **D-39:** Shields are passive armor in off-hand.
- **D-40:** Equipment provides small stat bonuses.
- **D-41:** No durability/degradation for M1.
- **D-42:** Weapon damage: damage_min/damage_max + stat scaling + zone scaling multiplier.
- **D-43:** No set bonuses. No procedural affixes (CON-04).
- **D-44:** Vendor consumables alongside crafting outputs.
- **D-45:** Claude picks which zone gets active node.
- **D-46:** Complete transformation when node collapses -- Layer 1 rooms fundamentally different.
- **D-47:** Partial overlay -- only rooms near node center get Layer 1 versions.
- **D-48:** Unique corrupted mob variants spawn only in Layer 1.
- **D-49:** Node failure follows NodeScript tick-driven progression.
- **D-50:** Layer 1 has exclusive lore fragments for Remnance/Echoes domain.
- **D-51:** Interactive stabilization mechanic for players.
- **D-52:** Claude picks node type from VALID_NODE_TYPES based on zone theme.

### Claude's Discretion
- District names and internal layout of Vael's Crossing
- Zone names, biome themes, and geographic placement on Varath
- Specific NPC names, dialogue content, and quest stub descriptions
- Mob type designs (species, abilities, behavior) per zone theme
- Equipment item names, stat values, and material tier progression
- Landmark designs and placement in the city
- Node zone selection and Layer 1 room design
- Number of rooms in Layer 1 overlay
- Wandering mob implementation approach

### Deferred Ideas (OUT OF SCOPE)
- Active shield block mechanic
- Equipment durability/degradation system
- Equipment set bonuses
- Cross-room ranged combat system
- Full quest system implementation (M1 has stubs only)
- Western continent (Sorath) hub cities and zones
- PvP combat
- Procedural equipment affixes (explicitly excluded by CON-04)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CON-01 | Hub City 1 (Vael's Crossing) authored via GUI builder with full services | AreaBuilder DSL fully supports all zone spec features; 100+ rooms structured as 6-8 districts; flight point, bank, guild halls, crafting stations, vendors, trainers, greeter NPC all expressible via existing DSL methods |
| CON-02 | 3 starter zones with Layer 0 content (rooms, mobs, NPCs, quests) | AreaBuilder DSL supports room(), spawn(), npc(), quest(), material(), lore_fragment(); mob template registry needed to give spawned mobs proper stats/abilities; wandering mob system needs implementation |
| CON-03 | 1 starter zone with active node and Layer 1 implementation | node() DSL method exists; initialize_node() creates Layer 1 rooms; NodeScript tick-driven progression ready; layer_1_overrides dict supports room description overrides; corrupted mob variants need spawn_condition="node_active" |
| CON-04 | Basic equipment (weapons/armor) available without procedural affixes | Equipment typeclass exists but VALID_SLOTS needs expansion from 7 to 13; item() DSL method and create_item_from_template() handle equipment creation; loot_tables.py LOOT_TABLES dict ready for mob_type entries |
</phase_requirements>

## Standard Stack

### Core (all existing -- no new dependencies)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia | 6.0 | MUD engine | Project foundation |
| Django ORM | 5.x | Data persistence | Evennia dependency |
| Python | 3.11+ | Language | Project requirement |

### Supporting (existing project modules)
| Module | Purpose | When to Use |
|--------|---------|-------------|
| `world/area_builder.py` | Zone authoring DSL | All zone spec files |
| `world/area_validator.py` | Validation constants | Zone type, room type, direction validation |
| `world/mob_spawner.py` | Runtime mob creation | Spawn definitions -> live mobs |
| `world/item_spawner.py` | Item creation from templates | Vendor items, loot drops, crafting output |
| `world/loot_tables.py` | Mob drop resolution | Zone-specific loot tables |
| `world/dialogue_engine.py` | NPC dialogue | Standing-tier greetings, topics, hints |
| `world/crafting_definitions.py` | Recipe registry | Existing 8 recipes + new ones |
| `world/skill_definitions.py` | Trainer registry | Populate TRAINER_REGISTRY |
| `world/combat_ai.py` | Mob AI + is_hunter chase | Mob ability selection, BFS pursuit |
| `world/ability_registry.py` | 330+ abilities | Mob ability assignment |
| `world/zone_object.py` | Node initialization | Layer 1 room creation |
| `world/scripts/node_script.py` | Node failure state machine | Tick-driven failure progression |
| `world/room_state.py` | Room flags | FLAG_VOCABULARY for zone room states |

### No Alternatives Needed
This phase uses exclusively existing project infrastructure. No new libraries required.

## Architecture Patterns

### Zone Spec File Structure
```
world/areas/
  __init__.py              # empty
  vaels_crossing.py        # Hub city zone spec
  ashreach_plains.py       # Starter zone 1
  reth_foothills.py        # Starter zone 2
  cantera_edge.py          # Starter zone 3 (node zone candidate)
  northeastern_coast.py    # Starter zone 4
```

### Pattern 1: Zone Spec File Anatomy
**What:** Each zone file defines a `build()` function that uses AreaBuilder DSL
**When to use:** Every zone

```python
# Source: world/area_builder.py DSL, world/areas/*.py convention
from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder()
    area.zone("zone_id", "Zone Name",
              zone_type="plains", continent="varath",
              faction_territory="imperial",
              world_x=100, world_y=200, world_radius=50)

    # Rooms
    entrance = area.room("entrance", "Zone Entrance",
                         "Description text.",
                         room_type="path",
                         grid_x=0, grid_y=0)

    # Exits
    area.exit(entrance, next_room, "north")

    # Cross-zone exits
    area.exit(entrance, "vaels_crossing:south_gate", "west")

    # Mob spawns
    area.spawn(clearing, "ash_wolf",
               behavior=["aggressive"],
               count_min=2, count_max=3,
               respawn_minutes=10)

    # Named mob (mini-boss)
    area.named_mob("alpha_ash_wolf", boss_room,
                   respawn_minutes=120,
                   respawn_variance=30,
                   sequence=[
                       {"trigger": "hp_below_50", "action": "echo",
                        "message": "The Alpha howls, summoning its pack!"},
                       {"trigger": "hp_below_50", "action": "spawn_mob",
                        "mob": "ash_wolf", "count": 2},
                   ])

    # NPCs
    area.npc(outpost, "ranger_captain",
             key="Ranger Captain Maren",
             npc_name="Maren",
             faction="wardens",
             dialogue={
                 "greeting_tiers": {...},
                 "topics": {...},
                 "base_hints": [...],
             })

    # Items
    area.item("iron_sword",
              key="Iron Sword", item_type="equipment",
              equip_slot="main_hand",
              damage_min=8, damage_max=14,
              stat_bonuses={"strength": 1},
              weight=3.0, rarity="normal", value=25,
              desc="A sturdy iron blade.")

    # Materials, lore, quests
    area.material("iron_ore", tier=1, terrain="rocky")
    area.lore_fragment("lore_001", ruin_room,
                       text="Ancient text...",
                       discovery_method="search",
                       scholar_path="remnance",
                       insight_gain=5)
    area.quest("quest_001", quest_type="kill",
               can_share=True)

    # Flight point (city only for M1)
    area.flight_point(courier_room, "vaels_crossing_courier",
                      name="Vael's Crossing Courier Platform")

    # Node (for the chosen node zone only)
    area.node(center_room, radius=5,
              lore_fragments=["lore_node_001"],
              layer_1_overrides={
                  "entrance": {"key": "Twisted Entrance [Node Active]",
                               "desc": "Corrupted description..."},
              })

    return area.build()
```

### Pattern 2: Mob Template Registry (NEW -- must be built)
**What:** Data-driven mapping of mob keys to full stat blocks
**When to use:** Before any zone content authoring begins

```python
# Source: Pattern derived from existing ability_registry.py and spawn system analysis
# world/mob_templates.py (NEW)

MOB_TEMPLATES = {
    "ash_wolf": {
        "key": "Ash Wolf",
        "mob_type": "ash_wolf",
        "desc": "A lean wolf with grey-white fur...",
        "base_aggression": "aggressive",
        "hp_min": 60, "hp_max": 90,
        "damage_min": 6, "damage_max": 12,
        "speed": 1.2,
        "abilities": ["bite", "howl"],
        "faction": None,
        "is_hunter": False,
        "detection_range": 3,
        "flee_threshold": 15,
        "wander": False,
        "loot_table": "ash_wolf",
    },
}

def apply_mob_template(mob, template_key):
    """Apply template stats to a spawned mob."""
    template = MOB_TEMPLATES.get(template_key)
    if not template:
        return
    for attr, value in template.items():
        if attr == "key":
            continue  # key already set at creation
        setattr(mob.db, attr, value)
```

### Pattern 3: Equipment Catalog as Item Definitions
**What:** Zone spec files register equipment via `area.item()`, vendors reference item_ids
**When to use:** Equipment definition

```python
# Equipment items registered on zone_obj.db.item_definitions
area.item("iron_longsword",
          key="Iron Longsword", item_type="equipment",
          equip_slot="main_hand",
          damage_min=10, damage_max=16,
          stat_bonuses={"strength": 2},
          material_tier=1,
          weight=4.0, rarity="normal", value=40,
          desc="A standard iron longsword.",
          two_handed=False)

# Two-handed weapon
area.item("iron_greatsword",
          key="Iron Greatsword", item_type="equipment",
          equip_slot="main_hand",  # uses both slots
          two_handed=True,
          damage_min=14, damage_max=22,
          stat_bonuses={"strength": 3},
          material_tier=1,
          weight=6.0, rarity="normal", value=60,
          desc="A heavy iron greatsword requiring both hands.")

# Shield (off-hand passive armor)
area.item("iron_buckler",
          key="Iron Buckler", item_type="equipment",
          equip_slot="off_hand",
          armor_value=3,
          stat_bonuses={"endurance": 1},
          material_tier=1,
          weight=3.0, rarity="normal", value=30,
          desc="A small iron shield.")
```

### Pattern 4: Vendor NPC with Stock
**What:** NPC with item references that player can buy
**When to use:** City vendor NPCs

```python
# Vendor NPC pattern -- vendor_items is a list of item_id strings
# that reference zone_obj.db.item_definitions
area.npc(market_room, "weapons_vendor",
         key="Korven the Weaponsmith",
         npc_name="Korven",
         faction="consortium",
         vendor_items=["iron_sword", "iron_dagger", "iron_longsword"],
         dialogue={
             "greeting_tiers": {
                 "neutral": "What do you need?",
                 "friendly": "Ah, good to see you again.",
             },
             "topics": {
                 "weapons": "I carry the basics. Good iron, honest work.",
                 "custom": "Custom orders? Maybe someday, if you bring materials.",
             },
         })
```

### Anti-Patterns to Avoid
- **Never reference levels in room/mob/NPC descriptions** -- Zone scaling makes all content appropriate for all players. No "suitable for levels 1-5" language.
- **Never hardcode mob friend/foe** -- Always use computed disposition via `base_disposition` and `base_aggression`.
- **Never invent room state flags outside FLAG_VOCABULARY** -- Add new flags to `world/room_state.py` first.
- **Never duplicate mob spawn definitions for rarity variants** -- Rarity comes from the affix roller at spawn time (D-21).
- **Never use `.append()` on db attributes** -- Always use SaverDict copy pattern: `current = list(room.db.X or []); current.append(y); room.db.X = current`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Room creation | Custom room creation code | `area.room()` | Idempotent tag-based lookup, grid coords |
| Mob spawning | Direct `create_object()` calls | `area.spawn()` + `mob_spawner.spawn_zone()` | Handles respawn timers, affix rolling, combat stats |
| Item creation | Direct object creation | `area.item()` + `item_spawner.create_item_from_template()` | Typeclass selection, attribute setup |
| NPC dialogue | Custom message handling | `area.npc(dialogue={...})` + dialogue_engine | Standing-tier greetings, topic resolution |
| Node failure | Custom state machine | `area.node()` + NodeScript | Tick-driven, Layer 1 room creation, player transport |
| Cross-zone exits | Manual exit wiring | `area.exit(r1, "zone:room", dir)` | Two-pass loading resolves load order |
| Loot resolution | Custom drop logic | `loot_tables.roll_loot()` | Skill-based tiers, rarity modifiers |
| Mob rarity | Separate rare mob spawns | Affix system `mob_affix_roller` | Automatic rarity roll, pack spawning |

**Key insight:** The AreaBuilder DSL was purpose-built for this phase. Every major content primitive has a DSL method. The only new code needed is infrastructure that bridges gaps between existing systems (mob templates, equipment slots, wander system).

## Common Pitfalls

### Pitfall 1: Equipment Slot Mismatch
**What goes wrong:** Code has 7 slots (`head, body, hands, feet, right_hand, left_hand, accessory`), decisions require 13 (`head, face, chest, back, hands, wrists, legs, feet, main_hand, off_hand, ring1, ring2, amulet`).
**Why it happens:** Equipment typeclass was built with placeholder slots in Phase 3.1 before final equipment design was locked.
**How to avoid:** Update `SoravelonEquipment.VALID_SLOTS` and `can_equip()` logic BEFORE authoring any equipment items. Also update `body` -> `chest`, `right_hand` -> `main_hand`, `left_hand` -> `off_hand`, and add `face`, `back`, `wrists`, `legs`, `ring1`, `ring2`, `amulet`.
**Warning signs:** `can_equip()` returning False for valid slot names.

### Pitfall 2: Mob Template Gap
**What goes wrong:** Spawned mobs have default stats (80-120 HP, 8-14 damage, passive, no abilities, no mob_type) because spawn_single_mob only sets zone_id, base_disposition, trust_sensitive, and flee_threshold from spawn_def.
**Why it happens:** The spawn system was built as infrastructure; mob templates were deferred to content phase.
**How to avoid:** Create `world/mob_templates.py` with MOB_TEMPLATES dict. Extend `spawn_single_mob` to apply template after creation. All zone specs must reference valid template keys.
**Warning signs:** All mobs having identical stats, no abilities, no mob_type for loot table lookup.

### Pitfall 3: No Wandering Mob System
**What goes wrong:** D-27 requires mobs that wander randomly between rooms, but only NPC def has a `wander` flag with no implementation.
**Why it happens:** Patrol system handles fixed routes; random wandering is a different system.
**How to avoid:** Implement a wander tick (similar to mob_spawner.spawn_tick) that periodically moves mobs with `db.wander=True` to a random connected room. Must respect zone boundaries, combat state (don't wander mid-combat), and room access rules.
**Warning signs:** Mobs flagged as wander=True sitting in their spawn room forever.

### Pitfall 4: SaverDict/SaverList Mutation Trap
**What goes wrong:** Appending to `db.spawn_definitions`, `db.item_definitions`, etc. silently fails because Evennia SaverDict doesn't detect in-place mutations.
**Why it happens:** Evennia's `db.*` attributes use lazy-save containers that only pickle on reassignment.
**How to avoid:** Always: `current = list(room.db.X or []); current.append(y); room.db.X = current`. The AreaBuilder already follows this pattern -- zone spec code should never manipulate db attrs directly.
**Warning signs:** Data appearing to save but being empty on reload.

### Pitfall 5: Two-Handed Weapon Slot Logic
**What goes wrong:** Two-handed weapons should occupy both main_hand and off_hand, but `can_equip()` only checks one slot.
**Why it happens:** The current equipment system has no concept of multi-slot items.
**How to avoid:** Add `db.two_handed` flag to equipment. In `can_equip()`, check both main_hand and off_hand are free. In `equip_item()`, mark both slots as occupied. In `unequip_item()`, clear both slots. Shield equip must check main_hand isn't a two-hander.
**Warning signs:** Players wielding a greatsword and a shield simultaneously.

### Pitfall 6: Loot Table mob_type Key Missing
**What goes wrong:** `roll_loot()` returns empty because `mob.db.mob_type` is None (never set by spawner).
**Why it happens:** `at_object_creation()` defaults `mob_type` to None, and spawn_single_mob never sets it.
**How to avoid:** Mob template system must set `db.mob_type` on every mob. Loot table keys must match mob_type values.
**Warning signs:** Mobs never dropping loot despite loot table entries existing.

### Pitfall 7: Cross-Zone Exit Load Order
**What goes wrong:** Zone A references a room in Zone B, but Zone B hasn't loaded yet.
**Why it happens:** `_load_all_zones()` loads files alphabetically; not all zones exist yet.
**How to avoid:** Two-pass loading (BLD-06) already implemented in `_load_all_zones()`. Deferred exits resolve in second pass. Just ensure zone file names sort in a reasonable order.
**Warning signs:** "Cross-zone exit STILL unresolved after second pass" log messages.

### Pitfall 8: Character Start Location
**What goes wrong:** New characters spawn in Limbo (Evennia default) instead of Vael's Crossing.
**Why it happens:** No `START_LOCATION` configured in settings.py.
**How to avoid:** After the greeter room is created, set `START_LOCATION` in settings.py to point to it by `#dbref` or tag lookup. Alternative: override `at_post_login` on Account to find the greeter room by tag.
**Warning signs:** New players seeing "Limbo" instead of the hub city.

### Pitfall 9: Ring Slot Duplication
**What goes wrong:** D-37 specifies "ring x2" (two ring slots) but equipment system treats slots as unique strings.
**Why it happens:** Each slot is a string; two rings need two distinct slot names.
**How to avoid:** Use `ring1` and `ring2` as distinct slot names. Equipment with `equip_slot="ring1"` vs `equip_slot="ring2"`. Consider `can_equip` logic that tries ring1 first, then ring2 if ring1 is occupied.
**Warning signs:** Players unable to wear two rings, or ring items always going to the same slot.

### Pitfall 10: Node Layer 1 Room Descriptions
**What goes wrong:** Layer 1 rooms created by `initialize_node()` get generic descriptions like "[room key] [Node Active]" instead of hand-authored corrupted descriptions.
**Why it happens:** `initialize_node()` creates Layer1Room objects with key "{original_key} [Node Active]" but doesn't set descriptions from layer_1_overrides.
**How to avoid:** The `area.node()` call stores `layer_1_overrides` dict. `build()` must pass these to `initialize_node()` which should apply overrides (key, desc) to Layer 1 rooms. Verify this path works or patch it.
**Warning signs:** Layer 1 rooms having placeholder descriptions.

## Code Examples

### Zone Spec Build Function (verified pattern from area_builder.py)
```python
from world.area_builder import AreaBuilder

def build():
    area = AreaBuilder()
    area.zone("vaels_crossing", "Vael's Crossing",
              zone_type="frontier", continent="varath",
              faction_territory="imperial",
              world_x=0, world_y=0, world_radius=100)

    # --- District: Harbor Gate ---
    harbor_gate = area.room("harbor_gate", "Harbor Gate",
        "The massive iron-banded gates of Vael's Crossing stand open, "
        "flanked by Imperial soldiers who eye every arrival with practiced "
        "suspicion. The cobblestones are worn smooth by generations of feet.",
        room_type="building", grid_x=0, grid_y=0)

    # ... more rooms ...

    return area.build()
```

### NPC with Full Dialogue (verified pattern from dialogue_engine.py)
```python
area.npc(guild_room, "combat_trainer",
    key="Sergeant Varek",
    npc_name="Varek",
    faction="empire",
    dialogue={
        "greeting_tiers": {
            "hostile": "Get out of my sight before I arrest you.",
            "suspicious": "State your business. Quickly.",
            "neutral": "Another would-be warrior? Let's see what you're made of.",
            "friendly": "Good to see you, soldier. Ready for a session?",
            "honored": "The finest blade I've trained in years. What do you need?",
        },
        "topics": {
            "training": "I teach the basics of combat -- footwork, guard positions, striking. "
                        "Cost is 50 Scales per session.",
            "weapons": "A good blade is an extension of yourself. Start with iron, "
                        "earn your way to steel.",
            "empire": "The Empire keeps the peace. That's enough for me.",
        },
        "base_hints": [
            "You look like you could use some training.",
            "The wilds outside the city walls aren't forgiving.",
        ],
    },
    ambient={
        "idle_echoes": [
            "Sergeant Varek barks orders at a group of recruits.",
            "The clang of training swords echoes through the yard.",
        ],
    })
```

### Spawn Definition with Template Reference
```python
# Spawn def stores template key; spawner applies full stats
area.spawn(clearing, "ash_wolf",
    behavior=["aggressive"],
    count_min=2, count_max=3,
    respawn_minutes=10,
    respawn_variance=3)
```

### Loot Table Entry (verified pattern from loot_tables.py)
```python
# world/loot_tables.py -- add to LOOT_TABLES dict
"ash_wolf": {
    "mob_type": "ash_wolf",
    "relevant_skill": "combat",
    "base_drop_chance": 0.65,
    "drops": [
        {
            "item_id": "ash_wolf_pelt",
            "key": "Ash Wolf Pelt",
            "item_type": "item",
            "weight": 0.6,
            "weight_in_pool": 10,
            "value_by_tier":  [3, 6, 12, 24, 48],
            "rarity_by_tier": ["normal", "normal", "normal", "magic", "rare"],
            "desc_by_tier": [
                "A rough ash wolf pelt, singed at the edges.",
                "A serviceable ash wolf pelt.",
                "A quality ash wolf pelt with thick fur.",
                "A fine ash wolf pelt, unusually soft.",
                "A pristine ash wolf pelt of extraordinary quality.",
            ],
        },
    ],
},
```

### Trainer Registry Entry (verified pattern from skill_definitions.py)
```python
# world/skill_definitions.py -- populate TRAINER_REGISTRY
TRAINER_REGISTRY = {
    "varek_combat_trainer": {
        "name": "Sergeant Varek",
        "trainer_quality": "journeyman",
        "quality_multiplier": 1.5,
        "skills_taught": ["reflexes", "intimidation", "climbing"],
        "cost_per_session": 50,
    },
    "herbalist_maren": {
        "name": "Maren",
        "trainer_quality": "apprentice",
        "quality_multiplier": 1.25,
        "skills_taught": ["herbalism", "first_aid"],
        "cost_per_session": 30,
    },
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 7 equipment slots | 13 slots needed per D-37 | Phase 7 | Must update SoravelonEquipment.VALID_SLOTS |
| No mob templates | Template registry needed | Phase 7 | Must create world/mob_templates.py |
| No wandering mobs | Wander tick system needed | Phase 7 | Must implement wander_mob_tick |
| Empty TRAINER_REGISTRY | Populated with city NPCs | Phase 7 | Must add entries to skill_definitions.py |
| Empty LOOT_TABLES | Zone-specific drop tables | Phase 7 | Must add entries to loot_tables.py |
| Empty world/areas/ | 5 zone spec files | Phase 7 | Content authoring core deliverable |
| Default start in Limbo | Start in Vael's Crossing | Phase 7 | Must configure START_LOCATION |

## Open Questions

1. **Vendor Buy/Sell Command**
   - What we know: NPC vendor pattern exists conceptually (vendor_items on NPC), but there's no `CmdBuy` or `CmdSell` command implemented.
   - What's unclear: Whether Phase 6c delivered vendor commands or if they need to be built.
   - Recommendation: Check for existing buy/sell commands. If missing, implement as part of infrastructure wave.

2. **Layer 1 Override Application**
   - What we know: `area.node()` stores `layer_1_overrides` dict. `initialize_node()` creates Layer1Room objects.
   - What's unclear: Whether `initialize_node()` currently applies the overrides dict to set L1 room descriptions, or if it just creates rooms with default "[key] [Node Active]" names.
   - Recommendation: Verify and patch if needed during infrastructure wave.

3. **Stabilization Mechanic (D-51)**
   - What we know: NodeScript has failure 0-100 with tick-driven progression. Players should be able to slow/reverse failure.
   - What's unclear: No stabilization command or interaction exists yet.
   - Recommendation: Implement a CmdStabilize that reduces node failure when used in node center room. Gate by node_reading skill.

4. **Death Respawn Location (D-14)**
   - What we know: Medic building should serve as death respawn point.
   - What's unclear: How the death system currently handles respawn location (default Evennia behavior sends to `home`).
   - Recommendation: Override character death handling to respawn at medic room tagged with `respawn_point` in city.

5. **Vendor Consumable Potions (D-44)**
   - What we know: Crafting system creates items, but vendor potions need to be purchasable without crafting.
   - What's unclear: Whether item_spawner handles consumable items with use effects (healing, buffs).
   - Recommendation: Create basic potion item definitions with `item_type="consumable"` and appropriate use effects.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies -- all work uses existing project codebase and Evennia framework already installed).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Evennia test runner (Django TestCase) + unittest.TestCase |
| Config file | `server/conf/settings.py` (Evennia settings) |
| Quick run command | `evennia test --settings server.conf.settings tests/test_area_builder.py` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CON-01 | Hub city loads with all services, greeter NPC reachable | smoke | `evennia test --settings server.conf.settings tests/test_vaels_crossing.py -x` | Wave 0 |
| CON-02 | 3 starter zones load with rooms, mobs, NPCs, quest stubs | smoke | `evennia test --settings server.conf.settings tests/test_starter_zones.py -x` | Wave 0 |
| CON-03 | Node zone Layer 1 rooms created, state transitions work | integration | `evennia test --settings server.conf.settings tests/test_node_zone.py -x` | Wave 0 |
| CON-04 | Equipment catalog items creatable, equippable, no procedural affixes | unit | `evennia test --settings server.conf.settings tests/test_equipment_catalog.py -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `evennia test --settings server.conf.settings tests/test_area_builder.py -x` (existing tests still pass)
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_mob_templates.py` -- covers mob template registry and application
- [ ] `tests/test_equipment_slots.py` -- covers 13-slot equipment system, two-handed logic
- [ ] `tests/test_vaels_crossing.py` -- smoke test for hub city zone loading
- [ ] `tests/test_starter_zones.py` -- smoke test for starter zone loading
- [ ] `tests/test_node_zone.py` -- integration test for node zone with Layer 1
- [ ] `tests/test_equipment_catalog.py` -- unit test for equipment item definitions
- [ ] `tests/test_wander_system.py` -- unit test for mob wandering tick

## Project Constraints (from CLAUDE.md)

- Store game state on `db` attributes (persisted) or `ndb` (volatile). Never raw Django fields on typeclasses.
- Custom Django models go in `world/models.py`; register the `world` app for migrations.
- All game logic lives in `world/` modules; typeclasses call into them.
- Tests use Evennia's `EvenniaTestCase` or `EvenniaCommandTestMixin`.
- Mob behavior is driven by computed disposition -- never hardcode friend/foe.
- Node failure uses a state machine (healthy -> stressed -> failing -> collapsed) -- respect the tick-driven progression.
- Room state flags must be defined in `FLAG_VOCABULARY` before use -- never invent ad-hoc flag names.
- Zone files in `world/areas/*.py` define `build()` functions imported at server start.
- Mobs get abilities from `db.abilities` list -- no CharacterAbility unlock needed.
- NPC objects created via `area.npc()` with is_npc=True, dialogue kwargs.
- Items defined via `area.item()` stored on zone_obj.db.item_definitions.

## Sources

### Primary (HIGH confidence)
- `world/area_builder.py` -- Full DSL API inspection (zone, room, exit, spawn, npc, named_mob, item, mob, quest, material, lore_fragment, flight_point, node methods)
- `world/area_validator.py` -- VALID_ZONE_TYPES, VALID_CONTINENTS, VALID_NODE_TYPES, VALID_ROOM_TYPES, VALID_DIRECTIONS
- `typeclasses/objects.py` -- SoravelonEquipment VALID_SLOTS = {head, body, hands, feet, right_hand, left_hand, accessory} -- confirmed 7-slot gap
- `typeclasses/mobs.py` -- SoravelonMob.at_object_creation() defaults -- confirmed mob_type=None, abilities=[], base_aggression="passive"
- `world/mob_spawner.py` -- spawn_single_mob only sets zone_id, base_disposition, trust_sensitive, flee_threshold -- confirmed template gap
- `world/loot_tables.py` -- LOOT_TABLES has one "wolf" template entry -- confirmed needs population
- `world/skill_definitions.py` -- TRAINER_REGISTRY is empty -- confirmed needs population
- `world/zone_object.py` -- initialize_node() API: zone_obj, node_type, center_room, radius, layer0_rooms, failure_start
- `world/item_spawner.py` -- create_item_from_template() sets extras as db.* via kwargs
- `server/conf/at_server_startstop.py` -- _load_all_zones() two-pass loading confirmed
- `C:\Obsidian\brain\Soravelon\Soravelon_World_Bible.md` -- Naming conventions, geography, Varath details
- `C:\Obsidian\brain\Soravelon\soravelon-factions.md` -- Faction conflict map, standing tiers

### Secondary (MEDIUM confidence)
- `.claude/skills/*/skill.md` -- Skill files for area-builder, node-system, combat-system, item-typeclasses, loot-tables, mob-affix-system, dialogue-system, crafting-system, inventory-engine

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all existing project modules, no new dependencies
- Architecture: HIGH -- AreaBuilder DSL API verified by source inspection, zone spec pattern established
- Infrastructure gaps: HIGH -- Equipment slot mismatch, mob template gap, and wander system absence confirmed by direct code inspection
- Content design: MEDIUM -- creative authoring (zone names, mob types, NPC dialogue) depends on Claude's discretion, constrained by vault naming conventions
- Pitfalls: HIGH -- all pitfalls identified from actual source code analysis

**Research date:** 2026-03-29
**Valid until:** 2026-04-28 (stable -- all infrastructure is project-internal)
