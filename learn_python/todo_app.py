import tasks
from utils import check_input_num


def main():
    """Main entry point of the program.    
    """
    while (True):
        print("1. Add a task. ")
        print("2. List tasks  ")
        print("3. Remove task. ")
        print("4. Exit. ")
        option = check_input_num("Enter an option to execute  .")
        print("Selected . ", option)
        match option:
            case 1:
                print("Option 1 matched. ")
                task = input("Enter task  .  ")
                tasks.add_tasks(task)
            case 2:
                print("Option 2 matched. ")
                tasks.list_tasks()
            case 3:
                print("Option 3 matched. ")
                index = check_input_num("Enter task position to be removed  .  ")
                if (index < 1 or index > tasks.get_task_count()):
                    print(f"Wrong input , There is no task with index {index}")
                else :
                    tasks.remove_task(index - 1)
            case 4:
                print("Option 4 matched. ")
                break
            case _ : 
                print("do nothing")        

if __name__ == "__main__":
    main()
