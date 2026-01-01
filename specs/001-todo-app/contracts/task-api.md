# API Contracts: In-Memory Console Todo App

## Task Management Endpoints

### Add Task
- **Operation**: `add_task(title: str, description: str = None, priority: str = "Medium", tags: list[str] = None, due_date: datetime = None, recurrence: str = None) -> int`
- **Purpose**: Create a new task and return its ID
- **Input**: Task details as specified
- **Output**: Unique task ID (int)
- **Errors**: ValidationError if required fields are invalid

### Get Task
- **Operation**: `get_task(task_id: int) -> Task`
- **Purpose**: Retrieve a specific task by ID
- **Input**: Task ID
- **Output**: Task object
- **Errors**: TaskNotFound if task doesn't exist

### Update Task
- **Operation**: `update_task(task_id: int, **updates) -> bool`
- **Purpose**: Update properties of an existing task
- **Input**: Task ID and update parameters
- **Output**: Success boolean
- **Errors**: TaskNotFound if task doesn't exist

### Delete Task
- **Operation**: `delete_task(task_id: int) -> bool`
- **Purpose**: Remove a task from the collection
- **Input**: Task ID
- **Output**: Success boolean
- **Errors**: TaskNotFound if task doesn't exist

### List Tasks
- **Operation**: `list_tasks(filters: dict = None, sort_by: str = None) -> list[Task]`
- **Purpose**: Retrieve multiple tasks with optional filtering and sorting
- **Input**: Optional filters and sort parameters
- **Output**: List of Task objects
- **Errors**: None

### Toggle Completion
- **Operation**: `toggle_completion(task_id: int) -> bool`
- **Purpose**: Toggle the completion status of a task
- **Input**: Task ID
- **Output**: New completion status
- **Errors**: TaskNotFound if task doesn't exist

### Search Tasks
- **Operation**: `search_tasks(query: str) -> list[Task]`
- **Purpose**: Find tasks by keyword in title or description
- **Input**: Search query string
- **Output**: List of matching Task objects
- **Errors**: None