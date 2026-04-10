# Phase 6a: Base Attributes & Combat System - Research

**Researched:** 2026-03-26
**Domain:** Character stats, turn-based combat, status effects, corpse containers, Evennia Script lifecycle
**Confidence:** HIGH

## Summary

Phase 6a builds the combat system that makes Soravelon playable. It spans two major systems: (1) a 7-stat base attribute system with descriptor-based display and use-driven growth, and (2) a full turn-based combat engine using Evennia Scripts to manage initiative, action budgets, damage resolution, status effects with compound triggers, and mob AI turns.

The existing codebase provides strong foundations. `ability_engine.py` has 10 stub effect handlers ready to be wired to real combat resolution. `zone_scaling.py` already handles per-player logarithmic scaling and mob HP initialization. `mob_disposition.py` computes the aggro float that determines auto-engage behavior. The OOB publisher has `push_combat_update()` and `push_stat_update()` placeholders ready for combat data schemas.

The primary architectural decision is CombatScript design. Following the project's established Script pattern (NodeScript, PatrolScript, FlightScript), the CombatScript attaches to a room and manages all combat state for that encounter. Evennia's official turn-based combat howto confirms this as the canonical approach: a Script-based handler stores combatant lists, turn actions, and initiative order, using `force_repeat()` for event-driven turn advancement and `at_repeat()` as the timeout fallback.

**Primary recommendation:** Build CombatScript as a room-attached SoravelonScript with event-driven turn processing (not tick-based), following Evennia's official CombatHandler pattern. Use `evennia.utils.utils.delay()` for round timers in group combat; wait indefinitely for solo play per D-18.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 7 base stats: Strength, Agility, Endurance, Mana, Acuity, Presence, Resonance. Each governs specific combat and world-interaction aspects per vault spec.
- **D-02:** Classic point-buy at character creation. All stats start at a base value, player distributes N bonus points. Min per stat = base, max per stat = base + cap. Ancestry provides modifiers on top.
- **D-03:** Player-facing display uses descriptors ONLY -- no numbers shown. 10 descriptors per stat, each stat has unique flavor words (e.g., Strength: "Feeble" to "Prodigious", Agility: "Sluggish" to "Ethereal"). Research designs all 70 descriptors (7 stats x 10 tiers).
- **D-04:** Stats grow through ACTION-SPECIFIC use, not domain XP. Melee hits grow Strength, successful dodges grow Agility, taking damage grows Endurance. Granular per-action tracking required.
- **D-05:** HP derived from Endurance attribute + level modifier. Three resource pools: HP (survival), Stamina (special actions + room-to-room movement), Domain Resource (guild-specific from Phase 5).
- **D-06:** Stamina fuels special actions and room-to-room movement during combat. Basic attacks and abilities do NOT cost stamina.
- **D-07:** Turn-based combat with FIXED initiative per encounter. Initiative = f(Agility stat). Each combatant has individual initiative slot. Re-roll NOT per round -- fixed for entire encounter.
- **D-08:** Full ACTION BUDGET system per vault spec. Actions per turn = f(Speed/Agility). Damage per action = base_damage / actions_per_turn modifier. Ability damage = base_damage x primary_stat_value.
- **D-09:** One ability use per turn maximum. Stats can grant multiple basic attacks per turn. Weapon speed + character stat determines number of basic attacks.
- **D-10:** Abilities have cooldowns (decrement at round end). Charged abilities (1-2 round cast) declared on acting character's turn; character auto-attacks during charge; resource generates during charge.
- **D-11:** Status effects tick at round end. Cooldowns decrement at round end.
- **D-12:** CombatScript attached to room manages combat. Drives initiative order, round progression, mob AI turns. Removed when combat ends. Same Script pattern as NodeScript/PatrolScript/FlightScript.
- **D-13:** Disposition-driven auto-engage. Aggressive mobs attack on sight based on disposition. `is_hunter` flag enables grid-distance aggro (BFS pathfinding to player within N rooms). NOT all aggressive mobs hunt -- only flagged ones.
- **D-14:** Auto-target + override. Player auto-targets last attacked mob. Can switch with 'target <mob>'. Persistent target on ndb.
- **D-15:** Individual initiative (interleaved player + mob turns). NOT group phases.
- **D-16:** On player's turn: show list of abilities off cooldown (ready to use) and abilities on cooldown with rounds remaining. NOT hints -- actual ability list.
- **D-17:** Hybrid input: show available options but accept typed commands ('attack goblin', 'use fireball goblin', 'flee').
- **D-18:** Round timer: WAIT INDEFINITELY for solo play. TIMED ROUNDS (configurable) for group combat. Auto-attack on timeout.
- **D-19:** Weapon base damage + stat scaling. Weapon has base damage range. Relevant stat (Strength for melee, etc.) adds bonus. Zone scaling applies as multiplier. Ability damage is separate formula from vault spec.
- **D-20:** Wide damage scale per vault: Low tier 50-500 HP, Mid tier 500-5000 HP, High tier thousands. Crits for 1000+ at appropriate tiers are a design goal.
- **D-21:** Elite mobs: treated as backend level +5 (+40% incoming damage, +25% damage reduction, +15% avoidance). Boss mobs: backend level +10 (+80%/+50%/+30%). Per-level scaling: +8%/+5%/+3%.
- **D-22:** Mob resistances per vault: physical, fire, ice, poison, lightning, arcane, none. Resistance = float 0.0-1.0 damage reduction per element.
- **D-23:** Status effects on ndb.active_effects list. Each entry: type, duration, source, magnitude. Cleared on encounter end. Tick down each round.
- **D-24:** Full compound effect system wired in this phase. Additive compounds (Poison+Slow=Venom Lag, Weaken+Poison=Corruption, Slow+Root=Petrify). Consuming compounds (Burn+Wet=Steam). Per vault spec.
- **D-25:** Stackable effects: Poison (5), Bleed (4), Burn (4), Weaken (3), Drain (2). Non-stackable: Slow, Root, Blind, Stun, Charm, Haste, Wet. Stronger replaces weaker for non-stackable.
- **D-26:** Player death: per vault -- respawn at nearest hub city medic (naked). Corpse spawns at death location with all carried equipment. Death recovery tiers (Municipal Medic, Death Insurance, Recovery Crew, Underworld Option).
- **D-27:** Mob death: corpse container model. Timed decay. Killer-locked loot (only killer or their group can loot for grace period, then opens to all, then decays). Room flags written on mob death (blood_soaked, fading_life, power_vacuum -- already exist from Phase 5).
- **D-28:** Flee: speed check + skill check + exit. Some skills give bonuses to escaping (e.g., Stealth). Failure = lose your turn. Can't flee while rooted/stunned. On success, character moves to random adjacent room.
- **D-29:** Individual initiative per player (interleaved with mobs). NOT all-players-then-all-mobs.
- **D-30:** Group loot uses existing group_engine loot modes (Personal, FFA, Round Robin, Need/Pass). Corpse container is killer-locked to killer's group.

