import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import save_data, load_data

def test_save_and_load(tmp_path):
    # Override database file for isolation
    from utils import storage
    storage.FILE = tmp_path / "file.json"

    users = [User("Patrick", "patrick@gmail.com")]
    projects = [Project("CLI Project", users[0].id)]
    tasks = [Task("Build CLI", projects[0].id)]

    save_data(users, projects, tasks)

    loaded_users, loaded_projects, loaded_tasks = load_data()
    
    assert len(loaded_users) == 1
    assert len(loaded_projects) == 1
    assert len(loaded_tasks) == 1

    assert loaded_users[0].name == "Patrick"
    assert loaded_projects[0].title == "CLI Project"
    assert loaded_tasks[0].title == "Build CLI"