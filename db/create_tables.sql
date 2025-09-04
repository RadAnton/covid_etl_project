CREATE TABLE IF NOT EXISTS covid_regions (
    iso3 VARCHAR(3) PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS covid_reports (
    iso3 VARCHAR(3),
    province TEXT NULL,
    date DATE,
    confirmed INT,
    deaths INT,
    recovered INT,
    daily_confirmed INT,
    daily_deaths INT,
    daily_recovered INT,
    load_ts TIMESTAMP NOT NULL,
    PRIMARY KEY (iso3, province, date)
);