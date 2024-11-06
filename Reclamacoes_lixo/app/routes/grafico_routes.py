from flask import Blueprint, session, render_template, request
from app.models import db, Reclamacao

grafico_bp = Blueprint('grafico', __name__)

@grafico_bp.route('/graficos')
def exibir_graficos():
    # Obtém a cidade do usuário logado a partir da sessão
    user_city = session.get('usuario_cidade')
    if not user_city:
        return "Cidade do usuário não encontrada na sessão.", 400

    # Busca todas as cidades únicas das reclamações
    cidades = db.session.query(Reclamacao.cidade).distinct().all()
    cidades = [cidade[0] for cidade in cidades]  # Extrai os nomes das cidades
    cidades.insert(0, "Todos")  # Adiciona "Todos" no início da lista

    # Filtro por cidade: mantém a cidade do usuário logado como padrão
    cidade_filtro = request.args.get('cidade', user_city)

    # Se "Todos" for selecionado, mostre todas as reclamações e ajuste o título
    if cidade_filtro == 'Todos':
        user_city = "Todos"
        reclamacoes_query = Reclamacao.query
    else:
        user_city = cidade_filtro  # Atualiza o nome da cidade no título
        reclamacoes_query = Reclamacao.query.filter(Reclamacao.cidade == cidade_filtro)

    # Consulta as reclamações agrupadas por `tipo_reclamacao`
    reclamacoes = db.session.query(
        Reclamacao.tipo_reclamacao,
        db.func.count(Reclamacao.id).label("total_count"),
        db.func.sum(db.case((Reclamacao.status == 'resolvido', 1), else_=0)).label("resolved_count"),
    ).filter(
        Reclamacao.cidade == cidade_filtro if cidade_filtro != 'Todos' else True
    ).group_by(Reclamacao.tipo_reclamacao).all()

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

    # Renderiza o template com os dados das reclamações, o nome da cidade, e a lista de cidades
    return render_template('Graficos/index.html', complaint_data=complaint_data, user_city=user_city, cidades=cidades)
