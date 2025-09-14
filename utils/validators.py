import re
from datetime import datetime

def validate_username(username):
    return len(username) >= 3 and re.match(r'^[a-zA-Z0-9_]+$', username)

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def validate_password(password):
    """Validate password meets requirements"""
    if len(password) < 8:
        return False
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check for at least one number
    if not re.search(r'[0-9]', password):
        return False
    
    # Check for at least one special character
    if not re.search(r'[@$!%*?&]', password):
        return False
    
    return True

def validate_sex(sex):
    return sex.lower() in ['male', 'female', 'other']

def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False