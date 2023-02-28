/* Задание 4.1 */
SELECT a.city,
       count(a.airport_code)
FROM dst_project.airports AS a
GROUP BY a.city
HAVING count(a.airport_code)>1;

/* Задание 4.2 */
-- Вопрос 1.
SELECT count(DISTINCT f.status)
FROM dst_project.flights AS f;
-- Вопрос 2.
SELECT count(f.flight_id)
FROM dst_project.flights AS f
WHERE f.status = 'Departed';
-- Вопрос 3.
SELECT count(DISTINCT s.seat_no)
FROM dst_project.seats AS s
WHERE s.aircraft_code = '773';
-- Вопрос 4.
SELECT count(f.status)
FROM dst_project.flights AS f
WHERE f.status = 'Arrived'
  AND f.actual_arrival BETWEEN '2017-4-1'::date AND '2017-9-1'::date;

/* Задание 4.3 */
-- Вопрос 1.
SELECT count(f.status)
FROM dst_project.flights AS f
WHERE f.status = 'Cancelled'
-- Вопрос 2.
SELECT count(a.model) "Amount",
       'Boeing' "Model"
FROM dst_project.aircrafts AS a
WHERE a.model like '%Boeing%'
UNION ALL
SELECT count(a.model),
       'Sukhoi'
FROM dst_project.aircrafts a
WHERE a.model like '%Sukhoi%'
UNION ALL
SELECT count(a.model),
       'Airbus'
FROM dst_project.aircrafts a
WHERE a.model like '%Airbus%'
-- Вопрос 3.
SELECT 'Europe' "Zone",
                count(ar.timezone) "Amount"
FROM dst_project.airports AS ar
WHERE ar.timezone like '%Europe%'
UNION ALL
SELECT 'Asia',
       count(ar.timezone)
FROM dst_project.airports AS ar
WHERE ar.timezone like '%Asia%'
UNION ALL
SELECT 'All',
       count(ar.airport_code)
FROM dst_project.airports AS ar
ORDER BY 2 DESC
-- Вопрос 4.
select
    f.flight_id, f.actual_arrival-f.scheduled_arrival "Delay" 
from
    dst_project.flights as f
where f.actual_arrival is not null
order by 2 desc
limit 1

/* Задание 4.4 */
-- Вопрос 1.
SELECT min(f.scheduled_departure)
FROM dst_project.flights AS f
-- Вопрос 2.
SELECT extract(epoch
               FROM max(f.scheduled_arrival-f.scheduled_departure))/60
FROM dst_project.flights AS f
-- Вопрос 3.
SELECT f.scheduled_arrival-f.scheduled_departure flight_lasts,
       f.departure_airport,
       f.arrival_airport
FROM dst_project.flights AS f
ORDER BY 1 DESC
LIMIT 1
-- Вопрос 4.
SELECT extract(epoch
               FROM avg(x.flight_lasts))/60
FROM
  (SELECT f.scheduled_arrival-f.scheduled_departure flight_lasts,
          f.departure_airport,
          f.arrival_airport
   FROM dst_project.flights AS f) x

/* Задание 4.5 */
-- Вопрос 1.
SELECT s.fare_conditions,
       count(DISTINCT s.seat_no)
FROM dst_project.seats s
GROUP BY 1
ORDER BY 2 DESC
-- Вопрос 2.
select min(b.total_amount)
from dst_project.bookings b
-- Вопрос 3.
SELECT *
FROM dst_project.tickets t
JOIN dst_project.boarding_passes b ON t.ticket_no = b.ticket_no
WHERE t.passenger_id = '4313 788533'

/* Задание 5.1 */
-- Вопрос 1.
SELECT count(f.flight_id)
FROM dst_project.airports AS ar
JOIN dst_project.flights f ON ar.airport_code = f.arrival_airport
WHERE ar.city = 'Anapa'
  AND extract(YEAR
              FROM f.actual_arrival) = 2017 --486
-- Вопрос 2.
SELECT count(f.flight_id)
FROM dst_project.airports AS ar
JOIN dst_project.flights f ON ar.airport_code = f.departure_airport
WHERE ar.city = 'Anapa'
  AND extract(YEAR
              FROM f.actual_departure) = 2017
  AND extract(MONTH
              FROM f.actual_departure) in (12,
                                           1,
                                           2) --127
-- Вопрос 3.
SELECT count(f.flight_id)
FROM dst_project.airports AS ar
JOIN dst_project.flights f ON ar.airport_code = f.departure_airport
WHERE ar.city = 'Anapa'
  AND f.status = 'Cancelled' --1
-- Вопрос 4.
SELECT count(f.flight_id)
FROM dst_project.airports AS ar
JOIN dst_project.flights f ON ar.airport_code = f.departure_airport
WHERE ar.city = 'Anapa'
  AND f.arrival_airport not in
    (SELECT f.arrival_airport
     FROM dst_project.airports AS ar
     JOIN dst_project.flights f ON ar.airport_code = f.arrival_airport
     WHERE ar.city = 'Moscow')
-- Вопрос 5.
SELECT s.aircraft_code,
       a.model,
       count(DISTINCT s.seat_no)
