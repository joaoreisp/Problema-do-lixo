import os
from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from app.models import db, Usuario
from config import Config

# Importa os blueprints
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.reclamacao_routes import UPLOAD_FOLDER, reclamacao_bp
from app.routes.grafico_routes import grafico_bp

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    
    # Inicializa extensões
    db.init_app(app)
    csrf = CSRFProtect(app)
    app.secret_key = app.config['SECRET_KEY'] 
    csrf.init_app(app)
    app.debug = True

    # Configurações do app
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads
    app.config.from_object(Config)

    # Registra blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reclamacao_bp)
    app.register_blueprint(grafico_bp)
    
    @app.before_request
    def add_user_to_globals():
        if 'usuario_id' in session:
            usuario = db.session.get(Usuario, session['usuario_id'])
            if usuario:
                session['usuario_nome'] = usuario.nome
                session['usuario_sobrenome'] = usuario.sobrenome
                session['usuario_profissao'] = usuario.profissao
                session['usuario_cidade'] = usuario.cidade
                session['nickname'] = f"{usuario.nome[0]}{usuario.sobrenome[0]}"

    return app
import os
from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from app.models import db, Usuario
from config import Config

# Importa os blueprints
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.reclamacao_routes import UPLOAD_FOLDER, reclamacao_bp
from app.routes.grafico_routes import grafico_bp

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    
    # Inicializa extensões
    db.init_app(app)
    csrf = CSRFProtect(app)
    app.secret_key = app.config['SECRET_KEY'] 
    csrf.init_app(app)
    app.debug = True

    # Configurações do app
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads
    app.config.from_object(Config)

    # Registra blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reclamacao_bp)
    app.register_blueprint(grafico_bp)
    
    @app.before_request
    def add_user_to_globals():
        if 'usuario_id' in session:
            usuario = db.session.get(Usuario, session['usuario_id'])
            if usuario:
                session['usuario_nome'] = usuario.nome
                session['usuario_sobrenome'] = usuario.sobrenome
                session['usuario_profissao'] = usuario.profissao
                session['usuario_cidade'] = usuario.cidade
                session['nickname'] = f"{usuario.nome[0]}{usuario.sobrenome[0]}"

    return app
