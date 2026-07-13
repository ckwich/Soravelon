"""Database-backed M3 golden path through live authored world content."""

from types import SimpleNamespace
from unittest.mock import patch

from evennia import create_object
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
        from typeclasses.mobs import SoravelonMob
        from typeclasses.objects import GatheringNode, Object
        from typeclasses.rooms import SoravelonRoom
        from world.ancestry_engine import set_ancestry
        from world.areas import ashreach_plains, vaels_crossing
        from world.combat_engine import handle_mob_death, resolve_basic_attack
        from world.crafting_engine import craft_item
        from world.encounter_rewards import claim_personal_rewards
        from world.equipment_effects import (
            apply_armor_mitigation,
            get_effective_stats,
            get_total_equipped_armor,
        )
        from world.gathering_engine import complete_gather
        from world.group_engine import accept_group_invite, send_group_invite
        from world.inventory_engine import (
            equip_item,
            get_equipped_items,
            unequip_item,
        )
        from world.item_spawner import create_item_from_catalog
        from world.mob_spawner import MOB_INSTANCE_TAG_CATEGORY
        from world.models import (
            CharacterAbility,
            CharacterGuild,
            CharacterQuest,
            EncounterReward,
            FactionStanding,
            GuildRecruitment,
            ProgressionEvent,
            SocialClaim,
            SocialFact,
            SocialKnowledge,
        )
        from world.node_helpers import attempt_stabilization, stabilization_tick
        from world.social_claim_repair import deny_social_claim
        from world.social_engine import (
            assert_social_claim,
            ensure_social_node,
            mark_known,
            record_social_fact,
        )
        from world.tag_search import search_objects_by_exact_tag
        from world.weapon_skills import infer_weapon_family_from_item
        from world.world_state import commit_session_xp, init_session_accumulators
        from world.zone_object import initialize_node

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

        # Starter equipment changes the real combat inputs and mitigates a hit.
        effective_stats = get_effective_stats(self.char1)
        base_stats = dict(self.char1.db.base_stats)
        self.assertTrue(
            any(effective_stats[stat] > value for stat, value in base_stats.items())
        )
        armor = get_total_equipped_armor(self.char1)
        self.assertGreater(armor, 0)
        training_mob = create_object(
            SoravelonMob,
            key="Roadside Sparring Construct",
            location=self.char1.location,
        )
        training_mob.db.base_stats = None
        training_mob.db.ref_damage_min = 20
        training_mob.db.ref_damage_max = 20
        training_mob.db.element = "physical"
        training_mob.db.crit_chance = 0.0
        training_mob.db.rarity = "normal"
        training_mob.db.resistances = {}
        training_mob.ndb.hp = 100
        training_mob.ndb.active_effects = []
        self.char1.ndb.hp = 100
        self.char1.ndb.active_effects = []
        with patch(
            "world.zone_scaling.get_mob_damage_for_player",
            return_value=(20, 20),
        ), patch("world.combat_engine.random.randint", return_value=20):
            hit, _message, mitigated_damage = resolve_basic_attack(
                training_mob,
                self.char1,
            )
        self.assertTrue(hit)
        self.assertEqual(mitigated_damage, apply_armor_mitigation(20, armor))
        training_mob.delete()

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

        # An authored Ashreach pool supplies ore that is processed and forged
        # at Vael's real forge, then used in the next combat.
        ashreach_zone = next(
            obj
            for obj in search_objects_by_exact_tag("ashreach_plains", "zone_id")
            if obj.tags.get("zone_object", category="object_type")
        )
        ore_pool = next(
            pool
            for pool in (ashreach_zone.db.gathering_pools or [])
            if "iron_ore" in pool["materials"]
        )
        self._walk_to(self._room(ore_pool["room_ids"][0]))
        ore_node = create_object(
            GatheringNode,
            key="Exposed Iron Seam",
            location=self.char1.location,
        )
        ore_node.db.node_type = "ore"
        ore_node.db.material_id = "iron_ore"
        ore_node.db.gathers_remaining = 6
        ore_node.db.tier = 1
        ore_node.db.zone_id = "ashreach_plains"
        ore_node.db.absorbed_property = "hardite"
        ore_node.db.profession_bonus = {"mining": 0.05, "smithing": 0.10}
        pickaxe = create_item_from_catalog("pickaxe", location=self.char1)
        gathered = []
        for _ in range(6):
            ok, message, items, broken = complete_gather(
                self.char1,
                ore_node,
                pickaxe,
                "mining",
                0,
            )
            self.assertTrue(ok, message)
            self.assertFalse(broken)
            gathered.extend(items)
        self.assertEqual(len(gathered), 6)
        self.assertTrue(all(item.db.material_id == "iron_ore" for item in gathered))

        self._walk_to(self._room("mk_forge"))
        self.assertTrue(
            self.char1.location.tags.has(
                "crafting_forge",
                category="crafting_station",
            )
        )
        for index in range(2):
            ok, message = craft_item(
                self.char1,
                "iron_ingot",
                operation_id=f"golden:iron-ingot:{index}",
            )
            self.assertTrue(ok, message)
        ok, message = craft_item(
            self.char1,
            "iron_dagger",
            operation_id="golden:iron-dagger",
        )
        self.assertTrue(ok, message)
        crafted_dagger = next(
            item
            for item in self.char1.contents
            if item.db.crafted_recipe_id == "iron_dagger"
        )
        current_weapon = next(
            item
            for item, record in get_equipped_items(self.char1)
            if record.equipment_slot == "main_hand"
        )
        unequipped, unequip_message = unequip_item(self.char1, current_weapon)
        self.assertTrue(unequipped, unequip_message)
        equipped, equip_message = equip_item(self.char1, crafted_dagger)
        self.assertTrue(equipped, equip_message)

        # A nearby ally receives independent credit and loot from the same
        # persisted death snapshot, while the crafted dagger is truly used.
        self.char2.location = self.char1.location
        ally_ancestry_set, ally_ancestry_message = set_ancestry(
            self.char2,
            "human",
        )
        self.assertTrue(ally_ancestry_set, ally_ancestry_message)
        self.char1.ndb.presence_nonce = "golden-leader-online"
        self.char2.ndb.presence_nonce = "golden-ally-online"
        invited, invite_message = send_group_invite(self.char1, self.char2)
        self.assertTrue(invited, invite_message)
        joined, join_message = accept_group_invite(self.char2)
        self.assertTrue(joined, join_message)
        init_session_accumulators(self.char2)

        named_mob = create_object(
            SoravelonMob,
            key="Ash-Marked Prowler",
            location=self.char1.location,
        )
        named_mob.db.base_stats = None
        named_mob.db.ref_damage_min = 1
        named_mob.db.ref_damage_max = 1
        named_mob.db.element = "physical"
        named_mob.db.crit_chance = 0.0
        named_mob.db.rarity = "normal"
        named_mob.db.resistances = {}
        named_mob.db.mob_type = "ash_marked_prowler"
        named_mob.db.mob_template_key = "ash_marked_prowler"
        named_mob.db.named_id = "golden_ash_marked_prowler"
        named_mob.db.personal_scales = 5
        named_mob.tags.add(
            "golden_ash_marked_prowler",
            category=MOB_INSTANCE_TAG_CATEGORY,
        )
        named_mob.ndb.hp = 1
        named_mob.ndb.active_effects = []
        named_mob.ndb.combat_handler = SimpleNamespace(
            get_player_combatants=lambda: [self.char1, self.char2]
        )
        attacked, _attack_message, damage = resolve_basic_attack(
            self.char1,
            named_mob,
            weapon=crafted_dagger,
        )
        self.assertTrue(attacked)
        self.assertGreaterEqual(damage, 1)

        def personal_drop(_mob, recipient):
            return [
                {
                    "item_id": f"golden_trophy_{recipient.id}",
                    "key": f"Trophy for {recipient.key}",
                    "item_type": "item",
                    "weight": 0.1,
                    "value": 1,
                    "loot_scope": "personal",
                }
            ]

        with patch("world.loot_tables.roll_loot", side_effect=personal_drop):
            handle_mob_death(named_mob, self.char1)

        leader_reward = EncounterReward.objects.get(character=self.char1)
        ally_reward = EncounterReward.objects.get(character=self.char2)
        self.assertEqual(leader_reward.corpse_id, ally_reward.corpse_id)
        leader_claim = claim_personal_rewards(
            self.char1,
            corpse_id=leader_reward.corpse_id,
        )
        ally_claim = claim_personal_rewards(
            self.char2,
            corpse_id=ally_reward.corpse_id,
        )
        self.assertEqual(leader_claim["claimed"], 1)
        self.assertEqual(ally_claim["claimed"], 1)
        self.assertNotEqual(leader_claim["items"], ally_claim["items"])

        commit_session_xp(self.char1)
        commit_session_xp(self.char2)
        combat_events = ProgressionEvent.objects.filter(
            source_id="golden_ash_marked_prowler",
            event_type="combat_outcome",
        )
        self.assertEqual(combat_events.count(), 2)
        self.assertTrue(
            all(event.domain_awards == {"combat": 25} for event in combat_events)
        )
        self.assertGreater(self.char1.db.domain_scores["combat"], 0)
        self.assertGreater(self.char2.db.domain_scores["combat"], 0)

        # The authored Warden delivery uses conversation and real walking,
        # then changes standing and propagates a claim between NPCs.
        calloway = next(
            npc
            for npc in search_objects_by_exact_tag(
                "npc_warden_agent_calloway",
                "npc_id",
            )
            if npc.db.zone_id == "vaels_crossing"
        )
        harven = next(
            npc
            for npc in search_objects_by_exact_tag(
                "npc_warden_outpost_commander",
                "npc_id",
            )
            if npc.db.zone_id == "ashreach_plains"
        )
        self._walk_to(calloway.location)
        with patch.object(self.char1, "msg"), patch(
            "world.oob_publisher.push_quest_update"
        ):
            talk = CmdTalk()
            talk.caller = self.char1
            talk.args = "Calloway"
            talk.func()
            self.assertEqual(
                self.char1.ndb.pending_quest_offer["quest"]["quest_id"],
                "vc_q_warden_report",
            )
            accept = CmdAccept()
            accept.caller = self.char1
            accept.args = ""
            accept.func()

            self._walk_to(harven.location)
            deliver = CmdTalk()
            deliver.caller = self.char1
            deliver.args = "Harven"
            deliver.func()

        warden_quest = CharacterQuest.objects.get(
            character=self.char1,
            quest_id="vc_q_warden_report",
        )
        self.assertEqual(warden_quest.status, "complete")
        self.assertEqual(
            FactionStanding.objects.get(
                character=self.char1,
                faction_id="wardens",
            ).standing,
            20_000,
        )
        delivered_fact_key = (
            f"fact:{self.char1.id}:vc_q_warden_report:delivered"
        )
        delivered_claim_key = (
            f"claim:calloway:{self.char1.id}:vc_q_warden_report:delivered"
        )
        self.assertTrue(SocialFact.objects.filter(fact_key=delivered_fact_key).exists())
        self.assertTrue(
            SocialClaim.objects.filter(claim_key=delivered_claim_key).exists()
        )
        self.assertEqual(
            set(
                SocialKnowledge.objects.filter(
                    claim__claim_key=delivered_claim_key
                ).values_list("node__node_key", flat=True)
            ),
            {
                "npc:npc_warden_agent_calloway",
                "npc:npc_warden_outpost_commander",
            },
        )

        # A separate local rumor can be answered without deleting its source.
        whistle = next(
            npc
            for npc in search_objects_by_exact_tag(
                "npc_innkeeper_whistle",
                "npc_id",
            )
            if npc.db.zone_id == "vaels_crossing"
        )
        self._walk_to(whistle.location)
        player_node = ensure_social_node(
            "player",
            str(self.char1.id),
            display_name=self.char1.key,
        )
        whistle_node = ensure_social_node(
            "npc",
            "npc_innkeeper_whistle",
            display_name=whistle.key,
            zone_id="vaels_crossing",
        )
        witness = ensure_social_node(
            "npc",
            "npc_debt_collector_raith",
            display_name="Raith",
            zone_id="vaels_crossing",
        )
        fact_ok, fact_message, rumor_fact = record_social_fact(
            fact_key=f"fact:golden:market:{self.char1.id}",
            subject_node_key=player_node.node_key,
            actor_node_key=witness.node_key,
            event_type="rumor_seeded",
            summary="Raith says the traveler lingered near a broken market lock.",
            tags=["market", "rumor"],
            visibility="local",
        )
        self.assertTrue(fact_ok, fact_message)
        claim_ok, claim_message, rumor = assert_social_claim(
            claim_key=f"claim:golden:market:{self.char1.id}",
            speaker_node_key=witness.node_key,
            subject_node_key=player_node.node_key,
            fact_key=rumor_fact.fact_key,
            claim_type="rumor",
            summary="Raith says the traveler was near a broken market lock.",
            status="rumor",
            confidence=0.45,
        )
        self.assertTrue(claim_ok, claim_message)
        known_ok, known_message, _knowledge = mark_known(
            node_key=whistle_node.node_key,
            claim_key=rumor.claim_key,
            source_node_key=witness.node_key,
            channel="tavern_rumor",
            confidence=0.45,
            spreading=False,
        )
        self.assertTrue(known_ok, known_message)
        repair = deny_social_claim(self.char1, whistle, topic_text="me")
        self.assertTrue(repair.ok, repair.message)
        self.assertEqual(repair.answered_claim_key, rumor.claim_key)
        rumor.refresh_from_db()
        self.assertEqual(rumor.status, "rumor")
        self.assertTrue(
            SocialKnowledge.objects.filter(
                node=whistle_node,
                claim=repair.claim,
                channel="direct_witness",
            ).exists()
        )

        # Finally, actual node state responds to pressure and a player's
        # stamina-backed stabilization attempt.
        node_zone = create_object(Object, key="Golden Path Node Zone")
        node_zone.db.zone_id = "golden_path_node"
        node_zone.tags.add("zone_object", category="object_type")
        node_room = create_object(SoravelonRoom, key="Shivering Stone Ring")
        node_room.db.zone_id = "golden_path_node"
        node_room.tags.add("golden_path_node", category="zone_id")
        node_script = initialize_node(
            node_zone,
            "resonance",
            node_room,
            0,
            [node_room],
            failure_start=29,
        )
        node_script.receive_tick(
            player_count=10,
            scholar_count=0,
            stabilizer_count=0,
        )
        self.assertEqual(node_script.db.state, "awakening")
        pressured_failure = node_script.db.failure
        self.char1.location = node_room
        self.char1.ndb.stamina = 20
        self.assertTrue(attempt_stabilization(self.char1, "golden_path_node"))
        node_script.receive_tick(
            player_count=0,
            scholar_count=0,
            stabilizer_count=1,
        )
        stabilization_tick(self.char1, "golden_path_node")
        self.assertLess(node_script.db.failure, pressured_failure)
        self.assertEqual(self.char1.ndb.stamina, 15)
