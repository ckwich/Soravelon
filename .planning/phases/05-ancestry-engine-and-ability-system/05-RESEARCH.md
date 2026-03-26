# Phase 5: Ancestry Engine and Ability System - Research

**Researched:** 2026-03-25
**Domain:** Ancestry engine, ability registry/dispatcher, room state system, guild discovery wiring
**Confidence:** HIGH

## Summary

Phase 5a builds the structural framework for the ancestry and ability systems without authoring individual ability definitions (that is Phase 5b). The work decomposes into six clear verticals: (1) ancestry engine with trait application and starting standings, (2) ability registry as a Python constant dict with effect-type dispatch, (3) CmdUseAbility dispatcher routing all 330+ abilities through one command, (4) room state system for temporary flags with lazy decay, (5) guild discovery wiring into the existing commit_session_xp flow, and (6) new player-facing commands (domains, abilities, ancestry selection, guild join).

The existing codebase provides strong foundations. Phase 4 delivered `world/guild_engine.py` (1692 lines) with GUILDS, SUBCLASSES, FINGERPRINTS registries, GTS computation, `check_guild_eligibility()`, and `join_guild()`. The `world/world_state.py:commit_session_xp()` function is the natural hook point for guild discovery. The `world/mob_disposition.py` already has ANCESTRY_FACTION_MODIFIERS and `get_ancestry_modifier()` that reads `character.db.ancestry` -- the ancestry engine just needs to SET this value. The Character typeclass already initializes `db.ancestry = None`.

All design decisions are locked in CONTEXT.md (D-01 through D-27). The vault documents (soravelon-ancestries.md, soravelon-abilities.md, soravelon-guilds.md, soravelon-fingerprints.md, soravelon-room-state.md) provide complete data models, flag vocabularies, and implementation specifications. Research confirms these are internally consistent and compatible with the existing codebase.

