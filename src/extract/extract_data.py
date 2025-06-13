import requests
import os
from dotenv import load_dotenv
import json

def extract_data(output_path, execution_dt):
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()
    
     # Obtém a chave da API do OpenWeather
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY não encontrada no ambiente. Verifique seu arquivo .env.")
    
    # Define os parâmetros da cidade e país
    CITY_NAME = 'Recife, BR'
    COUNTRY_CODE = 'BR'
    
    # Monta a URL da requisição para a API OpenWeather
    URL_OPEN_WEATHER = f'https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME},{COUNTRY_CODE}&appid={API_KEY}&units=metric&lang=en'

    # Faz a requisição GET para a API
    response = requests.get(URL_OPEN_WEATHER)
    data = response.json()

    # Garante que o diretório do arquivo de saída exista
    output_dir = os.path.dirname(output_path)
    os.makedirs(f'data/raw', exist_ok=True)

    # Salva o conteúdo JSON no arquivo especificado
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'Arquivo salvo em {output_path}')
    