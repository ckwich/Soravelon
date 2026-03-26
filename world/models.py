"""
Django models for Soravelon world-state engine.

These store relational data that describes relationships between entities,
not intrinsic character state. See soravelon-architecture.md Data Architecture
Principles for the rationale.

Records are created lazily — only when first needed. No record = default/neutral.
"""

from django.db import models


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
            # Use UniqueConstraint with condition to handle NULL subfaction_id.
            # unique_together treats NULLs as distinct on PostgreSQL, allowing
            # duplicate top-level faction rows. This constraint uses
            # nulls_distinct=False to prevent that.
            models.UniqueConstraint(
                fields=["character", "faction_id", "subfaction_id"],
                name="unique_faction_standing",
                nulls_distinct=False,
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
    last_practiced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("character", "skill_id")
        indexes = [
            models.Index(fields=["character", "skill_type"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.skill_id}={self.value}"


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

    class Meta:
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
    # NOT unique — a character can have multiple debt records over time
    # (one active, others paid/hunted/forgiven). Application-level check
    # in create_debt() enforces one active debt at a time.
    amount = models.IntegerField()
    deadline_playtime_seconds = models.IntegerField()
    status = models.CharField(max_length=16, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["character_id", "status"]),
        ]

    def __str__(self):
        return f"char={self.character_id}:debt={self.amount}:{self.status}"


class CharacterGuild(models.Model):
    """
    Character guild membership record.

    Source of truth for guild/subclass assignment. character.db.guild_id and
    character.db.subclass_id are fast-read caches updated when this model
    changes (D-15). Lazy creation: no record = Wanderer (no guild). Created
    on join_guild() (D-15).
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
            models.Index(fields=["guild_id"]),
        ]

    def __str__(self):
        return f"{self.character.db_key}:{self.guild_id}/{self.subclass_id}"
