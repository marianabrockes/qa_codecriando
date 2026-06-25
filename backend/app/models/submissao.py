from app import db
from datetime import datetime, timezone

class Submissao(db.Model):
    __tablename__ = 'submissoes'

    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    etapa_id = db.Column(db.Integer, db.ForeignKey('etapas.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # 'pendente', 'aprovado', 'reprovado'
    feedback = db.Column(db.Text, nullable=True)
    enviado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    avaliado_em = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'matricula_id': self.matricula_id,
            'etapa_id': self.etapa_id,
            'conteudo': self.conteudo,
            'status': self.status,
            'feedback': self.feedback,
            'enviado_em': self.enviado_em.isoformat(timespec='seconds'),
            'avaliado_em': self.avaliado_em.isoformat(timespec='seconds') if self.avaliado_em else None
        }