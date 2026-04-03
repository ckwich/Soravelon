# Phase 11: Quest MVP - Research

**Researched:** 2026-03-31
**Domain:** Django model + quest engine + action vocabulary integration + event hooks + player commands
**Confidence:** HIGH

## Summary

Phase 11 turns 20 authored quest specs (stored on zone objects via `area.quest()`) into a playable quest system. The work consists of four layers: (1) a new `CharacterQuest` Django model to track per-player quest state, (2) a stateless `world/quest_engine.py` module following the established engine pattern, (3) event hooks wired into existing mob death, item pickup, room enter, and dialogue systems, and (4) player-facing `quest` command plus reward payout via the existing `action_vocabulary.execute_action()` dispatch.

The project already has extensive infrastructure to support this: the `area.quest()` DSL stores quest definitions on `zone_obj.db.quest_definitions`, the dialogue system has `has_available_quest()` / `get_quest_offer()` stubs ready to wire, `CmdAccept` / `CmdDecline` exist with quest acceptance currently stubbed, and the `action_vocabulary` module provides reward dispatch for most reward types. Three new action handlers are needed: `give_scales`, `give_skill_xp`, and `modify_node_failure`.

**Primary recommendation:** Build the quest engine as a pure-logic module (`world/quest_engine.py`) with lightweight hooks inserted into 4 existing systems. Do NOT create a new Script or tick-driven mechanism -- quest progress is event-driven, fired from existing code paths.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** New `CharacterQuest` Django model: character FK, quest_id (str), status (active/complete/failed/abandoned), progress (int), started_at, completed_at. Migration required.
- **D-02:** Hard cap of 5 active quests per player. Must abandon one to accept a new one.
- **D-03:** Most quests re-acceptable after failure/abandonment. Builder sets optional `one_chance=True` flag per quest to permanently lock failed quests.
- **D-04:** Three terminal states: complete, failed, abandoned. Failed = system-triggered (timer, NPC death, wrong choice). Abandoned = player-triggered.
- **D-05:** Linear quest chains via `next_quest_id` field on quest spec. On completion, next quest auto-offers from same (or specified) NPC. Builder sets this in editor.
- **D-06:** No branching prerequisite system for MVP. Just linear chains. Branching can be added later.
- **D-07:** `kill` -- Track mob kills by template key or named_id. Progress: N/M killed. Fires on mob death event.
- **D-08:** `collect` -- Track items with specific item_tag in inventory. Progress: N/M collected. Checked on item pickup.
- **D-09:** `investigate` -- Visit a specific room. Tied to investigation skill -- may require successful `search` check at the location. Progress: 0 or 1 (boolean).
- **D-10:** `deliver` -- Carry a specific item to a specific NPC. Combines collect + talk_to. Progress: 0 or 1 (boolean).
- **D-11:** `talk_to` -- Talk to a specific NPC (for quest chain transitions). Progress: 0 or 1. Fires when player uses `talk` command with the target NPC.
- **D-12:** Rewards defined as action dict list, reusing the existing action_vocabulary pattern. Each reward = `{"action_type": "...", ...params}`. Builder already knows this from trigger authoring.
- **D-13:** Supported reward action types: give_scales, give_item, modify_standing, learn_recipe, give_skill_xp, teleport, spawn_mob, modify_node_failure, echo.
- **D-14:** Most reward types already exist as action_vocabulary handlers. Only `give_scales`, `give_skill_xp`, and `modify_node_failure` need new handlers.
- **D-15:** `quest` command with subcommands: `quest` (list all active), `quest <name>` (detail), `quest abandon <name>` (drop quest). Register in CharacterCmdSet.
- **D-16:** Quest list shows: quest name, progress bar, quest giver name. Detail shows: full description, objectives with progress, rewards preview.
- **D-17:** Wire `CmdAccept` in dialogue to create CharacterQuest record (currently stubbed).
- **D-18:** Wire `has_available_quest()` to check quest specs against player state (completed quests, active quests, one_chance flags).
- **D-19:** Quest progress hooks fire from existing systems: mob death -> kill objectives, item pickup -> collect objectives, room enter -> investigate objectives, talk command -> talk_to objectives.
- **D-20:** Quest completion triggers reward payout via action_vocabulary.execute_action() for each reward dict.
- **D-21:** Quest specs authored via `area.quest()` DSL method (already exists). Builder editor writes these into zone JSON. The quest engine reads quest specs from room/zone db attrs at runtime.
- **D-22:** All quest fields must be serializable to JSON for the builder: quest_id, quest_type, quest_giver, objectives (list of dicts), rewards (list of action dicts), next_quest_id, one_chance, share settings.

