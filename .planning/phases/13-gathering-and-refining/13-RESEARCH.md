# Phase 13: Gathering and Refining - Research

**Researched:** 2026-04-03
**Domain:** Resource gathering, material processing, fishing mini-game, tool durability, node discovery
**Confidence:** HIGH

## Summary

Phase 13 builds a full resource gathering and material processing pipeline on top of the existing crafting system (Phase 6c). The architecture mirrors the mob_spawner pattern: zone-level pool definitions manage stochastic node placement across eligible rooms, with a tick-driven script handling respawns. Gathering commands follow the `_BaseCraftCmd` pattern from `commands/cmd_crafting.py` (delay, move-cancel, skill integration). Processing recipes plug directly into the existing `RECIPE_REGISTRY` and `craft_item()` pipeline -- no new engine needed.

The critical integration points are: (1) AreaBuilder DSL extension for `gathering_pool()`, (2) new `MATERIAL_REGISTRY` in `world/material_definitions.py` as the central material taxonomy, (3) four new skill definitions (mining, woodcutting, skinning, prospecting) added to `world/skill_definitions.py`, (4) gathering commands as a `_BaseGatherCmd` family mirroring `_BaseCraftCmd`, (5) processing recipes added to `RECIPE_REGISTRY`, and (6) item_tag bridging for mob loot items to feed into the crafting ingredient pipeline.

**Primary recommendation:** Build bottom-up: material registry first, then gathering node infrastructure (typeclass + pool script + AreaBuilder DSL), then gathering commands, then processing recipes, then fishing mini-game, then prospect/survey + Sense integration. Each layer has clean test boundaries.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- D-01: Stochastic node spawning -- rooms flagged as eligible, nodes as Evennia objects, zone-wide pool management
- D-02: AreaBuilder DSL -- `area.gathering_pool('herb', rooms=[...], materials=[...], max_active=3, respawn_minutes=15)`
- D-03: Shared depletion -- nodes have random 2-6 use count, deplete and respawn in different eligible room
- D-04: Skill affects quality AND quantity of gathered materials
- D-05: Two-step max processing depth (raw -> processed, max 2 steps)
- D-06: Processing recipes go into existing RECIPE_REGISTRY, reuse _BaseCraftCmd pipeline
- D-07: Quality propagation -- raw material quality carries through processing
- D-08: Skill-based conversion ratio (3:1 -> 2:1 -> 1:1)
- D-09: MATERIAL_REGISTRY central dict in world/material_definitions.py
- D-10: 5 material tiers, expandable
- D-11: Mob drops feed processing pipeline as raw crafting materials
- D-12: Skill-specific commands: mine, harvest, chop, forage, fish, butcher
- D-13: 6 gathering skills: Mining (NEW), Herbalism (exists), Woodcutting (NEW), Foraging (exists), Fishing (exists), Skinning (NEW)
- D-14: Variable delay with skill reduction, min 40% of base timer
- D-15: Butcher targets corpses (CorpseContainer), extracts hides/bones/meat
- D-16: Active + idle fishing modes (cast -> bite -> reel vs auto-fishing)
- D-17: Fishing spots via gathering_pool system
- D-18: Optional bait system (bait improves catch, consumed per cast)
- D-19: Required tools per skill (pickaxe, hatchet, rod, sickle/shears)
- D-20: Tool durability with repair via smithing
- D-21: Tiered visibility (low=everyone, mid=skill gate, high=prospect/survey only)
- D-22: Prospect/survey -- straight-line scanning with directional indicators
- D-23: Sense integration -- vague environmental hints for gathering
- D-24: Common materials everywhere, rare exclusives per zone
- D-25: Zone difficulty influences tier range (floor/ceiling in gathering_pool)

### Claude's Discretion
- Exact gathering delay values per node tier
- Skill threshold breakpoints for tiered visibility
- Prospect/survey max range and scaling formula
- Tool durability values and repair cost formula
- Fishing bite timer ranges and idle catch intervals
- Bait items and bonus effects
- Processing recipe difficulty values
- Quality propagation formula
- GatheringNode typeclass implementation details
- Pool respawn timer randomization range
- Zone-exclusive material names

### Deferred Ideas (OUT OF SCOPE)
None.
</user_constraints>

## Standard Stack

