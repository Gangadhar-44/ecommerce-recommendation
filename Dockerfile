FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT ecommerce_recommendation.wsgi:application