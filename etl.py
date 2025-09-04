import pandas as pd
from utils import fetch_json
from datetime import datetime

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
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO covid_reports 
            (iso3, province, date, confirmed, deaths, recovered, daily_confirmed, daily_deaths, daily_recovered, load_ts)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (iso3, province, date) DO UPDATE
            SET confirmed = EXCLUDED.confirmed,
                deaths = EXCLUDED.deaths,
                recovered = EXCLUDED.recovered,
                daily_confirmed = EXCLUDED.daily_confirmed,
                daily_deaths = EXCLUDED.daily_deaths,
                daily_recovered = EXCLUDED.daily_recovered,
                load_ts = EXCLUDED.load_ts
        """, (
            row['iso3'], row['province'], row['date'],
            row['confirmed'], row['deaths'], row['recovered'],
            row['daily_confirmed'], row['daily_deaths'], row['daily_recovered'],
            row['load_ts']
        ))
    conn.commit()
    cursor.close()
