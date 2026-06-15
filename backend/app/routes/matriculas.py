from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.matricula import Matricula
from app.models.projeto import Projeto
from app.models.usuario import Usuario

matriculas_bp = Blueprint('matriculas', __name__)

@matriculas_bp.route('/matriculas', methods=['POST'])
@jwt_required()
def criar_matricula():
    """
    Matricular estudante em projeto
    ---
    tags:
      - Matrículas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - projeto_id
          properties:
            projeto_id:
              type: integer
              example: 1
    responses:
      201:
        description: Matrícula realizada com sucesso
      400:
        description: Estudante já matriculada neste projeto
      403:
        description: Apenas estudante pode se matricular
      404:
        description: Projeto não encontrado
    """
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if usuario.perfil != 'estudante':
        return jsonify({'erro': 'Apenas estudante pode se matricular em projetos'}), 403

    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    projeto_id = dados.get('projeto_id')

    if not projeto_id:
        return jsonify({'erro': 'projeto_id é obrigatório'}), 400

    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    if projeto.status != 'publicado':
        return jsonify({'erro': 'Não é possível se matricular em projeto não publicado'}), 400

    matricula_existente = Matricula.query.filter_by(
        estudante_id=usuario_id,
        projeto_id=projeto_id
    ).first()

    if matricula_existente:
        return jsonify({'erro': 'Estudante já matriculada neste projeto'}), 400

    matricula = Matricula(
        estudante_id=usuario_id,
        projeto_id=projeto_id
    )
    db.session.add(matricula)
    db.session.commit()

    return jsonify({
        'mensagem': 'Matrícula realizada com sucesso',
        'matricula': matricula.to_dict()
    }), 201


@matriculas_bp.route('/matriculas', methods=['GET'])
@jwt_required()
def listar_matriculas():
    """
    Listar matrículas da estudante logada
    ---
    tags:
      - Matrículas
    responses:
      200:
        description: Lista de matrículas
      403:
        description: Apenas estudante pode listar suas matrículas
    """
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if usuario.perfil != 'estudante':
        return jsonify({'erro': 'Apenas estudante pode listar matrículas'}), 403

    matriculas = Matricula.query.filter_by(estudante_id=usuario_id).all()

    return jsonify([m.to_dict() for m in matriculas]), 200


@matriculas_bp.route('/matriculas/<int:matricula_id>', methods=['DELETE'])
@jwt_required()
def cancelar_matricula(matricula_id):
    """
    Cancelar matrícula
    ---
    tags:
      - Matrículas
    parameters:
      - in: path
        name: matricula_id
        type: integer
        required: true
    responses:
      200:
        description: Matrícula cancelada com sucesso
      403:
        description: Sem permissão para cancelar esta matrícula
      404:
        description: Matrícula não encontrada
    """
    usuario_id = get_jwt_identity()
    matricula = Matricula.query.get(matricula_id)

    if not matricula:
        return jsonify({'erro': 'Matrícula não encontrada'}), 404

    if str(matricula.estudante_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para cancelar esta matrícula'}), 403

    db.session.delete(matricula)
    db.session.commit()

    return jsonify({'mensagem': 'Matrícula cancelada com sucesso'}), 200