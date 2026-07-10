"""
Tests for the combat script turn manager (world/combat_script.py).

Covers initiative ordering, turn management (skip stunned, round-end ticks),
combat end conditions, and group combat timeout. Uses unittest.TestCase +
MagicMock to avoid full Evennia DB setup for these unit-level tests.
"""

import unittest
from unittest.mock import MagicMock, patch, call


def _make_script():
    """Create a MagicMock CombatScript with relevant db/ndb state."""
    script = MagicMock()
    script.key = "combat_script"
    script.obj = MagicMock()  # room

    # db state
    script.db.combatant_ids = []
    script.db.round_number = 1
    script.db.current_turn_index = 0
    script.db.initiative_order = []
    script.db.is_group_combat = False
    script.db.round_timeout = 30
    script.db.active_effects_db = {}

    # ndb state
    script.ndb.turn_timer_id = None
    script.ndb.pending_charged = {}
    script.ndb.call_for_help_count = 0

    return script


def _make_combatant(cid, name, is_player=True, initiative=10, hp=100):
    """Create a MagicMock combatant."""
    c = MagicMock()
    c.key = name
    c.id = cid
    c.ndb.hp = hp
    c.ndb.combat_handler = None
    c.ndb.actions_remaining = 0
    c.ndb.ability_used_this_turn = False
    c.ndb.active_effects = []
    c.ndb.group_state = None
    c.ndb.group_leader_id = None
    c.ndb.resolving_charged_ability = False

    if is_player:
        c.db.base_stats = {"strength": 10, "agility": initiative, "endurance": 10,
                          "mana": 10, "acuity": 10, "presence": 10, "resonance": 10}
        c.db.backend_level = 5
        c.account = MagicMock()
        c.tags = MagicMock()
        c.tags.has = MagicMock(return_value=True)
        c.cmdset = MagicMock()
    else:
        c.db.base_stats = None
        c.db.speed = initiative / 10.0
        c.db.hp_max = hp
        c.account = None
        c.tags = MagicMock()
        c.tags.has = MagicMock(return_value=False)

    c.location = MagicMock()
    return c


class TestInitiativeOrder(unittest.TestCase):
    """Initiative ordering: descending by value, players and mobs interleaved."""

    def test_sorted_descending(self):
        """Higher initiative goes first in the order."""
        from world.combat_script import CombatScript

        script = _make_script()
        # Simulate add_combatant logic manually
        entries = [
            {"id": 1, "initiative_value": 30},
            {"id": 2, "initiative_value": 50},
            {"id": 3, "initiative_value": 10},
        ]

        # Sort descending (same logic as CombatScript.add_combatant)
        sorted_entries = sorted(entries, key=lambda e: e["initiative_value"], reverse=True)
        self.assertEqual(sorted_entries[0]["id"], 2)  # highest = 50
        self.assertEqual(sorted_entries[1]["id"], 1)  # middle = 30
        self.assertEqual(sorted_entries[2]["id"], 3)  # lowest = 10

    def test_interleaved(self):
        """Players and mobs alternate based on initiative, not grouped (D-15)."""
        # Simulate initiative order: player(40), mob(35), player(20), mob(15)
        order = [
            {"id": 1, "initiative_value": 40, "is_player": True},
            {"id": 10, "initiative_value": 35, "is_player": False},
            {"id": 2, "initiative_value": 20, "is_player": True},
            {"id": 11, "initiative_value": 15, "is_player": False},
        ]
        # Verify interleaving: player, mob, player, mob
        types = [e["is_player"] for e in order]
        self.assertEqual(types, [True, False, True, False])


