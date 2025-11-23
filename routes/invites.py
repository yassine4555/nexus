"""Invite code management routes (Data Service)."""

from datetime import datetime
from flask import Blueprint, request, jsonify
from models import InviteCode, db
from utils.decorators import require_api_key

invites_bp = Blueprint('invites', __name__, url_prefix='/invites')


@invites_bp.route('/', methods=['POST'])
@require_api_key
def create_invite():
    """Create a new invite code."""
    try:
        data = request.get_json()
        if not data or 'manager_id' not in data:
            return jsonify(status=400, message='Manager ID is required'), 400
            
        # Generate code if not provided
        code = data.get('code')
        if not code:
            code = InviteCode.generate_code()
            
        new_invite = InviteCode(
            code=code,
            manager_id=data['manager_id'],
            max_uses=data.get('max_uses', 1),
            expires_at=data.get('expires_at') # Should be ISO format string or None
        )
        
        db.session.add(new_invite)
        db.session.commit()
        
        return jsonify(
            status=201,
            message='Invite code created',
            data=new_invite.to_dict()
        ), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message=str(e)), 500


@invites_bp.route('/<code>', methods=['GET'])
@require_api_key
def get_invite(code):
    """Get invite code details."""
    try:
        invite = InviteCode.query.filter_by(code=code).first()
        
        if not invite:
            return jsonify(status=404, message='Invite code not found'), 404
            
        return jsonify(
            status=200,
            message='Invite code retrieved',
            data=invite.to_dict()
        ), 200
        
    except Exception as e:
        return jsonify(status=500, message=str(e)), 500


@invites_bp.route('/<code>/use', methods=['POST'])
@require_api_key
def use_invite(code):
    """Mark invite code as used."""
    try:
        invite = InviteCode.query.filter_by(code=code).first()
        
        if not invite:
            return jsonify(status=404, message='Invite code not found'), 404
            
        if not invite.is_valid():
            return jsonify(status=400, message='Invite code is invalid or expired'), 400
            
        data = request.get_json()
        used_by_id = data.get('used_by_id')
        
        invite.used_count += 1
        invite.used_at = datetime.utcnow()
        if used_by_id:
            invite.used_by = used_by_id
            
        if invite.max_uses and invite.used_count >= invite.max_uses:
            invite.is_active = False
            
        db.session.commit()
        
        return jsonify(
            status=200,
            message='Invite code used successfully',
            data=invite.to_dict()
        ), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message=str(e)), 500
