from flask import Flask
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