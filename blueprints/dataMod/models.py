from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'hr', 'manager', 'employee'
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    adress = db.Column(db.String(200))
    department = db.Column(db.String(100))

    employeesList = db.Column(db.ARRAY(db.String(120)))  # Liste des emails des employés sous ce manager
    #manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Self-reference pour assigner à un manager
    dateOfBirth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation pour les employés d'un manager (optionnel, pour queries futures)
    employees = db.relationship('User', backref=db.backref('manager', remote_side=[id]))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
           # 'manager_id': self.manager_id
        }