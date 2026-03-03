#input validation

import re

def validate_email(email: str) -> bool:
    #Check if email is in a valid format.
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_status(status: str) -> bool:
    #Check if status is valid ('Pending' or 'Completed').
    return status in {"Pending", "Completed"}

def validate_positive_int(value: int) -> bool:
    #Check if a value is a positive integer.
    return isinstance(value, int) and value > 0