import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models.task import Task

def test_task_creation():
    task = Task("Build CLI", project_id=1)
    assert task.title == "Build CLI"
    assert task.status == "Pending"
    assert task.assigned_user_id is None

def test_task_assign_and_complete():
    task = Task("Build CLI", project_id=1)
    task.assign_user(1)
    assert task.assigned_user_id == 1
    task.mark_complete()
    assert task.status == "Completed"