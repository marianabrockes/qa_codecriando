from app import db
from datetime import datetime, timezone

class Projeto(db.Model):
    __tablename__ = 'projetos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.String(20), nullable=False)  # 'iniciante', 'intermediario', 'avancado'
    status = db.Column(db.String(20), default='rascunho')  # 'rascunho' ou 'publicado'
    professor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    etapas = db.relationship('Etapa', backref='projeto', lazy=True, cascade='all, delete-orphan')
    matriculas = db.relationship('Matricula', backref='projeto', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'nivel': self.nivel,
            'status': self.status,
            'professor_id': self.professor_id,
            'criado_em': self.criado_em.isoformat(timespec='seconds'),
            'total_etapas': len(self.etapas)
        }