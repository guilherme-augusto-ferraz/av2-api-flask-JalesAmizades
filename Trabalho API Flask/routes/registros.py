from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.registro import Registro

registros_bp = Blueprint('registros', __name__)

# Criar um novo registro com o local e sua respectiva senha
@registros_bp.route('/create', methods=['POST'])
@jwt_required()
def create_registro():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    local = data.get('local')
    senha = data.get('senha', '')

    if not local:
        return jsonify({'error': 'Local é obrigatório para registrar a senha.'}), 400

    registro = Registro(local=local, senha=senha, user_id=user_id)
    db.session.add(registro)
    db.session.commit()

    return jsonify({'message': 'Senha registrada com sucesso', 'id': registro.id}), 201


# Lista os locais e senhas do usuário logado
@registros_bp.route('/', methods=['GET'])
@jwt_required()
def list_registros():
    user_id = get_jwt_identity()
    register = Registro.query.filter_by(user_id=user_id).all()
    result = [
        {
            'Id': r.id,
            'Local da senha': r.local,
            'Senha': r.senha,
            'Observação': r.obs,
            'Data': r.data.isoformat()
        } for r in register
    ]
    return jsonify(result), 200


# Atualizar o registro de um local e sua senha
@registros_bp.route('/<int:registro_id>', methods=['PUT'])
@jwt_required()
def update_registro(registro_id):
    user_id = get_jwt_identity()
    registro = Registro.query.filter_by(id=registro_id, user_id=user_id).first()

    if not registro:
        return jsonify({'error': 'Registro não encontrado'}), 404

    data = request.get_json()
    registro.local = data.get('Local', registro.titulo)
    registro.senha = data.get('Senha', registro.descricao)
    registro.obs = data.get('Observação', registro.concluida)

    db.session.commit()
    return jsonify({'message': 'Registro atualizado com sucesso'}), 200


# Deletar um registro pelo ID
@registros_bp.route('/<int:registro_id>', methods=['DELETE'])
@jwt_required()
def delete_registro(registro_id):
    user_id = get_jwt_identity()
    registro = Registro.query.filter_by(id=registro_id, user_id=user_id).first()

    if not registro:
        return jsonify({'error': 'Registro não encontrado'}), 404

    db.session.delete(registro)
    db.session.commit()
    return jsonify({'message': 'Registro excluído com sucesso'}), 200