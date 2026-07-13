"""
Django models for Soravelon world-state engine.

These store relational data that describes relationships between entities,
not intrinsic character state. See soravelon-architecture.md Data Architecture
Principles for the rationale.

Records are created lazily — only when first needed. No record = default/neutral.
"""

from django.db import models

from world.economy_ids import new_operation_id


class FactionStanding(models.Model):
    """
    Character ↔ faction relationship.
    Standing scale: -100,000 to +100,000.
    Trust scale: 0-100.
    """

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="faction_standings",
    )
    faction_id = models.CharField(max_length=64, db_index=True)
    subfaction_id = models.CharField(max_length=64, null=True, blank=True)
    standing = models.IntegerField(default=0)
    trust = models.IntegerField(default=50)
    betrayal_flag = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "faction_id"],
                condition=models.Q(subfaction_id__isnull=True),
                name="unique_top_faction_standing",
            ),
            models.UniqueConstraint(
                fields=["character", "faction_id", "subfaction_id"],
                condition=models.Q(subfaction_id__isnull=False),
                name="unique_subfaction_standing",
            ),
        ]
        indexes = [
            models.Index(
                fields=["faction_id", "subfaction_id", "standing"]
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.faction_id}={self.standing}"


class ZoneAttunement(models.Model):
    """
    Character ↔ zone attunement relationship.
    Score: 0-100 per zone.
    """

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="zone_attunements",
    )
    zone_id = models.CharField(max_length=64, db_index=True)
    score = models.FloatField(default=0.0)
    last_visited = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("character", "zone_id")

    def __str__(self):
        return f"{self.character.db_key}:{self.zone_id}={self.score}"


class CharacterSkill(models.Model):
    """
    Character ↔ skill relationship.
    Covers general proficiencies, zone attunement, creature attunement,
    and node attunement tracks. All use 0-100 scale.
    """

    SKILL_TYPES = [
        ("general", "General Proficiency"),
        ("zone_attunement", "Zone Attunement"),
        ("node_attunement", "Node Attunement"),
        ("creature_attunement", "Creature Attunement"),
    ]

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="skills",
    )
    skill_id = models.CharField(max_length=128)
    skill_type = models.CharField(max_length=32, choices=SKILL_TYPES)
    value = models.FloatField(default=0.0)
    passive_use_remainder = models.PositiveIntegerField(default=0)
    last_practiced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("character", "skill_id")
        indexes = [
            models.Index(fields=["character", "skill_type"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.skill_id}={self.value}"


class ProgressionEvent(models.Model):
    """Durable, idempotent authored domain and skill growth event."""

    EVENT_TYPES = (
        ("combat_outcome", "Combat outcome"),
        ("quest_outcome", "Quest outcome"),
        ("practice", "Practice"),
        ("gathering", "Gathering"),
        ("crafting", "Crafting"),
        ("exploration", "Exploration"),
        ("investigation", "Investigation"),
    )

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="progression_events",
    )
    event_id = models.CharField(max_length=160)
    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    source_id = models.CharField(max_length=128)
    domain_awards = models.JSONField(default=dict)
    skill_awards = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "event_id"],
                name="unique_character_progression_event",
            ),
        ]
        indexes = [
            models.Index(
                fields=["character", "applied_at"],
                name="progression_pending_idx",
            ),
            models.Index(
                fields=["event_type", "created_at"],
                name="progression_type_time_idx",
            ),
        ]

    def __str__(self):
        state = "applied" if self.applied_at else "pending"
        return f"{self.character_id}:{self.event_id}:{state}"


class NodeEventLog(models.Model):
    """
    Log of significant node events.
    Used for temporal stamps on lore drops and Scholar research.
    """
    zone_id = models.CharField(max_length=64)
    node_type = models.CharField(max_length=32)
    event_type = models.CharField(max_length=32)
    failure_at_event = models.FloatField()
    occurred_at = models.DateTimeField(auto_now_add=True)
    triggered_by = models.CharField(
        max_length=64, null=True, blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["zone_id", "occurred_at"]),
            models.Index(fields=["node_type", "event_type"]),
        ]

    def __str__(self):
        return f"{self.zone_id}:{self.event_type}@{self.failure_at_event}%"


