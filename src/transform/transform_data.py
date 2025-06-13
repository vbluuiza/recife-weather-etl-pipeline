import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
import os 
import glob


def find_most_recent_data(files_folder):
    """
    Encontra o arquivo JSON mais recente na pasta especificada, baseado na ordenação reversa.
    """
    files = sorted(files_folder.glob('recife_weather=*.json'), reverse=True)

    if not files:
        raise FileNotFoundError(f'Nenhum arquivo JSON encontrado na pasta {files_folder}.')
    
    # Retorna o caminho do arquivo mais recente como string
    return str(files[0])

def loading_data(path):
    """
    Lê o arquivo JSON, normaliza os dados e 
    retorna um DataFrame combinado com informações do tempo e metadados.
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
    - Converte timestamps para datetime
    - Ajusta o fuso horário
    - Converte datas para hora (HH:MM:SS)
    - Converte visibilidade de metros para quilômetros
    """
    
    # Renomeia colunas iniciais
    df = df.rename(columns={
    'id': 'weather_id',
    'main': 'weather_main',
    'description': 'weather_description'
})  
    # Remove colunas desnecessárias
    df = df.drop(columns=columns_drop)
    
    # Renomeia para nomes finais padronizados
    df = df.rename(columns=columns_rename)
    
    # Aplica o offset de timezone (fornecido em segundos)
    timezone = df['timezone'].iloc[0]
    offset = pd.Timedelta(seconds=timezone)
    
    # Converte timestamps Unix para datetime com fuso horário
    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], unit='s') + offset

    # Cria coluna com datetime completo (ano, mês, dia, hora, minuto, segundo)
    df['record_timestamp'] = df['measurement_datetime']
    
    # Extrai apenas o horário das colunas de tempo
    for column in date_columns:
        if column in df.columns:
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce')  # garante datetime
                df[column] = df[column].dt.strftime('%H:%M:%S')  # extrai só o horário
            except Exception as e:
                print(f"Erro ao formatar a coluna {column}: {e}")

        
    # Converte visibilidade de metros para quilômetros
    df['visibility_km'] = df['visibility_km'] / 1000
    
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
    # Formata a data e hora para usar no nome do arquivo CSV
    output_filename = f'processed_recife_weather={timestamp}.csv'
    output_path = processed_data_dir / output_filename
    
    # Cria a pasta destino se não existir
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Salva o DataFrame transformado em CSV, sem incluir o índice
    df.to_csv(output_path, index=False)
    
    print(f'Dados transformados salvos em {processed_data_dir} √')
    
    return df

