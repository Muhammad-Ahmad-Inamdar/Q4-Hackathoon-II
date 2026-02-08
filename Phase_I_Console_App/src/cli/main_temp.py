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
from utils.colors import *
from utils.dateFormatter import *
import inquirer


class ArrowMenuTodoCLI:
    """Arrow Key Menu-based Command Line Interface for the Todo Application"""

    def __init__(self):
        """Initialize the menu CLI with services"""
        self.repository = TodoRepository("todos.json")  # Enable file persistence
        self.service = TodoService(self.repository)
        self.running = True

    def display_tasks(self, tasks: List[Todo]):
        """Display a list of tasks in a formatted way with colors"""
        if not tasks:
            print(colored("\nNo tasks found.", Colors.YELLOW))
            return

        print(f"\n{colored('ID', Colors.BOLD):<3} {colored('Status', Colors.BOLD):<8} {colored('Title', Colors.BOLD):<30} {colored('Created', Colors.BOLD):<18} {colored('Deadline', Colors.BOLD):<18} {colored('Description', Colors.BOLD)}")
        print(colored("-" * 90, Colors.BLUE))
        for task in tasks:
            status = task_completed("COMPLETED") if task.completed else task_pending("PENDING")
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            created_date = format_datetime_for_display(task.created_at)
            deadline_date = format_datetime_for_display(task.deadline) if task.deadline else colored("No deadline", Colors.BRIGHT_BLACK)
            description = task.description if task.description else ""
            print(f"{colored(str(task.id), Colors.CYAN):<3} {status:<8} {colored(title, Colors.WHITE):<30} {colored(created_date, Colors.GREEN):<18} {deadline_date:<18} {colored(description, Colors.BRIGHT_WHITE)}")
        print()

    def get_user_input(self, prompt: str) -> str:
        """Get user input with a prompt"""
        try:
            return input(prompt).strip()
        except EOFError:
            print(colored("\nInput interrupted. Returning to menu...", Colors.YELLOW))
            return ""

    def get_task_id(self) -> Optional[int]:
        """Get task ID from user with validation"""
        try:
            id_str = self.get_user_input(colored("Enter task ID: ", Colors.BLUE))
            return int(id_str)
        except ValueError:
            print(colored("Error: Task ID must be a number", Colors.RED))
            input(colored("Press Enter to continue...", Colors.YELLOW))
            return None

    def handle_add_task(self):
        """Handle adding a new task with optional deadline"""
        print(colored("\n--- ADD TASK ---", Colors.BOLD))
        title = self.get_user_input(colored("Enter task title: ", Colors.BLUE))
        if not title:
            print(colored("Error: Title cannot be empty", Colors.RED))
            input(colored("Press Enter to continue...", Colors.YELLOW))
            return

        description = self.get_user_input(colored("Enter task description (optional, press Enter to skip): ", Colors.BLUE))
        if not description:
            description = None

        # Get deadline if user wants to add one
        add_deadline = self.get_user_input(colored("Add deadline? (y/N): ", Colors.BLUE))
        deadline = None
        if add_deadline.lower() in ['y', 'yes']:
            deadline_str = self.get_user_input(colored("Enter deadline (YYYY-MM-DD or MM/DD/YYYY): ", Colors.BLUE))
            deadline = parse_datetime(deadline_str)
            if deadline is None:
                print(colored("Invalid date format. Task will be created without deadline.", Colors.YELLOW))

        try:
            task = self.service.add_task(title, description, deadline)
            print(success(f"✓ Added task: '{task.title}' with ID {task.id}"))
        except ValueError as e:
            print(error(f"Error: {e}"))

        input(colored("\nPress Enter to continue...", Colors.YELLOW))

    def handle_list_tasks(self):
        """Handle listing all tasks with optional sorting and filtering"""
        print(colored("\n--- TASK LIST ---", Colors.BOLD))

        # Ask user if they want to sort or filter
        options = ['List all', 'Sort tasks', 'Filter tasks']
        questions = [
            inquirer.List('option',
                         message=colored("Choose an option", Colors.BLUE),
                         choices=options,
                         carousel=True
                         )
        ]
        answers = inquirer.prompt(questions)
        option = answers['option'] if answers else 'List all'

        tasks = self.service.get_all_tasks()

        if option == 'Sort tasks':
            sort_options = ['created_at', 'deadline', 'status']
            sort_order = ['asc', 'desc']

            sort_by_question = [
                inquirer.List('sort_by',
                             message=colored("Sort by", Colors.BLUE),
                             choices=sort_options,
                             carousel=True
                             )
            ]
            order_question = [
                inquirer.List('order',
                             message=colored("Order", Colors.BLUE),
                             choices=sort_order,
                             carousel=True
                             )
            ]

            sort_by = inquirer.prompt(sort_by_question)
            order = inquirer.prompt(order_question)

            if sort_by and order:
                tasks = self.service.sort_tasks(tasks, sort_by['sort_by'], order['order'])

        elif option == 'Filter tasks':
            filter_options = ['Completed', 'Incomplete', 'All']
            filter_question = [
                inquirer.List('filter',
                             message=colored("Filter by status", Colors.BLUE),
                             choices=filter_options,
                             carousel=True
                             )
            ]
            filter_choice = inquirer.prompt(filter_question)

            if filter_choice:
                if filter_choice['filter'] == 'Completed':
                    tasks = self.service.filter_tasks_by_status(tasks, True)
                elif filter_choice['filter'] == 'Incomplete':
                    tasks = self.service.filter_tasks_by_status(tasks, False)
                # 'All' means no filtering, just use original tasks list

        self.display_tasks(tasks)
        input(colored("Press Enter to continue...", Colors.YELLOW))

    def handle_complete_task(self):
        """Handle marking a task as complete"""
        print(colored("\n--- COMPLETE TASK ---", Colors.BOLD))
        task_id = self.get_task_id()
        if task_id is None:
            return

        task = self.service.complete_task(task_id)
        if task:
            print(success(f"✓ Task {task_id} marked as complete"))
        else:
            print(error(f"✗ Error: Task with ID {task_id} not found"))

        input(colored("Press Enter to continue...", Colors.YELLOW))

    def handle_incomplete_task(self):
        """Handle marking a task as incomplete"""
        print(colored("\n--- MARK TASK INCOMPLETE ---", Colors.BOLD))
        task_id = self.get_task_id()
        if task_id is None:
            return

        task = self.service.incomplete_task(task_id)
        if task:
            print(success(f"✓ Task {task_id} marked as incomplete"))
        else:
            print(error(f"✗ Error: Task with ID {task_id} not found"))

        input(colored("Press Enter to continue...", Colors.YELLOW))

    def handle_update_task(self):
        """Handle updating a task"""
        print(colored("\n--- UPDATE TASK ---", Colors.BOLD))
        task_id = self.get_task_id()
        if task_id is None:
            return

        # Get current task to show current values
        current_task = self.service.get_task_by_id(task_id)
        if not current_task:
            print(error(f"✗ Error: Task with ID {task_id} not found"))
            input(colored("Press Enter to continue...", Colors.YELLOW))
            return

        print(info(f"Current title: {current_task.title}"))
        print(info(f"Current description: {current_task.description or 'None'}"))
        print(info(f"Current deadline: {format_datetime_for_display(current_task.deadline) if current_task.deadline else 'None'}"))

        title = self.get_user_input(colored("Enter new title (or press Enter to keep current): ", Colors.BLUE))
        description = self.get_user_input(colored("Enter new description (or press Enter to keep current): ", Colors.BLUE))

        # Ask if user wants to update deadline
        update_deadline = self.get_user_input(colored("Update deadline? (y/N): ", Colors.BLUE))
        deadline = current_task.deadline  # default to current deadline
        if update_deadline.lower() in ['y', 'yes']:
            deadline_str = self.get_user_input(colored("Enter new deadline (YYYY-MM-DD or MM/DD/YYYY, or press Enter to remove): ", Colors.BLUE))
            if deadline_str:
                deadline = parse_datetime(deadline_str)
                if deadline is None:
                    print(colored("Invalid date format. Deadline will not be changed.", Colors.YELLOW))
                    deadline = current_task.deadline
            else:
                deadline = None  # Remove deadline if empty string provided

        # If user pressed Enter without typing, keep the original value
        if not title:
            title = current_task.title

        if not description or description == "None":
            # If description is empty or user wants to keep it empty
            if description == "":
                description = None
            else:
                description = current_task.description

        task = self.service.update_task(task_id, title, description, deadline)
        if task:
            print(success(f"✓ Task {task_id} updated"))
        else:
            print(error(f"✗ Error: Task with ID {task_id} not found"))

        input(colored("Press Enter to continue...", Colors.YELLOW))

    def handle_delete_task(self):
        """Handle deleting a task"""
        print(colored("\n--- DELETE TASK ---", Colors.BOLD))
        task_id = self.get_task_id()
        if task_id is None:
            return

        # Show the task before deletion
        task = self.service.get_task_by_id(task_id)
        if task:
            print(info(f"Task to delete: '{task.title}' (ID: {task.id})"))

        confirm = self.get_user_input(colored(f"Are you sure you want to delete task {task_id}? (y/N): ", Colors.RED))

        if confirm.lower() in ['y', 'yes']:
            success_result = self.service.delete_task(task_id)
            if success_result:
                print(success(f"✓ Task {task_id} deleted"))
            else:
                print(error(f"✗ Error: Task with ID {task_id} not found"))
        else:
            print(warning("Deletion cancelled."))

        input(colored("Press Enter to continue...", Colors.YELLOW))

    def show_main_menu(self):
        """Display the main menu with arrow-key selection"""
        questions = [
            inquirer.List('action',
                         message=colored("TODO APPLICATION - SELECT AN ACTION", Colors.BOLD),
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
        print(colored("\nWelcome to Todo Application!", Colors.BOLD))
        input(colored("\nPress Enter to continue...", Colors.YELLOW))

        while self.running:
            # Show the current tasks
            print(colored("\n" + "="*60, Colors.BLUE))
            print(colored("                   TODO TASKS", Colors.BOLD))
            print(colored("="*60, Colors.BLUE))
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
                confirm = self.get_user_input(colored("Are you sure you want to exit? (y/N): ", Colors.RED))
                if confirm.lower() in ['y', 'yes']:
                    print(colored("\nGoodbye!", Colors.BOLD))
                    self.running = False
                else:
                    continue


def main():
    """Main entry point"""
    cli = ArrowMenuTodoCLI()
    cli.run()


if __name__ == "__main__":
    main()