class InventoryItem(models.Model):
    """
    Metadata for an item in a character's inventory.
    Linked to Evennia object via item_id (dbref integer).
    One record per Evennia item object (unique item_id).
    """
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="inventory_items",
    )
    item_id = models.IntegerField(unique=True)
    quantity = models.IntegerField(default=1)
    container_id = models.IntegerField(null=True, blank=True)
    is_equipped = models.BooleanField(default=False)
    equipment_slot = models.CharField(
        max_length=32, null=True, blank=True
    )
    is_quest_item = models.BooleanField(default=False)
    quest_id = models.CharField(
        max_length=64, null=True, blank=True
    )
    keyring = models.BooleanField(default=False)
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "equipment_slot"],
                condition=models.Q(is_equipped=True),
                name="unique_equipped_slot",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="inventory_quantity_positive",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        is_equipped=False,
                        equipment_slot__isnull=True,
                    )
                    | (
                        models.Q(
                            is_equipped=True,
                            equipment_slot__isnull=False,
                            container_id__isnull=True,
                        )
                        & ~models.Q(equipment_slot="")
                    )
                ),
                name="inventory_equipment_state",
            ),
        ]
        indexes = [
            models.Index(fields=["character_id", "is_equipped"]),
            models.Index(fields=["character_id", "keyring"]),
            models.Index(fields=["character_id", "is_quest_item"]),
        ]

    def __str__(self):
        return f"char={self.character_id}:item={self.item_id}:qty={self.quantity}"


class BankAccount(models.Model):
    character = models.OneToOneField(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="bank_account",
    )
    balance = models.IntegerField(default=0)
    home_hub = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name="bank_balance_nonnegative",
            ),
        ]

    def __str__(self):
        return f"char={self.character_id}:balance={self.balance}"


class BankTransaction(models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="bank_transactions",
    )
    transaction_type = models.CharField(max_length=32)
    amount = models.IntegerField()
    balance_after = models.IntegerField()
    description = models.CharField(max_length=256, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)
    related_id = models.CharField(max_length=64, null=True, blank=True)
    operation_id = models.CharField(
        max_length=128,
        unique=True,
        default=new_operation_id,
        editable=False,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(amount=0),
                name="bank_tx_amount_nonzero",
            ),
            models.CheckConstraint(
                condition=models.Q(balance_after__gte=0),
                name="bank_tx_balance_nonnegative",
            ),
        ]
        indexes = [
            models.Index(fields=["character_id", "occurred_at"]),
            models.Index(fields=["character_id", "transaction_type"]),
        ]

    def __str__(self):
        return f"char={self.character_id}:{self.transaction_type}:{self.amount}"


class RecurringPayment(models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="recurring_payments",
    )
    payment_type = models.CharField(max_length=32)
    amount = models.IntegerField()
    interval_days = models.IntegerField(default=7)
    next_due = models.DateTimeField()
    active = models.BooleanField(default=True)
    grace_until = models.DateTimeField(null=True, blank=True)
    lapsed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "payment_type"],
                name="unique_recurring_payment",
            ),
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="recurring_amount_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(interval_days__gt=0),
                name="recurring_interval_positive",
            ),
        ]
        indexes = [
            models.Index(fields=["character_id", "payment_type"]),
            models.Index(fields=["next_due", "active"]),
        ]

    def __str__(self):
        return f"char={self.character_id}:{self.payment_type}:{self.amount}"


class DebtRecord(models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="debt_records",
    )
    # A character may retain historical resolved debts, but the conditional
    # database constraint below permits only one active record.
    amount = models.IntegerField()
    deadline_playtime_seconds = models.IntegerField()
    status = models.CharField(max_length=16, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character"],
                condition=models.Q(status="active"),
                name="unique_active_debt",
            ),
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="debt_amount_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(deadline_playtime_seconds__gte=0),
                name="debt_deadline_nonnegative",
            ),
        ]
        indexes = [
            models.Index(fields=["character_id", "status"]),
        ]

    def __str__(self):
        return f"char={self.character_id}:debt={self.amount}:{self.status}"


