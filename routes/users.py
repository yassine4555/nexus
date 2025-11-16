"""User management routes for CRUD operations."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from utils.validators import validate_email, validate_password
from utils.decorators import role_required

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (requires authentication)."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify(status=401, message='User not found'), 401
        
        # HR can see all users, managers see their team, employees see only themselves
        if current_user.role == 'hr':
            users = User.query.all()
        elif current_user.role == 'manager':
            # Manager sees themselves and their employees
            users = [current_user] + list(User.query.filter_by(manager_id=current_user_id).all())
        else:
            # Regular employees see only themselves
            users = [current_user]
        
        return jsonify(
            status=200,
            message='Users retrieved successfully',
            data=[user.to_dict() for user in users]
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message='Internal server error'), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user details."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify(status=401, message='User not found'), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(status=404, message='User not found'), 404
        
        # Check authorization
        if current_user.role == 'hr':
            # HR can view anyone
            include_sensitive = True
        elif current_user.role == 'manager' and (user.manager_id == current_user_id or user.id == current_user_id):
            # Managers can view themselves and their team
            include_sensitive = True
        elif current_user.id == user_id:
            # Users can view their own details
            include_sensitive = True
        else:
            return jsonify(status=403, message='Access denied'), 403
        
        return jsonify(
            status=200,
            message='User retrieved successfully',
            data=user.to_dict(include_sensitive=include_sensitive)
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message='Internal server error'), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user details."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify(status=401, message='User not found'), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(status=404, message='User not found'), 404
        
        # Authorization check
        if current_user.role == 'hr':
            # HR can update anyone
            can_update_all = True
        elif current_user.id == user_id:
            # Users can update their own info (limited fields)
            can_update_all = False
        else:
            return jsonify(status=403, message='Access denied'), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        # Fields that users can update themselves
        if 'first_name' in data:
            user.first_name = data['first_name'].strip() or None
        if 'last_name' in data:
            user.last_name = data['last_name'].strip() or None
        if 'address' in data:
            user.address = data['address'].strip() or None
        
        # Fields only HR can update
        if can_update_all:
            if 'email' in data:
                new_email = data['email'].strip()
                if not validate_email(new_email):
                    return jsonify(status=400, message='Invalid email format'), 400
                # Check if email already exists for another user
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != user_id:
                    return jsonify(status=409, message='Email already in use'), 409
                user.email = new_email
            
            if 'role' in data:
                if data['role'] not in ['hr', 'manager', 'employee']:
                    return jsonify(status=400, message='Invalid role'), 400
                user.role = data['role']
            
            if 'department' in data:
                user.department = data['department'].strip() or None
            
            if 'manager_id' in data:
                if data['manager_id']:
                    manager = User.query.get(data['manager_id'])
                    if not manager or manager.role != 'manager':
                        return jsonify(status=400, message='Invalid manager'), 400
                user.manager_id = data['manager_id']
        
        # Password update (both users and HR)
        if 'password' in data:
            new_password = data['password'].strip()
            is_valid, message = validate_password(new_password)
            if not is_valid:
                return jsonify(status=400, message=message), 400
            user.set_password(new_password)
        
        db.session.commit()
        
        return jsonify(
            status=200,
            message='User updated successfully',
            data=user.to_dict()
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('hr')
def delete_user(user_id):
    """Delete a user (HR only)."""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(status=404, message='User not found'), 404
        
        # Prevent deleting yourself
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            return jsonify(status=400, message='Cannot delete your own account'), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify(
            status=200,
            message='User deleted successfully'
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500


@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user's details."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify(status=401, message='User not found'), 401
        
        return jsonify(
            status=200,
            message='Current user retrieved successfully',
            data=user.to_dict(include_sensitive=True)
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message='Internal server error'), 500


@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current authenticated user's details."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify(status=401, message='User not found'), 401
        
        data = request.get_json()
        
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        # Users can update their own basic info
        if 'first_name' in data:
            user.first_name = data['first_name'].strip() or None
        if 'last_name' in data:
            user.last_name = data['last_name'].strip() or None
        if 'address' in data:
            user.address = data['address'].strip() or None
        
        # Password update
        if 'password' in data:
            new_password = data['password'].strip()
            is_valid, message = validate_password(new_password)
            if not is_valid:
                return jsonify(status=400, message=message), 400
            user.set_password(new_password)
        
        db.session.commit()
        
        return jsonify(
            status=200,
            message='Profile updated successfully',
            data=user.to_dict(include_sensitive=True)
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500
