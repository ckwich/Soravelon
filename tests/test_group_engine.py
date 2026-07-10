"""
Tests for group engine (Build Order Step 11).
Tests written FIRST per TDD.
"""

from unittest.mock import MagicMock

from evennia.utils.test_resources import EvenniaTest
from evennia import create_object


class GroupTestBase(EvenniaTest):
    def setUp(self):
        super().setUp()
        from typeclasses.rooms import SoravelonRoom
        self.room = create_object(SoravelonRoom, key="Room")
        self.room.db.zone_id = "test_zone"
        self.char1.location = self.room
        self.char2.location = self.room
        self.char1.db.backend_level = 10
        self.char2.db.backend_level = 10
        self.char1.ndb.presence_nonce = "leader-online"
        self.char2.ndb.presence_nonce = "member-online"

    def _make_char(self, key="Extra"):
        c = create_object(self.char1.__class__, key=key)
        c.location = self.room
        c.db.backend_level = 10
        return c


class TestSendInviteStoresPending(GroupTestBase):
    def test_send_invite_stores_pending(self):
        from world.group_engine import send_group_invite
        success, _ = send_group_invite(self.char1, self.char2)
        self.assertTrue(success)
        invite = self.char2.ndb.pending_group_invite
        self.assertEqual(invite["inviter_id"], self.char1.id)
        self.assertEqual(invite["presence_nonce"], "leader-online")


class TestSendInviteToSelfFails(GroupTestBase):
    def test_send_invite_to_self_fails(self):
        from world.group_engine import send_group_invite
        success, _ = send_group_invite(self.char1, self.char1)
        self.assertFalse(success)


class TestSendInviteToGroupedFails(GroupTestBase):
    def test_send_invite_to_grouped_player_fails(self):
        from world.group_engine import send_group_invite, accept_group_invite
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        c3 = self._make_char("C3")
        success, _ = send_group_invite(c3, self.char2)
        self.assertFalse(success)


class TestAcceptCreatesGroup(GroupTestBase):
    def test_accept_invite_creates_group(self):
        from world.group_engine import send_group_invite, accept_group_invite, is_in_group
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        self.assertTrue(is_in_group(self.char1))
        self.assertTrue(is_in_group(self.char2))
        state = self.char1.ndb.group_state
        self.assertIn(self.char1.id, state["members"])
        self.assertIn(self.char2.id, state["members"])


class TestGroupAllies(GroupTestBase):
    """Combat-facing ally relationship queries use live group membership."""

    def test_group_members_are_available_from_leader_or_member(self):
        """Combat can enumerate the same live group from either participant."""
        from world.group_engine import (
            accept_group_invite,
            get_group_members,
            send_group_invite,
        )

        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)

        self.assertEqual(
            {member.id for member in get_group_members(self.char1)},
            {self.char1.id, self.char2.id},
        )
        self.assertEqual(
            {member.id for member in get_group_members(self.char2)},
            {self.char1.id, self.char2.id},
        )

    def test_allies_are_reciprocal_for_leader_and_member_only(self):
        from world.group_engine import are_allies, accept_group_invite, send_group_invite

        outsider = self._make_char("Outsider")
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)

        self.assertTrue(are_allies(self.char1, self.char2))
        self.assertTrue(are_allies(self.char2, self.char1))
        self.assertFalse(are_allies(self.char1, outsider))
        outsider.ndb.group_leader_id = self.char1.id
        self.assertFalse(are_allies(self.char1, outsider))
        self.assertFalse(are_allies(self.char1, self.char1))

    def test_combat_recording_credits_only_live_group_allies(self):
        from world.combat_script import CombatScript
        from world.group_engine import accept_group_invite, send_group_invite

        outsider = self._make_char("Outsider")
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        outsider.ndb.group_leader_id = self.char1.id

        script = MagicMock()
        script.ndb.ally_action_count = {}
        script._resolve_combatants.return_value = [self.char1, self.char2, outsider]

        CombatScript.record_allied_action(script, self.char1)
        CombatScript.record_allied_action(script, self.char2)

        self.assertEqual(
            script.ndb.ally_action_count,
            {str(self.char2.id): 1, str(self.char1.id): 1},
        )


class TestAcceptAddsToExisting(GroupTestBase):
    def test_accept_invite_adds_to_existing_group(self):
        from world.group_engine import send_group_invite, accept_group_invite
        c3 = self._make_char("C3")
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        send_group_invite(self.char1, c3)
        accept_group_invite(c3)
        state = self.char1.ndb.group_state
        self.assertEqual(len(state["members"]), 3)


class TestDeclineClearsPending(GroupTestBase):
    def test_decline_invite_clears_pending(self):
        from world.group_engine import send_group_invite, decline_group_invite
        send_group_invite(self.char1, self.char2)
        decline_group_invite(self.char2)
        self.assertIsNone(self.char2.ndb.pending_group_invite)


class TestSendInviteRejectsPendingInvite(GroupTestBase):
    def test_send_invite_rejects_target_with_other_pending_invite(self):
        from world.group_engine import send_group_invite
        c3 = self._make_char("C3")
        c3.ndb.presence_nonce = "other-online"

        send_group_invite(c3, self.char2)
        success, msg = send_group_invite(self.char1, self.char2)

        self.assertFalse(success)
        self.assertIn("pending group invite", msg)
        self.assertEqual(
            self.char2.ndb.pending_group_invite["inviter_id"],
            c3.id,
        )


