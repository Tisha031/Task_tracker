from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.task import Task
from ..models.user import User
from ..models.category import Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('tasks', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    identity = get_jwt_identity()
    user_id = identity['id']
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    category_id = data.get('category_id')
    if not title:
        return jsonify({'msg': 'title required'}), 400
    t = Task(title=title, description=description, user_id=user_id)
    if due_date:
        t.due_date = datetime.fromisoformat(due_date)
    if category_id:
        t.category_id = category_id
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id, 'title': t.title}), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def list_tasks():
    identity = get_jwt_identity()
    user_id = identity['id']
    if identity.get('role') == 'admin':
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    out = []
    for t in tasks:
        out.append({
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'category': t.category.name if t.category else None,
            'user_id': t.user_id
        })
    return jsonify(out)

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    identity = get_jwt_identity()
    user_id = identity['id']
    t = Task.query.get_or_404(id)
    if t.user_id != user_id and identity.get('role') != 'admin':
        return jsonify({'msg': 'not allowed'}), 403
    data = request.get_json() or {}
    # only allow status change before due date
    if 'status' in data:
        if t.due_date and datetime.utcnow() > t.due_date:
            return jsonify({'msg': 'cannot change status after due date'}), 400
        t.status = data['status']
    if 'title' in data:
        t.title = data['title']
    if 'description' in data:
        t.description = data['description']
    if 'due_date' in data:
        t.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
    if 'category_id' in data:
        t.category_id = data['category_id']
    db.session.commit()
    return jsonify({'msg': 'updated'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    identity = get_jwt_identity()
    user_id = identity['id']
    t = Task.query.get_or_404(id)
    if t.user_id != user_id and identity.get('role') != 'admin':
        return jsonify({'msg': 'not allowed'}), 403
    db.session.delete(t)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
