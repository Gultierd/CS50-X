-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports; -- searching for the correct place and date from the reports, (3 witnesses, duck was stolen, bakery mentioned; 10:15 am)
SELECT name, transcript FROM interviews WHERE year = 2024 AND month = 7 AND day = 28; -- Getting interviews from those 3 witnesses
-- car in the bakery parking lot driving off, Emma's bakery, ATM on Leggett Street where thief withdrew money, phone call and earliest flight tomorrow
SELECT name FROM people WHERE id IN (SELECT person_id FROM atm_transactions JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number WHERE atm_location = "Leggett Street" AND year = 2024 AND month = 7 AND day = 28 AND transaction_type = "withdraw"); -- investigating ATM
-- getting names of suspects from withdrawals in possible time frame
SELECT activity, license_plate, hour, minute FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28; -- running plates from the scene
-- possible plates: 5P2BI95, 94KL13X, 6P58WS2, 4328GD8, G412CB7, L93JTIZ, 322W7JE, 0NTHK55
SELECT name FROM people WHERE license_plate IN ("5P2BI95", "94KL13X", "6P58WS2", "4328GD8", "G412CB7", "L93JTIZ", "322W7JE", "0NTHK55");
-- getting people from their plates - our current suspects
SELECT p1.name, p2.name FROM people AS p1 JOIN people AS p2 WHERE (p1.phone_number, p2.phone_number) IN (SELECT caller, receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE license_plate IN ("5P2BI95", "94KL13X", "6P58WS2", "4328GD8", "G412CB7", "L93JTIZ", "322W7JE", "0NTHK55")) AND year = 2024 AND month = 7 AND day = 28 AND duration < 60);
-- getting data on phone calls made that day by any of those suspects in search for accomplices
SELECT * FROM airports WHERE  id = (SELECT destination_airport_id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- getting data on the earliest flight the next day, from which we get the destination airport - LaGuardia Airport | New York City
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1));
-- names from passport numbers from that flight - among those people hides the thief
SELECT thief.name, accomplice.name FROM people AS thief JOIN people as accomplice
WHERE thief.name IN (SELECT name FROM people WHERE license_plate IN ("5P2BI95", "94KL13X", "6P58WS2", "4328GD8", "G412CB7", "L93JTIZ", "322W7JE", "0NTHK55"))
AND thief.name IN (SELECT name FROM people WHERE id IN (SELECT person_id FROM atm_transactions JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number WHERE atm_location = "Leggett Street" AND year = 2024 AND month = 7 AND day = 28 AND transaction_type = "withdraw"))
AND (thief.name, accomplice.name) IN (SELECT p1.name, p2.name FROM people AS p1 JOIN people AS p2 WHERE (p1.phone_number, p2.phone_number) IN (SELECT caller, receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE license_plate IN ("5P2BI95", "94KL13X", "6P58WS2", "4328GD8", "G412CB7", "L93JTIZ", "322W7JE", "0NTHK55")) AND year = 2024 AND month = 7 AND day = 28 AND duration < 60))
AND thief.name IN (SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1)))
-- getting potential pairs for thief and accomplice, combining previous clues - phone calls made that day, collected from license plates from the bakery parking lot, first flight the very next day and bank account from ATM transaction earlier
-- thief is bruce