### Claude's Discretion
- Exact point-buy numbers (total points, base value, per-stat cap)
- Exact action budget formula parameters
- CombatScript tick interval vs event-driven architecture
- Corpse container decay timer duration
- Exact stamina pool derivation formula
- Status effect duration balancing values

### Deferred Ideas (OUT OF SCOPE)
- Full threat engine (taunt, aggro tables, tank mechanics) -- post-launch per vault
- PvP combat -- not in scope
- Equipment stat bonuses -- Phase 7 (content) or equipment phase
- Rested XP bonus system -- separate utility phase
- Dragon companion combat integration -- companion design pass
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CMB-01 | Combat system integrates ability effects with damage, status, and targeting | CombatScript architecture + ability_engine wiring + damage formulas from vault |
| CMB-02 | Zone scaling applies per-player logarithmic factors during combat | Existing zone_scaling.py already handles this; combat engine calls get_combat_scale() |
| CMB-03 | Mob abilities fire based on weight, cooldown, and condition vocabulary | Mob ability schema from soravelon-mobs.md fully documented; AI turn logic in CombatScript |
| CMB-04 | Group combat uses existing group engine for proximity and loot | group_engine.py get_members_in_proximity() ready; corpse container with killer-locked loot |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia Scripts | 6.0.0 | CombatScript lifecycle, timer management | Official Evennia pattern for timed game state |
| evennia.utils.utils.delay() | 6.0.0 | Round timers for group combat | Non-blocking deferred call; used by FlightScript already |
| Django ORM | 6.0.3 | No new models needed (combat state is ndb-volatile) | Existing project DB layer |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| random (stdlib) | 3.12 | Damage rolls, initiative, status application | Every combat action |
| math (stdlib) | 3.12 | Stat derivation formulas, scaling | HP/stamina calculations |

No new pip packages required for this phase. All dependencies are already in the project.

## Architecture Patterns

### New Module Structure
```
world/
  combat_engine.py       # Core combat resolution: damage, status, compounds
  combat_script.py       # CombatScript class (room-attached)
  combat_ai.py           # Mob turn AI: ability selection, targeting
  base_attributes.py     # 7 stats, descriptors, point-buy, stat growth
  status_effects.py      # Effect application, compound triggers, tick logic
typeclasses/
  objects.py             # Add CorpseContainer class
commands/
  combat_commands.py     # CmdAttack, CmdUseAbility (exists), CmdFlee, CmdTarget
```

### Pattern 1: CombatScript (Room-Attached State Machine)

**What:** A SoravelonScript attached to a room that manages all combat state for an encounter. Created when combat begins, deleted when combat ends. Stores combatant list, initiative order, round counter, and per-combatant action state.

**When to use:** Every combat encounter.

