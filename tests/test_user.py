import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models.user import User
from models.project import Project

def test_user_creation():
    user = User("Patrick", "patrick@gmail.com")
    assert user.name == "Patrick"
    assert user.email == "patrick@gmail.com"
    assert user.projects == []

def test_user_add_project():
    user = User("Patrick", "patrick@gmail.com")
    project = Project("CLI Project", user.id)
    user.add_project(project)
    assert project in user.projects