**Primary recommendation:** Build vertically -- ancestry engine and room state are independent of the ability registry and can be developed in parallel. The ability registry structure and CmdUseAbility dispatcher are the critical-path items that Phase 5b depends on.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Phase 5 splits into 5a (engine + framework) and 5b (ability content authoring).
- **D-02:** Phase 5b uses collaborative in-conversation review, domain by domain. Claude proposes abilities for one domain (15 abilities + 9 subclass signatures), user reviews/revises, repeat for all 10 domains.
- **D-03:** 15 abilities per domain (3-4 per tier across 4 tiers) x 10 domains = 150 domain abilities. All accessible by primary guild members.
- **D-04:** 2 signature abilities per subclass x 90 subclasses = 180 signature abilities. Unique to specific subclass, not in any domain pool.
- **D-05:** Per character at max GTS: 15 primary domain + 4 secondary picks (1 of 3 per tier, player's choice) + 2 signatures = 21 known abilities. Active loadout: 8 selected from known pool.
- **D-06:** Signature 1 unlocks at Tier 3 (GTS 50+). Signature 2 unlocks at Tier 4 (GTS 85+).
- **D-07:** Secondary domain ability pick is permanent per tier -- player chooses 1 of 3 from secondary domain's tier pool. Two characters with same subclass can have different secondary picks.
- **D-08:** AbilityDefinition as Python constants in `world/ability_registry.py`. ABILITIES dict keyed by ability_id. Same pattern as GUILDS/SUBCLASSES in guild_engine.py.
- **D-09:** Full field shape from vault: id, name, domain, tier, resource_cost, resource_type, cooldown, charge_turns, effect_type, scaling_primary, scaling_secondary, application_chance, description, room_flag_written, attuned_variants. Combat-specific values stubbed but not wired until Phase 6.
- **D-10:** CmdUseAbility uses effect-type dispatch. ~10 handlers (damage, dot, buff, debuff, utility, social, tactical, compound_trigger, etc.) cover all 330 abilities. No per-ability callables.
- **D-11:** CharacterAbility Django model in world/models.py. Fields: character FK, ability_id, unlocked_at (timestamp), times_used. Relational data per project convention.
- **D-12:** Ability cooldowns on character.ndb.ability_cooldowns dict. Remaining rounds per ability. Cleared on encounter end. Per-encounter, volatile.
- **D-13:** Domain resource tracking: character.ndb.domain_resource = {type, current, max}. Resource type set from guild fingerprint. Build/decay/spend functions exist in 5a but only called from ability stubs. Combat system (Phase 6) wires real effects.
- **D-14:** New `world/ancestry_engine.py` module. ANCESTRY_TRAITS dict with trait data for Human, Kau'roran, Veth, Selvar. Starting standing application functions. Starting ability tracking.
- **D-15:** Ancestry starting abilities tracked as character.ndb.ancestry_ability_used (boolean, reset at encounter end). Each ancestry has exactly one starting ability, all once-per-combat.
- **D-16:** Ancestry selection: at_object_creation sets db.ancestry to None. CmdSetAncestry command lets player choose. Starting standings applied via modify_standing() on selection. Ancestry traits apply immediately.
- **D-17:** Post-XP-commit hook in commit_session_xp(). After domain scores update, call check_guild_eligibility(). If eligible and no guild, send a guild-flavored in-game recruitment message to the character.
- **D-18:** Guild induction: lightweight CmdJoinGuild stub in 5a. Shows NPC dialogue as text prompts (choose from menu). Recommends highest-scoring secondary but offers all qualified options. Replaced by proper NPC interaction in Phase 6.
- **D-19:** When GTS crosses a tier threshold, player receives a guild-flavored notification message. Must visit guild hall and run a claim command to unlock. Manual claim, not auto-add.
- **D-20:** Secondary domain ability selection happens at guild hall claim -- player sees 3 options from secondary domain's tier pool, picks 1. Permanent choice.
- **D-21:** Build `world/room_state.py` in Phase 5a. Module implements FLAG_VOCABULARY, lazy decay on ndb, get_room_flags(), add_room_flag(), remove_room_flag(), get_dominant_flag(), SENSE_PRIORITY.
- **D-22:** Resonance Sense passive: after each move and end-of-combat-round, Resonance-primary characters see a one-line atmospheric descriptor from SENSE_DISPLAY. Information only, not a buff.
- **D-23:** Attuned ability variants: ability definitions include attuned_variants dict keyed by room flag. When player uses ability and matching flag is active, present choice (standard vs attuned at extra resource cost). Stub as y/n prompt; auto_attune config deferred.
- **D-24:** Add `add_room_flag` to action vocabulary for builder-authored triggers. Flag writers for mob death (blood_soaked, fading_life, power_vacuum) wire into existing at_death in Phase 5a.
- **D-25:** Build `domains` command in Phase 5a. Shows domain scores as descriptors (Practiced, Skilled, etc), guild membership, GTS tier label, subclass name. Remnance hidden until character.db.remnance_discovered flag is True. When discovered, shows existing score retroactively.
- **D-26:** Build `abilities` command stub showing known abilities and active loadout.
- **D-27:** Update guild_engine.py SUBCLASSES dict -- Ironwright hook changed to "Builds weapons mid-battle -- improvised, brutal, adaptive; no companion -- Engineering knowledge applied to self and weapons".

### Claude's Discretion
- Exact text of guild recruitment messages per guild
- CmdJoinGuild text prompt flow details
- Ability registry Python dict field naming (within the vault-defined shape)
- Test organization and granularity
- Room state integration with existing at_death (mob death flag writers)
- Domain proficiency descriptor display formatting in `domains` command

### Deferred Ideas (OUT OF SCOPE)
- ABL-04 (360 ability definitions) -- Phase 5b, collaborative guild-by-guild authoring
- Combat system integration -- Phase 6. Ability effects are stubbed in 5a, wired in 6.
- NPC template system for guild induction -- Phase 6. 5a uses lightweight command stubs.
- auto_attune configuration -- later command system pass
- Sense display for non-Resonance -- future design (Remnance variant TBD)
- Full attuned variant UI polish -- Phase 6 combat polish
- Guild induction questlines -- content phase (10 questlines)
- Vaelborn discovery trigger sequence -- content design pass
- Companion system integration -- Milestone 2
- Node script room flag writers -- Phase 5a wires mob death flags; node pulse flags wire in Phase 6
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ANC-01 | Human ancestry with Empire Standing bonus and world-reaction traits | ANCESTRY_TRAITS dict from soravelon-ancestries.md; apply_ancestry_standings() using modify_standing(); Human: Empire +10,000 |
| ANC-02 | Kau'roran ancestry with size, cultural traits, and kiai ceremony access | ANCESTRY_TRAITS dict; Kau'roran: hp_bonus 1.30, strength_scaling 1.20, trust_build_rate 1.20; starting standings Kau'roran +20k, Wardens +10k, Empire -15k |
| ANC-03 | Veth ancestry with size modifiers, tunnel shortcuts, and information networks | ANCESTRY_TRAITS dict; Veth: agility_scaling 1.25, speed_bonus 1.15; Consortium +7,500; tunnel shortcut mechanism deferred to content |
| ANC-04 | Selvar ancestry with seasonal coat variation and social perception modifiers | ANCESTRY_TRAITS dict; coat_choice: summer (agility +10%, focus gen +5%) vs winter (endurance +10%, status resist +5%); -5,000 all factions + guilds +2,500 |
| ANC-05 | Ancestry modifiers feed into mob disposition calculation (additive, not override) | Already implemented: mob_disposition.py has ANCESTRY_FACTION_MODIFIERS and get_ancestry_modifier() reading character.db.ancestry. Ancestry engine just sets db.ancestry. |
| ABL-01 | Global data-driven ability registry (not per-character instances) | ABILITIES dict in world/ability_registry.py; D-08/D-09 define structure; same pattern as GUILDS/SUBCLASSES |
| ABL-02 | CmdUseAbility dispatcher handles all abilities through one command | D-10: effect-type dispatch with ~10 handlers; no per-ability Cmd classes |
| ABL-03 | Ability tier gating unlocks at GTS 0/20/50/85 | Existing get_guild_tier() returns 1-4; CharacterAbility model tracks unlocked abilities; tier check before execution |
| ABL-04 | All 90 subclasses have mechanically distinct ability sets | DEFERRED to Phase 5b per D-01. Phase 5a builds the registry structure with placeholder/stub entries only. |
| ABL-05 | Ability cooldowns tracked per-encounter on character.ndb | D-12: character.ndb.ability_cooldowns dict; remaining rounds per ability; cleared on encounter end |
| ABL-06 | Subclass engine derives identity from primary + secondary domain pair | Already built in guild_engine.py: SUBCLASSES dict, join_guild() derives subclass_id from primary+secondary. Phase 5a adds ability access rules based on this. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Evennia | 6.0.0 | MUD engine, typeclass system, command handler | Project foundation |
| Django | 6.0.3 | ORM for CharacterAbility model, migrations | Already in use |
| Python | 3.12.10 | All game logic | Project runtime |

### Supporting
No new external dependencies required. Phase 5a is pure Python code building on existing Evennia + Django stack. All new modules are `world/` engine files and `commands/` command classes.

## Architecture Patterns

### New Files to Create
```
world/
  ancestry_engine.py     # ANCESTRY_TRAITS, ANCESTRY_STARTING_STANDING, apply functions
  ability_registry.py    # ABILITIES dict, DOMAIN_ABILITIES, SUBCLASS_SIGNATURES lookups
  ability_engine.py      # use_ability(), effect-type dispatch, cooldown/resource management
  room_state.py          # FLAG_VOCABULARY, lazy decay, Sense support
commands/
  cmd_ancestry.py        # CmdSetAncestry
  cmd_guild.py           # CmdJoinGuild (stub)
  cmd_domains.py         # CmdDomains
  cmd_abilities.py       # CmdAbilities, CmdUseAbility
tests/
  test_ancestry_engine.py
  test_ability_engine.py
  test_room_state.py
  test_cmd_abilities.py  # (or consolidated into existing test files)
```

### Files to Modify
```
world/models.py                  # Add CharacterAbility model
world/migrations/0005_*.py       # New migration for CharacterAbility
world/guild_engine.py            # Update Ironwright hook (D-27)
world/world_state.py             # Add guild discovery hook in commit_session_xp()
world/action_vocabulary.py       # Add _action_add_room_flag handler
typeclasses/characters.py        # Add ndb inits, at_after_move Sense hook, db.remnance_discovered
typeclasses/mobs.py              # Add room flag writers in at_death()
commands/default_cmdsets.py      # Register new commands
```

### Pattern 1: Python Constant Registry (ABILITIES dict)
**What:** Static ability definitions as a module-level dict, keyed by ability_id.
**When to use:** All ability lookups. Same pattern as GUILDS, SUBCLASSES, FINGERPRINTS in guild_engine.py.
**Example:**
```python
# world/ability_registry.py
ABILITIES = {
    "resonant_strike": {
        "id": "resonant_strike",
        "name": "Resonant Strike",
        "domain": "resonance",
        "tier": 1,
        "resource_cost": 20,
        "resource_type": "resonance",
        "cooldown": 0,
        "charge_turns": 0,
        "effect_type": "damage",
        "scaling_primary": "resonance",
        "scaling_secondary": None,
        "application_chance": 1.0,
        "description": "Channel old patterns into a physical strike.",
        "room_flag_written": None,
        "attuned_variants": {
            "charged": {
                "extra_resource_cost": 10,
                "description": "Arc to a second target.",
                "extra_effect": {"type": "damage", "targets": "secondary", "damage_mult": 0.5},
            },
        },
    },
    # ... 329 more entries (populated in Phase 5b)
}

# Derived lookup tables (built at import time)
DOMAIN_ABILITIES = {}  # domain -> [ability_ids by tier]
SUBCLASS_SIGNATURES = {}  # subclass_id -> [signature_ability_ids]
```

### Pattern 2: Effect-Type Dispatch
**What:** CmdUseAbility looks up ability definition, then dispatches to an effect handler based on `effect_type` field.
**When to use:** All ability execution. Eliminates per-ability Cmd classes.
**Example:**
```python
# world/ability_engine.py
EFFECT_HANDLERS = {
    "damage": _handle_damage,
    "dot": _handle_dot,
    "buff": _handle_buff,
    "debuff": _handle_debuff,
    "utility": _handle_utility,
    "social": _handle_social,
    "tactical": _handle_tactical,
    "compound_trigger": _handle_compound_trigger,
    "heal": _handle_heal,
    "status": _handle_status,
}

def use_ability(character, ability_id, target=None):
    """
    Execute an ability. Returns (bool, str).
    Checks: known, tier gate, cooldown, resource, then dispatches.
    """
    ability = ABILITIES.get(ability_id)
    if not ability:
        return False, "Unknown ability."

    # Check character knows this ability
    ok, msg = _check_ability_access(character, ability_id)
    if not ok:
        return False, msg

    # Check cooldown
    cooldowns = character.ndb.ability_cooldowns or {}
    if cooldowns.get(ability_id, 0) > 0:
        return False, f"{ability['name']} is on cooldown ({cooldowns[ability_id]} rounds)."

    # Check and spend resource
    ok, msg = _check_and_spend_resource(character, ability)
    if not ok:
        return False, msg

    # Check attuned variant availability
    # (stub: y/n prompt deferred to combat UI)

    # Dispatch to effect handler
    handler = EFFECT_HANDLERS.get(ability["effect_type"])
    if not handler:
        return False, f"Unhandled effect type: {ability['effect_type']}"

    result = handler(character, ability, target)

    # Set cooldown
    if ability["cooldown"] > 0:
        cooldowns[ability_id] = ability["cooldown"]
        character.ndb.ability_cooldowns = cooldowns

    # Write room flag if specified
    if ability.get("room_flag_written") and character.location:
        from world.room_state import add_room_flag
        add_room_flag(character.location, ability["room_flag_written"])

    return True, result
```

### Pattern 3: Lazy Decay Room State
**What:** Room flags stored on room.ndb with timestamps; decay calculated on read, not by ticker.
**When to use:** All room state access. No global ticker scanning rooms.
**Example:** Full implementation provided in soravelon-room-state.md vault doc. FLAG_VOCABULARY dict with 20 flags, get_room_flags() applies lazy decay, get_dominant_flag() for Sense display.

### Pattern 4: CharacterAbility Model
**What:** Django model tracking which abilities a character has unlocked.
**When to use:** Ability access checks, progression tracking.
**Example:**
```python
# world/models.py
class CharacterAbility(models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="character_abilities",
    )
    ability_id = models.CharField(max_length=128, db_index=True)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    times_used = models.IntegerField(default=0)

    class Meta:
        unique_together = ("character", "ability_id")
        indexes = [
            models.Index(fields=["character_id", "ability_id"]),
        ]
```

### Anti-Patterns to Avoid
- **Per-ability Cmd classes:** Locked out by D-10. All abilities go through CmdUseAbility.
- **Global ticker for room state:** D-21 specifies lazy decay. No ticker scanning rooms.
- **Auto-unlock abilities:** D-19 requires manual claim at guild hall. No auto-add on tier threshold.
- **Hardcoded mob friend/foe:** Disposition is always computed. Ancestry modifiers are additive.
- **Storing room flags in DB:** D-21 uses ndb (ephemeral). Flags clear on server restart by design.
- **Exposing flag names to players:** Sense shows atmospheric text from SENSE_DISPLAY, never raw flag names.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Faction standing modification | Custom ancestry standing code | `world.world_state.modify_standing()` | Already handles all standing operations with F() atomic updates |
| GTS computation | New tier calculation | `world.guild_engine.calculate_guild_tier_score()` and `get_guild_tier()` | Already built in Phase 4, tested |
| Ancestry disposition modifiers | New disposition calculation | `world.mob_disposition.get_ancestry_modifier()` | Already reads character.db.ancestry, already has ANCESTRY_FACTION_MODIFIERS table |
| Guild eligibility check | New eligibility logic | `world.guild_engine.check_guild_eligibility()` | Already checks domain scores >= 30, filters by guild |
| Guild join | New guild membership logic | `world.guild_engine.join_guild()` | Creates CharacterGuild record, updates db caches |
| Domain proficiency labels | New label mapping | `world.guild_engine.DOMAIN_PROFICIENCY_LABELS` | Already defined in Phase 4 |

**Key insight:** Phase 4 built the entire guild infrastructure. Phase 5a plugs into it, it does not rebuild it.

## Common Pitfalls

### Pitfall 1: Migration Numbering
**What goes wrong:** New CharacterAbility migration collides with existing migration numbers.
**Why it happens:** Existing migrations are 0001-0004. New migration must be 0005.
**How to avoid:** Run `evennia makemigrations world` which auto-numbers. Verify it produces 0005.
**Warning signs:** Migration dependency errors on `evennia migrate`.

### Pitfall 2: SaverDict Copy Pattern for ability_cooldowns
**What goes wrong:** Mutating character.ndb dict directly may not trigger Evennia's save mechanism on ndb.
**Why it happens:** ndb is in-memory and not persisted, so SaverDict is not the concern here. However, reassigning the entire dict after mutation is still the safe pattern for consistency.
**How to avoid:** Always `cooldowns = dict(character.ndb.ability_cooldowns or {}); cooldowns[id] = val; character.ndb.ability_cooldowns = cooldowns`.
**Warning signs:** Cooldowns not updating between rounds.

### Pitfall 3: Circular Import Between ability_engine and guild_engine
**What goes wrong:** ability_engine imports from guild_engine for subclass lookups; guild_engine already imports from world_state.
**Why it happens:** Deep module dependency chain.
**How to avoid:** Use lazy imports inside functions (established project pattern). ability_registry.py should be pure constants with no imports from other world modules. ability_engine.py uses lazy imports for guild_engine lookups.
**Warning signs:** ImportError at module load time.

### Pitfall 4: commit_session_xp Hook Must Not Break Existing Flow
**What goes wrong:** Adding guild discovery check to commit_session_xp() causes errors that prevent XP commit.
**Why it happens:** New code raises exception inside the XP commit path.
**How to avoid:** Wrap guild discovery check in try/except. Log errors but never let them prevent the XP commit from completing. The hook should be a fire-and-forget notification.
**Warning signs:** XP not saving, error logs during session flush.

### Pitfall 5: Selvar -5000 All Factions Requires Iteration
**What goes wrong:** Applying Selvar starting standings requires knowing all known factions at creation time.
**Why it happens:** The design says "-5,000 to all known factions". Which factions are "known" at character creation?
**How to avoid:** Define a KNOWN_FACTIONS_AT_CREATION list in ancestry_engine.py. Apply -5,000 to each. Then apply the guild +2,500 offset. Do not iterate over all possible faction_ids in the database.
**Warning signs:** Missing or extra faction standings for Selvar characters.

### Pitfall 6: Remnance Hidden Domain Display
**What goes wrong:** Remnance score appears in domains command before character has discovered it.
**Why it happens:** Remnance XP accumulates silently. The display gate is character.db.remnance_discovered.
**How to avoid:** D-25 is explicit: filter Remnance from domains display unless db.remnance_discovered is True. Initialize db.remnance_discovered = False in at_object_creation().
**Warning signs:** Players seeing "Remnance: Unaware" before discovering the Vaelborn guild.

### Pitfall 7: CmdUseAbility Naming Collision
**What goes wrong:** `use` command conflicts with existing Evennia commands.
**Why it happens:** Evennia has default commands that might use similar verbs.
**How to avoid:** Use `use` as the command key (matching the design spec "use <ability>"). Add it to the CharacterCmdSet with appropriate priority. Test for collision with `evennia` default cmdset.
**Warning signs:** `use` command not resolving correctly, or overriding a system command.

### Pitfall 8: Room State ndb Not Initialized
**What goes wrong:** get_room_flags() tries to read room.ndb.room_state on rooms where it was never set.
**Why it happens:** Rooms created before Phase 5a have no ndb.room_state.
**How to avoid:** The vault design handles this: `state = room.ndb.room_state; if not state: return {}`. This is already correct -- ndb attributes return None when unset.
**Warning signs:** AttributeError on room.ndb.room_state (should not happen with correct None check).

## Code Examples

### Ancestry Engine Core
```python
# world/ancestry_engine.py
"""
Ancestry engine for Soravelon.

4 ancestries: Human, Kau'roran, Veth, Selvar.
Each has innate traits, starting standings, and one starting ability (once-per-combat).
Ancestry modifiers feed into mob disposition calculation (additive, not override).

Creative content from soravelon-ancestries.md vault. Not authored by Claude.
"""

ANCESTRY_TRAITS = {
    "human": {
        "name": "Human",
        "attribute_bonus": 1,
        "reputation_generation": 1.15,
        "status_duration_reduction": 0.10,
        "starting_ability": "second_wind",
        "domain_modifiers": {
            "combat": {"reputation_from_kills_scale": 1.2},
            "naturalism": {"attunement_any_zone": True},
            "subterfuge": {"network_from_jobs_scale": 1.2},
        },
    },
    # ... kauroran, veth, selvar per vault doc
}

ANCESTRY_STARTING_STANDING = {
    "human": {"empire": 10000},
    "kauroran": {"kauroran": 20000, "wardens": 10000, "empire": -15000},
    "veth": {"consortium": 7500},
    "selvar": {},  # -5000 all known factions handled specially
}

SELVAR_ALL_FACTIONS_PENALTY = -5000
SELVAR_GUILD_OFFSET = 2500
KNOWN_FACTIONS_AT_CREATION = [
    "empire", "wardens", "kauroran", "consortium",
]

VALID_ANCESTRIES = tuple(ANCESTRY_TRAITS.keys())
VALID_COATS = ("summer", "winter")


def set_ancestry(character, ancestry_id, coat=None):
    """
    Set character ancestry. Apply starting standings and traits.
    Returns (bool, str).
    """
    if character.db.ancestry:
        return False, "Ancestry already chosen."
    if ancestry_id not in ANCESTRY_TRAITS:
        return False, f"Unknown ancestry: {ancestry_id}"
    if ancestry_id == "selvar" and coat not in VALID_COATS:
        return False, "Selvar ancestry requires a coat choice (summer or winter)."

    character.db.ancestry = ancestry_id
    if coat:
        character.db.selvar_coat = coat

    _apply_starting_standings(character, ancestry_id)
    return True, f"You are {ANCESTRY_TRAITS[ancestry_id]['name']}."


def _apply_starting_standings(character, ancestry_id):
    """Apply starting faction standings for ancestry via modify_standing()."""
    from world.world_state import modify_standing

    standings = ANCESTRY_STARTING_STANDING.get(ancestry_id, {})
    for faction_id, amount in standings.items():
        modify_standing(character, faction_id, amount)

    # Selvar special: -5000 to all known factions, then +2500 guilds offset
    if ancestry_id == "selvar":
        for faction_id in KNOWN_FACTIONS_AT_CREATION:
            modify_standing(character, faction_id, SELVAR_ALL_FACTIONS_PENALTY)
        modify_standing(character, "guilds", SELVAR_GUILD_OFFSET)
```

### Guild Discovery Hook
```python
# Addition to world/world_state.py:commit_session_xp()
# After line: character.db.backend_level = calculate_backend_level(character)

# Guild discovery check (D-17)
try:
    _check_guild_discovery(character)
except Exception:
    import evennia
    evennia.logger.log_trace("Guild discovery check failed (non-fatal)")


def _check_guild_discovery(character):
    """Fire guild recruitment message if character qualifies and has no guild."""
    if character.db.guild_id:
        return
    from world.guild_engine import check_guild_eligibility
    eligible = check_guild_eligibility(character)
    if not eligible:
        return
    # Send recruitment message for first eligible guild
    # (guild-flavored text, not a system notification)
    from world.guild_engine import GUILDS
    guild = GUILDS.get(eligible[0], {})
    guild_name = guild.get("name", eligible[0])
    character.msg(
        f"|y[A messenger approaches with a sealed letter bearing the mark "
        f"of the {guild_name}.]|n"
    )
```

### Room Flag Writer in at_death
```python
# Addition to typeclasses/mobs.py:SoravelonMob.at_death()
# After existing loot drop code

# Write room state flags (D-24)
if room:
    from world.room_state import add_room_flag
    add_room_flag(room, "blood_soaked")

    # Nature-affinity mob death
    if self.db.faction and self.db.faction.lower() in ("verdance", "wardens", "nature"):
        add_room_flag(room, "fading_life")

    # Named/boss mob death
    is_named = self.tags.get("mob_id", category="mob_id") is not None
    is_boss = self.db.rarity == "legendary"
    if is_named or is_boss:
        add_room_flag(room, "power_vacuum")
```

### Sense Hook in at_after_move
```python
# Addition to typeclasses/characters.py:Character.at_after_move()
# After existing visited_room_ids tracking

# Resonance Sense passive (D-22)
if self.db.guild_id and self.location:
    from world.guild_engine import GUILDS
    guild = GUILDS.get(self.db.guild_id, {})
    if guild.get("primary_domain") == "resonance":
        from world.room_state import get_dominant_flag, SENSE_DISPLAY
        flag = get_dominant_flag(self.location)
        if flag:
            text = SENSE_DISPLAY.get(flag, "")
            if text:
                self.msg(f"|m[Sense] {text}|n")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Per-class command system | Single CmdUseAbility dispatcher | Phase 5 design | 330+ abilities through one command class |
| Hardcoded mob disposition | Computed from ancestry + standing + reputation | Phase 4 | Ancestry modifiers are additive, never hardcoded |
| No room state | Lazy-decay ndb flags | Phase 5 design | Environmental gameplay without global tickers |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest via `evennia test --settings settings tests/` |
| Config file | none (Evennia test runner handles setup) |
| Quick run command | `evennia test --settings settings tests/test_ancestry_engine.py -x` |
| Full suite command | `evennia test --settings settings tests/ -x` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ANC-01 | Human ancestry applies Empire +10,000 standing | unit | `evennia test --settings settings tests/test_ancestry_engine.py::TestHumanAncestry -x` | Wave 0 |
| ANC-02 | Kau'roran ancestry applies correct standings and traits | unit | `evennia test --settings settings tests/test_ancestry_engine.py::TestKauroranAncestry -x` | Wave 0 |
| ANC-03 | Veth ancestry applies Consortium +7,500 | unit | `evennia test --settings settings tests/test_ancestry_engine.py::TestVethAncestry -x` | Wave 0 |
| ANC-04 | Selvar coat choice and -5,000 all factions penalty | unit | `evennia test --settings settings tests/test_ancestry_engine.py::TestSelvarAncestry -x` | Wave 0 |
| ANC-05 | Ancestry feeds mob disposition (already tested in test_mob_disposition.py) | unit | `evennia test --settings settings tests/test_mob_disposition.py -x` | Exists |
| ABL-01 | Ability registry structure validates correctly | unit | `evennia test --settings settings tests/test_ability_engine.py::TestAbilityRegistry -x` | Wave 0 |
| ABL-02 | CmdUseAbility dispatches to correct effect handler | unit | `evennia test --settings settings tests/test_ability_engine.py::TestUseAbility -x` | Wave 0 |
| ABL-03 | Tier gating blocks abilities above current tier | unit | `evennia test --settings settings tests/test_ability_engine.py::TestTierGating -x` | Wave 0 |
| ABL-05 | Cooldowns decrement and clear on encounter end | unit | `evennia test --settings settings tests/test_ability_engine.py::TestCooldowns -x` | Wave 0 |
| ABL-06 | Subclass derives from primary + secondary domain pair | unit | `evennia test --settings settings tests/test_guild_engine.py -x` | Exists |
| D-21 | Room state lazy decay, flag addition/removal | unit | `evennia test --settings settings tests/test_room_state.py -x` | Wave 0 |
| D-17 | Guild discovery fires on commit_session_xp | unit | `evennia test --settings settings tests/test_world_state.py -x` | Exists (extend) |

### Sampling Rate
- **Per task commit:** `evennia test --settings settings tests/test_ancestry_engine.py tests/test_ability_engine.py tests/test_room_state.py -x`
- **Per wave merge:** `evennia test --settings settings tests/ -x`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_ancestry_engine.py` -- covers ANC-01 through ANC-04
- [ ] `tests/test_ability_engine.py` -- covers ABL-01, ABL-02, ABL-03, ABL-05
- [ ] `tests/test_room_state.py` -- covers D-21 room state operations

### Test Pattern Notes
- **Ancestry engine tests:** Can use `unittest.TestCase` with MagicMock for character objects. set_ancestry() only calls modify_standing() which can be mocked. Pure logic, no DB needed.
- **Ability engine tests:** Use `unittest.TestCase` with MagicMock. Effect handlers are stubs in 5a. Test dispatch routing and access checks.
- **Room state tests:** Use `unittest.TestCase` with MagicMock for room objects. Pure ndb operations. Use `time.time()` mocking for decay validation.
- **Model tests (CharacterAbility):** Use `EvenniaTest` for Django model creation/query tests. Same pattern as test_guild_engine_mutations.py.
- **Command tests:** Use `EvenniaCommandTestMixin` for CmdSetAncestry, CmdDomains. Same pattern as existing command tests.

## Open Questions

1. **Selvar "known factions" list**
   - What we know: Design says -5,000 to "all known factions". Four factions exist in ANCESTRY_FACTION_MODIFIERS: empire, wardens, kauroran, consortium, resistance.
   - What's unclear: Should Resistance be included in KNOWN_FACTIONS_AT_CREATION? Resistance is hidden for other ancestries. Selvar has hidden resistance +2,500 in HIDDEN_ANCESTRY_STANDING.
   - Recommendation: Apply -5,000 to the 4 overt factions (empire, wardens, kauroran, consortium). Apply resistance standing via HIDDEN_ANCESTRY_STANDING separately (+2,500). This keeps the "hidden faction" pattern consistent.

2. **GTS tier threshold notification timing**
   - What we know: D-19 says player gets notification when GTS crosses threshold. D-17 puts the hook in commit_session_xp.
   - What's unclear: Should tier crossing detection also happen in commit_session_xp, or only at guild hall visit?
   - Recommendation: Track last-known tier in CharacterGuild model or character.db. On each commit_session_xp, compare current tier to stored tier. If changed, send notification. Claim happens at guild hall.

3. **Ability registry population for Phase 5a stubs**
   - What we know: Phase 5a builds the registry structure. Phase 5b populates it.
   - What's unclear: How many stub abilities should 5a include for testing/validation?
   - Recommendation: Include 2-3 stub abilities per effect_type (~20 stubs total) to validate the dispatcher. Mark them clearly as placeholders. One per domain for Tier 1 ensures the domains command has something to show.

4. **Active loadout storage**
   - What we know: D-05 says 8 abilities in active loadout from 21 known.
   - What's unclear: Where to store the loadout -- db (persisted) or ndb (volatile)?
   - Recommendation: `character.db.active_loadout = []` (list of 8 ability_ids). Persisted because loadout is a deliberate player choice that should survive disconnects.

## Sources

### Primary (HIGH confidence)
- `soravelon-ancestries.md` vault doc -- complete ancestry data model, traits, standings
- `soravelon-abilities.md` vault doc -- ability structure, resource systems, GTS tiers
- `soravelon-guilds.md` vault doc -- 90 subclasses, guild tier labels, ability tier framework
- `soravelon-fingerprints.md` vault doc -- 10 domain fingerprints and resources
- `soravelon-room-state.md` vault doc -- complete room_state.py implementation with FLAG_VOCABULARY
- `world/guild_engine.py` codebase -- existing GUILDS, SUBCLASSES, FINGERPRINTS, GTS computation
- `world/world_state.py` codebase -- commit_session_xp() hook point, ALL_DOMAINS
- `world/mob_disposition.py` codebase -- ANCESTRY_FACTION_MODIFIERS, get_ancestry_modifier()
- `world/models.py` codebase -- existing Django models, CharacterGuild pattern
- `typeclasses/characters.py` codebase -- at_object_creation() initialization, at_after_move()
- `typeclasses/mobs.py` codebase -- at_death() hook point
- `05-CONTEXT.md` -- all 27 locked decisions

### Secondary (MEDIUM confidence)
- None needed -- all decisions are locked with vault sources

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies, pure Python on existing Evennia/Django
- Architecture: HIGH -- all patterns follow established project conventions, vault docs provide complete specs
- Pitfalls: HIGH -- identified from direct codebase analysis and project convention knowledge

**Research date:** 2026-03-25
**Valid until:** 2026-04-25 (stable -- no external dependencies to drift)
