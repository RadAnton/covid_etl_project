# COVID-19 ETL Pipeline

A simple ETL (Extract, Transform, Load) pipeline that fetches COVID-19 data from [covid-api.com](https://covid-api.com/api) and loads it into PostgreSQL.  
Built for learning Data Engineering workflows using Python, Pandas, and PostgreSQL.

---

## Features

- Fetch COVID-19 reports per country.
- Calculate daily confirmed, deaths, and recovered cases.
- Load transformed data into PostgreSQL with UPSERT (avoids duplicates).
- Logging of ETL process.
- Easy configuration via `config.yaml`.

---
