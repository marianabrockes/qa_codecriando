from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Cadastrar nova pessoa usuária
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - email
            - senha
            - perfil
          properties:
            nome:
              type: string
              example: Lua Silva
            email:
              type: string
              example: lua@email.com
            senha:
              type: string
              example: "123456"
            perfil:
              type: string
              example: estudante
    responses:
      201:
        description: Pessoa usuária cadastrada com sucesso
      400:
        description: Dados inválidos ou email já cadastrado
    """
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    perfil = dados.get('perfil')

    if not all([nome, email, senha, perfil]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    if perfil not in ['professor', 'estudante']:
        return jsonify({'erro': 'Perfil deve ser professor ou estudante'}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400

    senha_hash = generate_password_hash(senha)

    usuario = Usuario(nome=nome, email=email, senha=senha_hash, perfil=perfil)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({
        'mensagem': 'Pessoa usuária cadastrada com sucesso',
        'usuario': usuario.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autenticar pessoa usuária
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
              example: lua@email.com
            senha:
              type: string
              example: "123456"
    responses:
      200:
        description: Login realizado com sucesso
      401:
        description: Credenciais inválidas
    """
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    email = dados.get('email')
    senha = dados.get('senha')

    if not all([email, senha]):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha, senha):
        return jsonify({'erro': 'Email ou senha incorretos'}), 401

    token = create_access_token(identity=str(usuario.id))

    return jsonify({
        'token': token,
        'usuario': usuario.to_dict()
    }), 200