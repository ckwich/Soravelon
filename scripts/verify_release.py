"""One executable owner for Soravelon's automated release verification."""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFY_RELEASE = Path(__file__).resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@dataclass(frozen=True)
class ReleaseStep:
    name: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class ReleaseCandidateInputs:
    expected_database_name: str
    test_database_name: str
    git_commit: str
    protocol_host: str
    telnet_port: int
    web_port: int
    websocket_port: int
    allow_remote_protocol: bool = False

    def __post_init__(self) -> None:
        if re.fullmatch(
            r"soravelon_rehearsal_[a-z0-9][a-z0-9_]{0,62}",
            self.expected_database_name,
        ) is None:
            raise ValueError(
                "Candidate database must use the soravelon_rehearsal_* "
                "disposable naming contract."
            )
        if (
            re.fullmatch(
                r"test_soravelon_rehearsal_[a-z0-9][a-z0-9_]*",
                self.test_database_name,
            )
            is None
            or len(self.test_database_name) > 63
        ):
            raise ValueError(
                "Candidate test database must use the "
                "test_soravelon_rehearsal_* disposable naming contract."
            )
        if re.fullmatch(r"[0-9a-f]{7,64}", self.git_commit) is None:
            raise ValueError(
                "Candidate Git commit must be a 7-64 character lowercase "
                "hexadecimal object ID."
            )
        if not self.protocol_host.strip():
            raise ValueError("Candidate protocol host cannot be empty.")
        ports = (self.telnet_port, self.web_port, self.websocket_port)
        if any(not 1 <= port <= 65535 for port in ports):
            raise ValueError("Candidate protocol ports must be between 1 and 65535.")
        if len(set(ports)) != len(ports):
            raise ValueError("Candidate protocol ports must be distinct.")


def _python_command(*args: str) -> tuple[str, ...]:
    return (sys.executable, *args)


def _git_integrity_step() -> ReleaseStep:
    return ReleaseStep(
        "Git object integrity",
        ("git", "fsck", "--full", "--no-reflogs"),
    )


def _preflight_steps() -> list[ReleaseStep]:
    return [
        _git_integrity_step(),
        ReleaseStep(
            "Repository hygiene",
            _python_command("scripts/audit_repo_hygiene.py"),
        ),
        ReleaseStep("Working-tree diff check", ("git", "diff", "--check")),
        ReleaseStep(
            "Staged diff check",
            ("git", "diff", "--cached", "--check"),
        ),
        ReleaseStep(
            "World migration drift",
            _python_command(
                "-m",
                "django",
                "makemigrations",
                "world",
                "--check",
                "--dry-run",
                "--settings=server.conf.settings",
            ),
        ),
        ReleaseStep(
            "Fresh database migration",
            _python_command(
                "-m",
                "django",
                "migrate",
                "--noinput",
                "--settings=server.conf.settings",
            ),
        ),
        ReleaseStep(
            "Production deployment check",
            _python_command(
                "-m",
                "django",
                "check",
                "--deploy",
                "--fail-level",
                "WARNING",
                "--settings=server.conf.settings",
            ),
        ),
        ReleaseStep(
            "Smoke imports",
            _python_command("scripts/smoke_start.py"),
        ),
        ReleaseStep(
            "Economy and inventory reconciliation",
            _python_command(str(VERIFY_RELEASE), "reconcile"),
        ),
    ]


def _test_step(
    shard: str | None = None,
    *,
    keepdb: bool = False,
) -> ReleaseStep:
    command = list(_python_command("scripts/run_tests.py"))
    if keepdb:
        command.append("--keepdb")
    if shard:
        command.extend(_test_labels_for_shard(shard))
    return ReleaseStep("Canonical tests", tuple(command))


