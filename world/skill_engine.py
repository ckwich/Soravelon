"""
Skill engine for Soravelon.

Handles all three skill improvement methods:
- Passive use: ndb counts batch into durable remainders (10 uses = +0.1 before diminishing)
- Deliberate practice: 24hr rolling cooldown per skill, tier-based random gains
- Trainer sessions: NPC-driven, costs Scales, enhances next practice gain

Also handles ancestry seed application and the discovery trigger framework.
Skills are independent of the domain/guild system (SKL-04).

Performance: get_skill_value makes 1 DB read. commit_skill_accumulators makes
up to N locked get_or_create calls (only for skills with accumulated uses).
"""

import random
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from world.skill_definitions import (
    ANCESTRY_SKILL_SEEDS,
    DIMINISHING_BRACKETS,
    DISCOVERY_TRIGGERS,
    PASSIVE_ACCUMULATOR_THRESHOLD,
    PASSIVE_GAIN_PER_THRESHOLD,
    PRACTICE_GAINS,
    SELVAR_COAT_TO_LINEAGE,
    SKILL_DEFINITIONS,
    TRAINER_QUALITY_MULTIPLIER,
    TRAINER_REGISTRY,
)


# --- Internal Helpers ---

def _get_diminishing_rate(current_value):
    """Return the gain rate multiplier for the given skill value."""
    for low, high, rate in DIMINISHING_BRACKETS:
        if low <= current_value <= high:
            return rate
    return 0.0


def _get_practice_gain_range(current_value):
    """Return (min_gain, max_gain) for the given skill value tier."""
    for low, high, min_gain, max_gain in PRACTICE_GAINS:
        if low <= current_value <= high:
            return min_gain, max_gain
    return 0.0, 0.0


def _crossed_threshold(old_value, new_value):
    """Check if a skill value crossed any threshold (25/50/75/90/100)."""
    thresholds = [25, 50, 75, 90, 100]
    for t in thresholds:
        if old_value < t <= new_value:
            return True
    return False


# --- Read Functions ---

def get_skill_value(character, skill_id):
    """
    Get the current value of a skill for a character.
    Returns 0.0 for unlearned skills (lazy creation).
    """
    from world.models import CharacterSkill

    try:
        record = CharacterSkill.objects.get(
            character=character, skill_id=skill_id
        )
        return record.value
    except CharacterSkill.DoesNotExist:
        return 0.0


def get_skills_by_type(character, skill_type):
    """
    Get all non-zero skills of a given type for a character.
    Returns list of dicts with skill_id, name, value, last_practiced_at.
    """
    from world.models import CharacterSkill

    records = CharacterSkill.objects.filter(
        character=character,
        skill_type=skill_type,
        value__gt=0,
    ).order_by("-value")

    result = []
    for record in records:
        defn = SKILL_DEFINITIONS.get(record.skill_id, {})
        result.append({
            "skill_id": record.skill_id,
            "name": defn.get("name", record.skill_id),
            "value": record.value,
            "last_practiced_at": record.last_practiced_at,
        })
    return result


# --- Passive Use Accumulation ---

def accumulate_skill_use(character, skill_id, count=1):
    """
    Increment the ndb accumulator for a skill.
    No DB write — batched via commit_skill_accumulators().
    """
    key = f"skill_use_{skill_id}"
    current = getattr(character.ndb, key, 0) or 0
    setattr(character.ndb, key, current + count)


def commit_skill_accumulators(character):
    """
    Batch commit all accumulated skill uses from ndb to DB.
    Called at session end, safety flush, or explicit commit points.
    For each skill with >= PASSIVE_ACCUMULATOR_THRESHOLD uses,
    applies passive gain with diminishing returns.
    """
    pending = {
        skill_id: getattr(character.ndb, f"skill_use_{skill_id}", 0) or 0
        for skill_id in SKILL_DEFINITIONS
    }
    pending = {skill_id: count for skill_id, count in pending.items() if count > 0}
    if not pending:
        return

    with transaction.atomic():
        apply_skill_use_counts(character, pending)

    # Volatile counts clear only after every durable write succeeds. Partial
    # thresholds are now retained on CharacterSkill rather than in ndb.
    for skill_id in pending:
        setattr(character.ndb, f"skill_use_{skill_id}", 0)