### Claude's Discretion
- Quest progress notification text format
- Whether investigate objectives require search check or just room visit
- Failure condition implementation details (timers, NPC death detection)
- Quest sharing mechanics (can_share, share_radius, share_cap from existing quest specs)
- Whether to implement quest_type categories (investigation, kill, fetch) as mechanical or cosmetic

### Deferred Ideas (OUT OF SCOPE)
- Quest timers / time-limited quests -- future milestone
- Quest sharing between group members (can_share fields exist in specs but sharing deferred)
- LLM-generated quest content -- Milestone 2+
- Branching prerequisite chains (requires_quest list) -- future enhancement to D-05
- Quest map markers / compass directions -- future UI feature
</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Django ORM | 4.2+ (via Evennia 6.0) | CharacterQuest model, migrations, queries | Already the project's data layer |
| Evennia 6.0 | 6.0 | TypeclassDB FK, server hooks, command framework | Game engine |
| Python 3.11+ | 3.11+ | Type hints, f-strings, walrus operator | Project standard |

### Supporting
No additional libraries needed. All functionality builds on existing project infrastructure:
- `world/action_vocabulary.py` -- reward dispatch
- `world/dialogue_engine.py` -- quest offer stubs
- `commands/cmd_dialogue.py` -- CmdAccept/CmdDecline
- `world/oob_publisher.py` -- push_quest_update()

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Django model for quest state | db attributes on Character | Model provides indexed queries, queryset filtering, and proper relational constraints -- db attrs would require scanning all characters for quest-related queries |
| Event hooks in existing code | New Script-based tick system | Event-driven is simpler, no polling overhead, and quest progress only needs to fire when the triggering event actually occurs |

## Architecture Patterns

### Recommended Project Structure
```
world/
  quest_engine.py           # NEW: stateless quest logic (accept, progress, complete, abandon)
  quest_definitions.py      # NEW: constants (QUEST_STATUS, OBJECTIVE_TYPES, MAX_ACTIVE_QUESTS)
  action_vocabulary.py      # MODIFIED: +3 new handlers (give_scales, give_skill_xp, modify_node_failure)
  dialogue_engine.py        # MODIFIED: wire has_available_quest(), get_quest_offer()
  models.py                 # MODIFIED: +CharacterQuest model
  migrations/0008_*.py      # NEW: CharacterQuest migration
commands/
  cmd_quest.py              # NEW: CmdQuest (list, detail, abandon)
  cmd_dialogue.py           # MODIFIED: wire CmdAccept to create CharacterQuest
  default_cmdsets.py        # MODIFIED: register CmdQuest
typeclasses/
  mobs.py                   # MODIFIED: add quest progress hook in at_death()
  rooms.py                  # MODIFIED: add quest progress hook in at_object_receive()
tests/
  test_quest_engine.py      # NEW: quest engine unit tests
```

### Pattern 1: Stateless Engine Module
**What:** `world/quest_engine.py` follows the established pattern of stateless service functions that take a character + context and return `(bool, str)` tuples. No class instances, no state held in the module.
**When to use:** All quest operations (accept, progress update, complete, abandon, query).
**Example:**
```python
# world/quest_engine.py — follows world/banking.py, world/inventory_engine.py pattern

def accept_quest(character, quest_id, quest_spec):
    """
    Accept a quest. Creates CharacterQuest record.
    Returns (bool, str).
    """
    from world.models import CharacterQuest

    # Check active quest cap (D-02)
    active_count = CharacterQuest.objects.filter(
        character=character, status="active"
    ).count()
    if active_count >= MAX_ACTIVE_QUESTS:
        return False, "You already have 5 active quests. Abandon one first."

    # Check one_chance lock (D-03)
    if quest_spec.get("one_chance"):
        if CharacterQuest.objects.filter(
            character=character, quest_id=quest_id, status="failed"
        ).exists():
            return False, "This quest is no longer available to you."

    # Check not already active
    if CharacterQuest.objects.filter(
        character=character, quest_id=quest_id, status="active"
    ).exists():
        return False, "You already have this quest."

    CharacterQuest.objects.create(
        character=character,
        quest_id=quest_id,
        status="active",
        progress=0,
    )
    return True, f"Quest accepted: {quest_spec.get('name', quest_id)}"
```