def _candidate_steps(candidate: ReleaseCandidateInputs) -> list[ReleaseStep]:
    protocol_command = list(
        _python_command(
            "scripts/smoke_protocols.py",
            "--host",
            candidate.protocol_host,
            "--telnet-port",
            str(candidate.telnet_port),
            "--web-port",
            str(candidate.web_port),
            "--websocket-port",
            str(candidate.websocket_port),
            "--forwarded-https",
        )
    )
    if candidate.allow_remote_protocol:
        protocol_command.append("--allow-remote")
    prepared_content_step = ReleaseStep(
        "Prepared world-content verification",
        _python_command(
            "scripts/rehearse_content_release.py",
            "--database-kind",
            "prepared",
            "--expected-database-name",
            candidate.expected_database_name,
            "--git-commit",
            candidate.git_commit,
            "--format",
            "json",
        ),
    )
    preflight = _preflight_steps()
    return [
        preflight[0],
        prepared_content_step,
        *preflight[1:],
        ReleaseStep(
            "Playable world connectivity",
            _python_command("scripts/audit_world_connectivity.py"),
        ),
        ReleaseStep(
            "Authored content prose",
            _python_command("scripts/audit_content_prose.py"),
        ),
        ReleaseStep(
            "Transactional failure injection",
            _python_command(
                "scripts/run_tests.py",
                "--keepdb",
                "tests.test_content_revisions.TestWorldContentApplyLifecycle.test_injected_failure_rolls_back_runtime_and_persists_failure",
                "tests.test_economy_transactions.TestAtomicCashAndBankOperations.test_deposit_rolls_back_after_every_write",
                "tests.test_inventory_transactions.TestAtomicPickup.test_pickup_rolls_back_location_and_ownership_after_every_write",
                "tests.test_quest_outcomes.TestAtomicQuestOutcomes.test_failure_after_outcome_writes_rolls_back_every_effect",
            ),
        ),
        ReleaseStep(
            "Release gameplay verticals",
            _python_command(
                "scripts/run_tests.py",
                "--keepdb",
                "tests.test_m3_golden_path",
                "tests.test_m4_living_world_vertical",
                "tests.test_social_web_warden_route",
                "tests.test_cooperative_combat_vertical",
            ),
        ),
        _test_step(keepdb=True),
        ReleaseStep("Live player protocols", tuple(protocol_command)),
    ]


def _parse_shard(shard: str) -> tuple[int, int]:
    try:
        raw_index, raw_total = shard.split("/", 1)
        index = int(raw_index)
        total = int(raw_total)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Shard must use the form INDEX/TOTAL, for example 1/4.") from exc
    if total < 1 or index < 1 or index > total:
        raise ValueError("Shard INDEX must be between 1 and TOTAL.")
    return index, total


def _discover_test_labels() -> list[str]:
    return [
        f"tests.{path.stem}"
        for path in sorted((REPO_ROOT / "tests").glob("test_*.py"))
    ]


def _test_labels_for_shard(shard: str) -> list[str]:
    index, total = _parse_shard(shard)
    labels = _discover_test_labels()
    selected = [
        label
        for position, label in enumerate(labels)
        if position % total == index - 1
    ]
    if not selected:
        raise ValueError(f"Shard {shard} contains no test modules.")
    return selected


def build_release_steps(
    mode: str,
    shard: str | None = None,
    *,
    candidate: ReleaseCandidateInputs | None = None,
) -> list[ReleaseStep]:
    if mode == "preflight":
        if shard:
            raise ValueError("--shard is valid only for full or tests mode.")
        return _preflight_steps()
    if mode == "tests":
        return [_test_step(shard)]
    if mode == "full":
        return [*_preflight_steps(), _test_step(shard)]
    if mode == "candidate":
        if candidate is None:
            raise ValueError("Release candidate inputs are required for candidate mode.")
        if shard:
            raise ValueError("Release candidate verification must be unsharded.")
        return _candidate_steps(candidate)
    raise ValueError(f"Mode '{mode}' does not have a command plan.")


