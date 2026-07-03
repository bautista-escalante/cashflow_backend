FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2 y bcrypt
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Ajustá "app.main:app" si tu entrypoint tiene otro path (ej: "main:app")
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