class TestSendInviteClearsStalePendingInvite(GroupTestBase):
    def test_send_invite_replaces_stale_pending_invite(self):
        from world.group_engine import send_group_invite

        stale = self._make_char("Stale")
        stale.ndb.presence_nonce = None
        self.char2.ndb.pending_group_invite = {
            "inviter_id": stale.id,
            "presence_nonce": "expired-token",
        }

        success, _ = send_group_invite(self.char1, self.char2)

        self.assertTrue(success)
        self.assertEqual(
            self.char2.ndb.pending_group_invite["inviter_id"],
            self.char1.id,
        )


class TestLeaveRemovesMember(GroupTestBase):
    def test_leave_group_removes_member(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, leave_group, is_in_group
        )
        c3 = self._make_char("C3")
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        send_group_invite(self.char1, c3)
        accept_group_invite(c3)
        leave_group(self.char2)
        self.assertFalse(is_in_group(self.char2))
        state = self.char1.ndb.group_state
        self.assertNotIn(self.char2.id, state["members"])


class TestLeaderLeaveTransfers(GroupTestBase):
    def test_leader_leave_transfers_leadership(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, leave_group,
            is_group_leader, is_in_group
        )
        c3 = self._make_char("C3")
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        send_group_invite(self.char1, c3)
        accept_group_invite(c3)
        leave_group(self.char1)
        self.assertTrue(is_group_leader(self.char2))
        self.assertFalse(is_in_group(self.char1))


class TestLastMemberDissolves(GroupTestBase):
    def test_last_member_leave_dissolves_group(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, leave_group,
            is_in_group
        )
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        leave_group(self.char2)
        leave_group(self.char1)
        self.assertFalse(is_in_group(self.char1))
        self.assertIsNone(self.char1.ndb.group_state)


class TestKickMember(GroupTestBase):
    def test_kick_member(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, kick_from_group,
            is_in_group
        )
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        kick_from_group(self.char1, self.char2)
        self.assertFalse(is_in_group(self.char2))


class TestKickSelfFails(GroupTestBase):
    def test_kick_self_fails(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, kick_from_group
        )
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        success, _ = kick_from_group(self.char1, self.char1)
        self.assertFalse(success)


class TestSetLootModeValid(GroupTestBase):
    def test_set_loot_mode_valid(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, set_loot_mode
        )
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        success, _ = set_loot_mode(self.char1, "ffa")
        self.assertTrue(success)
        self.assertEqual(self.char1.ndb.group_state["loot_mode"], "ffa")


class TestSetLootModeInvalid(GroupTestBase):
    def test_set_loot_mode_invalid(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, set_loot_mode
        )
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        success, _ = set_loot_mode(self.char1, "bogus")
        self.assertFalse(success)


class TestLootModeNonLeaderFails(GroupTestBase):
    def test_loot_mode_non_leader_fails(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, set_loot_mode
        )
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        success, _ = set_loot_mode(self.char2, "ffa")
        self.assertFalse(success)


class TestGetMembersInZone(GroupTestBase):
    def test_get_members_in_zone(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite, get_members_in_zone
        )
        from typeclasses.rooms import SoravelonRoom
        c3 = self._make_char("C3")
        other_room = create_object(SoravelonRoom, key="Other")
        other_room.db.zone_id = "other_zone"
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        send_group_invite(self.char1, c3)
        accept_group_invite(c3)
        # Move c3 to different zone
        c3.location = other_room
        members = get_members_in_zone(self.char1, "test_zone")
        self.assertEqual(len(members), 2)  # char1 + char2, not c3


class TestGetMembersInZoneSolo(GroupTestBase):
    def test_get_members_in_zone_solo(self):
        from world.group_engine import get_members_in_zone
        members = get_members_in_zone(self.char1, "test_zone")
        self.assertEqual(len(members), 0)


class TestMaxGroupSizeEnforced(GroupTestBase):
    def test_max_group_size_enforced(self):
        from world.group_engine import send_group_invite, accept_group_invite
        members = []
        for i in range(5):
            c = self._make_char(f"Extra{i}")
            members.append(c)

        # Invite and accept 5 (total 6 with leader)
        for c in members:
            send_group_invite(self.char1, c)
            accept_group_invite(c)

        # 7th should fail
        c7 = self._make_char("Extra6")
        success, _ = send_group_invite(self.char1, c7)
        # Group is full — either invite fails or accept fails
        if success:
            s2, _ = accept_group_invite(c7)
            self.assertFalse(s2)
        else:
            self.assertFalse(success)


class TestOnDisconnectLeavesGroup(GroupTestBase):
    def test_on_disconnect_leaves_group(self):
        from world.group_engine import (
            send_group_invite, accept_group_invite,
            on_member_disconnect, is_in_group
        )
        c3 = self._make_char("C3")
        send_group_invite(self.char1, self.char2)
        accept_group_invite(self.char2)
        send_group_invite(self.char1, c3)
        accept_group_invite(c3)
        on_member_disconnect(self.char2)
        self.assertFalse(is_in_group(self.char2))


class TestAcceptInviteExpiresAfterInviterDisconnect(GroupTestBase):
    def test_accept_invite_fails_when_inviter_presence_expires(self):
        from world.group_engine import send_group_invite, accept_group_invite

        send_group_invite(self.char1, self.char2)
        self.char1.ndb.presence_nonce = None

        success, msg = accept_group_invite(self.char2)

        self.assertFalse(success)
        self.assertIn("pending group invite", msg.lower())
        self.assertIsNone(self.char2.ndb.pending_group_invite)


    # TestGroupScalingInZoneOnly removed — group scaling no longer exists.
    # get_members_in_zone() is tested in TestGetMembersInZone above.
    # It serves proximity mechanics (Tactics, abilities), not scaling.
