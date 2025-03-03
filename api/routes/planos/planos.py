from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user

planos_bp = Blueprint("planos_bp", __name__)

PLANOS = {
    'premium': {
        'nome': 'Plano Premium',
        'valor': 30.00,
        'periodo': 'mês',
        'descricao': 'Acesso a todos os recursos premium',
        'beneficios': [
            'Consultas ilimitadas',
            'Suporte prioritário 24/7',
            'Histórico detalhado',
            'Previsões avançadas'
        ]
    },
    'trial': {
        'nome': 'Plano Free Trial',
        'valor': 0.00,
        'periodo': '7 dias',
        'descricao': 'Acesso das funções do plano Premium por 7 dias',
        'beneficios': [
            'Acesso das funções do plano Premium'
        ]
    }
}

@planos_bp.route("/planos")
def planos():
    return render_template("planos.html", planos=PLANOS)

@planos_bp.route("/selecionar_plano/<tipo>")
@login_required
def selecionar_plano(tipo):
    if tipo not in PLANOS:
        return redirect(url_for('planos_bp.planos'))
    
    session['plano_selecionado'] = PLANOS[tipo]
    return redirect(url_for('pagamento_bp.pagamento'))

@planos_bp.route("/check_login")
def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return redirect(url_for("home_bp.home"))

@planos_bp.route("/assinar_premium")
@login_required
def assinar_premium():
    return redirect(url_for('planos_bp.planos'))
