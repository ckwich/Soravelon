"""
Wandering mob system -- mobs with db.wander=True periodically move
to a random connected room within their zone.

Called by a global ticker (registered in at_server_startstop.py).
Each tick, each wandering mob has a chance to move.

Key functions:
    wander_mob(mob)   - Move a single mob to a random valid exit
    wander_tick()     - Batch tick: find all wanderers, roll chance, move

Decision refs: D-27 in 07-CONTEXT.md
"""

import random
from unittest.mock import Mock

try:
    import evennia
except Exception:  # pragma: no cover - fallback for pure-logic tests
    class _EvenniaStub:
        @staticmethod
        def search_tag(*args, **kwargs):
            return []

    evennia = _EvenniaStub()


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WANDER_CHANCE = 0.4  # 40% chance per tick to actually move


def _get_combat_handler(mob):
    """Return the current combat handler without triggering MagicMock autovivification."""
    ndb = getattr(mob, "ndb", None)
    if ndb is None:
        return None
    if isinstance(ndb, Mock):
        return vars(ndb).get("combat_handler")
    return getattr(ndb, "combat_handler", None)


# ---------------------------------------------------------------------------
# Single mob movement
# ---------------------------------------------------------------------------

def wander_mob(mob):
    """
    Attempt to move a wandering mob to a random connected room.

    Skips if:
      - mob.db.wander is not True
      - mob is in combat (ndb.combat_handler is not None)
      - mob has an active PatrolScript (patrol takes priority)
      - mob is dead (db.is_dead)
      - no valid exits exist (same zone, no no_mobs tag)

    After moving, echoes arrival to the destination room.

    Args:
        mob: SoravelonMob instance.

    Returns:
        bool: True if mob moved, False otherwise.
    """
    # Guard: wander flag
    if not mob.db.wander:
        return False

    # Guard: in combat
    if _get_combat_handler(mob) is not None:
        return False

    # Guard: active patrol script takes priority
    patrol_scripts = mob.scripts.get("patrol_script")
    if patrol_scripts:
        return False

    # Guard: dead or deleted
    if not mob.pk or mob.db.is_dead:
        return False

    # Guard: no location
    if not mob.location:
        return False

    # Collect valid exits: same zone, no no_mobs tag on destination
    current_zone = mob.location.db.zone_id
    valid_exits = []
    for exit_obj in mob.location.exits:
        dest = exit_obj.destination
        if not dest:
            continue
        # Zone boundary check
        if dest.db.zone_id != current_zone:
            continue
        # no_mobs room check
        if dest.tags.get("no_mobs", category="room_flag"):
            continue
        valid_exits.append(exit_obj)

    if not valid_exits:
        return False

    # Pick random exit and move. Server-side wander movement should not trigger
    # player-style at_post_move look hooks.
    chosen_exit = random.choice(valid_exits)
    destination = chosen_exit.destination
    mob.location = destination

    # Echo arrival to destination room
    destination.msg_contents(f"{mob.key} wanders in.")

    return True


# ---------------------------------------------------------------------------
# Batch tick
# ---------------------------------------------------------------------------

def wander_tick():
    """
    Tick function called by TICKER_HANDLER every 60 seconds.

    Finds all mobs tagged "wanderer" (category="mob_behavior"),
    rolls a stochastic chance per mob, and calls wander_mob on
    those that pass.

    The 40% chance per tick means mobs move on average once per
    2.5 minutes -- creating organic, living zones without
    overwhelming movement.
    """
    wanderers = evennia.search_tag("wanderer", category="mob_behavior")

    for mob in wanderers:
        if random.random() < WANDER_CHANCE:
            wander_mob(mob)
