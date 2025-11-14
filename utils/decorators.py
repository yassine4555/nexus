"""Custom decorators for route protection."""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User


def role_required(*roles):
    """
    Decorator to require specific role(s) for accessing a route.
    
    Usage:
        @role_required('hr')
        @role_required('hr', 'manager')
    
    Args:
        *roles: Variable number of role names that are allowed
        
    Returns:
        Decorator function
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify(status=401, message='User not found'), 401
            
            if current_user.role not in roles:
                return jsonify(
                    status=403,
                    message=f'Access denied. Required role(s): {", ".join(roles)}'
                ), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
