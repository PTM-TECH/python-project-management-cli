
#CLI entry point for the Project Tracker system.

import argparse
from rich.console import Console
from rich.table import Table
from utils.storage import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task
from utils.validators import validate_email, validate_positive_int, validate_status

console = Console()
users, projects, tasks = load_data()

#setup argparse with subcommands
def create_parser():
    parser = argparse.ArgumentParser(
        description="CLI Project Management Tool"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Add User
    add_user = subparsers.add_parser("add-user", help="Add a new user")
    add_user.add_argument("--name", required=True, help="User name")
    add_user.add_argument("--email", required=True, help="User email")

    # List Users
    subparsers.add_parser("list-users", help="List all users")
    
    # Add Project
    add_project = subparsers.add_parser("add-project", help="Add a new project")
    add_project.add_argument("--user-id", type=int, required=True, help="Owner user ID")
    add_project.add_argument("--title", required=True, help="Project title")
    add_project.add_argument("--description", default="", help="Project description")

    # List Projects
    list_projects = subparsers.add_parser("list-projects", help="List projects")
    list_projects.add_argument("--user-id", type=int, help="Filter by user ID")

    # View Project
    view_project = subparsers.add_parser("view-project", help="View project details")
    view_project.add_argument("--id", type=int, required=True, help="Project ID")
    
    # Add Task
    add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    add_task.add_argument("--project-id", type=int, required=True, help="Project ID")
    add_task.add_argument("--title", required=True, help="Task title")
    add_task.add_argument("--user-id", type=int, help="Assign to user ID (optional)")

    # List Tasks
    list_tasks = subparsers.add_parser("list-tasks", help="List tasks for a project")
    list_tasks.add_argument("--project-id", type=int, required=True, help="Project ID")

    # Complete Task
    complete_task = subparsers.add_parser("complete-task", help="Mark task as complete")
    complete_task.add_argument("--id", type=int, required=True, help="Task ID")

    # Assign Task
    assign_task = subparsers.add_parser("assign-task", help="Assign task to a user")
    assign_task.add_argument("--id", type=int, required=True, help="Task ID")
    assign_task.add_argument("--user-id", type=int, required=True, help="User ID")

    # Update Task Status
    update_task = subparsers.add_parser("update-task-status", help="Update task status")
    update_task.add_argument("--id", type=int, required=True, help="Task ID")
    update_task.add_argument(
        "--status", required=True, choices=["Pending", "Completed"], help="New status"
    )

    return parser

#implement command logic

def handle_add_user(args):
    if not validate_email(args.email):
        console.print(f"[red]Error: Invalid email format '{args.email}'[/red]")
        return
    try:
        user = User(args.name, args.email)
        users.append(user)
        save_data(users, projects, tasks)
        console.print(f"[green]User '{user.name}' added successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        
#List users with rich table
def handle_list_users():
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users")

    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Projects")

    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            str(len(user.projects))
        )

    console.print(table)
#Find user helper function
def find_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_project(project_id):
    for project in projects:
        if project.id == project_id:
            return project
    return None

#add project handler
def handle_add_project(args):
    if not validate_positive_int(args.user_id):
        console.print(f"[red]Error: User ID must be a positive integer[/red]")
        return

    user = find_user(args.user_id)
    if not user:
        console.print("[red]Error: User not found.[/red]")
        return

    try:
        project = Project(args.title, user.id, args.description)
        projects.append(project)
        user.add_project(project)
        save_data(users, projects, tasks)
        console.print(f"[green]Project '{project.title}' created successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

#List projects with optional filter    
def handle_list_projects(args):
    filtered_projects = projects

    if args.user_id:
        filtered_projects = [p for p in projects if p.user_id == args.user_id]

        if not find_user(args.user_id):
            console.print("[red]Error: User not found.[/red]")
            return

    if not filtered_projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="Projects")

    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Owner ID")
    table.add_column("Tasks")

    for project in filtered_projects:
        table.add_row(
            str(project.id),
            project.title,
            str(project.user_id),
            str(len(project.tasks))
        )

    console.print(table)
#View project details
def handle_view_project(args):
    project = find_project(args.id)

    if not project:
        console.print("[red]Error: Project not found.[/red]")
        return

    console.print(f"[bold cyan]Project Details[/bold cyan]")
    console.print(f"ID: {project.id}")
    console.print(f"Title: {project.title}")
    console.print(f"Description: {project.description}")
    console.print(f"Owner ID: {project.user_id}")
    console.print(f"Tasks: {len(project.tasks)}")
    
#find task helper function
def find_task(task_id):
    for task in tasks:
        if task.id == task_id:
            return task
    return None
#add task
def handle_add_task(args):
    if not validate_positive_int(args.project_id):
        console.print("[red]Error: Project ID must be a positive integer[/red]")
        return
    project = find_project(args.project_id)
    if not project:
        console.print("[red]Error: Project not found.[/red]")
        return

    assigned_user_id = None
    if args.user_id:
        user = find_user(args.user_id)
        if not user:
            console.print("[red]Error: User not found.[/red]")
            return
        assigned_user_id = user.id

    try:
        task = Task(args.title, project.id, assigned_user_id)
        tasks.append(task)
        project.add_task(task)
        save_data(users, projects, tasks)
        console.print(f"[green]Task '{task.title}' added to project '{project.title}'[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        
#list task
def handle_list_tasks(args):
    project = find_project(args.project_id)
    if not project:
        console.print("[red]Error: Project not found.[/red]")
        return

    if not project.tasks:
        console.print("[yellow]No tasks found for this project.[/yellow]")
        return

    table = Table(title=f"Tasks for Project: {project.title}")

    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Assigned User ID")

    for task in project.tasks:
        table.add_row(
            str(task.id),
            task.title,
            task.status,
            str(task.assigned_user_id) if task.assigned_user_id else "-"
        )

    console.print(table)
#Complete task
def handle_complete_task(args):
    task = find_task(args.id)
    if not task:
        console.print("[red]Error: Task not found.[/red]")
        return
    task.mark_complete()
    save_data(users, projects, tasks)
    console.print(f"[green]Task '{task.title}' marked as Completed.[/green]")

#Assign task
def handle_assign_task(args):
    task = find_task(args.id)
    if not task:
        console.print("[red]Error: Task not found.[/red]")
        return

    user = find_user(args.user_id)
    if not user:
        console.print("[red]Error: User not found.[/red]")
        return

    task.assign_user(user.id)
    save_data(users, projects, tasks)
    console.print(f"[green]Task '{task.title}' assigned to user '{user.name}'[/green]")
    
#update task status
def handle_update_task_status(args):
    if not validate_status(args.status):
        console.print(f"[red]Error: Invalid status '{args.status}'[/red]")
        return
    task = find_task(args.id)
    if not task:
        console.print("[red]Error: Task not found.[/red]")
        return

    try:
        task.update_status(args.status)
        save_data(users, projects, tasks)
        console.print(f"[green]Task '{task.title}' status updated to {task.status}[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    
#connect commands to handlers
def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "add-user":
        handle_add_user(args)

    elif args.command == "list-users":
        handle_list_users()
        
    elif args.command == "add-project":
        handle_add_project(args)

    elif args.command == "list-projects":
        handle_list_projects(args)

    elif args.command == "view-project":
        handle_view_project(args)
    
    elif args.command == "add-task":
        handle_add_task(args)

    elif args.command == "list-tasks":
        handle_list_tasks(args)

    elif args.command == "complete-task":
        handle_complete_task(args)

    elif args.command == "assign-task":
        handle_assign_task(args)

    elif args.command == "update-task-status":
        handle_update_task_status(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()