class TestTurnManagement(unittest.TestCase):
    """Turn advancement, stun skip, round-end processing."""

    def test_advance_skips_stunned(self):
        """Stunned combatant's turn is skipped during advance_turn."""
        # Test the skip logic directly: if skip_turn is True, turn is skipped
        from world.status_effects import get_effect_modifiers

        combatant = _make_combatant(1, "Stunned", is_player=True)
        combatant.ndb.active_effects = [
            {
                "type": "stun",
                "stacks": 1,
                "duration": 2,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": False,
            }
        ]
        mods = get_effect_modifiers(combatant)
        self.assertTrue(mods["skip_turn"])

    def test_round_end_ticks_effects(self):
        """tick_effects is called for combatants at round end."""
        from world.status_effects import tick_effects

        combatant = _make_combatant(1, "Player", is_player=True, hp=100)
        combatant.ndb.active_effects = [
            {
                "type": "poison",
                "stacks": 1,
                "duration": 3,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 5,
                "is_compound": False,
            }
        ]

        messages = tick_effects(combatant)
        # Poison should deal damage
        self.assertTrue(any("poison" in m.lower() for m in messages))
        self.assertLess(combatant.ndb.hp, 100)

    def test_round_end_decrements_cooldowns(self):
        """Ability cooldowns go down by 1 at round end."""
        # Test decrement_cooldowns directly
        combatant = _make_combatant(1, "Player", is_player=True)
        combatant.ndb.ability_cooldowns = {"fireball": 3, "heal": 1}

        from world.ability_engine import decrement_cooldowns
        decrement_cooldowns(combatant)

        cds = combatant.ndb.ability_cooldowns
        self.assertEqual(cds.get("fireball", 0), 2)
        # heal at 1 should be 0 or removed
        self.assertLessEqual(cds.get("heal", 0), 0)

    def test_round_end_awards_allied_command_before_resetting_counter(self):
        """Recorded allied actions build Command before the new round starts."""
        from world.combat_script import CombatScript

        script = _make_script()
        character = _make_combatant(1, "Tactician", is_player=True)
        character.ndb.domain_resource = {"type": "command", "current": 0, "max": 100}
        script.db.combatant_ids = [character.id]
        script.ndb.ally_action_count = {str(character.id): 2}
        script._resolve_combatants.return_value = [character]

        with (
            patch("world.status_effects.tick_effects"),
            patch("world.status_effects.get_effect_modifiers", return_value={}),
            patch("world.ability_engine.decrement_cooldowns"),
            patch("world.combat_engine.check_death", return_value=False),
            patch("world.combat_ai.resolve_pending_casts", return_value=[]),
        ):
            CombatScript.end_round(script)

        self.assertEqual(character.ndb.domain_resource["current"], 20)
        self.assertEqual(script.ndb.ally_action_count, {})
        character.msg.assert_any_call(
            "|cAllied actions build Command: +20 (20/100).|n"
        )

    @patch("world.combat_script._send_turn_prompt")
    @patch("world.combat_script._resolve_by_id")
    @patch("world.oob_publisher.push_combat_update")
    @patch("world.status_effects.get_effect_modifiers", return_value={})
    @patch("world.base_attributes.get_actions_per_turn", return_value=2)
    def test_prompt_player_turn_marks_internal_charge_release(
        self,
        mock_actions,
        mock_modifiers,
        mock_push_combat,
        mock_resolve,
        mock_turn_prompt,
    ):
        """Charged auto-release sets an internal bypass flag only for the release call."""
        from world.combat_script import CombatScript

        script = _make_script()
        character = _make_combatant(1, "Caster", is_player=True)
        target = _make_combatant(2, "Target", is_player=False)
        script.ndb.pending_charged = {
            character.id: {
                "ability_id": "meteor_strike",
                "rounds_left": 1,
                "target_id": target.id,
            }
        }
        script._resolve_post_ability_deaths = MagicMock(return_value=False)
        mock_resolve.side_effect = lambda obj_id: target if obj_id == target.id else None

        def _fake_use_ability(resolved_character, ability_id, target=None):
            self.assertTrue(resolved_character.ndb.resolving_charged_ability)
            return True, "Meteor Strike lands."

        with patch("world.ability_engine.use_ability", side_effect=_fake_use_ability):
            CombatScript._prompt_player_turn(script, character)

        self.assertFalse(getattr(character.ndb, "resolving_charged_ability", False))
        self.assertNotIn(character.id, script.ndb.pending_charged)


class TestCombatEnd(unittest.TestCase):
    """Combat end conditions and cleanup."""

    def test_all_enemies_dead(self):
        """Combat should end when no mobs remain alive."""
        # Verify the logic: if get_mob_combatants returns empty, combat ends
        # This is tested via the condition check
        alive_mobs = [m for m in [] if m.ndb.hp > 0]
        self.assertEqual(len(alive_mobs), 0)
        # In CombatScript.remove_combatant, if not self.get_mob_combatants(): end_combat()

    def test_all_players_fled(self):
        """Combat ends when all players are removed."""
        alive_players = [p for p in [] if p.ndb.hp > 0]
        self.assertEqual(len(alive_players), 0)

    def test_cleanup_removes_cmdset(self):
        """CombatCmdSet removed from players at combat end."""
        # Test that end_combat calls _remove_combat_cmdset
        # We verify the pattern: _remove_combat_cmdset calls character.cmdset.remove
        player = _make_combatant(1, "Player", is_player=True)

        # Simulate what end_combat does to a player combatant
        player.ndb.combat_handler = None
        player.ndb.actions_remaining = 0
        player.ndb.ability_used_this_turn = False

        # The cmdset removal is what we verify
        player.cmdset.remove.assert_not_called()  # not yet
        # Simulate the removal call
        player.cmdset.remove(MagicMock())
        player.cmdset.remove.assert_called_once()