### Core (all existing -- no new packages)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia | 6.0 | Server engine, typeclasses, tags, delay(), scripts | Project foundation |
| Django ORM | 5.x | Models for any persistent tracking | Already used for CharacterRecipe, SpawnRecord |
| Python stdlib | 3.11+ | random, time, collections | No external deps needed |

### New Modules (to create)
| Module | Purpose | Pattern Source |
|--------|---------|----------------|
| `world/material_definitions.py` | MATERIAL_REGISTRY, tier constants, category mappings | Mirrors `world/crafting_definitions.py` |
| `world/gathering_engine.py` | Node spawning, depletion, pool management, gathering logic | Mirrors `world/mob_spawner.py` pool pattern |
| `commands/cmd_gathering.py` | mine, harvest, chop, forage, butcher + _BaseGatherCmd | Mirrors `commands/cmd_crafting.py` |
| `commands/cmd_fishing.py` | fish command with active/idle modes | Unique but follows _BaseGatherCmd base |
| `commands/cmd_prospect.py` | prospect/survey command | Standalone command |

### Existing Modules to Extend
| Module | Extension | 
|--------|-----------|
| `world/crafting_definitions.py` | Add processing recipes to RECIPE_REGISTRY |
| `world/skill_definitions.py` | Add mining, woodcutting, skinning, prospecting skills |
| `world/area_builder.py` | Add `gathering_pool()` DSL method |
| `world/item_spawner.py` | Ensure item_tag is set on created items |
| `world/room_state.py` | Add gathering-related flags to FLAG_VOCABULARY |
| `typeclasses/mobs.py` | Mark corpses as butcherable |
| `commands/cmd_sense.py` | Add gathering node hints |

**Installation:** No new packages needed. All within existing Evennia + Django stack.

## Architecture Patterns

### Recommended Project Structure
```
world/
  material_definitions.py    # MATERIAL_REGISTRY, MATERIAL_TIERS, GATHERING_CATEGORIES
  gathering_engine.py        # spawn_gathering_pool(), deplete_node(), gather_from_node(), 
                             # GatheringPoolScript, prospect_scan()
commands/
  cmd_gathering.py           # _BaseGatherCmd, CmdMine, CmdHarvest, CmdChop, CmdForage, CmdButcher
  cmd_fishing.py             # CmdFish (active + idle modes)
  cmd_prospect.py            # CmdProspect / CmdSurvey
typeclasses/
  objects.py                 # GatheringNode typeclass (extend existing file)
```

### Pattern 1: GatheringNode Typeclass
**What:** An Evennia object representing a harvestable resource node in a room.
**When to use:** Every spawned gathering node is this typeclass.
**Example:**
```python
# Source: mirrors CorpseContainer pattern in typeclasses/objects.py
class GatheringNode(SoravelonObject):
    """A resource node that can be gathered from."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.node_type = ""          # "ore", "herb", "wood", "fish_spot"
        self.db.material_id = ""        # key into MATERIAL_REGISTRY
        self.db.gathers_remaining = 4   # random 2-6 per D-03
        self.db.tier = 1                # material tier 1-5
        self.db.zone_id = ""
        self.db.pool_id = ""            # which gathering_pool spawned this
        self.db.visibility = "low"      # low/mid/high for D-21
        self.locks.add("get:false()")   # can't pick up nodes
    
    def gather(self, character):
        """Decrement gathers_remaining. Returns True if node depleted."""
        self.db.gathers_remaining -= 1
        if self.db.gathers_remaining <= 0:
            return True  # caller handles depletion + respawn
        return False
```

### Pattern 2: GatheringPoolScript (Zone-Level Tick)
**What:** An Evennia Script attached to the zone object managing node spawning/respawning per pool.
**When to use:** One script per gathering_pool definition per zone.
**Example:**
```python
# Source: mirrors mob_spawner SpawnRecord pattern + NodeScript tick pattern
class GatheringPoolScript(SoravelonScript):
    """Manages a gathering pool's node lifecycle."""
    
    def at_script_creation(self):
        self.db.pool_id = ""
        self.db.zone_id = ""
        self.db.eligible_room_ids = []   # room dbrefs
        self.db.materials = []           # material_ids from pool def
        self.db.max_active = 3
        self.db.respawn_minutes = 15
        self.db.tier_floor = 1
        self.db.tier_ceiling = 3
        self.db.active_node_ids = []     # dbref list of live nodes
        self.key = "gathering_pool"
        self.interval = 60               # check every 60 seconds
        self.persistent = True
    
    def at_repeat(self):
        """Tick: check for depleted nodes, spawn replacements if under max."""
        # Prune deleted/depleted nodes from active list
        # If active < max_active, pick random eligible room, spawn node
        pass
```

