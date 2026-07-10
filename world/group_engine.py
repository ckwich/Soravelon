"""
Group system for Soravelon.

Groups are session-state only — stored in ndb, not the database.
If the leader disconnects or leaves, leadership passes to another member.
Groups dissolve only when all members leave.
Maximum 6 players per group.

Loot modes: personal (default), ffa, round_robin.
Quest drops and Scales are ALWAYS personal regardless of loot mode.
"""

import evennia
import uuid

MAX_GROUP_SIZE = 6
VALID_LOOT_MODES = ("personal", "ffa", "round_robin")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_group_state(leader):
    return getattr(leader.ndb, 'group_state', None)


def _resolve_character(char_id):
    if char_id is None:
        return None
    objs = evennia.search_object("#" + str(char_id))
    return objs[0] if objs else None


def _ensure_presence_nonce(character):
    """Return a live-session invite nonce, creating one when needed."""
    nonce = getattr(character.ndb, "presence_nonce", None)
    if nonce:
        return nonce
    nonce = str(uuid.uuid4())
    character.ndb.presence_nonce = nonce
    return nonce


def _parse_pending_invite(invite_entry):
    """Normalize a pending invite entry to inviter_id/presence_nonce fields."""
    if not isinstance(invite_entry, dict):
        return None, None
    return invite_entry.get("inviter_id"), invite_entry.get("presence_nonce")


def _resolve_pending_invite(character):
    """
    Return a validated pending invite tuple or clear it if stale.

    The invite is only valid while the inviter still has the same
    `presence_nonce`, which expires on logout/reconnect.
    """
    invite_entry = getattr(character.ndb, "pending_group_invite", None)
    if not invite_entry:
        return None, None

    inviter_id, presence_nonce = _parse_pending_invite(invite_entry)
    inviter = _resolve_character(inviter_id)
    if (
        not inviter
        or not presence_nonce
        or getattr(inviter.ndb, "presence_nonce", None) != presence_nonce
    ):
        character.ndb.pending_group_invite = None
        return None, None

    return inviter, invite_entry


def get_group_state(character):
    """Return the public group-state dict for character's current group."""
    if not is_in_group(character):
        return None
    leader = _get_leader(character)
    if not leader:
        return None
    return _get_group_state(leader)


def _get_leader(character):
    leader_id = getattr(character.ndb, 'group_leader_id', None)
    if leader_id is None:
        return None
    return _resolve_character(leader_id)


def _get_group_members(leader):
    state = _get_group_state(leader)
    if not state:
        return []

    members = []
    valid_ids = []
    for char_id in state["members"]:
        objs = evennia.search_object("#" + str(char_id))
        if objs and getattr(objs[0].ndb, 'group_leader_id', None) == leader.id:
            members.append(objs[0])
            valid_ids.append(char_id)

    if len(valid_ids) != len(state["members"]):
        state["members"] = valid_ids
        leader.ndb.group_state = state

    return members


def is_in_group(character):
    return getattr(character.ndb, 'group_leader_id', None) is not None


def is_group_leader(character):
    state = _get_group_state(character)
    return bool(state and state.get("leader_id") == character.id)


def get_group_member_ids(character):
    """Return the live member IDs for character's current group."""
    return [member.id for member in get_group_members(character)]


def get_group_members(character):
    """Return the live members of character's current group.

    The leader owns durable group state, but gameplay systems must be able to
    ask from any member's perspective. `_get_group_members` also prunes stale
    entries, so callers never receive a cached or merely claimed relationship.
    """
    if not is_in_group(character):
        return []
    leader = _get_leader(character)
    if not leader:
        return []
    return _get_group_members(leader)


def are_allies(character, other):
    """Return whether two distinct characters share one live group.

    Group state lives only on the leader, while every member carries the
    leader ID. Checking both sides prevents stale member references or an
    arbitrary combatant from being treated as an ally.
    """
    if not character or not other or character.id == other.id:
        return False
    if not is_in_group(character) or not is_in_group(other):
        return False

    leader = _get_leader(character)
    if not leader or getattr(other.ndb, "group_leader_id", None) != leader.id:
        return False

    return any(member.id == other.id for member in _get_group_members(leader))


