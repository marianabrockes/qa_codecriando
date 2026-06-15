from app import db
from datetime import datetime, timezone

class Matricula(db.Model):
    __tablename__ = 'matriculas'

    id = db.Column(db.Integer, primary_key=True)
    estudante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    matriculado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    submissoes = db.relationship('Submissao', backref='matricula', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'estudante_id': self.estudante_id,
            'projeto_id': self.projeto_id,
            'matriculado_em': self.matriculado_em.isoformat()
        }