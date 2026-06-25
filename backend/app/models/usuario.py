from app import db
from datetime import datetime, timezone

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  # 'professor' ou 'estudante'
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    projetos = db.relationship('Projeto', backref='professor', lazy=True)
    matriculas = db.relationship('Matricula', backref='estudante', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'perfil': self.perfil,
            'criado_em': self.criado_em.isoformat(timespec='seconds')
        }