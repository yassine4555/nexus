"""User management routes for CRUD operations (Data Service)."""

from flask import Blueprint, request, jsonify
from models import User, db
from utils.validators import validate_email, validate_password
from utils.decorators import require_api_key

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['POST'])
@require_api_key
def create_user():
    """Create a new user (Internal API)."""
    try:
        data = request.get_json()
        
        # Basic validation
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
            
        email = data.get('email', '').strip()
        
        if User.query.filter_by(email=email).first():
            return jsonify(status=409, message='Email already registered'), 409
            
        # Create user directly
        new_user = User(
            email=email,
            role=data.get('role', 'employee'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            department=data.get('department'),
            manager_id=data.get('manager_id'),
            date_of_birth=data.get('date_of_birth')
        )
        
        # Set password if provided (hashed)
        if 'password' in data:
            new_user.set_password(data['password'])
            
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify(
            status=201,
            message='User created successfully',
            data=new_user.to_dict(include_sensitive=True)
        ), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message=str(e)), 500


@users_bp.route('/', methods=['GET'])
@require_api_key
def get_all_users():
    """Get all users (Internal API)."""
    try:
        # Optional filtering by role
        role = request.args.get('role')
        if role:
            users = User.query.filter_by(role=role).all()
        else:
            users = User.query.all()
        
        return jsonify(
            status=200,
            message='Users retrieved successfully',
            data=[user.to_dict(include_sensitive=True) for user in users]
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message=str(e)), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@require_api_key
def get_user(user_id):
    """Get specific user details (Internal API)."""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(status=404, message='User not found'), 404
        
        return jsonify(
            status=200,
            message='User retrieved successfully',
            data=user.to_dict(include_sensitive=True)
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message=str(e)), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
@require_api_key
def update_user(user_id):
    """Update user details (Internal API)."""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(status=404, message='User not found'), 404
        
        data = request.get_json()
        
        # Update fields directly
        if 'first_name' in data: user.first_name = data['first_name']
        if 'last_name' in data: user.last_name = data['last_name']
        if 'address' in data: user.address = data['address']
        if 'date_of_birth' in data: user.date_of_birth = data['date_of_birth']
        if 'department' in data: user.department = data['department']
        if 'role' in data: user.role = data['role']
        if 'manager_id' in data: user.manager_id = data['manager_id']
        if 'email' in data: user.email = data['email']
        
        if 'password' in data:
            user.set_password(data['password'])
            
        db.session.commit()
        
        return jsonify(
            status=200,
            message='User updated successfully',
            data=user.to_dict(include_sensitive=True)
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message=str(e)), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@require_api_key
def delete_user(user_id):
    """Delete a user (Internal API)."""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(status=404, message='User not found'), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify(
            status=200,
            message='User deleted successfully'
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message=str(e)), 500
