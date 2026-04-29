"""Central visibility rules for current-era Remnance content.

Remnance and the Vaelborn are implemented as internal future-event data, but
they must remain non-player-facing until a later story event explicitly opens
that layer of the world.
"""

HIDDEN_CURRENT_ERA_DOMAINS = {"remnance"}
HIDDEN_CURRENT_ERA_GUILDS = {"vaelborn"}
HIDDEN_CURRENT_ERA_RESOURCES = {"echoes"}


def is_remnance_player_visible(character=None):
    """
    Return whether this character may see Remnance-facing content.

    The old ``remnance_discovered`` flag is intentionally ignored here. The
    future unlock should be a deliberate world-event flag, not a lore breadcrumb.
    """
    if not character:
        return False

    db = getattr(character, "db", character)
    return bool(getattr(db, "remnance_player_visible", False))


def domain_is_player_visible(domain, character=None):
    """Return whether a domain may be named to the player."""
    normalized = str(domain or "").lower()
    if normalized not in HIDDEN_CURRENT_ERA_DOMAINS:
        return True
    return is_remnance_player_visible(character)


def guild_is_player_visible(guild_id=None, guild=None, character=None):
    """Return whether a guild may be named to the player."""
    normalized = str(guild_id or "").lower()
    if normalized in HIDDEN_CURRENT_ERA_GUILDS:
        return is_remnance_player_visible(character)

    guild = guild or {}
    if guild.get("hidden"):
        return is_remnance_player_visible(character)
    primary = guild.get("primary_domain")
    return domain_is_player_visible(primary, character)


def ability_is_player_visible(ability, character=None):
    """Return whether dynamic ability help/status may display an ability."""
    if not ability:
        return False
    if is_remnance_player_visible(character):
        return True

    domain_fields = (
        ability.get("domain"),
        ability.get("scaling_primary"),
        ability.get("scaling_secondary"),
    )
    if any(
        str(domain or "").lower() in HIDDEN_CURRENT_ERA_DOMAINS
        for domain in domain_fields
    ):
        return False

    resource = str(ability.get("resource_type") or "").lower()
    return resource not in HIDDEN_CURRENT_ERA_RESOURCES


def public_domain_label(domain):
    """Render a domain label without leaking future-event terminology."""
    if domain_is_player_visible(domain):
        return str(domain).title()
    return "Exploration"
