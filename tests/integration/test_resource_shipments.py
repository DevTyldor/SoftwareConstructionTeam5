import pytest
import requests


@pytest.fixture
def _data():
    return {
        "url": "http://127.0.0.1:3000/api/v1/",
        "api_key": "f4a5c6i7l8i9t0y1m2a3n4a5g6",
        "receiving_key": "r2e4c6e8i0v3i5n7g9s",
        "analytics_key": "d4s2a0b0a1n4a0l0y7t",
    }


# Happy flow


def test_get_shipments(_data):
    url = _data["url"] + "shipments"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 200 and a list of shipments
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_shipment(_data):
    url = _data["url"] + "shipments/6132"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 200 and shipment 6132
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()["id"] == 6132
    assert response.json()["reference"] == "SHP-006132"


def test_get_shipment_orders(_data):
    url = _data["url"] + "shipments/6132/orders"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 200 and a list of order IDs
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_shipment_items(_data):
    url = _data["url"] + "shipments/6132/items"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 200 and a list of items
    assert response.status_code == 200
    assert type(response.json()) == list


def test_post_shipment_then_get(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": 99990,
        "reference": "SHP-099990",
        "order_id": 4854,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(
        url,
        json=new_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 201

    response = requests.get(
        url + "/99990",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json()["id"] == 99990
    assert response.json()["reference"] == "SHP-099990"
    assert response.json()["order_id"] == 4854
    assert response.json()["carrier_name"] == "DSV"


def test_put_shipment_then_get(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": 99991,
        "reference": "SHP-099991",
        "order_id": 4854,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(
        url,
        json=new_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 201

    updated_shipment = new_shipment.copy()
    updated_shipment["carrier_name"] = "DHL"

    response = requests.put(
        url + "/99991",
        json=updated_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 200

    response = requests.get(
        url + "/99991",
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json()["id"] == 99991
    assert response.json()["carrier_name"] == "DHL"


# Bad flow


def test_get_shipments_trailing_slash(_data):
    url = _data["url"] + "shipments/"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


def test_get_shipment_zero_id(_data):
    url = _data["url"] + "shipments/0"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 404
    assert response.status_code == 404


def test_get_shipment_that_does_not_exist(_data):
    url = _data["url"] + "shipments/999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 404, not null with 200
    assert response.status_code == 404


def test_get_orders_of_shipment_that_does_not_exist(_data):
    url = _data["url"] + "shipments/999999/orders"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 404, not an empty list
    assert response.status_code == 404


def test_get_items_of_shipment_that_does_not_exist(_data):
    url = _data["url"] + "shipments/999999/items"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 404, not an empty list
    assert response.status_code == 404


def test_get_shipment_negative_id(_data):
    url = _data["url"] + "shipments/-1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_get_shipment_wrong_path(_data):
    url = _data["url"] + "shipments/6132/qwerty"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_put_shipment_negative_id(_data):
    url = _data["url"] + "shipments/-1"

    updated_shipment = {
        "id": -1,
        "reference": "SHP-000000",
        "order_id": 4854,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.put(
        url,
        json=updated_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 404


# Validation flow


def test_post_shipment_id_is_string(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": "99992",
        "reference": "SHP-099992",
        "order_id": 4854,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(
        url,
        json=new_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    # ID must be an integer
    assert response.status_code == 400


def test_post_shipment_order_id_wrong_type(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": 99993,
        "reference": "SHP-099993",
        "order_id": "geen nummer",
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(
        url,
        json=new_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    # Order ID must be an integer
    assert response.status_code == 400


def test_post_shipment_order_does_not_exist(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": 99994,
        "reference": "SHP-099994",
        "order_id": 999999,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(
        url,
        json=new_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    # Order 999999 does not exist
    assert response.status_code == 400


def test_post_shipment_invalid_date(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": 99995,
        "reference": "SHP-099995",
        "order_id": 4854,
        "shipment_date": "geen datum",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(
        url,
        json=new_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 400


def test_put_shipment_partial_body(_data):
    url = _data["url"] + "shipments/6132"

    response = requests.put(
        url,
        json={"carrier_name": "DHL"},
        headers={"API_KEY": _data["receiving_key"]},
    )

    # Only the carrier name, all other fields are missing
    assert response.status_code == 400


# Error flow


def test_get_shipment_id_not_a_number(_data):
    url = _data["url"] + "shipments/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Should give 400, not 500
    assert response.status_code == 400


def test_get_shipment_orders_id_not_a_number(_data):
    url = _data["url"] + "shipments/abc/orders"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_get_shipment_items_id_not_a_number(_data):
    url = _data["url"] + "shipments/abc/items"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_get_shipment_id_is_decimal(_data):
    url = _data["url"] + "shipments/1.5"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_shipment_without_body(_data):
    url = _data["url"] + "shipments"

    response = requests.post(
        url,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 400


def test_post_shipment_broken_json(_data):
    url = _data["url"] + "shipments"

    broken_json = '{"id": 99996, "reference": '

    response = requests.post(
        url,
        data=broken_json,
        headers={
            "API_KEY": _data["receiving_key"],
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400


def test_put_shipment_id_not_a_number(_data):
    url = _data["url"] + "shipments/abc"

    updated_shipment = {
        "id": 6132,
        "reference": "SHP-006132",
        "order_id": 4854,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.put(
        url,
        json=updated_shipment,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 400


def test_put_shipment_broken_json(_data):
    url = _data["url"] + "shipments/6132"

    broken_json = '{"id": 6132, "reference": '

    response = requests.put(
        url,
        data=broken_json,
        headers={
            "API_KEY": _data["receiving_key"],
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400


def test_put_shipment_orders_without_body(_data):
    url = _data["url"] + "shipments/6132/orders"

    response = requests.put(
        url,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 400


def test_put_shipment_items_without_body(_data):
    url = _data["url"] + "shipments/6132/items"

    response = requests.put(
        url,
        headers={"API_KEY": _data["receiving_key"]},
    )

    assert response.status_code == 400


# Security flow


def test_get_shipments_without_api_key(_data):
    url = _data["url"] + "shipments"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_shipment_without_api_key(_data):
    url = _data["url"] + "shipments/6132"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_shipment_orders_without_api_key(_data):
    url = _data["url"] + "shipments/6132/orders"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_shipment_items_without_api_key(_data):
    url = _data["url"] + "shipments/6132/items"

    response = requests.get(url)

    assert response.status_code == 401


def test_post_shipment_without_api_key(_data):
    url = _data["url"] + "shipments"

    new_shipment = {
        "id": 99997,
        "reference": "SHP-099997",
        "order_id": 4854,
        "shipment_date": "2026-04-04T14:03:45Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "DSV",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "created_at": "2026-04-04T14:03:45Z",
        "updated_at": "2026-04-05T21:21:08Z",
    }

    response = requests.post(url, json=new_shipment)

    assert response.status_code == 401


def test_put_shipment_without_api_key(_data):
    url = _data["url"] + "shipments/6132"

    response = requests.put(
        url,
        json={"carrier_name": "DHL"},
    )

    assert response.status_code == 401


def test_put_shipment_orders_without_api_key(_data):
    url = _data["url"] + "shipments/6132/orders"

    response = requests.put(url, json=[])

    assert response.status_code == 401


def test_put_shipment_items_without_api_key(_data):
    url = _data["url"] + "shipments/6132/items"

    response = requests.put(url, json=[])

    assert response.status_code == 401


def test_delete_shipment_without_api_key(_data):
    url = _data["url"] + "shipments/6132"

    response = requests.delete(url)

    assert response.status_code == 401
