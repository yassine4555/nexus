# routes/invite.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, InviteCode, db
from utils.decorators import role_required
from datetime import datetime, timedelta

invite_bp = Blueprint('invite', __name__, url_prefix='/invite')

@invite_bp.route('/codes', methods=['POST'])
@jwt_required()
@role_required('manager', 'hr')
def create_invite_code():
    """Manager or HR generates an invite code"""
    data = request.get_json() or {}
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)

    max_uses = data.get('max_uses', 1)
    if max_uses is not None and max_uses < 1:
        max_uses = 1

    expires_in_days = data.get('expires_in_days', 90)
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days) if expires_in_days else None

    # Generate unique code
    while True:
        code = InviteCode.generate_code(10)
        if not InviteCode.query.filter_by(code=code).first():
            break

    new_code = InviteCode(
        code=code,
        manager_id=current_user.id,
        max_uses=max_uses or None,
        expires_at=expires_at
    )
    db.session.add(new_code)
    db.session.commit()

    return jsonify(status=201, message="Invite code created", data=new_code.to_dict()), 201


@invite_bp.route('/codes', methods=['GET'])
@jwt_required()
@role_required('manager', 'hr')
def my_codes():
    """List all active codes created by the current manager/HR"""
    current_user_id = int(get_jwt_identity())
    codes = InviteCode.query.filter_by(manager_id=current_user_id).order_by(InviteCode.created_at.desc()).all()
    return jsonify(status=200, data=[c.to_dict() for c in codes]), 200


@invite_bp.route('/codes/<code>', methods=['DELETE'])
@jwt_required()
@role_required('manager', 'hr')
def revoke_code(code):
    current_user_id = int(get_jwt_identity())
    invite = InviteCode.query.filter_by(code=code, manager_id=current_user_id).first_or_404()
    invite.is_active = False
    db.session.commit()
    return jsonify(status=200, message="Code revoked"), 200