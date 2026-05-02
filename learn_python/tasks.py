tasks = []

def list_tasks():
    if not tasks :
        print("List is empty.")
        return
    tmp = 1
    for task in tasks :
        print(tmp , " : " , task)
        tmp += 1

def add_tasks(task):
    tasks.append(task)

def remove_task(index):
    if (index < 0 or index > len(tasks) - 1):
        print(f"Wrong input , There is no task with index {index}")
        return
    del tasks[index]

def get_task_count():
    return len(tasks)