from flask import Blueprint, request, jsonify, current_app
from ..extensions import db
from ..models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'email already registered'}), 400
    user = User(name=name, email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'registered'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'bad credentials'}), 401
    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    resp = jsonify({'msg': 'login successful', 'user': {'id': user.id, 'email': user.email, 'role': user.role}})
    # set HttpOnly cookie
    set_access_cookies(resp, access_token)
    return resp

@bp.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'msg': 'logout successful'})
    unset_jwt_cookies(resp)
    return resp

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = User.query.get(identity['id'])
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})
