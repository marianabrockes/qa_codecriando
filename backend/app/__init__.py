import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('codecriando')


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    Swagger(app)

    # Handlers de erro JWT
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        logger.warning('Requisição sem token: %s %s', request.method, request.path)
        return jsonify({'erro': 'Token de acesso ausente'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.warning('Token inválido: %s %s', request.method, request.path)
        return jsonify({'erro': 'Token de acesso inválido'}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        logger.warning('Token expirado: %s %s', request.method, request.path)
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

    # Log de todas as requisições
    @app.after_request
    def log_request(response):
        if response.status_code >= 400:
            logger.warning(
                '%s %s -> %s',
                request.method,
                request.path,
                response.status_code
            )
        else:
            logger.info(
                '%s %s -> %s',
                request.method,
                request.path,
                response.status_code
            )
        return response

    return app