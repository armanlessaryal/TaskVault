import json

print("Enter 'quit' to end the program")
print("Commands: add, view, deleted, completed, view deleted, view completed")


class TaskManager:

    def __init__(self):
        self.tasks = []
        self.completed_task = []
        self.deleted_task = []

    def save_data(self):
        data = {
            'tasks': self.tasks,
            'completed': self.completed_task,
            'deleted': self.deleted_task
        }

        with open('rev.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open('rev.json', 'r') as file:
                data = json.load(file)

            self.tasks = data.get('tasks', [])
            self.completed_task = data.get('completed', [])
            self.deleted_task = data.get('deleted', [])

        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            self.completed_task = []
            self.deleted_task = []

            self.save_data()

    def add_task(self):
        prompt = input("ADD TASK: ").strip()

        if prompt == "":
            print("You can't enter an empty task!")
            return

        self.tasks.append(prompt)
        self.save_data()

        print("Task added successfully!")

    def view(self, assigned_list):
        if not assigned_list:
            print("No available tasks!")
            return

        for counter, task in enumerate(assigned_list, start=1):
            print(counter, ":", task)

    def move_task(self, given_list, given_command):
        if not self.tasks:
            print("No tasks available to move!")
            return

        self.view(self.tasks)

        print("Which task do you want to " + given_command + "?")

        try:
            prompt = int(
                input("Enter the task number: ").strip()
            )

        except ValueError:
            print("Only integers are accepted!")
            return

        operation = prompt - 1

        if operation < 0 or operation >= len(self.tasks):
            print("Invalid task number!")
            return

        operated = self.tasks.pop(operation)
        given_list.append(operated)

        self.save_data()

        print("Task " + given_command.lower() + " successfully!")
        print("Use 'view completed' or 'view deleted' to see it.")


# Create the TaskManager object
manager = TaskManager()

# Load previously saved tasks
manager.load_data()


# Connect commands to their functions
commands = {
    'add': manager.add_task,
    'view': lambda: manager.view(manager.tasks),
    'deleted': lambda: manager.move_task(
        manager.deleted_task, 'Deleted'
    ),
    'completed': lambda: manager.move_task(
        manager.completed_task, 'Completed'
    ),
    'view completed': lambda: manager.view(
        manager.completed_task
    ),
    'view deleted': lambda: manager.view(
        manager.deleted_task
    )
}


# Main program loop
while True:
    command = input("\nYour Command: ").strip().lower()

    if command == 'quit':
        manager.save_data()
        print("Tasks saved. Goodbye!")
        break

    elif command in commands:
        commands[command]()

    else:
        print("Invalid command! Please try again.")