### Pattern 3: _BaseGatherCmd (Mirrors _BaseCraftCmd)
**What:** Shared command base for all gathering commands with delay, move-cancel, tool check, skill integration.
**When to use:** Every gathering command (mine, harvest, chop, forage, butcher) inherits this.
**Example:**
```python
# Source: mirrors _BaseCraftCmd in commands/cmd_crafting.py
class _BaseGatherCmd(Command):
    """Base for gathering commands."""
    gather_skill = None    # "mining", "herbalism", etc.
    gather_verb = None     # "mine", "harvest", etc.
    required_tool = None   # "pickaxe", "sickle", etc.
    locks = "cmd:all()"
    help_category = "Gathering"

    def func(self):
        character = self.caller
        # 1. Check for required tool in equipment
        # 2. Find gathering node in room matching this skill
        # 3. Calculate delay (base - skill reduction, min 40%)
        # 4. Show gather echo, set ndb.gathering_in_progress
        # 5. delay() -> callback: gather, create item, deplete node if empty
```

### Pattern 4: Processing Recipes in RECIPE_REGISTRY
**What:** Processing recipes use the existing crafting pipeline with a `recipe_type: "processing"` tag.
**When to use:** Every raw->processed conversion (ore->ingot, hide->leather_strip, etc.)
**Example:**
```python
# Source: extends RECIPE_REGISTRY in world/crafting_definitions.py
"iron_ingot": {
    "name": "Iron Ingot",
    "skill": "smithing",
    "difficulty": 15,
    "station": "forge",
    "recipe_type": "processing",    # distinguishes from crafting recipes
    "ingredients": [
        {"item_tag": "iron_ore", "quantity": 3},  # 3:1 at low skill
    ],
    "conversion_ratio": {           # NEW field for processing recipes
        "thresholds": [30, 60, 85],  # skill values
        "quantities": [3, 2, 1],     # ingredients needed at each tier
    },
    "output": {
        "template_id": "iron_ingot",
        "base_item_type": "material",
        "quality_affects": "material_quality",
    },
    "default_known": True,
    "command": "smith",
    "craft_time": 4,
    "craft_echo": "You heat the ore and hammer out impurities...",
},
```

### Pattern 5: Prospect/Survey Line-of-Sight Scan
**What:** Scans exits in cardinal directions, walking straight lines N rooms deep.
**When to use:** CmdProspect command only.
**Example:**
```python
# Source: NOT BFS -- explicit straight-line walking per D-22
CARDINAL_DIRECTIONS = ["north", "south", "east", "west"]

def prospect_scan(character, max_range):
    """Scan straight lines from character's room for gathering nodes."""
    results = []
    room = character.location
    for direction in CARDINAL_DIRECTIONS:
        current = room
        for distance in range(1, max_range + 1):
            exit_obj = _find_exit(current, direction)
            if not exit_obj:
                break
            current = exit_obj.destination
            nodes = [obj for obj in current.contents 
                     if hasattr(obj.db, 'node_type')]
            for node in nodes:
                results.append({
                    "direction": direction,
                    "distance": distance,
                    "node": node,
                })
    return results
```

### Anti-Patterns to Avoid
- **BFS for prospect/survey:** D-22 explicitly says straight-line scanning, NOT BFS. Do not use patrol_engine.find_path() or any graph traversal.
- **New crafting engine for processing:** D-06 says processing recipes go into RECIPE_REGISTRY. Do not create a separate processing engine -- extend `craft_item()` to handle conversion ratios.
- **Raw Django fields on GatheringNode:** Use `db` attributes per project convention. Never add raw Django model fields to typeclasses.
- **Hardcoded material lists:** All materials must be in MATERIAL_REGISTRY. Never scatter material definitions across multiple files.
- **item_tags on mob loot missing:** Current `item_spawner.create_item_from_template()` does NOT set item_tags. Without item_tags, mob loot cannot be used as crafting ingredients. This MUST be fixed.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Gathering delay + cancel | Custom timer system | `evennia.utils.delay()` + move check (same as _BaseCraftCmd) | Already proven pattern in crafting |
| Quality calculation | New quality formula | `calculate_craft_quality()` from crafting_engine | Same quality tiers, already tested |
| Skill progression | Custom XP system | `accumulate_skill_use()` + `get_skill_value()` from skill_engine | Handles diminishing returns, thresholds |
| Item creation | Manual Evennia object creation | `create_item_from_template()` from item_spawner | Handles typeclass selection, attrs |
| Recipe knowledge tracking | Custom tracking | `CharacterRecipe` model + `learn_recipe()` | Already handles discovery, idempotent |
| Node room placement | Custom room selection | Mirror `mob_spawner` zone-tag search pattern | `evennia.search_tag(zone_id, category="zone_id")` |
| Corpse access checks | Custom permission system | `CorpseContainer.can_loot()` | Already handles kill ownership + phases |

