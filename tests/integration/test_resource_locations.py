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


def create_location(_data, location_id=None):
    if location_id is None:
        location_id = generate_random_id()

    location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": f"TST-{location_id}",
        "name": "Test Location",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        _data["url"] + "locations",
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code == 201, f"API returned wrong status code: {response.status_code}, should be 201"
    return location


def test_GET_locations(_data):
    url = _data["url"] + "locations"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no location data"


def test_GET_location_by_id_regular(_data):
    location = create_location(_data)
    url = _data["url"] + "locations/" + str(location["id"])

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no location data"
    assert response_json["id"] == location["id"], "API returned an unexpected location"


def test_POST_location_creation(_data):
    location_id = generate_random_id()
    url = _data["url"] + "locations"

    location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": f"TST-{location_id}",
        "name": "Test Location Creation",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code == 201, f"API returned wrong status code: {response.status_code}, should be 201"

    response = requests.get(
        url + "/" + str(location_id),
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "New location does not exist. Creation failed."
    assert response_json["name"] == "Test Location Creation", "Location contains unexpected data"


def test_PUT_location_update(_data):
    location = create_location(_data)
    location_id = location["id"]
    url = _data["url"] + "locations/" + str(location_id)

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert response.json() is not None, "Location does not exist. Creation failed."

    location["name"] = "Updated Test Location"

    response = requests.put(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code == 200, f"API returned wrong status code: {response.status_code}, should be 200"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None, "Updated location does not exist"
    assert response_json["name"] == "Updated Test Location", "Location contains old name. Update failed."


def test_DELETE_location(_data):
    location = create_location(_data)
    location_id = location["id"]
    url = _data["url"] + "locations/" + str(location_id)

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert response.json() is not None, "Location does not exist. Creation failed."

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200, f"API returned wrong status code: {response.status_code}, should be 200"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert response.json() is None, "Location detected. Deletion failed."


def test_POST_location_creation_unauthorized(_data):
    location_id = generate_random_id()
    url = _data["url"] + "locations"

    location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": f"TST-{location_id}",
        "name": "Unauthorized Test Location",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        url,
        headers={"API_KEY": _data["unauthorized_key"]},
        json=location,
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(
        url + "/" + str(location_id),
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json() is None, "New location has been created despite being unauthorized"


def test_PUT_location_update_unauthorized(_data):
    location = create_location(_data)
    location_id = location["id"]
    url = _data["url"] + "locations/" + str(location_id)
    original_name = location["name"]
    location["name"] = "Unauthorized Location Update"

    response = requests.put(
        url,
        headers={"API_KEY": _data["unauthorized_key"]},
        json=location,
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    response_json = response.json()

    assert response_json is not None, "Location does not exist"
    assert response_json["name"] == original_name, "Location has been updated despite being unauthorized"


def test_DELETE_location_unauthorized(_data):
    location = create_location(_data)
    url = _data["url"] + "locations/" + str(location["id"])

    response = requests.delete(url, headers={"API_KEY": _data["unauthorized_key"]})

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert response.json() is not None, "Location has been deleted despite being unauthorized"


def test_POST_location_creation_no_key(_data):
    location_id = generate_random_id()
    url = _data["url"] + "locations"

    location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": f"TST-{location_id}",
        "name": "No Key Test Location",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(url, json=location)

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(
        url + "/" + str(location_id),
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json() is None, "New location has been created despite being unauthorized"


def test_PUT_location_update_no_key(_data):
    location = create_location(_data)
    location_id = location["id"]
    url = _data["url"] + "locations/" + str(location_id)
    original_name = location["name"]
    location["name"] = "No Key Location Update"

    response = requests.put(url, json=location)

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    response_json = response.json()

    assert response_json is not None, "Location does not exist"
    assert response_json["name"] == original_name, "Location has been updated despite being unauthorized"


def test_DELETE_location_no_key(_data):
    location = create_location(_data)
    url = _data["url"] + "locations/" + str(location["id"])

    response = requests.delete(url)

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert response.json() is not None, "Location has been deleted despite being unauthorized"


def test_GET_location_negative_id(_data):
    url = _data["url"] + "locations/-1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404, f"API returned status code {response.status_code}, should be 404"
    assert response.json() is None, "API returned data despite ID being invalid"


def test_POST_location_negative_id(_data):
    url = _data["url"] + "locations"
    location_id = -generate_random_id()

    location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": "TST-NEGATIVE",
        "name": "Invalid Negative ID Location",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code == 400, f"API returned status {response.status_code}, should be 400"

    response = requests.get(
        url + "/" + str(location_id),
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json() is None, "New location created despite ID being negative"


def test_PUT_location_negative_id(_data):
    location = create_location(_data)
    location_id = location["id"]
    url = _data["url"] + "locations/" + str(location_id)
    original_name = location["name"]
    location["id"] = -generate_random_id()
    location["name"] = "Invalid Negative ID Location"

    response = requests.put(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code == 400, f"API returned status {response.status_code}, should be 400"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    response_json = response.json()

    assert response_json is not None, "Location does not exist"
    assert response_json["name"] == original_name, "Location was updated despite an invalid ID"


def test_POST_location_creation_invalid_json(_data):
    url = _data["url"] + "locations"

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"], "Content-Type": "application/json"},
        data='{"id": 123, "name": ',
    )

    assert response.status_code in (400, 422), f"API returned wrong status code: {response.status_code}, should be 400 or 422"


def test_POST_location_creation_empty_body(_data):
    url = _data["url"] + "locations"

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        data="",
    )

    assert response.status_code in (400, 422), f"API returned wrong status code: {response.status_code}, should be 400 or 422"

def test_PUT_location_update_empty_body(_data):
    url = _data["url"] + "locations/1"

    response = requests.put(
        url,
        headers={"API_KEY": _data["api_key"]},
        data="",
    )

    assert response.status_code in (400, 422), f"API returned wrong status code: {response.status_code}, should be 400 or 422"


def test_POST_location_creation_wrong_json_type(_data):
    url = _data["url"] + "locations"

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=["location"],
    )

    assert response.status_code in (400, 422), f"API returned wrong status code: {response.status_code}, should be 400 or 422"


def test_POST_location_creation_missing_name(_data):
    url = _data["url"] + "locations"
    location_id = generate_random_id()

    location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": f"TST-{location_id}",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code in (400, 422), f"API returned wrong status code: {response.status_code}, should be 400 or 422"

    response = requests.get(
        url + "/" + str(location_id),
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    assert response.json() is None, "Location was created without a name"


def test_POST_location_creation_invalid_id_type(_data):
    url = _data["url"] + "locations"

    location = {
        "id": "not-a-number",
        "warehouse_id": 10,
        "code": "TST-INVALID-ID",
        "name": "Invalid ID Type Location",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=location,
    )

    assert response.status_code in (400, 422), f"API returned wrong status code: {response.status_code}, should be 400 or 422"


def test_POST_location_creation_duplicate_id(_data):
    location = create_location(_data)
    location_id = location["id"]
    url = _data["url"] + "locations"
    duplicate_location = {
        "id": location_id,
        "warehouse_id": 10,
        "code": f"DUP-{location_id}",
        "name": "Duplicate Test Location",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z",
    }

    response = requests.post(
        url,
        headers={"API_KEY": _data["api_key"]},
        json=duplicate_location,
    )

    assert response.status_code in (400, 409), f"API returned wrong status code: {response.status_code}, should be 400 or 409"

    response = requests.get(
        url + "/" + str(location_id),
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 200
    response_json = response.json()

    assert response_json is not None, "Existing location does not exist"
    assert response_json["name"] == location["name"], "Existing location was overwritten by a duplicate-ID POST request"


def test_GET_location_invalid_id(_data):
    url = _data["url"] + "locations/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code in (400, 404), f"API returned wrong status code: {response.status_code}, should be 400 or 404"


def test_GET_location_invalid_path(_data):
    url = _data["url"] + "locations/1/invalid"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404, f"API returned wrong status code: {response.status_code}, should be 404"


def test_PATCH_locations_unsupported_method(_data):
    url = _data["url"] + "locations"

    response = requests.patch(
        url,
        headers={"API_KEY": _data["api_key"]},
        json={"name": "Unexpected Update"},
    )

    assert response.status_code in (405, 501), f"API returned wrong status code: {response.status_code}, should be 405 or 501"
