import random

import pytest
import requests


@pytest.fixture
def _data():
    return {
        "url": "http://127.0.0.1:3000/api/v1/",
        "api_key": "gf38743yjf39kuf309fj8f30kvi908po39jv3uofjoi3",
        "unauthorized_key": "d4s2a0b0a1n4a0l0y7t",
    }


def generate_random_id():
    return random.randint(100000, 999999999)


def create_order(_data, order_id=None):
    if order_id is None:
        order_id = generate_random_id()

    order = {
        "id": order_id,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": f"ORD-{order_id}",
        "customer_po_number": f"PO-{order_id}",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z",
    }

    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code == 201, (
        f"API returned status {response.status_code} when creating an order: "
        f"{response.text}"
    )

    return order


def test_GET_order_by_id_regular(_data):
    response = requests.get(
        _data["url"] + "orders/1",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no order"


def test_POST_order_creation(_data):
    order = create_order(_data)

    response = requests.get(
        _data["url"] + f"orders/{order['id']}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "New order does not exist. Creation failed."
    assert response_json["id"] == order["id"], "Returned order has the wrong ID"


def test_PUT_order_update(_data):
    order = create_order(_data)
    order_id = order["id"]
    order["order_status"] = "Delivered"

    response = requests.put(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code == 200

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no order"
    assert (
        response_json["order_status"] == "Delivered"
    ), "Order contains old order status. Update failed."


def test_PUT_order_items_update(_data):
    url = _data["url"] + "orders/1/items"
    order_items = [{"item_id": 9999, "amount": 24}]

    response = requests.put(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=order_items,
    )

    assert response.status_code == 200

    response = requests.get(
        url,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no order items"
    assert len(response_json) > 0, "API returned an empty order item list"
    assert (
        response_json[0]["item_id"] == 9999
    ), "Order item contains old item ID. Update failed."


def test_DELETE_order_deletion(_data):
    order = create_order(_data)
    order_id = order["id"]

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json() is not None, "Order was not created before deletion"

    response = requests.delete(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code in (200, 404)
    assert response.json() is None, "Order detected. Deletion failed."


def test_POST_order_creation_unauthorized(_data):
    order_id = generate_random_id()
    order = {
        "id": order_id,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": f"ORD-{order_id}",
        "customer_po_number": f"PO-{order_id}",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z",
    }

    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["unauthorized_key"]},
        json=order,
    )

    assert (
        response.status_code == 403
    ), f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code in (200, 404)
    assert (
        response.json() is None
    ), "New order has been created despite being unauthorized"


def test_PUT_order_update_unauthorized(_data):
    order = create_order(_data)
    order_id = order["id"]
    original_order = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    ).json()

    changed_order = order.copy()
    changed_order["order_status"] = "Delivered"
    changed_order["reference"] = "UNAUTHORIZED-CHANGE"

    response = requests.put(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["unauthorized_key"]},
        json=changed_order,
    )

    assert (
        response.status_code == 403
    ), f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "Order no longer exists after unauthorized update"
    assert (
        response_json["order_status"] == original_order["order_status"]
    ), "Order status was changed despite being unauthorized"
    assert (
        response_json["reference"] == original_order["reference"]
    ), "Order reference was changed despite being unauthorized"


def test_DELETE_order_deletion_unauthorized(_data):
    order = create_order(_data)
    order_id = order["id"]
    url = _data["url"] + f"orders/{order_id}"

    response = requests.delete(
        url,
        headers={"API_KEY": _data["unauthorized_key"]},
    )

    assert (
        response.status_code == 403
    ), f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert (
        response.json() is not None
    ), "Order has been deleted despite being unauthorized"


def test_POST_order_creation_no_key(_data):
    order_id = generate_random_id()
    order = {
        "id": order_id,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": f"ORD-{order_id}",
        "customer_po_number": f"PO-{order_id}",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z",
    }

    response = requests.post(
        _data["url"] + "orders",
        json=order,
    )

    assert (
        response.status_code == 401
    ), f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code in (200, 404)
    assert (
        response.json() is None
    ), "New order has been created despite having no API key"


def test_PUT_order_update_no_key(_data):
    order = create_order(_data)
    order_id = order["id"]
    original_order = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    ).json()

    changed_order = order.copy()
    changed_order["order_status"] = "Delivered"
    changed_order["reference"] = "NO-KEY-CHANGE"

    response = requests.put(
        _data["url"] + f"orders/{order_id}",
        json=changed_order,
    )

    assert (
        response.status_code == 401
    ), f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "Order no longer exists after update attempt"
    assert (
        response_json["order_status"] == original_order["order_status"]
    ), "Order status was changed despite having no API key"
    assert (
        response_json["reference"] == original_order["reference"]
    ), "Order reference was changed despite having no API key"


