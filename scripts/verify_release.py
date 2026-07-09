"""One executable owner for Soravelon's automated release verification."""

from __future__ import annotations

import argparse
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


def _python_command(*args: str) -> tuple[str, ...]:
    return (sys.executable, *args)


def _preflight_steps() -> list[ReleaseStep]:
    return [
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


def _test_step(shard: str | None = None) -> ReleaseStep:
    command = list(_python_command("scripts/run_tests.py"))
    if shard:
        command.extend(_test_labels_for_shard(shard))
    return ReleaseStep("Canonical tests", tuple(command))


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


def build_release_steps(mode: str, shard: str | None = None) -> list[ReleaseStep]:
    if mode == "preflight":
        if shard:
            raise ValueError("--shard is valid only for full or tests mode.")
        return _preflight_steps()
    if mode == "tests":
        return [_test_step(shard)]
    if mode == "full":
        return [*_preflight_steps(), _test_step(shard)]
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
        choices=("full", "preflight", "tests", "reconcile"),
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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.mode == "reconcile":
        if args.shard or args.dry_run:
            _build_parser().error("reconcile mode does not accept --shard or --dry-run")
        return _run_reconciliation()
    try:
        steps = build_release_steps(args.mode, args.shard)
    except ValueError as exc:
        _build_parser().error(str(exc))
    return execute_steps(steps, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