**Architecture:**
```python
class CombatScript(SoravelonScript):
    """
    Room-attached combat manager. One per active encounter.

    db attributes (persistent across reload):
        combatant_ids: list[int]      # character/mob dbrefs in initiative order
        round_number: int
        current_turn_index: int       # index into combatant_ids
        initiative_order: list[dict]  # [{id, initiative_value}] sorted desc

    ndb attributes (volatile, rebuilt at_start):
        turn_timer_id: int|None       # delay() handle for group timeout
        pending_actions: dict         # {combatant_id: action_dict}

    NOT self-ticking (interval=0). Turn progression is event-driven:
    - Player submits action -> process_player_action() -> advance_turn()
    - Mob turn -> process_mob_turn() -> advance_turn()
    - Group timeout -> force_repeat() or delay callback -> auto_attack()
    """
```

**Why event-driven over tick-based:** Combat is inherently event-driven (player inputs, mob decisions). A tick-based approach would burn CPU checking "is it someone's turn?" every N seconds. Event-driven: process action, advance to next combatant, wait. The only timer is the group combat round timeout, handled by `delay()`.

**Lifecycle:**
1. `start_combat(room, initiator, targets)` -- create CombatScript on room, compute initiative, begin first turn
2. `at_start()` -- called on creation and server reload; re-adds CombatCmdSet to all combatants
3. `advance_turn()` -- move to next combatant in initiative order; if mob, auto-process; if player, prompt and wait
4. `end_round()` -- tick status effects, decrement cooldowns, check death, start next round
5. `end_combat()` -- clean up ndb, remove CombatCmdSet, call `self.delete()`

### Pattern 2: Status Effect Stack
```python
# On ndb.active_effects -- list of dicts
{
    "type": "poison",          # effect type string
    "stacks": 2,               # current stack count (stackable only)
    "duration": 4,             # rounds remaining
    "magnitude": 8,            # damage per tick or reduction value
    "source_id": 42,           # character/mob who applied it
    "max_stacks": 5,           # ceiling for this effect type
}
```

### Pattern 3: Corpse Container (Timed Decay)
```python
class CorpseContainer(SoravelonContainer):
    """
    Created on mob death. Contains mob's loot drops.
    Killer-locked for grace period, then open, then decays.
    Uses delay() for timed transitions -- NOT a Script.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.killer_id = None        # character who killed the mob
        self.db.killer_group_id = None  # group leader id (if grouped)
        self.db.loot_phase = "locked"   # locked -> open -> decayed
        self.db.created_at = None
```

### Anti-Patterns to Avoid
- **Tick-based combat polling:** Do NOT use `interval > 0` on CombatScript. Event-driven turn advancement is correct.
- **Combat state on character.db:** Combat state is volatile. Use ndb for targets, cooldowns, effects. Only base stats go on db.
- **Per-mob combat Scripts:** One CombatScript per room manages ALL combatants in that room's encounter. NOT one per mob.
- **Direct character.msg() for combat output:** Route through oob_publisher.push_combat_update() for client sync. Text output to MUD terminal is separate from OOB data.
- **getattr(obj.db, 'attr', default):** Per project conventions, always use `obj.db.attr or fallback`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Turn timer | Custom threading/sleep | `evennia.utils.utils.delay()` | Non-blocking, Twisted-safe, crash-safe |
| Combat CmdSet management | Manual cmd add/remove | `character.cmdset.add()/remove()` with mergetype | Evennia's cmdset stack handles priority and cleanup |
| Damage scaling | Custom scaling math | `zone_scaling.get_combat_scale()` | Already built and tested; logarithmic scaling ready |
| Resistance calculation | Custom resistance logic | `zone_scaling.apply_resistance()` | Already built with min-1-damage floor |
| Group member lookup | Custom group iteration | `group_engine.get_members_in_proximity()` | BFS proximity already implemented |
| Room flags on death | Custom flag management | `room_state.add_room_flag()` | Vocabulary-checked, lazy-decay, already wired in mobs.py at_death |
| Cooldown tracking | Custom timer system | `ability_engine.decrement_cooldowns()` | Already built per D-12 |
| Domain resource management | Custom pool logic | `ability_engine.build/spend_domain_resource()` | Already built per D-13 |

## Formulas from Vault (Canonical)

### HP Derivation (D-05)
```
HP = base_hp + (endurance_stat * hp_per_endurance) + (backend_level * hp_per_level)

Recommended parameters (Claude's discretion):
  base_hp = 50
  hp_per_endurance = 5       # Endurance 10 adds 50 HP
  hp_per_level = 10          # Level 50 adds 500 HP

Low tier (level ~5, Endurance ~8):  50 + 40 + 50 = 140 HP
Mid tier (level ~25, Endurance ~40): 50 + 200 + 250 = 500 HP
High tier (level ~45, Endurance ~80): 50 + 400 + 450 = 900 HP

Note: Mob damage at reference level deals 8-14 per hit. At scale factor ~1.83
(backend 50): ~15-26 per hit. This gives ~35-60 hits to kill a high-tier player,
which is appropriate for long multi-mob encounters.
```