**Key insight:** 80% of this phase is wiring existing patterns (crafting engine, mob spawner, skill engine, item spawner) into a new domain. The gathering-specific code is mainly: node lifecycle management, tool checking, fishing state machine, and prospect line-scanning.

## Common Pitfalls

### Pitfall 1: item_tag Gap on Mob Loot
**What goes wrong:** Mob loot items (boar_hide, spider_silk_thread, etc.) are created by `item_spawner.create_item_from_template()` which does NOT set item_tags. Crafting engine matches ingredients via `obj.tags.has(tag, category="item_tag")`. Without item_tags, mob drops cannot be used as crafting ingredients.
**Why it happens:** item_spawner was built for general items before crafting ingredient matching existed.
**How to avoid:** Add item_tag setting to `create_item_from_template()` -- set `item.tags.add(item_def["item_id"], category="item_tag")` after creation. This makes all spawned items (loot, gathered, purchased) usable as crafting ingredients.
**Warning signs:** Processing recipes that require mob drops (hide -> leather_strip) always fail with "You need X but only have 0."

### Pitfall 2: Conversion Ratio in craft_item() 
**What goes wrong:** `craft_item()` currently checks `recipe["ingredients"]` with fixed quantities. Processing recipes need dynamic quantities based on character skill (D-08: 3:1 -> 2:1 -> 1:1).
**Why it happens:** Original crafting engine was built for fixed-quantity recipes only.
**How to avoid:** Extend `_check_ingredients()` to check for `conversion_ratio` field in recipe. If present, calculate actual quantity needed based on character skill before matching.
**Warning signs:** All players consuming same number of raw materials regardless of skill level.

### Pitfall 3: GatheringNode Not Appearing in Room Description
**What goes wrong:** Nodes exist as Evennia objects in the room but players don't see them in `look` output.
**Why it happens:** Standard `return_appearance()` on rooms lists contents, but gathering nodes need skill-gated visibility (D-21).
**How to avoid:** Override `get_display_name()` on GatheringNode OR hook into room's `return_appearance()` to filter nodes by viewer's skill. Low-tier nodes always visible, mid/high-tier gated.
**Warning signs:** Players can see all nodes regardless of skill, or can't see any nodes at all.

### Pitfall 4: Corpse Decay vs Butcher Timing
**What goes wrong:** CorpseContainer has a decay timer (GRACE_PERIOD=120s + OPEN_PERIOD=300s = 7 min total). If butcher takes too long or player arrives late, corpse may decay before butchering.
**Why it happens:** Corpse lifecycle was designed for looting, not gathering. Butcher needs corpse to persist long enough.
**How to avoid:** Butcher should work within the existing corpse lifecycle -- no need to extend timers. 7 minutes is ample. But butcher must check `corpse.db.loot_phase != "decayed"` and respect `can_loot()` during locked phase.
**Warning signs:** "The corpse has already decayed" errors when players try to butcher.

### Pitfall 5: Gathering Pool Respawn in Wrong Room
**What goes wrong:** Node depletes in room A, respawn timer fires, new node spawns in room A again (same room). D-03 says "spawns in a different eligible room."
**Why it happens:** Random room selection without excluding the room where the node just depleted.
**How to avoid:** Track `last_depleted_room_id` on the pool script. Exclude it from random selection on next spawn (or weight it very low if only 2 eligible rooms).
**Warning signs:** Players notice nodes always reappear in the same spot, defeating anti-bot intent.

