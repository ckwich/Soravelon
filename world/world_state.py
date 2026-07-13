"""
Soravelon World-State Engine.

Five dimensions: Reputation, Attunement, Network, Bond, Legacy.
Aggregate scores stored as db_strvalue on character (fast read).
Session history accumulated in ndb, batch-committed at breakpoints.

Backend level derived from domain scores — NEVER exposed to players.
"""

from django.db.models import Avg

from world.domain_definitions import ALL_DOMAINS
from world.models import FactionStanding, ZoneAttunement

# --- Constants ---

ALL_DIMENSIONS = ("reputation", "network", "bond", "legacy", "attunement")

# Decay rates per 24h tick (offline only). Legacy never decays.
DECAY_RATES = {
    "reputation": 0.5,
    "network": 1.0,
    "bond": 0.2,
    "legacy": 0.0,
    "attunement": 0.0,  # handled per-zone, not aggregate
}

# Domain XP conversion rate: raw XP accumulated → score points gained.
# Diminishing returns are applied separately.
XP_CONVERSION_RATE = 0.1  # 10 authored raw XP = 1.0 score point at full rate

# Diminishing returns brackets for domain XP gain
DIMINISHING_BRACKETS = [
    (0, 25, 1.0),     # score 0-25: full rate
    (25, 50, 0.75),   # score 25-50: 75%
    (50, 75, 0.40),   # score 50-75: 40%
    (75, 90, 0.10),   # score 75-90: 10%
    (90, 100, 0.02),  # score 90-100: 2%
]


def _as_typeclass(obj):
    """Return the live typeclass for ObjectDB rows and already-wrapped objects."""
    return getattr(obj, "typeclass", obj)


# --- Dimension Score Management ---

def set_dimension_score(character, dimension, value):
    """Set a dimension aggregate score, clamped to 0-100."""
    clamped = max(0.0, min(100.0, float(value)))
    setattr(character.db, f"{dimension}_score", clamped)


def get_dimension_score(character, dimension):
    """Read a dimension aggregate score."""
    return float(getattr(character.db, f"{dimension}_score", 0.0) or 0.0)


# --- Decay ---

def apply_decay(character):
    """
    Apply dimension decay to a single character.
    Called per-character during the global decay tick.
    Legacy never decays. Attunement decay is per-zone (not here).
    """
    for dim, rate in DECAY_RATES.items():
        if rate <= 0.0:
            continue
        current = get_dimension_score(character, dim)
        if current > 0.0:
            new_val = max(0.0, current - rate)
            set_dimension_score(character, dim, new_val)


def decay_tick_all():
    """
    Global decay tick — called by TickerHandler every 24 real hours.
    Only applies to OFFLINE characters. Online characters are skipped.
    """
    from evennia.objects.models import ObjectDB

    # Get all character objects (tagged as player_character)
    characters = ObjectDB.objects.filter(
        db_tags__db_key="player_character",
        db_tags__db_category="character_type",
    )
    for char_db in characters:
        char = _as_typeclass(char_db)
        if char.is_connected:
            continue  # skip online characters
        apply_decay(char)


# --- Attunement Dual Representation ---

def update_zone_attunement(character, zone_id, delta):
    """Add delta to a per-zone attunement score, clamped to 0-100."""
    from django.utils import timezone

    record, _ = ZoneAttunement.objects.get_or_create(
        character=character,
        zone_id=zone_id,
        defaults={"score": 0.0},
    )
    new_score = max(0.0, min(100.0, record.score + float(delta)))
    record.score = new_score
    record.last_visited = timezone.now()
    record.save()


def recalculate_attunement_aggregate(character):
    """
    Recalculate character.db.attunement_score from all zone attunement records.
    Uses average of all zone scores, weighted toward higher values.
    """
    records = ZoneAttunement.objects.filter(character=character)
    if not records.exists():
        set_dimension_score(character, "attunement", 0.0)
        return

    result = records.aggregate(avg=Avg("score"))
    avg_score = result["avg"] or 0.0
    set_dimension_score(character, "attunement", avg_score)


# --- Domain XP & Batch Commit ---

def init_session_accumulators(character):
    """Initialize ndb session accumulators for all domains. Call on login."""
    for domain in ALL_DOMAINS:
        setattr(character.ndb, f"domain_xp_{domain}", 0)



def accumulate_domain_xp(character, domain, raw_xp):
    """Add raw XP to a domain's session accumulator (ndb, not persisted)."""
    key = f"domain_xp_{domain}"
    current = getattr(character.ndb, key, 0) or 0
    setattr(character.ndb, key, current + raw_xp)


