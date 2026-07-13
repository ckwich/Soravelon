"""
Tests for combat system fixes:
- Ability handler return normalization (bool, str) tuples
- Compound status effect burst damage (steam/discharge)
- Petrify break-on-damage via took_damage_this_round flag
- Corpse loot command and group loot distribution
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch, PropertyMock


# ---------------------------------------------------------------------------
# Minimal Django/Evennia stubs so we can import world modules in pure tests
# ---------------------------------------------------------------------------

def _ensure_stubs():
    """Inject minimal stubs for Django and Evennia if not already available."""
    needed = [
        "django", "django.conf", "django.db", "django.db.models",
        "django.db.models.functions", "django.core",
        "django.core.exceptions",
        "evennia", "evennia.utils", "evennia.utils.search",
        "evennia.utils.utils", "evennia.utils.delay",
        "evennia.utils.logger",
        "evennia.commands", "evennia.commands.command",
        "evennia.commands.cmdset",
    ]
    for mod_name in needed:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = types.ModuleType(mod_name)

    # django.conf.settings
    settings_mod = sys.modules["django.conf"]
    if not hasattr(settings_mod, "settings"):
        settings_mod.settings = MagicMock()

    # django.db.models needs F and field types
    models_mod = sys.modules["django.db.models"]
    if not hasattr(models_mod, "F"):
        models_mod.F = MagicMock()
    if not hasattr(models_mod, "Model"):
        class _FakeModel:
            class Meta:
                app_label = "world"
        models_mod.Model = _FakeModel
    # Field stubs
    for field in [
        "ForeignKey", "OneToOneField", "ManyToManyField",
        "CharField", "IntegerField", "FloatField",
        "BooleanField", "TextField", "DateTimeField", "JSONField",
        "BigIntegerField", "PositiveIntegerField", "DecimalField",
        "SmallIntegerField", "SlugField", "EmailField",
        "UniqueConstraint", "Index", "Manager", "QuerySet",
    ]:
        if not hasattr(models_mod, field):
            setattr(models_mod, field, MagicMock())
    if not hasattr(models_mod, "CASCADE"):
        models_mod.CASCADE = "CASCADE"
    if not hasattr(models_mod, "SET_NULL"):
        models_mod.SET_NULL = "SET_NULL"

    # evennia stubs
    ev = sys.modules["evennia"]
    if not hasattr(ev, "search_object"):
        ev.search_object = MagicMock(return_value=[])
    if not hasattr(ev, "create_object"):
        ev.create_object = MagicMock()

    # evennia.commands.command needs a Command base class
    ev_cmd = sys.modules["evennia.commands.command"]
    if not hasattr(ev_cmd, "Command"):
        class _FakeCommand:
            key = ""
            locks = ""
            help_category = ""
            args = ""
            caller = None
            def msg(self, *a, **kw): pass
        ev_cmd.Command = _FakeCommand

    # Stub evennia.objects for typeclasses.objects import chain
    for mod_name in [
        "evennia.objects", "evennia.objects.objects",
        "evennia.typeclasses", "evennia.typeclasses.models",
        "evennia.typeclasses.attributes",
        "evennia.typeclasses.tags",
        "evennia.locks", "evennia.locks.lockhandler",
    ]:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = types.ModuleType(mod_name)

    ev_utils = sys.modules["evennia.utils"]
    if not hasattr(ev_utils, "delay"):
        ev_utils.delay = MagicMock()
    if not hasattr(ev_utils, "logger"):
        ev_utils.logger = MagicMock()


_ensure_stubs()


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------

class _NDB:
    """Simple namespace that acts like Evennia's ndb."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def _make_character(name="TestChar", **ndb_kwargs):
    char = MagicMock()
    char.key = name
    char.id = id(char)
    # Ensure essential ndb attributes are always present
    defaults = {
        "active_effects": [],
        "took_damage_this_round": False,
        "domain_resource": {},
        "cooldowns": {},
        "combat_handler": None,
        "hp": 100,
        "stamina": 50,
        "ability_cooldowns": {},
    }
    defaults.update(ndb_kwargs)
    char.ndb = _NDB(**defaults)
    char.db = MagicMock()
    char.db.base_stats = {"strength": 10, "agility": 10, "acuity": 10,
                           "resonance": 10, "mana": 10, "presence": 10,
                           "endurance": 10}
    char.db.guild_id = None
    char.db.immunities = []
    char.location = MagicMock()
    char.location.tags = MagicMock()
    char.location.tags.has = MagicMock(return_value=False)
    return char


