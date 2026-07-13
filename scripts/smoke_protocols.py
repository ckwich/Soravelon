#!/usr/bin/env python3
"""Exercise Soravelon's live Telnet, web, and WebSocket entry points."""

from __future__ import annotations

import argparse
import http.client
import base64
import hashlib
import ipaddress
import json
import os
import socket
import sys


SORAVELON_BANNER = b"S O R A V E L O N"
MAX_RESPONSE_BYTES = 1_048_576


class ProtocolSmokeError(RuntimeError):
    """A live protocol entry point failed its observable contract."""


class _BufferedSocket:
    def __init__(self, connection: socket.socket, initial: bytes = b""):
        self.connection = connection
        self.buffer = bytearray(initial)

    def read_exact(self, length: int) -> bytes:
        while len(self.buffer) < length:
            chunk = self.connection.recv(max(4096, length - len(self.buffer)))
            if not chunk:
                raise ProtocolSmokeError("WebSocket closed during a frame.")
            self.buffer.extend(chunk)
            if len(self.buffer) > MAX_RESPONSE_BYTES:
                raise ProtocolSmokeError(
                    "WebSocket buffered more than the one-megabyte smoke limit."
                )
        value = bytes(self.buffer[:length])
        del self.buffer[:length]
        return value


def _receive_until(
    connection: socket.socket,
    marker: bytes,
    *,
    description: str,
) -> bytes:
    response = bytearray()
    while marker not in response:
        chunk = connection.recv(4096)
        if not chunk:
            raise ProtocolSmokeError(
                f"{description} closed before the Soravelon banner arrived."
            )
        response.extend(chunk)
        if len(response) > MAX_RESPONSE_BYTES:
            raise ProtocolSmokeError(
                f"{description} exceeded the one-megabyte smoke response limit."
            )
    return bytes(response)


