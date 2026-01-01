"""
Custom error classes for the In-Memory Console Todo App.
"""


class TaskError(Exception):
    """Base exception class for task-related errors."""
    pass


class TaskNotFound(TaskError):
    """Raised when a requested task does not exist."""
    pass


class ValidationError(TaskError):
    """Raised when validation of task attributes fails."""
    pass


class DuplicateTaskError(TaskError):
    """Raised when trying to create a duplicate task."""
    pass


class InvalidTaskOperationError(TaskError):
    """Raised when an invalid operation is attempted on a task."""
    pass