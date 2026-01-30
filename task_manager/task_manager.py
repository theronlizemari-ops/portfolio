# ===== Importing external modules ===========
import os
from datetime import date
from datetime import datetime


# ====== Class objects ===========
class User:  # creats an object of users

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __str__(self):
        return f"{self.name}, {self.password}"


class Task:

    def __init__(self, user_assigned, title, description,
                 date_assigned, due_date, completed):
        self.user = user_assigned
        self.title = title
        self.description = description
        self.date_assigend = date_assigned
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        return (f"{self.user}, {self.title}, {self.description}, "
                f"{self.date_assigend}, {self.due_date}, {self.completed}")


# ======= Functions =======
def reg_user():
    '''
    This function will add a new user to the user.txt file
    Requests input of a new username, a new password and password confirmation.
    If the new password and confirmed password are the same,
    they are added to user.txt file,
    '''

    print("\nRegister a new user.\n")

    while True:

        new_username = input("Please enter a new username: ").lower()

        if new_username in usernames_list:
            print("Error: This username already exists. Please try again.")
            continue

        new_password = input("Please enter the password: ")
        new_password_confirm = input("Please confirm the passowrd: ")

        if new_password == new_password_confirm:  # if passwords match

            try:  # new user appened to text file and user lists
                with open("user.txt", "a") as file:
                    file.write(f"\n{new_username}, {new_password}")

                    user_object = User(new_username, new_password)
                    user_list.append(user_object)
                    str_user_list.append(str(user_object))
                    usernames_list.append(new_username)

                    print("\nNew user successfully registered.\n")
                    break

            except (FileNotFoundError, TypeError, ValueError) as e:
                print(f"An error occurred: {e}. Could not add new user.")

        else:
            print("Passwords not not match. Please try again.")


def add_task():
    '''
    This function will allow a user to add a new task to task.txt file
    The user is prompted for the following:
        - the username of the person whom the task is assigned to,
        - the title of the task,
        - the description of the task,
        - the due date of the task
    The data is then added to the tasks.txt
    '''

    print("\nAdd a new task.")

    today = datetime.today().date()

    while True:

        # All information needed for task entry en tasks.txt
        # Some information requested form user
        assigned_person = input("Enter who the task is assigend to: ").lower()
        if assigned_person not in usernames_list:
            print("Username does not exist. Please try again.")

        else:
            date_task_assigned = str(date.today())
            task_completed = "no"
            title_task = input("Enter the title of the task: ")
            task_description = input("Enter a discription of the task: ")

            while True:
                task_due_date = input("Enter the task's due date "
                                      "(YYYY-MM-DD): ")
                try:
                    cor_task_date = datetime.strptime(task_due_date,
                                                      "%Y-%m-%d").date()
                    if cor_task_date > today:
                        break
                    else:
                        print("Invalid date. Cannot enter past date.")

                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")

            # Check if the information is correct
            print("\nPlease check if the information is correct.")
            print(f"The task is assigned to: {assigned_person}")
            print(f"The title of the task: {title_task}")
            print(f"Task description: {task_description}")
            print(f"Task due date: {cor_task_date}")

            task_confirm = input("\nIs the information correct?"
                                 " Yes/No ").lower()

            if task_confirm == "yes":

                try:  # add task to text file and task list
                    with open("tasks.txt", "a") as f:
                        f.write(f"\n{assigned_person}, {title_task}, "
                                f"{task_description}, "
                                f"{date_task_assigned}, {task_due_date}, "
                                f"{task_completed}")

                    task_object = Task(assigned_person, title_task,
                                       task_description,
                                       date_task_assigned, task_due_date,
                                       task_completed)
                    task_list.append(task_object)

                    print("\nNew task successfully added.")
                    break

                except (FileNotFoundError, TypeError, ValueError) as e:
                    print(f"An error occurred: {e}. Please try again.")

            elif task_confirm == "no":
                print("\nInformation incorrect. Enter new task again.")

            else:
                print("\nAn error occured. Please enter the new task again.")


