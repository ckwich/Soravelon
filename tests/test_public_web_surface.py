"""Player-facing website and webclient launch-surface contracts."""

import hashlib
import re
from pathlib import Path

from django.test import TestCase


class TestPublicWebSurface(TestCase):
    def test_homepage_introduces_the_living_world_instead_of_the_framework(self):
        response = self.client.get("/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("A living world remembers what you do", html)
        self.assertIn("Enter Soravelon", html)
        self.assertIn("Open-world exploration", html)
        self.assertNotIn("Welcome to Evennia!", html)
        self.assertNotIn("The Python MUD/MU* creation system", html)
        self.assertNotIn("Database Stats", html)

    def test_homepage_uses_the_public_soravelon_identity(self):
        response = self.client.get("/")
        html = response.content.decode()

        self.assertIn("Soravelon", html)
        self.assertIn("A living dark-fantasy world", html)
        self.assertNotIn("evennia_logo.png", html)
        self.assertIn("website/css/custom.css?v=20260713-2", html)

    def test_webclient_terminal_controls_have_accessible_names(self):
        response = self.client.get("/webclient/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('role="log"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('aria-label="Command input"', html)
        self.assertIn('aria-label="Send command"', html)
        self.assertIn("soravelon_oob.js?v=20260713-1", html)

    def test_webclient_restores_names_after_goldenlayout_rebuilds_controls(self):
        bridge = Path("web/static/webclient/js/plugins/soravelon_oob.js").read_text()

        self.assertIn("function applyAccessibilityLabels()", bridge)
        self.assertIn('querySelectorAll(".inputfield")', bridge)
        self.assertIn('setAttribute("aria-label", "Command input")', bridge)
        self.assertIn('querySelectorAll(".inputsend")', bridge)
        self.assertIn('setAttribute("aria-label", "Send command")', bridge)
        self.assertIn("postInit: postInit", bridge)
        self.assertIn("onLayoutChanged: onLayoutChanged", bridge)

    def test_public_browser_dependencies_are_local_pinned_and_licensed(self):
        homepage = self.client.get("/").content.decode()
        webclient = self.client.get("/webclient/").content.decode()

        remote_asset = re.compile(
            r'<(?:script|link)\b[^>]+(?:src|href)=["\']https?://', re.IGNORECASE
        )
        self.assertNotRegex(homepage, remote_asset)
        self.assertNotRegex(webclient, remote_asset)

        expected_assets = (
            "jquery-3.7.1.min.js",
            "bootstrap-4.6.2.min.css",
            "bootstrap-4.6.2.bundle.min.js",
            "goldenlayout-1.5.9.min.js",
            "goldenlayout-1.5.9-base.css",
            "goldenlayout-1.5.9-dark-theme.css",
            "favico-0.3.10.min.js",
        )
        rendered = homepage + webclient
        manifest = Path("web/static/vendor/THIRD_PARTY_ASSETS.md").read_text()
        for asset in expected_assets:
            asset_path = Path("web/static/vendor", asset)
            self.assertIn(f"/static/vendor/{asset}", rendered)
            self.assertTrue(asset_path.is_file())
            digest = hashlib.sha256(asset_path.read_bytes()).hexdigest()
            self.assertRegex(manifest, rf"{re.escape(asset)}.*`{digest}`")

    def test_help_index_uses_semantic_scannable_category_sections(self):
        response = self.client.get("/help/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('class="help-category-grid"', html)
        self.assertIn('<h2 class="help-category-title">Ancestries</h2>', html)
        self.assertNotIn("The box to the right", html)

    def test_help_topic_uses_a_readable_player_facing_heading(self):
        response = self.client.get("/help/systems/scaling/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1 class="card-title">Scaling</h1>', html)
        self.assertIn('class="help-entry-text"', html)
        self.assertNotIn("scaling detail", html.lower())