def _get_diminishing_rate(current_score):
    """Return the XP gain rate multiplier for the given domain score."""
    for low, high, rate in DIMINISHING_BRACKETS:
        if low <= current_score < high:
            return rate
    # Score at 100 — effectively no gain
    return 0.0


def commit_session_xp(character):
    """
    Batch commit all accumulated domain XP from ndb to DB.
    Called at session end, deliberate practice, login recovery, safety flush.
    """
    volatile_awards = {
        domain: getattr(character.ndb, f"domain_xp_{domain}", 0) or 0
        for domain in ALL_DOMAINS
    }

    def _apply_awards(durable_domain_awards, durable_skill_awards):
        # Copy to plain dict to avoid SaverDict N+1 repickle.
        scores = dict(character.db.domain_scores or {})
        for domain in ALL_DOMAINS:
            accumulated = volatile_awards[domain] + durable_domain_awards.get(domain, 0)
            if accumulated <= 0:
                continue

            current = scores.get(domain, 0.0)
            rate = _get_diminishing_rate(current)
            gain = accumulated * XP_CONVERSION_RATE * rate
            scores[domain] = min(100.0, current + gain)

        # This attribute write and durable event acknowledgement share one DB
        # transaction. A failure leaves every event pending for safe recovery.
        character.db.domain_scores = scores

        from world.skill_engine import apply_skill_use_counts

        apply_skill_use_counts(character, durable_skill_awards)

    from world.atomic_state import atomic_evennia_state
    from world.progression_engine import apply_pending_progression_events

    # Django rolls the Attribute row back, but Evennia's idmapper can retain
    # the attempted value. Track it so a failed mixed domain/skill apply is
    # safe to retry on this same live typeclass instance.
    with atomic_evennia_state(character) as cache_tracker:
        cache_tracker.track(character, attributes=("domain_scores",))
        apply_pending_progression_events(character, _apply_awards)

    # Volatile awards clear only after the durable transaction succeeds.
    for domain in ALL_DOMAINS:
        setattr(character.ndb, f"domain_xp_{domain}", 0)

    # Recalculate backend level
    character.db.backend_level = calculate_backend_level(character)

    # Recalculate attunement aggregate
    recalculate_attunement_aggregate(character)

    # Ability unlocks track ancestry + guild tier progression and should update
    # as soon as domain scores commit.
    from world.ability_engine import sync_character_ability_unlocks
    sync_character_ability_unlocks(character)

    # OOB: notify client of updated scores after XP commit (CLI-06)
    from world import oob_publisher
    oob_publisher.push_status_update(character)

    # Guild discovery check (D-17)
    try:
        _check_guild_discovery(character)
    except Exception:
        import evennia
        evennia.logger.log_trace("Guild discovery check failed (non-fatal)")


def _check_guild_discovery(character):
    """
    Persist and announce newly earned guild recruitment.

    Called from commit_session_xp. Repeated commits are silent because the
    durable recruitment row is the delivery authority.
    """
    if character.db.guild_id:
        return
    from world.guild_engine import GUILDS, ensure_guild_recruitments

    new_recruitments = ensure_guild_recruitments(character)
    if not new_recruitments:
        return
    for recruitment in new_recruitments:
        guild = GUILDS.get(recruitment.guild_id, {})
        guild_name = guild.get("name", recruitment.guild_id)
        character.msg(
            f"|y[A messenger brings a sealed letter from {guild_name}. "
            "It names a guild contact in Vael's Crossing; type "
            "|wjoinguild|y to review the invitation.]|n"
        )


# --- Backend Level (INTERNAL ONLY — never expose to player) ---

def calculate_backend_level(character):
    """
    Derive backend level 1-50 from weighted domain scores.
    This number is NEVER shown to the player.
    """
    scores = character.db.domain_scores or {}
    primary_domain = character.db.primary_domain
    secondary_domain = character.db.secondary_domain

    primary = scores.get(primary_domain, 0.0) if primary_domain else 0.0
    secondary = scores.get(secondary_domain, 0.0) if secondary_domain else 0.0

    others = [
        v
        for k, v in scores.items()
        if k not in (primary_domain, secondary_domain)
    ]

    weighted = (primary * 2.0) + (secondary * 1.5) + (sum(others) * 0.5)
    # Max possible: 200 + 150 + 400 = 750
    # Map 0-750 → levels 1-50
    return max(1, min(50, int(weighted / 15) + 1))


# --- Faction Standing ---

def modify_standing(character, faction_id, amount, reason, _transfer=False):
    """
    Modify Standing for a character with a faction.
    Clamps to -100,000 / +100,000. Uses F() for atomic update.
    """
    from django.db.models import F
    from django.db.models.functions import Greatest, Least

    record, _ = FactionStanding.objects.get_or_create(
        character=character,
        faction_id=faction_id,
        subfaction_id=None,
        defaults={"standing": 0, "trust": 50},
    )
    # Atomic update with clamping via Greatest/Least
    FactionStanding.objects.filter(id=record.id).update(
        standing=Greatest(-100000, Least(100000, F('standing') + amount))
    )
    record.refresh_from_db()