def _make_mob(name="TestMob", hp=100, **ndb_kwargs):
    mob = MagicMock()
    mob.key = name
    mob.id = id(mob)
    mob_defaults = {
        "hp": hp,
        "active_effects": [],
        "took_damage_this_round": False,
        "domain_resource": None,
        "cooldowns": {},
        "combat_handler": None,
        "stamina": 50,
    }
    mob_defaults.update(ndb_kwargs)
    mob.ndb = _NDB(**mob_defaults)
    mob.db = MagicMock()
    mob.db.base_stats = None
    mob.db.rarity = "normal"
    mob.db.immunities = []
    mob.db.ref_damage_min = 8
    mob.db.ref_damage_max = 14
    mob.db.crit_chance = 0.0
    mob.db.element = "physical"
    mob.location = MagicMock()
    return mob


# ===========================================================================
# Test Suite 1: Ability handler return normalization
# ===========================================================================

class TestAbilityHandlerReturns(unittest.TestCase):
    """Verify all 10 effect handlers return (bool, str) tuples."""

    def _call_handler(self, handler_name, ability_overrides=None):
        """Call a handler and return its result."""
        from world.ability_engine import EFFECT_HANDLERS
        handler = EFFECT_HANDLERS[handler_name]

        char = _make_character()
        target = _make_mob()
        ability = {
            "name": "Test Ability",
            "effect_type": handler_name,
            "damage_base": 10,
            "heal_base": 10,
            "status_effect": "poison",
            "buff_type": "haste",
            "debuff_type": "weaken",
            "effect_duration": 3,
            "effect_magnitude": 1.0,
            "scaling_primary": "combat",
            "application_chance": 1.0,
            "utility_action": None,
            "tactical_action": "self_buff",
        }
        if ability_overrides:
            ability.update(ability_overrides)
        return handler(char, ability, target)

    @patch("world.combat_engine.resolve_ability_damage",
           return_value=(True, "Hit for 10 damage.", 10))
    def test_handle_damage_returns_tuple(self, mock_resolve):
        result = self._call_handler("damage")
        self.assertIsInstance(result, tuple, "damage handler must return tuple")
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], str)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Poison applied."))
    def test_handle_dot_returns_tuple(self, mock_apply):
        result = self._call_handler("dot")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Haste applied."))
    def test_handle_buff_returns_tuple(self, mock_apply):
        result = self._call_handler("buff")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Weaken applied."))
    def test_handle_debuff_returns_tuple(self, mock_apply):
        result = self._call_handler("debuff")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Haste applied."))
    def test_handle_utility_returns_tuple(self, mock_apply):
        result = self._call_handler("utility")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Charm applied."))
    @patch("world.base_attributes.record_stat_use")
    def test_handle_social_returns_tuple(self, mock_record, mock_apply):
        result = self._call_handler("social")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Haste applied."))
    @patch("world.base_attributes.record_stat_use")
    def test_handle_tactical_returns_tuple(self, mock_record, mock_apply):
        result = self._call_handler("tactical")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.combat_engine.resolve_heal",
           return_value=(True, "Healed for 20.", 20))
    def test_handle_heal_returns_tuple(self, mock_heal):
        result = self._call_handler("heal")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Slow applied."))
    def test_handle_status_returns_tuple(self, mock_apply):
        result = self._call_handler("status")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("world.status_effects.apply_effect",
           return_value=(True, "Slow applied."))
    def test_handle_status_resisted_returns_tuple(self, mock_apply):
        """When application chance fails, still returns (bool, str)."""
        with patch("world.ability_engine.random") as mock_random:
            mock_random.random.return_value = 0.99  # > any chance < 1.0
            result = self._call_handler("status", {"application_chance": 0.5})
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertFalse(result[0])

    @patch("world.status_effects.check_compound_triggers",
           return_value=["steam"])
    def test_handle_compound_trigger_returns_tuple(self, mock_check):
        # Compound trigger handler is not in EFFECT_HANDLERS registry but
        # the function exists; call it directly to verify return contract.
        from world.ability_engine import _handle_compound_trigger
        char = _make_character()
        target = _make_mob()
        ability = {"name": "Test", "effect_type": "compound_trigger"}
        result = _handle_compound_trigger(char, ability, target)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)


