from typing import Dict, List, Optional, Tuple
from datetime import datetime
from src.models.task import Task, Priority, Recurrence
from src.lib.errors import TaskNotFound, ValidationError
from src.services.recurring_service import RecurringTaskService


class TaskManager:
    """
    Service entity responsible for managing the collection of tasks in memory.

    Responsibilities:
    - Maintaining the in-memory collection of tasks
    - Generating unique IDs for new tasks
    - Performing CRUD operations on tasks
    - Implementing search functionality across task titles and descriptions
    - Implementing filtering functionality based on various criteria
    - Implementing sorting functionality based on various criteria
    - Handling recurring task rescheduling
    """

    def __init__(self):
        """Initialize the task manager with an empty task collection."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1
        self.recurring_service = RecurringTaskService()

    def add_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence: Optional[Recurrence] = Recurrence.NONE
    ) -> int:
        """
        Create a new task and return its ID.

        Args:
            title: Required title of the task
            description: Optional description of the task
            priority: Priority level of the task (default: MEDIUM)
            tags: List of tags for the task (default: empty list)
            due_date: Optional due date and time for the task
            recurrence: Optional recurrence pattern for the task (default: NONE)

        Returns:
            int: The unique ID of the created task

        Raises:
            ValidationError: If required fields are invalid
        """
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        if tags is None:
            tags = []

        # Create a new task with a unique ID
        task_id = self.next_id
        self.next_id += 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )

        self.tasks[task_id] = task
        return task_id

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task object

        Raises:
            TaskNotFound: If task doesn't exist
        """
        if task_id not in self.tasks:
            raise TaskNotFound(f"Task with ID {task_id} does not exist")
        return self.tasks[task_id]

    def update_task(self, task_id: int, **updates) -> bool:
        """
        Update properties of an existing task.

        Args:
            task_id: The ID of the task to update
            **updates: The attributes to update

        Returns:
            bool: Success boolean

        Raises:
            TaskNotFound: If task doesn't exist
        """
        if task_id not in self.tasks:
            raise TaskNotFound(f"Task with ID {task_id} does not exist")

        task = self.tasks[task_id]
        original_completed = task.completed
        task.update_attributes(**updates)

        # Handle recurring tasks when they're marked as completed
        if 'completed' in updates and updates['completed'] is True and original_completed is False:
            if task.recurrence != Recurrence.NONE:
                # Create the next occurrence of the recurring task
                next_task = self.recurring_service.create_next_occurrence(task)
                if next_task:
                    # Assign a new ID to the next occurrence
                    next_task.id = self.next_id
                    self.next_id += 1
                    self.tasks[next_task.id] = next_task

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the collection.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: Success boolean

        Raises:
            TaskNotFound: If task doesn't exist
        """
        if task_id not in self.tasks:
            raise TaskNotFound(f"Task with ID {task_id} does not exist")

        del self.tasks[task_id]
        return True

    def list_tasks(
        self,
        filters: Optional[Dict] = None,
        sort_by: Optional[str] = None
    ) -> List[Task]:
        """
        Retrieve multiple tasks with optional filtering and sorting.

        Args:
            filters: Optional filters to apply
            sort_by: Optional sort parameter

        Returns:
            List[Task]: List of Task objects
        """
        tasks = list(self.tasks.values())

        # Apply filters if provided
        if filters:
            tasks = self._apply_filters(tasks, filters)

        # Apply sorting if provided
        if sort_by:
            tasks = self._apply_sorting(tasks, sort_by)

        return tasks

    def toggle_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            bool: New completion status

        Raises:
            TaskNotFound: If task doesn't exist
        """
        if task_id not in self.tasks:
            raise TaskNotFound(f"Task with ID {task_id} does not exist")

        task = self.tasks[task_id]
        original_completed = task.completed
        new_status = task.toggle_completion()

        # Handle recurring tasks when they're marked as completed
        if new_status is True and original_completed is False:
            if task.recurrence != Recurrence.NONE:
                # Create the next occurrence of the recurring task
                next_task = self.recurring_service.create_next_occurrence(task)
                if next_task:
                    # Assign a new ID to the next occurrence
                    next_task.id = self.next_id
                    self.next_id += 1
                    self.tasks[next_task.id] = next_task

        return new_status

    def search_tasks(self, query: str) -> List[Task]:
        """
        Find tasks by keyword in title or description.

        Args:
            query: Search query string

        Returns:
            List[Task]: List of matching Task objects
        """
        if not query:
            return []

        query_lower = query.lower()
        matching_tasks = []

        for task in self.tasks.values():
            if query_lower in task.title.lower() or \
               (task.description and query_lower in task.description.lower()):
                matching_tasks.append(task)

        return matching_tasks

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """
        Get tasks that are due within the specified number of days.

        Args:
            days: Number of days to look ahead (default: 7)

        Returns:
            List[Task]: List of tasks due within the specified number of days
        """
        from datetime import timedelta
        now = datetime.now()
        future_date = now + timedelta(days=days)

        upcoming_tasks = []
        for task in self.tasks.values():
            if task.due_date and not task.completed:
                if now <= task.due_date <= future_date:
                    upcoming_tasks.append(task)

        return upcoming_tasks

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get tasks that are overdue (due date has passed and not completed).

        Returns:
            List[Task]: List of overdue tasks
        """
        now = datetime.now()

        overdue_tasks = []
        for task in self.tasks.values():
            if task.due_date and not task.completed:
                if task.due_date < now:
                    overdue_tasks.append(task)

        return overdue_tasks

    def _apply_filters(self, tasks: List[Task], filters: Dict) -> List[Task]:
        """Apply filters to a list of tasks."""
        filtered_tasks = []

        for task in tasks:
            match = True

            # Filter by completion status
            if 'completed' in filters:
                if filters['completed'] != task.completed:
                    match = False

            # Filter by priority
            if 'priority' in filters:
                if isinstance(filters['priority'], str):
                    priority = Priority(filters['priority'].title())
                else:
                    priority = filters['priority']

                if priority != task.priority:
                    match = False

            # Filter by tag
            if 'tag' in filters:
                tag = filters['tag']
                if tag not in task.tags:
                    match = False

            # Filter by due date range
            if 'due_date_from' in filters or 'due_date_to' in filters:
                if task.due_date:
                    if 'due_date_from' in filters and task.due_date < filters['due_date_from']:
                        match = False
                    if 'due_date_to' in filters and task.due_date > filters['due_date_to']:
                        match = False
                else:
                    # If task has no due date but filter is applied, exclude it
                    if 'due_date_from' in filters or 'due_date_to' in filters:
                        match = False

            if match:
                filtered_tasks.append(task)

        return filtered_tasks

    def _apply_sorting(self, tasks: List[Task], sort_by: str) -> List[Task]:
        """Apply sorting to a list of tasks."""
        if sort_by == 'due_date_asc':
            return sorted(tasks, key=lambda t: (t.due_date is None, t.due_date))
        elif sort_by == 'due_date_desc':
            return sorted(tasks, key=lambda t: (t.due_date is not None, t.due_date), reverse=True)
        elif sort_by == 'priority':
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            return sorted(tasks, key=lambda t: priority_order[t.priority])
        elif sort_by == 'title':
            return sorted(tasks, key=lambda t: t.title.lower())
        else:
            # Default: sort by ID
            return sorted(tasks, key=lambda t: t.id)