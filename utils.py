import requests
import logging
import psycopg2
import yaml
import os

def load_config(path='config.yaml'):
    with open(path) as f:
        return yaml.safe_load(f)

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_db_connection(_cfg=None):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "covid_db"),
        user=os.getenv("DB_USER", "antonradchenko"),
        password=os.getenv("DB_PASSWORD", "secret123"),
    )
    return conn

def fetch_json(url, retries=3):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logging.error(f"Attempt {i+1} failed: {e}")
    raise Exception(f"Failed to fetch data from {url} after {retries} retries")
