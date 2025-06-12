import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

def extract_data(datetime, timestamp):
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Obtém a chave da API a partir das variáveis de ambiente
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY não encontrada no ambiente. Verifique seu arquivo .env.")
    
    # Define o nome da cidade e o código do país para a requisição
    CITY_NAME = 'Recife, BR'
    COUNTRY_CODE = 'BR'
    
    # Monta a URL da API do OpenWeather com parâmetros e chave de API
    URL_OPEN_WEATHER = f'https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME},{COUNTRY_CODE}&appid={API_KEY}&units=metric&lang=en'

    # Faz a requisição GET para a API
    response = requests.get(URL_OPEN_WEATHER)
    
    # Converte a resposta JSON para um dicionário Python
    data = response.json()
    
    # Imprime os dados recebidos de forma formatada para visualização
    print("Dados recebidos da API OpenWeather:")

    # Define o caminho do arquivo onde o JSON será salvo, dentro da pasta 'data/raw'
    file_path = f'data/raw/recife_weather={timestamp}.json'
    
    # Cria a pasta 'data/raw' caso ela não exista
    os.makedirs(f'data/raw', exist_ok=True)

    # Salva os dados JSON no arquivo com indentação e encoding UTF-8
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'Arquivo salvo em {file_path}')
    