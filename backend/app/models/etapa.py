from app import db
from datetime import datetime, timezone

class Etapa(db.Model):
    __tablename__ = 'etapas'

    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    instrucao = db.Column(db.Text, nullable=False)
    ordem = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    submissoes = db.relationship('Submissao', backref='etapa', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'projeto_id': self.projeto_id,
            'titulo': self.titulo,
            'instrucao': self.instrucao,
            'ordem': self.ordem,
            'criado_em': self.criado_em.isoformat()
        }