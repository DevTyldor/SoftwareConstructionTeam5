import pytest
import requests

# This file runs tests for all API endpoints of locations.


# HAPPY FLOW - if all these tests succeed it means the application fully works
@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'gf38743yjf39kuf309fj8f30kvi908po39jv3uofjoi3',
        'unauthorized_key': "d4s2a0b0a1n4a0l0y7t" # this key only has read(GET) access on resource locations
    }


def test_GET_locations(_data):
    url = _data['url'] + 'locations'

    # Send a GET request to the API
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200

    response_json = response.json()
            
    assert response_json is not None, "API returned no location data"


def test_GET_location_by_id_regular(_data):
    url = _data['url'] + 'locations/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    status_code = response.status_code

    assert status_code == 200

    response_json = response.json()

    assert response_json is not None, "API returned no location data"


def test_POST_location_creation(_data):
    url = _data['url'] + 'locations'

    location = {
        "id": 999999999,
        "warehouse_id": 10,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
        }

    response = requests.post(
        url,
        headers={'API_KEY': _data['api_key']},
        json=location
    )

    assert response.status_code == 201

    response = requests.get(_data['url'] + 'locations/999999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is not None, "New location does not exist. Creation failed."


def test_PUT_location_update(_data):
    url = _data['url'] + 'locations/999999999'

    location = {
        "id": 999999999,
        "warehouse_id": 1,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
    }

    response = requests.put(
        url,
        headers={'API_KEY': _data['api_key']},
        json=location
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + 'locations/999999999', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Updated location does not exist"

    assert response_json["name"] == "New Zone", "Location contains old name. Update failed."


def test_DELETE_location(_data):
    url = _data['url'] + 'locations/999999999'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200


    response = requests.get(_data['url'] + 'locations/999999999', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code is 200
    
    response_json = response.json()
    
    assert response_json is None, "Location detected. Deletion failed."

# SECURITY - API should reject requests with an API key that's not authorized to make that request.

def test_POST_location_creation_unauthorized(_data):
    url = _data['url'] + 'locations'

    location = {
        "id": 999999999,
        "warehouse_id": 10,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
        }

    response = requests.post(
        url,
        headers={'API_KEY': _data['unauthorized_key']},
        json=location
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(_data['url'] + 'locations/999999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is None, "New location has been created despite being unauthorized"


def test_PUT_location_update_unauthorized(_data):
    url = _data['url'] + 'locations/1'

    location = {
        "id": 1,
        "warehouse_id": 1,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
    }

    response = requests.put(
        url,
        headers={'API_KEY': _data['unauthorized_key']},
        json=location
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"

    response = requests.get(_data['url'] + 'locations/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Updated location does not exist"

    assert response_json["name"] != "New Zone", "Location has been updated despite being unauthorized"


def test_DELETE_location_unauthorized(_data):
    url = _data['url'] + 'locations/1'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['unauthorized_key']}
    )

    assert response.status_code == 403, f"API returned wrong status code: {response.status_code}, should be 403"


    response = requests.get(_data['url'] + 'locations/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code is 200
    
    response_json = response.json()
    
    assert response_json is not None, "Location has been deleted despite being unauthorized"

def test_POST_location_creation_no_key(_data):
    url = _data['url'] + 'locations'

    location = {
        "id": 999999999,
        "warehouse_id": 10,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
        }

    response = requests.post(
        url,
        json=location
    )

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(_data['url'] + 'locations/999999999', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is None, "New location has been created despite being unauthorized"


def test_PUT_location_update_no_key(_data):
    url = _data['url'] + 'locations/1'

    location = {
        "id": 1,
        "warehouse_id": 1,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
    }

    response = requests.put(
        url,
        json=location
    )

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"

    response = requests.get(_data['url'] + 'locations/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Updated location does not exist"

    assert response_json["name"] != "New Zone", "Location has been updated despite being unauthorized"


def test_DELETE_location_no_key(_data):
    url = _data['url'] + 'locations/1'

    response = requests.delete(
        url
    )

    assert response.status_code == 401, f"API returned wrong status code: {response.status_code}, should be 401"


    response = requests.get(_data['url'] + 'locations/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code is 200
    
    response_json = response.json()
    
    assert response_json is not None, "Location has been deleted despite being unauthorized"

# BAD FLOW - API should gracefully reject these malformed requests with correct error codes.

def test_GET_location_negative_id(_data):
    url = _data['url'] + 'locations/-1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    status_code = response.status_code

    assert status_code == 404, f"API returned status code {status_code}, should be 404"

    response_json = response.json()

    assert response_json is None, "API returned data despite ID being invalid"


def test_POST_location_negative_id(_data):
    url = _data['url'] + 'locations'
    
    location = {
        "id": -2,
        "warehouse_id": 10,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
        }
    
    response = requests.post(
        url,
        headers={'API_KEY': _data['api_key']},
        json=location
    )
    
    assert response.status_code == 400, f"API returned status {response.status_code}, should be 400"
    
    response = requests.get(_data['url'] + 'locations/-2', headers={'API_KEY': _data['api_key']})
            
    status_code = response.status_code
            
    assert status_code == 200
            
    response_json = response.json()
            
    assert response_json is None, "New location created despite ID being negative"


def test_PUT_location_negative_id(_data):
    url = _data['url'] + 'locations/1'
    
    location = {
        "id": -2,
        "warehouse_id": 10,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "New Zone",
        "created_at": "2024-12-08T10:37:19Z",
        "updated_at": "2024-12-30T06:59:18Z"
        }
    
    response = requests.post(
        url,
        headers={'API_KEY': _data['api_key']},
        json=location
    )
    
    assert response.status_code == 400, f"API returned status {response.status_code}, should be 400"
    
    response = requests.get(_data['url'] + 'locations/-2', headers={'API_KEY': _data['api_key']})
            
    status_code = response.status_code
            
    assert status_code != 200, f"API returns status 200 on negative ID. "
            
    response_json = response.json()
            
    assert response_json is None, "Found updated location with ID -2, however, this ID is invalid"