class BankDraft(models.Model):
    """Durable identity and lifecycle state for a Consortium bank draft."""

    STATUS_CHOICES = [
        ("issued", "Issued"),
        ("redeemed", "Redeemed"),
        ("void", "Void"),
    ]

    draft_key = models.CharField(max_length=160, unique=True)
    issuer_character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_bank_drafts",
    )
    issuer_character_ref = models.BigIntegerField()
    denomination = models.IntegerField()
    item_id = models.BigIntegerField(unique=True)
    operation_id = models.CharField(
        max_length=128,
        unique=True,
        default=new_operation_id,
        editable=False,
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="issued",
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_operation_id = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
    )
    redeemed_by = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="redeemed_bank_drafts",
    )
    redeemer_character_ref = models.BigIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(denomination__gt=0),
                name="bank_draft_amount_positive",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        status="issued",
                        resolved_at__isnull=True,
                        resolution_operation_id__isnull=True,
                        redeemer_character_ref__isnull=True,
                    )
                    | models.Q(
                        status="redeemed",
                        resolved_at__isnull=False,
                        resolution_operation_id__isnull=False,
                        redeemer_character_ref__isnull=False,
                    )
                    | models.Q(
                        status="void",
                        resolved_at__isnull=False,
                        resolution_operation_id__isnull=False,
                        redeemer_character_ref__isnull=True,
                    )
                ),
                name="bank_draft_state_coherent",
            ),
            models.CheckConstraint(
                condition=(
                    (
                        models.Q(issuer_character__isnull=True)
                        | models.Q(
                            issuer_character_id=models.F("issuer_character_ref")
                        )
                    )
                    & (
                        models.Q(redeemed_by__isnull=True)
                        | models.Q(
                            redeemed_by_id=models.F("redeemer_character_ref")
                        )
                    )
                ),
                name="bank_draft_actor_refs_match",
            ),
        ]
        indexes = [
            models.Index(
                fields=["issuer_character", "status"],
                name="world_draft_issuer_status_idx",
            ),
            models.Index(
                fields=["status", "issued_at"],
                name="world_draft_status_issued_idx",
            ),
        ]

    def __str__(self):
        return f"{self.draft_key}:{self.denomination}:{self.status}"


class GameOperation(models.Model):
    """Exactly-once receipt for cross-system player state mutations."""

    operation_id = models.CharField(
        max_length=128,
        unique=True,
        default=new_operation_id,
        editable=False,
    )
    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="game_operations",
    )
    character_ref = models.BigIntegerField()
    operation_type = models.CharField(max_length=48)
    related_id = models.CharField(max_length=160)
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(character__isnull=True)
                    | models.Q(character_id=models.F("character_ref"))
                ),
                name="game_operation_actor_ref_matches",
            ),
        ]
        indexes = [
            models.Index(
                fields=["character", "operation_type"],
                name="world_gameop_actor_type_idx",
            ),
            models.Index(
                fields=["operation_type", "related_id"],
                name="world_gameop_type_related_idx",
            ),
        ]

    def __str__(self):
        return f"{self.operation_type}:{self.operation_id}"


class EncounterReward(models.Model):
    """One durable, independently claimable personal reward per encounter."""

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="encounter_rewards",
    )
    corpse_id = models.BigIntegerField(db_index=True)
    source_mob_key = models.CharField(max_length=128)
    item_definitions = models.JSONField(default=list)
    scales = models.IntegerField(default=0)
    granted_at = models.DateTimeField(auto_now_add=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "corpse_id"],
                name="unique_personal_encounter_reward",
            ),
            models.CheckConstraint(
                condition=models.Q(scales__gte=0),
                name="encounter_reward_scales_nonnegative",
            ),
        ]
        indexes = [
            models.Index(
                fields=["character", "claimed_at"],
                name="world_reward_claim_idx",
            ),
        ]

    def __str__(self):
        return f"char={self.character_id}:corpse={self.corpse_id}"


