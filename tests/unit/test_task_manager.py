import pytest
from datetime import datetime
from src.services.task_manager import TaskManager
from src.models.task import Task, Priority, Recurrence
from src.lib.errors import TaskNotFound, ValidationError


class TestTaskManagerCRUD:
    """Unit tests for TaskManager CRUD operations."""

    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    def test_add_task_success(self):
        """Test successfully adding a task."""
        task_id = self.manager.add_task(
            title="Test Task",
            description="Test Description",
            priority=Priority.HIGH,
            tags=["test", "example"],
            due_date=datetime(2023, 12, 31),
            recurrence=Recurrence.NONE
        )

        assert task_id == 1
        assert len(self.manager.tasks) == 1

        task = self.manager.get_task(task_id)
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == Priority.HIGH
        assert task.tags == ["test", "example"]
        assert task.due_date == datetime(2023, 12, 31)
        assert task.recurrence == Recurrence.NONE

    def test_add_task_with_minimal_data(self):
        """Test adding a task with minimal required data."""
        task_id = self.manager.add_task(title="Minimal Task")

        assert task_id == 1
        task = self.manager.get_task(task_id)
        assert task.title == "Minimal Task"
        assert task.description is None
        assert task.priority == Priority.MEDIUM
        assert task.tags == []
        assert task.due_date is None
        assert task.recurrence == Recurrence.NONE

    def test_add_task_fails_with_empty_title(self):
        """Test that adding a task with empty title raises an error."""
        with pytest.raises(ValidationError, match="Task title cannot be empty"):
            self.manager.add_task(title="")

    def test_get_task_success(self):
        """Test successfully retrieving a task."""
        task_id = self.manager.add_task(title="Test Task")
        task = self.manager.get_task(task_id)

        assert task.id == task_id
        assert task.title == "Test Task"

    def test_get_task_fails_with_nonexistent_id(self):
        """Test that retrieving a non-existent task raises an error."""
        with pytest.raises(TaskNotFound, match="Task with ID 999 does not exist"):
            self.manager.get_task(999)

    def test_update_task_success(self):
        """Test successfully updating a task."""
        task_id = self.manager.add_task(
            title="Original Title",
            description="Original Description"
        )

        # Update the task
        success = self.manager.update_task(
            task_id,
            title="Updated Title",
            description="Updated Description",
            priority=Priority.HIGH
        )

        assert success is True

        # Verify the updates
        updated_task = self.manager.get_task(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == Priority.HIGH

    def test_update_task_fails_with_nonexistent_id(self):
        """Test that updating a non-existent task raises an error."""
        with pytest.raises(TaskNotFound, match="Task with ID 999 does not exist"):
            self.manager.update_task(999, title="Updated Title")

    def test_delete_task_success(self):
        """Test successfully deleting a task."""
        task_id = self.manager.add_task(title="Test Task")
        assert len(self.manager.tasks) == 1

        success = self.manager.delete_task(task_id)
        assert success is True
        assert len(self.manager.tasks) == 0

    def test_delete_task_fails_with_nonexistent_id(self):
        """Test that deleting a non-existent task raises an error."""
        with pytest.raises(TaskNotFound, match="Task with ID 999 does not exist"):
            self.manager.delete_task(999)

    def test_list_tasks_empty(self):
        """Test listing tasks when there are no tasks."""
        tasks = self.manager.list_tasks()
        assert tasks == []

    def test_list_tasks_all(self):
        """Test listing all tasks."""
        task_id1 = self.manager.add_task(title="Task 1")
        task_id2 = self.manager.add_task(title="Task 2")

        tasks = self.manager.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].id in [task_id1, task_id2]
        assert tasks[1].id in [task_id1, task_id2]
        assert tasks[0].id != tasks[1].id

    def test_toggle_completion_success(self):
        """Test successfully toggling task completion."""
        task_id = self.manager.add_task(title="Test Task", completed=False)

        # Toggle to completed
        new_status = self.manager.toggle_completion(task_id)
        assert new_status is True

        task = self.manager.get_task(task_id)
        assert task.completed is True

        # Toggle back to incomplete
        new_status = self.manager.toggle_completion(task_id)
        assert new_status is False

        task = self.manager.get_task(task_id)
        assert task.completed is False

    def test_toggle_completion_fails_with_nonexistent_id(self):
        """Test that toggling completion of a non-existent task raises an error."""
        with pytest.raises(TaskNotFound, match="Task with ID 999 does not exist"):
            self.manager.toggle_completion(999)

    def test_search_tasks_by_title(self):
        """Test searching tasks by title."""
        task_id1 = self.manager.add_task(title="Buy groceries")
        task_id2 = self.manager.add_task(title="Walk the dog")
        task_id3 = self.manager.add_task(title="Clean the house")

        # Search for "groceries"
        results = self.manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].id == task_id1

        # Search for "the" (should match "the" in "the dog" and "the house")
        results = self.manager.search_tasks("the")
        assert len(results) == 2
        result_ids = [task.id for task in results]
        assert task_id2 in result_ids
        assert task_id3 in result_ids

    def test_search_tasks_by_description(self):
        """Test searching tasks by description."""
        task_id1 = self.manager.add_task(
            title="Task 1",
            description="This is a task about groceries"
        )
        task_id2 = self.manager.add_task(
            title="Task 2",
            description="This is a task about walking"
        )

        # Search for "groceries" in description
        results = self.manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].id == task_id1

    def test_search_tasks_case_insensitive(self):
        """Test that search is case insensitive."""
        task_id = self.manager.add_task(title="Buy GROCERIES")

        results = self.manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].id == task_id

    def test_search_tasks_empty_query(self):
        """Test that empty search query returns empty list."""
        self.manager.add_task(title="Test Task")

        results = self.manager.search_tasks("")
        assert results == []

        results = self.manager.search_tasks(None)
        assert results == []

    def test_toggle_completion_success(self):
        """Test successfully toggling task completion."""
        task_id = self.manager.add_task(title="Test Task", completed=False)

        # Toggle to completed
        new_status = self.manager.toggle_completion(task_id)
        assert new_status is True

        task = self.manager.get_task(task_id)
        assert task.completed is True

        # Toggle back to incomplete
        new_status = self.manager.toggle_completion(task_id)
        assert new_status is False

        task = self.manager.get_task(task_id)
        assert task.completed is False

    def test_toggle_completion_fails_with_nonexistent_id(self):
        """Test that toggling completion of a non-existent task raises an error."""
        with pytest.raises(TaskNotFound, match="Task with ID 999 does not exist"):
            self.manager.toggle_completion(999)


