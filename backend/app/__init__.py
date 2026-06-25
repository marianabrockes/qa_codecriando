from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config.from_object('app.config.Config')

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    Swagger(app)

    # Handlers de erro JWT
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({'erro': 'Token de acesso ausente'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'erro': 'Token de acesso inválido'}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({'erro': 'Token de acesso expirado'}), 401

    # Registra rotas
    from app.routes.auth import auth_bp
    from app.routes.projetos import projetos_bp
    from app.routes.etapas import etapas_bp
    from app.routes.matriculas import matriculas_bp
    from app.routes.submissoes import submissoes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(projetos_bp)
    app.register_blueprint(etapas_bp)
    app.register_blueprint(matriculas_bp)
    app.register_blueprint(submissoes_bp)

    return app