from datetime import datetime
import os
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.models import db, Usuario, Reclamacao, tipo_de_reclamacoes
from config import Config  
app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

# Defina o diretório onde as imagens serão armazenadas
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config.from_object(Config)


app.secret_key = app.config['SECRET_KEY'] 
csrf = CSRFProtect(app)


db.init_app(app)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        cidade = request.form['cidade']
        uf = request.form['uf']
        bairro = request.form['bairro']
        profissao = request.form['profissao']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar-senha']
        
     
        if senha != confirmar_senha:
            return "Senhas não coincidem", 400
        
       
        if Usuario.query.filter_by(email=email).first():
            return "E-mail já cadastrado", 400
        
       
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome,
            sobrenome=sobrenome,
            cidade=cidade,
            uf=uf,
            bairro=bairro,
            profissao=profissao,
            email=email,
            senha=senha_hash
        )
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            print(f"Usuário {nome} adicionado com sucesso!")  
            return '', 204  
        except Exception as e:
            db.session.rollback()  
            print(f"Erro ao salvar os dados: {str(e)}")  
            return "Houve um erro ao salvar os dados", 500
    
    return render_template('cadastro.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id 
            return render_template('index.html')
        else:
            flash('E-mail ou senha incorretos', 'danger')  #
            return redirect(url_for('login'))

    return render_template('login.html')
       
       
@app.route('/index', methods=['GET', 'POST'])
def criar_reclamacao():
    if request.method == 'POST':
        # Outros dados do formulário
        descricao = request.form['descricao']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        usuario_id = session['usuario_id']

        # Verifica se um arquivo foi anexado
        if 'anexo' not in request.files:
            flash('Nenhum arquivo anexado', 'danger')
            return redirect(request.url)

        file = request.files['anexo']

        if file.filename == '':
            flash('Nenhuma imagem selecionada', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)  # Salva a imagem no diretório

            # Cria a reclamação no banco de dados, armazenando o caminho da imagem
            nova_reclamacao = Reclamacao(
                usuario_id=usuario_id,
                descricao=descricao,
                cidade=cidade,
                bairro=bairro,
                anexo=filename,  # Armazena o nome do arquivo no banco
                data=datetime.now()
            )
            db.session.add(nova_reclamacao)
            db.session.commit()

            flash('Reclamação criada com sucesso!', 'success')
            return redirect(url_for('listar_reclamacoes'))
    usuarios = Usuario.query.all()
    print(usuarios)
    return render_template('index.html', usuarios=usuarios)
       
@app.route('/reclamacoes', methods=['GET'])
def listar_reclamacoes():
    try:
        usuarios = Usuario.query.all()  # Consulta todos os usuários
        reclamacoes = Reclamacao.query.all()
        tipo_de_reclamacao = tipo_de_reclamacoes.query.all()
        # Garantir que 'anexo' é tratado como string (ou nulo) em cada reclamação
        for reclamacao in reclamacoes:
            
            print(reclamacao.data_criacao)  # Acessa o atributo 'data_criacao'
            reclamacao.anexo = str(reclamacao.anexo) if reclamacao.anexo else None
        return render_template('reclamacoes.html', usuarios=usuarios, reclamacoes=reclamacoes, tipo_de_reclamacao=tipo_de_reclamacao)  # Passa os dados para o template
    except Exception as e:
        print(f"Erro ao buscar os dados: {str(e)}")
        return "Houve um erro ao buscar os dados", 500





if __name__ == '__main__':
    with app.app_context():  
        db.create_all() 
    app.run(debug=True)
