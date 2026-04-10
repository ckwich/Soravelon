# Phase 4: Domain Fingerprints and Guild Engine - Research

**Researched:** 2026-03-25
**Domain:** Domain identity design, guild/subclass constant registries, GTS computation, Django model
**Confidence:** HIGH

## Summary

Phase 4 produces four deliverables: (1) a consolidated design document extracting creative content from three vault sources, (2) Python constant registries for guilds, subclasses, fingerprints, and tier labels in `world/guild_engine.py`, (3) GTS computation and guild eligibility engine functions, and (4) a `CharacterGuild` Django model in `world/models.py` with migration.

The implementation is straightforward because all creative content already exists in vault documents (`soravelon-fingerprints.md`, `soravelon-guilds.md`, `soravelon-abilities.md`). The engineering work is: consolidate into a planning doc, transcribe static data into Python dicts, write a handful of pure computation functions, and add one Django model. No tick-driven systems, no command layer, no NPC wiring.

Key finding: there is no `get_domain_score()` helper function. Domain scores are accessed directly via `character.db.domain_scores.get(domain, 0.0)`. The guild engine functions will follow this same pattern.

**Primary recommendation:** Build this phase in three waves -- design doc consolidation, constant registries + engine functions, Django model + migration. All computation is on-the-fly with no caching except the `db.guild_id`/`db.subclass_id` fast-read caches on Character.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** All 10 domain fingerprints are authored by the user in vault docs (soravelon-fingerprints.md, soravelon-guilds.md, soravelon-abilities.md). Claude does not author creative content -- Claude consolidates vault material into a .planning/ design doc.
- **D-02:** Design doc format is Markdown in `.planning/phases/04-domain-fingerprints-guild-engine/`. Downstream agents read this doc to understand domain identity before authoring abilities in Phase 5.
- **D-03:** The design doc extracts: 10 fingerprint verbs + resources, 90 subclass definitions (name/fantasy/hook), guild tier labels, GTS formula, and data model shapes.
- **D-04:** Guild discovery triggers via post-XP-commit hook. When domain XP commits and a score crosses 30 (Practiced threshold), check if `guild_id` is None. If so, schedule a guild approach event.
- **D-05:** The trigger check is **not wired in Phase 4**. Phase 4 builds the engine; discovery wiring is Phase 5+ content work. The engine exposes a `check_guild_eligibility(character)` function that returns which guild(s) a character qualifies for.
- **D-06:** Guild tier labels stored as Python constants in `world/guild_engine.py`. Dict keyed by guild_id to list of 4 label strings. Matches existing ALL_DOMAINS pattern.
- **D-07:** GTS (Guild Tier Score) is always computed on-the-fly: `(primary_domain_score x 0.66) + (secondary_domain_score x 0.33)`. No stored/cached GTS value. Function: `calculate_guild_tier_score(character) -> float`.
- **D-08:** Tier thresholds: Tier 1 (0-20), Tier 2 (20-50), Tier 3 (50-85), Tier 4 (85+). Function: `get_guild_tier(character) -> int` and `get_guild_tier_label(character) -> str`.
- **D-09:** GuildDefinition and SubclassDefinition are Python constant dicts in `world/guild_engine.py`, not Django models. Static data that never changes at runtime.
- **D-10:** GUILDS dict structure: `{guild_id: {name, primary_domain, hub_cities, hidden, motto, resource_type}}`.
- **D-11:** SUBCLASSES dict structure: `{subclass_id: {name, primary_domain, secondary_domain, guild_id, fantasy, hook}}`.
- **D-12:** GUILD_TIER_LABELS dict structure: `{guild_id: [tier1_label, tier2_label, tier3_label, tier4_label]}`.
- **D-13:** FINGERPRINTS dict structure: `{domain: {verb, resource, resource_type, description}}`.
- **D-14:** CharacterGuild is a new Django model in `world/models.py`. Fields: character (FK to ObjectDB), guild_id, primary_domain, secondary_domain, subclass_id, joined_at (DateTimeField), induction_complete (BooleanField). One row per character.
- **D-15:** Hybrid storage: CharacterGuild Django model is source of truth. `character.db.guild_id` and `character.db.subclass_id` remain as fast-read caches, updated when the model changes. Avoids DB join on every ability/GTS check.
- **D-16:** CharacterAbility model is **deferred to Phase 5**. Phase 4 only needs to compute which tier a character is at, not track unlocked abilities.

