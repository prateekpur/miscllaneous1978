import tasks_json as tasks
from utils import check_input_num


def main():
    """Main entry point of the program.    
    """
    while (True):
        print("1. Add a task. ")
        print("2. List tasks  ")
        print("3. Remove task. ")
        print("4. Complete task. ")
        print("5. Write to file. ")
        print("6. Read from file. ")
        print("7. Exit. ")
        option = check_input_num("Enter an option to execute  .")
        print("Selected . ", option)
        match option:
            case 1:
                task = input("Enter task  .  ")
                tasks.add_task(task)
            case 2:
                tasks.list_tasks()
            case 3:
                index = check_input_num("Enter task position to be removed  .  ")
                if (index < 1 or index > tasks.get_task_count()):
                    print(f"Wrong input , There is no task with index {index}")
                else :
                    tasks.remove_task(index - 1)
            case 4:
                index = check_input_num("Enter task position to be updated  .  ")
                if (index < 1 or index > tasks.get_task_count()):
                    print(f"Wrong input , There is no task with index {index}")
                else :
                    tasks.complete_task(index - 1)
            case 5:
                filename = input("Enter filename : ")
                tasks.save_tasks(filename)
                break
            case 6:
                tasks.read_tasks("test.json")
            case 7:
                print("Option 5 matched. ")
                break
            case _:
                print("")

if __name__ == "__main__":
    main()