### Pitfall 6: Fishing State Machine Complexity
**What goes wrong:** Active fishing (cast -> bite -> reel) has multiple async states with timers, and idle fishing needs periodic auto-catches. Both running on the same character creates state conflicts.
**Why it happens:** Two modes sharing one command with different state machines.
**How to avoid:** Use `character.ndb.fishing_state` dict to track mode, current phase, and timer references. Clear state completely on mode switch. Cancel pending timers on move/interrupt.
**Warning signs:** "ghost" fishing timers firing after player moved, or idle mode accidentally triggering active mode rewards.

### Pitfall 7: New Skills Not in SKILL_DEFINITIONS
**What goes wrong:** Gathering commands call `get_skill_value(character, "mining")` but "mining" doesn't exist in `SKILL_DEFINITIONS`, returning 0 always.
**Why it happens:** New skills declared in CONTEXT.md but not yet added to skill_definitions.py.
**How to avoid:** Add mining, woodcutting, skinning to SKILL_DEFINITIONS early (Wave 0 or Wave 1). Include thresholds, domain_bonus, trainer_required_above.
**Warning signs:** All gathering attempts treat player as 0 skill.

### Pitfall 8: FLAG_VOCABULARY Missing Gathering Flags
**What goes wrong:** Trying to add gathering-related room flags (for Sense hints) without defining them in FLAG_VOCABULARY first.
**Why it happens:** Project convention requires all flags in FLAG_VOCABULARY before use.
**How to avoid:** Add gathering flags ("mineral_deposits", "rich_soil", "dense_foliage", "water_source") to FLAG_VOCABULARY as part of the infrastructure wave.
**Warning signs:** `add_room_flag: unknown flag` warnings in logs.

## Code Examples

### Material Registry Structure
```python
# world/material_definitions.py
# Source: project convention (mirrors crafting_definitions.py pattern)

MATERIAL_TIERS = {
    1: "Common",
    2: "Uncommon", 
    3: "Rare",
    4: "Exceptional",
    5: "Legendary",
}

GATHERING_CATEGORIES = {
    "ore": {"skill": "mining", "tool": "pickaxe", "command": "mine"},
    "herb": {"skill": "herbalism", "tool": "sickle", "command": "harvest"},
    "wood": {"skill": "woodcutting", "tool": "hatchet", "command": "chop"},
    "forage": {"skill": "foraging", "tool": None, "command": "forage"},
    "fish": {"skill": "fishing", "tool": "fishing_rod", "command": "fish"},
    "hide": {"skill": "skinning", "tool": "skinning_knife", "command": "butcher"},
}

# Base delay per tier (seconds). Skill reduces but never below 40%.
GATHER_DELAY_BY_TIER = {
    1: 4,
    2: 6,
    3: 8,
    4: 12,
    5: 16,
}

MATERIAL_REGISTRY = {
    # --- Ores ---
    "iron_ore": {
        "display_name": "Iron Ore",
        "category": "ore",
        "tier": 1,
        "raw_form": "iron_ore",
        "processed_form": "iron_ingot",
        "gathering_skill": "mining",
        "processing_skill": "smithing",
        "processing_station": "forge",
    },
    "steel_ore": {
        "display_name": "Steel Ore",
        "category": "ore",
        "tier": 2,
        "raw_form": "steel_ore",
        "processed_form": "steel_ingot",
        "gathering_skill": "mining",
        "processing_skill": "smithing",
        "processing_station": "forge",
    },
    # ... more materials per category
}
```

### Tool Check Pattern
```python
# Source: project convention (equipment check via db.equipment_slot + item_tag)
def check_tool(character, required_tool):
    """Check if character has required tool equipped or in inventory."""
    if not required_tool:
        return (True, None)  # foraging needs no tool
    
    for item in character.contents:
        if item.tags.has(required_tool, category="item_tag"):
            if getattr(item.db, "durability", None) is not None:
                if item.db.durability <= 0:
                    return (False, f"|rYour {item.key} is broken and needs repair.|n")
            return (True, item)
    
    tool_name = required_tool.replace("_", " ")
    return (False, f"|rYou need a {tool_name} to do that.|n")
```

### Skill-Based Conversion Ratio
```python
# Source: D-08 from CONTEXT.md
def get_conversion_quantity(character, recipe):
    """Calculate ingredient quantity needed based on skill."""
    conversion = recipe.get("conversion_ratio")
    if not conversion:
        return None  # use recipe's fixed quantities
    
    from world.skill_engine import get_skill_value
    skill = get_skill_value(character, recipe["skill"])
    
    thresholds = conversion["thresholds"]  # e.g., [30, 60, 85]
    quantities = conversion["quantities"]  # e.g., [3, 2, 1]
    
    for i, threshold in enumerate(thresholds):
        if skill < threshold:
            return quantities[i]
    return quantities[-1]  # highest skill tier
```

