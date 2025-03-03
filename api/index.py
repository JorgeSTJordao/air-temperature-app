from api import app
from api.models.usuario import Usuario
from flask import render_template, flash, redirect, url_for
from dotenv import load_dotenv
from api.forms.login import FormsLogin
from api.forms.cadastro import FormsCadastro
from flask_bcrypt import Bcrypt
from api.routes.home import home_bp
from api.routes.planos.planos import planos_bp
from api.routes.pagamento.pagamento import pagamento_bp
from api.models.usuario import Usuario
from flask_login import login_user
load_dotenv()

app.register_blueprint(home_bp)
app.register_blueprint(planos_bp)
app.register_blueprint(pagamento_bp)

# Definindo o Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def landingpage():
    return render_template("landing.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    forms_login = FormsLogin()

    if forms_login.validate_on_submit():
        usuario_existe = Usuario.read_user(forms_login.email.data)

        if usuario_existe and bcrypt.check_password_hash(usuario_existe.senha, forms_login.senha.data):
            flash("Login realizado com sucesso!", "success")
    
            login_user(usuario_existe)

            return redirect(url_for("home_bp.home"))
        elif not usuario_existe:
            flash(f"Usuário inexistente com o e-mail {forms_login.email.data}", "danger")
        else:
            flash(f"Senha incorreta", "danger")

    return render_template("login.html", forms_login=forms_login)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    forms_cadastro = FormsCadastro()

    if forms_cadastro.validate_on_submit():
        usuario_existe = Usuario.read_user(forms_cadastro.email.data)

        if usuario_existe:     
            if usuario_existe.telefone.email:
                flash(f"Usuário já existente com o e-mail {forms_cadastro.email.data}", "danger")
            elif usuario_existe.telefone:
                flash(f"Esse telefone já está sendo utilizado", "danger")
        else:
            # Envio de código via SMS
            senha_hash = bcrypt.generate_password_hash(forms_cadastro.senha.data).decode("utf-8")

            Usuario.create(email=forms_cadastro.email.data, senha=senha_hash, telefone=forms_cadastro.telefone.data)
            flash("Cadastro realizado com sucesso!", "success")

            return redirect(url_for("planos_bp.planos"))

    return render_template("cadastro.html", forms_cadastro=forms_cadastro)