class TestUseAbilityUnpacks(unittest.TestCase):
    """Verify use_ability correctly unpacks (ok, msg) from handler."""

    def test_ability_access_is_a_public_engine_contract(self):
        from world.ability_engine import check_ability_access

        char = _make_character()
        char.db.abilities = ["slash"]
        fake_registry = types.ModuleType("world.ability_registry")
        fake_registry.ABILITIES = {
            "slash": {"name": "Slash", "effect_type": "damage"},
        }

        with patch.dict(sys.modules, {"world.ability_registry": fake_registry}):
            self.assertEqual(check_ability_access(char, "slash"), (True, ""))

    @patch("world.ability_engine.check_ability_access",
           return_value=(True, ""))
    @patch("world.ability_engine._check_and_spend_resource",
           return_value=(True, ""))
    def test_use_ability_unpacks_tuple(self, mock_resource, mock_access):
        from world.ability_engine import use_ability

        char = _make_character()
        char.ndb.ability_cooldowns = {}
        target = _make_mob()

        slash_ability = {"name": "Slash", "effect_type": "damage"}

        # Stub the ability registry import inside use_ability
        fake_registry = types.ModuleType("world.ability_registry")
        fake_registry.ABILITIES = {"slash": slash_ability}

        fake_models = MagicMock()
        fake_models.CharacterAbility = MagicMock()
        fake_models.CharacterAbility.objects.filter.return_value.update = MagicMock()

        with patch.dict(sys.modules, {
            "world.ability_registry": fake_registry,
            "world.models": fake_models,
        }):
            with patch.dict(
                "world.ability_engine.EFFECT_HANDLERS",
                {"damage": MagicMock(return_value=(True, "Hit!"))},
            ):
                ok, msg = use_ability(char, "slash", target)
                self.assertTrue(ok)
                self.assertEqual(msg, "Hit!")


# ===========================================================================
# Test Suite 2: Compound status effect burst damage
# ===========================================================================

