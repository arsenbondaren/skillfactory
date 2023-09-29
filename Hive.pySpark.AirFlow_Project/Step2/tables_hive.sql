%hive

CREATE EXTERNAL TABLE IF NOT EXISTS staging.cities (
    iso2_country VARCHAR(2), 
    city VARCHAR(40), 
    accentCity VARCHAR(40), 
    region INT, 
    population INT, 
    latitude FLOAT, 
    longitude FLOAT
    );
CREATE EXTERNAL TABLE IF NOT EXISTS staging.capital (
    iso2_country VARCHAR(2), 
    capital VARCHAR(40)
    );
CREATE EXTERNAL TABLE IF NOT EXISTS staging.continent (
    iso2_country VARCHAR(2), 
    continent_code VARCHAR(2)
    );
CREATE EXTERNAL TABLE IF NOT EXISTS staging.currency (
    iso2_country VARCHAR(2), 
    currency_code VARCHAR(3)
    );
CREATE EXTERNAL TABLE IF NOT EXISTS staging.iso3 (
    iso2_country VARCHAR(2), 
    iso3_country VARCHAR(3)
    );
CREATE EXTERNAL TABLE IF NOT EXISTS staging.country_names (
    iso2_country VARCHAR(2), 
    country_name VARCHAR(40)
    );
CREATE EXTERNAL TABLE IF NOT EXISTS staging.phone (
    iso2_country VARCHAR(2), 
    phone_code VARCHAR(10)
    );

CREATE EXTERNAL TABLE IF NOT EXISTS staging.countries (
    country VARCHAR(40), 
    region VARCHAR(40), 
    population INT, 
    area FLOAT COMMENT 'sq. mi.',
    pop_density FLOAT COMMENT 'per sq. mi.', 
    coastline FLOAT COMMENT 'coast/area ratio', 
    net_migration FLOAT,
    infant_mortality FLOAT COMMENT 'per 1000 births', 
    GDP INT COMMENT '$ per capita', 
    literacy FLOAT COMMENT '%',
    phones FLOAT COMMENT 'per 1000', 
    arable FLOAT COMMENT '%', 
    crops FLOAT COMMENT '%', 
    other FLOAT COMMENT '%',
    climate INT, 
    birthrate FLOAT, 
    deathrate FLOAT, 
    agriculture FLOAT, 
    industry FLOAT, 
    service FLOAT
    );

CREATE EXTERNAL TABLE IF NOT EXISTS staging.nobel_laureates (
    year INT, 
    category VARCHAR(40), 
    prize VARCHAR(50), 
    motivation VARCHAR(100), 
    prize_share VARCHAR(4), 
    laureate_id INT, 
    laureate_type VARCHAR(20), 
    full_name VARCHAR(50), 
    birth_date DATE, 
    birth_city VARCHAR(40), 
    birth_country VARCHAR(40), 
    sex VARCHAR(20), 
    organization_name VARCHAR(50), 
    organization_city VARCHAR(40), 
    organization_country VARCHAR(40), 
    death_date DATE, 
    death_city VARCHAR(40), 
    death_country VARCHAR(40)
    );