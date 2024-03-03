# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import random
import csv

# Initialize Flask application
app = Flask(__name__)

# Initialize an empty list to store tasks
tasks = []

# Function to save tasks to CSV
def save_tasks():
    with open('tasks.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['description', 'priority'])
        writer.writeheader()
        writer.writerows(tasks)

# Function to load tasks from CSV
def load_tasks():
    try:
        with open('tasks.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        pass

# Load tasks from CSV when the application starts
load_tasks()

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')


# Route to add a task
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    description = data.get('description')
    priority = data.get('priority')

    # Check if the task already exists
    for task in tasks:
        if task['description'] == description:
            return jsonify({'message': 'Task already exists.'}), 400

    # Add the task to the list
    tasks.append({'description': description, 'priority': priority})
    save_tasks()

    return jsonify({'message': 'Task added successfully'})

# Route to remove a task
@app.route('/remove_task', methods=['DELETE'])
def remove_task():
    description = request.args.get('description')  # Get the description of the task to be removed from the query parameters
    for task in tasks:
        if task['description'] == description:
            tasks.remove(task)  # Remove the task from the tasks list
            save_tasks()
            return jsonify({'message': 'Task removed successfully'})
    return jsonify({'message': 'Task not found'})


# Route to list all tasks
@app.route('/list_tasks')
def list_tasks():
    return jsonify(tasks)  # Return the list of tasks as JSON


# Route to recommend a task
@app.route('/recommend_task')
def recommend_task():
    high_priority_tasks = [task for task in tasks if task['priority'] == 'High']

    if high_priority_tasks:
        random_task = random.choice(high_priority_tasks)
        return jsonify(random_task)
    else:
        return jsonify({'message': 'No high-priority tasks available for recommendation.'})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
