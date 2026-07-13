"""Behavior contracts for the authored room-prose release gate."""

import unittest
from pathlib import Path


def _area_source(*descriptions):
    room_lines = []
    for index, description in enumerate(descriptions, start=1):
        room_lines.append(
            f"    area.room('room_{index}', name='Room {index}', "
            f"desc={description!r})"
        )
    return "\n".join(
        [
            "from world.area_builder import AreaBuilder",
            "",
            "def build():",
            "    area = AreaBuilder('prose_test')",
            "    area.zone(name='Prose Test', zone_type='frontier', continent='varath')",
            *room_lines,
            "    return area.build()",
            "",
        ]
    )


class TestContentProseAudit(unittest.TestCase):
    def test_rejects_player_facing_meta_language(self):
        from scripts.audit_content_prose import audit_prose_sources

        audit = audit_prose_sources(
            {
                "world/areas/meta.py": _area_source(
                    "This part of the road centers on a bend built for players."
                )
            }
        )

        self.assertEqual(
            {finding.code for finding in audit.findings},
            {"meta-prose"},
        )

    def test_rejects_exact_duplicate_room_descriptions(self):
        from scripts.audit_content_prose import audit_prose_sources

        description = "Rain darkens the cedar steps. A bell rope knocks in the wind."
        audit = audit_prose_sources(
            {"world/areas/duplicate.py": _area_source(description, description)}
        )

        self.assertIn(
            "duplicate-description",
            {finding.code for finding in audit.findings},
        )

    def test_rejects_one_sentence_reused_across_four_rooms(self):
        from scripts.audit_content_prose import audit_prose_sources

        shared = "Salt mist beads on the black rail."
        descriptions = [
            f"{shared} Detail {index} marks this particular landing."
            for index in range(4)
        ]
        audit = audit_prose_sources(
            {"world/areas/repeated.py": _area_source(*descriptions)}
        )

        self.assertIn(
            "repeated-sentence",
            {finding.code for finding in audit.findings},
        )

    def test_exact_allowlist_key_suppresses_only_reviewed_finding(self):
        from scripts.audit_content_prose import audit_prose_sources

        sources = {
            "world/areas/meta.py": _area_source(
                "A chalk note promises gameplay beside the quay crane."
            )
        }
        first = audit_prose_sources(sources)
        self.assertTrue(first.findings)

        allowed = audit_prose_sources(
            sources,
            allowlist={first.findings[0].allowlist_key},
        )

        self.assertEqual(allowed.findings, ())

    def test_specific_non_meta_room_prose_passes(self):
        from scripts.audit_content_prose import audit_prose_sources

        audit = audit_prose_sources(
            {
                "world/areas/clean.py": _area_source(
                    "Three wet bootprints cross the flour dust toward the back door.",
                    "A cracked blue cup holds nails beside the cooper's unfinished hoop.",
                    "Wind pushes eelgrass under the east piling, where a red cord is tied.",
                )
            }
        )

        self.assertEqual(audit.findings, ())

    def test_spatial_centers_on_phrase_is_not_treated_as_meta_prose(self):
        from scripts.audit_content_prose import audit_prose_sources

        audit = audit_prose_sources(
            {
                "world/areas/clean.py": _area_source(
                    "The court still centers on a cracked bell frame, though the bell now rings for quarry shifts."
                )
            }
        )

        self.assertEqual(audit.findings, ())

    def test_live_repo_exposes_the_known_vault_dependent_rewrite_gate(self):
        from scripts.audit_content_prose import audit_prose_directory

        areas_dir = Path(__file__).resolve().parents[1] / "world" / "areas"
        audit = audit_prose_directory(areas_dir)

        self.assertTrue(audit.findings)
        self.assertTrue(
            {"meta-prose", "repeated-sentence"}.issubset(
                {finding.code for finding in audit.findings}
            )
        )
        flagged_paths = {finding.source_path for finding in audit.findings}
        self.assertIn("world/areas/korahei.py", flagged_paths)
        self.assertIn("world/areas/tremen.py", flagged_paths)