def execute_steps(
    steps: Sequence[ReleaseStep],
    *,
    dry_run: bool = False,
) -> int:
    for position, step in enumerate(steps, start=1):
        command_text = shlex.join(step.command)
        print(f"[{position}/{len(steps)}] {step.name}: {command_text}", flush=True)
        if dry_run:
            continue
        result = subprocess.run(
            step.command,
            cwd=REPO_ROOT,
            check=False,
        )
        if result.returncode != 0:
            print(
                f"Release verification FAILED at '{step.name}' "
                f"(exit {result.returncode}).",
                file=sys.stderr,
            )
            return result.returncode or 1
    if dry_run:
        print("Dry run only: no verification commands were executed.")
    else:
        print("Automated release verification passed.")
    print(
        "TLS, DNS, reverse-proxy behavior, and systemd lifecycle remain "
        "external host proofs."
    )
    return 0


def find_reconciliation_issues(
    *,
    accounts: Sequence[Any],
    transactions: Sequence[Any],
    inventory_items: Sequence[Any],
    objects_by_id: Mapping[int, Any],
) -> list[str]:
    """Return ID-only economy and inventory persistence contradictions."""
    issues: list[str] = []
    accounts_by_character = {
        account.character_id: account for account in accounts
    }
    transactions_by_character: dict[int, list[Any]] = {}
    for transaction in transactions:
        transactions_by_character.setdefault(transaction.character_id, []).append(
            transaction
        )
        if transaction.character_id not in accounts_by_character:
            issues.append(
                f"transaction id={transaction.id} has no bank account for "
                f"character_id={transaction.character_id}"
            )

    for character_id, account in sorted(accounts_by_character.items()):
        if account.balance < 0:
            issues.append(
                f"account character_id={character_id} has negative balance"
            )
        ledger = sorted(
            transactions_by_character.get(character_id, ()),
            key=lambda transaction: transaction.id,
        )
        running_balance = 0
        for transaction in ledger:
            running_balance += transaction.amount
            if transaction.balance_after != running_balance:
                issues.append(
                    f"transaction id={transaction.id} balance_after disagrees "
                    "with ledger order"
                )
        if running_balance != account.balance:
            issues.append(
                f"account character_id={character_id} balance disagrees with ledger"
            )

    inventory_by_item_id: dict[int, Any] = {}
    for record in inventory_items:
        if record.item_id in inventory_by_item_id:
            issues.append(
                f"inventory id={record.id} duplicates item_id={record.item_id}"
            )
        inventory_by_item_id[record.item_id] = record

    for record in inventory_items:
        prefix = f"inventory id={record.id}"
        if record.quantity < 1:
            issues.append(f"{prefix} has non-positive quantity")

        item_object = objects_by_id.get(record.item_id)
        if item_object is None:
            issues.append(f"{prefix} references missing item_id={record.item_id}")
        elif getattr(item_object, "db_location_id", None) != record.character_id:
            issues.append(f"{prefix} item location disagrees with character ownership")

        if record.is_equipped:
            if not record.equipment_slot:
                issues.append(f"{prefix} is equipped without an equipment slot")
            if record.container_id is not None:
                issues.append(f"{prefix} is both equipped and contained")
        elif record.equipment_slot:
            issues.append(f"{prefix} has an equipment slot while not equipped")

        if record.container_id is not None:
            if record.container_id not in objects_by_id:
                issues.append(
                    f"{prefix} references missing container_id={record.container_id}"
                )
            container_record = inventory_by_item_id.get(record.container_id)
            if container_record is None:
                issues.append(
                    f"{prefix} container_id={record.container_id} is not owned"
                )
            elif container_record.character_id != record.character_id:
                issues.append(f"{prefix} container belongs to another character")

    return sorted(set(issues))