def get_standing(character, faction_id):
    """Get Standing value for a character with a faction. 0 if no record."""
    try:
        record = character.faction_standings.get(
            faction_id=faction_id, subfaction_id=None
        )
        return record.standing
    except FactionStanding.DoesNotExist:
        return 0


def get_trust(character, faction_id):
    """Get Trust value for a character with a faction. 50 if no record."""
    try:
        record = character.faction_standings.get(
            faction_id=faction_id, subfaction_id=None
        )
        return record.trust
    except FactionStanding.DoesNotExist:
        return 50


def get_betrayal(character, faction_id):
    """Get betrayal flag for a character with a faction. False if no record."""
    try:
        record = character.faction_standings.get(
            faction_id=faction_id, subfaction_id=None
        )
        return record.betrayal_flag
    except FactionStanding.DoesNotExist:
        return False


def get_zone_attunement(character, zone):
    """Get zone attunement score for a character. 0 if no record."""
    if zone is None:
        return 0.0
    zone_id = zone.db.zone_id if hasattr(zone, "db") else str(zone)
    try:
        record = character.zone_attunements.get(zone_id=zone_id)
        return record.score
    except ZoneAttunement.DoesNotExist:
        return 0.0


# --- Context Packet (NPC template / future LLM interface) ---

def get_character_context_packet(character, npc=None, zone=None):
    """
    Build the context dict consumed by the NPC template system.
    Same packet will later feed LLM — do not break this interface.
    """
    npc_faction = npc.db.faction if npc and hasattr(npc, "db") else None

    return {
        # Character identity
        "ancestry": character.db.ancestry,
        "primary_domain": character.db.primary_domain,
        "secondary_domain": character.db.secondary_domain,
        "guild": character.db.guild_id,
        "subclass": character.db.subclass_id,
        "backend_level": character.db.backend_level,  # internal use only

        # World-state dimensions (0-100 aggregates)
        "reputation": float(character.db.reputation_score or 0),
        "network": float(character.db.network_score or 0),
        "bond": float(character.db.bond_score or 0),
        "legacy": float(character.db.legacy_score or 0),
        "attunement": float(character.db.attunement_score or 0),

        # Faction-specific (populated if npc provided)
        "standing": get_standing(character, npc_faction) if npc_faction else None,
        "trust": get_trust(character, npc_faction) if npc_faction else None,
        "betrayal_flag": (
            get_betrayal(character, npc_faction) if npc_faction else None
        ),

        # Zone-specific
        "zone_attunement": (
            get_zone_attunement(character, zone) if zone else None
        ),

        # Companion
        "companion_present": bool(character.db.companion_id),
        "companion_type": character.db.companion_type,
        "companion_tier": character.db.companion_tier,

        # World event summary — populated when LLM quest system is built.
        # NPC template system ignores None fields.
        "world_event_summary": None,
    }


# --- World Event Logging ---

def log_world_event(event_type, description, zone_id=None,
                    faction_id=None, character_id=None, data=None):
    """
    Record a significant world event.
    Call this from any system that produces world-state changes:
    - Named mob kills
    - Faction Standing threshold crossings
    - Node activation/stabilization
    - Quest consequence world expressions
    - Legacy dimension entries

    Safe to call now — populates WorldEventLog immediately.
    LLM reads these events when quest generation is built.
    """
    from world.models import WorldEventLog
    WorldEventLog.objects.create(
        event_type=event_type,
        description=description,
        zone_id=zone_id or "",
        faction_id=faction_id or "",
        character_id=character_id,
        data=data or {},
    )


# --- TickerHandler callbacks ---

def world_state_decay_tick(*args, **kwargs):
    """TickerHandler callback for 24h decay tick."""
    decay_tick_all()


def session_xp_safety_flush(*args, **kwargs):
    """
    TickerHandler callback for 10-minute safety flush.
    Commits accumulated XP for all online characters.
    """
    from evennia.objects.models import ObjectDB

    characters = ObjectDB.objects.filter(
        db_tags__db_key="player_character",
        db_tags__db_category="character_type",
    )
    for char_db in characters:
        char = _as_typeclass(char_db)
        if char.is_connected:
            commit_session_xp(char)
            # Flush ALL accumulators consistently (F6 fix)
            from world.skill_engine import commit_skill_accumulators
            commit_skill_accumulators(char)
            from world.base_attributes import commit_stat_growth
            commit_stat_growth(char)