### Pattern 2: Event-Driven Progress Hooks
**What:** Lightweight checks inserted into existing event paths. Each hook queries `CharacterQuest.objects.filter()` to find matching active quests and updates progress.
**When to use:** Every quest progress trigger point (mob death, item pickup, room enter, talk).
**Example:**
```python
# Called from typeclasses/mobs.py at_death()
def check_kill_objectives(character, mob):
    """Check if any active quest has a kill objective matching this mob."""
    from world.models import CharacterQuest

    mob_template = mob.db.mob_template or mob.key
    mob_named_id = mob.db.mob_id or ""

    active_quests = CharacterQuest.objects.filter(
        character=character, status="active"
    )
    for cq in active_quests:
        quest_spec = _get_quest_spec(cq.quest_id)
        if not quest_spec:
            continue
        for obj in (quest_spec.get("objectives") or []):
            if obj.get("type") != "kill":
                continue
            target = obj.get("target")
            if target in (mob_template, mob_named_id):
                _increment_progress(cq, obj)
```

### Pattern 3: Quest Spec Lookup from Zone Objects
**What:** Quest definitions are stored on zone objects as `db.quest_definitions` (list of dicts). The engine looks up specs by scanning zone objects at runtime.
**When to use:** Any time the engine needs to read a quest's definition (objectives, rewards, chain info).
**Example:**
```python
def _get_quest_spec(quest_id):
    """Find a quest spec by ID across all loaded zones."""
    import evennia
    zone_objs = evennia.search_tag("zone_object", category="object_type")
    for zo in zone_objs:
        for qdef in (zo.db.quest_definitions or []):
            if qdef.get("quest_id") == quest_id:
                return qdef
    return None
```
**Performance note:** With 5 zones and ~4 quests each, this is fast enough. For scale, cache in a module-level dict rebuilt on server reload.

### Pattern 4: Reward Payout via Action Vocabulary
**What:** Quest completion iterates the quest spec's `rewards` list and calls `execute_action()` for each reward dict. This reuses the entire trigger action dispatch system.
**When to use:** On quest completion (after all objectives met).
**Example:**
```python
def _pay_rewards(character, quest_spec):
    """Execute all reward actions for a completed quest."""
    from world.action_vocabulary import execute_action

    context = {"character": character, "room": character.location}
    rewards = quest_spec.get("rewards") or []
    for reward_dict in rewards:
        execute_action(reward_dict, context)
```

### Anti-Patterns to Avoid
- **Script-based polling:** Do NOT create a QuestScript that checks progress on a timer. Quest progress is purely event-driven.
- **Storing quest state on db attributes:** Use the Django model. `db.active_quests` as a list would lose indexing, query capability, and atomic updates.
- **Duplicating action handler logic:** Rewards MUST go through `execute_action()`, not custom reward functions. This keeps the action vocabulary as the single dispatch point.
- **Direct room/mob DB writes from quest engine:** Always use existing engine functions (e.g., `pick_up()` for item rewards, `modify_standing()` for faction rewards).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Reward dispatch | Custom reward switch statement | `action_vocabulary.execute_action()` | 11+ action types already implemented; consistent interface |
| Item creation for rewards | Manual object creation | `create_item_from_template()` via `give_item` handler | Handles typeclass selection, db attrs, auto-stacking |
| Faction standing changes | Direct model update | `modify_standing()` via existing handler | Handles trust, betrayal flags, event logging |
| Scale currency awards | Direct `db.carried_scales +=` | New `give_scales` handler using `F()` expressions or banking pattern | Must follow atomic balance update convention |
| Skill XP awards | Direct `CharacterSkill` writes | New `give_skill_xp` handler calling `accumulate_skill_use()` | Respects ndb accumulator pattern, diminishing returns |
| OOB quest notifications | Direct `character.msg()` | `oob_publisher.push_quest_update()` | Follows OOB publisher convention, debouncing |
| NPC quest availability check | Ad-hoc logic in commands | `dialogue_engine.has_available_quest()` | Interface already exists as stub, designed for this |

