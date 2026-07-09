"""
Tests for the Soravelon world-state engine (Build Order Step 2).

Tests written FIRST per TDD discipline. These must all fail before
any production code is written.
"""

from evennia.utils.test_resources import EvenniaTest


class TestDimensionAggregateRange(EvenniaTest):
    """Dimension aggregate scores must stay within 0-100."""

    def test_scores_never_exceed_100(self):
        """Attempting to set a score above 100 clamps to 100."""
        from world.world_state import set_dimension_score

        set_dimension_score(self.char1, "reputation", 150.0)
        self.assertLessEqual(self.char1.db.reputation_score, 100.0)

    def test_scores_never_go_below_0(self):
        """Attempting to set a score below 0 clamps to 0."""
        from world.world_state import set_dimension_score

        set_dimension_score(self.char1, "reputation", -10.0)
        self.assertGreaterEqual(self.char1.db.reputation_score, 0.0)

    def test_all_five_dimensions_clamp(self):
        """All five dimensions respect the 0-100 range."""
        from world.world_state import set_dimension_score

        for dim in ("reputation", "network", "bond", "legacy", "attunement"):
            set_dimension_score(self.char1, dim, 200.0)
            score = getattr(self.char1.db, f"{dim}_score")
            self.assertLessEqual(score, 100.0, f"{dim} exceeded 100")

            set_dimension_score(self.char1, dim, -50.0)
            score = getattr(self.char1.db, f"{dim}_score")
            self.assertGreaterEqual(score, 0.0, f"{dim} went below 0")


class TestLegacyNoDecay(EvenniaTest):
    """Legacy score must never decrease from the decay tick."""

    def test_legacy_unaffected_by_decay(self):
        """Decay tick does not reduce Legacy score."""
        from world.world_state import set_dimension_score, apply_decay

        set_dimension_score(self.char1, "legacy", 50.0)
        before = self.char1.db.legacy_score

        apply_decay(self.char1)

        self.assertEqual(self.char1.db.legacy_score, before)

    def test_other_dimensions_do_decay(self):
        """Non-Legacy dimensions are reduced by decay (sanity check)."""
        from world.world_state import set_dimension_score, apply_decay

        set_dimension_score(self.char1, "reputation", 50.0)

        apply_decay(self.char1)

        self.assertLess(self.char1.db.reputation_score, 50.0)


class TestAttunementDualRepresentation(EvenniaTest):
    """Aggregate attunement_score updates when zone attunement records change."""

    def test_aggregate_updates_on_zone_change(self):
        """Setting a zone attunement record recalculates the aggregate."""
        from world.world_state import (
            update_zone_attunement,
            recalculate_attunement_aggregate,
        )

        update_zone_attunement(self.char1, "cantera_forest", 75.0)
        update_zone_attunement(self.char1, "tremen", 25.0)

        recalculate_attunement_aggregate(self.char1)

        # Aggregate should reflect the zone values (exact formula may vary,
        # but it must be > 0 and <= 100)
        agg = self.char1.db.attunement_score
        self.assertGreater(agg, 0.0)
        self.assertLessEqual(agg, 100.0)

    def test_zone_records_created_lazily(self):
        """No ZoneAttunement record exists until first interaction."""
        from world.models import ZoneAttunement

        count = ZoneAttunement.objects.filter(
            character=self.char1
        ).count()
        self.assertEqual(count, 0)


class TestBatchCommit(EvenniaTest):
    """ndb accumulator is zeroed after commit, DB value updated correctly."""

    def test_accumulator_cleared_after_commit(self):
        """ndb domain XP accumulator resets to 0 after batch commit."""
        from world.world_state import (
            accumulate_domain_xp,
            commit_session_xp,
            init_session_accumulators,
        )

        init_session_accumulators(self.char1)
        self.char1.db.domain_scores = {"combat": 0.0}
        self.char1.db.primary_domain = "combat"
        self.char1.db.secondary_domain = None

        accumulate_domain_xp(self.char1, "combat", 500)

        self.assertGreater(self.char1.ndb.domain_xp_combat, 0)

        commit_session_xp(self.char1)

        self.assertEqual(self.char1.ndb.domain_xp_combat, 0)

    def test_db_score_increases_after_commit(self):
        """Domain score in DB increases after committing accumulated XP."""
        from world.world_state import (
            accumulate_domain_xp,
            commit_session_xp,
            init_session_accumulators,
        )

        init_session_accumulators(self.char1)
        self.char1.db.domain_scores = {"combat": 10.0}
        self.char1.db.primary_domain = "combat"
        self.char1.db.secondary_domain = None
        self.char1.db.backend_level = 1

        accumulate_domain_xp(self.char1, "combat", 5000)
        commit_session_xp(self.char1)

        self.assertGreater(self.char1.db.domain_scores["combat"], 10.0)


