import pytest
import requests

#this resource runs test on all endpoints of the resource supplier. 
#It is a template for testing other resources as well. 
#The test cases are defined in the test_get_supplier function, which returns a list of dictionaries representing each test case.
# Each dictionary contains the name of the test, the HTTP method, the URL, the expected status code, and an optional payload for POST requests.

@pytest.fixture
def _data():
    return{
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6'
    }

#Happy flow test cases for the resource supplier.
def test_get_suppliers(_data):
    '''test get all suppliers'''
    url = _data['url'] + 'suppliers'
    headers = {"API_KEY": _data['api_key']}

    try:
        response = requests.get(
            url, 
            headers=headers
            )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

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
    id = 2
    url = _data['url'] + f'suppliers/{id}'
    headers = {"API_KEY": _data['api_key']}

    response = requests.get(
        url, 
        headers=headers
        )

    response_code = response.status_code
    response_json = response.json()

    assert response_code == 200, "API returned a non-200 status code for GET request"
    assert response_json is not None, f'API returned no data for supplier with id {id}, with status code {response_code}'
    assert response_json['id'] == id, f'API returned data for supplier with id {response_json["id"]}, expected {id}. Status code: {response_code}'



def test_POST_supplier_creation(_data):
    '''test create new supplier with id 99999'''
    url = _data['url'] + 'suppliers'
    headers = {'API_KEY': _data['api_key']}

    supplier = {
        "id": 99999,
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

    response = requests.get(_data['url'] + 'suppliers/11', headers=headers)

    status_code = response.status_code
    try:
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Expecting None response for GET request after creation, but got an error: {e}")

    assert status_code == 200, "API returned a non-200 status code for GET request after creation"
    assert response_json is None, f"New supplier does not exist. Creation failed. Status code: {response.status_code}"


def test_PUT_supplier_update(_data):
    '''test update supplier with id 1'''
    id = 1
    url = _data['url'] + 'suppliers/1'
    headers = {'API_KEY': _data['api_key']}
    supplier = {
        "id": id,
        "name": "Jumbo EFC Utrecht Supplies",
        "address": "Laan van Mathenesse 9a",
        "city": "Utrecht",
        "zip_code": "2665 MZ",
        "province": "Utrecht",
        "country": "Netherlands",
        "contact_name": "Lola van Mare",
        "phone_number": "0801-845146",
        "reference": "blw-efc@jumbo-logistiek.nl",
        "created_at": "2024-02-11T05:19:57Z",
        "updated_at": "2024-03-09T12:13:49Z"
    }

    # Update the supplier data
    response = requests.put(
        url,
        headers=headers,
        json=supplier
    )

    assert response.status_code == 200, "API returned a non-200 status code for PUT request"
    # Get the updated supplier data after the update
    response = requests.get(_data['url'] + f'suppliers/{id}', headers=headers)

    status_code = response.status_code
    updated_supplier = response.json()

    assert status_code == 200, "API returned a non-200 status code for GET request after update"
    # assert updated_supplier is not None, "API returned no supplier data"
    supplier_keys = supplier.keys()
    for key in supplier_keys:
        assert updated_supplier[key] == supplier[key], f"API returned incorrect data for key '{key}'. Expected: {supplier[key]}, Got: {updated_supplier[key]}"


def test_DELETE_supplier_deletion(_data):
    '''remove test supplier with id 11'''
    id = 1
    url = _data['url'] + f'suppliers/{id}'
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
    

    assert status_code == 200, "Supplier still exists after deletion. DELETE request failed."
    try:
        response_json = response.json()
        assert response_json is None, "Supplier still exists after deletion. DELETE request failed."
    except AssertionError as e:
        pytest.fail(f"Supplier still exists after deletion. DELETE request failed. Status code: {status_code}, Response: {response_json}")