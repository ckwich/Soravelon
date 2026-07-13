"""Durable, local-contact guild recruitment and induction contracts."""

from unittest.mock import MagicMock

from evennia.utils.test_resources import EvenniaTest


class TestGuildRecruitment(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.db.domain_scores = {"naturalism": 30.0, "resonance": 5.0}
        self.char1.db.guild_id = None
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.subclass_id = None

    def _place_verdance_contact(self):
        self.room1.tags.add("gq_naturalism_hall", category="room_id")
        self.obj1.location = self.room1
        self.obj1.db.npc_id = "npc_guildmaster_naturalism_elwen"
        self.obj1.tags.add(
            "npc_guildmaster_naturalism_elwen",
            category="npc_id",
        )
        self.char1.location = self.room1
        return self.obj1

    def test_practiced_threshold_creates_durable_invitation_not_membership(self):
        from world.guild_engine import ensure_guild_recruitments
        from world.models import CharacterAbility, CharacterGuild, GuildRecruitment

        created = ensure_guild_recruitments(self.char1)

        self.assertEqual([record.guild_id for record in created], ["verdance"])
        invitation = GuildRecruitment.objects.get(character=self.char1)
        self.assertEqual(invitation.status, "offered")
        self.assertEqual(
            invitation.contact_npc_id,
            "npc_guildmaster_naturalism_elwen",
        )
        self.assertEqual(invitation.location_room_id, "gq_naturalism_hall")
        self.assertFalse(CharacterGuild.objects.filter(character=self.char1).exists())
        self.assertFalse(CharacterAbility.objects.filter(character=self.char1).exists())
        self.assertIsNone(self.char1.db.guild_id)

    def test_remote_induction_fails_without_mutating_membership(self):
        from world.guild_engine import complete_recruitment_induction, ensure_guild_recruitments
        from world.models import CharacterGuild

        invitation = ensure_guild_recruitments(self.char1)[0]
        self.obj1.db.npc_id = "npc_guildmaster_naturalism_elwen"
        self.obj1.location = self.room1
        self.char1.location = self.room2

        success, message = complete_recruitment_induction(
            self.char1,
            invitation,
            "resonance",
            self.obj1,
        )

        self.assertFalse(success)
        self.assertIn("in person", message.lower())
        self.assertFalse(CharacterGuild.objects.filter(character=self.char1).exists())
        self.assertIsNone(self.char1.db.guild_id)

    def test_contact_induction_commits_membership_social_fact_and_abilities_once(self):
        from world.guild_engine import complete_recruitment_induction, ensure_guild_recruitments
        from world.models import (
            CharacterAbility,
            CharacterGuild,
            GuildRecruitment,
            SocialFact,
        )

        contact = self._place_verdance_contact()
        invitation = ensure_guild_recruitments(self.char1)[0]

        success, message = complete_recruitment_induction(
            self.char1,
            invitation,
            "resonance",
            contact,
        )

        self.assertTrue(success, message)
        membership = CharacterGuild.objects.get(character=self.char1)
        self.assertTrue(membership.induction_complete)
        self.assertEqual(membership.guild_id, "verdance")
        self.assertEqual(membership.secondary_domain, "resonance")
        self.assertEqual(self.char1.db.guild_id, "verdance")
        self.assertTrue(CharacterAbility.objects.filter(character=self.char1).exists())
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, "completed")
        self.assertIsNotNone(invitation.completed_at)
        self.assertTrue(
            SocialFact.objects.filter(
                fact_key=f"fact:guild_induction:{self.char1.id}:verdance"
            ).exists()
        )

        replay, replay_message = complete_recruitment_induction(
            self.char1,
            invitation,
            "resonance",
            contact,
        )
        self.assertTrue(replay, replay_message)
        self.assertEqual(CharacterGuild.objects.filter(character=self.char1).count(), 1)
        self.assertEqual(GuildRecruitment.objects.filter(character=self.char1).count(), 1)

    def test_talk_then_accept_keeps_secondary_choice_inside_contact_scene(self):
        from evennia.utils import create

        from commands.cmd_dialogue import CmdAccept, CmdTalk
        from typeclasses.mobs import SoravelonMob
        from world.guild_engine import ensure_guild_recruitments

        self.room1.tags.add("gq_naturalism_hall", category="room_id")
        self.char1.location = self.room1
        self.char1.msg = MagicMock()
        contact = create.create_object(
            SoravelonMob,
            key="Elwen",
            location=self.room1,
        )
        contact.db.is_npc = True
        contact.db.npc_id = "npc_guildmaster_naturalism_elwen"
        contact.db.dialogue_greeting_tiers = {
            "neutral": "You found the hall. Now tell me what else shaped you."
        }
        contact.db.dialogue_topics = {}
        contact.db.dialogue_base_hints = []
        contact.db.dialogue_tier_hints = {}
        contact.db.dialogue_quest_hints = {}
        contact.db.dialogue_network_hints = []
        contact.db.dialogue_scholar_hints = []
        contact.db.dialogue_warden_hints = []
        ensure_guild_recruitments(self.char1)

        talk = CmdTalk()
        talk.caller = self.char1
        talk.args = "Elwen"
        talk.func()

        pending = self.char1.ndb.pending_guild_recruitment
        self.assertEqual(pending["npc"], contact)
        messages = [call.args[0] for call in self.char1.msg.call_args_list]
        self.assertTrue(any("accept <secondary_domain>" in msg for msg in messages))
        self.assertTrue(all("score:" not in msg.lower() for msg in messages))

        accept = CmdAccept()
        accept.caller = self.char1
        accept.args = "resonance"
        accept.func()

        self.assertEqual(self.char1.db.guild_id, "verdance")
        self.assertIsNone(self.char1.ndb.pending_guild_recruitment)
        self.assertTrue(
            any(
                "verdance" in call.args[0].lower()
                for call in self.char1.msg.call_args_list
            )
        )

    def test_decline_leaves_durable_invitation_open(self):
        from commands.cmd_dialogue import CmdDecline
        from world.guild_engine import ensure_guild_recruitments

        self.char1.msg = MagicMock()
        invitation = ensure_guild_recruitments(self.char1)[0]
        self.char1.ndb.pending_guild_recruitment = {
            "npc": self.obj1,
            "recruitment_id": invitation.id,
        }

        decline = CmdDecline()
        decline.caller = self.char1
        decline.args = ""
        decline.func()

        invitation.refresh_from_db()
        self.assertEqual(invitation.status, "offered")
        self.assertIsNone(self.char1.ndb.pending_guild_recruitment)
        self.assertIn("invitation remains", self.char1.msg.call_args[0][0].lower())