# ---------------------------------------------------------------------------
# Group formation
# ---------------------------------------------------------------------------

def send_group_invite(inviter, target):
    if target == inviter:
        return False, "You can't invite yourself."

    if is_in_group(target):
        return False, f"{target.key} is already in a group."

    if is_in_group(inviter):
        leader = _get_leader(inviter)
        if leader:
            members = _get_group_members(leader)
            if len(members) >= MAX_GROUP_SIZE:
                return False, f"Your group is full ({MAX_GROUP_SIZE} max)."

    pending_inviter, _ = _resolve_pending_invite(target)
    if pending_inviter:
        if pending_inviter.id == inviter.id:
            return False, f"{target.key} already has your pending group invite."
        return False, f"{target.key} already has a pending group invite."

    target.ndb.pending_group_invite = {
        "inviter_id": inviter.id,
        "presence_nonce": _ensure_presence_nonce(inviter),
    }
    target.msg(
        f"|w{inviter.key}|n invites you to join their group. "
        f"Type '|wgroup accept|n' or '|wgroup decline|n'."
    )
    inviter.msg(f"Group invite sent to {target.key}.")
    return True, ""


def accept_group_invite(character):
    inviter, _ = _resolve_pending_invite(character)
    if not inviter:
        return False, "You have no pending group invite."

    character.ndb.pending_group_invite = None

    if is_in_group(inviter):
        leader = _get_leader(inviter)
        if not leader:
            return False, "That group invite has expired."
    else:
        leader = inviter
        leader.ndb.group_leader_id = leader.id
        leader.ndb.group_state = {
            "members": [leader.id],
            "leader_id": leader.id,
            "loot_mode": "personal",
            "round_robin_index": 0,
        }

    members = _get_group_members(leader)
    if len(members) >= MAX_GROUP_SIZE:
        return False, "That group is now full."

    state = leader.ndb.group_state
    state["members"].append(character.id)
    leader.ndb.group_state = state
    character.ndb.group_leader_id = leader.id

    for member in _get_group_members(leader):
        if member != character:
            member.msg(f"|w{character.key}|n has joined the group.")

    character.msg(
        f"You join {leader.key}'s group. "
        f"({len(state['members'])}/{MAX_GROUP_SIZE})"
    )
    return True, ""


def decline_group_invite(character):
    invite_entry = getattr(character.ndb, 'pending_group_invite', None)
    if not invite_entry:
        return False, "You have no pending group invite."

    character.ndb.pending_group_invite = None

    inviter_id, _ = _parse_pending_invite(invite_entry)
    inviter = _resolve_character(inviter_id)
    if inviter:
        inviter.msg(f"{character.key} declined your group invite.")

    return True, f"You decline the group invite."


def leave_group(character):
    if not is_in_group(character):
        return False, "You're not in a group."

    leader = _get_leader(character)
    if not leader:
        character.ndb.group_leader_id = None
        return True, "You leave the group."

    state = _get_group_state(leader)
    if not state:
        character.ndb.group_leader_id = None
        return True, "You leave the group."

    state["members"] = [
        mid for mid in state["members"] if mid != character.id
    ]
    leader.ndb.group_state = state
    character.ndb.group_leader_id = None

    remaining = _get_group_members(leader)
    for member in remaining:
        member.msg(f"|w{character.key}|n has left the group.")

    if not remaining:
        leader.ndb.group_state = None
        leader.ndb.group_leader_id = None
        return True, "You leave the group. The group is now empty."

    if character == leader:
        new_leader = remaining[0]
        _transfer_leadership_internal(leader, new_leader, state, old_leader_stays=False)
        new_leader.msg("|wYou are now the group leader.|n")

    character.msg("You leave the group.")
    return True, ""


def kick_from_group(leader, target):
    if not is_group_leader(leader):
        return False, "Only the group leader can kick members."
    if target == leader:
        return False, "You can't kick yourself. Use 'group leave'."

    state = _get_group_state(leader)
    if target.id not in state["members"]:
        return False, f"{target.key} isn't in your group."

    state["members"] = [mid for mid in state["members"] if mid != target.id]
    leader.ndb.group_state = state
    target.ndb.group_leader_id = None

    target.msg("You have been removed from the group.")
    for member in _get_group_members(leader):
        member.msg(f"|w{target.key}|n was removed from the group.")

    return True, f"You remove {target.key} from the group."