def apply_skill_use_counts(character, skill_counts):
    """Persist passive-use counts, including sub-threshold remainders."""
    from world.models import CharacterSkill

    for skill_id, use_count in skill_counts.items():
        if skill_id not in SKILL_DEFINITIONS:
            raise ValueError(f"Unknown skill: {skill_id}")
        if not isinstance(use_count, int) or isinstance(use_count, bool) or use_count <= 0:
            raise ValueError(f"Skill use count for {skill_id} must be a positive integer.")

        record, _ = CharacterSkill.objects.select_for_update().get_or_create(
            character=character,
            skill_id=skill_id,
            defaults={
                "skill_type": SKILL_DEFINITIONS[skill_id]["skill_type"],
                "value": 0.0,
                "passive_use_remainder": 0,
            },
        )

        accumulated = int(record.passive_use_remainder or 0) + use_count
        thresholds_hit, remainder = divmod(accumulated, PASSIVE_ACCUMULATOR_THRESHOLD)
        old_value = record.value
        current = record.value
        for _ in range(thresholds_hit):
            rate = _get_diminishing_rate(current)
            current = min(100.0, current + PASSIVE_GAIN_PER_THRESHOLD * rate)

        record.value = current
        record.passive_use_remainder = remainder
        record.save(update_fields=["value", "passive_use_remainder"])

        if current > old_value and _crossed_threshold(old_value, current):
            check_discoveries(character, skill_id, current)


# --- Deliberate Practice ---

def practice_skill(character, skill_id):
    """
    Practice a skill deliberately. 24hr rolling cooldown per skill.
    Returns (bool, str).
    """
    from world.models import CharacterSkill

    if skill_id not in SKILL_DEFINITIONS:
        return (False, f"Unknown skill: {skill_id}")

    defn = SKILL_DEFINITIONS[skill_id]

    record, _ = CharacterSkill.objects.get_or_create(
        character=character,
        skill_id=skill_id,
        defaults={
            "skill_type": defn["skill_type"],
            "value": 0.0,
        },
    )

    now = timezone.now()
    if record.last_practiced_at:
        elapsed = now - record.last_practiced_at
        if elapsed < timedelta(hours=24):
            remaining = timedelta(hours=24) - elapsed
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            return (
                False,
                f"|y[{defn['name']}: next practice in {hours}h {minutes}m]|n",
            )

    if record.value >= 100.0:
        return (False, f"|y[{defn['name']}: already at mastery (100)]|n")

    old_value = record.value

    min_gain, max_gain = _get_practice_gain_range(record.value)
    base_gain = random.uniform(min_gain, max_gain)
    rate = _get_diminishing_rate(record.value)
    gain = base_gain * rate

    # Check trainer bonus (consumed on use)
    trainer_key = f"trainer_bonus_{skill_id}"
    trainer_mult = getattr(character.ndb, trainer_key, None)
    if trainer_mult:
        gain *= trainer_mult
        setattr(character.ndb, trainer_key, None)

    # Above threshold without trainer = halved gain
    trainer_threshold = defn.get("trainer_required_above", 50)
    trainer_note = ""
    if record.value > trainer_threshold and not trainer_mult:
        gain *= 0.5
        trainer_note = (
            f"\n|w[Above {trainer_threshold} — find a trainer "
            f"to improve faster]|n"
        )

    record.value = min(100.0, record.value + gain)
    record.last_practiced_at = now
    record.save()

    if _crossed_threshold(old_value, record.value):
        check_discoveries(character, skill_id, record.value)

    return (
        True,
        f"|g[{defn['name']}: {old_value:.0f} -> {record.value:.0f}]|n"
        f"\n|w[Next practice available in 24 hours]|n"
        f"{trainer_note}",
    )