### Stamina Derivation (D-05, D-06)
```
Stamina = base_stamina + (endurance_stat * stam_per_endurance)

Recommended:
  base_stamina = 30
  stam_per_endurance = 2

Stamina costs:
  Room-to-room movement (during combat): 5 stamina
  Special actions: varies per action, typically 10-20
  Basic attacks: 0 (free)
  Abilities: 0 (use domain resource instead)

Stamina recovers between encounters (full reset). No in-combat regen baseline.
```

### Action Budget (D-08, vault spec)
```
actions_per_turn = floor(1 + agility_stat / action_divisor)

Recommended:
  action_divisor = 30

Agility 10:  1 + 0 = 1 action
Agility 30:  1 + 1 = 2 actions
Agility 60:  1 + 2 = 3 actions
Agility 90:  1 + 3 = 4 actions (practical cap)

Damage per action = base_damage / sqrt(actions_per_turn)
  1 action:  100% damage each
  2 actions: ~71% damage each (142% total -- slight advantage)
  3 actions: ~58% damage each (174% total)
  4 actions: ~50% damage each (200% total -- strong but ability-limited)

One ability use per turn (D-09). Extra actions are basic attacks only.
```

### Initiative (D-07)
```
initiative = agility_stat + random.randint(1, 20)

Fixed for entire encounter. Sorted descending. Ties broken by random.
```

### Basic Attack Damage (D-19)
```
For melee:
  raw_damage = random.randint(weapon_damage_min, weapon_damage_max) +
               (strength_stat * stat_scaling_factor)

  stat_scaling_factor = 0.5  (1 point of Strength = 0.5 base damage)

Scaled damage = zone_scaling.get_player_damage_to_mob(raw_damage, mob, character)
Final damage  = zone_scaling.apply_resistance(scaled_damage, element, target)
```

### Ability Damage (D-08, vault spec)
```
ability_base = ability_definition["damage_base"]
primary_stat = character.db.base_stats[ability["scaling_primary"]]
secondary_stat = character.db.base_stats.get(ability.get("scaling_secondary"), 0)

raw_ability_damage = ability_base * (1 + primary_stat * 0.02 + secondary_stat * 0.01)

Scaled and resisted same as basic attacks.
```

### Elite/Boss Scaling (D-21, vault spec)
```
Per level above player backend level:
  +8% incoming damage to player
  +5% damage reduction from player attacks
  +3% avoidance/resistance

Elite: treated as backend_level + 5
  incoming_damage_mult = 1.0 + (5 * 0.08) = 1.40
  damage_reduction = 5 * 0.05 = 0.25
  avoidance = 5 * 0.03 = 0.15

Boss: treated as backend_level + 10
  incoming_damage_mult = 1.0 + (10 * 0.08) = 1.80
  damage_reduction = 10 * 0.05 = 0.50
  avoidance = 10 * 0.03 = 0.30
```

### Stat Growth Through Use (D-04)
```
Action-to-stat mapping:
  Melee hit lands         -> +strength_xp
  Successful dodge        -> +agility_xp
  Damage taken (survived) -> +endurance_xp
  Spell cast              -> +mana_xp
  Cooldown reduction used -> +acuity_xp (per ability with CDR)
  Social ability lands    -> +presence_xp
  Resonance ability used  -> +resonance_stat_xp

Growth rate: diminishing returns curve (same as domain XP)
  Stat 0-25:  full rate
  Stat 25-50: 75% rate
  Stat 50-75: 40% rate
  Stat 75-90: 10% rate
  Stat 90-100: 2% rate

Per-action XP gain: 1-3 points per qualifying action
Stats stored on character.db.base_stats dict, accumulated on ndb during session
```

## Base Attribute Descriptors (D-03)

All 70 descriptors -- 10 tiers per stat, each with unique flavor.

### Strength
| Range | Descriptor |
|-------|------------|
| 0-9 | Feeble |
| 10-19 | Frail |
| 20-29 | Average |
| 30-39 | Sturdy |
| 40-49 | Strong |
| 50-59 | Powerful |
| 60-69 | Mighty |
| 70-79 | Formidable |
| 80-89 | Colossal |
| 90-100 | Prodigious |

### Agility
| Range | Descriptor |
|-------|------------|
| 0-9 | Sluggish |
| 10-19 | Clumsy |
| 20-29 | Steady |
| 30-39 | Nimble |
| 40-49 | Quick |
| 50-59 | Deft |
| 60-69 | Swift |
| 70-79 | Fleet |
| 80-89 | Blinding |
| 90-100 | Ethereal |

### Endurance
| Range | Descriptor |
|-------|------------|
| 0-9 | Fragile |
| 10-19 | Delicate |
| 20-29 | Hardy |
| 30-39 | Tough |
| 40-49 | Resilient |
| 50-59 | Stout |
| 60-69 | Stalwart |
| 70-79 | Unyielding |
| 80-89 | Ironforged |
| 90-100 | Indomitable |

