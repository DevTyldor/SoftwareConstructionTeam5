import pytest
import requests

# This file runs tests for all API endpoints of warehouses.

@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'gf38743yjf39kuf309fj8f30kvi908po39jv3uofjoi3',
        'unauthorized_key': 's1h3i5p7p9i2n4g6s8t' # This key only has GET access on resource warehouses
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
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is None, "Warehouse detected. Deletion failed."


# SECURITY - API should reject requests with an API key that's not authorized to make that request.

def test_POST_warehouse_creation_unauthorized(_data):
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
        headers={'API_KEY': _data['unauthorized_key']},
        json=warehouse
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(_data['url'] + 'warehouses/999999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is None, "New warehouse has been created despite being unauthorized"


def test_PUT_warehouse_update_unauthorized(_data):
    url = _data['url'] + 'warehouses/1'

    warehouse = {
    "id": 1,
    "code": "VGH-AMB",
    "name": "Jumbo DC Utrecht",
    "address": "De Amert 409",
    "city": "Utrecht",
    "zip_code": "5462 GH",
    "province": "Noord-Brabant",
    "country": "Netherlands",
    "contact_name": "Ali Schellekens",
    "contact_phone": "(032) 1819600",
    "contact_email": "vgh-amb@jumbo-logistiek.nl",
    "created_at": "2024-06-21T22:43:23Z",
    "updated_at": "2024-06-23T04:51:45Z"
    }

    response = requests.put(
        url,
        headers={'API_KEY': _data['unauthorized_key']},
        json=warehouse
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(_data['url'] + 'warehouses/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Updated warehouse does not exist"

    assert response_json["name"] != "Jumbo DC Utrecht", "Warehouse has been updated despite being unauthorized"


def test_DELETE_warehouse_unauthorized(_data):
    url = _data['url'] + 'warehouses/1'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['unauthorized_key']}
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"


    response = requests.get(_data['url'] + 'warehouses/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Warehouse has been deleted despite being unauthorized"

def test_POST_warehouse_creation_no_key(_data):
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
        json=warehouse
    )

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(_data['url'] + 'warehouses/999999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is None, "New warehouse has been created despite being unauthorized"


def test_PUT_warehouse_update_no_key(_data):
    url = _data['url'] + 'warehouses/1'

    warehouse = {
        "id": 1,
        "code": "VGH-AMB",
        "name": "Jumbo DC Utrecht",
        "address": "De Amert 409",
        "city": "Utrecht",
        "zip_code": "5462 GH",
        "province": "Noord-Brabant",
        "country": "Netherlands",
        "contact_name": "Ali Schellekens",
        "contact_phone": "(032) 1819600",
        "contact_email": "vgh-amb@jumbo-logistiek.nl",
        "created_at": "2024-06-21T22:43:23Z",
        "updated_at": "2024-06-23T04:51:45Z"
        }

    response = requests.put(
        url,
        json=warehouse
    )

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(_data['url'] + 'warehouses/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Updated warehouse does not exist"

    assert response_json["name"] != "Jumbo DC Utrecht", "Warehouse has been updated despite being unauthorized"


def test_DELETE_warehouse_no_key(_data):
    url = _data['url'] + 'warehouses/1'

    response = requests.delete(
        url
    )

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"


    response = requests.get(_data['url'] + 'warehouses/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Warehouse has been deleted despite being unauthorized"