# --- Trainer Sessions ---

def train_with_trainer(character, skill_id, trainer_id):
    """
    Train with an NPC trainer. Costs Scales, enhances next practice gain.
    Returns (bool, str).
    """
    if trainer_id not in TRAINER_REGISTRY:
        return (False, "That trainer is not available.")

    trainer = TRAINER_REGISTRY[trainer_id]

    if skill_id not in trainer.get("skills_taught", []):
        return (False, f"{trainer['name']} does not teach that skill.")

    if skill_id not in SKILL_DEFINITIONS:
        return (False, f"Unknown skill: {skill_id}")

    cost = trainer.get("cost_per_session", 50)
    carried = character.db.carried_scales or 0
    if carried < cost:
        return (
            False,
            f"|r[Not enough Scales. Training costs {cost}, "
            f"you carry {carried}.]|n",
        )

    character.db.carried_scales = carried - cost

    quality = trainer.get("trainer_quality", "apprentice")
    multiplier = TRAINER_QUALITY_MULTIPLIER.get(quality, 1.25)
    trainer_key = f"trainer_bonus_{skill_id}"
    setattr(character.ndb, trainer_key, multiplier)

    defn = SKILL_DEFINITIONS[skill_id]
    return (
        True,
        f"|g[{trainer['name']} coached you on {defn['name']}. "
        f"Next practice will be enhanced.]|n"
        f"\n|w[{cost} Scales deducted]|n",
    )


# --- Ancestry Skill Seeds ---

def apply_ancestry_skill_seeds(character, ancestry_id, coat=None):
    """
    Apply starting skill values based on ancestry.
    Called at character creation. For Selvar, coat determines lineage.
    """
    from world.models import CharacterSkill

    if ancestry_id.startswith("selvar") and coat:
        lineage = SELVAR_COAT_TO_LINEAGE.get(coat)
        ancestry_key = lineage if lineage else ancestry_id
    else:
        ancestry_key = ancestry_id

    seeds = ANCESTRY_SKILL_SEEDS.get(ancestry_key, {})

    for seed_skill_id, seed_value in seeds.items():
        if seed_skill_id not in SKILL_DEFINITIONS:
            continue

        defn = SKILL_DEFINITIONS[seed_skill_id]
        record, created = CharacterSkill.objects.get_or_create(
            character=character,
            skill_id=seed_skill_id,
            defaults={
                "skill_type": defn["skill_type"],
                "value": seed_value,
            },
        )

        # Defensive: only raise, never lower
        if not created and record.value < seed_value:
            record.value = seed_value
            record.save()


# --- Discovery Framework ---

def check_discoveries(character, changed_skill_id, new_value):
    """
    Check if any discovery triggers are met after a skill threshold crossing.
    Uses SaverDict copy pattern for character.db.discoveries mutation.
    """
    from world.models import CharacterSkill

    discovered = set(character.db.discoveries or [])

    for trigger in DISCOVERY_TRIGGERS:
        trigger_id = trigger["id"]
        if trigger_id in discovered:
            continue

        conditions = trigger.get("conditions", {})
        all_met = True
        for req_skill_id, req_value in conditions.items():
            if req_skill_id == changed_skill_id:
                if new_value < req_value:
                    all_met = False
                    break
            else:
                try:
                    record = CharacterSkill.objects.get(
                        character=character, skill_id=req_skill_id
                    )
                    if record.value < req_value:
                        all_met = False
                        break
                except CharacterSkill.DoesNotExist:
                    all_met = False
                    break

        if all_met:
            # SaverDict copy pattern
            new_discovered = list(discovered)
            new_discovered.append(trigger_id)
            character.db.discoveries = new_discovered
            discovered.add(trigger_id)

            message = trigger.get("message", "You discover something new...")
            character.msg(f"|m[Discovery: {message}]|n")