### Mana
| Range | Descriptor |
|-------|------------|
| 0-9 | Inert |
| 10-19 | Dim |
| 20-29 | Flickering |
| 30-39 | Luminous |
| 40-49 | Radiant |
| 50-59 | Brilliant |
| 60-69 | Blazing |
| 70-79 | Incandescent |
| 80-89 | Resplendent |
| 90-100 | Transcendent |

### Acuity
| Range | Descriptor |
|-------|------------|
| 0-9 | Dull |
| 10-19 | Unfocused |
| 20-29 | Attentive |
| 30-39 | Sharp |
| 40-49 | Keen |
| 50-59 | Precise |
| 60-69 | Insightful |
| 70-79 | Piercing |
| 80-89 | Prescient |
| 90-100 | Omniscient |

### Presence
| Range | Descriptor |
|-------|------------|
| 0-9 | Invisible |
| 10-19 | Meek |
| 20-29 | Noticeable |
| 30-39 | Engaging |
| 40-49 | Commanding |
| 50-59 | Imposing |
| 60-69 | Magnetic |
| 70-79 | Sovereign |
| 80-89 | Overwhelming |
| 90-100 | Legendary |

### Resonance
| Range | Descriptor |
|-------|------------|
| 0-9 | Deaf |
| 10-19 | Faint |
| 20-29 | Attuned |
| 30-39 | Receptive |
| 40-49 | Sensitive |
| 50-59 | Harmonic |
| 60-69 | Resonant |
| 70-79 | Reverberant |
| 80-89 | Symphonic |
| 90-100 | Primordial |

### Point-Buy Recommendation (Claude's Discretion)
```
Base value per stat: 10 (all 7 stats start here)
Bonus points to distribute: 20
Per-stat maximum at creation: 25 (base 10 + max 15 from points)
Per-stat minimum: 5 (can reduce below base by 5 to free more points)

This gives:
  Focused build (2 stats at 25): 10+15+15 = 40 spent, 10 to spread
  Balanced build (all stats ~13): 3 each across 7 = 21 -- slight overspend, drop one

Ancestry modifiers apply AFTER point buy (additive, range -3 to +5).
```

## Status Effect Compound Matrix (Vault Canonical)

### Additive Compounds (both effects persist + new effect added)
| Effect 1 | Effect 2 | Compound Result | Mechanical Effect |
|----------|----------|-----------------|-------------------|
| Poison | Slow | Venom Lag | Both persist + bonus poison damage per tick |
| Weaken | Poison | Corruption | Both persist + poison stack ceiling +1 |
| Slow | Root | Petrify | Both persist + extended duration, breaks on damage |

### Consuming Compounds (both consumed, replaced by result)
| Effect 1 | Effect 2 | Compound Result | Mechanical Effect |
|----------|----------|-----------------|-------------------|
| Burn | Wet | Steam | Both consumed; burst damage = 75% remaining Burn DoT; action budget -1 next round; armor reduction 2 rounds |

### Status Effect Constants
```python
STACKABLE_EFFECTS = {
    "poison": {"max_stacks": 5, "base_damage": 8, "diminishing": [8, 5, 3, 2, 1]},
    "bleed":  {"max_stacks": 4, "base_damage": 6, "diminishing": [6, 4, 3, 2]},
    "burn":   {"max_stacks": 4, "base_damage": 7, "diminishing": [7, 5, 3, 2]},
    "weaken": {"max_stacks": 3, "reduction_per_stack": 0.08},
    "drain":  {"max_stacks": 2, "drain_per_stack": 5},
}

NON_STACKABLE_EFFECTS = {
    "slow":  {"action_budget_penalty": 1},
    "root":  {"prevents_flee": True},
    "blind": {"miss_chance_increase": 0.25},
    "stun":  {"skip_turn": True},
    "charm": {"skip_turn": True, "no_hostile_action": True},
    "haste": {"action_budget_bonus": 1},
    "wet":   {"burn_chance_reduction": 0.50, "burn_magnitude_reduction": 0.25,
              "action_penalty_on_apply": 1},
}
```

## CombatScript State Design

### What CombatScript Holds (db -- persistent across reload)
```python
self.db.combatant_ids = []          # list of dbrefs in initiative order
self.db.round_number = 1
self.db.current_turn_index = 0
self.db.initiative_order = []       # [{id, initiative_value}] sorted desc
self.db.is_group_combat = False     # True if any player is in a group
self.db.round_timeout = 30          # seconds, only used if is_group_combat
```

### What CombatScript Holds (ndb -- volatile, rebuilt on reload)
```python
self.ndb.turn_timer_id = None       # delay() handle for timeout cancel
self.ndb.pending_charged = {}       # {char_id: {ability_id, rounds_left}}
self.ndb.call_for_help_count = 0    # call_for_help cap (max 3 per encounter)
```

