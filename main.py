from pathlib import Path
from src.extract.extract_data import extract_data
from src.transform.transform_data import transform_data, loading_data, find_most_recent_data
from src.load.load_data import load_data

from config.config import FILES_FOLDER, COLUMNS_DROP, COLUMNS_RENAME, TIMESTAMP, PROCESSED_DATA_DIR, DATETIME, FOLDER_PATH, DATE_COLUMNS

def main():
    try:
        print("="*50)
        print("Iniciando pipeline ETL Recife Weather")
        print("="*50)
        
        # Etapa 1: Extract (ETL)
        print("\n🔎 [1/3] Extraindo dados...")
        extract_data(datetime=DATETIME, timestamp=TIMESTAMP)
        path = find_most_recent_data(FILES_FOLDER)
        print(f"✅ Arquivo encontrado: {path}")
        
        # Etapa 2: Transform (ETL)
        print("\n🛠️ [2/3] Carregando e normalizando dados...")
        raw_df = loading_data(path)
        print("✅ Dados carregados e normalizados")
        
        # Etapa 2.1: Transform (ETL)
        print("\n📦 [2/3] Transformando e salvando dados processados...")
        transform_data(
            df=raw_df,
            columns_drop=COLUMNS_DROP,
            columns_rename=COLUMNS_RENAME,
            date_columns=DATE_COLUMNS,
            processed_data_dir=PROCESSED_DATA_DIR,
            timestamp=TIMESTAMP
        )
        print("✅ Dados transformados")
        
        # Etapa 2: Load (ETL)
        print("\n🚚 [3/3] Carregando dados processados para o destino final...")
        load_data(folder_path=FOLDER_PATH)
        print("✅ Dados carregados com sucesso!")
        
        print("\nPipeline executado com sucesso!")
        print("="*50)
        
    except Exception as e:
        print("="*50)
        print(f"❌ Ocorreu um erro no pipeline: {e}")
        print("="*50)
        
if __name__ == "__main__":
    main()