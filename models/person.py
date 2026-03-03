
#Base class -> person

class Person:

    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    # --- Properties ---
    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    def __str__(self):
        return f"{self.name} ({self.email})"