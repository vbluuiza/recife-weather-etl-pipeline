import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
import os 
import glob
import pytz
from config.settings import RECIFE_TZ


def find_most_recent_data(files_folder):
    """
    Retorna o caminho do arquivo JSON mais recente na pasta especificada.
    Os arquivos são identificados pelo padrão 'recife_weather_*.json'.
    """
    files = sorted(files_folder.glob('recife_weather_*.json'), reverse=True)

    if not files:
        raise FileNotFoundError(f'Nenhum arquivo JSON encontrado na pasta {files_folder}.')
    
    return str(files[0])

def loading_data(path):
    """
    Lê e normaliza o conteúdo de um arquivo JSON contendo dados climáticos.
    Retorna um DataFrame consolidado com dados principais e meteorológicos.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            
        # Normaliza os dados principais e o campo 'weather'
        df_main = pd.json_normalize(data_json)
        df_weather = pd.json_normalize(data_json['weather'])

        # Remove coluna aninhada duplicada e concatena as informações do tempo
        df_main = df_main.drop('weather', axis=1)
        df = pd.concat([df_weather, df_main], axis=1)
        
        print('Dados carregados e normalizados com sucesso. √')
        return df
    
    except Exception as e:
        print(f'Erro ao carregar e normalizar dados: {e}')
        raise
    
def transform_data(df, columns_drop, processed_data_dir, columns_rename, date_columns, timestamp):
    """
    Aplica transformações no DataFrame bruto:
    - Renomeia colunas
    - Remove colunas irrelevantes
    - Converte timestamps Unix para horário local (HH:MM:SS)
    - Gera timestamp de registro
    - Converte visibilidade para km
    - Ordena colunas e exporta o resultado como CSV
    """
    
    # Renomeia colunas brutas para nomes temporários mais descritivos
    df = df.rename(columns={
    'id': 'weather_id',
    'main': 'weather_main',
    'description': 'weather_description'
})  
    # Remove colunas desnecessárias
    df = df.drop(columns=columns_drop)
    
    # Renomeia para nomes finais padronizados
    df = df.rename(columns=columns_rename)
    
    now = datetime.now(RECIFE_TZ)
    
    # Aplica o offset de timezone (fornecido em segundos)
    timezone = df['timezone'].iloc[0]
    offset = pd.Timedelta(seconds=timezone)
    
    # Converte colunas de data (Unix) para formato local (HH:MM:SS em Recife)
    for column in date_columns:
        if column in df.columns:
            try:
                df[column] = pd.to_datetime(df[column], unit='s')
                df[column] = df[column].dt.tz_localize('UTC').dt.tz_convert(RECIFE_TZ)
                df[column] = df[column].dt.strftime('%H:%M:%S')
            except Exception as e:
                print(f"Erro ao formatar a coluna {column}: {e}")
                
    # Adiciona o timestamp de execução local (sem milissegundos)
    df['record_timestamp'] = df['record_timestamp'] = datetime.now(RECIFE_TZ)
    df['record_timestamp'] = df['record_timestamp'].dt.floor('S')

    # Converte visibilidade de metros para quilômetros, se existir
    if 'visibility_km' in df.columns:
        df['visibility_km'] = df['visibility_km'] / 1000
    
    # Ordena as colunas conforme ordem definida
    order_columns = [
        'city',
        'country_code',
        
        'weather_condition',
        'weather_description',
        
        'temperature',
        'feels_like_temp',
        'temp_min',
        'temp_max',
        'pressure',
        'humidity',
        
        'visibility_km',
        'wind_speed',
        'wind_direction_degrees',
        'cloudiness_percent',
        
        'latitude',
        'longitude',

        'measurement_datetime',
        'sunrise_datetime',
        'sunset_datetime',
        'record_timestamp',
        
        'timezone'
    ]
    
    existed_columns_order = [col for col in order_columns if col in df.columns]
    df = df[existed_columns_order]
    
    # Gera o caminho do arquivo de saída com base no timestamp atual
    output_filename = f'processed_recife_weather_{timestamp}.csv'
    output_path = processed_data_dir / output_filename
    
    # Cria a pasta destino se não existir
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Salva o DataFrame transformado em CSV, sem incluir o índice
    df.to_csv(output_path, index=False)
    
    print(f'Dados transformados salvos em {processed_data_dir} √')
    
    return df

