from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.etapa import Etapa
from app.models.projeto import Projeto

etapas_bp = Blueprint('etapas', __name__)

@etapas_bp.route('/projetos/<int:projeto_id>/etapas', methods=['POST'])
@jwt_required()
def criar_etapa(projeto_id):
    """
    Criar etapa em um projeto
    ---
    tags:
      - Etapas
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
          required:
            - titulo
            - instrucao
            - ordem
          properties:
            titulo:
              type: string
              example: Crie sua primeira tag HTML
            instrucao:
              type: string
              example: Use a tag h1 para escrever um título
            ordem:
              type: integer
              example: 1
    responses:
      201:
        description: Etapa criada com sucesso
      400:
        description: Dados inválidos
      403:
        description: Sem permissão para adicionar etapas neste projeto
      404:
        description: Projeto não encontrado
    """
    usuario_id = get_jwt_identity()
    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    if str(projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para adicionar etapas neste projeto'}), 403

    if projeto.status == 'publicado':
        return jsonify({'erro': 'Não é possível adicionar etapas em projeto já publicado'}), 400

    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    titulo = dados.get('titulo')
    instrucao = dados.get('instrucao')
    ordem = dados.get('ordem')

    if not all([titulo, instrucao, ordem]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    etapa = Etapa(
        projeto_id=projeto_id,
        titulo=titulo,
        instrucao=instrucao,
        ordem=ordem
    )
    db.session.add(etapa)
    db.session.commit()

    return jsonify({
        'mensagem': 'Etapa criada com sucesso',
        'etapa': etapa.to_dict()
    }), 201


@etapas_bp.route('/etapas/<int:etapa_id>', methods=['PUT'])
@jwt_required()
def editar_etapa(etapa_id):
    """
    Editar etapa
    ---
    tags:
      - Etapas
    parameters:
      - in: path
        name: etapa_id
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
            instrucao:
              type: string
            ordem:
              type: integer
    responses:
      200:
        description: Etapa atualizada com sucesso
      400:
        description: Não é possível editar etapa de projeto publicado
      403:
        description: Sem permissão para editar esta etapa
      404:
        description: Etapa não encontrada
    """
    usuario_id = get_jwt_identity()
    etapa = Etapa.query.get(etapa_id)

    if not etapa:
        return jsonify({'erro': 'Etapa não encontrada'}), 404

    if str(etapa.projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para editar esta etapa'}), 403

    if etapa.projeto.status == 'publicado':
        return jsonify({'erro': 'Não é possível editar etapa de projeto já publicado'}), 400

    dados = request.get_json()

    if dados.get('titulo'):
        etapa.titulo = dados.get('titulo')
    if dados.get('instrucao'):
        etapa.instrucao = dados.get('instrucao')
    if dados.get('ordem'):
        etapa.ordem = dados.get('ordem')

    db.session.commit()

    return jsonify({
        'mensagem': 'Etapa atualizada com sucesso',
        'etapa': etapa.to_dict()
    }), 200


@etapas_bp.route('/etapas/<int:etapa_id>', methods=['DELETE'])
@jwt_required()
def deletar_etapa(etapa_id):
    """
    Deletar etapa
    ---
    tags:
      - Etapas
    parameters:
      - in: path
        name: etapa_id
        type: integer
        required: true
    responses:
      200:
        description: Etapa deletada com sucesso
      400:
        description: Não é possível deletar etapa de projeto publicado
      403:
        description: Sem permissão para deletar esta etapa
      404:
        description: Etapa não encontrada
    """
    usuario_id = get_jwt_identity()
    etapa = Etapa.query.get(etapa_id)

    if not etapa:
        return jsonify({'erro': 'Etapa não encontrada'}), 404

    if str(etapa.projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para deletar esta etapa'}), 403

    if etapa.projeto.status == 'publicado':
        return jsonify({'erro': 'Não é possível deletar etapa de projeto já publicado'}), 400

    db.session.delete(etapa)
    db.session.commit()

    return jsonify({'mensagem': 'Etapa deletada com sucesso'}), 200