Таблицы в озере создаем с помощью DDL запросов в Hive:

CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.cities_incr (
    iso2_country VARCHAR(2), 
    city VARCHAR(40), 
    accentCity VARCHAR(40), 
    region INT, 
    population INT, 
    latitude FLOAT, 
    longitude FLOAT
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ","
    LOCATION '/tmp/arsen/cities'
    TBLPROPERTIES ("skip.header.line.count"="1");
/*Внешняя таблица, которая смотрит в директорию с данными в файле о городах (если информация хранится в файле). Используем ее для заполнения данных в основной таблице с партициями. */

CREATE TABLE IF NOT EXISTS bandarenka_staging.cities (
    iso2_country VARCHAR(2), 
    city VARCHAR(40), 
    accentCity VARCHAR(40), 
    region INT, 
    population INT, 
    latitude FLOAT, 
    longitude FLOAT
    )
    PARTITIONED BY (file_date DATE)
    STORED AS ORC;
/* Примером заполнения таблицы для данных полученых 1 ноября может быть:
INSERT INTO TABLE bandarenka_staging.cities partition(file_date='2022-11-01') SELECT * FROM bandarenka_staging.cities_incr;
Теперь файл с данными можно удалить из директории.
При поступлении новых данных создаем новую партицию соответствующей даты. Старую при необходимости удаляем.*/

CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.countries_incr (
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
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    LOCATION '/tmp/arsen/countries'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE TABLE IF NOT EXISTS bandarenka_staging.countries (
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
    )
    PARTITIONED BY (file_date DATE)
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde';
/*Алгоритм заполнения таблицы аналогичен примеру с таблицей cities
INSERT INTO TABLE bandarenka_staging.countries PARTITION (file_date='2022-11-01') SELECT * FROM bandarenka_staging.countries_incr
Файл из директории внешней таблицы можно удалять*/

CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.capital (
    iso2_country VARCHAR(2), 
    capital VARCHAR(40)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/arsen/capital'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.continent (
    iso2_country VARCHAR(2), 
    continent_code VARCHAR(2)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/arsen/continent'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.currency (
    iso2_country VARCHAR(2), 
    currency_code VARCHAR(3)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/arsen/currency'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.iso3 (
    iso2_country VARCHAR(2), 
    iso3_country VARCHAR(3)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/arsen/iso3'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.names (
    iso2_country VARCHAR(2), 
    country_name VARCHAR(40)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/arsen/names'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.phone (
    iso2_country VARCHAR(2), 
    phone_code VARCHAR(10)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/arsen/phone'
    TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS bandarenka_staging.nobel_laureates (
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
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    LOCATION '/tmp/arsen/nobel'
    TBLPROPERTIES ("skip.header.line.count"="1");/*Создаем внешнюю таблицу, в которую будут автоматически добавляться строки из приходящих в папку дельт (исходя из предложенного в задании допущения)*/
 CREATE TABLE IF NOT EXISTS bandarenka_staging.nobel_laureates_orc STORED AS ORC AS SELECT * FROM bandarenka_staging.nobel_laureates;   
 
 Далее создаем снежинку и датасет с помощью Spark:

%spark.pyspark
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import HiveContext
hc = HiveContext(sc)

# Загружаем датафрейм из таблицы и меняем формат записи некоторых стран и городов. Т.к. есть города и страны с двумя названиями (старое и актуальное), разделим их и запишем в отдельные колонки. Также изменим формат записи некоторых стран и городов, чтобы совпадали их названия в других таблицах.
d = {'Trinidad' : 'Trinidad and Tobago', 'Guadeloupe Island' : 'Guadeloupe', 'Republic of Macedonia' : 'Macedonia', "People's Republic of China" : 'China', 'frankfurt-on-the-main' : 'frankfurt'} # Словарь для замены названий стран и городов
df_laureate_info = spark.read.format('ORC').load("/apps/hive/warehouse/bandarenka_staging.db/nobel_laureates_orc")
df_laureate_info = df_laureate_info.withColumn('birth_city', F.lower(df_laureate_info.birth_city)).drop(df_laureate_info.birth_city)
df_laureate_info = df_laureate_info.withColumn("current_country_name", F.regexp_extract(df_laureate_info.birth_country, r"\(([^()]+)\)$", 1)).replace('', None)
df_laureate_info = df_laureate_info.withColumn('current_birth_country_name', F.coalesce(df_laureate_info.current_country_name, df_laureate_info.birth_country)).drop(df_laureate_info.current_country_name)
df_laureate_info = df_laureate_info.withColumn("original_birth_country_name", F.split(df_laureate_info.birth_country, "\(").getItem(0))
df_laureate_info = df_laureate_info.withColumn("original_birth_country_name", F.trim(df_laureate_info.original_birth_country_name)).drop(df_laureate_info.original_birth_country_name)
df_laureate_info = df_laureate_info.withColumn("birth_state", F.split(df_laureate_info.birth_city, ",").getItem(1))
df_laureate_info = df_laureate_info.withColumn("birth_city", F.split(df_laureate_info.birth_city, ",").getItem(0)).drop(df_laureate_info.birth_city)
df_laureate_info = df_laureate_info.withColumn("birth_city", F.trim(df_laureate_info.birth_city)).drop(df_laureate_info.birth_city)
df_laureate_info = df_laureate_info.withColumn("original_birth_city_name", F.split(df_laureate_info.birth_city, "\(").getItem(0))
df_laureate_info = df_laureate_info.withColumn("original_birth_city_name", F.trim(df_laureate_info.original_birth_city_name)).drop(df_laureate_info.original_birth_city_name)
df_laureate_info = df_laureate_info.withColumn("current_city_name", F.regexp_extract(df_laureate_info.birth_city, r"\(([^()]+)\)$", 1)).replace('', None)
df_laureate_info = df_laureate_info.withColumn('current_birth_city_name', F.coalesce(df_laureate_info.current_city_name, df_laureate_info.birth_city)).drop(df_laureate_info.current_city_name)
df_laureate_info = df_laureate_info.drop("birth_country", "birth_city", "year", "category", "prize", "motivation", "prize_share", "organization_city", "organization_country")
df_laureate_info = df_laureate_info.replace(d)
df_laureate_info.write.saveAsTable("bandarenka_step5.laureate_info", format='ORC', mode='overwrite')

w = Window.orderBy('year')
df_nobel = spark.sql("SELECT laureate_id, year FROM bandarenka_staging.nobel_laureates_orc")
df_nobel = df_nobel.withColumn('prize_id', F.row_number().over(w)) # Добавляем колонку с id для каждой награды, упорядочив по году выдачи 
df_nobel.write.saveAsTable("bandarenka_step5.nobel", format='ORC', mode='overwrite')

df_cities = hc.sql("SELECT iso2_country, city, population city_population, latitude, longitude FROM bandarenka_staging.cities")
df_cities = df_cities.withColumn('city_id', F.monotonically_increasing_id())
df_cities.write.saveAsTable("bandarenka_step5.cities", format='ORC', mode='overwrite')

df_organization_info = hc.sql("SELECT organization_name, organization_city, organization_country FROM bandarenka_staging.nobel_laureates_orc")
df_organization_info = df_organization_info.distinct()
df_organization_info.write.saveAsTable("bandarenka_step5.organization_info", format='ORC', mode='overwrite')

# Меняем формат записи некоторых стран, чтобы можно было джойнить с другими таблицами
dc = {'Bosnia & Herzegovina' : 'Bosnia and Herzegovina', 'Korea, South' : 'South Korea', 'United States' : 'United States of America', 'Trinidad & Tobago' : 'Trinidad and Tobago', 'Burma' : 'Myanmar'}
df_countries = hc.sql("SELECT country, region, population, area, birthrate, deathrate, climate, literacy FROM bandarenka_staging.countries")
df_countries = df_countries.replace(dc)
df_countries.write.saveAsTable("bandarenka_step5.countries", format='ORC', mode='overwrite')

df_prize_info = hc.sql("SELECT prize, category, motivation, prize_share, year FROM bandarenka_staging.nobel_laureates_orc")
w = Window.orderBy('year')
df_prize_info = df_prize_info.withColumn('prize_id', F.row_number().over(w))# Добавляем колонку с id для каждой награды, упорядочив по году выдачи. Сортировка такая же как в таблице nobel выше, соответственно id наград будут совпадать
df_prize_info = df_prize_info.drop("year")
df_prize_info.write.saveAsTable("bandarenka_step5.prize_info", format='ORC', mode='overwrite')

Собираем датасет (также в Spark):

query = "SELECT n.prize_id, n.laureate_id, n.year award_year, li.full_name, li.current_birth_country_name, li.birth_date, li.death_date, li.laureate_type, li.organization_name, li.current_birth_city_name, li.death_city, li.sex, pi.prize prize_name, pi.prize_share, pi.category, pi.motivation, ct.city_population, cntr.country_population, cntr.region country_region, cntr.area country_area, cntr.literacy country_literacy, cntr.climate, cntr.birthrate, cntr.deathrate, oi.organization_country "

query2 = "FROM bandarenka_step4.nobel as n LEFT JOIN bandarenka_step4.laureate_info as li ON n.laureate_id = li.laureate_id LEFT JOIN bandarenka_step4.prize_info as pi ON n.prize_id = pi.prize_id LEFT JOIN bandarenka_step4.cities as ct ON li.current_birth_city_name = ct.city LEFT JOIN bandarenka_step4.countries as cntr ON li.current_birth_country_name = cntr.country LEFT JOIN bandarenka_step4.organization_info as oi ON li.organization_name = oi.organization_name"

dataset = hc.sql(query+query2)
dataset.distinct().write.saveAsTable("bandarenka_step5.dataset", format='ORC', mode='overwrite')    
