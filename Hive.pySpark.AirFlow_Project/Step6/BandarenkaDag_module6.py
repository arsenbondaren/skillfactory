import sys
sys.path.append('/usr/lib/spark/python')
sys.path.append('/usr/lib/spark/python/lib/py4j-0.10.7-src.zip')

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import HiveContext

from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.subdag_operator import SubDagOperator
import os, datetime
from datetime import date

DAG_NAME = 'BandarenkaLoadTables'

#Таблицы, которые будем копировать в кластер, сохраняем в переменную
Variable.set(DAG_NAME+"_TABLES","capital,continent,countries_of_the_world,currency,iso3,names,nobel-laureates,phone,worldcitiespop")

tableNames = Variable.get(DAG_NAME+"_TABLES")
sched = None
stDt = datetime.datetime(2022, 12, 8)

#Создадим подграф для переноса файлов в цикле
def SubDag(parent_dag_name, start_date, schedule_interval, tableName):
    
    dag = DAG('%s.%s'%(parent_dag_name, tableName), schedule_interval=schedule_interval, start_date=start_date )

    deleteTableCmd = f"""
    hdfs dfs -rm -r -f -skipTrash /tmp/air_arsen/{tableName}"""

    createFileCmd = f"""
    hdfs dfs -mkdir -p /tmp/air_arsen/{tableName}
    hdfs dfs -put -f /var/lib/zeppelin/arsen_json/{tableName}.csv /tmp/air_arsen/{tableName}/{tableName}.csv"""

    deleteTable = BashOperator(task_id = 'deleteTable', bash_command = deleteTableCmd, dag = dag)

    createFile = BashOperator(task_id = 'createFile', bash_command = createFileCmd, dag = dag)

    deleteTable >> createFile

    return dag

today = str(date.today())

#Создаем таблицы в Hive
createTablesCmd = f"""cat > arsen_script.txt <<EOF
CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.cities_incr (
    iso2_country VARCHAR(2), 
    city VARCHAR(40), 
    accentCity VARCHAR(40), 
    region INT, 
    population INT, 
    latitude FLOAT, 
    longitude FLOAT
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ","
    LOCATION '/tmp/air_arsen/worldcitiespop'
    TBLPROPERTIES ("skip.header.line.count"="1");
/*Внешняя таблица, которая смотрит в директорию с данными в файле о городах (если информация хранится в файле). Используем ее для заполнения данных в основной таблице с партициями. */

CREATE TABLE IF NOT EXISTS air_bandarenka_staging.cities (
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
/* Примером заполнения таблицы для данных полученых сегодня может быть:*/
INSERT INTO TABLE air_bandarenka_staging.cities partition(file_date='{today}') SELECT * FROM air_bandarenka_staging.cities_incr;

CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.countries_incr (
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
    LOCATION '/tmp/air_arsen/countries_of_the_world'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE TABLE IF NOT EXISTS air_bandarenka_staging.countries (
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
/*Алгоритм заполнения таблицы аналогичен примеру с таблицей cities*/
INSERT INTO TABLE air_bandarenka_staging.countries PARTITION (file_date='{today}') SELECT * FROM air_bandarenka_staging.countries_incr;
/*Файл из директории внешней таблицы можно удалять*/

CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.capital (
    iso2_country VARCHAR(2), 
    capital VARCHAR(40)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/air_arsen/capital'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.continent (
    iso2_country VARCHAR(2), 
    continent_code VARCHAR(2)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/air_arsen/continent'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.currency (
    iso2_country VARCHAR(2), 
    currency_code VARCHAR(3)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/air_arsen/currency'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.iso3 (
    iso2_country VARCHAR(2), 
    iso3_country VARCHAR(3)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/air_arsen/iso3'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.names (
    iso2_country VARCHAR(2), 
    country_name VARCHAR(40)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/air_arsen/names'
    TBLPROPERTIES ("skip.header.line.count"="1");
CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.phone (
    iso2_country VARCHAR(2), 
    phone_code VARCHAR(10)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION '/tmp/air_arsen/phone'
    TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS air_bandarenka_staging.nobel_laureates (
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
    LOCATION '/tmp/air_arsen/nobel-laureates'
    TBLPROPERTIES ("skip.header.line.count"="1");
/*Создаем внешнюю таблицу, в которую будут автоматически добавляться строки из приходящих в папку дельт (исходя из предложенного в задании допущения)*/

CREATE TABLE IF NOT EXISTS air_bandarenka_staging.nobel_laureates_orc STORED AS ORC AS SELECT * FROM air_bandarenka_staging.nobel_laureates;
EOF
beeline -u jdbc:hive2://10.93.1.9:10000 hive eee -f arsen_script.txt >>arsen_hive_stdout.txt 2>arsen_hive_stderr.txt"""

