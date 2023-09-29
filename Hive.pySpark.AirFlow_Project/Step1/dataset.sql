CREATE TABLE dataset (prize_id INT, prize_name VARCHAR, laureat_name VARCHAR, sex VARCHAR,
					 laureat_type VARCHAR, birth_country VARCHAR, birth_city VARCHAR,
					 award_year INT, prize_category VARCHAR, birth_date DATE,
					 death_date DATE, birth_city_population NUMERIC, birth_country_literacy NUMERIC,
					 prize_share VARCHAR, laureat_in_organization BOOL, birth_country_population NUMERIC,
					 prize_motivation TEXT);
/* В датасете собрана основная информация о лауреате и о награде; также дана сопутствующая информация
о стране и городе откуда лауреат родом, есть колонка с булевым типом о принадлежности лауреата какой-либо
организации. Некоторая информация умышленно не была добавлена в датасет из-за большого кол-ва пропусков*/
