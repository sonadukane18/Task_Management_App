import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import random

# Initialize an empty task dictionary
tasks = {}

# Load pre-existing tasks from a CSV file (if any)
try:
    tasks_df = pd.read_csv('tasks.csv')
    tasks = tasks_df.set_index('description')['priority'].to_dict()
except FileNotFoundError:
    pass

# Train the task priority classifier
vectorizer = CountVectorizer()
clf = MultinomialNB()
model = make_pipeline(vectorizer, clf)
model.fit(list(tasks.keys()), list(tasks.values()))


# Function to save tasks to a CSV file
def save_tasks():
    tasks_df = pd.DataFrame(list(tasks.items()), columns=['description', 'priority'])
    tasks_df.to_csv('tasks.csv', index=False)


# Function to add a task to the list
def add_task(description, priority):
    tasks[description] = priority
    save_tasks()


# Function to remove a task by description
def remove_task(description):
    if description in tasks:
        del tasks[description]
        save_tasks()
    else:
        print("Task not found.")


# Function to list all tasks
def list_tasks():
    if not tasks:
        print("No tasks available.")
    else:
        tasks_df = pd.DataFrame(list(tasks.items()), columns=['Description', 'Priority'])
        print(tasks_df)


# Function to recommend a task based on machine learning
def recommend_task():
    if tasks:
        # Get high-priority tasks
        high_priority_tasks = [desc for desc, priority in tasks.items() if priority == 'High']

        if high_priority_tasks:
            # Choose a random high-priority task
            random_task = random.choice(high_priority_tasks)
            print(f"Recommended task: {random_task} - Priority: High")
        else:
            print("No high-priority tasks available for recommendation.")
    else:
        print("No tasks available for recommendations.")


# Main menu
while True:
    print("\nTask Management App")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. List Tasks")
    print("4. Recommend Task")
    print("5. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        description = input("Enter task description: ")
        priority = input("Enter task priority (Low/Medium/High): ").capitalize()
        if priority not in {'Low', 'Medium', 'High'}:
            print("Invalid priority. Please enter either Low, Medium, or High.")
            continue
        add_task(description, priority)
        print("Task added successfully.")

    elif choice == "2":
        description = input("Enter task description to remove: ")
        remove_task(description)
        print("Task removed successfully.")

    elif choice == "3":
        list_tasks()

    elif choice == "4":
        recommend_task()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please select a valid option.")
