import requests
import os
from dotenv import load_dotenv

#https://www.weatherapi.com/docs/
load_dotenv()

# Sua chave de API
WEATHERAPI = os.getenv("WEATHERAPI")

# URL atual
url = "http://api.weatherapi.com/v1/current.json?"
# Parâmetros
current_weather_params = f"key={WEATHERAPI}&q=-28.2933,-49.9337&lang=pt"

temperatura_atual_json = requests.get(url + current_weather_params)
temperatura_atual_dict = temperatura_atual_json.json()

print(temperatura_atual_dict)
