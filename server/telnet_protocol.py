"""Soravelon's compatibility fix for Evennia 6 Telnet byte input."""

import re

from evennia.server.portal.telnet import (
    TelnetProtocol as EvenniaTelnetProtocol,
    _HTTP_WARNING,
    _IDLE_COMMAND,
    _RE_LINEBREAK,
)
from twisted.conch.telnet import NULL


_HTTP_BYTES_REGEX = re.compile(
    rb"(GET|HEAD|POST|PUT|DELETE|TRACE|OPTIONS|CONNECT|PATCH) "
    rb"(.*? HTTP/[0-9]\.[0-9])",
    re.I,
)


class SoravelonTelnetProtocol(EvenniaTelnetProtocol):
    """Accept Twisted's byte payloads without weakening the HTTP guard."""

    def applicationDataReceived(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")

        if not data:
            chunks = [data]
        elif data.strip() == NULL:
            chunks = [_IDLE_COMMAND]
        else:
            chunks = _RE_LINEBREAK.split(data)

            if len(chunks) > 2 and _HTTP_BYTES_REGEX.match(chunks[0]):
                self.transport.write(_HTTP_WARNING)
                self.transport.loseConnection()
                return

            if self.line_buffer and len(chunks) > 1:
                chunks[0] = self.line_buffer + chunks[0]
                self.line_buffer = b""
            self.line_buffer += chunks.pop()

        for chunk in chunks:
            self.data_in(text=chunk + b"\n")
