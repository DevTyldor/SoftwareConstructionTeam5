import pytest
import requests

# This file runs tests for all API endpoints of orders.

@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'gf38743yjf39kuf309fj8f30kvi908po39jv3uofjoi3',
        'unauthorized_key': 'd4s2a0b0a1n4a0l0y7t' # Custom key without post, put, delete access on orders but does have get permission
    }

def test_GET_order_by_id_regular(_data):
    url = _data['url'] + 'orders/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no order"


def test_POST_order_creation(_data):
    url = _data['url'] + 'orders'

    order = {
    "id": 999999,
    "client_id": 123,
    "order_date": "2025-03-05T04:42:29Z",
    "request_date": "2025-03-09T00:27:04Z",
    "reference": "ORD-000001",
    "customer_po_number": "PO-662159",
    "order_status": "Shipped",
    "shipping_notes": None,
    "warehouse_id": 2,
    "ship_to_client_id": 31,
    "bill_to_client_id": 87,
    "created_at": "2025-03-05T04:42:29Z",
    "updated_at": "2025-03-08T00:23:16Z"
  }

    response = requests.post(
        url,
        headers={'API_KEY': _data['api_key']},
        json=order
    )

    assert response.status_code == 201

    response = requests.get(_data['url'] + 'orders/999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is not None, "New order does not exist. Creation failed."


def test_PUT_order_update(_data):
    url = _data['url'] + 'orders/999999'

    order = {
    "id": 999999,
    "client_id": 123,
    "order_date": "2025-03-05T04:42:29Z",
    "request_date": "2025-03-09T00:27:04Z",
    "reference": "ORD-000001",
    "customer_po_number": "PO-662159",
    "order_status": "Delivered",
    "shipping_notes": None,
    "warehouse_id": 2,
    "ship_to_client_id": 31,
    "bill_to_client_id": 87,
    "created_at": "2025-03-05T04:42:29Z",
    "updated_at": "2025-03-08T00:23:16Z"
  }

    response = requests.put(
        url,
        headers={'API_KEY': _data['api_key']},
        json=order
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + 'orders/999999', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "API returned no order"
    
    assert response_json["order_status"] == "Delivered", "Order contains old order status. Update failed."


def test_PUT_order_items_update(_data):
    url = _data['url'] + 'orders/1/items'

    order = [{
    "item_id": 9999,
    "amount": 24
  }]

    response = requests.put(
        url,
        headers={'API_KEY': _data['api_key']},
        json=order
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + 'orders/1/items', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json[0] is not None, "API returned no order items"
    
    assert response_json[0]["item_id"] == 9999, "Order item contains old item ID. Update failed."


def test_DELETE_order_deletion(_data):
    url = _data['url'] + 'orders/999999'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200


    response = requests.get(_data['url'] + 'orders/999999', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code is 200
    
    response_json = response.json()
    
    assert response_json is None, "Order detected. Deletion failed."


# SECURITY - API should reject requests with an API key that's not authorized
# to make that request.

def test_POST_order_creation_unauthorized(_data):
    url = _data['url'] + 'orders'

    order = {
        "id": 999999,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-000001",
        "customer_po_number": "PO-662159",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z"
    }

    response = requests.post(
        url,
        headers={'API_KEY': _data['unauthorized_key']},
        json=order
    )

    assert response.status_code == 403, \
        f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(
        _data['url'] + 'orders/999999',
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 404, \
        f"API returned status {response.status_code}, order should not exist"

    response_json = response.json()

    assert response_json is None, \
        "New order has been created despite being unauthorized"


def test_PUT_order_update_unauthorized(_data):
    url = _data['url'] + 'orders/1'

    order = {
        "id": 1,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "UNAUTHORIZED-CHANGE",
        "customer_po_number": "UNAUTHORIZED-CHANGE",
        "order_status": "Delivered",
        "shipping_notes": "UNAUTHORIZED CHANGE",
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z"
    }

    original_response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert original_response.status_code == 200

    original_order = original_response.json()

    response = requests.put(
        url,
        headers={'API_KEY': _data['unauthorized_key']},
        json=order
    )

    assert response.status_code == 403, \
        f"API returned wrong status code: {response.status_code}, should be 403"

    # Check that the unauthorized update did not change the order.
    response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, \
        "Order no longer exists after unauthorized update"

    assert response_json["order_status"] == original_order["order_status"], \
        "Order status was changed despite being unauthorized"

    assert response_json["reference"] == original_order["reference"], \
        "Order reference was changed despite being unauthorized"


def test_DELETE_order_deletion_unauthorized(_data):
    url = _data['url'] + 'orders/1'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['unauthorized_key']}
    )

    assert response.status_code == 403, \
        f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, \
        "Order has been deleted despite being unauthorized"


def test_POST_order_creation_no_key(_data):
    url = _data['url'] + 'orders'

    order = {
        "id": 999999,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-000001",
        "customer_po_number": "PO-662159",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z"
    }

    response = requests.post(
        url,
        json=order
    )

    assert response.status_code == 401, \
        f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(
        _data['url'] + 'orders/999999',
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 404, \
        f"API returned status {response.status_code}, order should not exist"

    response_json = response.json()

    assert response_json is None, \
        "New order has been created despite having no API key"


def test_PUT_order_update_no_key(_data):
    url = _data['url'] + 'orders/1'

    order = {
        "id": 1,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "UNAUTHORIZED-CHANGE",
        "customer_po_number": "UNAUTHORIZED-CHANGE",
        "order_status": "Delivered",
        "shipping_notes": "UNAUTHORIZED CHANGE",
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z"
    }

    # Get the original order first.
    original_response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert original_response.status_code == 200

    original_order = original_response.json()

    response = requests.put(
        url,
        json=order
    )

    assert response.status_code == 401, \
        f"API returned wrong status code: {response.status_code}, should be 401"

    # Verify that the order was not changed.
    response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, \
        "Order no longer exists after unauthorized update"

    assert response_json["order_status"] == original_order["order_status"], \
        "Order status was changed despite having no API key"

    assert response_json["reference"] == original_order["reference"], \
        "Order reference was changed despite having no API key"


def test_DELETE_order_deletion_no_key(_data):
    url = _data['url'] + 'orders/1'

    response = requests.delete(
        url
    )

    assert response.status_code == 401, \
        f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, \
        "Order has been deleted despite having no API key"
