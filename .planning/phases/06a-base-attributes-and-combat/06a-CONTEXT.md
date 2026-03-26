# Phase 6a: Base Attributes & Combat System - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the character base attribute system (7 stats, point-buy at creation, descriptor-based display, stat growth through use) and the full turn-based combat system (CombatScript, initiative, action budget, damage formula, status effects with compounds, corpse containers, flee mechanics). This phase makes combat functional — players can fight mobs using abilities from Phase 5 with real damage resolution.

</domain>

<decisions>
## Implementation Decisions

### Base Attribute System
- **D-01:** 7 base stats: Strength, Agility, Endurance, Mana, Acuity, Presence, Resonance. Each governs specific combat and world-interaction aspects per vault spec.
- **D-02:** Classic point-buy at character creation. All stats start at a base value, player distributes N bonus points. Min per stat = base, max per stat = base + cap. Ancestry provides modifiers on top.
- **D-03:** Player-facing display uses descriptors ONLY — no numbers shown. 10 descriptors per stat, each stat has unique flavor words (e.g., Strength: "Feeble" → "Prodigious", Agility: "Sluggish" → "Ethereal"). Research designs all 70 descriptors (7 stats × 10 tiers).
- **D-04:** Stats grow through ACTION-SPECIFIC use, not domain XP. Melee hits grow Strength, successful dodges grow Agility, taking damage grows Endurance. Granular per-action tracking required.
- **D-05:** HP derived from Endurance attribute + level modifier. Three resource pools: HP (survival), Stamina (special actions + room-to-room movement), Domain Resource (guild-specific from Phase 5).
- **D-06:** Stamina fuels special actions and room-to-room movement during combat. Basic attacks and abilities do NOT cost stamina.

### Combat Model
- **D-07:** Turn-based combat with FIXED initiative per encounter. Initiative = f(Agility stat). Each combatant has individual initiative slot. Re-roll NOT per round — fixed for entire encounter.
- **D-08:** Full ACTION BUDGET system per vault spec. Actions per turn = f(Speed/Agility). Damage per action = base_damage / actions_per_turn modifier. Ability damage = base_damage × primary_stat_value.
- **D-09:** One ability use per turn maximum. Stats can grant multiple basic attacks per turn. Weapon speed + character stat determines number of basic attacks.
- **D-10:** Abilities have cooldowns (decrement at round end). Charged abilities (1-2 round cast) declared on acting character's turn; character auto-attacks during charge; resource generates during charge.
- **D-11:** Status effects tick at round end. Cooldowns decrement at round end.

### Combat Architecture
- **D-12:** CombatScript attached to room manages combat. Drives initiative order, round progression, mob AI turns. Removed when combat ends. Same Script pattern as NodeScript/PatrolScript/FlightScript.
- **D-13:** Disposition-driven auto-engage. Aggressive mobs attack on sight based on disposition. `is_hunter` flag enables grid-distance aggro (BFS pathfinding to player within N rooms). NOT all aggressive mobs hunt — only flagged ones.
- **D-14:** Auto-target + override. Player auto-targets last attacked mob. Can switch with 'target <mob>'. Persistent target on ndb.
- **D-15:** Individual initiative (interleaved player + mob turns). NOT group phases.

### Turn UI
- **D-16:** On player's turn: show list of abilities off cooldown (ready to use) and abilities on cooldown with rounds remaining. NOT hints — actual ability list.
- **D-17:** Hybrid input: show available options but accept typed commands ('attack goblin', 'use fireball goblin', 'flee').
- **D-18:** Round timer: WAIT INDEFINITELY for solo play. TIMED ROUNDS (configurable) for group combat. Auto-attack on timeout.

### Damage & Scaling
- **D-19:** Weapon base damage + stat scaling. Weapon has base damage range. Relevant stat (Strength for melee, etc.) adds bonus. Zone scaling applies as multiplier. Ability damage is separate formula from vault spec.
- **D-20:** Wide damage scale per vault: Low tier 50-500 HP, Mid tier 500-5000 HP, High tier thousands. Crits for 1000+ at appropriate tiers are a design goal.
- **D-21:** Elite mobs: treated as backend level +5 (+40% incoming damage, +25% damage reduction, +15% avoidance). Boss mobs: backend level +10 (+80%/+50%/+30%). Per-level scaling: +8%/+5%/+3%.
- **D-22:** Mob resistances per vault: physical, fire, ice, poison, lightning, arcane, none. Resistance = float 0.0-1.0 damage reduction per element.

### Status Effects & Compounds
- **D-23:** Status effects on ndb.active_effects list. Each entry: type, duration, source, magnitude. Cleared on encounter end. Tick down each round.
- **D-24:** Full compound effect system wired in this phase. Additive compounds (Poison+Slow=Venom Lag, Weaken+Poison=Corruption, Slow+Root=Petrify). Consuming compounds (Burn+Wet=Steam). Per vault spec.
- **D-25:** Stackable effects: Poison (5), Bleed (4), Burn (4), Weaken (3), Drain (2). Non-stackable: Slow, Root, Blind, Stun, Charm, Haste, Wet. Stronger replaces weaker for non-stackable.

