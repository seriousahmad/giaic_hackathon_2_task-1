# Data Model: In-Memory Console Todo App

## Task Entity

**Name**: Task
**Description**: The core entity representing a todo item in the application

### Fields
- `id` (int): Unique identifier for the task (auto-incrementing integer)
- `title` (str): Required title of the task (cannot be empty)
- `description` (str): Optional description of the task (can be None or empty string)
- `completed` (bool): Boolean indicating if the task is completed (default: False)
- `priority` (str): Priority level of the task (values: "High", "Medium", "Low"; default: "Medium")
- `tags` (list[str]): List of tags/categories for the task (default: empty list)
- `due_date` (datetime): Optional due date and time for the task (can be None)
- `recurrence` (str): Optional recurrence pattern for the task (values: "daily", "weekly", "monthly", None; default: None)
- `created_at` (datetime): Timestamp when the task was created (auto-set)
- `updated_at` (datetime): Timestamp when the task was last updated (auto-updated)

### Validation Rules
- `title` must not be empty or None
- `priority` must be one of "High", "Medium", or "Low"
- `tags` must be a list of strings
- `due_date` must be a valid datetime object or None
- `recurrence` must be one of "daily", "weekly", "monthly", or None

### State Transitions
- A task can transition from `completed=False` to `completed=True` when marked as done
- A task can transition from `completed=True` to `completed=False` when unmarked
- When a recurring task is marked as completed, a new task instance is created with an updated due date based on the recurrence pattern

## TaskManager Entity

**Name**: TaskManager
**Description**: Service entity responsible for managing the collection of tasks in memory

### Responsibilities
- Maintaining the in-memory collection of tasks
- Generating unique IDs for new tasks
- Performing CRUD operations on tasks
- Implementing search functionality across task titles and descriptions
- Implementing filtering functionality based on various criteria
- Implementing sorting functionality based on various criteria
- Handling recurring task rescheduling

### Internal Structure
- `tasks` (dict[int, Task]): Dictionary mapping task IDs to Task objects
- `next_id` (int): Counter for generating unique task IDs

## Enums

### Priority Enum
- Values: HIGH, MEDIUM, LOW
- Used for the priority field in Task entity

### Recurrence Enum
- Values: DAILY, WEEKLY, MONTHLY, NONE
- Used for the recurrence field in Task entity

## Relationships
- TaskManager contains multiple Task entities (one-to-many relationship)
- Each Task has a single TaskManager that manages it