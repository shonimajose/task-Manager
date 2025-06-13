import os
import json
from colorama import init

init(autoreset=True)

# Color definitions
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

STATUS_OPTIONS = {"Pending", "Inprogress", "Onhold", "Canceled", "Completed"}


class TaskManager:
    def __init__(self):
        self.task = self.load_tasks()

    def load_tasks(self):
        if os.path.exists("task.json"):
            try:
                with open("task.json", "r") as file:
                    tasks = json.load(file)
                    for task in tasks:
                        if "status" not in task or not task["status"]:
                            task["status"] = "Pending"
                    return tasks
            except Exception as e:
                print(f"{RED}An error occurred while loading tasks: {e}{RESET}")
        return []

    def save_tasks(self):
        try:
            with open("task.json", "w") as file:
                json.dump(self.task, file, indent=4)
        except Exception as e:
            print(f"{RED}An error occurred while saving tasks: {e}{RESET}")

    def add_task(self, title, description, status):
        task = {"title": title, "description": description, "status": status}
        self.task.append(task)
        self.save_tasks()
        print(f"{GREEN}*** TASK '{title}' ADDED SUCCESSFULLY ***{RESET}")

    def task_details(self, title):
        for task in self.task:
            if task["title"].lower() == title.lower():
                print(f"{GREEN}Title: {task['title']} - Description: {task['description']} - Status: {task['status']}{RESET}")
                break

    def view_tasks(self):
        if not self.task:
            print(f"{RED}NO TASK TO SHOW!!!!!{RESET}")
        else:
            for i, task in enumerate(self.task, 1):
                print(f"{BLUE}{i}. {task['title']} - {task['description']} - [{task['status']}] {RESET}")
        print(f"{RED}{'=' * 30}{RESET}")

    def mark_task_status(self, task_number, status):
        while True:
            if 0 < task_number <= len(self.task):
                task = self.task[task_number - 1]
                if task["status"].lower() == status.lower():
                    print(f"{RED}TASK {task_number} IS ALREADY MARKED AS {status.upper()} **{RESET}")
                else:
                    task["status"] = status
                    self.save_tasks()
                    print(f"{GREEN}** TASK {task_number} STATUS UPDATED TO {status.upper()} **{RESET}")
                break
            else:
                print(f"{RED}Invalid task number!{RESET}")
                break

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.task):
            del self.task[task_number - 1]
            self.save_tasks()
            print(f"{RED}** TASK {task_number} DELETED SUCCESSFULLY **{RESET}")
        else:
            print(f"{RED}Invalid task number!{RESET}")
        


def retry_input(prompt, validator=None, error_msg="Invalid input!", max_retries=3):
    for attempt in range(max_retries):
        user_input = input(f"{BLUE}{prompt}{RESET}").strip()
        if not validator or validator(user_input):
            return user_input
        print(f"{RED}{error_msg} (Attempt {attempt + 1} of {max_retries}){RESET}")
    print(f"{RED}Too many failed attempts. Returning to the main menu.{RESET}")
    return None


def prompt_task_creation(task_manager):
    while True:
        title = retry_input("Enter Title of the Task: ", validator=lambda x: len(x) > 0, error_msg="Title cannot be empty")
        if title is None:
            return

        if any(task["title"].lower() == title.lower() for task in task_manager.task):
            print(f"{RED}Task with the title '{title}' already exists!{RESET}")
            task_manager.task_details(title)
        else:
            description = input(f"{BLUE}Enter Description: {RESET} ")
            status = retry_input(
                f"Enter status ({'/'.join(STATUS_OPTIONS)}): ",
                validator=lambda s: s.title() in STATUS_OPTIONS,
                error_msg="Invalid status"
            )
            if status is None:
                return
            task_manager.add_task(title, description, status.title())

        more = input(f"{BLUE}Do you want to add another task? (y/n): {RESET}").strip().lower()
        if more != 'y':
            break



def main():
    task_manager = TaskManager()

    while True:
        print("\n1. Add New Task")
        print("2. View Tasks")
        print("3. Update Task Status")
        print("4. Delete Task")
        print("5. Exit")

        choice = retry_input("Choose an option (1-5): ", validator=lambda c: c in "12345", error_msg="Please choose between 1-5")
        if choice is None:
            continue

        if choice == "1":
            prompt_task_creation(task_manager)

        elif choice == "2":
            task_manager.view_tasks()

        elif choice == "3":
            if not task_manager.task:
                print(f"{RED}No tasks available to update. Please add tasks first!{RESET}")
                continue
            task_manager.view_tasks()
            task_number_str = retry_input("Enter the task number to update: ", lambda x: x.isdigit() and 1 <= int(x) <= len(task_manager.task), f"Please enter a number between 1 and {len(task_manager.task)}")
            if task_number_str:
                status = retry_input(
                    f"Enter new status ({'/'.join(STATUS_OPTIONS)}): ",
                    lambda s: s.title() in STATUS_OPTIONS,
                    "Invalid status"
                )
                if status:
                    task_manager.mark_task_status(int(task_number_str), status.title())

        elif choice == "4":
            while True:
                  
                if not task_manager.task:
                    print(f"{RED}No tasks available to delete. Please add tasks first!{RESET}")
                    break
                task_manager.view_tasks()
                task_number_str = retry_input("Enter the task number to delete: ", lambda x: x.isdigit() and 1 <= int(x) <= len(task_manager.task), f"Please enter a number between 1 and {len(task_manager.task)}")
                if task_number_str:
                    task_manager.delete_task(int(task_number_str))
                    
                more = retry_input("Do you want to delete another task? (y/n): ", lambda x: x.lower() in ['y', 'n'], "Enter y or n")
                if more.lower() != 'y':
                    break    

        elif choice == "5":
            confirm_exit = retry_input("Are you sure you want to exit? (y/n): ", validator=lambda x: x.lower() in ['y', 'n'], error_msg="Please enter y or n")
            if confirm_exit and confirm_exit.lower() == 'y':
                print(f"{YELLOW}Exiting the Manager, goodbye!{RESET}")
                break


if __name__ == "__main__":
    main()