class CharacterGuild(models.Model):
    """
    Character guild membership record.

    Source of truth for guild/subclass assignment. character.db.guild_id and
    character.db.subclass_id are fast-read caches updated when this model
    changes (D-15). Lazy creation: no record = Wanderer (no guild). Created
    only when an authored recruitment induction completes.
    """

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
            models.Index(
                fields=["guild_id"],
                name="world_charac_guild_i_idx",
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.guild_id}/{self.subclass_id}"


class GuildRecruitment(models.Model):
    """Durable invitation and completed induction provenance."""

    STATUS_CHOICES = (
        ("offered", "Offered"),
        ("completed", "Completed"),
    )

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="guild_recruitments",
    )
    guild_id = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="offered")
    contact_npc_id = models.CharField(max_length=128)
    location_zone_id = models.CharField(max_length=64)
    location_room_id = models.CharField(max_length=128)
    secondary_domain = models.CharField(max_length=32, blank=True, default="")
    offered_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "guild_id"],
                name="unique_character_guild_recruitment",
            ),
        ]
        indexes = [
            models.Index(
                fields=["character", "status"],
                name="guild_recruitment_status_idx",
            ),
        ]

    def __str__(self):
        return f"{self.character_id}:{self.guild_id}:{self.status}"


class CharacterAbility(models.Model):
    """
    Tracks which abilities a character has unlocked.

    Source of truth for ability access. Created when player claims an ability
    at guild hall (D-19). Queried by ability engine for access checks.
    """

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
            models.Index(
                fields=["character_id", "ability_id"],
                name="world_charac_charact_idx",
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.ability_id}"


class CharacterQuest(models.Model):
    """
    Tracks a character's progress on a specific quest.

    Per D-01: character FK, quest_id (str), status, progress (JSONField dict),
    started_at, completed_at.
    Per D-04: Three terminal states: complete, failed, abandoned. Active = in-progress.
    Progress uses a dict keyed by objective key (e.g. {"kill_ash_wolf": 4, "collect_fang": 2})
    so multi-objective quests track each objective independently.
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
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default="active"
    )
    progress = models.JSONField(default=dict)
    accepted_spec = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    outcome_operation_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )
    outcome_result = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(
                fields=["character", "status"],
                name="world_cq_char_status_idx",
            ),
            models.Index(
                fields=["character", "quest_id"],
                name="world_cq_char_quest_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        status="complete",
                        completed_at__isnull=False,
                        outcome_operation_id__isnull=False,
                    )
                    | models.Q(
                        ~models.Q(status="complete"),
                        completed_at__isnull=True,
                        outcome_operation_id__isnull=True,
                    )
                ),
                name="character_quest_completion_consistent",
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.quest_id}={self.status}"


class QuestShareOffer(models.Model):
    """A player-consented offer of one frozen quest run to one ally."""

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("expired", "Expired"),
    )

    source_quest = models.ForeignKey(
        CharacterQuest,
        on_delete=models.CASCADE,
        related_name="share_offers",
    )
    accepted_quest = models.OneToOneField(
        CharacterQuest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_share_offer",
    )
    sender = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="sent_quest_share_offers",
    )
    recipient = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="received_quest_share_offers",
    )
    quest_id = models.CharField(max_length=128, db_index=True)
    quest_spec = models.JSONField(default=dict)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_quest", "recipient"],
                name="unique_quest_share_recipient",
            ),
            models.CheckConstraint(
                condition=~models.Q(sender=models.F("recipient")),
                name="quest_share_sender_not_recipient",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        status="pending",
                        responded_at__isnull=True,
                        accepted_quest__isnull=True,
                    )
                    | models.Q(
                        status="accepted",
                        responded_at__isnull=False,
                        accepted_quest__isnull=False,
                    )
                    | models.Q(
                        status__in=("declined", "expired"),
                        responded_at__isnull=False,
                        accepted_quest__isnull=True,
                    )
                ),
                name="quest_share_response_consistent",
            ),
        ]
        indexes = [
            models.Index(
                fields=["recipient", "status"],
                name="quest_share_recipient_idx",
            ),
            models.Index(
                fields=["source_quest", "status"],
                name="quest_share_source_idx",
            ),
        ]

    def __str__(self):
        return f"{self.sender_id}->{self.recipient_id}:{self.quest_id}:{self.status}"


class CharacterAccessGrant(models.Model):
    """A durable, named permission earned through an authored game outcome."""

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="access_grants",
    )
    grant_key = models.CharField(max_length=128)
    source_quest_id = models.CharField(max_length=128, blank=True, default="")
    metadata = models.JSONField(default=dict)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["character", "grant_key"],
                name="character_access_grant_unique",
            ),
        ]
        indexes = [
            models.Index(
                fields=["grant_key"],
                name="world_access_grant_key_idx",
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.grant_key}"


class KnownTopicRecord(models.Model):
    """
    Tracks which dialogue topics a character has learned from each NPC.

    Used by the hint system to suppress already-known topics and re-surface
    them when context changes (via context_hash comparison). Lazy creation:
    no record = topic not yet learned from this NPC.
    """

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="known_topics",
    )
    npc_id = models.CharField(max_length=128)
    topic_key = models.CharField(max_length=128)
    context_hash = models.CharField(max_length=64, blank=True, default="")
    learned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("character", "npc_id", "topic_key")
        indexes = [
            models.Index(
                fields=["character", "npc_id"],
                name="world_known_charact_424052_idx",
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.npc_id}/{self.topic_key}"


class WorldEventLog(models.Model):
    """
    Log of significant world events.
    Consumed by the LLM quest generation system and world-state queries.
    """

    event_type = models.CharField(max_length=64, db_index=True)
    zone_id = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    faction_id = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    character_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    data = models.JSONField(default=dict)
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["event_type", "occurred_at"]),
            models.Index(fields=["zone_id", "occurred_at"]),
            models.Index(fields=["faction_id", "occurred_at"]),
        ]

    def __str__(self):
        return f"{self.event_type}:{self.zone_id}@{self.occurred_at}"


class SocialNode(models.Model):
    """A node in Soravelon's runtime social knowledge graph."""

    node_key = models.CharField(max_length=192, unique=True)
    node_type = models.CharField(max_length=32, db_index=True)
    display_name = models.CharField(max_length=160, blank=True, default="")
    zone_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    settlement_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    faction_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["node_type", "zone_id"]),
            models.Index(fields=["node_type", "settlement_id"]),
        ]

    def __str__(self):
        return self.node_key


