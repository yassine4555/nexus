"""Routes package."""

from routes.auth import auth_bp
from routes.hr import hr_bp
from routes.users import users_bp

__all__ = ['auth_bp', 'hr_bp', 'users_bp']
