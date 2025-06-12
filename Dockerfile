# Usa imagem oficial do Python
FROM python:3.11-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto
COPY . .

# Instale as dependências do Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponha a porta do Postgres se necessário (opcional)
# EXPOSE 5432

# Defina variáveis de ambiente (opcional, pode usar .env)
ENV PYTHONUNBUFFERED=1

# Comando para rodar o pipeline
CMD ["python", "main.py"]