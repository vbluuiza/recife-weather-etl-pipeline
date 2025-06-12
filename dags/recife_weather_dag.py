import sys
from pathlib import Path
import pendulum

# Define o diretório atual (pasta da DAG) e o diretório raiz do projeto
DAG_FOLDER = Path(__file__).parent
PROJECT_ROOT = DAG_FOLDER.parent
sys.path.append(str(PROJECT_ROOT))

# Imports do Airflow
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Imports de funções próprias do projeto (camadas de ETL)
from src.extract.extract_data import extract_data
from src.transform.transform_data import transform_data, loading_data
from src.load.load_data import load_data

# Importa variáveis e constantes da configuração do projeto
from config.settings import (
    FILES_FOLDER,
    PROCESSED_DATA_DIR,
    COLUMNS_DROP,
    COLUMNS_RENAME,
    DATE_COLUMNS,
    DB_SCHEMA,
    DB_TABLENAME
)


# Define a DAG (pipeline) principal utilizando o decorator do Airflow
@dag(
    dag_id='recife_weather_pipeline',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval='0 */9 * * *',   # Executa a cada 9 horas
    catchup=False,  # Evita execuções retroativas
    doc_md="""
    ### Pipeline ETL para Dados Meteorológicos de Recife
    1. Extrai dados da API e salva JSON.
    2. Transforma JSON em CSV limpo.
    3. Garante que a tabela exista no Postgres.
    4. Carrega CSV no banco.
    """,
    tags=['weather', 'etl', 'recife'],
)
def recife_weather_pipeline():

    # Task de extração dos dados da API
    @task
    def extract(ts_nodash, data_interval_start=None):
        print(f"Iniciando extração para a execução: {ts_nodash}")
        output_path = f"{FILES_FOLDER}/recife_weather_{ts_nodash}.json"  # Define o nome do arquivo de saída
        extract_data(output_path=output_path, execution_dt=data_interval_start) # Executa a função de extração
        return output_path # Retorna o caminho do arquivo extraído

    # Task de transformação dos dados brutos
    @task
    def transform(raw_file_path: str):
        print(f"Iniciando transformação para o arquivo: {raw_file_path}")
        raw_df = loading_data(raw_file_path)  # Carrega os dados do JSON em um DataFrame
        timestamp = Path(raw_file_path).stem.split('_')[-1] # Extrai o timestamp do nome do arquivo

        # Aplica as transformações definidas nas configurações
        processed_file_path = transform_data(
            df=raw_df,
            columns_drop=COLUMNS_DROP,
            columns_rename=COLUMNS_RENAME,
            date_columns=DATE_COLUMNS,
            processed_data_dir=PROCESSED_DATA_DIR,
            timestamp=timestamp
        )
        print(f"Arquivo transformado salvo em: {processed_file_path}")
        return processed_file_path # Retorna o caminho do CSV transformado

    # Operador SQL que garante a existência da tabela no banco de dados Postgres
    ensure_table_exists = PostgresOperator(
        task_id="ensure_table_exists",
        postgres_conn_id="postgres_etl_conn", # Conexão definida no Airflow
        sql=f"""
            CREATE SCHEMA IF NOT EXISTS {DB_SCHEMA};
            CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.{DB_TABLENAME} (
                city VARCHAR(255),
                country_code VARCHAR(10),
                weather_condition VARCHAR(255),
                weather_description TEXT,
                temperature REAL,
                feels_like_temp REAL,
                temp_min REAL,
                temp_max REAL,
                pressure INTEGER,
                humidity INTEGER,
                visibility_km REAL,
                wind_speed REAL,
                wind_direction_degrees INTEGER,
                cloudiness_percent INTEGER,
                latitude NUMERIC(10, 7),
                longitude NUMERIC(10, 7),
                measurement_datetime TIME,
                sunrise_datetime TIME,
                sunset_datetime TIME,
                record_timestamp TIMESTAMP,
                timezone VARCHAR(255)
            );
        """, # SQL para criação da tabela, se ela ainda não existir
    )

    # Tarefa de carregamento dos dados processados no banco de dados
    @task
    def load(processed_df): 
        """Etapa 4: Carregar"""
        print("Iniciando carregamento dos dados para o banco...")
        
        load_data(df=processed_df) # Executa a função de carregamento
        print("Dados carregados com sucesso!")

    # Definição da ordem de execução das tarefas no pipeline
    extract_output = extract() # Extração dos dados
    transform_output = transform(extract_output) # Transformação dos dados extraídos
    load_output = load(transform_output) # Carregamento dos dados transformados

    # Encadeamento da dependência entre as tarefas:
    # Primeiro transforma -> garante que a tabela existe -> depois carrega no banco
    transform_output.operator >> ensure_table_exists >> load_output.operator


# Executa a definição da DAG
recife_weather_pipeline()