class SocialEdge(models.Model):
    """A contact path that can carry social facts or claims between nodes."""

    DIRECTION_CHOICES = [
        ("one_way", "One Way"),
        ("two_way", "Two Way"),
        ("broadcast", "Broadcast"),
        ("gatekept", "Gatekept"),
    ]

    edge_key = models.CharField(max_length=240, unique=True)
    source_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="outgoing_social_edges",
    )
    target_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="incoming_social_edges",
    )
    edge_type = models.CharField(max_length=64, db_index=True)
    directionality = models.CharField(
        max_length=16,
        choices=DIRECTION_CHOICES,
        default="one_way",
    )
    trust = models.FloatField(default=0.5)
    latency_seconds = models.PositiveIntegerField(default=0)
    bandwidth = models.PositiveIntegerField(default=3)
    secrecy = models.CharField(max_length=32, blank=True, default="")
    distortion = models.CharField(max_length=32, blank=True, default="")
    scope_tags = models.JSONField(default=list)
    blockers = models.JSONField(default=list)
    required_tags = models.JSONField(default=list)
    blocked_tags = models.JSONField(default=list)
    active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(trust__gte=0.0, trust__lte=1.0),
                name="social_edge_trust_probability",
            ),
        ]
        indexes = [
            models.Index(fields=["source_node", "active"]),
            models.Index(fields=["target_node", "active"]),
            models.Index(fields=["edge_type", "active"]),
        ]

    def __str__(self):
        return self.edge_key