createDatabaseCmd = """cat > arsen_script.txt <<EOF
CREATE DATABASE IF NOT EXISTS air_bandarenka_staging;
CREATE DATABASE IF NOT EXISTS air_bandarenka_snowball;
EOF
beeline -u jdbc:hive2://10.93.1.9:10000 hive eee -f arsen_script.txt >>arsen_hive_stdout.txt 2>arsen_hive_stderr.txt"""

def makeSnowball():
    """Функция, создающая снежинку из сохраненных данных в Hive"""
    
    os.environ["JAVA_HOME"] = "/usr"
    os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
    os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
    
    spark = SparkSession.builder.master("yarn-client").appName("spark_airflow").config("hive.metastore.uris", "thrift://10.93.1.9:9083").enableHiveSupport().getOrCreate()

    hc = HiveContext(spark._sc)

# Загружаем датафрейм из таблицы и меняем формат записи некоторых стран и городов. Т.к. есть города и страны с двумя названиями (старое и актуальное), разделим их и запишем в отдельные колонки. Также изменим формат записи некоторых стран и городов, чтобы совпадали их названия в других таблицах.
    d = {'Trinidad' : 'Trinidad and Tobago', 'Guadeloupe Island' : 'Guadeloupe', 'Republic of Macedonia' : 'Macedonia', "People's Republic of China" : 'China', 'frankfurt-on-the-main' : 'frankfurt'} # Словарь для замены названий стран и городов
    df_laureate_info = spark.read.format('ORC').load("/apps/hive/warehouse/air_bandarenka_staging.db/nobel_laureates_orc")
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
    df_laureate_info.write.saveAsTable("air_bandarenka_snowball.laureate_info", format='ORC', mode='overwrite')

    w = Window.orderBy('year')
    df_nobel = spark.sql("SELECT laureate_id, year FROM air_bandarenka_staging.nobel_laureates_orc")
    df_nobel = df_nobel.withColumn('prize_id', F.row_number().over(w)) # Добавляем колонку с id для каждой награды, упорядочив по году выдачи 
    df_nobel.write.saveAsTable("air_bandarenka_snowball.nobel", format='ORC', mode='overwrite')

    df_cities = hc.sql("SELECT iso2_country, city, population city_population, latitude, longitude FROM air_bandarenka_staging.cities")
    df_cities = df_cities.withColumn('city_id', F.monotonically_increasing_id())
    df_cities.write.saveAsTable("air_bandarenka_snowball.cities", format='ORC', mode='overwrite')

    df_organization_info = hc.sql("SELECT organization_name, organization_city, organization_country FROM air_bandarenka_staging.nobel_laureates_orc")
    df_organization_info = df_organization_info.distinct()
    df_organization_info.write.saveAsTable("air_bandarenka_snowball.organization_info", format='ORC', mode='overwrite')

    # Меняем формат записи некоторых стран, чтобы можно было джойнить с другими таблицами
    dc = {'Bosnia & Herzegovina' : 'Bosnia and Herzegovina', 'Korea, South' : 'South Korea', 'United States' : 'United States of America', 'Trinidad & Tobago' : 'Trinidad and Tobago', 'Burma' : 'Myanmar'}
    df_countries = hc.sql("SELECT country, region, population, area, birthrate, deathrate, climate, literacy FROM air_bandarenka_staging.countries")
    df_countries = df_countries.replace(dc)
    df_countries.write.saveAsTable("air_bandarenka_snowball.countries", format='ORC', mode='overwrite')

    df_prize_info = hc.sql("SELECT prize, category, motivation, prize_share, year FROM air_bandarenka_staging.nobel_laureates_orc")
    w = Window.orderBy('year')
    df_prize_info = df_prize_info.withColumn('prize_id', F.row_number().over(w))# Добавляем колонку с id для каждой награды, упорядочив по году выдачи. Сортировка такая же как в таблице nobel выше, соответственно id наград будут совпадать
    df_prize_info = df_prize_info.drop("year")
    df_prize_info.write.saveAsTable("air_bandarenka_snowball.prize_info", format='ORC', mode='overwrite')
    
    spark.stop()