### What Combatants Hold (ndb -- volatile per encounter)
```python
character.ndb.combat_handler = self         # back-reference to CombatScript
character.ndb.combat_target_id = None       # auto-target
character.ndb.active_effects = []           # status effect list
character.ndb.actions_remaining = 0         # this turn's budget
character.ndb.ability_used_this_turn = False # one ability per turn cap
```

### CombatScript Interaction with Room/Combatants

1. **Start:** `start_combat(room, attacker, defender)` creates script on room. Adds CombatCmdSet to all players. Mobs don't need CmdSets.
2. **Join:** Additional mobs/players join mid-combat via `add_combatant()`. Re-sort initiative with new member inserted at their initiative value.
3. **Player turn:** Script calls `prompt_player_turn(character)` which shows available abilities and waits. Player command triggers `process_player_action()`.
4. **Mob turn:** Script calls `process_mob_turn(mob)` which delegates to `combat_ai.select_mob_action()`.
5. **Round end:** After all combatants have acted, tick effects, decrement cooldowns, check death conditions, increment round.
6. **Cleanup:** When combat ends (all enemies dead, all players fled, etc.), remove CombatCmdSet from players, call `self.delete()`.

### CombatCmdSet Design
```python
class CombatCmdSet(CmdSet):
    """Added to players when combat begins. Replaces default movement."""
    mergetype = "Replace"
    priority = 10
    no_exits = True    # Block normal exit traversal during combat

    # Contains: CmdAttack, CmdUseAbility, CmdFlee, CmdTarget, CmdPass
```

## Corpse Container Design (D-27)

```python
class CorpseContainer(SoravelonContainer):
    """
    Spawned on mob death. Contains loot drops.
    Three loot phases: locked -> open -> decayed (deleted).
    """
    GRACE_PERIOD = 120      # 2 minutes killer-locked
    OPEN_PERIOD = 300       # 5 minutes open to all

    def at_object_creation(self):
        super().at_object_creation()
        self.db.killer_id = None
        self.db.killer_group_leader_id = None
        self.db.loot_phase = "locked"
        self.db.mob_key = ""
        self.db.mob_rarity = "normal"
        self.locks.add("get:false()")  # corpses cannot be picked up

    def can_loot(self, character):
        """Check if character can access this corpse's contents."""
        if self.db.loot_phase == "locked":
            # Killer or killer's group only
            if character.id == self.db.killer_id:
                return True, None
            if self.db.killer_group_leader_id:
                leader_id = getattr(character.ndb, 'group_leader_id', None)
                if leader_id == self.db.killer_group_leader_id:
                    return True, None
            return False, "This corpse belongs to someone else."
        if self.db.loot_phase == "open":
            return True, None
        return False, "Nothing remains."
```

Decay uses `evennia.utils.utils.delay()` -- NOT a Script:
```python
from evennia.utils.utils import delay

def spawn_corpse(mob, killer):
    corpse = create_object(CorpseContainer, key=f"corpse of {mob.key}", location=mob.location)
    corpse.db.killer_id = killer.id
    # ... populate with loot ...

    # Schedule phase transitions
    delay(CorpseContainer.GRACE_PERIOD, _transition_corpse, corpse.id, "open")
    delay(CorpseContainer.GRACE_PERIOD + CorpseContainer.OPEN_PERIOD,
          _transition_corpse, corpse.id, "decayed")

def _transition_corpse(corpse_id, new_phase):
    from evennia import search_object
    results = search_object("#" + str(corpse_id))
    if not results:
        return
    corpse = results[0]
    if new_phase == "decayed":
        corpse.delete()
    else:
        corpse.db.loot_phase = new_phase
```

## Wiring ability_engine Stubs to Real Combat

The 10 stub handlers in `ability_engine.py` need to be replaced with real combat resolution:

| Handler | Stub Now | Wire To |
|---------|----------|---------|
| `_handle_damage` | Returns text | `combat_engine.resolve_damage(character, ability, target)` |
| `_handle_dot` | Returns text | `status_effects.apply_effect(target, ability.effect_type, ...)` |
| `_handle_buff` | Returns text | `status_effects.apply_buff(character, ability.buff_type, ...)` |
| `_handle_debuff` | Returns text | `status_effects.apply_effect(target, ability.debuff_type, ...)` |
| `_handle_utility` | Returns text | Context-dependent; utility effects vary |
| `_handle_social` | Returns text | `combat_engine.resolve_social(character, ability, target)` |
| `_handle_tactical` | Returns text | `combat_engine.resolve_tactical(character, ability, targets)` |
| `_handle_compound_trigger` | Returns text | `status_effects.check_compound_triggers(target)` |
| `_handle_heal` | Returns text | `combat_engine.resolve_heal(character, ability, target)` |
| `_handle_status` | Returns text | `status_effects.apply_effect(target, ability.status_type, ...)` |

Each handler returns `(success: bool, message: str)` per project convention. The `use_ability()` dispatch function already handles cooldown set and room flag writing -- handlers only need to resolve the effect.

## OOB Combat Integration