def verify_telnet(*, host: str, port: int, timeout: float) -> str:
    """Prove the real Telnet listener accepts and round-trips unlogged input."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            connection.settimeout(timeout)
            _receive_until(connection, SORAVELON_BANNER, description="Telnet login")
            connection.sendall(b"look\r\n")
            _receive_until(
                connection,
                SORAVELON_BANNER,
                description="Telnet look round-trip",
            )
    except (OSError, TimeoutError) as exc:
        raise ProtocolSmokeError(
            f"Telnet {host}:{port} did not complete the look round-trip: {exc}"
        ) from exc
    return f"{host}:{port} login banner and look round-trip"


def verify_webclient_http(*, host: str, port: int, timeout: float) -> str:
    """Prove the stock webclient entry page is served over real HTTP."""
    connection = http.client.HTTPConnection(host, port, timeout=timeout)
    try:
        connection.request("GET", "/webclient/")
        response = connection.getresponse()
        body = response.read(MAX_RESPONSE_BYTES + 1)
    except (OSError, TimeoutError, http.client.HTTPException) as exc:
        raise ProtocolSmokeError(
            f"Webclient HTTP {host}:{port} could not be loaded: {exc}"
        ) from exc
    finally:
        connection.close()

    if response.status != 200:
        raise ProtocolSmokeError(
            f"Webclient HTTP {host}:{port} returned status {response.status}, not 200."
        )
    if len(body) > MAX_RESPONSE_BYTES:
        raise ProtocolSmokeError("Webclient page exceeded the one-megabyte smoke limit.")
    if b"webclient" not in body.lower():
        raise ProtocolSmokeError(
            "Webclient HTTP response did not contain the expected webclient surface."
        )
    if b"soravelon_oob.js" not in body:
        raise ProtocolSmokeError(
            "Webclient HTTP response did not load the Soravelon OOB "
            "compatibility bridge."
        )
    return (
        f"{host}:{port}/webclient/ webclient page returned HTTP 200 with "
        "the Soravelon OOB bridge"
    )


def _receive_http_headers(connection: socket.socket) -> tuple[bytes, bytes]:
    response = bytearray()
    delimiter = b"\r\n\r\n"
    while delimiter not in response:
        chunk = connection.recv(4096)
        if not chunk:
            raise ProtocolSmokeError("WebSocket closed during its HTTP handshake.")
        response.extend(chunk)
        if len(response) > 65_536:
            raise ProtocolSmokeError("WebSocket handshake headers exceeded 64 KiB.")
    header_block, remainder = bytes(response).split(delimiter, 1)
    return header_block, remainder


def _parse_http_headers(header_block: bytes) -> tuple[str, dict[str, str]]:
    try:
        lines = header_block.decode("ascii").split("\r\n")
        status_line = lines[0]
        headers = {
            key.strip().lower(): value.strip()
            for key, value in (line.split(":", 1) for line in lines[1:] if ":" in line)
        }
    except (UnicodeDecodeError, IndexError, ValueError) as exc:
        raise ProtocolSmokeError("WebSocket returned malformed HTTP headers.") from exc
    return status_line, headers


def _receive_websocket_text(reader: _BufferedSocket) -> str:
    while True:
        first, second = reader.read_exact(2)
        final = bool(first & 0x80)
        opcode = first & 0x0F
        masked = bool(second & 0x80)
        payload_length = second & 0x7F
        if not final:
            raise ProtocolSmokeError("Fragmented WebSocket frames are outside this smoke gate.")
        if masked:
            raise ProtocolSmokeError("The WebSocket server sent an illegally masked frame.")
        if payload_length == 126:
            payload_length = int.from_bytes(reader.read_exact(2), "big")
        elif payload_length == 127:
            payload_length = int.from_bytes(reader.read_exact(8), "big")
        if payload_length > MAX_RESPONSE_BYTES:
            raise ProtocolSmokeError("WebSocket frame exceeded the one-megabyte limit.")
        payload = reader.read_exact(payload_length)

        if opcode == 0x1:
            try:
                return payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ProtocolSmokeError("WebSocket text was not valid UTF-8.") from exc
        if opcode == 0x8:
            raise ProtocolSmokeError("WebSocket closed before the smoke gate completed.")
        if opcode == 0x9:
            reader.connection.sendall(_encode_client_control_frame(0xA, payload))
            continue
        if opcode == 0xA:
            continue
        raise ProtocolSmokeError(f"Unexpected WebSocket opcode {opcode}.")


def _encode_client_control_frame(opcode: int, payload: bytes) -> bytes:
    if len(payload) > 125:
        raise ValueError("WebSocket control payloads cannot exceed 125 bytes.")
    mask_key = os.urandom(4)
    masked_payload = bytes(
        value ^ mask_key[index % 4]
        for index, value in enumerate(payload)
    )
    return bytes((0x80 | opcode, 0x80 | len(payload))) + mask_key + masked_payload


def _encode_client_text_frame(
    text: str,
    *,
    mask_key: bytes | None = None,
) -> bytes:
    """Encode one RFC 6455 client text frame with mandatory masking."""
    payload = text.encode("utf-8")
    if mask_key is None:
        mask_key = os.urandom(4)
    if len(mask_key) != 4:
        raise ValueError("A WebSocket mask key must contain exactly four bytes.")

    payload_length = len(payload)
    if payload_length < 126:
        length_bytes = bytes((0x80 | payload_length,))
    elif payload_length <= 0xFFFF:
        length_bytes = bytes((0x80 | 126,)) + payload_length.to_bytes(2, "big")
    else:
        length_bytes = bytes((0x80 | 127,)) + payload_length.to_bytes(8, "big")

    masked_payload = bytes(
        value ^ mask_key[index % 4]
        for index, value in enumerate(payload)
    )
    return b"\x81" + length_bytes + mask_key + masked_payload


def _receive_banner_event(reader: _BufferedSocket, *, stage: str) -> None:
    for _attempt in range(32):
        raw_event = _receive_websocket_text(reader)
        try:
            event = json.loads(raw_event)
        except json.JSONDecodeError as exc:
            raise ProtocolSmokeError(
                f"WebSocket {stage} returned non-JSON text."
            ) from exc
        if not isinstance(event, list) or len(event) != 3:
            raise ProtocolSmokeError(
                f"WebSocket {stage} returned an invalid Evennia event envelope."
            )
        if event[0] == "text" and "S O R A V E L O N" in str(event[1]):
            return
    raise ProtocolSmokeError(
        f"WebSocket {stage} did not emit the Soravelon banner within 32 events."
    )


def verify_websocket(*, host: str, port: int, timeout: float) -> str:
    """Negotiate Evennia's real WebSocket protocol and round-trip ``look``."""
    websocket_key = base64.b64encode(os.urandom(16)).decode("ascii")
    expected_accept = base64.b64encode(
        hashlib.sha1(
            (websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode(
                "ascii"
            )
        ).digest()
    ).decode("ascii")
    request = (
        "GET /?protocol-smoke&1&codex HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {websocket_key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "Sec-WebSocket-Protocol: v1.evennia.com\r\n"
        "\r\n"
    ).encode("ascii")

    try:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            connection.settimeout(timeout)
            connection.sendall(request)
            header_block, remainder = _receive_http_headers(connection)
            status_line, headers = _parse_http_headers(header_block)
            if " 101 " not in f" {status_line} ":
                raise ProtocolSmokeError(
                    f"WebSocket handshake returned '{status_line}', not HTTP 101."
                )
            if headers.get("upgrade", "").lower() != "websocket":
                raise ProtocolSmokeError("WebSocket handshake omitted Upgrade: websocket.")
            if headers.get("sec-websocket-accept") != expected_accept:
                raise ProtocolSmokeError("WebSocket handshake accept hash was invalid.")
            if headers.get("sec-websocket-protocol") != "v1.evennia.com":
                raise ProtocolSmokeError(
                    "WebSocket did not negotiate Evennia's v1.evennia.com protocol."
                )

            reader = _BufferedSocket(connection, remainder)
            _receive_banner_event(reader, stage="login")
            connection.sendall(
                _encode_client_text_frame(json.dumps(["text", ["look"], {}]))
            )
            _receive_banner_event(reader, stage="look round-trip")
    except ProtocolSmokeError:
        raise
    except (OSError, TimeoutError) as exc:
        raise ProtocolSmokeError(
            f"WebSocket {host}:{port} did not complete the look round-trip: {exc}"
        ) from exc

    return f"{host}:{port} v1.evennia.com login banner and look round-trip"


def _port(raw_value: str) -> int:
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("port must be an integer") from exc
    if not 1 <= value <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return value


def _is_loopback_host(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Round-trip Soravelon's live Telnet and stock webclient protocols."
        )
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--telnet-port", type=_port, required=True)
    parser.add_argument("--web-port", type=_port, required=True)
    parser.add_argument("--websocket-port", type=_port, required=True)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="explicitly authorize network checks against a non-loopback host",
    )
    args = parser.parse_args(argv)

    if not _is_loopback_host(args.host) and not args.allow_remote:
        print(
            "FAIL remote protocol smoke requires explicit --allow-remote authority.",
            file=sys.stderr,
        )
        return 2
    if args.timeout <= 0:
        print("FAIL --timeout must be greater than zero.", file=sys.stderr)
        return 2

    checks = (
        (
            "telnet",
            verify_telnet,
            {"host": args.host, "port": args.telnet_port, "timeout": args.timeout},
        ),
        (
            "webclient HTTP",
            verify_webclient_http,
            {"host": args.host, "port": args.web_port, "timeout": args.timeout},
        ),
        (
            "websocket",
            verify_websocket,
            {
                "host": args.host,
                "port": args.websocket_port,
                "timeout": args.timeout,
            },
        ),
    )
    for name, check, kwargs in checks:
        try:
            detail = check(**kwargs)
        except ProtocolSmokeError as exc:
            print(f"FAIL {name}: {exc}", file=sys.stderr)
            return 1
        print(f"PASS {name}: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
