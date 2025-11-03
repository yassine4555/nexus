from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
hr_bp = Blueprint('hr', __name__, url_prefix='/hr')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(status=400, message='Email and password required'), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify(status=409, message='Email already exists'), 409

    new_user = User(
        email=data['email'],
        role=data.get('role', 'employee'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify(status=201, data=new_user.to_dict(), message='Account created'), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(status=400, message='Email and password required'), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify(status=401, message='Invalid credentials'), 401

    access_token = create_access_token(identity=user.id)

    return jsonify(status=200, data={'access_token': access_token, 'user': user.to_dict()}, message='Logged in successfully'), 200


@hr_bp.route('/assignemployee', methods=['POST'])
@jwt_required()
def assign_employee():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user or current_user.role != 'hr':
        return jsonify(status=403, message='HR role required'), 403

    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('manager_id'):
        return jsonify(status=400, message='Email, password, and manager_id required'), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify(status=409, message='Email already exists'), 409

    manager = User.query.get(data['manager_id'])
    if not manager or manager.role != 'manager':
        return jsonify(status=404, message='Manager not found or invalid role'), 404

    new_employee = User(
        email=data['email'],
        role='employee',
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        manager_id=manager.id
    )
    new_employee.set_password(data['password'])

    db.session.add(new_employee)
    db.session.commit()

    return jsonify(status=201, data=new_employee.to_dict(), message='Employee added to team'), 201