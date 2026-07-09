"""Startup configuration regression tests."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestServerStartup(unittest.TestCase):
    def test_at_server_start_registers_callable_ticker_callbacks(self):
        from server.conf import at_server_startstop

        ticker = MagicMock()

        with (
            patch("evennia.TICKER_HANDLER", ticker),
            patch("world.node_helpers.initialize_node_pool"),
            patch("world.mob_spawner.initialize_spawn_records"),
            patch.object(at_server_startstop, "_load_all_zones"),
        ):
            at_server_startstop.at_server_start()

        callbacks = [
            call.kwargs["callback"]
            for call in ticker.add.call_args_list
        ]
        self.assertEqual(len(callbacks), 7)
        self.assertTrue(all(callable(callback) for callback in callbacks))
        self.assertFalse(any(isinstance(callback, str) for callback in callbacks))

    def test_production_webserver_ports_use_evennia_tuple_shape(self):
        module_path = (
            Path(__file__).resolve().parents[1]
            / "server"
            / "conf"
            / "production_settings.py"
        )
        spec = importlib.util.spec_from_file_location(
            "soravelon_test_production_settings",
            module_path,
        )
        module = importlib.util.module_from_spec(spec)
        env = {
            "SECRET_KEY": (
                "soravelon-production-test-key-"
                "0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            "ALLOWED_HOSTS": "game.example.test",
            "CSRF_TRUSTED_ORIGINS": "https://game.example.test",
            "DATABASE_ENGINE": "postgresql",
            "DATABASE_NAME": "soravelon_test",
            "DATABASE_USER": "soravelon_test",
            "DATABASE_PASSWORD": "database-test-password",
            "WEBSERVER_PORT": "4401",
            "WEBSERVER_INTERNAL_PORT": "4405",
            "WEBSOCKET_CLIENT_PORT": "4402",
            "SSH_PORT": "4404",
            "SSH_ENABLED": "true",
        }
        with patch.dict("os.environ", env, clear=True):
            assert spec.loader is not None
            spec.loader.exec_module(module)

        self.assertEqual(module.WEBSERVER_PORTS, [(4401, 4405)])
        self.assertEqual(module.WEBSOCKET_CLIENT_PORT, 4402)
        self.assertEqual(module.SSH_PORTS, [4404])
