-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Used to see all crimes commited to find the robbery information
SELECT * FROM crime_scene_reports;

-- Used to find all interviews that mention a bakery
SELECT * FROM interviews WHERE transcript LIKE "%bakery%";

-- Used to find all security footage during the crime
SELECT * FROM bakery_security_logs JOIN people ON bakery_security_logs.license_plate = people.license_plate WHERE year = 2023 AND month = 7 AND day = 28 ORDER BY name;

-- Used to find all ATM transaction during the crime as described by the second interviewee and joining it with the information of the people
SELECT * FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Used to find all phone calls on 7/28/23 less than a minute
SELECT * FROM phone_calls JOIN people ON phone_calls.caller = people.phone_number WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;

-- Used to find all flights the day after the crime
SELECT * FROM flights WHERE year = 2023 AND month = 7 AND day = 29;

-- Used to find all passengers on the flight and their names
SELECT * FROM passengers JOIN people ON passengers.passport_number = people.passport_number WHERE flight_id = 36;




-- Possible suspects from all previous queries
-- Bruce or Taylor


-- Checking Taylor
-- Used to check who Taylor called
SELECT * FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = 'Taylor');

-- Used to check whose phone number the one Taylor called is
SELECT * FROM people WHERE phone_number = '(676) 555-6554';

-- Taylor is not the robber


-- Checking Bruce
-- Used to check who Bruce called
SELECT * FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce');

-- Used to check whose phone number the one Bruce called is
SELECT * FROM people WHERE phone_number = '(375) 555-8161';

-- Used to check where Bruce went
SELECT * FROM airports WHERE id = 4;


-- Conclusion: Bruce is the robber, Robin is the accomplice, and New York City is the city to which Bruce escaped to

