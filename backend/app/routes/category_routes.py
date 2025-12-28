from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.category import Category
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('categories', __name__)

def admin_required():
    identity = get_jwt_identity()
    return identity and identity.get('role') == 'admin'

@bp.route('/', methods=['GET'])
@jwt_required()
def list_categories():
    cats = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in cats])

@bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    if not admin_required():
        return jsonify({'msg': 'admin only'}), 403
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'name required'}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({'msg': 'already exists'}), 400
    c = Category(name=name)
    db.session.add(c)
    db.session.commit()
    return jsonify({'id': c.id, 'name': c.name}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    if not admin_required():
        return jsonify({'msg': 'admin only'}), 403
    c = Category.query.get_or_404(id)
    data = request.get_json() or {}
    name = data.get('name')
    if name:
        c.name = name
        db.session.commit()
    return jsonify({'id': c.id, 'name': c.name})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    if not admin_required():
        return jsonify({'msg': 'admin only'}), 403
    c = Category.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