### Claude's Discretion
- Exact Python dict key naming and structure details beyond the shapes above
- Helper function signatures and internal organization of guild_engine.py
- Migration file structure
- Test organization and test case granularity

### Deferred Ideas (OUT OF SCOPE)
- Guild discovery NPC wiring (Phase 5+)
- Guild induction questlines (Phase 5+)
- Secondary domain choice UI (Phase 5+)
- CharacterAbility model + ability definitions (Phase 5)
- AbilityDefinition constant registry (Phase 5)
- `domains` command display (Phase 5+)
- `guild` command display (Phase 5+)
- Vaelborn discovery trigger sequence (content pass)
- Resource system implementation (combat system phase)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DOM-01 | 10 domains tracked with 0-100 scores and diminishing returns | Already implemented in `world/world_state.py` (ALL_DOMAINS, domain_scores dict, DIMINISHING_BRACKETS). Phase 4 adds the fingerprint identity layer on top. |
| DOM-02 | Guild Tier Score computed as (primary x 0.66) + (secondary x 0.33) | `calculate_guild_tier_score()` reads `character.db.domain_scores` dict directly + `character.db.primary_domain`/`secondary_domain`. Pure arithmetic, no DB reads. |
| DOM-03 | Guild discovers player organically at Practiced proficiency (~30 domain score) | `check_guild_eligibility(character)` function checks all domain scores against threshold 30, returns eligible guild_ids. Wiring deferred to Phase 5 but function exists. |
| DOM-04 | GTS tier labels provide non-numeric progression feedback to players | `get_guild_tier_label(character)` looks up guild_id in GUILD_TIER_LABELS dict, indexes by tier. Returns string like "Veilwalker" or "Attuned". |
| DOM-05 | 10 domain mechanical fingerprints designed (distinct gameplay verb per domain) | Design document consolidates vault content. FINGERPRINTS dict in guild_engine.py codifies the 10 verbs programmatically. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Django | 6.0.3 | ORM for CharacterGuild model | Already in stack, all world models use it |
| Evennia | 6.0.0 | ObjectDB FK target, typeclass system | Game engine |

### Supporting
No new libraries needed. This phase is pure Python constants + one Django model + computation functions.

## Architecture Patterns

### Recommended Module Structure
```
world/
  guild_engine.py          # NEW — constants + computation functions
  models.py                # MODIFIED — add CharacterGuild model
  world_state.py           # UNCHANGED — GTS reads domain_scores from here
```

### Pattern 1: Python Constant Registry (locked decision D-09)
**What:** Static game data stored as module-level dicts, not Django models
**When to use:** Data that never changes at runtime and is read frequently
**Existing examples:** `ALL_DOMAINS` tuple, `DIMINISHING_BRACKETS` list, `ANCESTRY_FACTION_MODIFIERS` dict
**Example:**
```python
# Source: D-10, D-11, D-12, D-13 from CONTEXT.md
GUILDS = {
    "ironblood": {
        "name": "Guild of Ironblood",
        "primary_domain": "combat",
        "hub_cities": ["caldenmere", "tremen"],
        "hidden": False,
        "motto": "Strength is not a gift. It is a debt you pay every day.",
        "resource_type": "momentum",
    },
    # ... 9 more guilds
}

SUBCLASSES = {
    "duskblade": {
        "name": "Duskblade",
        "primary_domain": "combat",
        "secondary_domain": "subterfuge",
        "guild_id": "ironblood",
        "fantasy": "A fighter who disappears between strikes...",
        "hook": "Momentum spends on mid-combat Vanish...",
    },
    # ... 89 more subclasses
}

GUILD_TIER_LABELS = {
    "ironblood": ["Scrapper", "Ironblood", "Warblade", "Bloodsworn"],
    # ... 9 more guilds
}

FINGERPRINTS = {
    "combat": {
        "verb": "press",
        "resource": "Momentum",
        "resource_type": "momentum",
        "description": "Sustained aggression...",
    },
    # ... 9 more domains
}
```

