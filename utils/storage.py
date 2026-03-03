
import json
import os

from models.user import User
from models.project import Project
from models.task import Task

FILE = "data/file.json"

def save_data(users, projects, tasks):

    #Save all users, projects, and tasks to JSON file.

    data = {
        "users": [user.to_dict() for user in users],
        "projects": [project.to_dict() for project in projects],
        "tasks": [task.to_dict() for task in tasks],
    }

    try:
        with open(FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")
        
def load_data():
    #Load data from JSON file.
    #Returns lists of User, Project, and Task objects.

    if not os.path.exists(FILE):
        return [], [], []

    try:
        with open(FILE, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Warning: Corrupt JSON file. Starting fresh.")
        return [], [], []
    except IOError as e:
        print(f"Error loading data: {e}")
        return [], [], []

    return rebuild_objects(data)

def rebuild_objects(data):
    
    #Rebuild Python objects from loaded JSON data.
    users = []
    projects = []
    tasks = []

    user_lookup = {}
    project_lookup = {}

    # Rebuild Users
    for user_data in data.get("users", []):
        user = User(user_data["name"], user_data["email"])
        user._id = user_data["id"]
        users.append(user)
        user_lookup[user.id] = user

    # Update User ID counter
    if users:
        User._id_counter = max(user.id for user in users) + 1

    # Rebuild Projects
    for project_data in data.get("projects", []):
        project = Project(
            project_data["title"],
            project_data["user_id"],
            project_data.get("description", "")
        )
        project._id = project_data["id"]
        projects.append(project)
        project_lookup[project.id] = project

    if projects:
        Project._id_counter = max(project.id for project in projects) + 1

    # Rebuild Tasks
    for task_data in data.get("tasks", []):
        task = Task(
            task_data["title"],
            task_data["project_id"],
            task_data.get("assigned_user_id")
        )
        task._id = task_data["id"]
        task.update_status(task_data["status"])
        tasks.append(task)

    if tasks:
        Task._id_counter = max(task.id for task in tasks) + 1

    # Reconnect Relationships
    for project in projects:
        user = user_lookup.get(project.user_id)
        if user:
            user.add_project(project)

    for task in tasks:
        project = project_lookup.get(task.project_id)
        if project:
            project.add_task(task)

    return users, projects, tasks