class TestTaskManagerFilters:
    """Unit tests for TaskManager filtering functionality."""

    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

        # Add some test tasks
        self.task1_id = self.manager.add_task(
            title="Task 1",
            completed=False,
            priority=Priority.HIGH
        )
        self.task2_id = self.manager.add_task(
            title="Task 2",
            completed=True,
            priority=Priority.MEDIUM
        )
        self.task3_id = self.manager.add_task(
            title="Task 3",
            completed=False,
            priority=Priority.LOW,
            tags=["work"]
        )

    def test_filter_by_completion_status(self):
        """Test filtering tasks by completion status."""
        # Filter for completed tasks
        completed_tasks = self.manager.list_tasks(filters={'completed': True})
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == self.task2_id

        # Filter for incomplete tasks
        incomplete_tasks = self.manager.list_tasks(filters={'completed': False})
        assert len(incomplete_tasks) == 2
        task_ids = [task.id for task in incomplete_tasks]
        assert self.task1_id in task_ids
        assert self.task3_id in task_ids

    def test_filter_by_priority(self):
        """Test filtering tasks by priority."""
        # Filter for high priority tasks
        high_priority_tasks = self.manager.list_tasks(filters={'priority': Priority.HIGH})
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].id == self.task1_id

        # Filter for medium priority tasks
        medium_priority_tasks = self.manager.list_tasks(filters={'priority': Priority.MEDIUM})
        assert len(medium_priority_tasks) == 1
        assert medium_priority_tasks[0].id == self.task2_id

    def test_filter_by_tag(self):
        """Test filtering tasks by tag."""
        # Filter for tasks with "work" tag
        work_tasks = self.manager.list_tasks(filters={'tag': "work"})
        assert len(work_tasks) == 1
        assert work_tasks[0].id == self.task3_id

    def test_multiple_filters(self):
        """Test applying multiple filters."""
        # Filter for incomplete AND high priority tasks
        filtered_tasks = self.manager.list_tasks(
            filters={'completed': False, 'priority': Priority.HIGH}
        )
        assert len(filtered_tasks) == 1
        assert filtered_tasks[0].id == self.task1_id


