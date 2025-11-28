from flask import Blueprint, request, jsonify  
from flask_jwt_extended import create_access_token
from database import db
from models.user import User

users_bp = Blueprint('users', __name__)

# Rota para registrar um novo usuário
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios!"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "O usuário já existe"}), 400

    user = User(username = username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"Mensagem": "Usuário registrado com sucesso"}), 201
# Rota para login do usuário
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    usuario = User.query.filter_by(username=username).first()
    if not usuario or not usuario.check_password(password):
        return jsonify({'error': 'Credenciais inválidas'}), 401
# Gerar o token JWT e devolve para o user
    token = create_access_token(identity=str(usuario.id))
    return jsonify({'token': token}), 200