# app/routes/user_routes.py
from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from app.models import db, Usuario

user_bp = Blueprint('user', __name__)

@user_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form.get('sobrenome', '')  
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        profissao = request.form['profissao']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmSenha']
        
        if senha != confirmar_senha:
            return jsonify({"error": "Senhas não coincidem"}), 400
        
        if Usuario.query.filter_by(email=email).first():
            return jsonify({"error": "E-mail já cadastrado"}), 400
        
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome,
            sobrenome=sobrenome,  
            cidade=cidade,
            bairro=bairro,
            profissao=profissao,
            email=email,
            senha=senha_hash
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return jsonify({"success": "Usuário cadastrado com sucesso"}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar os dados: {str(e)}")
            return jsonify({"error": "Houve um erro ao salvar os dados"}), 500
    return render_template('Cadastro/index.html')
