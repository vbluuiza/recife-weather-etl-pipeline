import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Time
import os
import glob
import pytz
from config.settings import RECIFE_TZ


def load_data(df):
    # Carrega variáveis de ambiente do arquivo .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Garante que o objeto recebido é um DataFrame válido
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Objeto recebido não é um DataFrame.")
    
    # Recupera a URL de conexão do banco de dados a partir das variáveis de ambiente
    database_url = os.getenv('CREATE_ENGINE')
    if not database_url:
        raise ValueError('Variável de ambiente CREATE_ENGINE não encontrada.')
    
    # Colunas que devem ser convertidas para tipo horário (HH:MM:SS)
    date_columns = [
        'measurement_datetime', 
        'sunrise_datetime', 
        'sunset_datetime',
    ]
    
    # Lê o arquivo CSV em um DataFrame do pandas
    print("DataFrame recebido para carregamento:")
    
   # Converte colunas de horário (Unix timestamp -> time)
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%H:%M:%S', errors='coerce').dt.time
            
    # Converte record_timestamp para datetime
    df['record_timestamp'] = pd.to_datetime(df['record_timestamp'], errors='coerce')

   # Aplica fuso horário se necessário
    if not pd.api.types.is_datetime64tz_dtype(df['record_timestamp']):
        df['record_timestamp'] = df['record_timestamp'].dt.tz_localize(RECIFE_TZ, ambiguous='NaT', nonexistent='NaT')

    # Converte para horário de Recife e remove o timezone (salva como timestamp local)
    df['record_timestamp'] = df['record_timestamp'].dt.tz_convert(RECIFE_TZ).dt.tz_localize(None)
            
    # Cria a engine de conexão com o banco de dados
    print(f'Conectando ao banco de dados...{database_url} √')
    engine = create_engine(database_url)
    
    # Salva os dados no banco de dados na tabela especificada
    print('Enviando dados para a tabela "recife_weather_records" √')
    dtype_map = {col: Time() for col in date_columns}
    df.to_sql("recife_weather_records", con=engine, if_exists="append", index=False, dtype=dtype_map)
    
    print("\n✅ Dados salvos com sucesso no Postgres")
