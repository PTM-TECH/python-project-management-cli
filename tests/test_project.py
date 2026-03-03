import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models.project import Project
from models.task import Task

def test_project_creation():
    project = Project("CLI Project", user_id=1, description="Developing CLI Project")
    assert project.title == "CLI Project"
    assert project.description == "Developing CLI Project"
    assert project.tasks == []

def test_project_add_task():
    project = Project("CLI Project", user_id=1)
    task = Task("Build CLI", project_id=project.id)
    project.add_task(task)
    assert task in project.tasks