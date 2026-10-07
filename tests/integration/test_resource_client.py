import pytest
import requests

@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6'
    }

def test_GET_clients(_data):
    url = _data['url'] + '/clients'
    headers = {'API_KEY': _data['api_key']}

    # Send a GET request to the API
    response = requests.get(url, headers=headers)

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_GET_client_by_id_regular(_data):
    url = _data['url'] + '/clients/1'
    headers = {'API_KEY': _data['api_key']}

    response = requests.get(url, headers=headers)

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no client data"


def test_POST_client_creation(_data):
    url = _data['url'] + '/clients'
    headers = {'API_KEY': _data['api_key']}

    client = {
        "id": 11,
        "name": "Jane Doe",
        "address": "Laan van Mathenesse 9a",
        "city": "Utrecht",
        "zip_code": "2665 MZ",
        "province": "Utrecht",
        "country": "Netherlands",
        "contact_phone": "0801-845146",
        "contact_email": "jane.doe@example.com",
        "created_at": "2024-02-11T05:19:57Z",
        "updated_at": "2024-03-09T12:13:49Z"
    }

    response = requests.post(
        url,
        headers=headers,
        json=client
    )

    assert response.status_code == 201

    response = requests.get(_data['url'] + '/clients/11', headers=headers)

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "New client does not exist. Creation failed."


def test_PUT_client_update(_data):
    url = _data['url'] + '/clients/1'
    headers = {'API_KEY': _data['api_key']}

    client = {
        "id": 1,
        "name": "Jane Doe Renamed",
        "address": "Laan van Mathenesse 9a",
        "city": "Utrecht",
        "zip_code": "2665 MZ",
        "province": "Utrecht",
        "country": "Netherlands",
        "contact_phone": "0801-845146",
        "contact_email": "jane.doe@example.com",
        "created_at": "2024-02-11T05:19:57Z",
        "updated_at": "2024-03-09T12:13:49Z"
    }

    response = requests.put(
        url,
        headers=headers,
        json=client
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + '/clients/1', headers=headers)

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no client data"

    assert response_json["name"] == "Jane Doe Renamed", "Client contains old name. Update failed."


def test_DELETE_client_deletion(_data):
    url = _data['url'] + '/clients/1'
    headers = {'API_KEY': _data['api_key']}

    response = requests.delete(
        url,
        headers=headers
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + '/clients/1', headers=headers)

    status_code = response.status_code

    assert status_code == 404, "Client still reachable. Deletion failed."
