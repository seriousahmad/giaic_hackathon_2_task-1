from typing import Optional, List
from datetime import datetime
from src.services.task_manager import TaskManager
from src.models.task import Task, Priority, Recurrence
from src.lib.utils import parse_date, format_task_display, validate_task_title, sanitize_input
from src.lib.errors import TaskNotFound, ValidationError


class ConsoleUI:
    """
    Console interface and user interaction handler.

    Handles all user interactions through the console, including:
    - Menu-driven navigation
    - Command input processing
    - Task display formatting
    - User prompts and confirmations
    """

    def __init__(self):
        """Initialize the console UI with a task manager."""
        self.task_manager = TaskManager()
        self.running = True

    def run(self):
        """Main application loop."""
        print("Welcome to the In-Memory Console Todo App!")
        print("Type 'help' for available commands.")

        while self.running:
            try:
                command = input("\n> ").strip().lower()
                self.process_command(command)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    def process_command(self, command: str):
        """Process a user command."""
        if command in ['quit', 'exit', 'q']:
            self.running = False
        elif command in ['help', 'h', '?']:
            self.show_help()
        elif command.startswith('add'):
            self.handle_add_task(command)
        elif command.startswith('list') or command == 'ls':
            self.handle_list_tasks(command)
        elif command.startswith('view'):
            self.handle_view_task(command)
        elif command.startswith('update'):
            self.handle_update_task(command)
        elif command.startswith('delete') or command.startswith('remove'):
            self.handle_delete_task(command)
        elif command.startswith('complete') or command.startswith('done'):
            self.handle_toggle_completion(command)
        elif command.startswith('search'):
            self.handle_search_tasks(command)
        elif command.startswith('menu'):
            self.show_menu()
        elif command.startswith('overdue'):
            self.handle_overdue_tasks()
        elif command.startswith('upcoming') or command.startswith('due'):
            self.handle_upcoming_tasks()
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    def show_help(self):
        """Display help information."""
        help_text = """
Available commands:
  add [title] - Add a new task
  list [options] - List all tasks (options: --completed, --incomplete, --priority=HIGH/MEDIUM/LOW)
  view [id] - View details of a specific task
  update [id] [field=value] - Update a task (e.g., update 1 title=New Title)
  delete [id] - Delete a task
  complete [id] - Toggle task completion status
  search [query] - Search tasks by keyword
  overdue - Show overdue tasks
  upcoming/due - Show upcoming tasks
  menu - Show menu options
  help - Show this help
  quit/exit/q - Exit the application
        """
        print(help_text.strip())

    def show_menu(self):
        """Display menu options."""
        menu_text = """
Menu Options:
  1. Add Task
  2. List Tasks
  3. View Task
  4. Update Task
  5. Delete Task
  6. Toggle Task Completion
  7. Search Tasks
  8. Show Overdue Tasks
  9. Show Upcoming Tasks
  10. Help
  11. Exit
        """
        print(menu_text.strip())

    def handle_overdue_tasks(self):
        """Handle showing overdue tasks."""
        try:
            overdue_tasks = self.task_manager.get_overdue_tasks()

            if not overdue_tasks:
                print("No overdue tasks found.")
                return

            print(f"\nOverdue Tasks ({len(overdue_tasks)}):")
            for task in overdue_tasks:
                print(format_task_display(task))

        except Exception as e:
            print(f"Error retrieving overdue tasks: {e}")

    def handle_upcoming_tasks(self):
        """Handle showing upcoming tasks."""
        try:
            upcoming_tasks = self.task_manager.get_upcoming_tasks()

            if not upcoming_tasks:
                print("No upcoming tasks found.")
                return

            print(f"\nUpcoming Tasks ({len(upcoming_tasks)}):")
            for task in upcoming_tasks:
                print(format_task_display(task))

        except Exception as e:
            print(f"Error retrieving upcoming tasks: {e}")

    def handle_add_task(self, command: str):
        """Handle adding a new task."""
        try:
            # Extract the title (everything after 'add ')
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Usage: add [title] [optional: --description=... --priority=... --tags=... --due=...]")
                return

            title = parts[1].strip()

            # For now, just add a basic task with the provided title
            task_id = self.task_manager.add_task(title=title)
            print(f"Task added successfully with ID: {task_id}")
        except ValidationError as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error adding task: {e}")

    def handle_list_tasks(self, command: str):
        """Handle listing tasks."""
        try:
            # Parse filters from the command
            filters = {}

            # Check for completion filter
            if '--completed' in command:
                filters['completed'] = True
            elif '--incomplete' in command:
                filters['completed'] = False

            # Check for priority filter
            for priority in ['high', 'medium', 'low']:
                if f'--priority={priority}' in command:
                    filters['priority'] = Priority[priority.upper()]

            # Check for sorting
            sort_by = None
            if '--sort-due-date' in command:
                if '--desc' in command:
                    sort_by = 'due_date_desc'
                else:
                    sort_by = 'due_date_asc'
            elif '--sort-priority' in command:
                sort_by = 'priority'
            elif '--sort-title' in command:
                sort_by = 'title'

            tasks = self.task_manager.list_tasks(filters=filters, sort_by=sort_by)

            if not tasks:
                print("No tasks found.")
                return

            print(f"\nFound {len(tasks)} task(s):")
            for task in tasks:
                print(format_task_display(task))

        except Exception as e:
            print(f"Error listing tasks: {e}")

    def handle_view_task(self, command: str):
        """Handle viewing a specific task."""
        try:
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Usage: view [id]")
                return

            task_id = int(parts[1])
            task = self.task_manager.get_task(task_id)
            print("\nTask Details:")
            print(format_task_display(task))

        except ValueError:
            print("Please provide a valid task ID (number).")
        except TaskNotFound as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error viewing task: {e}")

    def handle_update_task(self, command: str):
        """Handle updating a task."""
        try:
            # Parse: update [id] [field=value] [field2=value2] ...
            parts = command.split(' ', 2)
            if len(parts) < 3:
                print("Usage: update [id] [field=value] [field2=value2] ...")
                print("Fields: title, description, priority (HIGH/MEDIUM/LOW), tags (comma-separated), due (YYYY-MM-DD)")
                return

            task_id_str, updates_str = parts[1], parts[2]
            task_id = int(task_id_str)

            # Parse updates
            updates = {}
            update_pairs = updates_str.split()

            for pair in update_pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key = key.strip().lower()
                    value = value.strip()

                    if key == 'priority':
                        try:
                            updates[key] = Priority[value.upper()]
                        except KeyError:
                            print(f"Invalid priority value. Use HIGH, MEDIUM, or LOW.")
                            return
                    elif key == 'tags':
                        updates[key] = [tag.strip() for tag in value.split(',')]
                    elif key == 'due':
                        updates[key] = parse_date(value)
                    elif key == 'completed':
                        updates[key] = value.lower() in ['true', '1', 'yes', 'y']
                    else:
                        updates[key] = value

            self.task_manager.update_task(task_id, **updates)
            print(f"Task {task_id} updated successfully.")

        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Usage: update [id] [field=value] [field2=value2] ...")
        except TaskNotFound as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error updating task: {e}")

    def handle_delete_task(self, command: str):
        """Handle deleting a task."""
        try:
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Usage: delete [id]")
                return

            task_id = int(parts[1])

            # Confirmation prompt
            task = self.task_manager.get_task(task_id)
            print(f"About to delete task: {task.title}")
            confirm = input("Are you sure? (y/N): ").lower()

            if confirm in ['y', 'yes']:
                self.task_manager.delete_task(task_id)
                print(f"Task {task_id} deleted successfully.")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Please provide a valid task ID (number).")
        except TaskNotFound as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def handle_toggle_completion(self, command: str):
        """Handle toggling task completion status."""
        try:
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Usage: complete [id]")
                return

            task_id = int(parts[1])
            new_status = self.task_manager.toggle_completion(task_id)
            status_str = "completed" if new_status else "incomplete"
            print(f"Task {task_id} marked as {status_str}.")

        except ValueError:
            print("Please provide a valid task ID (number).")
        except TaskNotFound as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error toggling completion: {e}")

    def handle_search_tasks(self, command: str):
        """Handle searching for tasks."""
        try:
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("Usage: search [query]")
                return

            query = parts[1]
            tasks = self.task_manager.search_tasks(query)

            if not tasks:
                print("No tasks found matching your query.")
                return

            print(f"\nFound {len(tasks)} task(s) matching '{query}':")
            for task in tasks:
                print(format_task_display(task))

        except Exception as e:
            print(f"Error searching tasks: {e}")


def main():
    """Main entry point for the application."""
    ui = ConsoleUI()
    ui.run()


if __name__ == "__main__":
    main()