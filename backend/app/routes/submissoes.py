from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models.submissao import Submissao
from app.models.matricula import Matricula
from app.models.etapa import Etapa
from app.models.projeto import Projeto
from app.models.usuario import Usuario

submissoes_bp = Blueprint('submissoes', __name__)

@submissoes_bp.route('/submissoes', methods=['POST'])
@jwt_required()
def criar_submissao():
    """
    Submeter etapa de um projeto
    ---
    tags:
      - Submissões
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - matricula_id
            - etapa_id
            - conteudo
          properties:
            matricula_id:
              type: integer
              example: 1
            etapa_id:
              type: integer
              example: 1
            conteudo:
              type: string
              example: "Minha solução para a etapa"
    responses:
      201:
        description: Submissão realizada com sucesso
      400:
        description: Etapa anterior não aprovada ou dados inválidos
      403:
        description: Sem permissão para submeter esta etapa
      404:
        description: Matrícula ou etapa não encontrada
    """
    usuario_id = get_jwt_identity()
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    matricula_id = dados.get('matricula_id')
    etapa_id = dados.get('etapa_id')
    conteudo = dados.get('conteudo')

    if not all([matricula_id, etapa_id, conteudo]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    matricula = Matricula.query.get(matricula_id)

    if not matricula:
        return jsonify({'erro': 'Matrícula não encontrada'}), 404

    if str(matricula.estudante_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para submeter nesta matrícula'}), 403

    etapa = Etapa.query.get(etapa_id)

    if not etapa:
        return jsonify({'erro': 'Etapa não encontrada'}), 404

    if etapa.projeto_id != matricula.projeto_id:
        return jsonify({'erro': 'Etapa não pertence ao projeto desta matrícula'}), 400

    if etapa.ordem > 1:
        etapa_anterior = Etapa.query.filter_by(
            projeto_id=etapa.projeto_id,
            ordem=etapa.ordem - 1
        ).first()

        if etapa_anterior:
            submissao_anterior = Submissao.query.filter_by(
                matricula_id=matricula_id,
                etapa_id=etapa_anterior.id
            ).first()

            if not submissao_anterior or submissao_anterior.status != 'aprovado':
                return jsonify({'erro': 'A etapa anterior precisa ser aprovada antes de continuar'}), 400

    submissao = Submissao(
        matricula_id=matricula_id,
        etapa_id=etapa_id,
        conteudo=conteudo
    )
    db.session.add(submissao)
    db.session.commit()

    return jsonify({
        'mensagem': 'Submissão realizada com sucesso',
        'submissao': submissao.to_dict()
    }), 201


@submissoes_bp.route('/submissoes/<int:submissao_id>', methods=['GET'])
@jwt_required()
def detalhar_submissao(submissao_id):
    """
    Detalhar submissão
    ---
    tags:
      - Submissões
    parameters:
      - in: path
        name: submissao_id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da submissão
      403:
        description: Sem permissão para ver esta submissão
      404:
        description: Submissão não encontrada
    """
    usuario_id = get_jwt_identity()
    submissao = Submissao.query.get(submissao_id)

    if not submissao:
        return jsonify({'erro': 'Submissão não encontrada'}), 404

    matricula = Matricula.query.get(submissao.matricula_id)
    projeto = Projeto.query.get(matricula.projeto_id)

    eh_estudante_dona = str(matricula.estudante_id) == str(usuario_id)
    eh_professor_dono = str(projeto.professor_id) == str(usuario_id)

    if not eh_estudante_dona and not eh_professor_dono:
        return jsonify({'erro': 'Sem permissão para ver esta submissão'}), 403

    return jsonify(submissao.to_dict()), 200


@submissoes_bp.route('/submissoes/<int:submissao_id>/avaliar', methods=['PATCH'])
@jwt_required()
def avaliar_submissao(submissao_id):
    """
    Avaliar submissão
    ---
    tags:
      - Submissões
    parameters:
      - in: path
        name: submissao_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              example: aprovado
            feedback:
              type: string
              example: Muito bem! Solução correta.
    responses:
      200:
        description: Submissão avaliada com sucesso
      400:
        description: Status inválido
      403:
        description: Sem permissão para avaliar esta submissão
      404:
        description: Submissão não encontrada
    """
    usuario_id = get_jwt_identity()
    submissao = Submissao.query.get(submissao_id)

    if not submissao:
        return jsonify({'erro': 'Submissão não encontrada'}), 404

    matricula = Matricula.query.get(submissao.matricula_id)
    projeto = Projeto.query.get(matricula.projeto_id)

    if str(projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para avaliar esta submissão'}), 403

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    status = dados.get('status')

    if status not in ['aprovado', 'reprovado']:
        return jsonify({'erro': 'Status deve ser aprovado ou reprovado'}), 400

    submissao.status = status
    submissao.feedback = dados.get('feedback')
    submissao.avaliado_em = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify({
        'mensagem': 'Submissão avaliada com sucesso',
        'submissao': submissao.to_dict()
    }), 200


@submissoes_bp.route('/projetos/<int:projeto_id>/submissoes', methods=['GET'])
@jwt_required()
def listar_submissoes_projeto(projeto_id):
    """
    Listar submissões de um projeto
    ---
    tags:
      - Submissões
    parameters:
      - in: path
        name: projeto_id
        type: integer
        required: true
    responses:
      200:
        description: Lista de submissões do projeto
      403:
        description: Sem permissão para ver as submissões deste projeto
      404:
        description: Projeto não encontrado
    """
    usuario_id = get_jwt_identity()
    projeto = Projeto.query.get(projeto_id)

    if not projeto:
        return jsonify({'erro': 'Projeto não encontrado'}), 404

    if str(projeto.professor_id) != str(usuario_id):
        return jsonify({'erro': 'Sem permissão para ver as submissões deste projeto'}), 403

    matriculas = Matricula.query.filter_by(projeto_id=projeto_id).all()

    resultado = []
    for matricula in matriculas:
        submissoes = Submissao.query.filter_by(matricula_id=matricula.id).all()
        for submissao in submissoes:
            resultado.append(submissao.to_dict())

    return jsonify(resultado), 200