class TestBackendLevelNeverExposed(EvenniaTest):
    """Backend level must never appear in any player-facing output."""

    def test_backend_level_exists_on_character(self):
        """Backend level is stored on the character (for internal use)."""
        from world.world_state import calculate_backend_level

        self.char1.db.domain_scores = {"combat": 50.0}
        self.char1.db.primary_domain = "combat"
        self.char1.db.secondary_domain = None

        level = calculate_backend_level(self.char1)

        self.assertIsInstance(level, int)
        self.assertGreaterEqual(level, 1)
        self.assertLessEqual(level, 50)

    def test_backend_level_range(self):
        """Backend level is always 1-50 regardless of input."""
        from world.world_state import calculate_backend_level

        # Zero scores → level 1
        self.char1.db.domain_scores = {}
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.assertEqual(calculate_backend_level(self.char1), 1)

        # Max scores → level 50
        self.char1.db.domain_scores = {d: 100.0 for d in [
            "combat", "subterfuge", "naturalism", "resonance", "arcana",
            "diplomacy", "alchemy", "tactics", "engineering", "remnance",
        ]}
        self.char1.db.primary_domain = "combat"
        self.char1.db.secondary_domain = "subterfuge"
        self.assertEqual(calculate_backend_level(self.char1), 50)


class TestContextPacketStructure(EvenniaTest):
    """Context packet contains all required fields, no missing keys."""

    def test_packet_has_all_required_fields(self):
        """Packet returned by get_character_context_packet has all keys."""
        from world.world_state import get_character_context_packet

        # Set up minimal character state
        self.char1.db.ancestry = "human"
        self.char1.db.primary_domain = "combat"
        self.char1.db.secondary_domain = "subterfuge"
        self.char1.db.guild_id = "ironblood"
        self.char1.db.subclass_id = "duskblade"
        self.char1.db.backend_level = 5
        self.char1.db.reputation_score = 10.0
        self.char1.db.network_score = 5.0
        self.char1.db.bond_score = 0.0
        self.char1.db.legacy_score = 0.0
        self.char1.db.attunement_score = 0.0
        self.char1.db.companion_id = None
        self.char1.db.companion_type = None
        self.char1.db.companion_tier = None

        packet = get_character_context_packet(self.char1)

        required_keys = {
            "ancestry", "primary_domain", "secondary_domain",
            "guild", "subclass", "backend_level",
            "reputation", "network", "bond", "legacy", "attunement",
            "standing", "trust", "betrayal_flag",
            "zone_attunement",
            "companion_present", "companion_type", "companion_tier",
        }
        self.assertTrue(
            required_keys.issubset(packet.keys()),
            f"Missing keys: {required_keys - packet.keys()}"
        )

    def test_packet_without_npc_has_null_faction_fields(self):
        """Without an NPC, faction fields are None."""
        from world.world_state import get_character_context_packet

        self.char1.db.ancestry = "human"
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.guild_id = None
        self.char1.db.subclass_id = None
        self.char1.db.backend_level = 1
        self.char1.db.reputation_score = 0.0
        self.char1.db.network_score = 0.0
        self.char1.db.bond_score = 0.0
        self.char1.db.legacy_score = 0.0
        self.char1.db.attunement_score = 0.0
        self.char1.db.companion_id = None
        self.char1.db.companion_type = None
        self.char1.db.companion_tier = None

        packet = get_character_context_packet(self.char1)

        self.assertIsNone(packet["standing"])
        self.assertIsNone(packet["trust"])
        self.assertIsNone(packet["betrayal_flag"])
        self.assertIsNone(packet["zone_attunement"])


class TestFactionStandingRange(EvenniaTest):
    """Standing must be clamped to -100,000 / +100,000."""

    def test_standing_clamped_high(self):
        """Standing cannot exceed +100,000."""
        from world.models import FactionStanding

        record = FactionStanding.objects.create(
            character=self.char1,
            faction_id="empire",
            standing=150000,
        )
        # The model itself stores the raw value; clamping happens in
        # the modify_standing function
        from world.world_state import modify_standing

        # Reset to 0 and add way too much
        record.standing = 0
        record.save()
        modify_standing(self.char1, "empire", 200000, "test")

        record.refresh_from_db()
        self.assertLessEqual(record.standing, 100000)

    def test_standing_clamped_low(self):
        """Standing cannot go below -100,000."""
        from world.world_state import modify_standing
        from world.models import FactionStanding

        FactionStanding.objects.create(
            character=self.char1,
            faction_id="wardens",
            standing=0,
        )

        modify_standing(self.char1, "wardens", -200000, "test")

        record = FactionStanding.objects.get(
            character=self.char1, faction_id="wardens"
        )
        self.assertGreaterEqual(record.standing, -100000)


