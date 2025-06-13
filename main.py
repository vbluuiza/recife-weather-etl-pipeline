from pathlib import Path
from src.extract.extract_data import extract_data
from src.transform.transform_data import transform_data, loading_data, find_most_recent_data
from src.load.load_data import load_data
from datetime import datetime
import pandas as pd

from config.settings import FILES_FOLDER, COLUMNS_DROP, COLUMNS_RENAME, PROCESSED_DATA_DIR, FOLDER_PATH, DATE_COLUMNS



def main():
    """
    Executa o pipeline ETL (fora do Docker) completo para coleta de dados meteorológicos de Recife:
    1. Extração via API
    2. Transformação e limpeza
    3. Carga no banco de dados
    """
    
    # Gera timestamp atual e define caminho do arquivo bruto (.json)
    DATETIME = datetime.now()
    TIMESTAMP = DATETIME.strftime('%d-%m-%Y_%H-%M-%S')
    output_path = FILES_FOLDER / f"recife_weather_{TIMESTAMP}.json"
    
    try:
        print("="*50)
        print("Iniciando pipeline ETL Recife Weather")
        print("="*50)
        
        # Etapa 1: Extract (ETL)
        print("\n🔎 [1/3] Extraindo dados...")
        extract_data(output_path=output_path, execution_dt=DATETIME)
        path = find_most_recent_data(FILES_FOLDER)
        print(f"✅ Arquivo encontrado: {path}\n")
        
        # Etapa 2: Transform (ETL)
        print("\n🛠️ [2/3] Carregando e normalizando dados...")
        raw_df = loading_data(path)
        print("✅ Dados carregados e normalizados\n")
        
        # Etapa 2.1: Transform (ETL)
        print("\n📦 [2/3] Transformando e salvando dados processados...")
        processed_path = transform_data(
            df=raw_df,
            columns_drop=COLUMNS_DROP,
            columns_rename=COLUMNS_RENAME,
            date_columns=DATE_COLUMNS,
            processed_data_dir=PROCESSED_DATA_DIR,
            timestamp=TIMESTAMP
        )
        print("✅ Transformação concluída\n")
        
        # Etapa 3: Load (ETL)
        print("\n🚚 [3/3] Carregando dados processados para o destino final...")
        load_data(df=processed_path)
        print("✅ Dados carregados com sucesso no banco!\n")
        
        print("\nPipeline executado com sucesso!")
        print("="*50)
        
    except Exception as e:
        print("="*50)
        print(f"❌ Ocorreu um erro no pipeline: {e}")
        print("="*50)
        
if __name__ == "__main__":
    main()