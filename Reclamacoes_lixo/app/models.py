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
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento com a tabela 'reclamacoes'
    reclamacoes = db.relationship('Reclamacao', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome} {self.sobrenome}>'

class Reclamacao(db.Model):
    __tablename__ = 'reclamacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_reclamacao_id = db.Column(db.Integer, db.ForeignKey('tipos_de_reclamacao.id'), nullable=False)  # Nome correto da tabela referenciada
    tipo_reclamacao = db.relationship('tipo_de_reclamacoes', backref='reclamacoes')  # Ajustado para o nome correto da tabela
    descricao = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    anexo = db.Column(db.String(255))
    data_criacao = db.Column(db.TIMESTAMP, default=datetime.utcnow)  # Coluna existente
    data_atualizacao = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # Coluna existente

    def __repr__(self):
        return f'<Reclamacao {self.descricao[:30]}...>'

class tipo_de_reclamacoes(db.Model):
    __tablename__ = 'tipos_de_reclamacao'  # O nome da tabela precisa ser consistente com a ForeignKey
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Tipo de Reclamação {self.tipo[:30]}...>'  # Corrigido para `self.tipo`
