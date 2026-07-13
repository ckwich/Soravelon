"""Contracts for the stock-webclient Soravelon OOB compatibility bridge."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = (
    REPO_ROOT
    / "web"
    / "static"
    / "webclient"
    / "js"
    / "plugins"
    / "soravelon_oob.js"
)
TEMPLATE_PATH = REPO_ROOT / "web" / "templates" / "webclient" / "webclient.html"
EXPECTED_EVENTS = {
    "combat_update",
    "flight_progress",
    "inventory_update",
    "map_update",
    "node_event",
    "quest_update",
    "stat_update",
    "status_update",
}


class TestStockWebclientOobBridge(unittest.TestCase):
    def test_template_loads_the_project_owned_bridge(self):
        template = TEMPLATE_PATH.read_text()

        self.assertIn('{% extends "webclient/base.html" %}', template)
        self.assertIn(
            '{% static "webclient/js/plugins/soravelon_oob.js" %}',
            template,
        )
        self.assertIn('id="messagewindow"', template)
        self.assertIn('id="inputfield"', template)

    def test_bridge_claims_every_server_event_without_rendering_raw_state(self):
        bridge = BRIDGE_PATH.read_text()
        event_block = re.search(
            r"SORAVELON_OOB_EVENTS\s*=\s*Object\.freeze\(\[(.*?)\]\)",
            bridge,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(event_block)
        events = set(re.findall(r'"([a-z_]+)"', event_block.group(1)))

        self.assertEqual(events, EXPECTED_EVENTS)
        self.assertIn("Evennia.emitter.on(eventName", bridge)
        self.assertIn("window.soravelonState", bridge)
        self.assertNotIn("messagewindow", bridge)
        self.assertNotIn("innerHTML", bridge)
        self.assertNotIn(".append(", bridge)


if __name__ == "__main__":
    unittest.main()
