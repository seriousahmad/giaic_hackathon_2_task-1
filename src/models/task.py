from datetime import datetime
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, field

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Recurrence(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NONE = None

@dataclass
class Task:
    """
    The core entity representing a todo item in the application.

    Attributes:
        id: Unique identifier for the task (auto-incrementing integer)
        title: Required title of the task (cannot be empty)
        description: Optional description of the task (can be None or empty string)
        completed: Boolean indicating if the task is completed (default: False)
        priority: Priority level of the task (values: "High", "Medium", "Low"; default: "Medium")
        tags: List of tags/categories for the task (default: empty list)
        due_date: Optional due date and time for the task (can be None)
        recurrence: Optional recurrence pattern for the task (values: "daily", "weekly", "monthly", None; default: None)
        created_at: Timestamp when the task was created (auto-set)
        updated_at: Timestamp when the task was last updated (auto-updated)
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    recurrence: Optional[Recurrence] = Recurrence.NONE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the task after initialization."""
        self.validate()
        # Set updated_at to current time after any changes
        self.updated_at = datetime.now()

    def validate(self):
        """Validate the task attributes according to the specification."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or None")

        if self.priority not in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            raise ValueError(f"Priority must be one of {[Priority.HIGH, Priority.MEDIUM, Priority.LOW]}")

        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list of strings")

        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError("All tags must be strings")

        if self.due_date is not None and not isinstance(self.due_date, datetime):
            raise ValueError("Due date must be a datetime object or None")

        if self.recurrence not in [Recurrence.DAILY, Recurrence.WEEKLY, Recurrence.MONTHLY, Recurrence.NONE]:
            raise ValueError(f"Recurrence must be one of {[Recurrence.DAILY, Recurrence.WEEKLY, Recurrence.MONTHLY, Recurrence.NONE]}")

    def toggle_completion(self) -> bool:
        """Toggle the completion status of the task."""
        self.completed = not self.completed
        self.updated_at = datetime.now()
        return self.completed

    def update_attributes(self, **kwargs):
        """Update task attributes with validation."""
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                if attr == 'priority' and value is not None:
                    if isinstance(value, str):
                        value = Priority(value.title())
                    elif not isinstance(value, Priority):
                        raise ValueError(f"Priority must be a Priority enum or string")
                elif attr == 'recurrence' and value is not None:
                    if isinstance(value, str):
                        value = Recurrence(value.lower()) if value.lower() in ['daily', 'weekly', 'monthly'] else Recurrence.NONE
                    elif not isinstance(value, Recurrence):
                        raise ValueError(f"Recurrence must be a Recurrence enum or string")
                elif attr == 'tags' and value is not None:
                    if not isinstance(value, list):
                        raise ValueError("Tags must be a list of strings")

                setattr(self, attr, value)

        self.updated_at = datetime.now()
        self.validate()