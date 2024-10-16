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
    uf = db.Column(db.String(2), nullable=False)  # UF (Estado)
    bairro = db.Column(db.String(255), nullable=False)
    profissao = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)  # Senha hash
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento com a tabela 'reclamacoes'
    reclamacoes = db.relationship('Reclamacao', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome} {self.sobrenome}>'


# Modelo para a tabela 'reclamacoes'
class Reclamacao(db.Model):
    __tablename__ = 'reclamacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_reclamacao_id = db.Column(db.Integer, db.ForeignKey('tipos_de_reclamacao.id'), nullable=False)
    
    # Relacionamento com TipoDeReclamacao
    tipo_reclamacao = db.relationship('TipoDeReclamacao', backref='reclamacoes', lazy=True)
    
    descricao = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    anexo = db.Column(db.String(255))  # Caminho do anexo
    data_criacao = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    data_atualizacao = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Reclamacao {self.descricao[:30]}...>'

# Modelo para a tabela 'tipos_de_reclamacao'
class TipoDeReclamacao(db.Model):
    __tablename__ = 'tipos_de_reclamacao'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<TipoDeReclamacao {self.tipo}>'
