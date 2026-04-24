"""Tests for reconnect/login/logout lifecycle orchestration."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


def _make_character(guild_id=None, ancestry="human", backend_level=1):
    char = MagicMock()
    char.id = 7
    char.key = "LifecycleTester"
    char.db = SimpleNamespace(
        ancestry=ancestry,
        backend_level=backend_level,
        guild_id=guild_id,
        remnance_discovered=False,
    )
    char.ndb = SimpleNamespace()
    char._send_new_player_guidance = None
    char.scripts.get.return_value = [MagicMock()]
    char.msg = MagicMock()
    return char


class TestSessionLifecycle(unittest.TestCase):
    """Regression coverage for reconnect and combat-preservation behavior."""

    @patch("world.oob_publisher.push_inventory_update")
    @patch("world.oob_publisher.push_map_update")
    @patch("world.oob_publisher.push_stat_update")
    @patch("world.oob_publisher.push_status_update")
    @patch("world.ability_engine.sync_character_ability_unlocks")
    @patch("world.recovery_engine.start_regen")
    @patch("world.base_attributes.derive_max_stamina", return_value=80)
    @patch("world.base_attributes.derive_max_hp", return_value=120)
    @patch("world.world_state.init_session_accumulators")
    def test_on_login_initializes_missing_runtime_state(
        self,
        mock_init_session,
        mock_hp,
        mock_stamina,
        mock_start_regen,
        mock_sync_unlocks,
        mock_push_status,
        mock_push_stat,
        mock_push_map,
        mock_push_inventory,
    ):
        from world.session_lifecycle import on_login

        char = _make_character()

        on_login(char)

        self.assertIsNone(char.ndb.combat_handler)
        self.assertEqual(char.ndb.active_effects, [])
        self.assertEqual(char.ndb.hp, 120)
        self.assertEqual(char.ndb.stamina, 80)
        self.assertEqual(char.ndb.ability_cooldowns, {})
        self.assertFalse(char.ndb.ability_used_this_turn)
        self.assertEqual(char.ndb.oob_debounce, {})
        self.assertIsInstance(char.ndb.presence_nonce, str)
        mock_sync_unlocks.assert_called_once_with(char)
        mock_start_regen.assert_called_once_with(char)
        mock_push_status.assert_called_once_with(char)
        mock_push_stat.assert_called_once_with(char)
        mock_push_map.assert_called_once_with(char)
        mock_push_inventory.assert_called_once_with(char)

    @patch("world.oob_publisher.push_combat_update")
    @patch("world.combat_script._build_combat_oob", return_value={"round": 4})
    @patch("world.combat_script._send_turn_prompt")
    @patch("world.combat_script._add_combat_cmdset")
    @patch("world.ability_engine.initialize_domain_resource")
    @patch("world.oob_publisher.push_inventory_update")
    @patch("world.oob_publisher.push_map_update")
    @patch("world.oob_publisher.push_stat_update")
    @patch("world.oob_publisher.push_status_update")
    @patch("world.ability_engine.sync_character_ability_unlocks")
    @patch("world.recovery_engine.start_regen")
    @patch("world.base_attributes.derive_max_stamina", return_value=80)
    @patch("world.base_attributes.derive_max_hp", return_value=120)
    @patch("world.world_state.init_session_accumulators")
    def test_on_login_preserves_runtime_state_and_rejoins_active_combat(
        self,
        mock_init_session,
        mock_hp,
        mock_stamina,
        mock_start_regen,
        mock_sync_unlocks,
        mock_push_status,
        mock_push_stat,
        mock_push_map,
        mock_push_inventory,
        mock_init_resource,
        mock_add_cmdset,
        mock_turn_prompt,
        mock_build_oob,
        mock_push_combat,
    ):
        from world.session_lifecycle import on_login

        char = _make_character(guild_id="circle")
        handler = MagicMock()
        handler.is_combatant.return_value = True
        handler.get_current_combatant.return_value = char

        char.ndb.combat_handler = handler
        char.ndb.combat_target_id = 99
        char.ndb.active_effects = [{"type": "poison", "duration": 2}]
        char.ndb.actions_remaining = 2
        char.ndb.ability_used_this_turn = True
        char.ndb.hp = 33
        char.ndb.stamina = 12
        char.ndb.charged_ability = "storm_lance"
        char.ndb.ability_cooldowns = {"storm_lance": 3}
        char.ndb.ancestry_ability_used = True
        char.ndb.domain_resource = {"type": "mana", "current": 14, "max": 40}
        char.ndb.oob_debounce = {"map_update": 123.0}

        on_login(char)

        self.assertIs(char.ndb.combat_handler, handler)
        self.assertEqual(char.ndb.combat_target_id, 99)
        self.assertEqual(char.ndb.active_effects, [{"type": "poison", "duration": 2}])
        self.assertEqual(char.ndb.actions_remaining, 2)
        self.assertTrue(char.ndb.ability_used_this_turn)
        self.assertEqual(char.ndb.hp, 33)
        self.assertEqual(char.ndb.stamina, 12)
        self.assertEqual(char.ndb.charged_ability, "storm_lance")
        self.assertEqual(char.ndb.ability_cooldowns, {"storm_lance": 3})
        self.assertTrue(char.ndb.ancestry_ability_used)
        self.assertEqual(char.ndb.domain_resource["current"], 14)
        self.assertEqual(char.ndb.oob_debounce, {})
        self.assertIsInstance(char.ndb.presence_nonce, str)
        mock_sync_unlocks.assert_called_once_with(char)
        mock_init_resource.assert_not_called()
        mock_add_cmdset.assert_called_once_with(char)
        mock_turn_prompt.assert_called_once_with(char, handler)
        mock_push_combat.assert_called_once_with(char, {"round": 4})

    @patch("world.recovery_engine.stop_regen")
    @patch("world.group_engine.on_member_disconnect")
    @patch("world.skill_engine.commit_skill_accumulators")
    @patch("world.world_state.commit_session_xp")
    @patch("world.base_attributes.commit_stat_growth")
    def test_on_logout_preserves_active_combat_state(
        self,
        mock_commit_stats,
        mock_commit_xp,
        mock_commit_skills,
        mock_group_disconnect,
        mock_stop_regen,
    ):
        from world.session_lifecycle import on_logout

        char = _make_character()
        handler = MagicMock()
        handler.is_combatant.return_value = True
        handler.db = SimpleNamespace(active_effects_db={})
        char.ndb.combat_handler = handler
        char.ndb.active_effects = [{"type": "poison", "duration": 2}]

        on_logout(char)

        handler.remove_combatant.assert_not_called()
        self.assertIs(char.ndb.combat_handler, handler)
        self.assertIsNone(char.ndb.presence_nonce)
        self.assertEqual(
            handler.db.active_effects_db["7"],
            [{"type": "poison", "duration": 2}],
        )
        mock_stop_regen.assert_called_once_with(char)

    def test_guidance_prompts_for_missing_ancestry(self):
        from world.session_lifecycle import get_new_player_guidance

        char = _make_character(ancestry=None)

        guidance = get_new_player_guidance(char)

        self.assertIn("choose an ancestry", guidance.lower())
        self.assertIn("ancestry", guidance.lower())

    @patch("world.guild_engine.check_guild_eligibility", return_value=["ironblood"])
    @patch("world.guild_engine.GUILDS", {"ironblood": {"name": "Ironblood"}})
    def test_guidance_points_eligible_guildless_character_to_joinguild(
        self,
        mock_guild_eligibility,
    ):
        from world.session_lifecycle import get_new_player_guidance

        char = _make_character(guild_id=None)

        guidance = get_new_player_guidance(char)

        self.assertIn("joinguild", guidance.lower())
        self.assertIn("secondary_domain", guidance.lower())

    @patch("world.quest_engine.get_active_quests", return_value=[])
    def test_guidance_points_low_level_guild_member_toward_quests(
        self,
        mock_get_active_quests,
    ):
        from world.session_lifecycle import get_new_player_guidance

        char = _make_character(guild_id="circle", backend_level=2)

        guidance = get_new_player_guidance(char)

        self.assertIn("talk", guidance.lower())
        self.assertIn("quest", guidance.lower())

    @patch("world.quest_engine.get_active_quests", return_value=[])
    def test_guidance_is_suppressed_for_established_characters(
        self,
        mock_get_active_quests,
    ):
        from world.session_lifecycle import get_new_player_guidance

        char = _make_character(guild_id="circle", backend_level=9)

        self.assertIsNone(get_new_player_guidance(char))
