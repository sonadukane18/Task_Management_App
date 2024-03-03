// static/js/app.js

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const taskForm = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');
    const recommendButton = document.getElementById('recommendTask');
    const recommendedTask = document.getElementById('recommendedTask');

    // Event listener for adding a task
    taskForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get task description and priority from form
        const description = document.getElementById('taskDescription').value;
        const priority = document.getElementById('taskPriority').value;

        // Validate task description and priority
        if (description.trim() === '') {
            alert('Please enter a task description.');
            return;
        }

        if (priority === 'Choose...') {
            alert('Please select a task priority.');
            return;
        }

        // Send AJAX POST request to add task
        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description, priority })
        })
        .then(response => response.json())
        .then(data => {
            // Refresh task list
            listTasks();
        })
        .catch(error => console.error('Error adding task:', error));
    });

    // Event listener for removing a task
    taskList.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-task')) {
            const description = event.target.dataset.description;

            // Send AJAX DELETE request to remove task
            fetch(`/remove_task?description=${description}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                // Refresh task list
                listTasks();
            })
            .catch(error => console.error('Error removing task:', error));
        }
    });

    // Event listener for recommending a task
    recommendButton.addEventListener('click', function() {
        // Send AJAX GET request to recommend task
        fetch('/recommend_task')
        .then(response => response.json())
        .then(data => {
            if (data.hasOwnProperty('message')) {
                // No tasks available for recommendation
                alert(data.message);
            } else {
                // Display recommended task
                recommendedTask.textContent = `Recommended task: ${data.description} - Priority: ${data.priority}`;
                recommendedTask.style.display = 'block';
            }
        })
        .catch(error => console.error('Error recommending task:', error));
    });
    // for making tasklists collapsable
    document.addEventListener("DOMContentLoaded", function() {
    // Get the task list header element
    var header = document.querySelector('.task-list-header');

    // Get the task list body element
    var body = document.querySelector('.task-list-body');

    // Add click event listener to the header
    header.addEventListener('click', function() {
        // Toggle the visibility of the task list body
        if (body.style.display === 'none') {
            body.style.display = 'block';
        } else {
            body.style.display = 'none';
        }
    });
});

    // Function to add a task to the list
    function addTask(description, priority) {
        // Check if the task already exists
        if (tasks.find(task => task.description === description)) {
            alert('Task already exists.');
            return;
        }

        // Add the task to the tasks array
        tasks.push({ description, priority });

        // Save tasks to server
        saveTasks();

        // Refresh task list
        listTasks();
    }

    // Function to list tasks
    function listTasks() {
        // Clear existing task list
        taskList.innerHTML = '';

        // Send AJAX GET request to list tasks
        fetch('/list_tasks')
        .then(response => response.json())
        .then(tasks => {
            // Render tasks in task list
            tasks.forEach(task => {
                const listItem = document.createElement('li');
                listItem.classList.add('list-group-item');
                listItem.textContent = `${task.description} - Priority: ${task.priority}`;

                // Add remove button
                const removeButton = document.createElement('button');
                removeButton.textContent = 'Remove';
                removeButton.classList.add('btn', 'btn-danger', 'btn-sm', 'remove-task');
                removeButton.setAttribute('data-description', task.description);
                removeButton.style.float = 'right'; // Align button to the right
                listItem.appendChild(removeButton);

                taskList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error listing tasks:', error));
    }
    // Initial task listing
    listTasks();
});
