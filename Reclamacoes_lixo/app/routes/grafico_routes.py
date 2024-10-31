# app/routes/grafico_routes.py
from flask import Blueprint, session, render_template
from app.models import db, Reclamacao

grafico_bp = Blueprint('grafico', __name__)

@grafico_bp.route('/graficos')
def exibir_graficos():
    # Obtém a cidade do usuário logado a partir da sessão
    user_city = session.get('usuario_cidade')

    if not user_city:
        return "Cidade do usuário não encontrada na sessão.", 400

    # Consulta as reclamações da cidade do usuário, agrupando por `tipo_reclamacao`
    reclamacoes = db.session.query(
        Reclamacao.tipo_reclamacao,
        db.func.count(Reclamacao.id).label("total_count"),
        db.func.sum(db.case((Reclamacao.status == 'resolvido', 1), else_=0)).label("resolved_count"),
    ).filter(Reclamacao.cidade == user_city).group_by(Reclamacao.tipo_reclamacao).all()

    # Calcula a taxa de resolução e formata os dados para o template
    complaint_data = []
    for reclamacao in reclamacoes:
        resolved_count = reclamacao.resolved_count
        total_count = reclamacao.total_count
        resolution_rate = (resolved_count / total_count * 100) if total_count > 0 else 0

        data = {
            'title': reclamacao.tipo_reclamacao,
            'resolution_rate': int(resolution_rate),
            'resolved_count': resolved_count,
            'unresolved_count': total_count - resolved_count,
            'total_count': total_count
        }
        complaint_data.append(data)

    # Renderiza o template com os dados das reclamações e o nome da cidade do usuário
    return render_template('Graficos/index.html', complaint_data=complaint_data, user_city=user_city)
