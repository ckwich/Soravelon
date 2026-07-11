"""Regression tests for Soravelon's Telnet transport boundary."""

from unittest.mock import MagicMock

from django.test import SimpleTestCase


class TestSoravelonTelnetProtocol(SimpleTestCase):
    def _protocol(self):
        from server.telnet_protocol import SoravelonTelnetProtocol

        protocol = object.__new__(SoravelonTelnetProtocol)
        protocol.line_buffer = b""
        protocol.data_in = MagicMock()
        protocol.transport = MagicMock()
        return protocol

    def test_bytes_command_reaches_game_input(self):
        """Twisted's bytes payload is accepted instead of crashing the portal."""
        protocol = self._protocol()

        protocol.applicationDataReceived(b"look\r\n")

        protocol.data_in.assert_called_once_with(text=b"look\n")
        protocol.transport.loseConnection.assert_not_called()

    def test_bytes_http_probe_is_rejected_cleanly(self):
        """The Telnet port still rejects accidental HTTP traffic."""
        protocol = self._protocol()

        protocol.applicationDataReceived(b"GET / HTTP/1.1\r\n\r\n")

        protocol.data_in.assert_not_called()
        protocol.transport.write.assert_called_once()
        protocol.transport.loseConnection.assert_called_once()