class SocialFact(models.Model):
    """Authoritative social truth recorded by game systems."""

    VISIBILITY_CHOICES = [
        ("private", "Private"),
        ("witnessed", "Witnessed"),
        ("local", "Local"),
        ("institutional", "Institutional"),
        ("route", "Route"),
        ("global", "Global"),
    ]

    fact_key = models.CharField(max_length=192, unique=True)
    subject_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="subject_social_facts",
    )
    actor_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actor_social_facts",
    )
    scope_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scoped_social_facts",
    )
    event_type = models.CharField(max_length=64, db_index=True)
    summary = models.TextField()
    tags = models.JSONField(default=list)
    visibility = models.CharField(
        max_length=16,
        choices=VISIBILITY_CHOICES,
        default="local",
        db_index=True,
    )
    evidence = models.JSONField(default=dict)
    weight = models.FloatField(default=1.0)
    confidence = models.FloatField(default=1.0)
    occurred_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(confidence__gte=0.0, confidence__lte=1.0),
                name="social_fact_confidence_probability",
            ),
        ]
        indexes = [
            models.Index(fields=["subject_node", "visibility"]),
            models.Index(fields=["event_type", "created_at"]),
        ]

    def __str__(self):
        return self.fact_key


class SocialClaim(models.Model):
    """A social assertion made by a node about a fact or subject."""

    STATUS_CHOICES = [
        ("supported", "Supported"),
        ("rumor", "Rumor"),
        ("contested", "Contested"),
        ("false", "False"),
        ("unknown", "Unknown"),
    ]

    claim_key = models.CharField(max_length=224, unique=True)
    fact = models.ForeignKey(
        SocialFact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claims",
    )
    speaker_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="spoken_social_claims",
    )
    subject_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="subject_social_claims",
    )
    claim_type = models.CharField(max_length=64, db_index=True)
    summary = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="rumor")
    intent = models.CharField(max_length=64, blank=True, default="")
    bias_tags = models.JSONField(default=list)
    confidence = models.FloatField(default=0.5)
    visibility = models.CharField(
        max_length=16,
        choices=SocialFact.VISIBILITY_CHOICES,
        default="local",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(confidence__gte=0.0, confidence__lte=1.0),
                name="social_claim_confidence_probability",
            ),
        ]
        indexes = [
            models.Index(fields=["speaker_node", "claim_type"]),
            models.Index(fields=["subject_node", "status"]),
        ]

    def __str__(self):
        return self.claim_key


class SocialKnowledge(models.Model):
    """A record that a node knows or believes a fact or claim."""

    knowledge_key = models.CharField(max_length=260, unique=True)
    node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="social_knowledge",
    )
    fact = models.ForeignKey(
        SocialFact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="known_by",
    )
    claim = models.ForeignKey(
        SocialClaim,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="known_by",
    )
    source_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sourced_social_knowledge",
    )
    edge = models.ForeignKey(
        SocialEdge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carried_social_knowledge",
    )
    channel = models.CharField(max_length=64, db_index=True)
    confidence = models.FloatField(default=0.5)
    spreading = models.BooleanField(default=False, db_index=True)
    learned_at = models.DateTimeField(auto_now_add=True, db_index=True)
    available_after = models.DateTimeField(null=True, blank=True, db_index=True)
    last_dispatched_at = models.DateTimeField(null=True, blank=True, db_index=True)
    evidence = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(fact__isnull=False, claim__isnull=True)
                    | models.Q(fact__isnull=True, claim__isnull=False)
                ),
                name="social_knowledge_exactly_one_payload",
            ),
            models.CheckConstraint(
                condition=models.Q(confidence__gte=0.0, confidence__lte=1.0),
                name="social_knowledge_confidence_probability",
            ),
        ]
        indexes = [
            models.Index(fields=["node", "channel"]),
            models.Index(fields=["node", "spreading"]),
        ]

    def __str__(self):
        return self.knowledge_key


class SocialTrace(models.Model):
    """Audit trail explaining how social knowledge reached a node."""

    trace_key = models.CharField(max_length=280, unique=True)
    route_key = models.CharField(max_length=72, unique=True)
    knowledge = models.ForeignKey(
        SocialKnowledge,
        on_delete=models.CASCADE,
        related_name="traces",
    )
    from_node = models.ForeignKey(
        SocialNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="outgoing_social_traces",
    )
    to_node = models.ForeignKey(
        SocialNode,
        on_delete=models.CASCADE,
        related_name="incoming_social_traces",
    )
    edge = models.ForeignKey(
        SocialEdge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="social_traces",
    )
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(route_key__gt=""),
                name="social_trace_route_key_nonempty",
            ),
        ]
        indexes = [
            models.Index(fields=["to_node", "created_at"]),
        ]

    def __str__(self):
        return self.trace_key


