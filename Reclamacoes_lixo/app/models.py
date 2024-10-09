from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Modelo para a tabela 'usuarios'
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    uf = db.Column(db.String(2), nullable=False)  # Certifique-se de que este campo existe no formulário
    bairro = db.Column(db.String(255), nullable=False)
    profissao = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)  # Aumente o tamanho para senhas hash

    # Relacionamento com a tabela 'reclamacoes'
    reclamacoes = db.relationship('Reclamacao', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome} {self.sobrenome}>'

# Modelo para a tabela 'reclamacoes'
class Reclamacao(db.Model):
    __tablename__ = 'reclamacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    anexo = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Reclamacao {self.descricao[:30]}...>'
