from flask import Blueprint, current_app, render_template, request, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app.models import db, Reclamacao, Usuario
import os

reclamacao_bp = Blueprint('reclamacao', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Defina o diretório onde as imagens serão armazenadas
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', 'static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@reclamacao_bp.route('/index', methods=['GET', 'POST'])
def criar_reclamacao():
    usuarios = Usuario.query.all()


    if request.method == 'POST':
        
        try:
            # Captura os dados do formulário
            tipo_reclamacao = request.form.get('sector')
            cidade = request.form.get('city')
            bairro = request.form.get('neighborhood')
            descricao = request.form.get('description')
            
            print(tipo_reclamacao, cidade, bairro, descricao, session)

            # Obtenha o usuário logado
            id_usuario = session.get('usuario_id')
            if not id_usuario:
                flash('Usuário não autenticado.', 'danger')
                return redirect(url_for('auth.login'))

            # Verifica se um arquivo foi anexado
            file = request.files.get('anexo')
            if not file or file.filename == '':
                flash('Nenhum arquivo anexado', 'danger')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                # Verifique se o diretório existe e crie caso contrário
                if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                    os.makedirs(current_app.config['UPLOAD_FOLDER'])

                file.save(filepath)

                # Caminho relativo para o banco de dados
                relative_filepath = os.path.join('uploads', filename).replace('\\', '/')

                # Armazene o caminho no banco
                nova_reclamacao = Reclamacao(
                    tipo_reclamacao=tipo_reclamacao,
                    descricao=descricao,
                    cidade=cidade,
                    bairro=bairro,
                    anexo=relative_filepath,
                    usuario_id=id_usuario
                )


                db.session.add(nova_reclamacao)
                db.session.commit()  # Tentativa de commit

                flash('Reclamação criada com sucesso!', 'success')
                return redirect(url_for('reclamacao.listar_reclamacoes'))
            else:
                flash('Formato de arquivo não permitido', 'danger')

        except Exception as e:
            db.session.rollback()  # Reverte em caso de erro
            print(f"Erro ao salvar a reclamação no banco de dados: {str(e)}")
            flash(f'Ocorreu um erro ao salvar a reclamação: {str(e)}', 'danger')

    return render_template('Reclamar/index.html', usuarios=usuarios)


@reclamacao_bp.route('/reclamacoes', methods=['GET'])
def listar_reclamacoes():
    try:
        usuarios = Usuario.query.all()
        reclamacoes = Reclamacao.query.all()
        
        for reclamacao in reclamacoes:
            reclamacao.anexo = str(reclamacao.anexo) if reclamacao.anexo else None

        return render_template('Home_page/index.html', usuarios=usuarios, reclamacoes=reclamacoes)
    except Exception as e:
        print(f"Erro ao buscar os dados: {str(e)}")
        return "Houve um erro ao buscar os dados", 500