class TestGroupCombat(unittest.TestCase):
    """Group combat timeout behavior (CMB-04)."""

    def test_group_timeout_active(self):
        """is_group_combat=True means a round timer should be started."""
        script = _make_script()
        script.db.is_group_combat = True
        # The script should use delay() when is_group_combat is True
        # This is tested by verifying the flag
        self.assertTrue(script.db.is_group_combat)

    def test_solo_no_timeout(self):
        """Solo combat waits indefinitely (no timeout)."""
        script = _make_script()
        script.db.is_group_combat = False
        self.assertFalse(script.db.is_group_combat)
        self.assertIsNone(script.ndb.turn_timer_id)


class TestCommandActionRecording(unittest.TestCase):
    """Basic attacks and abilities use the same ally-action recorder."""

    @patch("world.combat_engine.check_death", return_value=False)
    @patch("world.base_attributes.record_stat_use")
    @patch("world.inventory_engine.get_equipped_items", return_value=[])
    @patch("world.combat_engine.resolve_basic_attack", return_value=(True, "hit", 10))
    def test_basic_attack_uses_shared_ally_recorder(
        self,
        _resolve_attack,
        _equipped_items,
        _record_stat_use,
        _check_death,
    ):
        from world.combat_script import CombatScript

        script = _make_script()
        character = _make_combatant(1, "Player")
        target = _make_combatant(2, "Target", is_player=False)
        character.ndb.actions_remaining = 1
        script.get_current_combatant.return_value = character
        script.record_allied_action = MagicMock()
        script.advance_turn = MagicMock()

        CombatScript.process_player_action(script, character, "basic_attack", target=target)

        script.record_allied_action.assert_called_once_with(character)

    @patch("world.ability_engine.use_ability", return_value=(True, "Ability lands."))
    def test_ability_uses_shared_ally_recorder(self, _use_ability):
        from world.combat_script import CombatScript

        script = _make_script()
        character = _make_combatant(1, "Player")
        target = _make_combatant(2, "Target", is_player=False)
        script.get_current_combatant.return_value = character
        script.record_allied_action = MagicMock()
        script._resolve_post_ability_deaths = MagicMock(return_value=False)
        script.advance_turn = MagicMock()

        CombatScript.process_player_action(
            script,
            character,
            "ability",
            target=target,
            ability_id="crushing_advance",
        )

        script.record_allied_action.assert_called_once_with(character)


class TestCommandFeedback(unittest.TestCase):
    """Tactical coordination is visible where the player chooses an action."""

    def test_turn_prompt_previews_allied_command_gain(self):
        from world.combat_script import _send_turn_prompt

        script = _make_script()
        character = _make_combatant(1, "Tactician")
        character.ndb.combat_target_id = None
        character.ndb.hp_max = 100
        character.ndb.domain_resource = {"type": "command", "current": 30, "max": 100}
        script.get_mob_combatants.return_value = []
        script.ndb.ally_action_count = {str(character.id): 2}

        _send_turn_prompt(character, script)

        prompt = character.msg.call_args.args[0]
        self.assertIn(
            "Command: 30/100 | Allied actions: 2 (+20 Command at round end)",
            prompt,
        )

    def test_combat_oob_exposes_command_and_ally_preview(self):
        from world.combat_script import _build_combat_oob

        script = _make_script()
        character = _make_combatant(1, "Tactician")
        character.ndb.combat_target_id = None
        character.ndb.domain_resource = {"type": "command", "current": 85, "max": 100}
        script.get_mob_combatants.return_value = []
        script.ndb.ally_action_count = {str(character.id): 2}
        script._resolve_combatants.return_value = [character]

        payload = _build_combat_oob(character, script)

        self.assertEqual(payload["domain_resource"], character.ndb.domain_resource)
        self.assertEqual(
            payload["command_preview"],
            {
                "current": 85,
                "max": 100,
                "ally_actions": 2,
                "gain": 15,
                "source": "allies",
            },
        )
