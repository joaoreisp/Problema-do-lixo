from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Modelo para a tabela 'usuarios'
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    profissao = db.Column(db.String(255))
    administrador =db.Column(db.Boolean, default= False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Relacionamento com Reclamacao usando back_populates
    reclamacoes = db.relationship("Reclamacao", back_populates="usuario")

    def __repr__(self):
        return f'<Usuario {self.nome} {self.sobrenome}>'


# Modelo para a tabela 'reclamacoes'
class Reclamacao(db.Model):
    __tablename__ = 'reclamacoes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    tipo_reclamacao = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    anonimo = db.Column(db.Boolean, default=False)
    estado =db.Column(db.Boolean, default= False)
    cidade = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    anexo = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pendente')
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    data_atualizacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamento com Usuario usando back_populates
    usuario = db.relationship("Usuario", back_populates="reclamacoes")
    resolucoes = db.relationship('Resolucao', back_populates='reclamacao', cascade='all, delete-orphan')
    def __repr__(self):
        return f'<Reclamacao {self.descricao[:30]}...>'
    
class Resolucao(db.Model):
    __tablename__ = 'resolucoes'

    id = db.Column(db.Integer, primary_key=True)
    reclamacao_id = db.Column(db.Integer, db.ForeignKey('reclamacoes.id'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    responsavel = db.Column(db.String(255), nullable=False)
    data_resolucao = db.Column(db.DateTime, default=datetime.utcnow)
    reclamacao = db.relationship('Reclamacao', back_populates='resolucoes')


