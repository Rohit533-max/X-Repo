def task():
    tasks = []  #empty list to store tasks
    print("--Welcome to the To-Do list app")

    total_tasks =  int(input("Enter the number of tasks: "))
    for i in range(1,total_tasks+1):
        name = input("Enter the task name:")
        tasks.append(name)
    print("Your tasks are:",tasks)

    #the code stop when the user wants
    while True:
        operation = int(input("Enter 1 to add a task\n 2 to remove a task\n 3 to update a task\n 4 to view all tasks\n 5 to exit:"))

        if operation ==1:
            new_task = input("Enter new task : ")
            tasks.append(new_task)
            print(f"Task {new_task} added successfully.")
        
        elif operation == 2:
            remove_task = input("Enter the task name to remove:")
            if remove_task in tasks:
                tasks.remove(remove_task)
            else:
                print("Invalid task entered")

        elif operation == 3:
            update_task = input("Enter the task name to update:")
            if update_task in tasks:
                new_task = input("Enter the new task: ")
                idx = tasks.index(update_task)
                tasks[idx] = new_task
            else:
                print("Task not found")
        elif operation == 4:
            print("Your tasks are: ",tasks)

        elif operation == 5:
            print("Exiting the app")
            break

d = task()
