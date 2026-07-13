"""Database-backed M3 golden path through live authored world content."""

from unittest.mock import patch

from evennia.utils.test_resources import EvenniaTest


FIRST_PRACTICED_STOPS = (
    ("hg_stable", "vc_stable_calm_nervous_mare"),
    ("mk_tanner", "vc_tanner_cut_repair_strap"),
    ("ash_road_03", "ash_road_read_wolf_sign"),
    ("grass_07", "ash_grass_test_shelter_grass"),
)


class TestM3GoldenPath(EvenniaTest):
    def _room(self, room_id):
        from world.tag_search import search_objects_by_exact_tag

        matches = search_objects_by_exact_tag(room_id, "room_id")
        self.assertEqual(len(matches), 1, room_id)
        return matches[0]

    def _walk_to(self, destination):
        from world.social_playtest_verification import _shortest_route

        route = _shortest_route(self.char1.location, destination)
        self.assertTrue(route, f"No walking route to {destination.key}")
        for exit_obj in route:
            origin = self.char1.location
            exit_obj.at_traverse(self.char1, exit_obj.destination)
            self.assertIsNot(self.char1.location, origin)
            self.assertIs(self.char1.location, exit_obj.destination)

    def _perform_authored_practice(self, opportunity_id):
        from commands.cmd_dynamic import DynamicAreaCommand

        command_def = next(
            definition
            for definition in (self.char1.location.db.custom_commands or [])
            if definition.get("action_dict", {}).get("opportunity_id") == opportunity_id
        )
        action = command_def["action_dict"]
        command = DynamicAreaCommand()
        command.caller = self.char1
        command.args = action["target"]
        command.action_dict = action
        command.func()

    def test_fresh_character_walks_from_arrival_to_practiced_and_induction(self):
        from commands.cmd_dialogue import CmdAccept, CmdTalk
        from world.ancestry_engine import set_ancestry
        from world.areas import ashreach_plains, vaels_crossing
        from world.inventory_engine import get_equipped_items
        from world.models import (
            CharacterAbility,
            CharacterGuild,
            GuildRecruitment,
            ProgressionEvent,
            SocialFact,
        )
        from world.tag_search import search_objects_by_exact_tag
        from world.weapon_skills import infer_weapon_family_from_item
        from world.world_state import commit_session_xp, init_session_accumulators

        # Cross-zone exits resolve on the second build of the first-loaded zone.
        ashreach_plains.build()
        vaels_crossing.build()
        ashreach_plains.build()

        self.char1.db.needs_start_location = True
        self.assertTrue(self.char1._place_at_start_location_if_available())
        self.assertIs(self.char1.location, self._room("hg_arrival"))

        ancestry_set, ancestry_message = set_ancestry(self.char1, "human")
        self.assertTrue(ancestry_set, ancestry_message)
        equipped = get_equipped_items(self.char1)
        self.assertTrue(equipped)
        equipped_snapshot = [
            (item.key, item.db.item_type, item.db.armor_value, record.equipment_slot)
            for item, record in equipped
        ]
        self.assertTrue(
            any(
                record.equipment_slot == "main_hand"
                and (item.db.damage_max or 0) > (item.db.damage_min or 0)
                and infer_weapon_family_from_item(item)
                for item, record in equipped
            ),
            equipped_snapshot,
        )
        self.assertTrue(
            any((item.db.armor_value or 0) > 0 for item, _record in equipped),
            equipped_snapshot,
        )
        self.assertFalse(
            CharacterAbility.objects.filter(
                character=self.char1,
                ability_id="thorn_lash",
            ).exists()
        )

        init_session_accumulators(self.char1)
        for room_id, opportunity_id in FIRST_PRACTICED_STOPS:
            self._walk_to(self._room(room_id))
            self._perform_authored_practice(opportunity_id)

        commit_session_xp(self.char1)
        self.assertEqual(self.char1.db.domain_scores, {"naturalism": 30.0})
        self.assertEqual(
            ProgressionEvent.objects.filter(
                character=self.char1,
                applied_at__isnull=False,
            ).count(),
            4,
        )
        invitation = GuildRecruitment.objects.get(
            character=self.char1,
            guild_id="verdance",
        )
        self.assertEqual(invitation.status, "offered")

        contact = next(
            npc
            for npc in search_objects_by_exact_tag(
                invitation.contact_npc_id,
                "npc_id",
            )
            if npc.db.zone_id == invitation.location_zone_id
        )
        self._walk_to(contact.location)

        with patch.object(self.char1, "msg"), patch(
            "world.oob_publisher.push_quest_update"
        ):
            talk = CmdTalk()
            talk.caller = self.char1
            talk.args = "Elwen"
            talk.func()

            accept = CmdAccept()
            accept.caller = self.char1
            accept.args = "resonance"
            accept.func()

        membership = CharacterGuild.objects.get(character=self.char1)
        self.assertTrue(membership.induction_complete)
        self.assertEqual(membership.guild_id, "verdance")
        self.assertEqual(membership.secondary_domain, "resonance")
        self.assertTrue(
            CharacterAbility.objects.filter(
                character=self.char1,
                ability_id="thorn_lash",
            ).exists()
        )
        self.assertTrue(
            SocialFact.objects.filter(
                fact_key=f"fact:guild_induction:{self.char1.id}:verdance"
            ).exists()
        )
