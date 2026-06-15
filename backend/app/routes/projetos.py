from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.projeto import Projeto
from app.models.usuario import Usuario
from app.models.matricula import Matricula

projetos_bp = Blueprint('projetos', __name__)

@projetos_bp.route('/projetos', methods=['POST'])
@jwt_required()
def criar_projeto():
    """
    Criar novo projeto
    ---
    tags:
      - Projetos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - titulo
            - descricao
            - nivel
          properties:
            titulo:
              type: string
              example: Minha primeira página web
            descricao:
              type: string
              example: Aprenda a criar uma página HTML do zero
            nivel:
              type: string
              example: iniciante
    responses:
      201:
        description: Projeto criado com sucesso
      400:
        description: Dados inválidos
      403:
        description: Apenas professor(a) pode criar projetos
    """
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if usuario.perfil != 'professor':
        return jsonify({'erro': 'Apenas professor(a) pode criar projetos'}), 403

    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    nivel = dados.get('nivel')

    if not all([titulo, descricao, nivel]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    if nivel not in ['iniciante', 'intermediario', 'avancado']:
        return jsonify({'erro': 'Nível deve ser iniciante, intermediario ou avancado'}), 400

    projeto = Projeto(
        titulo=titulo,
        descricao=descricao,
        nivel=nivel,
        professor_id=usuario_id
    )
    db.session.add(projeto)
    db.session.commit()

    return jsonify({
        'mensagem': 'Projeto criado com sucesso',
        'projeto': projeto.to_dict()
    }), 201


@projetos_bp.route('/projetos', methods=['GET'])
@jwt_required()
def listar_projetos():
    """
    Listar projetos publicados
    ---
    tags:
      - Projetos
    responses:
      200:
        description: Lista de projetos publicados
    """
    projetos = Projeto.query.filter_by(status='publicado').all()
    return jsonify([p.to_dict() for p in projetos]), 200


@projetos_bp.route('/projetos/<int:projeto_id>', methods=['GET'])
@jwt_required()
def detalhar_projeto(projeto_id):
    """
    Detalhar projeto com etapas
    ---
    tags:
      - Projetos
    parameters:
      - in: path
        name: projeto_id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do projeto
      404:
        description: Projeto não encontrado
    """
    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    projeto_dict = projeto.to_dict()
    projeto_dict['etapas'] = [e.to_dict() for e in projeto.etapas]

    return jsonify(projeto_dict), 200


@projetos_bp.route('/projetos/<int:projeto_id>', methods=['PUT'])
@jwt_required()
def editar_projeto(projeto_id):
    """
    Editar projeto
    ---
    tags:
      - Projetos
    parameters:
      - in: path
        name: projeto_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
            descricao:
              type: string
            nivel:
              type: string
    responses:
      200:
        description: Projeto atualizado com sucesso
      403:
        description: Sem permissão para editar este projeto
      404:
        description: Projeto não encontrado
    """
    usuario_id = get_jwt_identity()
    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    if str(projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para editar este projeto'}), 403

    if projeto.status == 'publicado':
        return jsonify({'erro': 'Não é possível editar projeto já publicado'}), 400

    dados = request.get_json()

    if dados.get('titulo'):
        projeto.titulo = dados.get('titulo')
    if dados.get('descricao'):
        projeto.descricao = dados.get('descricao')
    if dados.get('nivel'):
        projeto.nivel = dados.get('nivel')

    db.session.commit()

    return jsonify({
        'mensagem': 'Projeto atualizado com sucesso',
        'projeto': projeto.to_dict()
    }), 200


@projetos_bp.route('/projetos/<int:projeto_id>', methods=['DELETE'])
@jwt_required()
def deletar_projeto(projeto_id):
    """
    Deletar projeto
    ---
    tags:
      - Projetos
    parameters:
      - in: path
        name: projeto_id
        type: integer
        required: true
    responses:
      200:
        description: Projeto deletado com sucesso
      400:
        description: Projeto com matrículas ativas não pode ser deletado
      403:
        description: Sem permissão para deletar este projeto
      404:
        description: Projeto não encontrado
    """
    usuario_id = get_jwt_identity()
    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    if str(projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para deletar este projeto'}), 403

    if projeto.matriculas:
        return jsonify({'erro': 'Não é possível deletar projeto com matrículas ativas'}), 400

    db.session.delete(projeto)
    db.session.commit()

    return jsonify({'mensagem': 'Projeto deletado com sucesso'}), 200


@projetos_bp.route('/projetos/<int:projeto_id>/publicar', methods=['PATCH'])
@jwt_required()
def publicar_projeto(projeto_id):
    """
    Publicar projeto
    ---
    tags:
      - Projetos
    parameters:
      - in: path
        name: projeto_id
        type: integer
        required: true
    responses:
      200:
        description: Projeto publicado com sucesso
      400:
        description: Projeto sem etapas não pode ser publicado
      403:
        description: Sem permissão para publicar este projeto
      404:
        description: Projeto não encontrado
    """
    usuario_id = get_jwt_identity()
    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    if str(projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para publicar este projeto'}), 403

    if not projeto.etapas:
        return jsonify({'erro': 'Não é possível publicar projeto sem etapas'}), 400

    if projeto.status == 'publicado':
        return jsonify({'erro': 'Projeto já está publicado'}), 400

    projeto.status = 'publicado'
    db.session.commit()

    return jsonify({
        'mensagem': 'Projeto publicado com sucesso',
        'projeto': projeto.to_dict()
    }), 200