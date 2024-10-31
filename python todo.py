from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Initialize lists to store tasks and their statuses
tasks = []  # Main task list
hidden_tasks = []  # List for hidden tasks
PASSWORD = "your_password"  # Change this to set a password for hiding tasks

# HTML template with enhanced UI and animations
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced To-Do List</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
            padding: 20px;
        }

        .container {
            background: #fff;
            padding: 30px 25px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
            text-align: center;
            animation: fadeIn 0.7s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        h1 {
            color: #333;
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .form input[type="text"] {
            width: 70%;
            padding: 12px;
            margin-right: 10px;
            border: 2px solid #66a6ff;
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s ease;
        }

        .form input[type="text"]:focus {
            border-color: #3498db;
            outline: none;
        }

        .form button {
            background-color: #3498db;
            color: #fff;
            padding: 12px 18px;
            font-size: 1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .form button:hover {
            background-color: #2980b9;
        }

        .task-list, .hidden-list {
            list-style: none;
            padding: 0;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
            text-align: left;
        }

        .task-list li, .hidden-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 12px;
            background: #f0f4f8;
            border-radius: 8px;
            border: 1px solid #e0e7ef;
            transition: background 0.3s ease;
            animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .task-list li.completed span {
            color: #2ecc71;
            text-decoration: line-through;
        }

        .done-btn.completed {
            background-color: #2ecc71;
        }

        .inline-form {
            display: inline;
        }

        .inline-form button {
            background-color: #ff7675;
            padding: 5px 10px;
            border-radius: 8px;
            color: #fff;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            font-size: 0.9em;
        }

        .inline-form button:hover {
            background-color: #d63031;
        }

        .done-btn {
            background-color: #55efc4;
        }

        .done-btn:hover {
            background-color: #00b894;
        }

        .hide-btn {
            background-color: #636e72;
        }

        .hide-btn:hover {
            background-color: #2d3436;
        }

        .clear-btn {
            background-color: #e17055;
            margin-top: 15px;
            padding: 10px 15px;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            font-size: 1em;
        }

        .clear-btn:hover {
            background-color: #d63031;
        }

        .tab-link {
            color: #3498db;
            cursor: pointer;
            text-decoration: underline;
        }

        .hidden-container {
            background: #f0f4f8;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            display: none;
            animation: fadeIn 0.7s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>To-Do List</h1>
        <a href="#" onclick="toggleHiddenTasks();" class="tab-link">View Hidden Tasks</a>
        <div id="hidden-tasks" class="hidden-container">
            <h2>Hidden Tasks</h2>
            <ul class="hidden-list">
                {% for task in hidden_tasks %}
                <li>
                    <span>{{ task[0] }}</span>
                    <form action="{{ url_for('unhide_task', task_index=loop.index0) }}" method="POST" class="inline-form">
                        <button type="submit" class="done-btn">Unhide</button>
                    </form>
                </li>
                {% endfor %}
            </ul>
            <button onclick="document.getElementById('hidden-tasks').style.display='none';" class="clear-btn">Close</button>
        </div>
        
        <form action="{{ url_for('add_task') }}" method="POST" class="form" onsubmit="saveTasksToLocalStorage();">
            <input type="text" name="task" id="taskInput" placeholder="Enter a new task" required>
            <button type="submit">Add Task</button>
        </form>
        
        <ul class="task-list" id="taskList">
            {% for task, completed in tasks %}
            <li>
                <span>{{ task }}</span>
                <div>
                    <form action="{{ url_for('toggle_done', task_index=loop.index0) }}" method="POST" class="inline-form">
                        <button type="submit" class="done-btn {% if completed %}completed{% endif %}">{{ 'Undo' if completed else 'Done' }}</button>
                    </form>
                    <form action="{{ url_for('hide_task', task_index=loop.index0) }}" method="POST" class="inline-form" onsubmit="return confirmHide();">
                        <button type="submit" class="hide-btn">Hide</button>
                    </form>
                    <form action="{{ url_for('delete_task', task_index=loop.index0) }}" method="POST" class="inline-form">
                        <button type="submit" class="hide-btn">Delete</button>
                    </form>
                </div>
            </li>
            {% endfor %}
        </ul>

        {% if tasks %}
        <form action="{{ url_for('clear_tasks') }}" method="POST" class="form">
            <button type="submit" class="clear-btn">Clear All</button>
        </form>
        {% endif %}
    </div>

    <script>
        // Save tasks to local storage
        function saveTasksToLocalStorage() {
            const taskList = [];
            const tasks = document.querySelectorAll('#taskList li span');
            tasks.forEach(task => {
                taskList.push({ text: task.innerText, completed: task.parentElement.querySelector('.done-btn').classList.contains('completed') });
            });
            localStorage.setItem('tasks', JSON.stringify(taskList));
        }

        // Load tasks from local storage
        function loadTasksFromLocalStorage() {
            const savedTasks = JSON.parse(localStorage.getItem('tasks'));
            if (savedTasks) {
                savedTasks.forEach(task => {
                    addTaskToList(task.text, task.completed);
                });
            }
        }

        // Add a task to the list dynamically
        function addTaskToList(text, completed) {
            const taskList = document.getElementById('taskList');
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="${completed ? 'completed' : ''}">${text}</span>
                <div>
                    <form action="#" method="POST" class="inline-form">
                        <button type="button" class="done-btn ${completed ? 'completed' : ''}" onclick="toggleDone(this)">${completed ? 'Undo' : 'Done'}</button>
                    </form>
                    <form action="#" method="POST" class="inline-form">
                        <button type="button" class="hide-btn" onclick="hideTask(this)">Hide</button>
                    </form>
                    <form action="#" method="POST" class="inline-form">
                        <button type="button" class="hide-btn" onclick="deleteTask(this)">Delete</button>
                    </form>
                </div>
            `;
            taskList.appendChild(li);
        }

        // Toggle done status
        function toggleDone(button) {
            button.classList.toggle('completed');
            const taskText = button.parentElement.parentElement.querySelector('span');
            taskText.classList.toggle('completed');
            saveTasksToLocalStorage();
        }

        // Hide a task
        function hideTask(button) {
            if (confirm('Enter password to hide the task:') === PASSWORD) {
                const taskItem = button.parentElement.parentElement;
                taskItem.remove();
                saveTasksToLocalStorage();
            }
        }

        // Delete a task
        function deleteTask(button) {
            const taskItem = button.parentElement.parentElement;
            taskItem.remove();
            saveTasksToLocalStorage();
        }

        // Confirm hiding a task
        function confirmHide() {
            return confirm('Are you sure you want to hide this task?');
        }

        // Toggle hidden tasks display
        function toggleHiddenTasks() {
            const hiddenTasksDiv = document.getElementById('hidden-tasks');
            hiddenTasksDiv.style.display = hiddenTasksDiv.style.display === 'none' ? 'block' : 'none';
        }

        // Load tasks when the page is loaded
        window.onload = function() {
            loadTasksFromLocalStorage();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, tasks=tasks, hidden_tasks=hidden_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append((task, False))  # Append new task as not completed
    return redirect(url_for('home'))

@app.route('/toggle/<int:task_index>', methods=['POST'])
def toggle_done(task_index):
    if 0 <= task_index < len(tasks):
        task, completed = tasks[task_index]
        tasks[task_index] = (task, not completed)  # Toggle the completed status
    return redirect(url_for('home'))

@app.route('/hide/<int:task_index>', methods=['POST'])
def hide_task(task_index):
    if 0 <= task_index < len(tasks):
        hidden_tasks.append(tasks.pop(task_index))  # Move task to hidden
    return redirect(url_for('home'))

@app.route('/unhide/<int:task_index>', methods=['POST'])
def unhide_task(task_index):
    if 0 <= task_index < len(hidden_tasks):
        tasks.append(hidden_tasks.pop(task_index))  # Move task back to main list
    return redirect(url_for('home'))

@app.route('/delete/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)  # Delete task from main list
    return redirect(url_for('home'))

@app.route('/clear', methods=['POST'])
def clear_tasks():
    global tasks
    tasks = []  # Clear all tasks
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
