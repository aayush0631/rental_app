import re
from bson import ObjectId

def validate_email(email):
    """Simple email validation regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_object_id(id_str):
    """Check if a string is a valid MongoDB ObjectId."""
    return ObjectId.is_valid(id_str)

def validate_required_fields(data, fields):
    """
    Returns a list of missing fields from the data.
    """
    missing = [field for field in fields if field not in data or not data[field]]
    return missing
