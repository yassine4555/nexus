# models/invite_code.py
from models.database import db
from datetime import datetime, timedelta
import secrets
import string

class InviteCode(db.Model):
    __tablename__ = 'invite_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    max_uses = db.Column(db.Integer, default=1)      # 1 = one-time, None or 0 = unlimited
    used_count = db.Column(db.Integer, default=0)
    used_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    used_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    manager = db.relationship('User', foreign_keys=[manager_id], backref='invite_codes')
    used_by_user = db.relationship('User', foreign_keys=[used_by])

    @staticmethod
    def generate_code(length=10):
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        if self.max_uses and self.used_count >= self.max_uses:
            return False
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'manager_id': self.manager_id,
            'manager_name': f"{self.manager.first_name or ''} {self.manager.last_name or ''}".strip() or self.manager.email,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'max_uses': self.max_uses,
            'used_count': self.used_count,
            'is_active': self.is_active,
            'invite_link': f"http://127.0.0.1:5001/register?code={self.code}"
        }