class SocialTopologyBinding(models.Model):
    """Records which AreaBuilder zone owns an authored Social Web object."""

    KIND_CHOICES = [
        ("node", "Node"),
        ("edge", "Edge"),
    ]

    zone_id = models.CharField(max_length=64, db_index=True)
    kind = models.CharField(max_length=8, choices=KIND_CHOICES)
    object_key = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["zone_id", "kind", "object_key"],
                name="social_topology_binding_unique_owner",
            ),
        ]
        indexes = [
            models.Index(
                fields=["zone_id", "kind"],
                name="world_soc_zone_id_5d8f0e_idx",
            ),
            models.Index(
                fields=["kind", "object_key"],
                name="world_soc_kind_2bcf89_idx",
            ),
        ]

    def __str__(self):
        return f"{self.zone_id}:{self.kind}:{self.object_key}"


class SpawnRecord(models.Model):
    """
    Tracks active and respawning mobs per room spawn slot.
    One record per (room_id, spawn_index) pair.
    """

    room_id = models.IntegerField(db_index=True)
    spawn_index = models.IntegerField()
    mob_template_key = models.CharField(max_length=64)
    active_mob_ids = models.JSONField(default=list)
    respawn_at = models.DateTimeField(null=True, db_index=True)
    is_named = models.BooleanField(default=False)
    named_id = models.CharField(max_length=128, blank=True, default="")

    class Meta:
        unique_together = ("room_id", "spawn_index")
        indexes = [
            models.Index(
                fields=["respawn_at"],
                name="world_spawn_respawn_idx",
            ),
            models.Index(
                fields=["is_named"],
                name="world_spawn_is_named_idx",
            ),
        ]

    def __str__(self):
        return f"room={self.room_id}:idx={self.spawn_index}:{self.mob_template_key}"


class CharacterRecipe(models.Model):
    """
    Tracks which crafting recipes a character has learned.

    Recipes can be learned from trainer NPCs, recipe items, or granted by
    default. Lazy creation: no record = recipe not known.
    """

    character = models.ForeignKey(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="known_recipes",
    )
    recipe_id = models.CharField(max_length=128)
    learned_from = models.CharField(max_length=64, blank=True, default="")
    learned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("character", "recipe_id")
        indexes = [
            models.Index(
                fields=["character_id", "recipe_id"],
                name="world_chara_charact_cbd173_idx",
            ),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.recipe_id}"


class WorldContentRevision(models.Model):
    """Durable evidence for one reviewed immutable world-content manifest."""

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("applying", "Applying"),
        ("applied", "Applied"),
        ("superseded", "Superseded"),
        ("failed", "Failed"),
        ("rolled_back", "Rolled Back"),
    ]

    manifest_hash = models.CharField(max_length=64, db_index=True)
    schema_version = models.CharField(max_length=64)
    manifest = models.JSONField()
    plan = models.JSONField(default=dict)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="planned",
        db_index=True,
    )
    previous_revision = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="next_revisions",
    )
    git_commit = models.CharField(max_length=64)
    maintenance_approved = models.BooleanField(default=False)
    error = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["status"],
                condition=models.Q(status="applied"),
                name="world_content_single_applied_revision",
            ),
            models.CheckConstraint(
                condition=models.Q(manifest_hash__regex=r"^[0-9a-f]{64}$"),
                name="world_content_manifest_hash_hex",
            ),
        ]
        indexes = [
            models.Index(
                fields=["status", "-created_at"],
                name="world_content_status_idx",
            ),
        ]

    def __str__(self):
        return f"{self.manifest_hash[:12]}:{self.status}"


class WorldContentDeploymentLock(models.Model):
    """Singleton row used as the cross-process content deployment mutex."""

    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "world-content-deployment-lock"
