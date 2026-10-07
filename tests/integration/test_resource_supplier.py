import os
import pytest
import requests

#this resource runs test on all endpoints of the resource supplier. 
#It is a template for testing other resources as well. 
#The test cases are defined in the test_get_supplier function, which returns a list of dictionaries representing each test case.
# Each dictionary contains the name of the test, the HTTP method, the URL, the expected status code, and an optional payload for POST requests.

@pytest.fixture
def _data():
    return{
        'url': 'http://localhost:3000/api/v1',
        'api_key': os.getenv('API_KEY'),
    }

#Happy flow test cases for the resource supplier.
def test_get_suppliers(_data):
    '''test get all suppliers'''
    url = _data['url'] + '/suppliers'
    headers = {"API_KEY": _data['api_key']}

    response = requests.get(
        url, 
        headers=headers
        )

    status_code = response.status_code
    response_json = response.json()

    assert status_code == 200
    assert type(response_json) == list, "API returned a non-list response"

def test_get_supplier_by_id(_data):
    '''test get supplier by id'''
    id = 1
    url = f"{_data['url']}/suppliers/{id}"
    headers = {"API_KEY": _data['api_key']}

    response = requests.get(
        url, 
        headers=headers
        )
    
    response_json = response.json()

    assert response.status_code == 200, "API returned a non-200 status code for GET request"
    assert response_json["id"] == 1, "API returned the wrong supplier"



def test_POST_supplier_creation(_data):
    url = _data['url'] + '/suppliers'
    headers = {'API_KEY': _data['api_key']}

    supplier = {
        "id": 11,
        "name": "Jumbo EFC Utrecht Supplies",
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
        headers=headers,
        json=supplier
    )

    assert response.status_code == 201, "API returned a non-201 status code for POST request"

    response = requests.get(_data['url'] + '/suppliers/11', headers=headers)

    status_code = response.status_code
    response_json = response.json()

    assert status_code == 200, "API returned a non-200 status code for GET request after creation"
    assert response_json is not None, "New supplier does not exist. Creation failed."


def test_PUT_supplier_update(_data):
    url = _data['url'] + '/suppliers/1'
    headers = {'API_KEY': _data['api_key']}
    supplier = {
        "id": 1,
        "name": "Jumbo EFC Utrecht Supplies",
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
        headers=headers,
        json=supplier
    )

    assert response.status_code == 200, "API returned a non-200 status code for PUT request"

    response = requests.get(_data['url'] + '/suppliers/1', headers=headers)

    status_code = response.status_code
    response_json = response.json()

    assert status_code == 200, "API returned a non-200 status code for GET request after update"
    assert response_json is not None, "API returned no supplier data"
    assert response_json["name"] == "Jumbo EFC Utrecht Supplies", "Supplier contains old name. Update failed."


def test_DELETE_supplier_deletion(_data):
    url = _data['url'] + '/suppliers/1'
    headers = {'API_KEY': _data['api_key']}
    
    response = requests.delete(
        url,
        headers=headers
    )

    assert response.status_code == 200, "API returned a non-200 status code for DELETE request"

    response = requests.get(
        url, 
        headers=headers
        )

    status_code = response.status_code

    assert status_code == 404, "Supplier still reachable. Deletion failed."