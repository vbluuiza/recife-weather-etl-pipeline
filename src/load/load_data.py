import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Time
from dotenv import load_dotenv
import os
import glob


def load_data(folder_path):
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Busca todos os arquivos que correspondem ao padrão definido
    files = sorted(glob.glob(folder_path), reverse=True)
    if not files:
        print('🚫 Nenhum arquivo CSV de dados processados encontrado no diretório especificado.')
        return 
    
    # Seleciona o arquivo mais recente
    path = files[0]
    
    # Recupera a URL de conexão do banco de dados a partir das variáveis de ambiente
    database_url = os.getenv('CREATE_ENGINE')
    if not database_url:
        raise ValueError('Variável de ambiente CREATE_ENGINE não encontrada.')
    
    date_columns = [
        'measurement_datetime', 
        'sunrise_datetime', 
        'sunset_datetime',
    ]
    
    # Lê o arquivo CSV em um DataFrame do pandas
    print('Lendo dados do arquivo CSV... √')
    df = pd.read_csv(path)
    print(df.head())
    
    # Formantando o tipo das colunas no date_columns
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%H:%M:%S', errors='coerce').dt.time
            
    # Cria a engine de conexão com o banco de dados
    print(f'Conectando ao banco de dados...{database_url} √')
    engine = create_engine(database_url)
    
    
    # Salva os dados no banco de dados na tabela especificada
    print('Enviando dados para a tabela "recife_weather_records" √')
    dtype_map = {col: Time() for col in date_columns}
    df.to_sql("recife_weather_records", con=engine, if_exists="append", index=False)
    
    print("\n✅ Dados salvos com sucesso no Postgres")
