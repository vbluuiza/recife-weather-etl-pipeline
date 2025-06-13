import sys
from pathlib import Path
import pendulum
from pendulum import timezone

# Define os caminhos principais do projeto
DAG_FOLDER = Path(__file__).parent
PROJECT_ROOT = DAG_FOLDER.parent
sys.path.append(str(PROJECT_ROOT)) # Permite importar módulos da raiz do projeto

# Imports do Airflow
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Imports das funções do pipeline ETL
from src.extract.extract_data import extract_data
from src.transform.transform_data import transform_data, loading_data
from src.load.load_data import load_data

# Imports das configurações do projeto
from config.settings import (
    FILES_FOLDER,
    PROCESSED_DATA_DIR,
    COLUMNS_DROP,
    COLUMNS_RENAME,
    DATE_COLUMNS,
    DB_SCHEMA,
    DB_TABLENAME,
    RAW_FILENAME_PREFIX
)


# Define a DAG principal com agendamento e metadados
@dag(
    dag_id='recife_weather_pipeline',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval='0 */9 * * *',   # Executa a cada 9 horas
    catchup=False,  # Evita execuções retroativas
    doc_md="""
    ### 🌦️ Pipeline ETL de Clima - Recife
    Este pipeline executa automaticamente:
    1. Extração de dados da API do OpenWeather
    2. Transformação e limpeza dos dados
    3. Verificação/criação da tabela no PostgreSQL
    4. Carga dos dados no banco
    """,
    tags=['weather', 'etl', 'recife'],
)

def recife_weather_pipeline():

    # Task: Extração dos dados da API do OpenWeather
    @task
    def extract(ts_nodash=None, data_interval_start=None, **kwargs):
        # Recupera a data de execução e converte para o fuso horário de Recife
        execution_date = kwargs['execution_date']
        recife_time = execution_date.in_tz("America/Recife")
        
        # Formata timestamp para nome do arquivo
        timestamp = recife_time.strftime('%d-%m-%Y_%H-%M-%S')
        
        print(f"Iniciando extração para a execução: {timestamp}")
        output_path = f"{FILES_FOLDER}/recife_weather_{timestamp}.json"  # Define o nome do arquivo de saída
         
        # Executa a função de extração e salva JSON
        extract_data(output_path=output_path, execution_dt=data_interval_start) 
        return output_path

    # Task: Transformação dos dados extraídoss
    @task
    def transform(raw_file_path: str):
        print(f"Iniciando transformação para o arquivo: {raw_file_path}")
        
        # Carrega e normaliza JSON para DataFrame
        raw_df = loading_data(raw_file_path)  
        
        # Extrai timestamp do nome do arquivo
        timestamp = Path(raw_file_path).stem.replace(RAW_FILENAME_PREFIX, "") # Extrai o timestamp do nome do arquivo

        # Aplica transformações e retorna caminho do CSV processado
        processed_file_path = transform_data(
            df=raw_df,
            columns_drop=COLUMNS_DROP,
            columns_rename=COLUMNS_RENAME,
            date_columns=DATE_COLUMNS,
            processed_data_dir=PROCESSED_DATA_DIR,
            timestamp=timestamp
        )
        print(f"Arquivo transformado salvo em: {processed_file_path}")
        return processed_file_path

    # Task: Criação da tabela no banco (caso não exista)
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

    # Task: Carga dos dados transformados no banco de dados
    @task
    def load(processed_file_path): 
        print("Iniciando carregamento dos dados para o banco...")
        load_data(df=processed_file_path)
        print("Dados carregados com sucesso!")

    # Encadeamento das tasks: extract → transform → ensure_table_exists → load
    extract_output = extract() 
    transform_output = transform(extract_output)
    load_output = load(transform_output) 

    transform_output >> ensure_table_exists >> load_output


# Instancia a DAG
recife_weather_pipeline()

