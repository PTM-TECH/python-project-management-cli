# Python CLI Project Tracker

## Overview
A Python Command-Line Interface (CLI) tool to manage Users, Projects, and Tasks.  
Built with OOP, JSON persistence, and a rich CLI interface.


## Features
- Add/list users
- Add/list/view projects
- Add/list/assign/complete/update tasks
- Dynamic relationships: Users → Projects → Tasks
- Persistent storage in `data/file.json`
- Professional CLI with tables and colors (via `rich`)
- Unit tests with `pytest`

## Installation
1. Clone the repository:

fork the repository
git clone 
cd python-project-management-cli

## Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

## Install dependencies
pip install -r requirements.txt

## Usage - Run the CLI Commands

### Users
python main.py add-user --name "Patrick" --email "patrick@gmail.com"
python main.py list-users

### Projects
python main.py add-project --user-id 1 --title "CLI Project" --description "Developing CLI Project"
python main.py list-projects
python main.py view-project --id 1

### Tasks
python main.py add-task --project-id 1 --title "Build CLI" --user-id 1
python main.py list-tasks --project-id 1
python main.py complete-task --id 1
python main.py assign-task --id 1 --user-id 1
python main.py update-task-status --id 1 --status Pending

## Project Structure
project_Management_CLI/
│
├── main.py
├── requirements.txt
├── README.md
├── models/
│   ├── person.py
│   ├── user.py
│   ├── project.py
│   └── task.py
├── utils/
│   ├── storage.py
│   └── validators.py
├── data/
│   └── file.json
└── tests/
    ├── test_user.py
    ├── test_project.py
    ├── test_task.py
    └── test_storage.py

## Testing
pytest -v

## Author
Patrick Mutua