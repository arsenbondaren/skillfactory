CREATE TABLE public.nobel (prize_id INT, laureat_id INT, award_year INT, 
						  PRIMARY KEY(prize_id)); /* Таблица фактов, в ней отражен идентификатор награды, идентификатор лауреата и год вручения.*/

CREATE TABLE public.laureat_info ("id" INT, full_name VARCHAR,
								 country VARCHAR, bitrh_date DATE, 
								 death_date DATE, "type" VARCHAR, organization TEXT,
								 birth_city VARCHAR, sex VARCHAR, death_city VARCHAR); /* Таблица с информацией о лауреате, связана с таблицей фактов через id лауреата*/
								 
CREATE TABLE public.organization_info (organization_name TEXT, city VARCHAR,
                                      country VARCHAR); /* Таблица с информацией об организации которую представляет лауреат, связана с предыдущей по названию организации*/

CREATE TABLE public.cities (city_id INT, city_name VARCHAR, population INT,
                            country VARCHAR, latitude INT, longitude INT); /* Таблица с информацией о городах, связана с информацией о лауреате по названию города*/

CREATE TABLE public.countries ( country VARCHAR, population INT, region VARCHAR, birthrate INT,
							  deathrate INT, climate INT, literacy INT, area INT); /* Таблица с информацией по странам, связана с таблицей городов по названию страны*/

CREATE TABLE public.prize_info (prize_id INT, prize_name VARCHAR,
							    motivation TEXT, prize_share VARCHAR, category VARCHAR); /* Таблица с информацией касательно награды, связана с таблицей фактов через id награды*/