def test_DELETE_order_deletion_no_key(_data):
    order = create_order(_data)
    order_id = order["id"]
    url = _data["url"] + f"orders/{order_id}"

    response = requests.delete(url)

    assert (
        response.status_code == 401
    ), f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert (
        response.json() is not None
    ), "Order has been deleted despite having no API key"


def test_GET_order_negative_id(_data):
    response = requests.get(
        _data["url"] + "orders/-1",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code in (200, 400, 404)
    if response.status_code == 200:
        assert response.json() is None, "API returned an order for a negative ID"


def test_POST_order_negative_id(_data):
    order = {
        "id": -generate_random_id(),
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-NEGATIVE",
        "customer_po_number": "PO-NEGATIVE",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z",
    }

    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject a negative ID"


def test_PUT_order_negative_id(_data):
    order = create_order(_data)
    order_id = order["id"]
    order["id"] = -order_id
    order["order_status"] = "Invalid Update"

    response = requests.put(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject a negative ID"

    response = requests.get(
        _data["url"] + f"orders/{order_id}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert (
        response.json()["order_status"] == "Shipped"
    ), "Order was changed despite the invalid ID in the update body"


def test_POST_order_creation_invalid_json(_data):
    response = requests.post(
        _data["url"] + "orders",
        headers={
            "API_KEY": _data["api_key"],
            "Content-Type": "application/json",
        },
        data='{"id":',
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject invalid JSON"


def test_POST_order_creation_empty_body(_data):
    response = requests.post(
        _data["url"] + "orders",
        headers={
            "API_KEY": _data["api_key"],
            "Content-Type": "application/json",
        },
        data="",
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject an empty body"


def test_PUT_order_update_empty_body(_data):
    response = requests.put(
        _data["url"] + "orders/1",
        headers={
            "API_KEY": _data["api_key"],
            "Content-Type": "application/json",
        },
        data="",
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject an empty body"


def test_POST_order_creation_wrong_json_type(_data):
    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
        json=[{"id": generate_random_id()}],
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject a JSON array"


def test_POST_order_creation_missing_required_field(_data):
    order = {
        "id": generate_random_id(),
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-MISSING-FIELD",
        "customer_po_number": "PO-MISSING-FIELD",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z",
    }

    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject a missing order_status"


def test_POST_order_creation_invalid_id_type(_data):
    order = {
        "id": "invalid-id",
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-INVALID-ID",
        "customer_po_number": "PO-INVALID-ID",
        "order_status": "Shipped",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
        "created_at": "2025-03-05T04:42:29Z",
        "updated_at": "2025-03-08T00:23:16Z",
    }

    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code in (
        400,
        422,
    ), f"API returned wrong status code: {response.status_code}, should reject a string ID"


def test_POST_order_creation_duplicate_id(_data):
    order = create_order(_data)

    response = requests.post(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
        json=order,
    )

    assert response.status_code in (
        400,
        409,
    ), f"API returned wrong status code: {response.status_code}, should reject a duplicate ID"

    response = requests.get(
        _data["url"] + f"orders/{order['id']}",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json is not None
    assert (
        response_json["reference"] == order["reference"]
    ), "Existing order was changed by a duplicate creation request"


def test_GET_order_invalid_id(_data):
    response = requests.get(
        _data["url"] + "orders/invalid-id",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code in (
        400,
        404,
    ), f"API returned wrong status code: {response.status_code}, should reject an invalid ID"


def test_GET_order_invalid_path(_data):
    response = requests.get(
        _data["url"] + "orders/1/invalid",
        headers={"API_KEY": _data["api_key"]},
    )

    assert (
        response.status_code == 404
    ), f"API returned wrong status code: {response.status_code}, should be 404"


def test_PATCH_orders_unsupported_method(_data):
    response = requests.patch(
        _data["url"] + "orders",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code in (
        405,
        501,
    ), f"API returned wrong status code: {response.status_code}, should reject PATCH"