### Pattern 2: On-the-fly GTS Computation (locked decision D-07)
**What:** GTS is computed every time it's needed, never stored
**Why:** Domain scores change constantly (XP commits every 10 min). Storing GTS would require cache invalidation.
**Example:**
```python
def calculate_guild_tier_score(character):
    """Compute GTS from primary and secondary domain scores. Always fresh."""
    scores = character.db.domain_scores or {}
    primary = character.db.primary_domain
    secondary = character.db.secondary_domain
    if not primary:
        return 0.0
    p_score = scores.get(primary, 0.0)
    s_score = scores.get(secondary, 0.0) if secondary else 0.0
    return (p_score * 0.66) + (s_score * 0.33)
```

### Pattern 3: Hybrid Storage with Fast-Read Cache (locked decision D-15)
**What:** CharacterGuild model is source of truth; `character.db.guild_id` and `character.db.subclass_id` are fast-read caches
**Why:** GTS computation reads `character.db.primary_domain`/`secondary_domain` -- no DB join needed. Model is only queried for mutation operations.
**Example:**
```python
def join_guild(character, guild_id, secondary_domain):
    """
    Join a guild, creating CharacterGuild record and updating db caches.
    Returns (bool, str) per project convention.
    """
    guild = GUILDS.get(guild_id)
    if not guild:
        return False, f"Unknown guild: {guild_id}"
    primary = guild["primary_domain"]
    subclass_id = _resolve_subclass(primary, secondary_domain)
    if not subclass_id:
        return False, f"No subclass for {primary}/{secondary_domain}."

    from world.models import CharacterGuild as CGModel
    CGModel.objects.update_or_create(
        character=character,
        defaults={
            "guild_id": guild_id,
            "primary_domain": primary,
            "secondary_domain": secondary_domain,
            "subclass_id": subclass_id,
            "induction_complete": False,
        },
    )
    # Update fast-read caches
    character.db.guild_id = guild_id
    character.db.subclass_id = subclass_id
    character.db.primary_domain = primary
    character.db.secondary_domain = secondary_domain
    return True, f"You have joined the {guild['name']}."
```

### Pattern 4: (bool, str) Return Tuples
**What:** All engine functions that can fail return `(success, message)`
**Existing usage:** `banking.deposit()`, `inventory_engine.pick_up()`, `group_engine.send_group_invite()`
**Apply to:** `join_guild()`, `complete_induction()`, any mutation function in guild_engine.py

### Pattern 5: Lazy Record Creation
**What:** CharacterGuild record only created when character actually joins a guild
**Existing usage:** `BankAccount` created on first deposit, `FactionStanding` on first interaction
**Apply to:** No CharacterGuild record = Wanderer state (no guild). Functions check for `character.db.guild_id` first.

### Anti-Patterns to Avoid
- **Storing GTS in the database:** GTS must always be computed fresh (D-07). Never cache it.
- **Using Django models for static game data:** GUILDS, SUBCLASSES, FINGERPRINTS are compile-time constants, not runtime data (D-09).
- **Authoring creative content:** Claude consolidates vault material only -- never invents fingerprint verbs, subclass names, or guild lore (D-01).
- **Wiring guild discovery triggers:** Phase 4 builds the `check_guild_eligibility()` function but does NOT hook it into the XP commit pipeline (D-05).
- **Using `getattr(obj.db, 'attr', default)`:** Project convention is `character.db.guild_id or fallback` pattern.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Domain-to-guild mapping | Manual if/elif chain | GUILDS dict keyed by guild_id with primary_domain field | Dict lookup is O(1), maintainable |
| Subclass resolution from domain pair | Custom logic | Build a lookup index `{(primary, secondary): subclass_id}` from SUBCLASSES dict at module load | Two-key lookup, built once |
| Tier threshold logic | Nested if/elif | Sorted threshold list with bisect or simple iteration | Cleaner, fewer off-by-one bugs |

