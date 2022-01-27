from fastapi.testclient import TestClient

from api.api import app

client = TestClient(app)

# example test
def test_example():
    response = client.put("/delivery_fee",
    json = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2021-10-12T13:00:00Z"
		}
	)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}

# cart value tests
def test_example_cart_value_999():
	response = client.put("/delivery_fee",
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
	response = client.put("/delivery_fee",
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
	response = client.put("/delivery_fee",
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
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 10000,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 0}

# delivery distance tests
def test_example_delivery_distance_1499():
	response = client.put("/delivery_fee",
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
	response = client.put("/delivery_fee",
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
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 1501,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 610}


def test_example_maximum_delivery_fee():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 22355,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 1500}	

# number of items tests
def test_example_number_of_items_5():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 5,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 760}

def test_example_number_of_items_10():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 10,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 1010}

# time tests
def test_example_timezone_plus_2_hours():
	response = client.put("/delivery_fee",
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
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-15T15:05:24Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 781}

def test_example_timezone_plus_microseconds():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-03-12T13:00:00.012345Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 710}

# misc tests
def test_float_in_input():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790.3,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 200
	assert response.json() == {"delivery_fee": 710}

# error handling tests
def test_error_extra_field():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"extra": "data",
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error.extra"

def test_error_missing_field():
	response = client.put("/delivery_fee",
	json = {
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error.missing"

def test_error_wrong_field_name():
	response = client.put("/delivery_fee",
	json = {
		"cart-value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error.missing" and response.json()['detail'][1]['type'] == "value_error.extra"

def test_error_incorrect_time_no_timezone():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-12-13T13:00:00"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error"

def test_error_incorrect_date():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-02-30T13:00:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error"

def test_error_incorrect_time_missing_seconds():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-12-13T13:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error"

def test_error_incorrect_time_badly_formatted_microseconds():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 4,
		"time": "2021-03-12T13:00:00.01234Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error"

def test_error_no_items():
	response = client.put("/delivery_fee",
	json = {
		"cart_value": 790,
		"delivery_distance": 2235,
		"number_of_items": 0,
		"time": "2021-10-12T13:00:00Z"
		}
	)
	assert response.status_code == 422
	assert response.json()['detail'][0]['type'] == "value_error"