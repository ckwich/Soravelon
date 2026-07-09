import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from evennia.utils.test_resources import EvenniaTest


class TestSocialClaimRepairService(EvenniaTest):
    """Players can contest social claims without mutating hidden reputation."""

    def _npc(self):
        return SimpleNamespace(
            key="Whistle",
            db=SimpleNamespace(
                npc_id="npc_innkeeper_whistle",
                npc_name="Whistle",
                zone_id="vaels_crossing",
                faction="",
            ),
        )

    def _seed_known_rumor(self):
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )

        player = ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
        )
        innkeeper = ensure_social_node(
            "npc",
            "npc_innkeeper_whistle",
            display_name="Whistle",
            zone_id="vaels_crossing",
        )
        witness = ensure_social_node("npc", "npc_debt_collector_raith")
        ok, message, fact = record_social_fact(
            fact_key="fact:test_market_square_robbery",
            subject_node_key=player.node_key,
            actor_node_key=witness.node_key,
            event_type="rumor_seeded",
            summary="Someone claims the player was near the Market Square robbery.",
            tags=["market", "robbery", "rumor"],
            visibility="local",
        )
        self.assertTrue(ok, message)
        ok, message, claim = assert_social_claim(
            claim_key="claim:test_market_square_robbery",
            speaker_node_key=witness.node_key,
            subject_node_key=player.node_key,
            fact_key=fact.fact_key,
            claim_type="rumor",
            summary="Raith says the player was seen near the Market Square robbery.",
            status="rumor",
            intent="leverage",
            bias_tags=["market", "robbery"],
            confidence=0.45,
        )
        self.assertTrue(ok, message)
        ok, message, _knowledge = mark_known(
            node_key=innkeeper.node_key,
            claim_key=claim.claim_key,
            source_node_key=witness.node_key,
            channel="tavern_rumor",
            confidence=0.45,
            spreading=False,
        )
        self.assertTrue(ok, message)
        return player, innkeeper, witness, fact, claim

    def test_denial_records_player_claim_and_keeps_original_rumor(self):
        from world.models import SocialClaim, SocialKnowledge
        from world.social_claim_repair import deny_social_claim

        player, innkeeper, _witness, fact, rumor = self._seed_known_rumor()

        result = deny_social_claim(self.char1, self._npc(), topic_text="me")

        self.assertTrue(result.ok, result.message)
        denial = result.claim
        self.assertIsNotNone(denial)
        self.assertEqual(denial.claim_type, "denial")
        self.assertEqual(denial.status, "contested")
        self.assertEqual(denial.intent, "claim_repair")
        self.assertEqual(denial.speaker_node, player)
        self.assertEqual(denial.subject_node, player)
        self.assertEqual(denial.fact, fact)
        self.assertIn("deny", denial.summary.lower())

        rumor.refresh_from_db()
        self.assertEqual(rumor.status, "rumor")
        self.assertTrue(SocialClaim.objects.filter(claim_key=rumor.claim_key).exists())
        npc_knowledge = SocialKnowledge.objects.get(
            node=innkeeper,
            claim=denial,
        )
        self.assertEqual(npc_knowledge.channel, "direct_witness")
        self.assertEqual(npc_knowledge.source_node, player)
        self.assertFalse(npc_knowledge.spreading)
        self.assertIn("answered_claim_key", npc_knowledge.evidence)
        self.assertNotIn(rumor.claim_key, result.message)

    def test_denial_fails_closed_when_target_knows_no_repairable_claim(self):
        from world.social_claim_repair import deny_social_claim
        from world.social_engine import ensure_social_node

        ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
        )
        ensure_social_node("npc", "npc_innkeeper_whistle", display_name="Whistle")

        result = deny_social_claim(self.char1, self._npc(), topic_text="me")

        self.assertFalse(result.ok)
        self.assertIsNone(result.claim)
        self.assertIn("nothing specific", result.message.lower())


class TestCmdDeny(unittest.TestCase):
    """The player command is a thin safe wrapper over claim repair."""

    def test_deny_command_records_repair_through_service(self):
        from commands.cmd_social_verbs import CmdDeny

        caller = MagicMock()
        npc = MagicMock()
        npc.db.npc_name = "Whistle"
        result = SimpleNamespace(
            ok=True,
            message="hears your denial and weighs it against the story.",
            claim=MagicMock(),
        )

        with (
            patch(
                "commands.cmd_dialogue._find_npc_in_room",
                return_value=npc,
            ) as mock_find,
            patch(
                "world.social_claim_repair.deny_social_claim",
                return_value=result,
            ) as mock_deny,
        ):
            cmd = CmdDeny()
            cmd.caller = caller
            cmd.args = "Whistle about me"
            cmd.func()

        mock_find.assert_called_once_with(caller, "Whistle")
        mock_deny.assert_called_once_with(caller, npc, topic_text="me")
        caller.msg.assert_called_once_with(
            "|wWhistle|n hears your denial and weighs it against the story."
        )

    def test_deny_command_requires_about_me_shape(self):
        from commands.cmd_social_verbs import CmdDeny

        caller = MagicMock()
        cmd = CmdDeny()
        cmd.caller = caller
        cmd.args = "Whistle"

        cmd.func()

        caller.msg.assert_called_once()
        self.assertIn("Usage: deny <npc> about me", caller.msg.call_args[0][0])


class TestSocialVerbCmdsetRegistration(unittest.TestCase):
    def test_deny_command_is_registered_on_character_cmdset(self):
        from commands import default_cmdsets

        added_commands = []

        with patch.object(
            default_cmdsets.default_cmds.CharacterCmdSet,
            "at_cmdset_creation",
            return_value=None,
        ):
            cmdset = default_cmdsets.CharacterCmdSet()
            cmdset.add = added_commands.append
            cmdset.at_cmdset_creation()

        self.assertIn("deny", {cmd.key for cmd in added_commands})