**Key insight:** The project has a mature action vocabulary system. Quest rewards are just action dicts -- the same format builders already author for triggers. Building custom reward logic would violate the single-dispatch pattern and create a maintenance burden.

## Common Pitfalls

### Pitfall 1: Quest Spec Schema Mismatch
**What goes wrong:** The existing `area.quest()` DSL stores a flat dict with single `objective_type`/`objective_target`/`objective_count` fields. CONTEXT.md D-07 through D-11 describe a multi-objective system with an `objectives` list of dicts.
**Why it happens:** The DSL was authored before the quest engine was designed. Current quest specs have one objective each.
**How to avoid:** The quest engine must handle BOTH formats: (a) legacy flat format with single objective_type/target/count, and (b) new multi-objective format with `objectives: [{"type": ..., "target": ..., "count": ...}]`. Add a normalization step that converts flat format to a single-item objectives list. Update `area.quest()` to accept `objectives` kwarg for future quests.
**Warning signs:** Tests passing with new format but existing 20 quests failing at runtime.

### Pitfall 2: SaverDict Mutation Trap
**What goes wrong:** Direct mutation of `db.*` list/dict attributes silently fails to persist in Evennia.
**Why it happens:** Evennia's `SaverDict` requires reassignment to trigger the ORM save.
**How to avoid:** Always use the copy-mutate-reassign pattern. The CharacterQuest Django model avoids this entirely (standard ORM), but any `db.*` quest state on characters/zones must follow the pattern.
**Warning signs:** Progress updates not surviving server restarts.

### Pitfall 3: Circular Import from Quest Hooks
**What goes wrong:** Adding `from world.quest_engine import check_kill_objectives` at module level in `typeclasses/mobs.py` causes circular imports.
**Why it happens:** Quest engine imports models which import Evennia typeclasses.
**How to avoid:** Use lazy imports inside the hook functions, following the established pattern in this codebase. Every `world.*` import in typeclasses and commands is lazy (inside `func()` or handler methods).
**Warning signs:** `ImportError` on server start.

### Pitfall 4: Missing Quest Spec at Runtime
**What goes wrong:** A `CharacterQuest` record references a `quest_id` whose spec doesn't exist on any loaded zone object (zone not loaded, quest removed from spec, etc.).
**Why it happens:** Quest specs are stored on zone objects which are loaded at server start. If a zone fails to load, its quests become orphaned.
**How to avoid:** Always guard against `_get_quest_spec()` returning `None`. Silently skip progress checks for orphaned quests. Log a warning but don't crash.
**Warning signs:** `AttributeError: 'NoneType' object has no attribute 'get'` in quest progress hooks.

