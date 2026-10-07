import pytest
import requests

# This file runs tests for all API endpoints of locations.

@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'gf38743yjf39kuf309fj8f30kvi908po39jv3uofjoi3',
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
        "id": 500,
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

    response = requests.get(_data['url'] + 'locations/500', headers={'API_KEY': _data['api_key']})
        
    status_code = response.status_code
        
    assert status_code == 200
        
    response_json = response.json()
        
    assert response_json is not None, "New location does not exist. Creation failed."


def test_PUT_location_update(_data):
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
        headers={'API_KEY': _data['api_key']},
        json=location
    )

    assert response.status_code == 200

    response = requests.get(_data['url'] + 'locations/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code == 200
    
    response_json = response.json()
    
    assert response_json is not None, "Updated location does not exist"

    assert response_json["name"] == "New Zone", "Location contains old name. Update failed."


def test_DELETE_location_deletion(_data):
    url = _data['url'] + 'locations/1'

    response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200


    response = requests.get(_data['url'] + 'locations/1', headers={'API_KEY': _data['api_key']})
    
    status_code = response.status_code
    
    assert status_code is 200
    
    response_json = response.json()
    
    assert response_json is None, "Location detected. Deletion failed."