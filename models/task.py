
#task class-> represebts an individual task belonging to a project
class Task:
    #Represents a task in a project.
    _id_counter = 1

    def __init__(self, title: str, project_id: int, assigned_user_id: int = None):
        self._id = Task._id_counter
        Task._id_counter += 1

        self._title = title
        self._project_id = project_id
        self._assigned_user_id = assigned_user_id
        self._status = "Pending"
        
    #Properties
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def project_id(self):
        return self._project_id

    @property
    def assigned_user_id(self):
        return self._assigned_user_id

    @property
    def status(self):
        return self._status

    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value

    # Instance Methods
    def assign_user(self, user_id: int):
        #Assign this task to a user.
        self._assigned_user_id = user_id

    def mark_complete(self):
        #Mark the task as completed.
        self._status = "Completed"

    def update_status(self, status: str):
        #Update task status safely.
        if status not in ["Pending", "Completed"]:
            raise ValueError("Invalid status.")
        self._status = status

    def to_dict(self):
        #Convert task to dictionary for JSON storage.
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "assigned_user_id": self.assigned_user_id,
            "status": self.status
        }

    def __str__(self):
        return f"[Task {self.id}] {self.title} - {self.status}"