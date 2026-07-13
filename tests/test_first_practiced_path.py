"""Database-backed pacing contract for the authored first-Practiced arc."""

from pathlib import Path

from evennia.utils.test_resources import EvenniaTest

from world.content_compiler import compile_world_manifest, thaw_compiled_value


FIRST_PRACTICED_OPPORTUNITY_IDS = (
    "vc_stable_calm_nervous_mare",
    "vc_tanner_cut_repair_strap",
    "ash_road_read_wolf_sign",
    "ash_grass_test_shelter_grass",
)


def _authored_first_practiced_payloads():
    compilation = compile_world_manifest(Path("world/areas"))
    if compilation.manifest is None:
        raise AssertionError(compilation.diagnostics)

    by_id = {}
    for zone in compilation.manifest.zones:
        if zone.zone_id not in {"vaels_crossing", "ashreach_plains"}:
            continue
        for operation in zone.operations:
            if operation.method != "practice_opportunity":
                continue
            opportunity_id = operation.arguments[0]
            payload = thaw_compiled_value(operation.keyword_arguments)
            payload["opportunity_id"] = opportunity_id
            by_id[opportunity_id] = payload

    return [by_id[opportunity_id] for opportunity_id in FIRST_PRACTICED_OPPORTUNITY_IDS]


class TestFirstPracticedPath(EvenniaTest):
    def test_four_authored_interactions_reach_only_naturalism_practiced_once(self):
        from world.guild_engine import check_guild_eligibility
        from world.models import GuildRecruitment
        from world.practice_engine import resolve_practice_opportunity
        from world.world_state import commit_session_xp, init_session_accumulators

        self.char1.db.domain_scores = {}
        self.char1.db.guild_id = None
        init_session_accumulators(self.char1)
        payloads = _authored_first_practiced_payloads()

        for payload in payloads:
            success, message = resolve_practice_opportunity(
                payload,
                {"character": self.char1, "args": payload["target"]},
            )
            self.assertTrue(success, message)

        commit_session_xp(self.char1)

        self.assertEqual(self.char1.db.domain_scores, {"naturalism": 30.0})
        self.assertEqual(check_guild_eligibility(self.char1), ["verdance"])
        recruitment = GuildRecruitment.objects.get(character=self.char1)
        self.assertEqual(recruitment.guild_id, "verdance")
        self.assertEqual(recruitment.status, "offered")

        for payload in payloads:
            success, message = resolve_practice_opportunity(
                payload,
                {"character": self.char1, "args": payload["target"]},
            )
            self.assertFalse(success)
            self.assertIn("already", message.lower())

        commit_session_xp(self.char1)
        self.assertEqual(self.char1.db.domain_scores, {"naturalism": 30.0})
