import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///air_temperature_app.db"

db = SQLAlchemy(app)

login_manager = LoginManager(app)

# A variável é o nome da função que renderiza a página de login
login_manager.login_view = "login"

from api import index

# ✅ Criar ou resetar banco de dados
with app.app_context():
    db_path = os.path.join(os.getcwd(), "instance", "air_temperature_app.db")

    if os.path.exists(db_path):
        print("🔄 Banco de dados encontrado. Resetando...")
        db.drop_all()
        db.create_all()
        print("✅ Banco de dados recriado com sucesso!")
    else:
        print("🆕 Nenhum banco encontrado. Criando um novo...")
        db.create_all()
        print("✅ Banco de dados criado com sucesso!")

@login_manager.user_loader
def load_user(user_id):
    from api.models.usuario import Usuario
    
    return Usuario.query.get(int(user_id))