import logging
from utils import load_config, get_db_connection
from etl import fetch_reports_by_country, process_reports, save_reports_to_db

def main():
    cfg = load_config()
    logging.basicConfig(filename=cfg['log_file'], level=logging.INFO)
    logging.info("ETL started")
    
    conn = get_db_connection(cfg)
    
    for iso3 in cfg['countries']:
        logging.info(f"Fetching reports for {iso3}")
        df_raw = fetch_reports_by_country(iso3)
        if df_raw.empty:
            logging.warning(f"No data for {iso3}")
            continue
        
        df = process_reports(df_raw)
        save_reports_to_db(conn, df)
        logging.info(f"Saved {len(df)} rows for {iso3}")
    
    conn.close()
    logging.info("ETL finished")

if __name__ == "__main__":
    main()
