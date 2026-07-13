"""Contracts for the isolated real-protocol playtest boundary."""

from __future__ import annotations

import base64
from contextlib import redirect_stderr, redirect_stdout
import hashlib
from io import StringIO
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts import smoke_protocols


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestPlaytestSettings(unittest.TestCase):
    def _load_settings(self, overrides: dict[str, str]):
        env = os.environ.copy()
        env.pop("SORAVELON_PLAYTEST_DATABASE", None)
        env.pop("SORAVELON_PLAYTEST_LOG_DIR", None)
        env.pop("SORAVELON_PLAYTEST_PORT_BASE", None)
        env.update(overrides)
        script = """
import json
from server.conf import playtest_settings as settings
print(json.dumps({
    "database": settings.DATABASES["default"],
    "telnet_ports": settings.TELNET_PORTS,
    "telnet_interfaces": settings.TELNET_INTERFACES,
    "webserver_ports": settings.WEBSERVER_PORTS,
    "webserver_interfaces": settings.WEBSERVER_INTERFACES,
    "websocket_port": settings.WEBSOCKET_CLIENT_PORT,
    "websocket_interface": settings.WEBSOCKET_CLIENT_INTERFACE,
    "amp_port": settings.AMP_PORT,
    "amp_interface": settings.AMP_INTERFACE,
    "server_log": settings.SERVER_LOG_FILE,
    "portal_log": settings.PORTAL_LOG_FILE,
    "http_log": settings.HTTP_LOG_FILE,
    "log_dir": settings.LOG_DIR,
    "lockwarning_log": settings.LOCKWARNING_LOG_FILE,
}))
"""
        return subprocess.run(
            [sys.executable, "-c", script],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_settings_fail_closed_without_disposable_paths(self):
        result = self._load_settings({})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SORAVELON_PLAYTEST_DATABASE", result.stderr)

    def test_settings_isolate_database_logs_listeners_and_amp(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            database = temp / "playtest.db3"
            logs = temp / "logs"
            result = self._load_settings(
                {
                    "SORAVELON_PLAYTEST_DATABASE": str(database),
                    "SORAVELON_PLAYTEST_LOG_DIR": str(logs),
                    "SORAVELON_PLAYTEST_PORT_BASE": "45100",
                }
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            values = json.loads(result.stdout)
            self.assertEqual(
                values["database"],
                {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": str(database),
                },
            )
            self.assertEqual(values["telnet_ports"], [45100])
            self.assertEqual(values["telnet_interfaces"], ["127.0.0.1"])
            self.assertEqual(values["webserver_ports"], [[45101, 45105]])
            self.assertEqual(values["webserver_interfaces"], ["127.0.0.1"])
            self.assertEqual(values["websocket_port"], 45102)
            self.assertEqual(values["websocket_interface"], "127.0.0.1")
            self.assertEqual(values["amp_port"], 45106)
            self.assertEqual(values["amp_interface"], "127.0.0.1")
            self.assertEqual(values["server_log"], str(logs / "server.log"))
            self.assertEqual(values["portal_log"], str(logs / "portal.log"))
            self.assertEqual(values["http_log"], str(logs / "http.log"))
            self.assertEqual(values["log_dir"], str(logs))
            self.assertEqual(
                values["lockwarning_log"],
                str(logs / "lockwarnings.log"),
            )


class TestWebSocketFrames(unittest.TestCase):
    def test_client_text_frames_are_masked_and_recover_the_exact_json(self):
        payload = '["text", ["look"], {}]'

        frame = smoke_protocols._encode_client_text_frame(
            payload,
            mask_key=b"\x01\x02\x03\x04",
        )

        self.assertEqual(frame[0], 0x81)
        self.assertTrue(frame[1] & 0x80)
        payload_length = frame[1] & 0x7F
        self.assertEqual(payload_length, len(payload.encode("utf-8")))
        mask = frame[2:6]
        recovered = bytes(
            value ^ mask[index % 4]
            for index, value in enumerate(frame[6:])
        ).decode("utf-8")
        self.assertEqual(recovered, payload)


class TestLiveProtocolChecks(unittest.TestCase):
    def _serve_once(self, responder):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        failures: list[BaseException] = []

        def run_server():
            try:
                connection, _address = listener.accept()
                with connection:
                    responder(connection)
            except BaseException as exc:  # pragma: no cover - surfaced below
                failures.append(exc)
            finally:
                listener.close()

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        return port, thread, failures

    def test_telnet_check_round_trips_look_over_a_real_socket(self):
        received: list[bytes] = []

        def responder(connection):
            connection.sendall(b"S O R A V E L O N\r\nconnect or create\r\n")
            received.append(connection.recv(4096))
            connection.sendall(b"S O R A V E L O N\r\nconnect or create\r\n")

        port, thread, failures = self._serve_once(responder)

        detail = smoke_protocols.verify_telnet(
            host="127.0.0.1",
            port=port,
            timeout=2.0,
        )
        thread.join(timeout=2.0)

        self.assertEqual(failures, [])
        self.assertEqual(received, [b"look\r\n"])
        self.assertIn("look round-trip", detail)

    def test_webclient_check_loads_the_real_http_surface(self):
        received: list[bytes] = []

        def responder(connection):
            request = connection.recv(4096)
            received.append(request)
            body = (
                b"<html><title>Evennia Webclient</title>"
                b'<script src="soravelon_oob.js"></script></html>'
            )
            connection.sendall(
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/html\r\n"
                + f"Content-Length: {len(body)}\r\n".encode("ascii")
                + b"Connection: close\r\n\r\n"
                + body
            )

        port, thread, failures = self._serve_once(responder)

        detail = smoke_protocols.verify_webclient_http(
            host="127.0.0.1",
            port=port,
            timeout=2.0,
        )
        thread.join(timeout=2.0)

        self.assertEqual(failures, [])
        self.assertIn(b"GET /webclient/ HTTP/1.1", received[0])
        self.assertIn("webclient page returned HTTP 200", detail)

    def test_webclient_check_can_model_the_trusted_https_proxy(self):
        received: list[bytes] = []

        def responder(connection):
            request = connection.recv(4096)
            received.append(request)
            body = (
                b"<html><title>Evennia Webclient</title>"
                b'<script src="soravelon_oob.js"></script></html>'
            )
            connection.sendall(
                b"HTTP/1.1 200 OK\r\n"
                + f"Content-Length: {len(body)}\r\n".encode("ascii")
                + b"Connection: close\r\n\r\n"
                + body
            )

        port, thread, failures = self._serve_once(responder)

        detail = smoke_protocols.verify_webclient_http(
            host="127.0.0.1",
            port=port,
            timeout=2.0,
            forwarded_https=True,
        )
        thread.join(timeout=2.0)

        self.assertEqual(failures, [])
        self.assertIn(b"X-Forwarded-Proto: https\r\n", received[0])
        self.assertIn("forwarded HTTPS", detail)

    def test_webclient_check_rejects_a_page_without_the_oob_bridge(self):
        def responder(connection):
            connection.recv(4096)
            body = b"<html><title>Evennia Webclient</title></html>"
            connection.sendall(
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/html\r\n"
                + f"Content-Length: {len(body)}\r\n".encode("ascii")
                + b"Connection: close\r\n\r\n"
                + body
            )

        port, thread, failures = self._serve_once(responder)

        with self.assertRaisesRegex(
            smoke_protocols.ProtocolSmokeError,
            "Soravelon OOB compatibility bridge",
        ):
            smoke_protocols.verify_webclient_http(
                host="127.0.0.1",
                port=port,
                timeout=2.0,
            )
        thread.join(timeout=2.0)

        self.assertEqual(failures, [])

    def test_websocket_check_negotiates_evennia_and_round_trips_look(self):
        received_messages: list[list[object]] = []

        def server_text_frame(payload: str) -> bytes:
            data = payload.encode("utf-8")
            self.assertLess(len(data), 126)
            return bytes((0x81, len(data))) + data

        def responder(connection):
            request = bytearray()
            while b"\r\n\r\n" not in request:
                request.extend(connection.recv(4096))
            headers = request.decode("ascii").split("\r\n")
            key = next(
                line.split(":", 1)[1].strip()
                for line in headers
                if line.lower().startswith("sec-websocket-key:")
            )
            accept = base64.b64encode(
                hashlib.sha1(
                    (key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode(
                        "ascii"
                    )
                ).digest()
            )
            banner = json.dumps(
                ["text", ["S O R A V E L O N connect or create"], {}]
            )
            connection.sendall(
                b"HTTP/1.1 101 Switching Protocols\r\n"
                b"Upgrade: websocket\r\n"
                b"Connection: Upgrade\r\n"
                + b"Sec-WebSocket-Accept: "
                + accept
                + b"\r\n"
                + b"Sec-WebSocket-Protocol: v1.evennia.com\r\n\r\n"
                + server_text_frame(banner)
            )

            header = connection.recv(2)
            payload_length = header[1] & 0x7F
            mask = connection.recv(4)
            masked_payload = connection.recv(payload_length)
            payload = bytes(
                value ^ mask[index % 4]
                for index, value in enumerate(masked_payload)
            )
            received_messages.append(json.loads(payload.decode("utf-8")))
            connection.sendall(server_text_frame(banner))

        port, thread, failures = self._serve_once(responder)

        detail = smoke_protocols.verify_websocket(
            host="127.0.0.1",
            port=port,
            timeout=2.0,
        )
        thread.join(timeout=2.0)

        self.assertEqual(failures, [])
        self.assertEqual(received_messages, [["text", ["look"], {}]])
        self.assertIn("v1.evennia.com", detail)
        self.assertIn("look round-trip", detail)


class TestProtocolSmokeCli(unittest.TestCase):
    def test_cli_runs_every_real_entry_point_and_reports_passes(self):
        output = StringIO()
        with patch.object(
            smoke_protocols,
            "verify_telnet",
            return_value="telnet live",
        ), patch.object(
            smoke_protocols,
            "verify_webclient_http",
            return_value="http live",
        ) as verify_http, patch.object(
            smoke_protocols,
            "verify_websocket",
            return_value="websocket live",
        ), redirect_stdout(output):
            result = smoke_protocols.main(
                [
                    "--host",
                    "127.0.0.1",
                    "--telnet-port",
                    "45100",
                    "--web-port",
                    "45101",
                    "--websocket-port",
                    "45102",
                    "--forwarded-https",
                ]
            )

        self.assertEqual(result, 0)
        verify_http.assert_called_once_with(
            host="127.0.0.1",
            port=45101,
            timeout=5.0,
            forwarded_https=True,
        )
        self.assertIn("PASS telnet: telnet live", output.getvalue())
        self.assertIn("PASS webclient HTTP: http live", output.getvalue())
        self.assertIn("PASS websocket: websocket live", output.getvalue())

    def test_cli_refuses_remote_hosts_without_explicit_authority(self):
        error = StringIO()
        with redirect_stderr(error):
            result = smoke_protocols.main(
                [
                    "--host",
                    "192.0.2.1",
                    "--telnet-port",
                    "45100",
                    "--web-port",
                    "45101",
                    "--websocket-port",
                    "45102",
                ]
            )

        self.assertEqual(result, 2)
        self.assertIn("--allow-remote", error.getvalue())


class TestM5HumanPlaytestGuide(unittest.TestCase):
    def test_guide_covers_every_player_path_and_the_living_world_gate(self):
        guide = (
            REPO_ROOT / "docs" / "playtests" / "m5-release-acceptance.md"
        ).read_text()

        for heading in (
            "Fresh-player opening",
            "Co-op combat",
            "Social consequence",
            "Crafting and local economy",
            "Travel and exploration",
            "Quest consequence",
            "Recovery and return",
            "Living-world acceptance",
        ):
            with self.subTest(heading=heading):
                self.assertIn(f"## {heading}", guide)

        for player_command in (
            "calm nervous mare",
            "cut repair strap",
            "track wolf sign",
            "test shelter grass",
            "talk Elwen",
            "group invite",
            "quest share cellar",
            "talk Calloway",
            "talk Harven",
            "buy pickaxe",
            "mine",
            "smith iron ingot",
            "rest",
            "sleep",
            "wake",
        ):
            with self.subTest(player_command=player_command):
                self.assertIn(f"`{player_command}", guide)

        for acceptance_signal in (
            "time to first meaningful choice",
            "first confusion",
            "return pull",
            "hours",
            "no backend level",
            "no admin intervention",
            "actual Telnet",
            "actual stock webclient",
        ):
            with self.subTest(acceptance_signal=acceptance_signal):
                self.assertIn(acceptance_signal, guide)

        for forbidden_shortcut in (
            "`@tel",
            "`py ",
            "`socialmemory",
            "create_item_from_catalog",
            "create_object(",
        ):
            with self.subTest(forbidden_shortcut=forbidden_shortcut):
                self.assertNotIn(forbidden_shortcut, guide)


if __name__ == "__main__":
    unittest.main()
