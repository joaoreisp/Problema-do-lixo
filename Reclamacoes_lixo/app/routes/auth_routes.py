# app/routes/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "E-mail ou senha incorreto"}), 400
    return render_template('Login/index.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/senha')
def esqueceu_senha():
    return render_template('Senha/index.html')


@auth_bp.route('/redefinir_senha', methods=['GET', 'POST'])
def redefinir_senha():
    if request.method == 'POST':
        email = request.form['email']
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash('E-mail não encontrado.', 'danger')
        elif nova_senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
        else:
            usuario.senha = generate_password_hash(nova_senha)
            db.session.commit()
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('auth.login'))

    return render_template('Senha/redefinir_senha.html')