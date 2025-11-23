"""Input validation utilities."""

import re


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters
    - At least one letter
    - At least one number
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, 'Password is required'
    
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    if not re.search(r'[a-zA-Z]', password):
        return False, 'Password must contain at least one letter'
    
    if not re.search(r'\d', password):
        return False, 'Password must contain at least one number'
    
    return True, 'Valid password'
