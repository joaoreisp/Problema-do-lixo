from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Usuario  
from config import Config  
app = Flask(__name__, static_folder='app/static', template_folder='app/templates')


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id 
            return redirect(url_for('dashboard')) 
        else:
            flash('E-mail ou senha incorretos', 'danger')  #
            return redirect(url_for('login'))

    return render_template('login.html')
if __name__ == '__main__':
    with app.app_context():  
        db.create_all() 
    app.run(debug=True)
