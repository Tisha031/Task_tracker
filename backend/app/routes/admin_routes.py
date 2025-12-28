from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('admin', __name__)

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def admin_list_tasks():
    identity = get_jwt_identity()
    if identity.get('role') != 'admin':
        return jsonify({'msg': 'admin only'}), 403
    # filters: user_id, status
    q = Task.query
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    if user_id:
        q = q.filter_by(user_id=user_id)
    if status:
        q = q.filter_by(status=status)
    tasks = q.order_by(Task.created_at.desc()).all()
    out = []
    for t in tasks:
        out.append({
            'id': t.id,
            'title': t.title,
            'status': t.status,
            'user_id': t.user_id,
            'due_date': t.due_date.isoformat() if t.due_date else None
        })
    return jsonify(out)