### Gathering Pool DSL (AreaBuilder Extension)
```python
# Source: mirrors area.spawn() pattern in area_builder.py
def gathering_pool(self, pool_type, rooms, materials, **kwargs):
    """Register a gathering pool definition on this zone."""
    pool_def = {
        "pool_type": pool_type,         # "ore", "herb", "wood", "fish"
        "room_ids": rooms,              # list of room_id strings
        "materials": materials,          # list of material_id strings
        "max_active": kwargs.get("max_active", 3),
        "respawn_minutes": kwargs.get("respawn_minutes", 15),
        "respawn_variance": kwargs.get("respawn_variance", 5),
        "tier_floor": kwargs.get("tier_floor", 1),
        "tier_ceiling": kwargs.get("tier_ceiling", 3),
    }
    current = list(self._zone_obj.db.gathering_pools or [])
    current.append(pool_def)
    self._zone_obj.db.gathering_pools = current
    return self
```

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Evennia test runner (Django TestCase) + unittest.TestCase |
| Config file | `server/conf/settings.py` (test settings) |
| Quick run command | `evennia test --settings server.conf.settings tests/test_gathering.py` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SC-1 | Gathering nodes spawn randomly in eligible rooms per zone pool | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestGatheringPoolSpawn -x` | Wave 0 |
| SC-2 | Gathering commands require tools and apply skill-based delay | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestGatherCommands -x` | Wave 0 |
| SC-3 | Processing recipes convert raw to processed with skill-based ratios | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestProcessingRecipes -x` | Wave 0 |
| SC-4 | MATERIAL_REGISTRY defines materials with 5 tiers | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestMaterialRegistry -x` | Wave 0 |
| SC-5 | Fishing active mini-game (cast/bite/reel) + idle mode | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestFishing -x` | Wave 0 |
| SC-6 | Tools degrade with use and are repairable | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestToolDurability -x` | Wave 0 |
| SC-7 | Prospect/survey reveals nodes in straight lines | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestProspect -x` | Wave 0 |
| SC-8 | Mob loot drops feed into processing pipeline | unit | `evennia test --settings server.conf.settings tests/test_gathering.py::TestMobLootProcessing -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `evennia test --settings server.conf.settings tests/test_gathering.py -x`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_gathering.py` -- covers all 8 success criteria
- [ ] `tests/test_material_definitions.py` -- validates MATERIAL_REGISTRY structure (optional, can fold into test_gathering)

## Project Constraints (from CLAUDE.md)

- Store game state on `db` attributes (persisted) or `ndb` (volatile). Never raw Django fields on typeclasses.
- Custom Django models go in `world/models.py`; register the `world` app for migrations.
- All game logic lives in `world/` modules; typeclasses call into them.
- Tests use Evennia's `EvenniaTestCase` or `EvenniaCommandTestMixin`.
- Room state flags must be defined in `FLAG_VOCABULARY` before use.
- Functions that can fail return `(bool, str)` per project convention.
- Lazy imports inside functions to avoid circular imports at load time.
- Use `commands.command.Command` (local base) not `evennia.Command`.

## Key Integration Points

### 1. item_spawner.py -- MUST Add item_tag
Current `create_item_from_template()` does NOT set `item_tag` category tags on created items. The crafting engine matches ingredients via `obj.tags.has(tag, category="item_tag")`. Without this fix, NO mob loot or gathered material can be used as a crafting ingredient.

**Fix:** Add `item.tags.add(item_def["item_id"], category="item_tag")` in `create_item_from_template()` after item creation. This is a prerequisite for the entire processing pipeline.

### 2. crafting_engine.py -- Extend for Conversion Ratios
`_check_ingredients()` uses fixed `ingredient["quantity"]` values. Processing recipes need dynamic quantities based on skill level (D-08). Either:
- Add a pre-processing step that adjusts ingredient quantities before calling `_check_ingredients()`
- Or extend `_check_ingredients()` to check for `conversion_ratio` field

### 3. AreaBuilder.build() -- Initialize gathering_pools
`build()` already initializes `zone_obj.db.material_definitions = []`. Add `zone_obj.db.gathering_pools = []` alongside it, and call gathering pool initialization after zone build (same place as `spawn_zone()`).

### 4. Mob at_death -- Corpse butcherability
`handle_mob_death()` in `combat_engine.py` creates a CorpseContainer. The corpse already stores `mob_key` and `mob_rarity`. Butcher command needs to look up what materials this mob type yields (via loot tables or a new `BUTCHER_YIELDS` mapping keyed by mob_type).

### 5. Sense Command Extension
`cmd_sense.py` reads `room_state.get_room_flags()`. Add gathering-related flags to FLAG_VOCABULARY (e.g., "mineral_deposits", "water_source") and set them on rooms with gathering pools during zone build. Sense then automatically shows hints.

## Open Questions

1. **Do we need a Django model for gathering nodes?**
   - What we know: Mob spawner uses SpawnRecord model for crash-recovery. Gathering nodes are ephemeral (deplete in minutes). 
   - What's unclear: Is ndb-based tracking on the GatheringPoolScript sufficient, or do we need persistent records for server restart recovery?
   - Recommendation: Use `db` attributes on the pool script (persistent across restarts) to track active_node_ids. No separate Django model needed -- the script reconstructs state from its db attrs. This mirrors how zone_obj stores spawn_definitions.

2. **How do gathered items get quality?**
   - What we know: D-04 says skill affects quality. Existing quality tiers are flawed/standard/fine/superior/masterwork.
   - What's unclear: Does `calculate_craft_quality()` apply directly, or does gathering need its own formula?
   - Recommendation: Reuse `calculate_craft_quality(skill_value, tier_difficulty)` where tier_difficulty maps from node tier (tier 1 = difficulty 10, tier 5 = difficulty 80). This reuses tested code and aligns gathered material quality with crafting quality.

3. **Prospecting skill -- new skill or use existing?**
   - What we know: D-13 lists 6 gathering skills. Prospect/survey (D-22) is a discovery mechanic, not a gathering skill.
   - What's unclear: Should prospect use foraging skill, a generic "prospecting" skill, or the relevant gathering skill for each node type?
   - Recommendation: Use the relevant gathering skill for visibility checks (mining skill reveals ore nodes). Prospect/survey uses the highest of the character's gathering skills as its range determinant. No separate "prospecting" skill needed.

## Sources

### Primary (HIGH confidence)
- `world/crafting_engine.py` -- Full read, verified quality tiers, ingredient matching, craft_item pipeline
- `world/crafting_definitions.py` -- Full read, verified RECIPE_REGISTRY structure, QUALITY_TIERS, STATION_REQUIREMENTS
- `commands/cmd_crafting.py` -- Full read, verified _BaseCraftCmd pattern (delay, move-cancel, skill)
- `world/mob_spawner.py` -- Full read, verified spawn pool pattern, respawn scheduling, SpawnRecord
- `world/item_spawner.py` -- Full read, verified create_item_from_template (NO item_tag setting)
- `world/loot_tables.py` -- Partial read, verified roll_loot pipeline, _build_item_def structure
- `world/skill_definitions.py` -- Full read, verified existing skills (herbalism, foraging, fishing exist; mining/woodcutting/skinning do NOT)
- `world/skill_engine.py` -- Partial read, verified get_skill_value, accumulate_skill_use
- `world/area_builder.py` -- Partial read, verified spawn() DSL, item() DSL, build() initialization
- `typeclasses/mobs.py` -- Read at_death, verified loot drop + corpse spawn flow
- `world/combat_engine.py` -- Searched, verified spawn_corpse creates CorpseContainer with mob_key, mob_rarity
- `typeclasses/objects.py` -- Verified CorpseContainer (GRACE_PERIOD=120s, OPEN_PERIOD=300s, can_loot)
- `commands/cmd_sense.py` -- Read, verified it reads room_state flags
- `.claude/skills/crafting-system/skill.md` -- Read, verified crafting system conventions

### Secondary (MEDIUM confidence)
- Phase 13 CONTEXT.md -- All locked decisions (D-01 through D-25) treated as authoritative

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all existing Evennia patterns, no new dependencies
- Architecture: HIGH -- mirrors proven mob_spawner + crafting_engine patterns
- Pitfalls: HIGH -- identified from direct code reading of existing integration points
- Integration points: HIGH -- verified by reading actual source code, not assumptions

**Research date:** 2026-04-03
**Valid until:** 2026-05-03 (stable codebase, patterns unlikely to change)
