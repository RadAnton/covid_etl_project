import pandas as pd
from utils import fetch_json
from datetime import datetime
from psycopg2.extras import execute_batch

API_BASE = "https://covid-api.com/api"

def fetch_reports_by_country(iso3):
    url = f"{API_BASE}/reports?iso={iso3}"
    data = fetch_json(url)
    if data and 'data' in data:
        df = pd.DataFrame(data['data'])
        return df
    return pd.DataFrame()

def process_reports(df):
    df = df[['region', 'confirmed', 'deaths', 'recovered', 'date']].copy()
    
    df['province'] = df['region'].apply(lambda x: x.get('province'))
    df['iso3'] = df['region'].apply(lambda x: x.get('iso'))
    df['country'] = df['region'].apply(lambda x: x.get('name'))
    
    df = df.drop(columns=['region'])
    
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    df = df.sort_values(['iso3', 'province', 'date'])
    
    df['daily_confirmed'] = df.groupby(['iso3', 'province'])['confirmed'].diff().fillna(df['confirmed'])
    df['daily_deaths'] = df.groupby(['iso3', 'province'])['deaths'].diff().fillna(df['deaths'])
    df['daily_recovered'] = df.groupby(['iso3', 'province'])['recovered'].diff().fillna(df['recovered'])
    
    df['load_ts'] = datetime.now()
    
    return df

def save_reports_to_db(conn, df):
    with conn.cursor() as cur:
        data = [
            (
                int(row.confirmed) if row.confirmed is not None else None,
                int(row.deaths) if row.deaths is not None else None,
                int(row.recovered) if row.recovered is not None else None,
                row.date,
                row.province,
                row.iso3,
                int(row.daily_confirmed) if row.daily_confirmed is not None else None,
                int(row.daily_deaths) if row.daily_deaths is not None else None,
                int(row.daily_recovered) if row.daily_recovered is not None else None,
                row.load_ts,
            )
            for row in df.itertuples(index=False)
        ]

        query = """
        INSERT INTO covid_reports (
            confirmed, deaths, recovered, date,
            province, iso3,
            daily_confirmed, daily_deaths, daily_recovered,
            load_ts
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (iso3, province, date)
        DO UPDATE SET
            confirmed = EXCLUDED.confirmed,
            deaths = EXCLUDED.deaths,
            recovered = EXCLUDED.recovered,
            daily_confirmed = EXCLUDED.daily_confirmed,
            daily_deaths = EXCLUDED.daily_deaths,
            daily_recovered = EXCLUDED.daily_recovered,
            load_ts = EXCLUDED.load_ts
        """

        execute_batch(cur, query, data, page_size=500)

    conn.commit()