### Death & Corpse
- **D-26:** Player death: per vault — respawn at nearest hub city medic (naked). Corpse spawns at death location with all carried equipment. Death recovery tiers (Municipal Medic → Death Insurance → Recovery Crew → Underworld Option).
- **D-27:** Mob death: corpse container model. Timed decay. Killer-locked loot (only killer or their group can loot for grace period, then opens to all, then decays). Room flags written on mob death (blood_soaked, fading_life, power_vacuum — already exist from Phase 5).
- **D-28:** Flee: speed check + skill check + exit. Some skills give bonuses to escaping (e.g., Stealth). Failure = lose your turn. Can't flee while rooted/stunned. On success, character moves to random adjacent room.

### Group Combat
- **D-29:** Individual initiative per player (interleaved with mobs). NOT all-players-then-all-mobs.
- **D-30:** Group loot uses existing group_engine loot modes (Personal, FFA, Round Robin, Need/Pass). Corpse container is killer-locked to killer's group.

### Claude's Discretion
- Exact point-buy numbers (total points, base value, per-stat cap)
- Exact action budget formula parameters
- CombatScript tick interval vs event-driven architecture
- Corpse container decay timer duration
- Exact stamina pool derivation formula
- Status effect duration balancing values

</decisions>

<specifics>
## Specific Ideas

- "A fierce warrior has 'prodigious' strength but a 'dull' Acuity" — descriptors must be relative to the stat itself and feel natural for that attribute
- Domain resource system from Phase 5 is the third pool (Momentum for Combat guild, Focus for Subterfuge, Balance for Naturalism, etc.)
- Speed gives more actions per turn but lower damage per action — universally useful but doesn't dominate because each ability scales from a different primary stat
- Charged abilities auto-attack during charge turns, resource still generates
- Status effects are important combat tools, not niceties — DoT builds are legitimate and competitive

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Combat System
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Combat System Foundation — Turn structure, action budget, speed/damage tradeoff, damage scale, elite/boss scaling
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Core Stat System — 7 base stats with governs table
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Domain Resources — 10 domain resources with unique mechanics per guild
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Status Effect System — Stackable/non-stackable effects, compound effects, node interactions

### Mob Combat Reference
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Mob Targeting — Simple targeting (last attacker, re-roll on flee)
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Mob Disposition System — Disposition float, behavior thresholds
- `C:\Obsidian\brain\Soravelon\soravelon-mobs.md` §Mob Ability System — Full ability schema, element/status/targeting/condition vocabularies, cooldown tracking, resistance calculation

### Death & Recovery
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` §Death and Recovery System — Recovery tiers, corpse mechanics, Hunted state

### Existing Code
- `world/ability_engine.py` — Phase 5 ability dispatch with stub effect handlers (wire to real combat here)
- `world/ability_registry.py` — Ability definitions with effect types, costs, cooldowns
- `world/zone_scaling.py` — Per-player logarithmic scaling, mob HP initialization
- `world/mob_disposition.py` — Disposition float computation
- `world/room_state.py` — Room flags written on mob death

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `world/ability_engine.py:use_ability()` — Dispatch framework exists with 10 stub handlers. Wire to real combat damage resolution.
- `world/zone_scaling.py:calculate_player_scale_factor()` — Logarithmic scaling ready. `initialize_mob_combat_stats()` sets mob HP/damage.
- `world/mob_disposition.py:get_mob_disposition()` — Returns -1.0 to +1.0. Use to determine auto-engage behavior.
- `world/room_state.py:add_room_flag()` — Already writes combat-relevant flags (blood_soaked, burning, etc.)
- `typeclasses/mobs.py:at_death()` — Already writes room flags on death. Extend for corpse creation and loot.
- `world/group_engine.py` — Group membership and loot mode queries ready for combat integration.
- `world/oob_publisher.py` — Push combat state updates to client.

### Established Patterns
- CombatScript follows the Script pattern: NodeScript (30s tick), PatrolScript (per-mob), FlightScript (per-flight). CombatScript attaches to room, manages turn state.
- `(bool, str)` return tuples for combat resolution functions.
- ndb for volatile combat state (cooldowns, targets, active_effects). db for persistent state (stats, equipment).
- F() expressions for any balance/HP updates that could race.

### Integration Points
- Character.at_object_creation() needs base stat initialization
- Character puppet hook needs combat state ndb init
- Ability engine effect handlers need real damage/status resolution
- OOB publisher needs combat message type
- Group engine loot modes need corpse container integration

</code_context>

<deferred>
## Deferred Ideas

- Full threat engine (taunt, aggro tables, tank mechanics) — post-launch per vault
- PvP combat — not in scope
- Equipment stat bonuses — Phase 7 (content) or equipment phase
- Rested XP bonus system — separate utility phase
- Dragon companion combat integration — companion design pass

</deferred>

---

*Phase: 06a-base-attributes-and-combat*
*Context gathered: 2026-03-26*
