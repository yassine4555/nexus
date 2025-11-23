"""Routes package."""

from routes.users import users_bp
from routes.invites import invites_bp

__all__ = ['users_bp', 'invites_bp']
