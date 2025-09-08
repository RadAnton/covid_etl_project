FROM python:3.11-slim

# Set working directory
WORKDIR /Users/antonradchenko/Documents/covid_etl_project

# Install system dependencies (for psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

RUN chmod +x wait_for_db.sh


CMD ["./wait_for_db.sh", "db", "python", "main.py"]