## Common Pitfalls

### Pitfall 1: Domain Score Scale Mismatch
**What goes wrong:** Vault doc `soravelon-abilities.md` shows a "0.0-10.0" score scale in the `DomainScore` data model proposal, but the actual codebase uses 0-100 scale consistently (`world_state.py` DIMINISHING_BRACKETS, `character.db.domain_scores`).
**Why it happens:** The vault doc is a design document with a proposed data model that was never implemented. The actual implementation in `world_state.py` uses 0-100.
**How to avoid:** Always use 0-100 scale. The vault doc's "Practiced ~3.0" maps to score ~30 in the actual 0-100 scale. GTS formula uses the 0-100 scores directly: `(primary x 0.66) + (secondary x 0.33)` yields max 99.
**Warning signs:** Any reference to scores in 0-10 range in code.

### Pitfall 2: No get_domain_score() Helper Exists
**What goes wrong:** CONTEXT.md references `get_domain_score()` as an existing function, but no such function exists in the codebase.
**Why it happens:** Context doc described intended interface, not actual implementation.
**How to avoid:** Read domain scores directly: `(character.db.domain_scores or {}).get(domain, 0.0)`. The guild engine should follow this existing pattern or create its own helper.
**Warning signs:** ImportError when trying to import `get_domain_score` from `world_state`.

### Pitfall 3: Vaelborn Hidden Guild Edge Cases
**What goes wrong:** Vaelborn (Remnance) guild has `hidden: True` and tier 1 label is "(hidden)" / placeholder. Code that iterates all guilds for display must filter hidden guilds. Code that checks eligibility must handle that Remnance XP accumulates silently.
**Why it happens:** Vaelborn is a special case by design.
**How to avoid:** `check_guild_eligibility()` should still include Vaelborn in results -- the filtering of hidden guilds is a display concern (Phase 5+). Include a `hidden` field in GUILDS dict.
**Warning signs:** Vaelborn appearing in player-facing guild lists before discovery.

### Pitfall 4: Duplicate Subclass Names Across Guilds
**What goes wrong:** Some domain pairs have different names depending on which is primary. Example: Arcana+Remnance = "Voidscribe" (Arcana primary) vs Remnance+Arcana = "Firstform" (Vaelborn primary). Subclass IDs must be unique.
**Why it happens:** The 90-subclass matrix intentionally creates different identities for reversed domain pairs.
**How to avoid:** Use lowercase slugified name as subclass_id (e.g., "voidscribe", "firstform"). The `_resolve_subclass(primary, secondary)` helper should build a `{(primary_domain, secondary_domain): subclass_id}` lookup dict at module level.
**Warning signs:** KeyError or duplicate key when building the subclass lookup.

### Pitfall 5: SaverDict Copy Pattern for db.domain_scores
**What goes wrong:** Reading `character.db.domain_scores` for GTS is safe (read-only). But if any guild engine function mutates domain_scores, it must use the copy-mutate-assign pattern.
**Why it happens:** Evennia SaverDict triggers a DB write on every key mutation.
**How to avoid:** GTS computation is read-only -- no issue. But `join_guild()` setting `character.db.primary_domain` and `character.db.secondary_domain` are simple attribute sets, not dict mutations, so no SaverDict concern there.
**Warning signs:** N+1 DB writes in a single operation touching domain_scores.

