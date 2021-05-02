# Overview
Restful api for car rental system.

Running environment:
- python 3.8, Flask, MySQL, Redis, Docker, pytest

#### Usage cases implementation
- Car registration
    - Check car availability and register a car by providing the car name, category,
    customer name, birthday and the number of days to book
- Car return
    - Return the rental car by providing a booking id and the mileage at return.
- Cancel booking
    - Booking can be canceled within the 15 minutes after registered by providing the booking id

#### Main challenges
1. Data misalignment / data disorder / data inconsistency
2. Proper architecture
3. Relational tables design
4. Proper response of restful api for exceptions

This solution is able to handle the above challenges.
1. Redis queue is utilized to prevent data inconsistency problem which may caused by concurrency, i.e when people want
to register the same type of car nearly at the same time but the number of available cars can not serve the total amount
of people that are booking.
2. This solution comprises API, MySQL, and Redis. MySQL is used as transactional database for data persistence, Redis is
used as a queue service, in which contents are produced and consumed by the API.
3. 2 tables will be created, which are `car` and `booking` , they are used for properly storing cars and booking 
information respectively.
4. This feature considers response messages and status codes for exceptions requests as well

This solution also covers these features:
- Dockerization
- Functional testing
- API middleware
- Logging
- Command line interface utilities that interact with application

## Starting application
I assume you have docker and Postman (or any other equivalent) setup.

Building images
```bash
docker-compose build --no-cache --force-rm
```
Bring up containers
```bash
docker-compose up
```
Open a new terminal, create tables and prepare data

```bash
docker-compose run api python manager.py create_tables
docker-compose run api python manager.py flush_redis_keys # Optional
docker-compose run api python manager.py load_data
```

Start your Postman or your terminal, make `POST` request to the `register`, `car_return`, and `cancel` endpoint.
- register endpoint path: http://0.0.0.0:5001/api/v1/register
- return car endpoint path: http://0.0.0.0:5001/api/v1/return
- cancel car endpoint path: http://0.0.0.0:5001/api/v1/cancel

Here are some examples of json parameters, if you want to reproduce, it is very recommended that you can use Postman,
and open 3 tabs with the above 3 links, and copy paste the following parameters and send POST requests. It is also very
convenient for you to modify parameters and test the restful api in different sequences. 

Sample parameters to register a car
```json
{
	"name": "Volvo S9",
	"car_category": "premium",
	"customer": "Jessica",
	"birthday": "1994-06-17",
	"rental_days": 2
}
```
Response of successful booking
```json
{
    "booking_id": "20210503050132-IISA",
    "category": "premium",
    "customer": {
        "birthday": "1994-06-17",
        "name": "Jessica"
    },
    "name": "Volvo S9",
    "nr": "BUE325",
    "rental": {
        "rental_days": 2,
        "start_date": "2021-05-03"
    }
}
```
Pick the booking id `20210502191746-IJJS` and return the car with the following json parameter
```json
{
	"booking_id": "20210503050132-IISA",
	"mileage": 370
}
```
then will get the following response
```json
{
    "booking_id": "20210503050132-IISA",
    "car": {
        "category": "premium",
        "current_mileage": 370,
        "used_mileage": 55.5
    },
    "status": "success",
    "total_price": 675
}
```

To cancel a booking, booking another car again with the same parameter:
```json
{
    "booking_id": "20210503050648-ICIC",
    "category": "premium",
    "customer": {
        "birthday": "1994-06-17",
        "name": "Jessica"
    },
    "name": "Volvo S9",
    "nr": "BVE355",
    "rental": {
        "rental_days": 2,
        "start_date": "2021-05-03"
    }
}
```
and cancel it with the booking id
```json
{
	"booking_id": "20210503050648-ICIC"
}
```
and get this response:
```json
{
    "booking_id": "20210503050648-ICIC",
    "status": "Canceled"
}
```
Please note that I am using this query to prepare the original data, so here is also convenient for you to know which
cars are available at the beginning
```mysql-psql
        INSERT INTO test.car(name, number, category, available, mileage)
        VALUES  ("Audi A5", "BEW345", "premium", true, 212.6),
                ("Audi A3", "WWW457", "compact", true, 175.4),
                ("Audi A3", "OPD557", "compact", true, 145.4),
                ("BMW X1", "RTW555", "compact", true, 155.4),
                ("Audi A7", "NMN234", "premium", true, 123.7),
                ("Volvo S9", "BUE325", "premium", true, 314.5),
                ("Volvo S9", "BVE355", "premium", true, 344.5),
                ("Volvo S9", "BUR724", "premium", true, 124.5),
                ("Volvo S9", "BHH727", "premium", true, 234.5),
                ("Mercedes benz vito", "IYG989", "minivan", true, 93);
```

## Functional testing
```bash
docker-compose run api py.test tests/*
```