from django.core.exceptions import ValidationError
from .models import Task


def change_task_status(task: Task, new_status: str) -> None:
    """
    Change task status while enforcing workflow rules.
    """

    if task.status == Task.STATUS_PENDING and new_status == Task.STATUS_COMPLETED:
        raise ValidationError(
            "Task cannot be completed directly from Pending state."
        )

    task.status = new_status
    task.full_clean()
    task.save(update_fields=["status"])


def soft_delete_task(task: Task) -> None:
    """
    Soft delete a task instead of removing it from database.
    """
    task.is_deleted = True
    task.save(update_fields=["is_deleted"])
