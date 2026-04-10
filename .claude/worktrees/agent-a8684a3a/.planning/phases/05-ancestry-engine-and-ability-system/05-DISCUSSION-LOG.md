# Phase 5: Ancestry Engine and Ability System - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-26
**Phase:** 05-ancestry-engine-and-ability-system
**Areas discussed:** Phase split strategy, Ability authoring scope, Ability data model, Ancestry engine scope, Guild discovery wiring, Subclass engine mechanics, Resource system stubs, 5b collaborative workflow, Ability unlock flow, Secondary domain ability pick, Ability definition fields, Room state system, Domains command, Ironwright update

---

## Phase Split Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Split into 5a + 5b | Ancestry engine + ability framework separate from ability content authoring | ✓ |
| Keep as one phase | One massive phase, 11 requirements | |
| Split three ways | 5a ancestries, 5b engine, 5c content | |

**User's choice:** Split into 5a (engine + framework) and 5b (ability definitions)

## Ability Authoring Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Claude designs all | Claude proposes all 330 abilities | |
| User provides designs | User authors in vault docs | |
| Collaborative guild by guild | Claude proposes per domain, user reviews | ✓ |

**User's choice:** Collaborative in-conversation review, domain by domain
**Notes:** User corrected ability count: 15 per domain (3 per tier) × 10 = 150 domain + 2 signatures × 90 = 180 → 330 total. Per character: 21 known, 8 active loadout.

## Ability Data Model

| Option | Description | Selected |
|--------|-------------|----------|
| Python constants | ABILITIES dict in ability_registry.py | ✓ |
| Django model | AbilityDefinition table | |
| YAML data files | world/data/abilities/*.yaml | |

## CmdUseAbility Dispatch

| Option | Description | Selected |
|--------|-------------|----------|
| Effect-type dispatch | ~10 handlers by effect_type field | ✓ |
| Per-ability callables | Each ability has a function reference | |
| Generic apply function | One function handles everything | |

## Cooldown Tracking

| Option | Description | Selected |
|--------|-------------|----------|
| character.ndb per-encounter | Dict on character.ndb, cleared on encounter end | ✓ |
| mob.ndb per-encounter | Cooldowns on mob | |
| Hybrid character+mob | Players on character.ndb, mobs on mob.ndb | |

## CharacterAbility Model

| Option | Description | Selected |
|--------|-------------|----------|
| Django model | CharacterAbility in models.py | ✓ |
| db attribute dict | character.db.unlocked_abilities set | |
| Hybrid model + cache | Model + db cache set | |

## Ancestry Engine Location

| Option | Description | Selected |
|--------|-------------|----------|
| New world/ancestry_engine.py | Dedicated module | ✓ |
| Inside world/world_state.py | Co-locate with domain tracking | |
| Inside guild_engine.py | Co-locate with guild data | |

## Starting Ability Tracking

| Option | Description | Selected |
|--------|-------------|----------|
| character.ndb.ancestry_ability_used | Boolean, reset per encounter | ✓ |
| Part of ability_cooldowns dict | Unified with regular cooldowns | |
| Automatic passive triggers | Auto-trigger, no tracking | |

## Ancestry Selection

| Option | Description | Selected |
|--------|-------------|----------|
| at_object_creation + CmdSetAncestry | Default None, command to choose | ✓ |
| During at_object_creation only | Must set at creation | |
| Deferred to content phase | Engine only, no selection | |

## Guild Discovery Trigger

| Option | Description | Selected |
|--------|-------------|----------|
| Post-XP-commit + recruitment msg | In-game flavored message | ✓ |
| Post-XP-commit + NPC spawn | Spawn recruiter NPC | |
| Stub only — log message | Log, no player notification | |

**User's choice:** Post-XP-commit hook + in-game guild-flavored recruitment message

## Secondary Domain Selection

| Option | Description | Selected |
|--------|-------------|----------|
| CmdChooseSecondary | Player runs command | |
| Auto-detect from scores | Second-highest auto-selected | |
| Narrative NPC interaction | Guild master presents options with recommendation | ✓ |

**User's choice:** Blend of auto-detect and narrative — recommend highest scores but offer all qualified options. Lightweight stub in 5a.

## Guild Induction Stub

| Option | Description | Selected |
|--------|-------------|----------|
| Lightweight stub in 5a | Temporary CmdJoinGuild with text prompts | ✓ |
| Defer to Phase 6 | join_guild only callable programmatically | |
| Full NPC interaction in 5a | Build mini NPC dialogue | |

## Resource System

| Option | Description | Selected |
|--------|-------------|----------|
| Tracking only — no effects | ndb tracking, build/decay/spend functions | ✓ |
| Full implementation | All 10 resources functional | |
| Constants only | Names in dict, no tracking | |

## Ability Unlock Flow

| Option | Description | Selected |
|--------|-------------|----------|
| Narrative msg + auto-add | Auto-unlock on tier change | |
| Guild notification + manual claim | Guild-flavored msg, claim at guild hall | ✓ |
| Silent unlock | No notification | |

**User's choice:** Guild-specific flavored notification, manual claim from guild hall

## Secondary Domain Ability Pick

| Option | Description | Selected |
|--------|-------------|----------|
| Player chooses from 3 | Per tier, pick 1 of 3 from secondary pool | ✓ |
| Predetermined by subclass | Fixed per subclass | |
| Auto-pick highest synergy | System selects | |

## Ability Definition Fields

| Option | Description | Selected |
|--------|-------------|----------|
| Full shape from vault | All fields including combat math (stubbed) | ✓ |
| Minimal — identity only | id, name, domain, tier, description | |
| Medium — dispatch-ready | id, name, tier, resource_cost, cooldown, effect_type | |

## Signature Ability Tier Gating

| Option | Description | Selected |
|--------|-------------|----------|
| Tier 2 + Tier 4 | Sig 1 at GTS 20, Sig 2 at GTS 85 | |
| Always available | Both on subclass confirm | |
| Tier 3 + Tier 4 | Sig 1 at GTS 50, Sig 2 at GTS 85 | ✓ |

**Notes:** Corrected from earlier discussion based on vault doc update.

## Domains Command

| Option | Description | Selected |
|--------|-------------|----------|
| Build in 5a | Full display with Remnance hiding | ✓ |
| Defer to Phase 6/7 | Engine functions only | |
| Minimal stub | Domain scores only | |

## Room State System

| Option | Description | Selected |
|--------|-------------|----------|
| Build in 5a | Full module + Sense + flag writers | ✓ |
| Defer to Phase 6 | Build with combat system | |
| Minimal stub | Module exists, no Sense | |

## Ironwright Update

| Option | Description | Selected |
|--------|-------------|----------|
| Update in 5a | Fix SUBCLASSES dict hook text | ✓ |
| Defer to 5b | Update during ability authoring | |

---

## Claude's Discretion

- Guild recruitment message text per guild
- CmdJoinGuild text prompt flow details
- Ability registry field naming
- Test organization
- Room state mob death flag integration
- Domain proficiency display formatting

## Deferred Ideas

- ABL-04 (all ability definitions) → Phase 5b
- Combat system integration → Phase 6
- NPC template system for induction → Phase 6
- auto_attune configuration → later
- Companion system → Milestone 2