### Pitfall 6: CharacterGuild OneToOneField vs ForeignKey
**What goes wrong:** Using ForeignKey allows multiple guild records per character. Design says one row per character.
**Why it happens:** D-14 says "One row per character" but uses FK language.
**How to avoid:** Use `OneToOneField` on character, not `ForeignKey`. This enforces the one-record constraint at the database level. Matches `BankAccount` pattern which also uses `OneToOneField`.
**Warning signs:** Multiple CharacterGuild records for same character causing ambiguous lookups.

## Code Examples

### GTS Computation (verified against vault formula)
```python
# Source: soravelon-abilities.md "Guild Tier Score and Ability Unlocking" section
# GTS = (Primary domain score x 0.66) + (Secondary domain score x 0.33)
# Max possible with both at 100: 99
# Tier thresholds: 0-20, 20-50, 50-85, 85+

GTS_TIER_THRESHOLDS = [
    (85, 4),   # Tier 4: 85+
    (50, 3),   # Tier 3: 50-85
    (20, 2),   # Tier 2: 20-50
    (0, 1),    # Tier 1: 0-20
]

def calculate_guild_tier_score(character):
    scores = character.db.domain_scores or {}
    primary = character.db.primary_domain
    secondary = character.db.secondary_domain
    if not primary:
        return 0.0
    p_score = float(scores.get(primary, 0.0))
    s_score = float(scores.get(secondary, 0.0)) if secondary else 0.0
    return (p_score * 0.66) + (s_score * 0.33)

def get_guild_tier(character):
    gts = calculate_guild_tier_score(character)
    for threshold, tier in GTS_TIER_THRESHOLDS:
        if gts >= threshold:
            return tier
    return 1

def get_guild_tier_label(character):
    guild_id = character.db.guild_id
    if not guild_id:
        return "Wanderer"
    tier = get_guild_tier(character)
    labels = GUILD_TIER_LABELS.get(guild_id)
    if not labels:
        return "Unknown"
    return labels[tier - 1]  # 0-indexed list, 1-indexed tier
```

### Guild Eligibility Check (DOM-03)
```python
# Source: D-04, D-05 from CONTEXT.md
# Threshold: domain score >= 30 (Practiced proficiency on 0-100 scale)

GUILD_ELIGIBILITY_THRESHOLD = 30

# Build reverse lookup: domain -> guild_id
_DOMAIN_TO_GUILD = {g["primary_domain"]: gid for gid, g in GUILDS.items()}

def check_guild_eligibility(character):
    """
    Return list of guild_ids the character qualifies for.
    A character qualifies when any domain score >= 30 and they have no guild.
    """
    if character.db.guild_id:
        return []  # already in a guild
    scores = character.db.domain_scores or {}
    eligible = []
    for domain, score in scores.items():
        if score >= GUILD_ELIGIBILITY_THRESHOLD:
            guild_id = _DOMAIN_TO_GUILD.get(domain)
            if guild_id:
                eligible.append(guild_id)
    return eligible
```

### Subclass Resolution Lookup
```python
# Build at module load from SUBCLASSES dict
_DOMAIN_PAIR_TO_SUBCLASS = {}
for sc_id, sc in SUBCLASSES.items():
    key = (sc["primary_domain"], sc["secondary_domain"])
    _DOMAIN_PAIR_TO_SUBCLASS[key] = sc_id

def _resolve_subclass(primary_domain, secondary_domain):
    """Return subclass_id for a domain pair, or None."""
    return _DOMAIN_PAIR_TO_SUBCLASS.get((primary_domain, secondary_domain))
```

### CharacterGuild Django Model
```python
# Source: D-14 from CONTEXT.md
# Follows BankAccount pattern (OneToOneField, lazy creation)

class CharacterGuild(models.Model):
    character = models.OneToOneField(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="guild_record",
    )
    guild_id = models.CharField(max_length=64, db_index=True)
    primary_domain = models.CharField(max_length=32)
    secondary_domain = models.CharField(max_length=32)
    subclass_id = models.CharField(max_length=64, db_index=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    induction_complete = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["guild_id"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.guild_id}/{self.subclass_id}"
```

