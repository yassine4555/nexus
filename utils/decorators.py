"""Custom decorators for route protection."""

from functools import wraps
from flask import request, jsonify, current_app

def require_api_key(fn):
    """
    Decorator to require Internal API Key for accessing a route.
    Replaces JWT and Role-based security.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-Internal-Key')
        
        if not api_key:
            return jsonify(status=401, message='Missing API Key'), 401
            
        if api_key != current_app.config['INTERNAL_API_KEY']:
            return jsonify(status=403, message='Invalid API Key'), 403
            
        return fn(*args, **kwargs)
    return wrapper
