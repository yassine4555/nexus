"""Authentication routes for user registration and login."""

from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from models import User, InviteCode, db  # ← Added InviteCode here
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user – now supports invite_code"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(status=400, message='Request body is required'), 400

        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        invite_code_str = data.get('invite_code') or data.get('code')

        if not email or not password:
            return jsonify(status=400, message='Email and password are required'), 400

        if not validate_email(email):
            return jsonify(status=400, message='Invalid email format'), 400

        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify(status=400, message=message), 400

        if User.query.filter_by(email=email).first():
            return jsonify(status=409, message='Email already registered'), 409

        manager_id = None
        code_obj = None  # ← Important: define outside the if block

        if invite_code_str:
            # Make code case-insensitive and remove spaces
            clean_code = invite_code_str.strip().upper()
            code_obj = InviteCode.query.filter_by(code=clean_code).first()

            if not code_obj or not code_obj.is_valid():
                return jsonify(status=400, message='Invalid or expired invite code'), 400

            manager_id = code_obj.manager_id

            # Update usage count
            code_obj.used_count += 1

            if code_obj.max_uses == 1:
                code_obj.used_at = datetime.utcnow()
                # used_by will be set after user creation

            if code_obj.max_uses and code_obj.used_count >= code_obj.max_uses:
                code_obj.is_active = False

        new_user = User(
            email=email,
            role='employee',
            first_name=data.get('first_name') or data.get('firstName'),
            last_name=data.get('last_name') or data.get('lastName'),
            address=data.get('address'),
            department=data.get('department'),
            
            
            manager_id=manager_id
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.flush()  # Get new_user.id

        # If it was a one-time code → assign the user who used it
        if code_obj and code_obj.used_by is None:
             code_obj.used_by = new_user.id
        code_obj.used_at = datetime.utcnow()  

        db.session.commit()

        access_token = create_access_token(identity=str(new_user.id))

        return jsonify(
            status=201,
            message='Account created successfully',
            data={
                'access_token': access_token,
                'user': new_user.to_dict()
            }
        ), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Register error: {e}")
        return jsonify(status=500, message='Internal server error'), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify(status=400, message='Email and password are required'), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify(status=401, message='Invalid email or password'), 401
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify(
            status=200,
            message='Login successful',
            data={
                'access_token': access_token,
                'user': user.to_dict()
            }
        ), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {e}")
        return jsonify(status=500, message='Internal server error'), 500