## Data Inventory from Vault Sources

### 10 Guilds (from soravelon-guilds.md)
| guild_id | Name | Domain | Resource | Hidden |
|----------|------|--------|----------|--------|
| ironblood | Guild of Ironblood | combat | momentum | No |
| veilcraft | Guild of Veilcraft | subterfuge | focus | No |
| verdance | Guild of Verdance | naturalism | balance | No |
| resonance | Guild of Resonance | resonance | resonance | No |
| arcane | Guild of the Arcane | arcana | mana | No |
| accord | Guild of Accord | diplomacy | influence | No |
| thornwork | Guild of Thornwork | alchemy | reagents | No |
| warcraft | Guild of Warcraft | tactics | command | No |
| forge | Guild of Forge | engineering | components | No |
| vaelborn | Guild of Vaelborn | remnance | echoes | Yes |

### 10 Fingerprints (from soravelon-fingerprints.md)
| Domain | Verb | Resource |
|--------|------|----------|
| combat | press | Momentum |
| subterfuge | read | Focus |
| naturalism | calibrate | Balance |
| resonance | attune | Resonance |
| arcana | ration | Mana |
| diplomacy | leverage | Influence |
| alchemy | prepare | Reagents |
| tactics | orchestrate | Command |
| engineering | construct | Components |
| remnance | excavate | Echoes |

### 90 Subclasses (from soravelon-guilds.md)
All 90 subclasses are fully defined in the vault with name, fantasy, and hook. Each guild has 9 subclasses (one per non-primary domain). The complete list is extractable directly from the vault tables. No creative authoring required.

### Tier Labels (from soravelon-guilds.md)
```
Threshold:    0-20        20-50         50-85         85+
Ironblood:    Scrapper    Ironblood     Warblade      Bloodsworn
Veilcraft:    Shadow      Veilwalker    Phantom       The Unseen
Verdance:     Wanderer    Rootbound     Verdant       Ancient Voice
Resonance:    Listener    Attuned       Resonant      Harmonic
Arcane:       Initiate    Arcanist      Adept         Loremaster
Accord:       Envoy       Accord        Arbiter       Voice of the Realm
Thornwork:    Brewer      Thornworker   Compound      Transmuter
Warcraft:     Conscript   Tactician     Commander     Warchief
Forge:        Tinkerer    Forgehand     Artificer     Architect
Vaelborn:     (hidden)    Echoing       Vaelborn      The Unbroken
```

### Domain Proficiency Descriptors (from soravelon-abilities.md)
```
Score 0-9:    Unaware
Score 10-19:  Novice
Score 20-29:  Dabbler
Score 30-39:  Practiced     <-- guild eligibility threshold
Score 40-49:  Skilled
Score 50-59:  Proficient
Score 60-69:  Expert
Score 70-79:  Seasoned
Score 80-89:  Masterful
Score 90-99:  Virtuosic
Score 100:    Transcendent
```

Note: These are for the `domains` command display (Phase 5+). Phase 4 may optionally include these as constants for downstream use, at Claude's discretion.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | unittest (via `evennia test --settings settings tests/`) |
| Config file | None (Evennia test runner) |
| Quick run command | `evennia test --settings settings tests/test_guild_engine.py` |
| Full suite command | `evennia test --settings settings tests/` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOM-01 | Domain scores 0-100 with diminishing returns (pre-existing) | unit | `evennia test --settings settings tests/test_world_state.py` | Existing |
| DOM-02 | GTS = (primary x 0.66) + (secondary x 0.33) | unit | `evennia test --settings settings tests/test_guild_engine.py::TestGTSComputation` | Wave 0 |
| DOM-03 | check_guild_eligibility returns guilds at score >= 30 | unit | `evennia test --settings settings tests/test_guild_engine.py::TestGuildEligibility` | Wave 0 |
| DOM-04 | get_guild_tier_label returns correct tier label string | unit | `evennia test --settings settings tests/test_guild_engine.py::TestTierLabels` | Wave 0 |
| DOM-05 | FINGERPRINTS dict has 10 entries with distinct verbs | unit | `evennia test --settings settings tests/test_guild_engine.py::TestFingerprintRegistry` | Wave 0 |

