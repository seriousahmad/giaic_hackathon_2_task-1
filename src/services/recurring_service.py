from datetime import datetime, timedelta
from typing import Optional
from src.models.task import Task, Recurrence


class RecurringTaskService:
    """
    Service for handling recurring tasks.

    Responsibilities:
    - Creating new task instances when recurring tasks are marked complete
    - Calculating new due dates based on recurrence patterns
    - Managing the lifecycle of recurring tasks
    """

    def __init__(self):
        """Initialize the recurring task service."""
        pass

    def calculate_next_occurrence(self, task: Task) -> Optional[datetime]:
        """
        Calculate the next occurrence date for a recurring task.

        Args:
            task: The recurring task

        Returns:
            datetime: The next occurrence date, or None if task is not recurring
        """
        if not task.due_date:
            return None

        if task.recurrence == Recurrence.NONE:
            return None

        if task.recurrence == Recurrence.DAILY:
            return task.due_date + timedelta(days=1)
        elif task.recurrence == Recurrence.WEEKLY:
            return task.due_date + timedelta(weeks=1)
        elif task.recurrence == Recurrence.MONTHLY:
            # For monthly recurrence, add 1 month
            # This handles month boundaries appropriately
            current_date = task.due_date
            next_month = current_date.month + 1
            next_year = current_date.year

            if next_month > 12:
                next_month = 1
                next_year += 1

            # Handle days that don't exist in all months (e.g., Jan 31 -> Feb 31 doesn't exist)
            import calendar
            max_day = calendar.monthrange(next_year, next_month)[1]
            day = min(current_date.day, max_day)

            return current_date.replace(year=next_year, month=next_month, day=day)

        return None

    def create_next_occurrence(self, task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task.

        Args:
            task: The recurring task that was completed

        Returns:
            Task: A new task instance with updated due date, or None if not recurring
        """
        if task.recurrence == Recurrence.NONE:
            return None

        next_due_date = self.calculate_next_occurrence(task)
        if not next_due_date:
            return None

        # Create a new task with the same properties but updated due date
        # The new task will have a new ID, reset completion status, and updated timestamps
        from src.models.task import Task, Priority
        new_task = Task(
            id=0,  # Will be assigned a new ID by the task manager
            title=task.title,
            description=task.description,
            completed=False,  # New occurrence starts as incomplete
            priority=task.priority,
            tags=task.tags.copy(),  # Copy the tags
            due_date=next_due_date,
            recurrence=task.recurrence,  # Keep the same recurrence pattern
            # created_at will be set to current time by __post_init__
            # updated_at will be set to current time by __post_init__
        )

        return new_task