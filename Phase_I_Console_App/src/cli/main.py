#!/usr/bin/env python3
"""
Arrow Key Menu CLI Todo Application

This module provides an interactive arrow-key navigable menu
for managing todo items, similar to professional CLI tools.
"""
import sys
import os
from typing import List, Optional

# Add the parent directory to the path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from todo.models import Todo
from todo.repository import TodoRepository
from todo.services import TodoService
import inquirer


class ArrowMenuTodoCLI:
    """Arrow Key Menu-based Command Line Interface for the Todo Application"""

    def __init__(self):
        """Initialize the menu CLI with services"""
        self.repository = TodoRepository("todos.json")  # Enable file persistence
        self.service = TodoService(self.repository)
        self.running = True

    def display_tasks(self, tasks: List[Todo]):
        """Display a list of tasks in a formatted way"""
        if not tasks:
            print("\nNo tasks found.")
            return

        print(f"\n{'ID':<3} {'Status':<8} {'Title':<30} {'Description'}")
        print("-" * 70)
        for task in tasks:
            status = "X" if task.completed else "O"
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            description = task.description if task.description else ""
            print(f"{task.id:<3} {status:<8} {title:<30} {description}")
        print()

    def get_user_input(self, prompt: str) -> str:
        """Get user input with a prompt"""
        try:
            return input(prompt).strip()
        except EOFError:
            print("\nInput interrupted. Returning to menu...")
            return ""

    def get_task_id(self) -> Optional[int]:
        """Get task ID from user with validation"""
        try:
            id_str = self.get_user_input("Enter task ID: ")
            return int(id_str)
        except ValueError:
            print("Error: Task ID must be a number")
            input("Press Enter to continue...")
            return None

    def handle_add_task(self):
        """Handle adding a new task"""
        print("\n--- ADD TASK ---")
        title = self.get_user_input("Enter task title: ")
        if not title:
            print("Error: Title cannot be empty")
            input("Press Enter to continue...")
            return

        description = self.get_user_input("Enter task description (optional, press Enter to skip): ")
        if not description:
            description = None

        try:
            task = self.service.add_task(title, description)
            print(f"✓ Added task: '{task.title}' with ID {task.id}")
        except ValueError as e:
            print(f"Error: {e}")

        input("\nPress Enter to continue...")

    def handle_list_tasks(self):
        """Handle listing all tasks"""
        print("\n--- TASK LIST ---")
        tasks = self.service.get_all_tasks()
        self.display_tasks(tasks)
        input("Press Enter to continue...")

    def handle_complete_task(self):
        """Handle marking a task as complete"""
        print("\n--- COMPLETE TASK ---")
        task_id = self.get_task_id()
        if task_id is None:
            return

        task = self.service.complete_task(task_id)
        if task:
            print(f"✓ Task {task_id} marked as complete")
        else:
            print(f"✗ Error: Task with ID {task_id} not found")

        input("Press Enter to continue...")

    def handle_incomplete_task(self):
        """Handle marking a task as incomplete"""
        print("\n--- MARK TASK INCOMPLETE ---")
        task_id = self.get_task_id()
        if task_id is None:
            return

        task = self.service.incomplete_task(task_id)
        if task:
            print(f"✓ Task {task_id} marked as incomplete")
        else:
            print(f"✗ Error: Task with ID {task_id} not found")

        input("Press Enter to continue...")

    def handle_update_task(self):
        """Handle updating a task"""
        print("\n--- UPDATE TASK ---")
        task_id = self.get_task_id()
        if task_id is None:
            return

        # Get current task to show current values
        current_task = self.service.get_task_by_id(task_id)
        if not current_task:
            print(f"✗ Error: Task with ID {task_id} not found")
            input("Press Enter to continue...")
            return

        print(f"Current title: {current_task.title}")
        print(f"Current description: {current_task.description or 'None'}")

        title = self.get_user_input("Enter new title (or press Enter to keep current): ")
        description = self.get_user_input("Enter new description (or press Enter to keep current): ")

        # If user pressed Enter without typing, keep the original value
        if not title:
            title = current_task.title

        if not description or description == "None":
            # If description is empty or user wants to keep it empty
            if description == "":
                description = None
            else:
                description = current_task.description

        task = self.service.update_task(task_id, title, description)
        if task:
            print(f"✓ Task {task_id} updated")
        else:
            print(f"✗ Error: Task with ID {task_id} not found")

        input("Press Enter to continue...")

    def handle_delete_task(self):
        """Handle deleting a task"""
        print("\n--- DELETE TASK ---")
        task_id = self.get_task_id()
        if task_id is None:
            return

        # Show the task before deletion
        task = self.service.get_task_by_id(task_id)
        if task:
            print(f"Task to delete: '{task.title}' (ID: {task.id})")

        confirm = self.get_user_input(f"Are you sure you want to delete task {task_id}? (y/N): ")

        if confirm.lower() in ['y', 'yes']:
            success = self.service.delete_task(task_id)
            if success:
                print(f"✓ Task {task_id} deleted")
            else:
                print(f"✗ Error: Task with ID {task_id} not found")
        else:
            print("Deletion cancelled.")

        input("Press Enter to continue...")

    def show_main_menu(self):
        """Display the main menu with arrow-key selection"""
        questions = [
            inquirer.List('action',
                         message="TODO APPLICATION - SELECT AN ACTION",
                         choices=[
                             'Add Task',
                             'List All Tasks',
                             'Complete Task',
                             'Mark Task Incomplete',
                             'Update Task',
                             'Delete Task',
                             'Exit'
                         ],
                         carousel=True  # Enables wrapping around the list
                         )
        ]

        answers = inquirer.prompt(questions)
        return answers['action'] if answers else None

    def run(self):
        """Run the main application loop with arrow-key menu interface"""
        print("\nWelcome to Todo Application!")
        input("\nPress Enter to continue...")

        while self.running:
            # Show the current tasks
            print("\n" + "="*60)
            print("                   TODO TASKS")
            print("="*60)
            self.display_tasks(self.service.get_all_tasks())

            # Show menu and get selection
            action = self.show_main_menu()

            if action == 'Add Task':
                self.handle_add_task()
            elif action == 'List All Tasks':
                self.handle_list_tasks()
            elif action == 'Complete Task':
                self.handle_complete_task()
            elif action == 'Mark Task Incomplete':
                self.handle_incomplete_task()
            elif action == 'Update Task':
                self.handle_update_task()
            elif action == 'Delete Task':
                self.handle_delete_task()
            elif action == 'Exit':
                confirm = self.get_user_input("Are you sure you want to exit? (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    print("\nGoodbye!")
                    self.running = False
                else:
                    continue


def main():
    """Main entry point"""
    cli = ArrowMenuTodoCLI()
    cli.run()


if __name__ == "__main__":
    main()