from pathlib import Path
from datetime import datetime
import pytz
# Diretórios
FILES_FOLDER = Path('data/raw')
PROCESSED_DATA_DIR = Path('data/processed')
FOLDER_PATH = 'data/processed/processed_recife_weather_*.csv'

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

# Nome do schema e tabela no Postgres
DB_SCHEMA = "weather_data"
DB_TABLENAME = "recife_weather_records"


RAW_FILENAME_PREFIX = "recife_weather_"

RECIFE_TZ = pytz.timezone("America/Recife")