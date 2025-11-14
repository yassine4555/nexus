"""HR routes for managing employees and teams."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from utils.validators import validate_email, validate_password
from utils.decorators import role_required

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')


@hr_bp.route('/employees', methods=['POST'])
@jwt_required()
@role_required('hr')
def create_employee():
    """Create a new employee and assign to a manager (HR only)."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        manager_id = data.get('manager_id')
        
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
        
        # Validate manager if provided
        if manager_id:
            manager = User.query.get(manager_id)
            if not manager:
                return jsonify(status=404, message='Manager not found'), 404
            if manager.role != 'manager':
                return jsonify(status=400, message='Assigned user is not a manager'), 400
        
        # Create new employee
        new_employee = User(
            email=email,
            role='employee',
            first_name=data.get('first_name', '').strip() or None,
            last_name=data.get('last_name', '').strip() or None,
            department=data.get('department', '').strip() or None,
            manager_id=manager_id
        )
        new_employee.set_password(password)
        
        db.session.add(new_employee)
        db.session.commit()
        
        return jsonify(
            status=201,
            message='Employee created successfully',
            data=new_employee.to_dict()
        ), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500


@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
@role_required('hr', 'manager')
def get_employees():
    """Get list of employees (HR can see all, managers see their team)."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role == 'hr':
            # HR can see all employees
            employees = User.query.filter_by(role='employee').all()
        elif current_user.role == 'manager':
            # Managers see only their direct reports
            employees = User.query.filter_by(manager_id=current_user_id).all()
        else:
            return jsonify(status=403, message='Access denied'), 403
        
        return jsonify(
            status=200,
            message='Employees retrieved successfully',
            data=[emp.to_dict() for emp in employees]
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message='Internal server error'), 500


@hr_bp.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
@role_required('hr', 'manager')
def get_employee(employee_id):
    """Get specific employee details."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        employee = User.query.get(employee_id)
        
        if not employee:
            return jsonify(status=404, message='Employee not found'), 404
        
        # Check authorization
        if current_user.role == 'manager' and employee.manager_id != current_user_id:
            return jsonify(status=403, message='Access denied'), 403
        
        return jsonify(
            status=200,
            message='Employee retrieved successfully',
            data=employee.to_dict(include_sensitive=True)
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message='Internal server error'), 500


@hr_bp.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
@role_required('hr')
def update_employee(employee_id):
    """Update employee details (HR only)."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify(status=400, message='Request body is required'), 400
        
        employee = User.query.get(employee_id)
        
        if not employee:
            return jsonify(status=404, message='Employee not found'), 404
        
        # Update allowed fields
        if 'first_name' in data:
            employee.first_name = data['first_name'].strip() or None
        if 'last_name' in data:
            employee.last_name = data['last_name'].strip() or None
        if 'department' in data:
            employee.department = data['department'].strip() or None
        if 'manager_id' in data:
            if data['manager_id']:
                manager = User.query.get(data['manager_id'])
                if not manager or manager.role != 'manager':
                    return jsonify(status=400, message='Invalid manager'), 400
            employee.manager_id = data['manager_id']
        
        db.session.commit()
        
        return jsonify(
            status=200,
            message='Employee updated successfully',
            data=employee.to_dict()
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500


@hr_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
@role_required('hr')
def delete_employee(employee_id):
    """Delete an employee (HR only)."""
    try:
        employee = User.query.get(employee_id)
        
        if not employee:
            return jsonify(status=404, message='Employee not found'), 404
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify(
            status=200,
            message='Employee deleted successfully'
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message='Internal server error'), 500
