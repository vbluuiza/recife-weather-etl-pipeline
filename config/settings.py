from pathlib import Path
from datetime import datetime

# Diretórios
FILES_FOLDER = Path('data/raw')
PROCESSED_DATA_DIR = Path('data/processed')
# Define o padrão dos arquivos de dados processados
FOLDER_PATH = 'data/processed/processed_recife_weather=*.csv'

# Timestamp atual no formato padronizado
DATETIME = datetime.now()
TIMESTAMP = DATETIME.strftime('%Y-%m-%d_%H-%M-%S')

# Dicionário para renomear colunas
COLUMNS_RENAME = {
    'weather_main': 'weather_condition',
    'dt': 'measurement_datetime',
    'visibility': 'visibility_km',
    'name': 'city',
    'coord.lon': 'longitude',
    'coord.lat': 'latitude',
    'sys.country': 'country_code',
    'main.temp': 'temperature',
    'main.feels_like': 'feels_like_temp',
    'main.temp_min': 'temp_min',
    'main.temp_max': 'temp_max',
    'main.pressure': 'pressure',
    'main.humidity': 'humidity',
    'wind.speed': 'wind_speed',
    'wind.deg': 'wind_direction_degrees',
    'clouds.all': 'cloudiness_percent',
    'sys.sunrise': 'sunrise_datetime',
    'sys.sunset': 'sunset_datetime'
}

# Colunas a remover
COLUMNS_DROP = ['icon', 'base', 'main.grnd_level', 'main.sea_level', 
                'sys.type', 'sys.id', 'cod', 'weather_id']

# Colunas com timestamps Unix
DATE_COLUMNS = ['measurement_datetime', 'sunrise_datetime', 'sunset_datetime']

DB_SCHEMA = "weather_data"
DB_TABLENAME = "recife_weather_records"