### push_combat_update Schema (fills Phase 6 placeholder)
```python
{
    "state": "active",              # active / player_turn / waiting / ended
    "round": 3,
    "your_turn": True,
    "actions_remaining": 2,
    "combatants": [
        {
            "id": 42,
            "name": "Forest Wolf",
            "hp_pct": 0.65,         # percentage, not raw number
            "is_mob": True,
            "effects": ["poison"],
            "is_current": False,
        },
    ],
    "available_abilities": [
        {"id": "momentum_strike", "name": "Momentum Strike", "ready": True},
        {"id": "bladestorm_sig1", "name": "Tempest Cleave", "ready": False, "cooldown": 2},
    ],
    "target_id": 42,
    "last_action": "You strike the Forest Wolf for 45 damage.",
}
```

### push_stat_update Schema (fills Phase 6 placeholder)
```python
{
    "hp": 340,
    "hp_max": 500,
    "stamina": 28,
    "stamina_max": 50,
    "domain_resource": {"type": "momentum", "current": 65, "max": 100},
    "conditions": ["poison_2", "haste"],  # effect_type + stack count if stackable
}
```

## Common Pitfalls

### Pitfall 1: ndb State Lost on Server Reload
**What goes wrong:** All ndb combat state (effects, targets, cooldowns) is lost on `evennia reload`.
**Why it happens:** ndb is volatile by design.
**How to avoid:** CombatScript stores critical state on db (combatant_ids, round_number, initiative_order). The `at_start()` hook rebuilds ndb state from db state. Active effects need to be stored on db if combat must survive reload.
**Warning signs:** Combat "freezes" after reload -- players have CombatCmdSet but no combat handler reference.
**Recommendation:** Store `active_effects` on CombatScript.db as a dict keyed by combatant_id, not on individual combatant.ndb. This is the only way to survive reload.

### Pitfall 2: CombatScript Outlives Its Combatants
**What goes wrong:** Script keeps running after all combatants are dead or disconnected.
**Why it happens:** No cleanup check in advance_turn().
**How to avoid:** Every call to `advance_turn()` must check: are there still valid combatants? If not, `end_combat()`. Guard pattern from PatrolScript (check `mob.pk`).
**Warning signs:** Orphaned CombatScripts accumulating on rooms.

### Pitfall 3: SaverDict Mutation on ndb Lists
**What goes wrong:** Appending to ndb list doesn't persist.
**Why it happens:** Evennia's SaverDict requires copy-modify-reassign for list mutations.
**How to avoid:** Always copy: `effects = list(target.ndb.active_effects or []); effects.append(new); target.ndb.active_effects = effects`
**Warning signs:** Effects "disappearing" after being applied.

### Pitfall 4: F() Race on HP Updates
**What goes wrong:** Concurrent HP modifications produce incorrect results.
**Why it happens:** Two damage applications read the same HP, both write HP-damage.
**How to avoid:** HP is on `mob.db.hp` (Evennia attribute, not Django field). Evennia attributes don't support F() expressions. Since combat is turn-based and sequential (one action resolves at a time), this is not actually a race condition. Just read-modify-write directly.
**Warning signs:** None expected -- turn-based sequential processing eliminates concurrency.

### Pitfall 5: CombatCmdSet Not Removed on Disconnect
**What goes wrong:** Player reconnects with CombatCmdSet still active but no combat handler.
**Why it happens:** `at_pre_unpuppet` doesn't clean up combat state.
**How to avoid:** In `Character.at_pre_unpuppet()`, check for and remove CombatCmdSet. In `CombatScript.at_start()`, validate all player combatants are still connected.
**Warning signs:** Player locked in combat commands after reconnect with no active fight.

### Pitfall 6: Corpse delay() Lost on Reload
**What goes wrong:** Corpse never decays because `delay()` callbacks are lost on server reload.
**Why it happens:** `delay()` is in-memory only.
**How to avoid:** Store `corpse.db.decay_at` timestamp. Add a periodic cleanup sweep (60s ticker) that finds corpses past their decay time and deletes them. Belt-and-suspenders: delay() for normal operation, ticker for crash recovery.
**Warning signs:** Rooms accumulating old corpses that never despawn.

