import pytest
import requests

# This file runs tests for all API endpoints of warehouses.

@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'gf38743yjf39kuf309fj8f30kvi908po39jv3uofjoi3',
    }


def test_GET_warehouses(_data):
    url = _data['url'] + 'warehouses'

    # Send a GET request to the API
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_GET_warehouse_by_id_regular(_data):
    url = _data['url'] + 'warehouses/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no warehouse data"


def test_GET_warehouse_location_by_id(_data):
    url = _data['url'] + 'warehouses/1/locations'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no warehouse data"


def test_POST_warehouse_creation(_data):
    url = _data['url'] + 'warehouses'

    warehouse = {
        "id": 999999,
        "code": "BLW-EFC",
        "name": "Jumbo EFC Utrecht",
        "address": "Laan van Mathenesse 9a",
        "city": "Utrecht",
        "zip_code": "2665 MZ",
        "province": "Utrecht",
        "country": "Netherlands",
        "contact_name": "Lola van Mare",
        "contact_phone": "0801-845146",
        "contact_email": "blw-efc@jumbo-logistiek.nl",
        "created_at": "2024-02-11T05:19:57Z",
        "updated_at": "2024-03-09T12:13:49Z"
    }

    response = requests.post(
        url,
        headers={'API_KEY': _data['api_key']},
        json=warehouse
    )

    assert response.status_code == 201

    response = requests.get(_data['url'] + 'warehouses/999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is not None, "New warehouse does not exist. Creation failed."


def test_PUT_warehouse_update(_data):
    url = _data['url'] + 'warehouses/999999'

    warehouse = {
        "id": 999999,
        "code": "BLW-EFC",
        "name": "Jumbo EFC Utrecht",
        "address": "Laan van Mathenesse 9a",
        "city": "Utrecht",
        "zip_code": "2665 MZ",
        "province": "Utrecht",
        "country": "Netherlands",
        "contact_name": "Lola van Mare",
        "contact_phone": "0801-845146",
        "contact_email": "blw-efc@jumbo-logistiek.nl",
        "created_at": "2024-02-11T05:19:57Z",
        "updated_at": "2024-03-09T12:13:49Z"
    }

    response = requests.put(
        url,
        headers={'API_KEY': _data['api_key']},
        json=warehouse
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + 'warehouses/999999', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "API returned no warehouse data"
    
    assert response_json["name"] == "Jumbo EFC Utrecht", "Warehouse contains old name. Update failed."


def test_DELETE_warehouse_deletion(_data):
    url = _data['url'] + 'warehouses/999999'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200


    response = requests.get(_data['url'] + 'warehouses/999999', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code is 200
    
    response_json = response.json()
    
    assert response_json is None, "Warehouse detected. Deletion failed."