def view_all():
    '''
    Using the task_list, this function will print all tasks to the
    console in a user-friendly format.
    '''
    # --- Display tasks ---
    for i, obj in enumerate(task_list, start=1):
        print(f"\nTask {i}")
        print(f"Task:              {obj.title}")
        print(f"Assigned to:       {obj.user}")
        print(f"Date assigned:     {obj.date_assigend}")
        print(f"Due date:          {obj.due_date}")
        print(f"Task complete?     {obj.completed}")
        print(f"Task description:  {obj.description}\n")


def view_mine(username):
    '''
    This function will print tasks assigend to a spesific user.
    The code will
        - Use the task_list
        - Check if the username of the person logged in is the same as the
          username read from the file.
        - Print the tasks in a user-friendly format.
        - Allow the user to edit the tasks
    '''
    # --- Filter for tasks belonging to this user ---
    today = datetime.today().date()

    user_tasks = [t for t in task_list if t.user == username]

    if not user_tasks:
        print("No tasks for this user found.")
        return

    # --- Display tasks ---
    for i, obj in enumerate(user_tasks, start=1):
        print(f"\nTask {i}")
        print(f"Task:              {obj.title}")
        print(f"Assigned to:       {obj.user}")
        print(f"Date assigned:     {obj.date_assigend}")
        print(f"Due date:          {obj.due_date}")
        print(f"Task complete?     {obj.completed}")
        print(f"Task description:  {obj.description}")

    # --- Let user select a task to edit ---
    while True:
        try:
            edit_select = int(input("\nEnter number of the task to edit"
                                    " (-1 to exit): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if edit_select == -1:
            print("Exit without editing.")
            break

        if edit_select < 1 or edit_select > len(user_tasks):
            print("Invalid task number.")
            continue

        task_to_edit = user_tasks[edit_select - 1]

        try:
            edit_option = int(input(
                "\nSelect an option:\n"
                "1 - Edit who the task is assigned to\n"
                "2 - Edit the due date\n"
                "3 - Mark the task as complete\n"
                "-1 - Exit without editing\n"
                "Choice: "
                ))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if edit_option == -1:
            print("Exit without editing.")
            break

        elif edit_option == 1:
            change_user = input("Enter username to assign to: ")
            if change_user in usernames_list:
                task_to_edit.user = change_user
                print(f"Task {edit_select} now assigned to {change_user}.")
            else:
                print("Invalid username. Please try again.\n")

        elif edit_option == 2:
            if task_to_edit.completed.lower() == "no":
                while True:
                    change_date = input("Enter new due date (YYYY-MM-DD): ")
                    try:
                        edited_due_date = datetime.strptime(change_date,
                                                            "%Y-%m-%d").date()
                        if edited_due_date > today:
                            task_to_edit.due_date = edited_due_date.strftime(
                                "%Y-%m-%d")
                            print(f"Task {edit_select} due date updated.")
                            break
                        else:
                            print("Sorry, cannot enter past date.")
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD.")
            else:
                print("You cannot edit this task."
                      " It has already been completed.")

        elif edit_option == 3:
            task_to_edit.completed = "yes"
            print(f"Task {edit_select} marked as complete.")

        else:
            print("Invalid selection. Please try again.")

    # --- Write updated tasks back to file once user enters "-1" ---
    with open("tasks.txt", "w") as file:
        for obj in task_list:
            file.write(f"{str(obj)}\n")


def delete_task():
    '''
    This function displays all tasks in the task_list.
    It allows a user the select a task to delete, and
    outputs a new tasks file and appends to the deleted task file.
    '''
    # --- Display all tasks ---
    for i, obj in enumerate(task_list, start=1):
        print(f"\nTask {i}")
        print(f"Task:              {obj.title}")
        print(f"Assigned to:       {obj.user}")
        print(f"Date assigned:     {obj.date_assigend}")
        print(f"Due date:          {obj.due_date}")
        print(f"Task complete?     {obj.completed}")
        print(f"Task description:  {obj.description}")

    # select item to delete
    del_select = int(input("\nEnter number of the task you want to delete: "))
    deleted_task_list.append(task_list[del_select - 1])
    del task_list[del_select - 1]

    # rewrite tasks file without selected item
    with open("tasks.txt", "w") as f:
        for item in task_list:
            f.write(f"{item}\n")
    print(f"\nTask {del_select} has been deleted.")

    # write deleted item to text file for record keeping
    with open("deleted.txt", "a") as file:
        for item in deleted_task_list:
            file.write(f"{item}\n")


def view_completed():
    '''
    This function uses the task_list and filters the tasks to
    show the tasks that have been completed.
    '''
    # --- Filter for tasks that are completed ---
    completed_tasks = [t for t in task_list if t.completed == "yes"]

    if not completed_tasks:
        print("No completed tasks found.")
        return

    # --- Display complteded tasks ---
    for i, obj in enumerate(completed_tasks, start=1):
        print(f"\nTask {i}")
        print(f"Task:              {obj.title}")
        print(f"Assigned to:       {obj.user}")
        print(f"Date assigned:     {obj.date_assigend}")
        print(f"Due date:          {obj.due_date}")
        print(f"Task complete?     {obj.completed}")
        print(f"Task description:  {obj.description}")


def display_statistics():
    '''
    This function gets statistics on tasks and users, and displays
    the results in the console.

    The task overview contains:
        The total number of tasks that have been generated and
        tracked using the task_manager.py.
        The total number of completed tasks.
        The total number of uncompleted tasks.
        The total number of tasks that are incompleted and
        that are overdue.
        The percentage of tasks that are incomplete.
        The percentage of tasks that are overdue.

    The user overview contains:
        The total number of users registered with task_manager.py.
        The total number of tasks that have been generated and
        tracked using task_manager.py
        For each user, it also describes:
            The total number of tasks assigned to that user.
            The percentage of the total number of tasks assigned to that user
            The percentage of the tasks that have been completed
            The percentage of the tasks that are incompleted
            The percentage of the tasks that are incompleted and overdue
    '''

    # get statistics for task overview
    # Count active tasks
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
        line_count = len(lines)

    # Count deleted tasks
    with open("deleted.txt", "r") as file:
        lines_del = file.readlines()
        lines_del_count = len(lines_del)

    # Sum of active and deleted tasks
    total_tasks = line_count + lines_del_count

    # Completed and uncompleted tasks
    today = datetime.today().date()
    try:
        with open("tasks.txt", "r") as file:

            for line in file:  # reads file line by line
                contents = line.split(", ")

                # slicing text file contents
                task_title = contents[1]
                due_date_task = contents[4]
                task_status = contents[5].strip()

                # finding spesific tasks and appending them to lists
                if task_status == "yes":
                    completed_task_list.append(task_title)

                if task_status == "no":
                    incompleted_task_list.append(task_title)
                    date_compare = datetime.strptime(due_date_task,
                                                     "%Y-%m-%d").date()
                    if date_compare < today:
                        overdue_task_list.append(task_title)

            # Counting tasks in lists
            completed_task_count = len(completed_task_list)
            incompleted_task_count = len(incompleted_task_list)
            persent_complete = round((completed_task_count/line_count)*100)
            persent_incomplete = round((incompleted_task_count/line_count)*100)
            overdue_task_count = len(overdue_task_list)
            persent_overdue = round((overdue_task_count/line_count)*100)

    except FileNotFoundError:
        print("Error: File for tasks not found.")

    # task overview
    # print numbers to console
    print("\nOverview of tasks generated using the task_manager.py")
    print(f"Total active tasks:              {line_count}")
    print(f"The total of deleted tasks:      {lines_del_count}")
    print(f"Total number of generated tasks: {total_tasks}")

    # printing statistics of all tasks
    print("\nOverview of task completeness")
    print(f"Number of completed tasks:          {completed_task_count}")
    print(f"Percentage of completed tasks:      {persent_complete}%")
    print(f"Number of incompleted tasks:        {incompleted_task_count}")
    print(f"Percentage of incompleted tasks:    {persent_incomplete}%")
    print(f"Incompleted tasks that are overdue: {overdue_task_count}")
    print(f"Percentage of overdue tasks:        {persent_overdue}%")

    with open("task_overview", "w") as f:  # writing statistics to file
        f.write(
            "\nOverview of tasks generated using the task_manager.py"
            f"\nTotal active tasks:              {line_count}"
            f"\nThe total of deleted tasks:      {lines_del_count}"
            f"\nTotal number of generated tasks: {total_tasks}"
            "\n"
            "\nOverview of task completeness"
            f"\nNumber of completed tasks:          {completed_task_count}"
            f"\nPercentage of completed tasks:      {persent_complete}%"
            f"\nNumber of incompleted tasks:        {incompleted_task_count}"
            f"\nPercentage of incompleted tasks:    {persent_incomplete}%"
            f"\nIncompleted tasks that are overdue: {overdue_task_count}"
            f"\nPercentage of overdue tasks:        {persent_overdue}%"
        )

    # user overview
    # get statistics for user overview
    print("\nOverview of tasks per user")
    print(f"\nTotal tasks generated by program: {total_tasks}"
          f"\nTotal amount of users:            {len(usernames_list)}")

    with open("user_overview.txt", "w") as f:  # writing statistics to file
        f.write("Overview of users and tasks assigend to them\n")
        f.write(f"\nTotal tasks generated by program: {total_tasks}"
                f"\nTotal amount of users:            {len(usernames_list)}\n")

    for user_obj in user_list:
        # Filter tasks for this user
        user_tasks = [task for task in task_list if task.user == user_obj.name]

        # Separate completed vs uncompleted
        completed_tasks = [task for task in user_tasks
                           if task.completed.lower() == "yes"]
        uncompleted_tasks = [task for task in user_tasks
                             if task.completed.lower() == "no"]

        # Find overdue tasks (only among uncompleted)
        overdue_tasks = [
            task for task in uncompleted_tasks
            if datetime.strptime(task.due_date, "%Y-%m-%d").date() < today
        ]

        # Count
        try:
            total = len(user_tasks)
            persent_total = round((total/total_tasks) * 100)
            completed_count = len(completed_tasks)
            uncompleted_count = len(uncompleted_tasks)
            per_uncompleted_count = round((uncompleted_count/total) * 100)
            overdue_count = len(overdue_tasks)
            per_overdue_count = round((overdue_count/total) * 100)

        except ZeroDivisionError:
            persent_total = 0
            per_uncompleted_count = 0
            per_overdue_count = 0

        # Printing statistics of tasks per user
        print(f"\nStats for {user_obj.name}:")
        print(f"Total tasks:                    {total}")
        print(f"% of all tasks assigned:        {persent_total}%")
        print(f"Completed:                      {completed_count}")
        print(f"Uncompleted:                    {uncompleted_count}")
        print(f"% of tasks uncompleted:         {per_uncompleted_count}%")
        print(f"Overdue:                        {overdue_count}")
        print(f"% of incompleted tasks overdue: {per_overdue_count}%\n")

        with open("user_overview.txt", "a") as f:  # writing statistics to file
            f.write(
                f"\nStats for {user_obj.name}:"
                f"\nTotal tasks:                    {total}"
                f"\n% of all tasks assigned:        {persent_total}%"
                f"\nCompleted:                      {completed_count}"
                f"\nUncompleted:                    {uncompleted_count}"
                f"\n% of tasks uncompleted:         {per_uncompleted_count}%"
                f"\nOverdue:                        {overdue_count}"
                f"\n% of incompleted tasks overdue: {per_overdue_count}%\n"
            )
    print("\nReprots succesfully generated.\n")


def generate_reports():
    '''
    This function does everything that display_statisctics does,
    but it writes text files instead of displaying the results in
    the console.
    '''

    # get statistics for task overview
    # Count active tasks
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
        line_count = len(lines)

    # Count deleted tasks
    with open("deleted.txt", "r") as file:
        lines_del = file.readlines()
        lines_del_count = len(lines_del)

    # Sum of active and deleted tasks
    total_tasks = line_count + lines_del_count

    # Completed and uncompleted tasks
    today = datetime.today().date()
    try:
        with open("tasks.txt", "r") as file:

            for line in file:  # reads file line by line
                contents = line.split(", ")

                # slicing text file contents
                task_title = contents[1]
                due_date_task = contents[4]
                task_status = contents[5].strip()

                # finding spesific tasks and appending them to lists
                if task_status == "yes":
                    completed_task_list.append(task_title)

                if task_status == "no":
                    incompleted_task_list.append(task_title)
                    date_compare = datetime.strptime(due_date_task,
                                                     "%Y-%m-%d").date()
                    if date_compare < today:
                        overdue_task_list.append(task_title)

            # Counting tasks in lists
            completed_task_count = len(completed_task_list)
            incompleted_task_count = len(incompleted_task_list)
            persent_complete = round((completed_task_count/line_count)*100)
            persent_incomplete = round((incompleted_task_count/line_count)*100)
            overdue_task_count = len(overdue_task_list)
            persent_overdue = round((overdue_task_count/line_count)*100)

    except FileNotFoundError:
        print("Error: File for tasks not found.")

    # write task_overview.txt
    with open("task_overview", "w") as f:
        f.write(
            "\nOverview of tasks generated using the task_manager.py"
            f"\nTotal active tasks:              {line_count}"
            f"\nThe total of deleted tasks:      {lines_del_count}"
            f"\nTotal number of generated tasks: {total_tasks}"
            "\n"
            "\nOverview of task completeness"
            f"\nNumber of completed tasks:          {completed_task_count}"
            f"\nPercentage of completed tasks:      {persent_complete}%"
            f"\nNumber of incompleted tasks:        {incompleted_task_count}"
            f"\nPercentage of incompleted tasks:    {persent_incomplete}%"
            f"\nIncompleted tasks that are overdue: {overdue_task_count}"
            f"\nPercentage of overdue tasks:        {persent_overdue}%"
        )

    # get statistics for user overview
    with open("user_overview.txt", "w") as f:
        f.write("Overview of users and tasks assigend to them\n")
        f.write(f"\nTotal tasks generated by program: {total_tasks}"
                f"\nTotal amount of users:            {len(usernames_list)}\n")

    for user_obj in user_list:
        # Filter tasks for this user
        user_tasks = [task for task in task_list if task.user == user_obj.name]

        # Separate completed vs uncompleted
        completed_tasks = [task for task in user_tasks
                           if task.completed.lower() == "yes"]
        uncompleted_tasks = [task for task in user_tasks
                             if task.completed.lower() == "no"]

        # Find overdue tasks (only among uncompleted)
        overdue_tasks = [
            task for task in uncompleted_tasks
            if datetime.strptime(task.due_date, "%Y-%m-%d").date() < today
        ]

        # Count
        try:
            total = len(user_tasks)
            persent_total = round((total/total_tasks) * 100)
            completed_count = len(completed_tasks)
            uncompleted_count = len(uncompleted_tasks)
            per_uncompleted_count = round((uncompleted_count/total) * 100)
            overdue_count = len(overdue_tasks)
            per_overdue_count = round((overdue_count/total) * 100)

        except ZeroDivisionError:
            persent_total = 0
            per_uncompleted_count = 0
            per_overdue_count = 0

        # write statistics of tasks per user to file
        with open("user_overview.txt", "a") as f:
            f.write(
                f"\nStats for {user_obj.name}:"
                f"\nTotal tasks:                    {total}"
                f"\n% of all tasks assigned:        {persent_total}%"
                f"\nCompleted:                      {completed_count}"
                f"\nUncompleted:                    {uncompleted_count}"
                f"\n% of tasks uncompleted:         {per_uncompleted_count}%"
                f"\nOverdue:                        {overdue_count}"
                f"\n% of incompleted tasks overdue: {per_overdue_count}%\n"
            )
    print("\nReprots succesfully generated.\n")


def menu_admin(username_input):  # shows menu when admin loged in
    '''
    Displays the menu for the admin, calls functions accordingly.
    '''
    while True:
        # Present the menu to the admin and
        # make sure that the user input is converted to lower case.
        menu = input(
            '''Select one of the following options:
            r   - register a user
            a   - add task
            va  - view all tasks
            vm  - view my tasks
            vc  - view completed tasks
            del - delete tasks
            ds  - display statistics
            gr  - generate reports
            e   - exit

            Choice: ''').lower()

        if menu == 'r':  # register new user to the user.txt file
            reg_user()

        elif menu == 'a':  # add a new task to task.txt file
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(username_input)

        elif menu == 'vc':
            view_completed()

        elif menu == 'del':
            delete_task()

        elif menu == 'ds':
            display_statistics()

        elif menu == 'gr':
            generate_reports()

        elif menu == 'e':
            print('Goodbye!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")


def menu_not_admin(username_input):  # shows menu when non-admin logend in
    '''
    Displays the menu for non-admins, calls functions accordingly.
    '''
    while True:
        # Present the menu to the non_admin and
        # make sure that the user input is converted to lower case.
        menu = input(
            '''Select one of the following options:
            a   - add task
            va  - view all tasks
            vm  - view my tasks
            e   - exit

            Choice: ''').lower()

        if menu == 'a':  # add a new task to task.txt file
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(username_input)

        elif menu == 'e':
            print('Goodbye!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")


# ====== Foundation ======

# Dynamic file names and paths of input files
user_file_name = "user.txt"
user_file_path = os.path.join(os.getcwd(), user_file_name)
task_file_name = "tasks.txt"
task_file_path = os.path.join(os.getcwd(), task_file_name)

# Empty Lists needed for functions
user_list = []  # list of User objects
str_user_list = []  # for login
usernames_list = []  # used in reg_user, view_mine, and statistics functions
task_list = []  # list of Task objects
deleted_task_list = []  # used in the delete_task function
completed_task_list = []  # used in statistics functions
incompleted_task_list = []  # used in statistics functions
overdue_task_list = []  # used in statistics functions

# ----- Base code needed for most functions and login-----

# To read user file, create User objects, and append to user_list
if os.path.exists(user_file_name):

    try:

        with open(user_file_name, "r") as f:  # reading the file

            for line in f:
                contents = line.split(", ")

                stored_username = contents[0]
                stored_user_password = contents[1]
                clean_user_password = stored_user_password.strip()

                # creating an User object and adding it to the user list
                user_object = User(stored_username, clean_user_password)
                user_list.append(user_object)
                str_user_list.append(str(user_object))

                # used to not duplicate usernames when reg_user
                usernames_list.append(stored_username)

    except FileNotFoundError:
        print("An error occurred."
              f"Please check the integrity of {user_file_name}."
              )

else:
    print(
        f"Error, please make sure {user_file_name} is downloaded "
        f"in your current working folder: \n{user_file_path}"
        )

# To read tasks file, create Task objects, and append to task_list
if os.path.exists(task_file_name):

    try:
        with open(task_file_name, "r") as file:
            for line in file:
                contents = line.strip().split(", ")

                task_user = contents[0]
                task_title = contents[1]
                description_task = contents[2]
                date_task_assigned = contents[3]
                due_date_task = contents[4]
                task_status = contents[5]

                task_object = Task(task_user, task_title, description_task,
                                   date_task_assigned, due_date_task,
                                   task_status)
                task_list.append(task_object)

    except FileNotFoundError:
        print("An error occurred."
              f"Please check the integrity of {task_file_name}."
              )

else:
    print(
        f"Error, please make sure {task_file_name} is downloaded "
        f"in your current working folder: \n{task_file_path}"
        )

# ==== Login Section ====

while True:  # while loop for user input to log in
    username_input = input("Username: ").lower()
    password_input = input("Password: ")
    login_object = f"{username_input}, {password_input}"

    try:
        if login_object in str_user_list:
            print("Access granted.\n")
            if username_input == "admin":
                menu_admin(username_input)
            else:
                menu_not_admin(username_input)
            break

        else:
            print("Access denied. Please try again.")

    except TypeError:
        print("Internal error: user list is not valid.")
