#!/usr/bin/env python
"""Reject templated or player-facing meta prose in authored room content."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import sys
from typing import Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from world.content_compiler import (  # noqa: E402
    _operation_value,
    compile_world_sources,
)


MAX_SENTENCE_REUSE = 3
MIN_REPEATED_SENTENCE_LENGTH = 24
DEFAULT_PROSE_ALLOWLIST = frozenset()

META_PROSE_PATTERNS = (
    ("player", re.compile(r"\bplayers?\b", re.IGNORECASE)),
    ("this-part-of", re.compile(r"\bthis part of\b", re.IGNORECASE)),
    (
        "production-language",
        re.compile(
            r"\b(?:gameplay|playtest|quest hook|player-facing content)\b",
            re.IGNORECASE,
        ),
    ),
    ("grounded-in-play", re.compile(r"\bgrounded in play\b", re.IGNORECASE)),
    (
        "reward-system",
        re.compile(
            r"\brewards? (?:exploration|investigation|gathering)\b",
            re.IGNORECASE,
        ),
    ),
    ("not-a-lecture", re.compile(r"\bnot a lecture\b", re.IGNORECASE)),
)


class ProseAuditError(RuntimeError):
    """Raised when source cannot first satisfy the content compiler."""


@dataclass(frozen=True)
class RoomProse:
    source_path: str
    line: int
    room_id: str
    text: str


@dataclass(frozen=True)
class ProseFinding:
    source_path: str
    line: int
    room_id: str
    code: str
    message: str
    allowlist_key: str


@dataclass(frozen=True)
class ProseAudit:
    findings: tuple[ProseFinding, ...]


def _normalize_text(text):
    return " ".join(str(text or "").split()).strip().casefold()


def _fingerprint(text):
    return hashlib.sha256(_normalize_text(text).encode("utf-8")).hexdigest()[:16]


def _sentences(text):
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
        if sentence.strip()
    ]


def _room_prose_from_sources(sources):
    compilation = compile_world_sources(sources)
    if compilation.diagnostics:
        details = "; ".join(
            f"{item.source_path}:{item.line} [{item.code}] {item.message}"
            for item in compilation.diagnostics
        )
        raise ProseAuditError(f"Content compilation failed before prose audit: {details}")

    rooms = []
    for zone in compilation.manifest.zones:
        for operation in zone.operations:
            if operation.method != "room" or not operation.arguments:
                continue
            room_id = operation.arguments[0]
            description = _operation_value(operation, 2, "desc", "")
            if not isinstance(room_id, str) or not isinstance(description, str):
                continue
            rooms.append(
                RoomProse(
                    source_path=operation.source_path,
                    line=operation.line,
                    room_id=room_id,
                    text=description,
                )
            )
    return tuple(rooms)


def _meta_findings(rooms):
    findings = []
    for room in rooms:
        for pattern_name, pattern in META_PROSE_PATTERNS:
            match = pattern.search(room.text)
            if not match:
                continue
            findings.append(
                ProseFinding(
                    source_path=room.source_path,
                    line=room.line,
                    room_id=room.room_id,
                    code="meta-prose",
                    message=(
                        f"Room description uses author-facing phrase "
                        f"{match.group(0)!r}."
                    ),
                    allowlist_key=(
                        f"meta-prose:{room.source_path}:{room.room_id}:{pattern_name}"
                    ),
                )
            )
    return findings


def _duplicate_description_findings(rooms):
    grouped = defaultdict(list)
    for room in rooms:
        normalized = _normalize_text(room.text)
        if normalized:
            grouped[normalized].append(room)

    findings = []
    for normalized, duplicates in grouped.items():
        if len(duplicates) < 2:
            continue
        first = duplicates[0]
        room_list = ", ".join(
            f"{room.source_path}:{room.room_id}" for room in duplicates
        )
        findings.append(
            ProseFinding(
                source_path=first.source_path,
                line=first.line,
                room_id=first.room_id,
                code="duplicate-description",
                message=f"Exact room description is shared by: {room_list}.",
                allowlist_key=f"duplicate-description:{_fingerprint(normalized)}",
            )
        )
    return findings


def _repeated_sentence_findings(rooms):
    grouped = defaultdict(list)
    originals = {}
    for room in rooms:
        seen_in_room = set()
        for sentence in _sentences(room.text):
            normalized = _normalize_text(sentence)
            if (
                len(normalized) < MIN_REPEATED_SENTENCE_LENGTH
                or normalized in seen_in_room
            ):
                continue
            seen_in_room.add(normalized)
            grouped[normalized].append(room)
            originals.setdefault(normalized, sentence)

    findings = []
    for normalized, occurrences in grouped.items():
        if len(occurrences) <= MAX_SENTENCE_REUSE:
            continue
        first = occurrences[0]
        findings.append(
            ProseFinding(
                source_path=first.source_path,
                line=first.line,
                room_id=first.room_id,
                code="repeated-sentence",
                message=(
                    f"Sentence appears in {len(occurrences)} room descriptions "
                    f"(maximum {MAX_SENTENCE_REUSE}): {originals[normalized]!r}."
                ),
                allowlist_key=f"repeated-sentence:{_fingerprint(normalized)}",
            )
        )
    return findings


def audit_prose_sources(
    sources: Mapping[str, str],
    *,
    allowlist=DEFAULT_PROSE_ALLOWLIST,
):
    """Audit literal area sources and return non-allowlisted findings."""

    rooms = _room_prose_from_sources(sources)
    findings = [
        *_meta_findings(rooms),
        *_duplicate_description_findings(rooms),
        *_repeated_sentence_findings(rooms),
    ]
    allowed = frozenset(allowlist)
    return ProseAudit(
        findings=tuple(
            sorted(
                (
                    finding
                    for finding in findings
                    if finding.allowlist_key not in allowed
                ),
                key=lambda finding: (
                    finding.source_path,
                    finding.line,
                    finding.code,
                    finding.allowlist_key,
                ),
            )
        )
    )


def audit_prose_directory(areas_dir: Path, *, allowlist=DEFAULT_PROSE_ALLOWLIST):
    """Audit every literal Python area source in deterministic path order."""

    project_root = areas_dir.parents[1]
    sources = {
        path.relative_to(project_root).as_posix(): path.read_text()
        for path in sorted(areas_dir.glob("*.py"))
        if not path.name.startswith("_")
    }
    return audit_prose_sources(sources, allowlist=allowlist)


def main():
    areas_dir = PROJECT_ROOT / "world" / "areas"
    try:
        audit = audit_prose_directory(areas_dir)
    except ProseAuditError as exc:
        print(f"Content prose audit ERROR: {exc}", file=sys.stderr)
        return 2
    if not audit.findings:
        print("Content prose audit OK: no scaffold or repeated room prose")
        return 0

    print(f"Content prose audit FAILED: {len(audit.findings)} finding(s)")
    for finding in audit.findings:
        print(
            f"{finding.source_path}:{finding.line} "
            f"[{finding.code}] {finding.room_id}: {finding.message} "
            f"(allowlist: {finding.allowlist_key})"
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
