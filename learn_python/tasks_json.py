from dataclasses import dataclass, asdict
import json

@dataclass
class Task:
    desc: str
    completed: bool

tasks = []

def list_tasks():
    if not tasks :
        print("No tasks.")
        return
    tmp = 1
    for task in tasks :
        print(tmp , " : " , task.desc, " : ", task.completed )
        tmp += 1

def add_task(task):
    tasks.append(Task(task, False))

def complete_task(index) :
    if (index < 0 or index > len(tasks) - 1):
        print(f"Wrong input , There is no task with index {index}")
        return
    tasks[index].completed = True

def remove_task(index):
    if (index < 0 or index > len(tasks) - 1):
        print(f"Wrong input , There is no task with index {index}")
        return
    del tasks[index]

def get_task_count():
    return len(tasks)

def save_tasks(filename):
    print(tasks)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([asdict(task) for task in tasks], f, indent=2)

def read_tasks(filename):
    global tasks
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            tasks = [Task(**item) for item in data]
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
    except TypeError as e:
        print("Invalid JSON schema:", e)