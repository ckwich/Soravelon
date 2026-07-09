"""Exactly-once receipts shared by composite gameplay workflows."""

from world.economy_ids import new_operation_id
from world.models import GameOperation


class GameOperationConflict(RuntimeError):
    """An operation ID was reused for a materially different effect."""


def normalize_operation_id(value=None):
    operation_id = new_operation_id() if value is None else value
    if not isinstance(operation_id, str) or not operation_id.strip():
        raise ValueError("operation_id must be a non-empty string")
    if len(operation_id) > 128:
        raise ValueError("operation_id cannot exceed 128 characters")
    return operation_id


def get_operation_replay(
    *,
    character,
    operation_id,
    operation_type,
    related_id,
):
    """Return a locked matching receipt or raise on key reuse."""

    receipt = GameOperation.objects.select_for_update().filter(
        operation_id=operation_id,
    ).first()
    if not receipt:
        return None
    if (
        receipt.character_ref != character.id
        or receipt.operation_type != operation_type
        or receipt.related_id != related_id
    ):
        raise GameOperationConflict(
            f"operation_id '{operation_id}' was already used for another effect"
        )
    return receipt


def record_operation(
    *,
    character,
    operation_id,
    operation_type,
    related_id,
    result,
):
    """Record a completed composite effect inside its owning transaction."""

    return GameOperation.objects.create(
        operation_id=operation_id,
        character_id=character.id,
        character_ref=character.id,
        operation_type=operation_type,
        related_id=related_id,
        result=result,
    )