class TestCompoundBurstDamage(unittest.TestCase):
    """Test steam and discharge burst damage in tick_effects."""

    def test_steam_burst_damage(self):
        """Steam compound deals 15% max HP burst damage on first tick."""
        from world.status_effects import tick_effects

        target = _make_mob(hp=100)
        target.ndb.max_hp = 100
        target.ndb.active_effects = [{
            "type": "steam",
            "stacks": 1,
            "duration": 3,
            "initial_duration": 3,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]

        messages = tick_effects(target)
        # Should deal 15% of 100 = 15 damage
        self.assertEqual(target.ndb.hp, 85)
        self.assertTrue(any("Steam" in m or "steam" in m.lower() for m in messages))

    def test_discharge_burst_damage(self):
        """Discharge compound deals 20% max HP burst damage on first tick."""
        from world.status_effects import tick_effects

        target = _make_mob(hp=100)
        target.ndb.max_hp = 100
        target.ndb.active_effects = [{
            "type": "discharge",
            "stacks": 1,
            "duration": 3,
            "initial_duration": 3,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]

        messages = tick_effects(target)
        # Should deal 20% of 100 = 20 damage
        self.assertEqual(target.ndb.hp, 80)
        self.assertTrue(any("discharge" in m.lower() or "Discharge" in m for m in messages))

    def test_steam_no_burst_on_subsequent_tick(self):
        """Steam does not burst again after first tick."""
        from world.status_effects import tick_effects

        target = _make_mob(hp=100)
        target.ndb.max_hp = 100
        target.ndb.active_effects = [{
            "type": "steam",
            "stacks": 1,
            "duration": 2,  # Less than initial_duration
            "initial_duration": 3,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]

        tick_effects(target)
        # Should NOT deal burst damage on subsequent ticks
        self.assertEqual(target.ndb.hp, 100)


class TestPetrifyBreakOnDamage(unittest.TestCase):
    """Test petrify removal when target takes damage."""

    def test_petrify_breaks_on_damage(self):
        """Petrify removed when took_damage_this_round is True."""
        from world.status_effects import tick_effects

        target = _make_mob(hp=100)
        target.ndb.took_damage_this_round = True
        target.ndb.active_effects = [{
            "type": "petrify",
            "stacks": 1,
            "duration": 5,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]

        messages = tick_effects(target)
        # Petrify should be removed
        remaining_types = [e["type"] for e in target.ndb.active_effects]
        self.assertNotIn("petrify", remaining_types)
        self.assertTrue(any("shatter" in m.lower() or "Petrify" in m for m in messages))

    def test_petrify_persists_without_damage(self):
        """Petrify stays if no damage taken this round."""
        from world.status_effects import tick_effects

        target = _make_mob(hp=100)
        target.ndb.took_damage_this_round = False
        target.ndb.active_effects = [{
            "type": "petrify",
            "stacks": 1,
            "duration": 5,
            "magnitude": 1.0,
            "source_id": None,
            "max_stacks": 1,
            "is_compound": True,
        }]

        tick_effects(target)
        remaining_types = [e["type"] for e in target.ndb.active_effects]
        self.assertIn("petrify", remaining_types)


class TestTookDamageFlag(unittest.TestCase):
    """Test that combat damage resolution sets took_damage_this_round."""

    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, *a: d)
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, *a: d)
    @patch("world.base_attributes.record_stat_use")
    def test_took_damage_flag_set(self, mock_record, mock_resist, mock_scale):
        """resolve_ability_damage sets target.ndb.took_damage_this_round = True."""
        from world.combat_engine import resolve_ability_damage

        char = _make_character()
        target = _make_mob(hp=100)
        target.ndb.took_damage_this_round = False
        target.ndb.active_effects = []

        ability = {
            "name": "Slash",
            "damage_base": 10,
            "scaling_primary": "combat",
            "element": "physical",
        }

        with patch("world.combat_engine.roll_crit", return_value=(False, 1.0)):
            resolve_ability_damage(char, ability, target)

        self.assertTrue(target.ndb.took_damage_this_round)

    @patch("world.zone_scaling.get_player_damage_to_mob", side_effect=lambda d, *a: d)
    @patch("world.zone_scaling.get_mob_damage_for_player", return_value=(8, 14))
    @patch("world.zone_scaling.apply_resistance", side_effect=lambda d, *a: d)
    @patch("world.base_attributes.record_stat_use")
    def test_took_damage_flag_set_basic_attack(self, mock_record, mock_resist,
                                                mock_mob_dmg, mock_scale):
        """resolve_basic_attack sets target.ndb.took_damage_this_round = True."""
        from world.combat_engine import resolve_basic_attack

        attacker = _make_character()
        attacker.ndb.active_effects = []  # needed for get_effect_modifiers
        target = _make_mob(hp=100)
        target.ndb.took_damage_this_round = False
        target.ndb.active_effects = []

        with (
            patch("world.combat_engine.roll_crit", return_value=(False, 1.0)),
            patch(
                "world.weapon_skills.weapon_skill_damage_bonus_for_attack",
                return_value=0.0,
            ),
        ):
            resolve_basic_attack(attacker, target)

        self.assertTrue(target.ndb.took_damage_this_round)


# ===========================================================================
# Test Suite 3: Compound creation stores initial_duration
# ===========================================================================

class TestCompoundCreationInitialDuration(unittest.TestCase):
    """Verify check_compound_triggers stores initial_duration on new entries."""

    def test_compound_stores_initial_duration(self):
        """Compound entry includes initial_duration key."""
        from world.status_effects import check_compound_triggers

        target = _make_mob()
        # Set up burn + wet to trigger steam (consuming compound)
        target.ndb.active_effects = [
            {
                "type": "burn",
                "stacks": 1,
                "duration": 3,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 4,
                "is_compound": False,
            },
            {
                "type": "wet",
                "stacks": 1,
                "duration": 3,
                "magnitude": 1.0,
                "source_id": None,
                "max_stacks": 1,
                "is_compound": False,
            },
        ]

        triggered = check_compound_triggers(target)
        self.assertIn("steam", triggered)

        # Find the steam entry
        effects = target.ndb.active_effects
        steam_entry = next(e for e in effects if e["type"] == "steam")
        self.assertIn("initial_duration", steam_entry)
        self.assertEqual(steam_entry["initial_duration"], steam_entry["duration"])


# ===========================================================================
# Test Suite 4: Corpse loot command
# ===========================================================================

# Stub the heavy Evennia import chain that cmd_loot triggers
# We build fake modules so `from commands.cmd_loot import CmdLoot` works.
_cmd_loot_module = None

def _get_cmd_loot():
    """Lazy-import cmd_loot with mocked heavy deps."""
    global _cmd_loot_module
    if _cmd_loot_module is not None:
        return _cmd_loot_module

    # Stub the full evennia import tree that typeclasses.objects needs
    _extra_stubs = [
        "evennia.objects", "evennia.objects.objects",
        "evennia.typeclasses", "evennia.typeclasses.models",
        "evennia.typeclasses.attributes", "evennia.typeclasses.tags",
        "evennia.locks", "evennia.locks.lockhandler",
        "evennia.scripts", "evennia.scripts.scripts",
        "evennia.accounts", "evennia.accounts.accounts",
        "evennia.objects.models",
        "evennia.typeclasses.mixins",
    ]
    for mod_name in _extra_stubs:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = types.ModuleType(mod_name)

    # evennia.objects.objects.DefaultObject needs to be a class
    obj_mod = sys.modules["evennia.objects.objects"]
    if not hasattr(obj_mod, "DefaultObject"):
        obj_mod.DefaultObject = type("DefaultObject", (), {
            "at_object_creation": lambda self: None,
        })

    import commands.cmd_loot as mod
    _cmd_loot_module = mod
    return mod


class TestCmdLoot(unittest.TestCase):
    """Tests for the CmdLoot command."""

    def _make_corpse(self, killer_id=1, phase="locked", scales=0):
        corpse = MagicMock()
        corpse.key = "corpse of TestMob"
        corpse.db = MagicMock()
        corpse.db.killer_id = killer_id
        corpse.db.scales = scales
        corpse.db.loot_phase = phase
        corpse.contents = []
        return corpse

    def _make_corpse_instance(self, killer_id=1, phase="locked", scales=0):
        """Create a corpse mock that passes isinstance checks."""
        mod = _get_cmd_loot()
        corpse = MagicMock()
        # Make isinstance(corpse, CorpseContainer) return True
        corpse.__class__ = mod.CorpseContainer
        corpse.key = "corpse of TestMob"
        corpse.db = MagicMock()
        corpse.db.killer_id = killer_id
        corpse.db.scales = scales
        corpse.db.loot_phase = phase
        corpse.contents = []
        return corpse

    def test_loot_command_finds_corpse(self):
        """CmdLoot._find_corpse finds CorpseContainer in room."""
        mod = _get_cmd_loot()
        cmd = mod.CmdLoot()
        cmd.args = ""

        char = _make_character()
        corpse = self._make_corpse_instance()
        corpse.can_loot = MagicMock(return_value=(True, ""))
        char.location.contents = [corpse]
        cmd.caller = char

        found = cmd._find_corpse(char)
        self.assertIsNotNone(found)

    def test_loot_respects_locked_phase(self):
        """Non-killer cannot loot during locked phase."""
        mod = _get_cmd_loot()
        cmd = mod.CmdLoot()
        cmd.args = ""

        char = _make_character()
        corpse = self._make_corpse_instance(killer_id=999, phase="locked")
        corpse.can_loot = MagicMock(return_value=(False, "Loot is still being claimed."))

        char.location.contents = [corpse]
        cmd.caller = char

        cmd.func()
        char.msg.assert_called()
        msg_text = str(char.msg.call_args)
        self.assertTrue("claimed" in msg_text.lower() or "Loot" in msg_text)

    def test_loot_transfers_scales(self):
        """Corpse Scales transfer to character.db.carried_scales."""
        mod = _get_cmd_loot()
        cmd = mod.CmdLoot()
        cmd.args = ""

        char = _make_character()
        char.db.carried_scales = 50
        char.ndb.group_leader_id = None

        corpse = self._make_corpse_instance(killer_id=char.id, scales=100)
        corpse.can_loot = MagicMock(return_value=(True, ""))
        corpse.contents = []

        char.location.contents = [corpse]
        cmd.caller = char

        with patch("world.group_engine.is_in_group", return_value=False):
            cmd.func()

        self.assertEqual(char.db.carried_scales, 150)
        self.assertEqual(corpse.db.scales, 0)

    def test_loot_transfers_items_from_corpse_container(self):
        """CmdLoot passes the corpse to inventory pickup so contained drops can move."""
        mod = _get_cmd_loot()
        cmd = mod.CmdLoot()
        cmd.args = ""

        char = _make_character()
        char.db.carried_scales = 0
        char.ndb.group_leader_id = None

        corpse = self._make_corpse_instance(killer_id=char.id, scales=0)
        corpse.can_loot = MagicMock(return_value=(True, ""))
        item = MagicMock()
        item.key = "wolf pelt"
        item.location = corpse
        corpse.contents = [item]

        char.location.contents = [corpse]
        cmd.caller = char

        with patch("world.group_engine.is_in_group", return_value=False), \
             patch("world.inventory_engine.pick_up", return_value=(True, "picked")) as mock_pick_up:
            cmd.func()

        mock_pick_up.assert_called_once_with(char, item, container=corpse)
        self.assertIn("wolf pelt", str(char.msg.call_args))


# ===========================================================================
# Test Suite 5: Group loot distribution
# ===========================================================================

class TestGroupLoot(unittest.TestCase):
    """Tests for group loot distribution functions."""

    def test_group_loot_personal(self):
        """Personal mode: only killer gets loot rights."""
        from world.group_engine import get_designated_looter

        killer = _make_character("Killer")
        other = _make_character("Other")

        # Set up group state
        leader = killer
        leader.ndb.group_leader_id = leader.id
        leader.ndb.group_state = {
            "members": [leader.id, other.id],
            "leader_id": leader.id,
            "loot_mode": "personal",
            "round_robin_index": 0,
        }
        other.ndb.group_leader_id = leader.id

        corpse = MagicMock()
        corpse.db = MagicMock()
        corpse.db.killer_id = killer.id

        with patch("world.group_engine.evennia") as mock_ev:
            mock_ev.search_object = MagicMock(
                side_effect=lambda s: [killer] if str(killer.id) in s else [other]
            )
            designated = get_designated_looter(killer, corpse)
            self.assertEqual(designated.id, killer.id)

    def test_group_loot_round_robin(self):
        """Round robin rotates loot rights among group members."""
        from world.group_engine import get_designated_looter

        char1 = _make_character("Char1")
        char2 = _make_character("Char2")
        char3 = _make_character("Char3")

        leader = char1
        leader.ndb.group_leader_id = leader.id
        leader.ndb.group_state = {
            "members": [char1.id, char2.id, char3.id],
            "leader_id": leader.id,
            "loot_mode": "round_robin",
            "round_robin_index": 1,  # char2's turn
        }
        char2.ndb.group_leader_id = leader.id
        char3.ndb.group_leader_id = leader.id

        corpse = MagicMock()

        with patch("world.group_engine.evennia") as mock_ev:
            def search_side_effect(s):
                for c in [char1, char2, char3]:
                    if str(c.id) in s:
                        return [c]
                return []
            mock_ev.search_object = MagicMock(side_effect=search_side_effect)

            designated = get_designated_looter(char2, corpse)
            self.assertEqual(designated.id, char2.id)

    def test_round_robin_skips_group_members_outside_the_encounter_snapshot(self):
        """A remote member cannot block local participants' shared loot turn."""
        from world.group_engine import get_designated_looter

        leader = _make_character("Leader")
        remote = _make_character("Remote")
        local = _make_character("Local")
        leader.ndb.group_leader_id = leader.id
        leader.ndb.group_state = {
            "members": [leader.id, remote.id, local.id],
            "leader_id": leader.id,
            "loot_mode": "round_robin",
            "round_robin_index": 1,
        }
        remote.ndb.group_leader_id = leader.id
        local.ndb.group_leader_id = leader.id
        corpse = MagicMock()
        corpse.db.authorized_looter_ids = [leader.id, local.id]

        with patch("world.group_engine.evennia") as mock_ev:
            mock_ev.search_object.side_effect = lambda value: {
                str(leader.id): [leader],
                str(remote.id): [remote],
                str(local.id): [local],
            }.get(value.removeprefix("#"), [])

            designated = get_designated_looter(leader, corpse)

        self.assertEqual(designated.id, local.id)

    def test_distribute_group_loot_returns_designated(self):
        """get_designated_looter returns None for ffa mode (anyone can loot)."""
        from world.group_engine import get_designated_looter

        char = _make_character("Char1")
        char.ndb.group_leader_id = char.id
        char.ndb.group_state = {
            "members": [char.id],
            "leader_id": char.id,
            "loot_mode": "ffa",
            "round_robin_index": 0,
        }

        corpse = MagicMock()

        with patch("world.group_engine.evennia") as mock_ev:
            mock_ev.search_object = MagicMock(return_value=[char])
            result = get_designated_looter(char, corpse)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
