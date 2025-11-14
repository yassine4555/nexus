"""Routes package."""

from routes.auth import auth_bp
from routes.hr import hr_bp

__all__ = ['auth_bp', 'hr_bp']
