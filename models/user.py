"""User model for authentication and authorization."""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db


class User(db.Model):
    """User model with role-based access control."""
    
    __tablename__ = 'users'
    
    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # 'hr', 'manager', 'employee'
    
    # Personal information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    
    # Work information
    department = db.Column(db.String(100))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employees = db.relationship(
        'User',
        backref=db.backref('manager', remote_side=[id]),
        lazy='dynamic'
    )
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """Convert user object to dictionary."""
        data = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'department': self.department,
            'manager_id': self.manager_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data['address'] = self.address
            data['date_of_birth'] = self.date_of_birth.isoformat() if self.date_of_birth else None
        
        return data
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
