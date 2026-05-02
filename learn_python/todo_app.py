tasks = []
def check_input_num(prompt):
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input, please enter a number")

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
                add_tasks(task)
            case 2:
                print("Option 2 matched. ")
                list_tasks()
            case 3:
                print("Option 3 matched. ")
                index = check_input_num("Enter task position to be removed  .  ")
                if (index < 1 or index > len(tasks)):
                    print(f"Wrong input , There is no task with index {index}")
                else :
                    remove_task(index - 1)
            case 4:
                print("Option 4 matched. ")
                break
            case _ : 
                print("do nothing")        

if __name__ == "__main__":
    main()