def makeDataset():
    """Функция для создания датасета"""

    os.environ["JAVA_HOME"] = "/usr"
    os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
    os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
    #os.environ["PYSPARK_SUBMIT_ARGS"] = """--driver-class-path /usr/share/java/mysql-connector-java.jar --jars /usr/share/java/mysql-connector-java.jar pyspark-shell"""
    
    spark = SparkSession.builder.master("yarn-client").appName("spark_airflow").config("hive.metastore.uris", "thrift://10.93.1.9:9083").enableHiveSupport().getOrCreate()

    hc = HiveContext(spark._sc)

    query = "SELECT n.prize_id, n.laureate_id, n.year award_year, li.full_name, li.current_birth_country_name, li.birth_date, li.death_date, li.laureate_type, li.organization_name, li.current_birth_city_name, li.death_city, li.sex, pi.prize prize_name, pi.prize_share, pi.category, pi.motivation, ct.city_population, cntr.population country_population, cntr.region country_region, cntr.area country_area, cntr.literacy country_literacy, cntr.climate, cntr.birthrate, cntr.deathrate, oi.organization_country "

    query2 = "FROM air_bandarenka_snowball.nobel as n LEFT JOIN air_bandarenka_snowball.laureate_info as li ON n.laureate_id = li.laureate_id LEFT JOIN air_bandarenka_snowball.prize_info as pi ON n.prize_id = pi.prize_id LEFT JOIN air_bandarenka_snowball.cities as ct ON li.current_birth_city_name = ct.city LEFT JOIN air_bandarenka_snowball.countries as cntr ON li.current_birth_country_name = cntr.country LEFT JOIN air_bandarenka_snowball.organization_info as oi ON li.organization_name = oi.organization_name"

    dataset = hc.sql(query+query2)
    dataset.distinct().write.saveAsTable("air_bandarenka_snowball.dataset", format='ORC', mode='overwrite')
    
    spark.stop()

mainDag = DAG(dag_id=DAG_NAME, schedule_interval=sched, start_date=stDt, catchup=False)

createTables = BashOperator(task_id= 'createTables', bash_command = createTablesCmd, dag = mainDag)

createDatabase = BashOperator(task_id = 'createDatabase', bash_command = createDatabaseCmd, dag = mainDag)

createSnowball = PythonOperator( task_id='createSnowball', python_callable=makeSnowball, dag=mainDag)

createDataset = PythonOperator( task_id='createDataset', python_callable=makeDataset, dag=mainDag)

prevDag = createDatabase
for tab in tableNames.split(","):
    nextDag = SubDagOperator( subdag=SubDag(DAG_NAME,stDt,sched,tab),task_id=tab, dag=mainDag, trigger_rule='all_done' )
    prevDag >> nextDag
    prevDag = nextDag
prevDag >> createTables >> createSnowball >> createDataset