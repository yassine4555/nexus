"""Authentication routes for user registration and login."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User, db
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        print("d5al")
        data = request.get_json()
        print(data)
        
        # Validate required fields
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        email = data.get('email', '')
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify(status=400, message='Email and password are required'), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify(status=400, message='Invalid email format'), 400
        
        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify(status=400, message=message), 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify(status=409, message='Email already registered'), 409
        
        # Create new user
        new_user = User(
            email=email,
            role=data.get('role', 'employee'),
            first_name=data.get('firstName', '') or None,
            last_name=data.get('lastName', '') or None,
            address=data.get('address', '') or None,
            date_of_birth=data.get('dateOfBirth', None),
            department=data.get('department', '') or None,
            manager_id=data.get('managerId') or None
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify(
            status=201,
            message='Account created successfully',
            data=new_user.to_dict()
        ), 201
        
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        email = data.get('email', '')
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify(status=400, message='Email and password are required'), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Verify credentials
        if not user or not user.check_password(password):
            return jsonify(status=401, message='Invalid email or password'), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify(
            status=200,
            message='Login successful',
            data={
                'access_token': access_token,
                'user': user.to_dict()
            }
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message='Internal server error'), 500
