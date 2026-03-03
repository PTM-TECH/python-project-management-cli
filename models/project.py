
#Project class->project that belongs to a user
#contains multiple tasks
class Project:

    _id_counter = 1

    def __init__(self, title: str, user_id: int, description: str = ""):
        self._id = Project._id_counter
        Project._id_counter += 1

        self._title = title
        self._description = description
        self._user_id = user_id
        # One-to-many relationship (Project → Tasks)
        self._tasks = []  

    #properties
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def user_id(self):
        return self._user_id

    @property
    def tasks(self):
        return self._tasks

    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value
    #instance methods
    def add_task(self, task):
        #Add a task to this project.
        self._tasks.append(task)

    def remove_task(self, task):
        #Remove a task from this project.
        if task in self._tasks:
            self._tasks.remove(task)

    def update_description(self, description: str):
        #Update project description.
        self._description = description

    def to_dict(self):
        #Convert project to dictionary for JSON storage.
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "tasks": [task.id for task in self._tasks]
        }

    def __str__(self):
        return f"[Project {self.id}] {self.title} ({len(self.tasks)} task(s))"