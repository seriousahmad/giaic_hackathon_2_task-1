from datetime import datetime
from typing import Union
import re


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string into a datetime object.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime: Parsed datetime object

    Raises:
        ValueError: If the date string format is not recognized
    """
    # Common date formats to try
    formats = [
        "%Y-%m-%d",           # 2023-12-25
        "%Y-%m-%d %H:%M",     # 2023-12-25 14:30
        "%Y-%m-%d %H:%M:%S",  # 2023-12-25 14:30:00
        "%m/%d/%Y",           # 12/25/2023
        "%m/%d/%Y %H:%M",     # 12/25/2023 14:30
        "%m/%d/%Y %H:%M:%S",  # 12/25/2023 14:30:00
        "%d/%m/%Y",           # 25/12/2023
        "%d/%m/%Y %H:%M",     # 25/12/2023 14:30
        "%d/%m/%Y %H:%M:%S",  # 25/12/2023 14:30:00
        "%B %d, %Y",          # December 25, 2023
        "%b %d, %Y",          # Dec 25, 2023
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    # If none of the standard formats work, try to extract date with regex
    # Pattern for YYYY-MM-DD
    pattern = r"(\d{4})-(\d{1,2})-(\d{1,2})"
    match = re.search(pattern, date_str)
    if match:
        year, month, day = map(int, match.groups())
        return datetime(year, month, day)

    raise ValueError(f"Unable to parse date string: {date_str}")


def format_task_display(task) -> str:
    """
    Format a task for display in the console.

    Args:
        task: Task object to format

    Returns:
        str: Formatted task string for display
    """
    status = "[✓]" if task.completed else "[ ]"
    priority_str = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)

    result = f"{status} [{task.id}] {task.title} (Priority: {priority_str}"

    if task.tags:
        result += f", Tags: {', '.join(task.tags)}"

    if task.due_date:
        result += f", Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"

    result += ")"

    if task.description:
        result += f"\n    Description: {task.description}"

    return result


def validate_task_title(title: str) -> bool:
    """
    Validate a task title according to the specification.

    Args:
        title: Title to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not title or not title.strip():
        return False

    # Check if title is too long (optional validation)
    if len(title.strip()) > 200:  # Arbitrary limit
        return False

    return True


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection or other issues.

    Args:
        user_input: Raw user input

    Returns:
        str: Sanitized input
    """
    if user_input is None:
        return ""

    # Strip leading/trailing whitespace
    sanitized = user_input.strip()

    # Replace multiple whitespace with single space
    sanitized = ' '.join(sanitized.split())

    return sanitized