### Pitfall 7: Mob AI Infinite Loop
**What goes wrong:** Mob with no usable abilities (all on cooldown, no basic attack defined) causes infinite loop in ability selection.
**Why it happens:** AI selection loop retries finding an ability.
**How to avoid:** Always have a fallback: if no ability is available, mob performs a basic attack (damage_min to damage_max, physical element). Every mob has these stats.
**Warning signs:** Server freeze during mob turn.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Evennia test utilities + unittest.TestCase + MagicMock |
| Config file | None -- uses `evennia test --settings server.conf.settings tests/` |
| Quick run command | `evennia test --settings server.conf.settings tests/test_combat_engine.py -x` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CMB-01 | Ability effects resolve to real damage/status | unit | `evennia test --settings server.conf.settings tests/test_combat_engine.py -x` | Wave 0 |
| CMB-01 | Status compound triggers fire correctly | unit | `evennia test --settings server.conf.settings tests/test_status_effects.py -x` | Wave 0 |
| CMB-01 | CombatScript turn advancement works | unit | `evennia test --settings server.conf.settings tests/test_combat_script.py -x` | Wave 0 |
| CMB-02 | Zone scaling applies during combat damage | unit | `evennia test --settings server.conf.settings tests/test_combat_engine.py::TestScalingIntegration -x` | Wave 0 |
| CMB-03 | Mob AI selects abilities by weight/cooldown/condition | unit | `evennia test --settings server.conf.settings tests/test_combat_ai.py -x` | Wave 0 |
| CMB-04 | Group loot mode applies to corpse container | unit | `evennia test --settings server.conf.settings tests/test_combat_engine.py::TestCorpseLocking -x` | Wave 0 |
| -- | Base attribute descriptors return correct text | unit | `evennia test --settings server.conf.settings tests/test_base_attributes.py -x` | Wave 0 |
| -- | Point-buy validation enforces constraints | unit | `evennia test --settings server.conf.settings tests/test_base_attributes.py::TestPointBuy -x` | Wave 0 |
| -- | Stat growth accumulates correctly | unit | `evennia test --settings server.conf.settings tests/test_base_attributes.py::TestStatGrowth -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `evennia test --settings server.conf.settings tests/test_combat_engine.py tests/test_status_effects.py tests/test_base_attributes.py -x`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_combat_engine.py` -- covers CMB-01, CMB-02, CMB-04
- [ ] `tests/test_combat_script.py` -- covers CMB-01 turn management
- [ ] `tests/test_combat_ai.py` -- covers CMB-03
- [ ] `tests/test_status_effects.py` -- covers CMB-01 compound triggers
- [ ] `tests/test_base_attributes.py` -- covers descriptor display, point-buy, stat growth

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Per-mob combat scripts | Single room-attached CombatHandler | Evennia 1.0+ best practice | One script manages all combatants; cleaner cleanup |
| Tick-based turn polling | Event-driven with delay() timeout | Current Evennia docs | Better performance, no wasted cycles |
| Global TickerHandler for combat | Script-based per-encounter | NodeScript uses global tick, combat should NOT | Combat is per-room, not global |

## Open Questions

1. **Stat growth batch commit timing**
   - What we know: Domain XP uses ndb accumulators flushed every 600s by SessionCommitScript
   - What's unclear: Should base stat XP use the same flush mechanism or a separate one?
   - Recommendation: Piggyback on existing SessionCommitScript -- add stat XP flush alongside domain XP flush

2. **Combat survival across server reload**
   - What we know: db attributes survive reload, ndb does not
   - What's unclear: Is mid-combat reload a supported scenario or accept-and-restart?
   - Recommendation: Store enough on CombatScript.db to resume (combatant_ids, initiative, round, effects). Rebuild CombatCmdSets in at_start(). Accept that the current turn resets.

3. **Charged ability interruption**
   - What we know: D-10 says charged abilities take 1-2 rounds. Players can interrupt with Stun/Root per vault.
   - What's unclear: Does Root interrupt a charge, or only Stun? Vault says "Stun or Root" for mob casts.
   - Recommendation: Both Stun and Root interrupt charges (per vault mob casting rules). Consistent for player and mob charges.

## Sources

### Primary (HIGH confidence)
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` -- Combat System Foundation, Core Stats, Domain Resources, Status Effects, Death/Recovery
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` -- Mob Stats, Targeting, Ability Schema, Resistance Calculation, Disposition System
- `C:\Obsidian\brain\Soravelon\soravelon-spawn-system.md` -- SpawnRecord model, death hook, respawn scheduling
- [Evennia Scripts Documentation](https://www.evennia.com/docs/latest/Components/Scripts.html) -- Script lifecycle hooks
- [Evennia Turn-based Combat System](https://www.evennia.com/docs/latest/Howtos/Turn-based-Combat-System.html) -- CombatHandler pattern

### Secondary (MEDIUM confidence)
- Existing codebase patterns: NodeScript, PatrolScript, FlightScript -- established Script patterns in this project
- Existing ability_engine.py, zone_scaling.py, mob_disposition.py -- integration points verified by code reading

### Tertiary (LOW confidence)
- Exact balancing numbers (damage formulas, action budget divisors, HP scaling) -- reasonable starting values but will need tuning in playtesting

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies, all Evennia built-in
- Architecture: HIGH -- follows established project patterns and Evennia best practices
- Formulas: MEDIUM -- vault provides direction, exact numbers are Claude's discretion with reasonable defaults
- Pitfalls: HIGH -- derived from existing project pitfalls and Evennia documentation
- Descriptors: MEDIUM -- creative content, may need refinement during implementation

**Research date:** 2026-03-26
**Valid until:** 2026-04-26 (stable domain -- game design, not library versions)
