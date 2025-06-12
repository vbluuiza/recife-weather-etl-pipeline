# 🌦️ Recife Weather ETL Pipeline

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para coletar, processar e armazenar dados climáticos da cidade de Recife utilizando a API do OpenWeather e salvando os dados em um banco de dados PostgreSQL.

---

## 🚀 Funcionalidades

- **Extração:** Coleta dados climáticos em tempo real da API OpenWeather.
- **Transformação:** Limpa, normaliza e converte os dados para um formato tabular pronto para análise.
- **Carga:** Salva os dados processados em uma tabela do PostgreSQL.

---

## 📁 Estrutura do Projeto

```
api_weather_pipeline/
│
├── config/                # Configurações e constantes do pipeline
├── data/
│   ├── raw/               # Dados brutos extraídos da API
│   └── processed/         # Dados processados prontos para carga
├── notebooks/             # Notebooks para análise e exploração dos dados
├── src/
│   ├── extract/           # Scripts de extração de dados
│   ├── transform/         # Scripts de transformação de dados
│   └── load/              # Scripts de carga de dados
├── .env                   # Variáveis de ambiente (API Key, conexão DB)
├── requirements.txt       # Dependências do projeto
├── Dockerfile             # Dockerfile para containerização
├── main.py                # Script principal do pipeline
└── README.md              # Este arquivo
```

---

## ⚙️ Como Executar

### 1. Pré-requisitos

- Python 3.11+
- PostgreSQL rodando e acessível
- Conta e chave de API do [OpenWeather](https://openweathermap.org/api)
- Docker (opcional, mas recomendado)

### 2. Configuração

1. **Clone o repositório:**
    
    ```bash
    git clone <https://github.com/seu-usuario/api_weather_pipeline.git>
    cd api_weather_pipeline
    ```
    
2. **Configure o arquivo `.env`:**
    
    ```bash
    API_KEY=SuaChaveDaAPI
    CREATE_ENGINE=postgresql+psycopg2://usuario:senha@host:porta/nome_do_banco
    ```
    
3. **Instale as dependências:**
    
    ```bash
    pip install -r requirements.txt
    ```
    

### 3. Executando o Pipeline

### Localmente

```bash
docker build -t api-weather-pipeline .
docker run --env-file .env api-weather-pipeline
```

## 📝 Notebooks

Veja exemplos de análise e exploração dos dados em [`notebooks/analysing_data.ipynb`](https://www.notion.so/notebooks/analysing_data.ipynb).

## 🛠️ Principais Tecnologias

- Python (pandas, SQLAlchemy, dotenv)
- PostgreSQL
- Docker
- OpenWeather API

---

## 📄 Licença

Este projeto é open-source e está sob a licença MIT.

---

## **👩‍💻 Desenvolvido por**

Luiza Vieira – Estudante de Análise e Desenvolvimento de Sistemas - Cesar School

- 💼 [LinkedIn](https://www.linkedin.com/in/vbluuiza)
- 💻 [GitHub](https://github.com/vbluuiza)