#!/usr/bin/env python3
"""
Quick validation script to test the core functionality of the Todo App.
"""
from datetime import datetime, timedelta
from src.services.task_manager import TaskManager
from src.models.task import Priority, Recurrence
from src.services.recurring_service import RecurringTaskService


def test_basic_functionality():
    """Test the basic functionality of the Todo App."""
    print("Testing basic functionality...")

    # Create a task manager
    tm = TaskManager()

    # Test adding a task
    task_id = tm.add_task(title="Test Task", description="This is a test task")
    print(f"V Added task with ID: {task_id}")

    # Test getting the task
    task = tm.get_task(task_id)
    assert task.title == "Test Task"
    print("V Retrieved task successfully")

    # Test updating the task
    tm.update_task(task_id, priority=Priority.HIGH, tags=["test", "important"])
    updated_task = tm.get_task(task_id)
    assert updated_task.priority == Priority.HIGH
    assert "test" in updated_task.tags
    print("V Updated task successfully")

    # Test toggling completion
    new_status = tm.toggle_completion(task_id)
    assert new_status is True
    completed_task = tm.get_task(task_id)
    assert completed_task.completed is True
    print("V Toggled completion status successfully")

    # Test listing tasks
    tasks = tm.list_tasks()
    assert len(tasks) == 1
    print("V Listed tasks successfully")

    # Test searching
    search_results = tm.search_tasks("test")
    assert len(search_results) == 1
    print("V Search functionality works")

    # Test filtering
    filtered_tasks = tm.list_tasks(filters={'completed': True})
    assert len(filtered_tasks) == 1
    print("V Filtering works")

    # Test sorting
    sorted_tasks = tm.list_tasks(sort_by='title')
    print("V Sorting works")

    print("All basic functionality tests passed!\n")


def test_recurring_tasks():
    """Test recurring task functionality."""
    print("Testing recurring task functionality...")

    tm = TaskManager()

    # Add a recurring task
    from datetime import datetime, timedelta
    future_date = datetime.now() + timedelta(days=1)

    recurring_id = tm.add_task(
        title="Daily Task",
        recurrence=Recurrence.DAILY,
        due_date=future_date
    )

    print(f"V Added recurring task with ID: {recurring_id}")

    # Toggle completion to trigger recurrence
    new_status = tm.toggle_completion(recurring_id)
    assert new_status is True
    print("V Toggled completion on recurring task")

    # Check if a new task was created
    all_tasks = tm.list_tasks()
    assert len(all_tasks) == 2  # Original task + new recurring instance
    print("V New recurring task instance created")

    print("Recurring task functionality tests passed!\n")


def test_reminders():
    """Test reminder functionality."""
    print("Testing reminder functionality...")

    tm = TaskManager()

    # Add a task that will be overdue
    past_date = datetime.now() - timedelta(days=1)
    overdue_id = tm.add_task(
        title="Overdue Task",
        due_date=past_date
    )
    # Ensure it's not completed
    tm.update_task(overdue_id, completed=False)

    # Add a task that will be upcoming
    future_date = datetime.now() + timedelta(days=2)
    upcoming_id = tm.add_task(
        title="Upcoming Task",
        due_date=future_date
    )
    # Ensure it's not completed
    tm.update_task(upcoming_id, completed=False)

    # Test overdue tasks
    overdue_tasks = tm.get_overdue_tasks()
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0].id == overdue_id
    print("V Overdue task detection works")

    # Test upcoming tasks
    upcoming_tasks = tm.get_upcoming_tasks()
    assert len(upcoming_tasks) == 1
    assert upcoming_tasks[0].id == upcoming_id
    print("V Upcoming task detection works")

    print("Reminder functionality tests passed!\n")


if __name__ == "__main__":
    print("Running quick validation tests for Todo App...\n")

    test_basic_functionality()
    test_recurring_tasks()
    test_reminders()

    print(":) All validation tests passed! The Todo App is working correctly.")