def _load_reconciliation_state() -> tuple[list[Any], list[Any], list[Any], dict[int, Any]]:
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
    import django

    django.setup()

    from evennia.objects.models import ObjectDB
    from world.models import BankAccount, BankTransaction, InventoryItem

    accounts = list(BankAccount.objects.order_by("character_id"))
    transactions = list(BankTransaction.objects.order_by("character_id", "id"))
    inventory_items = list(InventoryItem.objects.order_by("id"))
    object_ids = {
        object_id
        for record in inventory_items
        for object_id in (record.item_id, record.container_id)
        if object_id is not None
    }
    objects_by_id = ObjectDB.objects.in_bulk(object_ids)
    return accounts, transactions, inventory_items, objects_by_id


def _run_reconciliation() -> int:
    accounts, transactions, inventory_items, objects_by_id = (
        _load_reconciliation_state()
    )
    issues = find_reconciliation_issues(
        accounts=accounts,
        transactions=transactions,
        inventory_items=inventory_items,
        objects_by_id=objects_by_id,
    )
    if issues:
        print(
            f"Economy/inventory reconciliation FAILED: {len(issues)} issue(s)",
            file=sys.stderr,
        )
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print("Economy/inventory reconciliation passed.")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        nargs="?",
        default="full",
        choices=("full", "preflight", "tests", "reconcile", "candidate"),
    )
    parser.add_argument(
        "--shard",
        help="Run one deterministic canonical-test shard as INDEX/TOTAL.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selected command plan without executing it.",
    )
    parser.add_argument(
        "--expected-database-name",
        help="Candidate-only exact soravelon_rehearsal_* database name.",
    )
    parser.add_argument(
        "--test-database-name",
        help=(
            "Candidate-only pre-created "
            "test_soravelon_rehearsal_* database name."
        ),
    )
    parser.add_argument("--git-commit", help="Candidate-only Git object identity.")
    parser.add_argument(
        "--protocol-host",
        help="Candidate-only live Evennia protocol host.",
    )
    parser.add_argument("--telnet-port", type=int, help="Candidate-only Telnet port.")
    parser.add_argument("--web-port", type=int, help="Candidate-only HTTP port.")
    parser.add_argument(
        "--websocket-port",
        type=int,
        help="Candidate-only WebSocket port.",
    )
    parser.add_argument(
        "--allow-remote-protocol",
        action="store_true",
        help="Explicitly permit candidate protocol checks beyond loopback.",
    )
    return parser


def _candidate_inputs_from_args(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> ReleaseCandidateInputs | None:
    candidate_values = {
        "expected_database_name": args.expected_database_name,
        "test_database_name": args.test_database_name,
        "git_commit": args.git_commit,
        "protocol_host": args.protocol_host,
        "telnet_port": args.telnet_port,
        "web_port": args.web_port,
        "websocket_port": args.websocket_port,
    }
    if args.mode != "candidate":
        if any(value is not None for value in candidate_values.values()) or (
            args.allow_remote_protocol
        ):
            parser.error("candidate inputs are valid only in candidate mode")
        return None

    missing = [name for name, value in candidate_values.items() if value is None]
    if missing:
        parser.error(
            "candidate mode requires: "
            + ", ".join(f"--{name.replace('_', '-')}" for name in missing)
        )
    for name in ("telnet_port", "web_port", "websocket_port"):
        value = candidate_values[name]
        if not 1 <= value <= 65535:
            parser.error(f"--{name.replace('_', '-')} must be between 1 and 65535")
    try:
        return ReleaseCandidateInputs(
            **candidate_values,
            allow_remote_protocol=args.allow_remote_protocol,
        )
    except ValueError as exc:
        parser.error(str(exc))


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    candidate = _candidate_inputs_from_args(parser, args)
    if candidate is not None:
        os.environ["DATABASE_TEST_NAME"] = candidate.test_database_name
    if args.mode == "reconcile":
        if args.shard or args.dry_run:
            parser.error("reconcile mode does not accept --shard or --dry-run")
        return _run_reconciliation()
    try:
        steps = build_release_steps(args.mode, args.shard, candidate=candidate)
    except ValueError as exc:
        parser.error(str(exc))
    return execute_steps(steps, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
