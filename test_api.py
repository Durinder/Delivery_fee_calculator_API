from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_example():
    response = client.post("/delivery_fee",
        json={
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2021-10-12T13:00:00Z"
		}
	)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}