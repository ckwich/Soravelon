"""Player-facing website and webclient launch-surface contracts."""

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
