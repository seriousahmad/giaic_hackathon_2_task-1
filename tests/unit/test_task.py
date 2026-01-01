import pytest
from datetime import datetime
from src.models.task import Task, Priority, Recurrence


class TestTaskModel:
    """Unit tests for the Task model validation."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            priority=Priority.MEDIUM,
            tags=["test", "example"],
            due_date=datetime(2023, 12, 31),
            recurrence=Recurrence.NONE
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.tags == ["test", "example"]
        assert task.due_date == datetime(2023, 12, 31)
        assert task.recurrence == Recurrence.NONE

    def test_task_creation_with_minimal_data(self):
        """Test creating a task with minimal required data."""
        task = Task(id=1, title="Minimal Task")

        assert task.id == 1
        assert task.title == "Minimal Task"
        assert task.description is None
        assert task.completed is False
        assert task.priority == Priority.MEDIUM  # Default value
        assert task.tags == []  # Default value
        assert task.due_date is None  # Default value
        assert task.recurrence == Recurrence.NONE  # Default value

    def test_task_creation_fails_with_empty_title(self):
        """Test that creating a task with an empty title raises an error."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="")

    def test_task_creation_fails_with_none_title(self):
        """Test that creating a task with a None title raises an error."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title=None)

    def test_task_creation_fails_with_whitespace_only_title(self):
        """Test that creating a task with whitespace-only title raises an error."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="   ")

    def test_task_priority_validation(self):
        """Test that priority validation works correctly."""
        # Valid priorities should work
        task = Task(id=1, title="Test", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH

        task = Task(id=1, title="Test", priority=Priority.MEDIUM)
        assert task.priority == Priority.MEDIUM

        task = Task(id=1, title="Test", priority=Priority.LOW)
        assert task.priority == Priority.LOW

        # Invalid priority should raise an error
        with pytest.raises(ValueError):
            Task(id=1, title="Test", priority="INVALID")

    def test_task_tags_validation(self):
        """Test that tags validation works correctly."""
        # Valid tags should work
        task = Task(id=1, title="Test", tags=["tag1", "tag2"])
        assert task.tags == ["tag1", "tag2"]

        # Empty tags list should work
        task = Task(id=1, title="Test", tags=[])
        assert task.tags == []

        # Non-list tags should raise an error
        with pytest.raises(ValueError):
            Task(id=1, title="Test", tags="not_a_list")

        # Non-string tags should raise an error
        with pytest.raises(ValueError):
            Task(id=1, title="Test", tags=["valid", 123])

    def test_task_recurrence_validation(self):
        """Test that recurrence validation works correctly."""
        # Valid recurrences should work
        task = Task(id=1, title="Test", recurrence=Recurrence.DAILY)
        assert task.recurrence == Recurrence.DAILY

        task = Task(id=1, title="Test", recurrence=Recurrence.WEEKLY)
        assert task.recurrence == Recurrence.WEEKLY

        task = Task(id=1, title="Test", recurrence=Recurrence.MONTHLY)
        assert task.recurrence == Recurrence.MONTHLY

        task = Task(id=1, title="Test", recurrence=Recurrence.NONE)
        assert task.recurrence == Recurrence.NONE

        # Invalid recurrence should raise an error
        with pytest.raises(ValueError):
            Task(id=1, title="Test", recurrence="INVALID")

    def test_task_due_date_validation(self):
        """Test that due date validation works correctly."""
        # Valid due date should work
        dt = datetime(2023, 12, 31)
        task = Task(id=1, title="Test", due_date=dt)
        assert task.due_date == dt

        # None due date should work
        task = Task(id=1, title="Test", due_date=None)
        assert task.due_date is None

        # Invalid due date should raise an error
        with pytest.raises(ValueError):
            Task(id=1, title="Test", due_date="not_a_datetime")

    def test_toggle_completion(self):
        """Test toggling task completion status."""
        task = Task(id=1, title="Test Task", completed=False)
        assert task.completed is False

        # Toggle to completed
        new_status = task.toggle_completion()
        assert new_status is True
        assert task.completed is True

        # Toggle back to incomplete
        new_status = task.toggle_completion()
        assert new_status is False
        assert task.completed is False

    def test_update_attributes(self):
        """Test updating task attributes."""
        task = Task(id=1, title="Original Title")

        # Update title
        task.update_attributes(title="New Title")
        assert task.title == "New Title"

        # Update multiple attributes
        task.update_attributes(
            description="Updated Description",
            priority=Priority.HIGH,
            completed=True
        )
        assert task.description == "Updated Description"
        assert task.priority == Priority.HIGH
        assert task.completed is True

    def test_update_attributes_with_string_priority(self):
        """Test updating task priority with string value."""
        task = Task(id=1, title="Test Task")

        # Update priority with string
        task.update_attributes(priority="high")
        assert task.priority == Priority.HIGH

        task.update_attributes(priority="medium")
        assert task.priority == Priority.MEDIUM

        task.update_attributes(priority="low")
        assert task.priority == Priority.LOW

    def test_update_attributes_with_string_recurrence(self):
        """Test updating task recurrence with string value."""
        task = Task(id=1, title="Test Task")

        # Update recurrence with string
        task.update_attributes(recurrence="daily")
        assert task.recurrence == Recurrence.DAILY

        task.update_attributes(recurrence="weekly")
        assert task.recurrence == Recurrence.WEEKLY

        task.update_attributes(recurrence="monthly")
        assert task.recurrence == Recurrence.MONTHLY

        task.update_attributes(recurrence="none")
        assert task.recurrence == Recurrence.NONE

    def test_priority_assignment_and_validation(self):
        """Test priority assignment and validation."""
        # Test creating task with different priorities
        task_high = Task(id=1, title="Test", priority=Priority.HIGH)
        assert task_high.priority == Priority.HIGH

        task_medium = Task(id=2, title="Test", priority=Priority.MEDIUM)
        assert task_medium.priority == Priority.MEDIUM

        task_low = Task(id=3, title="Test", priority=Priority.LOW)
        assert task_low.priority == Priority.LOW

        # Test updating priority
        task = Task(id=4, title="Test")
        assert task.priority == Priority.MEDIUM  # Default value

        task.update_attributes(priority=Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_tag_management(self):
        """Test tag management functionality."""
        # Test creating task with tags
        task = Task(id=1, title="Test", tags=["work", "important"])
        assert "work" in task.tags
        assert "important" in task.tags
        assert len(task.tags) == 2

        # Test updating tags
        task.update_attributes(tags=["home", "personal"])
        assert "home" in task.tags
        assert "personal" in task.tags
        assert "work" not in task.tags
        assert "important" not in task.tags
        assert len(task.tags) == 2

        # Test adding to existing tags
        current_tags = task.tags.copy()
        current_tags.append("urgent")
        task.update_attributes(tags=current_tags)
        assert "urgent" in task.tags
        assert len(task.tags) == 3