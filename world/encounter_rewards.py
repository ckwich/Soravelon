"""Durable personal reward and proximity-credit rules for combat encounters."""

from django.utils import timezone


def snapshot_reward_recipients(mob, killer):
    """Return the live, same-room allied players participating at death time."""
    if not _is_player(killer):
        return []

    room = getattr(mob, "location", None)
    candidates = [killer]
    handler = getattr(getattr(mob, "ndb", None), "combat_handler", None)
    get_players = getattr(handler, "get_player_combatants", None)
    if callable(get_players):
        candidates.extend(get_players() or [])

    from world.group_engine import are_allies

    recipients = []
    seen_ids = set()
    for candidate in candidates:
        candidate_id = getattr(candidate, "id", None)
        if (
            not candidate
            or candidate_id in seen_ids
            or getattr(candidate, "location", None) != room
            or not _is_player(candidate)
        ):
            continue
        if candidate is not killer and not are_allies(killer, candidate):
            continue
        recipients.append(candidate)
        seen_ids.add(candidate_id)
    return recipients


def create_personal_entitlements(mob, corpse, recipients):
    """Persist one independent personal reward package for every recipient."""
    from world.loot_tables import roll_loot
    from world.models import EncounterReward

    created_for = []
    scales = _personal_scales(mob)
    for recipient in recipients:
        item_definitions = [
            item_def
            for item_def in roll_loot(mob, recipient)
            if _is_personal_drop(item_def)
        ]
        if not item_definitions and not scales:
            continue
        EncounterReward.objects.create(
            character=recipient,
            corpse_id=corpse.id,
            source_mob_key=_mob_reward_key(mob),
            item_definitions=item_definitions,
            scales=scales,
        )
        created_for.append(recipient)
    return created_for


def roll_shared_drops(mob, killer):
    """Roll only authored shared drops; personal loot is handled per recipient."""
    from world.loot_tables import roll_loot

    return [
        item_def
        for item_def in roll_loot(mob, killer)
        if not _is_personal_drop(item_def)
    ]


def claim_personal_rewards(character, *, corpse_id=None):
    """Claim pending personal rewards without consuming any other player's row."""
    from world.item_spawner import create_item_from_template
    from world.models import EncounterReward

    # Command tests and tooling can use lightweight stand-ins. Durable claims
    # require an actual persisted Evennia character row.
    if not isinstance(getattr(character, "pk", None), int):
        return {"items": [], "scales": 0, "claimed": 0}

    from world.atomic_state import atomic_evennia_state

    with atomic_evennia_state(character) as tracker:
        tracker.track(character, attributes=("carried_scales",))
        rewards = EncounterReward.objects.select_for_update().filter(
            character=character,
            claimed_at__isnull=True,
        )
        if corpse_id is not None:
            rewards = rewards.filter(corpse_id=corpse_id)
        rewards = list(rewards.order_by("granted_at", "id"))
        if not rewards:
            return {"items": [], "scales": 0, "claimed": 0}

        item_names = []
        scales = 0
        for reward in rewards:
            for item_def in reward.item_definitions or []:
                create_item_from_template(item_def, location=character)
                item_names.append(item_def.get("key") or item_def.get("item_id", "item"))
            scales += reward.scales

        if scales:
            character.db.carried_scales = (character.db.carried_scales or 0) + scales

        claimed_at = timezone.now()
        for reward in rewards:
            reward.claimed_at = claimed_at
            reward.save(update_fields=["claimed_at"])

    return {"items": item_names, "scales": scales, "claimed": len(rewards)}


def grant_kill_credit(recipients, mob):
    """Advance objectives and one-time named/boss progression for recipients."""
    from world.quest_engine import check_kill_objectives
    from world.mob_spawner import MOB_INSTANCE_TAG_CATEGORY
    from world.progression_engine import record_combat_outcome

    named_tag = mob.tags.get(category=MOB_INSTANCE_TAG_CATEGORY)
    is_named = bool(named_tag)
    is_legendary = getattr(mob.db, "rarity", None) == "legendary"
    source_id = (
        getattr(mob.db, "named_id", None)
        or named_tag
        or _mob_reward_key(mob)
    )

    for recipient in recipients:
        if _is_player(recipient):
            check_kill_objectives(recipient, mob)
            if not isinstance(getattr(recipient, "pk", None), int):
                continue
            progressed, progression_message = record_combat_outcome(
                recipient,
                str(source_id),
                is_named=is_named,
                is_legendary=is_legendary,
            )
            if not progressed:
                import evennia

                evennia.logger.log_err(
                    "Combat progression rejected for "
                    f"{source_id}: {progression_message}"
                )


def _is_personal_drop(item_def):
    """Quest items and default drops are personal; shared drops require intent."""
    if item_def.get("is_quest_item"):
        return True
    return item_def.get("loot_scope", "personal") == "personal"


def _personal_scales(mob):
    value = getattr(mob.db, "personal_scales", 0)
    if not isinstance(value, (int, float)):
        return 0
    return max(0, int(value))


def _mob_reward_key(mob):
    for attr_name in ("mob_type", "mob_template_key"):
        value = getattr(mob.db, attr_name, None)
        if isinstance(value, str) and value:
            return value
    return mob.key


def _is_player(character):
    return bool(getattr(character, "account", None))