def transfer_leadership(current_leader, new_leader):
    if not is_group_leader(current_leader):
        return False, "You are not the group leader."

    state = _get_group_state(current_leader)
    if new_leader.id not in state["members"]:
        return False, f"{new_leader.key} isn't in your group."

    _transfer_leadership_internal(current_leader, new_leader, state)

    for member in _get_group_members(new_leader):
        member.msg(f"|w{new_leader.key}|n is now the group leader.")
    return True, ""


def _transfer_leadership_internal(old_leader, new_leader, state, old_leader_stays=True):
    state["leader_id"] = new_leader.id
    new_leader.ndb.group_state = state
    new_leader.ndb.group_leader_id = new_leader.id
    old_leader.ndb.group_state = None
    old_leader.ndb.group_leader_id = new_leader.id if old_leader_stays else None


def set_loot_mode(leader, mode):
    if not is_group_leader(leader):
        return False, "Only the group leader can change loot mode."
    if mode not in VALID_LOOT_MODES:
        return False, (
            f"Invalid loot mode. Choose: {', '.join(VALID_LOOT_MODES)}"
        )

    state = _get_group_state(leader)
    state["loot_mode"] = mode
    leader.ndb.group_state = state

    for member in _get_group_members(leader):
        member.msg(f"Loot mode set to: |w{mode}|n")

    return True, ""


# ---------------------------------------------------------------------------
# Zone and proximity queries
# ---------------------------------------------------------------------------

def get_members_in_zone(character, zone_id):
    if not is_in_group(character):
        return []

    leader = _get_leader(character)
    if not leader:
        return []

    members_in_zone = []
    for member in _get_group_members(leader):
        room = member.location
        if room and (room.db.zone_id or "") == zone_id:
            members_in_zone.append(member)

    return members_in_zone


def get_members_in_proximity(character, radius=3):
    from world.node_helpers import get_rooms_in_radius

    if not is_in_group(character):
        return [character]

    leader = _get_leader(character)
    if not leader:
        return [character]

    current_room = character.location
    if not current_room:
        return [character]

    nearby_rooms = set(get_rooms_in_radius(current_room, radius))

    nearby_members = []
    for member in _get_group_members(leader):
        if member.location in nearby_rooms:
            nearby_members.append(member)

    return nearby_members


# ---------------------------------------------------------------------------
# Loot distribution (D-27)
# ---------------------------------------------------------------------------

def get_designated_looter(character, corpse):
    """
    Determine who should loot based on group loot mode.
    Returns the designated character, or None if anyone can loot.

    personal mode: only the killer
    ffa mode: anyone (return None)
    round_robin mode: next in rotation
    """
    if not is_in_group(character):
        return None

    leader = _get_leader(character)
    if not leader:
        return None

    state = _get_group_state(leader)
    if not state:
        return None

    mode = state.get("loot_mode", "personal")

    if mode == "ffa":
        return None  # Anyone can loot

    if mode == "personal":
        # Only killer
        killer_id = corpse.db.killer_id
        if killer_id == character.id:
            return character
        # Find killer in group
        members = _get_group_members(leader)
        for m in members:
            if m.id == killer_id:
                return m
        return character  # fallback

    if mode == "round_robin":
        members = _get_group_members(leader)
        if not members:
            return character
        idx = state.get("round_robin_index", 0) % len(members)
        return members[idx]

    return character


def advance_round_robin(character):
    """Advance round robin index after successful loot."""
    leader = _get_leader(character)
    if not leader:
        return
    state = _get_group_state(leader)
    if not state or state.get("loot_mode") != "round_robin":
        return
    members = _get_group_members(leader)
    if not members:
        return
    state["round_robin_index"] = (state.get("round_robin_index", 0) + 1) % len(members)
    leader.ndb.group_state = state


# ---------------------------------------------------------------------------
# Disconnect cleanup
# ---------------------------------------------------------------------------

def on_member_disconnect(character):
    if not is_in_group(character):
        return
    leave_group(character)