### Pitfall 5: Race Condition on Progress Increment
**What goes wrong:** Two mob deaths fire simultaneously, both read progress=4, both write progress=5, quest completes with 5/6 kill requirement actually met.
**Why it happens:** Evennia's event loop is single-threaded for Twisted callbacks, but Django ORM reads aren't locked.
**How to avoid:** Use `F()` expressions for progress increments: `CharacterQuest.objects.filter(id=cq.id).update(progress=F('progress') + 1)`. Then re-read to check completion. This follows the atomic balance update convention (base skill rule #6).
**Warning signs:** Quests completing with wrong progress counts under concurrent events.

### Pitfall 6: Quest Spec Format Needs Enrichment
**What goes wrong:** The existing 20 quest specs lack the fields the quest engine needs: `name`, `description`, `objectives` (as list), `rewards` (as action dicts), `next_quest_id`, `one_chance`.
**Why it happens:** The `area.quest()` DSL was designed for data collection, not runtime execution. Current specs have `consequence_small`/`consequence_medium` (narrative text) and empty `reward_tiers`.
**How to avoid:** Phase must include a plan to enrich the `area.quest()` DSL to accept all new fields, AND update the 20 existing quest specs to include `name`, `description`, `objectives` list, and `rewards` list. This is a content authoring task, not just engine work.
**Warning signs:** All 20 quests accepted but none completable because objectives/rewards are empty.

### Pitfall 7: Node Failure Modification Needs Script Access
**What goes wrong:** The `modify_node_failure` action handler can't find the NodeScript to adjust failure percentage.
**Why it happens:** NodeScripts are attached to zone objects, not globally registered. Need to look up the zone object by zone_id, then find its script.
**How to avoid:** The handler should: (1) get `zone_id` from the action dict, (2) `search_tag(zone_id, category="zone_id")` to find the zone object, (3) get the `node_script` from `zone_obj.scripts.get("node_script")`, (4) adjust `script.db.failure` and call `script._update_state()`.
**Warning signs:** `modify_node_failure` silently failing because no script found.

## Code Examples

### CharacterQuest Django Model
```python
# world/models.py — new model (migration 0008)
class CharacterQuest(models.Model):
    """
    Tracks a character's progress on a specific quest.
    One record per (character, quest_id, attempt). Terminal states:
    complete, failed, abandoned. Active state: active.
    """
    STATUS_CHOICES = [
        ("active", "Active"),
        ("complete", "Complete"),
        ("failed", "Failed"),
        ("abandoned", "Abandoned"),
    ]

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="character_quests",
    )
    quest_id = models.CharField(max_length=128, db_index=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="active")
    progress = models.JSONField(default=dict)  # {"kill_ash_wolf": 4, "collect_fang": 2}
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["character", "status"]),
            models.Index(fields=["character", "quest_id"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.quest_id}={self.status}"
```

**Design note on `progress` field:** Using a JSONField dict (keyed by objective identifier) rather than a single integer allows multi-objective quests to track each objective independently. For single-objective quests, this is just `{"main": 4}`.

### New Action Handlers
```python
# In world/action_vocabulary.py

def _handle_give_scales(action_dict, context, _depth):
    """Award Scales to character's carried_scales."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    amount = action_dict.get("amount", 0)
    if amount <= 0:
        return False, "give_scales: invalid amount"
    current = character.db.carried_scales or 0
    character.db.carried_scales = current + amount
    character.msg(f"|y[+{amount} Scales]|n")
    return True, ""


def _handle_give_skill_xp(action_dict, context, _depth):
    """Award skill XP via the accumulator pattern."""
    character = context.get("character")
    if not character:
        return False, "No character in context"
    skill_id = action_dict.get("skill_id")
    count = action_dict.get("count", 1)
    if not skill_id:
        return False, "give_skill_xp: missing skill_id"
    from world.skill_engine import accumulate_skill_use
    accumulate_skill_use(character, skill_id, count)
    return True, ""


def _handle_modify_node_failure(action_dict, context, _depth):
    """Adjust node failure percentage for a zone."""
    zone_id = action_dict.get("zone_id")
    delta = action_dict.get("delta", 0)
    if not zone_id:
        return False, "modify_node_failure: missing zone_id"
    import evennia
    zone_objs = evennia.search_tag(zone_id, category="zone_id")
    if not zone_objs:
        return False, f"modify_node_failure: zone '{zone_id}' not found"
    zone_obj = zone_objs[0]
    scripts = zone_obj.scripts.get("node_script")
    if not scripts:
        return False, f"modify_node_failure: no node_script on zone '{zone_id}'"
    script = scripts[0]
    old_failure = script.db.failure
    new_failure = max(0.0, min(100.0, old_failure + delta))
    script.db.failure = new_failure
    script._update_state(old_failure, new_failure)
    return True, ""
```

### Wiring CmdAccept to Quest Engine
```python
# In commands/cmd_dialogue.py CmdAccept.func()
# Replace the stub section:

from world.quest_engine import accept_quest
success, msg = accept_quest(character, quest_data.get("quest_id"), quest_data)
if not success:
    character.msg(f"|r{msg}|n")
    character.ndb.pending_quest_offer = None
    return
# ... existing OOB push and confirmation message ...
```

### Quest Progress Hook in Mob Death
```python
# In typeclasses/mobs.py at_death(), after existing trigger/loot code:

# Quest progress: kill objectives (D-07)
if killer and hasattr(killer, 'account') and killer.account:
    from world.quest_engine import check_kill_objectives
    check_kill_objectives(killer, self)
```

### Dialogue Engine Quest Availability
```python
# Wire has_available_quest() in world/dialogue_engine.py
def has_available_quest(npc, character):
    """Check if NPC has a quest available for this character."""
    from world.quest_engine import get_available_quest_for_npc
    return get_available_quest_for_npc(npc, character) is not None


def get_quest_offer(npc, character):
    """Get the quest offer data for display."""
    from world.quest_engine import get_available_quest_for_npc
    return get_available_quest_for_npc(npc, character)
```

### Quest Spec Enrichment (area.quest DSL update)
```python
# Updated area.quest() call with full fields:
area.quest(
    "vc_q_rat_problem",
    name="Cellar Menace",
    description="Marta Voss needs someone to clear the rats from her cellar.",
    quest_type="combat",       # cosmetic category
    quest_giver="npc_barkeep_marta_voss",
    objectives=[
        {"type": "kill", "target": "sewer_rat", "count": 10,
         "description": "Kill sewer rats"},
    ],
    rewards=[
        {"action_type": "give_scales", "amount": 50},
        {"action_type": "modify_standing", "faction_id": "consortium", "delta": 100},
        {"action_type": "echo", "message": "|gMarta nods approvingly. 'That should keep them out for a while.'|n"},
    ],
    # Legacy fields preserved for backward compat:
    objective_type="kill",
    objective_target="sewer_rat",
    objective_count=10,
)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single-objective flat quest spec | Multi-objective `objectives` list | This phase | All 20 quest specs need enrichment |
| `has_available_quest()` returns False | Wired to quest engine | This phase | NPCs now offer quests dynamically |
| `CmdAccept` stub (no record creation) | Creates `CharacterQuest` record | This phase | Quest acceptance becomes functional |
| `set_quest_flag` stub in action_vocabulary | Removed/replaced by quest engine queries | This phase | Quest state in model, not flags |
| `reward_tiers` empty dict | `rewards` list of action dicts | This phase | Rewards are executable |

**Deprecated/outdated:**
- `set_quest_flag` action type: Replace with quest-engine-driven state. Quest completion is checked via `CharacterQuest.status`, not flags.
- `objective_type`/`objective_target`/`objective_count` flat fields on quest specs: Preserved for backward compat but engine reads from `objectives` list.
- `reward_tiers` dict: Replaced by flat `rewards` list of action dicts.
- `consequence_small`/`consequence_medium` fields: Narrative metadata, not mechanical. Preserved but not consumed by engine.

## Open Questions

1. **Quest spec enrichment scope**
   - What we know: All 20 existing quest specs use legacy flat format. They need `name`, `description`, `objectives` list, and `rewards` list added.
   - What's unclear: How much creative writing is needed for quest names/descriptions. Some quest specs have `objective_type` values that don't match the 5 MVP types (e.g., `"escort"`, `"craft"`, `"gather"`, `"recover"`). These need mapping to the 5 supported types or flagging as non-functional in MVP.
   - Recommendation: Map `gather`/`recover` to `collect`, map `craft` to `collect` (collect crafted item), and either implement `escort` as `talk_to` at destination or flag `cantera_lost_traveler` as non-functional in MVP. Author all 20 quest names/descriptions as part of the enrichment plan.

2. **Investigate objective: search check vs. room visit**
   - What we know: D-09 says "may require successful `search` check at the location."
   - What's unclear: Whether this adds significant complexity worth implementing in MVP.
   - Recommendation: For MVP, `investigate` objectives complete on room entry (simpler). Add optional `requires_search: true` flag that gates completion behind a `CmdSearch` usage at the room. This is a low-effort enhancement that adds gameplay depth.

3. **Quest_type as mechanical vs. cosmetic**
   - What we know: Quest specs have `quest_type` values like "combat", "investigation", "delivery", "social", "crafting", "exploration", "gathering".
   - What's unclear: Whether these should affect gameplay (e.g., different XP types, different UI icons).
   - Recommendation: Treat as cosmetic label for MVP. Store on the spec, display in quest UI, but no mechanical effect. This keeps scope tight.

4. **Non-MVP objective types in existing specs**
   - What we know: Some existing specs use objective types not in the 5 MVP types: `"escort"` (cantera_lost_traveler), `"craft"` (vc_q_forging_commission), `"gather"` (vc_q_herbalist_gathering, rf_q_rare_ingredients), `"recover"` (vc_q_stolen_goods), `"discover"` (ashreach_ruin_investigation).
   - Recommendation: Map these to MVP types: `gather` -> `collect`, `recover` -> `collect`, `discover` -> `investigate`, `craft` -> `collect` (require finished item in inventory), `escort` -> `talk_to` (talk to NPC at destination). Document the mapping.

## Existing Quest Spec Inventory

| Zone | Quest ID | Type | Giver | Objective | Count | MVP Mapping |
|------|----------|------|-------|-----------|-------|-------------|
| Vael's Crossing | vc_q_missing_shipment | investigation | npc_broker_carston | investigate | 1 | investigate |
| Vael's Crossing | vc_q_rat_problem | combat | npc_barkeep_marta_voss | kill | 10 | kill |
| Vael's Crossing | vc_q_warden_report | delivery | npc_warden_agent_calloway | deliver | 1 | deliver |
| Vael's Crossing | vc_q_debt_collection | social | npc_debt_collector_raith | collect | 3 | collect |
| Vael's Crossing | vc_q_forging_commission | crafting | npc_smith_goram | craft | 1 | collect |
| Vael's Crossing | vc_q_stolen_goods | investigation | npc_fence_shadow_mekk | recover | 5 | collect |
| Vael's Crossing | vc_q_tower_mystery | exploration | npc_guildmaster_remnance_morwen | investigate | 3 | investigate |
| Vael's Crossing | vc_q_herbalist_gathering | gathering | npc_herbalist_old_ystra | gather | 5 | collect |
| Ashreach | ashreach_wolf_overpopulation | kill | npc_warden_captain_ashwyn | kill | 10 | kill |
| Ashreach | ashreach_bandit_problem | kill | npc_warden_captain_ashwyn | kill | 6 | kill |
| Ashreach | ashreach_ruin_investigation | investigate | npc_hermit_scholar_obed | discover | 3 | investigate |
| Reth Foothills | rf_q_lost_miners | investigation | npc_foreman_halvek | investigate | 3 | investigate |
| Reth Foothills | rf_q_troll_menace | combat | npc_warden_captain_serra | kill | 5 | kill |
| Reth Foothills | rf_q_rare_ingredients | gathering | npc_hermit_alchemist_old_renn | gather | 4 | collect |
| Cantera Edge | cantera_resupply | delivery | npc_warden_kaelen | deliver | 3 | deliver |
| Cantera Edge | cantera_lost_traveler | escort | npc_traveler_mirren | escort | 1 | talk_to |
| Cantera Edge | cantera_node_study | investigation | npc_druid_thaelen | collect | 5 | collect |
| Stormhaven Coast | sc_q_raider_bounty | combat | npc_coastguard_captain_aldren | kill | 10 | kill |
| Stormhaven Coast | sc_q_deep_cave_rumors | exploration | npc_fisherman_old_korrin | investigate | 1 | investigate |
| Stormhaven Coast | sc_q_smuggler_delivery | delivery | npc_smuggler_contact_veyra | deliver | 1 | deliver |

**Summary:** 5 kill, 5 investigate, 4 collect (mapped), 3 deliver, 1 talk_to (mapped escort), 2 collect (mapped gather) = all 20 map to MVP types.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | unittest.TestCase + MagicMock (pure logic), EvenniaTest (model tests) |
| Config file | `tests/` directory, run via `evennia test --settings server.conf.settings tests/` |
| Quick run command | `evennia test --settings server.conf.settings tests/test_quest_engine.py` |
| Full suite command | `evennia test --settings server.conf.settings tests/` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| D-01 | CharacterQuest model creation and constraints | unit (EvenniaTest) | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestCharacterQuestModel -x` | Wave 0 |
| D-02 | 5 active quest cap enforcement | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestAcceptQuest -x` | Wave 0 |
| D-03 | one_chance flag blocks re-acceptance | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestOneChance -x` | Wave 0 |
| D-07 | Kill objective progress on mob death | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestKillObjective -x` | Wave 0 |
| D-08 | Collect objective progress on pickup | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestCollectObjective -x` | Wave 0 |
| D-09 | Investigate objective on room enter | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestInvestigateObjective -x` | Wave 0 |
| D-10 | Deliver objective (item + NPC) | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestDeliverObjective -x` | Wave 0 |
| D-11 | Talk_to objective on talk command | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestTalkToObjective -x` | Wave 0 |
| D-12/D-20 | Reward payout via action_vocabulary | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestRewardPayout -x` | Wave 0 |
| D-14 | New action handlers (give_scales, give_skill_xp, modify_node_failure) | unit | `evennia test --settings server.conf.settings tests/test_action_vocabulary.py -x` | Existing file, add tests |
| D-15/D-16 | CmdQuest list, detail, abandon | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestCmdQuest -x` | Wave 0 |
| D-17 | CmdAccept creates CharacterQuest | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestCmdAcceptWired -x` | Wave 0 |
| D-18 | has_available_quest wired correctly | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestQuestAvailability -x` | Wave 0 |
| D-05 | Quest chain auto-offer on completion | unit | `evennia test --settings server.conf.settings tests/test_quest_engine.py::TestQuestChain -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `evennia test --settings server.conf.settings tests/test_quest_engine.py`
- **Per wave merge:** `evennia test --settings server.conf.settings tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_quest_engine.py` -- covers D-01 through D-22
- [ ] Add `give_scales`, `give_skill_xp`, `modify_node_failure` tests to existing `tests/test_action_vocabulary.py`

## Project Constraints (from CLAUDE.md)

1. **Return `(bool, str)` tuples** from all quest engine functions -- no exceptions for normal flow
2. **Backend level is INTERNAL ONLY** -- never expose to players (quest text must not reference levels)
3. **Lazy record creation** -- missing CharacterQuest record = no quest (default state)
4. **SaverDict copy pattern** -- any `db.*` mutations must copy-mutate-reassign
5. **Relational data in Django models** -- CharacterQuest goes in `world/models.py`, not `db.*` attributes
6. **Atomic balance updates** -- quest progress increments should use `F()` expressions
7. **OOB messages through oob_publisher** -- quest notifications via `push_quest_update()`
8. **Lazy imports throughout** -- all `world.*` imports inside functions in typeclasses/commands
9. **All game logic in `world/` modules** -- CmdQuest is a thin dispatcher to quest_engine.py
10. **Custom Django models in `world/models.py`** -- register via migration
11. **Tests use EvenniaTestCase for model tests, unittest.TestCase+MagicMock for pure logic**
12. **No visible levels** -- quest rewards/descriptions must not reference player levels

## Sources

### Primary (HIGH confidence)
- `world/action_vocabulary.py` -- Verified all 14 existing action handlers, stub list, and execute_action() dispatch pattern
- `world/dialogue_engine.py` -- Verified has_available_quest() and get_quest_offer() stubs, _build_dialogue_context() quest state stubs
- `commands/cmd_dialogue.py` -- Verified CmdAccept/CmdDecline implementation, pending_quest_offer lifecycle
- `world/area_builder.py:quest()` -- Verified quest spec storage format on zone_obj.db.quest_definitions
- `world/models.py` -- Verified all existing model patterns (FK to ObjectDB, unique_together, auto timestamps, indexes)
- `world/areas/*.py` -- Verified all 20 quest spec definitions across 5 zones
- `typeclasses/mobs.py:at_death()` -- Verified mob death hook location and existing trigger/loot code
- `typeclasses/rooms.py:at_object_receive()` -- Verified room entry hook location and existing trigger/flight code
- `commands/default_cmdsets.py` -- Verified CharacterCmdSet command registration pattern
- `world/migrations/` -- Verified latest migration is 0007_merge; next is 0008

### Secondary (MEDIUM confidence)
- Quest spec enrichment needs -- inferred from comparing existing flat specs vs. CONTEXT.md multi-objective design
- Performance of zone-object scan for quest lookup -- expected fast with 5 zones; no benchmarks

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new libraries, all existing infrastructure
- Architecture: HIGH - follows established patterns (stateless engines, action vocabulary, Django models, lazy imports)
- Pitfalls: HIGH - derived from direct code inspection of all integration points
- Quest spec enrichment: MEDIUM - 20 quest specs need creative content (names, descriptions, rewards) which is authoring work

**Research date:** 2026-03-31
**Valid until:** 2026-04-30 (stable -- no external dependencies, all internal code)
