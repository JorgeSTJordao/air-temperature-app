from flask import Blueprint, render_template, request, flash
from api.forms.location import FormsLocation
from api.config.URL_BASE import URL_BASE
from api.routes.planos.planos import planos_bp
from api.routes.pagamento.pagamento import pagamento_bp
import os
import requests
from flask_login import login_required

# Sua chave de API
WEATHERAPI = os.getenv("WEATHERAPI")

# URL base da API
url = URL_BASE

home_bp = Blueprint("home_bp", __name__)

home_bp.register_blueprint(planos_bp)
home_bp.register_blueprint(pagamento_bp)
@home_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    forms_location = FormsLocation()
    valores_temp = None

    if request.method == "POST":
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        try:
            # Parâmetros (Latitude e Longitude)
            current_weather_params = f"key={WEATHERAPI}&q={latitude},{longitude}"

            # Requisição
            response = requests.get(url + current_weather_params)
            temperatura_atual_dict = response.json()

            # Verifica se houve erro na resposta
            if response.status_code != 200 or "error" in temperatura_atual_dict:
                flash("Erro: Coordenadas não são aceitas ou são inválidas.", "danger")
            else:
                # Processamento dos dados
                valores_temp = [
                    temperatura_atual_dict['location']['name'],     # Nome da cidade
                    temperatura_atual_dict['location']['region'],   # Região
                    temperatura_atual_dict['location']['country'],  # País
                    temperatura_atual_dict['current']['temp_c'],    # Temperatura em Celsius
                    round(temperatura_atual_dict['current']['temp_c'] + 273.15, 2)  # Temperatura em Kelvin
                ]

        except Exception as e:
            flash("Erro ao processar a solicitação. Verifique os valores inseridos.", "danger")
            print("Erro:", e)

    return render_template("home.html", forms_location=forms_location, valores_temp=valores_temp)