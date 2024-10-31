# To-Do-List-Application
The Enhanced To-Do List Application is a modern, user-friendly web application designed to help users efficiently manage their daily tasks and activities. Built using Flask, this application combines functionality with an attractive user interface, making it an essential tool for anyone looking to stay organized.


Key Features:
Task Management: Easily add new tasks to your list with a simple input field. Users can mark tasks as complete with a click of a button, providing immediate visual feedback through color changes.

Hide and Unhide Tasks: Users can hide tasks they want to keep out of sight by entering a password. This feature helps maintain focus on current priorities without permanently deleting tasks.

Task Deletion: If tasks are no longer needed, users can permanently remove them from their lists with the delete functionality.

Clear All Tasks: With a single button, users can clear the entire task list, allowing for easy reset when starting fresh.

Persistent Storage: Leveraging the browser's local storage, the application saves tasks automatically. This means that users can close their browser and return later to find their tasks still intact.

Responsive and Attractive UI: The application is designed to be fully responsive, adapting seamlessly to different devices and screen sizes. Smooth animations enhance the user experience, making task management more engaging and enjoyable.

Ideal for:
The Enhanced To-Do List Application is perfect for students, professionals, and anyone needing a simple yet effective way to keep track of their tasks. Whether you're managing daily chores, project deadlines, or personal goals, this application provides the tools you need to stay organized and productive.

With its blend of functionality and design, the Enhanced To-Do List Application empowers users to take control of their time and priorities effortlessly.


Enhanced To-Do List Application
Overview
The Enhanced To-Do List Application is a simple yet powerful web application built with Flask that allows users to manage their tasks efficiently. The app provides functionalities to add, complete, hide, unhide, delete, and clear tasks, along with a visually appealing user interface that includes animations and smooth transitions. Tasks are saved in the browser's local storage for persistence across sessions.

Features
Add Tasks: Easily add new tasks to your to-do list.
Complete Tasks: Mark tasks as done with a single click. The button color changes to indicate completion.
Hide Tasks: Hide tasks securely with a password. Hidden tasks are stored in a separate section.
Unhide Tasks: Restore hidden tasks back to the main list.
Delete Tasks: Permanently remove tasks from the list.
Clear All Tasks: Clear the entire task list with a single button click.
Local Storage: Tasks are saved in the browser's local storage, ensuring data persistence across sessions.
Responsive Design: The application is designed to be mobile-friendly and adjusts to various screen sizes.
Smooth UI and Animations: The app features animations for a better user experience.
Prerequisites
Python 3.x
Flask
Installation
Clone this repository or download the code:


git clone <repository-url>
Navigate to the project directory:

cd <project-directory>
Install Flask if you haven't already:

pip install Flask
Save the provided code to a file named app.py in your project directory.

Run the application:

python app.py
Open your web browser and navigate to http://127.0.0.1:5000 to access the To-Do List application.

Usage
Adding a Task: Type your task in the input field and click "Add Task."
Completing a Task: Click the "Done" button next to a task to mark it as completed.
Hiding a Task: Click the "Hide" button next to a task and enter the password to hide it.
Viewing Hidden Tasks: Click the "View Hidden Tasks" link to see and manage hidden tasks.
Unhiding a Task: Click the "Unhide" button next to a hidden task to return it to the main list.
Deleting a Task: Click the "Delete" button to remove a task permanently.
Clearing All Tasks: Click the "Clear All" button to delete all tasks in the list.
Customization
You can change the password for hiding tasks by modifying the PASSWORD variable in the code.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Inspired by various task management applications.
Developed using Flask, HTML, CSS, and JavaScript.
