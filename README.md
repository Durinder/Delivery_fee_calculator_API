# Delivery Fee Calculator
Preliminary Assignment for Wolt Summer 2022 Backend Engineering Internships Position

This is an HTTP API for calculating delivery fees.

## Specifics
API accepts requests with JSON formatted payloads and outputs the calculated delivery fee in JSON in the response payload.

API is built with FastAPI in Python.
### Request format
```
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}
```
### Response format
```
{"delivery_fee": 710}
```
### Rules for calculating a delivery fee
- If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
- A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
  - Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  - Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  - Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
- If the number of items is five or more, an additional 50 cent surcharge is added for each item above four
  - Example 1: If the number of items is 4, no extra surcharge
  - Example 2: If the number of items is 5, 50 cents surcharge is added
  - Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
- The delivery fee can never be more than 15€, including possible surcharges.
- The delivery is free (0€) when the cart value is equal or more than 100€.
- During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.1x. However, the fee still cannot be more than the max (15€).
## Structuring
config.json contains constants from the rules stated above that are loaded and cached by the API with the first request sent to the endpoint /delivery_fee.

api.py contains validation for inputs and on requests to /delivery_fee it calls calculate_delivery_fee.py with two class instances as arguments, order with input values and rules loaded from config.json. It also returns the json response for requests.

calculate_delivery_fee.py contains the real calculation with order values and rules and returns the delivery fee as an integer.

tests/ directory contains test_api.py with many test cases that are run with pytest as well as the requests/ directory with test cases as .rest files.

## Prerequisites
Dependancies can be installed with:

```pip install -r requirements.txt```

Alternatively install the following:

```python -m pip install fastapi uvicorn[standard]```

Start server in development mode:

```uvicorn api.api:app --reload```

By default the server runs on http://127.0.0.1.:8000

## Usage
Send HTTP PUT requests to the single endpoint /delivery_fee

Example request:

```curl -X PUT 127.0.0.1:8000/delivery_fee -H 'Content-Type: application/json' -d '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}'```

### Testing
run automated testing with either

```pytest```

or

```python -m pytest```

tests/requests folder contains .rest files for additional testing
