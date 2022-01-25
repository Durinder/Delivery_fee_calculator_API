from xml.etree.ElementInclude import include
from fastapi.testclient import TestClient
from pyparsing import rest_of_line

from api import app

client = TestClient(app)


def test_example():
    response = client.post("/delivery_fee",
    json = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2021-10-12T13:00:00Z"
		}
	)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}

def test_example_cart_value_999():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 999,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 501}

def test_example_cart_value_1000():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 1000,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 500}

def test_example_cart_value_9999():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 9999,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 500}

def test_example_cart_value_10000():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 10000,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 0}

def test_example_delivery_distance_1499():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 1499,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 510}

def test_example_delivery_distance_1500():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 1500,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 510}

def test_example_delivery_distance_1501():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 1501,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 610}

def test_example_timezone_plus_2_hours():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-03-12T13:00:00+02:00"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 710}

def test_example_friday_rush():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-15T15:05:24Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 781}

def test_float_in_input():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790.3,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 710}

def test_error_extra_field():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"extra": "data",
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json() == {"value_error"}

def test_error_incorrect_time_no_timezone():
	response = client.post("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-12-13T13:00:00"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error"