class TestTaskManagerSorting:
    """Unit tests for TaskManager sorting functionality."""

    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    def test_sort_by_title(self):
        """Test sorting tasks by title."""
        # Add tasks in non-alphabetical order
        task3_id = self.manager.add_task(title="Zebra Task")
        task1_id = self.manager.add_task(title="Apple Task")
        task2_id = self.manager.add_task(title="Banana Task")

        # Sort by title (ascending)
        sorted_tasks = self.manager.list_tasks(sort_by='title')
        titles = [task.title for task in sorted_tasks]
        assert titles == ["Apple Task", "Banana Task", "Zebra Task"]

    def test_sort_by_priority(self):
        """Test sorting tasks by priority."""
        # Add tasks with different priorities
        low_task_id = self.manager.add_task(title="Low Priority", priority=Priority.LOW)
        high_task_id = self.manager.add_task(title="High Priority", priority=Priority.HIGH)
        medium_task_id = self.manager.add_task(title="Medium Priority", priority=Priority.MEDIUM)

        # Sort by priority (High to Low)
        sorted_tasks = self.manager.list_tasks(sort_by='priority')
        priorities = [task.priority for task in sorted_tasks]
        expected_priorities = [Priority.HIGH, Priority.MEDIUM, Priority.LOW]
        assert priorities == expected_priorities

    def test_search_functionality(self):
        """Test searching tasks by keyword."""
        # Add test tasks
        task1_id = self.manager.add_task(
            title="Buy groceries",
            description="Get milk, bread, and eggs"
        )
        task2_id = self.manager.add_task(
            title="Walk the dog",
            description="Take Max for a long walk"
        )
        task3_id = self.manager.add_task(
            title="Clean the house",
            description="Vacuum and dust all rooms"
        )

        # Search for "groceries" in title
        results = self.manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].id == task1_id

        # Search for "milk" in description
        results = self.manager.search_tasks("milk")
        assert len(results) == 1
        assert results[0].id == task1_id

        # Search for "the" which appears in both "the dog" and "the house"
        results = self.manager.search_tasks("the")
        assert len(results) == 2
        result_ids = [task.id for task in results]
        assert task2_id in result_ids
        assert task3_id in result_ids

        # Search case insensitive
        results = self.manager.search_tasks("GROCERIES")
        assert len(results) == 1
        assert results[0].id == task1_id

        # Search for non-existent term
        results = self.manager.search_tasks("nonexistent")
        assert len(results) == 0

        # Empty search
        results = self.manager.search_tasks("")
        assert len(results) == 0

    def test_filter_functionality(self):
        """Test filtering tasks by various criteria."""
        # Add test tasks with different attributes
        task1_id = self.manager.add_task(
            title="Urgent Task",
            completed=False,
            priority=Priority.HIGH,
            tags=["work", "urgent"]
        )
        task2_id = self.manager.add_task(
            title="Completed Task",
            completed=True,
            priority=Priority.MEDIUM,
            tags=["personal"]
        )
        task3_id = self.manager.add_task(
            title="Low Priority Task",
            completed=False,
            priority=Priority.LOW,
            tags=["later"]
        )

        # Filter by completion status (completed)
        completed_tasks = self.manager.list_tasks(filters={'completed': True})
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task2_id

        # Filter by completion status (incomplete)
        incomplete_tasks = self.manager.list_tasks(filters={'completed': False})
        assert len(incomplete_tasks) == 2
        incomplete_ids = [task.id for task in incomplete_tasks]
        assert task1_id in incomplete_ids
        assert task3_id in incomplete_ids

        # Filter by priority (HIGH)
        high_priority_tasks = self.manager.list_tasks(filters={'priority': Priority.HIGH})
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].id == task1_id

        # Filter by tag
        work_tasks = self.manager.list_tasks(filters={'tag': "work"})
        assert len(work_tasks) == 1
        assert work_tasks[0].id == task1_id

        # Filter by multiple criteria
        incomplete_high_tasks = self.manager.list_tasks(
            filters={'completed': False, 'priority': Priority.HIGH}
        )
        assert len(incomplete_high_tasks) == 1
        assert incomplete_high_tasks[0].id == task1_id

    def test_sort_functionality(self):
        """Test sorting tasks by various criteria."""
        # Add tasks in non-sorted order
        task_low = self.manager.add_task(title="Low Priority", priority=Priority.LOW)
        task_high = self.manager.add_task(title="High Priority", priority=Priority.HIGH)
        task_medium = self.manager.add_task(title="Medium Priority", priority=Priority.MEDIUM)

        # Sort by priority (High to Low)
        sorted_tasks = self.manager.list_tasks(sort_by='priority')
        priorities = [task.priority for task in sorted_tasks]
        expected_priorities = [Priority.HIGH, Priority.MEDIUM, Priority.LOW]
        assert priorities == expected_priorities

        # Add tasks for title sorting
        task_z = self.manager.add_task(title="Zebra Task")
        task_a = self.manager.add_task(title="Apple Task")
        task_m = self.manager.add_task(title="Monkey Task")

        # Sort by title
        sorted_tasks = self.manager.list_tasks(sort_by='title')
        titles = [task.title for task in sorted_tasks]
        expected_titles = ["Apple Task", "High Priority", "Low Priority", "Medium Priority", "Monkey Task", "Zebra Task"]
        assert titles == expected_titles

        # Add tasks with due dates for date sorting
        from datetime import datetime
        future_task = self.manager.add_task(
            title="Future Task",
            due_date=datetime(2024, 12, 31)
        )
        past_task = self.manager.add_task(
            title="Past Task",
            due_date=datetime(2023, 1, 1)
        )
        no_date_task = self.manager.add_task(title="No Date Task")

        # Sort by due date ascending (earliest first, None values last)
        sorted_tasks = self.manager.list_tasks(sort_by='due_date_asc')
        # The exact order will depend on how None values are handled
        # In our implementation, None values come last due to the sort key
        due_dates = [task.due_date for task in sorted_tasks]
        # Filter out tasks without due dates for comparison
        actual_dates = [dt for dt in due_dates if dt is not None]
        expected_dates = [datetime(2023, 1, 1), datetime(2024, 12, 31)]
        assert actual_dates == expected_dates

        # Sort by due date descending (latest first)
        sorted_tasks = self.manager.list_tasks(sort_by='due_date_desc')
        due_dates = [task.due_date for task in sorted_tasks]
        actual_dates = [dt for dt in due_dates if dt is not None]
        expected_dates = [datetime(2024, 12, 31), datetime(2023, 1, 1)]  # Reversed
        assert actual_dates == expected_dates