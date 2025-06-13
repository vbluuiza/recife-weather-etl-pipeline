# 🌦️ Recife Weather Pipeline

Pipeline ETL para coleta, processamento e armazenamento de dados meteorológicos de Recife, utilizando **Python**, **Apache Airflow** e **PostgreSQL**.

---

## 📚 Visão Geral

- **Extração:** Coleta dados da API OpenWeather e salva em JSON.
- **Transformação:** Normaliza, limpa e transforma os dados em CSV.
- **Carga:** Insere os dados processados em um banco PostgreSQL.
- **Orquestração:** Todo o fluxo é automatizado via Apache Airflow.

---

## 🗂️ Estrutura do Projeto

```bash
api_weather_pipeline/
├── config/                  # Configurações globais do pipeline
│   └── settings.py
├── dags/                    # DAGs do Airflow
│   └── recife_weather_dag.py
├── data/                    # Dados brutos e processados (ignorado pelo git)
│   ├── raw/
│   └── processed/
├── logs/                    # Logs do Airflow (ignorado pelo git)
├── plugins/                 # Plugins customizados do Airflow (opcional)
├── src/                     # Código fonte do ETL
│   ├── extract/
│   │   └── extract_data.py
│   ├── transform/
│   │   └── transform_data.py
│   └── load/
│       └── load_data.py
├── notebooks/               # Notebooks de análise e exploração
├── tests/                   # Testes automatizados
├── .env                     # Variáveis de ambiente (NÃO subir para o git)
├── .gitignore
├── .dockerignore
├── docker-compose.yml       # Orquestração dos containers
├── Dockerfile               # Build customizado (opcional)
├── requirements.txt         # Dependências Python
└── main.py                  # Execução manual do pipeline (fora do Airflow)

```

---

## ⚙️ Configuração do Ambiente

### 1. **Pré-requisitos**

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11+ (apenas para execução manual)

### 2. **Clone o Repositório**

```bash
git clone https://github.com/seu-usuario/api_weather_pipeline.git
cd api_weather_pipeline
```

### 3. **Crie o Arquivo `.env`**

Baseie-se no modelo abaixo:

```bash
API_KEY=SEU_TOKEN_OPENWEATHER
CREATE_ENGINE=postgresql+psycopg2://usuario:senha@postgres-etl:5432/recife_weather
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=recife_weather
# ...demais variáveis do Airflow...
```

### 4. **Suba o Ambiente com Docker Compose**

```bash
docker-compose up -d
```

- O Airflow estará disponível em: [http://localhost:8080](http://localhost:8080/)
- Usuário e senha definidos no `.env`

### 5. **Ative a DAG no Airflow**

1. Acesse a interface web do Airflow
2. Ative a DAG `recife_weather_pipeline`
3. Você pode disparar manualmente ou aguardar a execução automática

---

## 🛠️ Execução Manual (fora do Airflow)

Se desejar rodar o pipeline manualmente:

```bash
python main.py
```

---

## 🧩 Principais Arquivos

- `dags/recife_weather_dag.py`: DAG principal do Airflow
- `src/extract/extract_data.py`: Função de extração da API
- `src/transform/transform_data.py`: Funções de transformação
- `src/load/load_data.py`: Função de carga no PostgreSQL
- `config/settings.py`: Parâmetros globais do pipeline
- `main.py`: Execução manual do pipeline

---

## 📝 Observações

- Os diretórios `data/raw`, `data/processed` e `logs` estão no `.gitignore`
- A tabela é criada automaticamente no banco se não existir
- O Airflow usa a conexão nomeada `postgres_etl_conn`

---

## 📚 Licença

Este projeto é open-source e está sob a licença MIT.

---

## 👩‍💻 Desenvolvido por

Luiza Vieira – Estudante de Análise e Desenvolvimento de Sistemas - Cesar School

- 💼 [LinkedIn](https://www.linkedin.com/in/vbluuiza)
- 💻 [GitHub](https://github.com/vbluuiza)