### Test Pattern Decision
GTS computation and guild eligibility are pure logic functions that read from `character.db.domain_scores`. These can use `unittest.TestCase` with `MagicMock` characters -- no Evennia DB needed. The `join_guild()` function creates a Django model record, so it needs `EvenniaTest` (or Django `TestCase`).

Recommended split:
- Pure computation tests (GTS, tiers, eligibility, registry validation): `unittest.TestCase` + MagicMock
- Model mutation tests (join_guild, complete_induction): `EvenniaTest`

This follows the established pattern from Phase 1 (patrol_engine, trigger_engine, flight_engine tests all use unittest.TestCase with MagicMock).

### Sampling Rate
- **Per task commit:** `evennia test --settings settings tests/test_guild_engine.py`
- **Per wave merge:** `evennia test --settings settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_guild_engine.py` -- covers DOM-02 through DOM-05
- [ ] No conftest needed (unittest.TestCase pattern, not pytest fixtures)
- [ ] No framework install needed (Evennia test runner already available)

## Open Questions

1. **Domain proficiency descriptors in Phase 4?**
   - What we know: The vault defines 11 descriptor bands (Unaware through Transcendent). These are for the `domains` command display (Phase 5+).
   - What's unclear: Should Phase 4 include `DOMAIN_PROFICIENCY_LABELS` constant for downstream use, or defer entirely?
   - Recommendation: Include as a constant in guild_engine.py -- cheap to add, useful for Phase 5 and testing.

2. **Arcane guild tradition split**
   - What we know: Imperial and Western Arcana are mechanically identical, culturally distinct. Single guild entry with a note (per vault).
   - What's unclear: Does the GUILDS dict need a `traditions` field or is this purely narrative?
   - Recommendation: Single "arcane" guild entry. Hub_cities list includes all four cities. Tradition distinction is content/narrative, not engine data.

3. **Vaelborn Tier 1 label placeholder**
   - What we know: Tier 1 label is "(hidden)" or empty. When guild surfaces, label appears retroactively.
   - What's unclear: Should the constant store empty string, None, or the "(hidden)" placeholder?
   - Recommendation: Store empty string `""` for tier 1. Display logic (Phase 5+) handles the hidden state.

## Sources

### Primary (HIGH confidence)
- `C:\Obsidian\brain\Soravelon\soravelon-fingerprints.md` -- All 10 domain fingerprints with verbs, resources, descriptions
- `C:\Obsidian\brain\Soravelon\soravelon-guilds.md` -- 10 guilds, 90 subclasses, tier labels, GTS formula, data model shapes
- `C:\Obsidian\brain\Soravelon\soravelon-abilities.md` -- GTS computation, domain proficiency descriptors, domain score growth curve, guild discovery flow
- `world/world_state.py` -- Existing ALL_DOMAINS, domain_scores, calculate_backend_level()
- `world/models.py` -- Existing Django model patterns (FactionStanding, BankAccount)
- `typeclasses/characters.py` -- Existing db.guild_id, db.subclass_id, db.primary_domain, db.secondary_domain placeholders

### Secondary (MEDIUM confidence)
- None needed -- all data comes from vault sources and existing codebase

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries, pure Python + existing Django
- Architecture: HIGH -- follows established patterns (constant dicts, (bool,str) returns, lazy creation, hybrid storage)
- Pitfalls: HIGH -- identified from actual codebase inspection (no get_domain_score, scale mismatch, Vaelborn edge case)
- Data completeness: HIGH -- all 10 guilds, 90 subclasses, 10 fingerprints fully defined in vault

**Research date:** 2026-03-25
**Valid until:** Indefinite -- vault creative content is locked, codebase patterns are stable
