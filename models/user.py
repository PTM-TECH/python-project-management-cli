
from models.person import Person

#user class which inherits from Person
class User(Person):
    # Class-level counter for unique IDs
    _id_counter = 1  

    def __init__(self, name: str, email: str):
        super().__init__(name, email)

        self._id = User._id_counter
        User._id_counter += 1
        
        # One-to-many relationship
        self._projects = []  

    # properties
    @property
    def id(self):
        return self._id

    @property
    def projects(self):
        return self._projects

    #instance methods
    def add_project(self, project):
        #assign a project to this user.
        self._projects.append(project)

    def remove_project(self, project):
        #remove a project from the user.
        if project in self._projects:
            self._projects.remove(project)

    def to_dict(self):
        #convert user to dictionary for JSON storage.
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [project.id for project in self._projects]
        }

    def __str__(self):
        return f"[User {self.id}] {self.name} - {len(self.projects)} project(s)"