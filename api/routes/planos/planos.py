from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user

planos_bp = Blueprint("planos_bp", __name__)

@planos_bp.route("/planos")
def planos():
    return render_template("planos.html")

@planos_bp.route("/check_login")
def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return redirect(url_for("home"))

@planos_bp.route("/assinar_premium")
@login_required
def assinar_premium():
    # Aqui vai a lógica de assinatura do plano premium
    return render_template("planos.html")