FROM dst_project.airports AS ar
JOIN dst_project.flights f ON ar.airport_code = f.departure_airport
JOIN dst_project.seats s ON s.aircraft_code = f.aircraft_code
JOIN dst_project.aircrafts a ON a.aircraft_code = s.aircraft_code
WHERE ar.city = 'Anapa'
GROUP BY s.aircraft_code,
         a.model
ORDER BY 3 DESC

/* Итоговый запрос */
WITH b AS
  (SELECT f.flight_id,
          sum(b.total_amount) total_booking_price
   FROM dst_project.tickets t
   LEFT JOIN dst_project.bookings b ON b.book_ref = t.book_ref
   LEFT JOIN dst_project.ticket_flights tf ON tf.ticket_no = t.ticket_no
   LEFT JOIN dst_project.flights f ON f.flight_id = tf.flight_id
   GROUP BY 1)
SELECT f.flight_id,
       f.scheduled_departure departure,
       f.scheduled_arrival arrival,
       f.departure_airport,
       f.arrival_airport,
       f.aircraft_code,
       tfe.Economy_sold,
       tfc.Comfort_sold,
       tfb.Business_sold,
       tf_te.price_eco_sold,
       tf_tb.price_bus_sold,
       tf_tt.price_total,
       ac.model aircraft_model,
       ac.range aircraft_range,
       sge.amount_eco_seats,
       sgb.amount_bus_seats,
       sg1.total_seats,
       b.total_booking_price,
       ap.city arrival_city,
       ap.longitude airport_longitude,
       ap.latitude airport_latitude,
       aaq_ap.anapa_long,
       aaq_ap.anapa_lat
FROM dst_project.flights f
LEFT JOIN
  (SELECT tf.flight_id,
          count(tf.fare_conditions) Economy_sold
   FROM dst_project.ticket_flights tf
   WHERE tf.fare_conditions = 'Economy'
   GROUP BY tf.flight_id) AS tfe ON tfe.flight_id = f.flight_id
LEFT JOIN
  (SELECT tf.flight_id,
          count(tf.fare_conditions) Comfort_sold
   FROM dst_project.ticket_flights tf
   WHERE tf.fare_conditions = 'Comfort'
   GROUP BY tf.flight_id) AS tfc ON tfc.flight_id = f.flight_id
LEFT JOIN
  (SELECT tf.flight_id,
          count(tf.fare_conditions) Business_sold
   FROM dst_project.ticket_flights tf
   WHERE tf.fare_conditions = 'Business'
   GROUP BY tf.flight_id) AS tfb ON tfb.flight_id = f.flight_id
LEFT JOIN
  (SELECT tf.flight_id,
          sum(tf.amount) price_eco_sold
   FROM dst_project.ticket_flights tf
   WHERE tf.fare_conditions = 'Economy'
   GROUP BY 1) AS tf_te ON tf_te.flight_id = f.flight_id
LEFT JOIN
  (SELECT tf.flight_id,
          sum(tf.amount) price_bus_sold
   FROM dst_project.ticket_flights tf
   WHERE tf.fare_conditions = 'Business'
   GROUP BY 1) AS tf_tb ON tf_tb.flight_id = f.flight_id
LEFT JOIN
  (SELECT tf.flight_id,
          sum(tf.amount) price_total
   FROM dst_project.ticket_flights tf
   GROUP BY 1) AS tf_tt ON tf_tt.flight_id = f.flight_id
LEFT JOIN dst_project.aircrafts ac ON ac.aircraft_code = f.aircraft_code
LEFT JOIN
  (SELECT DISTINCT s.aircraft_code,
                   count(DISTINCT s.seat_no) amount_eco_seats
   FROM dst_project.seats s
   WHERE s.fare_conditions = 'Economy'
   GROUP BY 1) AS sge ON sge.aircraft_code = f.aircraft_code
LEFT JOIN
  (SELECT DISTINCT s.aircraft_code,
                   count(DISTINCT s.seat_no) amount_bus_seats
   FROM dst_project.seats s
   WHERE s.fare_conditions = 'Business'
   GROUP BY 1) AS sgb ON sgb.aircraft_code = f.aircraft_code
LEFT JOIN
  (SELECT DISTINCT s.aircraft_code,
                   count(DISTINCT s.seat_no) total_seats
   FROM dst_project.seats s
   GROUP BY 1) AS sg1 ON sg1.aircraft_code = f.aircraft_code
LEFT JOIN b ON b.flight_id = f.flight_id
LEFT JOIN dst_project.airports AS ap ON ap.airport_code = f.arrival_airport
LEFT JOIN
  (SELECT ap.airport_code,
          ap.longitude anapa_long,
          ap.latitude anapa_lat
   FROM dst_project.airports ap
   WHERE ap.airport_code = 'AAQ') AS aaq_ap ON aaq_ap.airport_code = f.departure_airport
WHERE f.departure_airport = 'AAQ'
  AND (date_trunc('month', f.scheduled_departure) in ('2017-01-01',
                                                      '2017-02-01',
                                                      '2017-12-01'))
  AND f.status not in ('Cancelled')