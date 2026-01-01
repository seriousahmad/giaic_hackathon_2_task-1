# Quickstart Guide: In-Memory Console Todo App

## Overview
This guide provides instructions for getting started with the In-Memory Console Todo App, a command-line application for managing tasks with priorities, tags, search, and recurring functionality.

## Prerequisites
- Python 3.12 or higher
- UV package manager (for dependency management)

## Installation
1. Clone or download the project repository
2. Navigate to the project directory
3. Install dependencies using UV:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

## Running the Application
Execute the main application file:
```bash
python -m src.cli.console_ui
```

## Basic Usage
1. **Adding a Task**: Use the "Add Task" command and provide a title and optional details
2. **Viewing Tasks**: Use the "View Tasks" command to see all tasks
3. **Completing Tasks**: Use the "Complete Task" command with the task ID
4. **Searching Tasks**: Use the "Search" command with a keyword
5. **Filtering and Sorting**: Use available filter and sort options from the main menu

## Key Features
- Add, update, delete, and view tasks
- Mark tasks as complete/incomplete
- Assign priorities (High, Medium, Low) and tags
- Search tasks by keyword
- Filter tasks by status, priority, tags, or due date
- Sort tasks by due date, priority, or alphabetically
- Recurring tasks that automatically reschedule when completed
- Console-based reminders for due and overdue tasks

## Example Workflow
1. Start the application
2. Add a new task: "Buy groceries" with due date and "shopping" tag
3. View all tasks to confirm it was added
4. Mark the task as complete when done
5. Search for tasks containing "groceries" to find the task again if needed

## Troubleshooting
- If the application fails to start, ensure Python 3.12+ is installed
- If commands don't work, check that you're using the correct syntax as prompted
- For any errors, the application will display helpful error messages instead of raw stack traces