class TestDecayPausedOnline(EvenniaTest):
    """Decay tick must not reduce scores for characters currently online."""

    def test_online_character_skipped(self):
        """If character is connected, decay_tick does not reduce scores."""
        from world.world_state import set_dimension_score, decay_tick_all
        from unittest.mock import patch

        set_dimension_score(self.char1, "reputation", 50.0)

        # Mock is_connected to return True (character is online)
        with patch.object(
            type(self.char1), "is_connected", new_callable=lambda: property(lambda s: True)
        ):
            decay_tick_all()

        self.assertEqual(self.char1.db.reputation_score, 50.0)


class TestSessionXpSafetyFlush(EvenniaTest):
    """The safety flush ticker must handle live Evennia query results."""

    def test_online_typeclass_result_flushes_without_typeclass_attribute(self):
        """Evennia 6 may return an already-wrapped Character from ObjectDB filters."""
        from unittest.mock import patch
        from world.world_state import session_xp_safety_flush

        class OnlineCharacter:
            @property
            def is_connected(self):
                return True

        character = OnlineCharacter()
        with (
            patch("evennia.objects.models.ObjectDB.objects.filter", return_value=[character]),
            patch("world.world_state.commit_session_xp") as commit_xp,
            patch("world.skill_engine.commit_skill_accumulators") as commit_skills,
            patch("world.base_attributes.commit_stat_growth") as commit_stats,
        ):
            session_xp_safety_flush()

        commit_xp.assert_called_once_with(character)
        commit_skills.assert_called_once_with(character)
        commit_stats.assert_called_once_with(character)


class TestWorldEventLogCreation(EvenniaTest):
    """log_world_event() creates a WorldEventLog record."""

    def test_world_event_log_creation(self):
        """log_world_event() creates a record with correct fields."""
        from world.world_state import log_world_event
        from world.models import WorldEventLog

        log_world_event(
            event_type="named_mob_kill",
            description="Old Guardian was slain in Cantera Forest.",
            zone_id="cantera_forest",
            character_id=self.char1.id,
            data={"mob_instance_id": "old_guardian", "participants": 1},
        )

        record = WorldEventLog.objects.latest("occurred_at")
        self.assertEqual(record.event_type, "named_mob_kill")
        self.assertEqual(record.zone_id, "cantera_forest")
        self.assertEqual(record.character_id, self.char1.id)
        self.assertIn("mob_instance_id", record.data)


class TestWorldEventLogAllEventTypes(EvenniaTest):
    """Each valid event_type string creates a record without error."""

    def test_world_event_log_all_event_types(self):
        """All expected event types can be stored."""
        from world.world_state import log_world_event
        from world.models import WorldEventLog

        event_types = [
            "named_mob_kill", "faction_shift", "node_activation",
            "node_stabilized", "quest_consequence", "legacy_entry",
            "llm_quest_outcome", "political_shift",
        ]
        for et in event_types:
            log_world_event(
                event_type=et,
                description=f"Test event: {et}",
            )

        self.assertEqual(WorldEventLog.objects.count(), len(event_types))


class TestContextPacketHasWorldEventSummary(EvenniaTest):
    """Context packet contains world_event_summary key."""

    def test_context_packet_has_world_event_summary(self):
        """Context packet contains world_event_summary (may be None)."""
        from world.world_state import get_character_context_packet

        self.char1.db.ancestry = "human"
        self.char1.db.primary_domain = None
        self.char1.db.secondary_domain = None
        self.char1.db.guild_id = None
        self.char1.db.subclass_id = None
        self.char1.db.backend_level = 1
        self.char1.db.reputation_score = 0.0
        self.char1.db.network_score = 0.0
        self.char1.db.bond_score = 0.0
        self.char1.db.legacy_score = 0.0
        self.char1.db.attunement_score = 0.0
        self.char1.db.companion_id = None
        self.char1.db.companion_type = None
        self.char1.db.companion_tier = None

        packet = get_character_context_packet(self.char1)

        self.assertIn("world_event_summary", packet)
        self.assertIsNone(packet["world_event_summary"])
