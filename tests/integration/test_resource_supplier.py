import pytest
import requests

#this resource runs test on all endpoints of the resource supplier. 
#It is a template for testing other resources as well. 
#The test cases are defined in the test_get_supplier function, which returns a list of dictionaries representing each test case.
# Each dictionary contains the name of the test, the HTTP method, the URL, the expected status code, and an optional payload for POST requests.

@pytest.fixture
def _data():
    return{
        'url': 'http://127.0.0.1:3000/api/v1/',
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
    '''test update supplier with id'''
    id = 1
    url = _data['url'] + 'suppliers/{id}'
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
    '''remove test supplier with id 99999'''
    id = 99999
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

# Extra supplier tests
#
# These tests do not depend on supplier 1 or 2 (the tests above change and delete them).
# They create their own suppliers with a unique id and delete them afterwards.
# Assumptions about the API: a rejected duplicate or invalid body gives 400/409/422,
# a missing or wrong API key gives 401/403, and an unknown supplier gives 404
# (or 200 with an empty body, as the delete test above expects).

# REJECTED = (400, 409, 422)
# UNAUTHORIZED = (401, 403)


# def is_not_found(response):
#     '''A missing supplier is either a 404 or a 200 with an empty body.'''
#     if response.status_code == 404:
#         return True
#     if response.status_code == 200:
#         try:
#             return response.json() in (None, {}, [])
#         except ValueError:
#             return False
#     return False


# @pytest.fixture
# def new_supplier(_data):
#     '''Factory for test suppliers: new_supplier() creates one through the API,
#     new_supplier(create=False) only builds the payload. Created suppliers are
#     deleted again after the test.'''
#     headers = {'API_KEY': _data['api_key']}
#     created = []

#     def factory(create=True, **overrides):
#         supplier = {
#             "id": 900000,
#             "name": "Test Supplier",
#             "address": "Laan van Mathenesse 9a",
#             "city": "Utrecht",
#             "zip_code": "2665 MZ",
#             "province": "Utrecht",
#             "country": "Netherlands",
#             "contact_name": "Lola van Mare",
#             "contact_phone": "0801-845146",
#             "contact_email": "test-supplier@example.com",
#             "created_at": "2024-02-11T05:19:57Z",
#             "updated_at": "2024-03-09T12:13:49Z"
#         }
#         supplier.update(overrides)
#         created.append(supplier["id"])
#         if create:
#             response = requests.post(_data['url'] + 'suppliers', headers=headers, json=supplier)
#             assert response.status_code == 201, f"Setup failed: POST returned {response.status_code}: {response.text}"
#         return supplier

#     yield factory

#     for supplier_id in created:
#         requests.delete(_data['url'] + f'suppliers/{supplier_id}', headers=headers)

# #Testing read
# def test_GET_suppliers_returns_list_of_suppliers(_data):
#     '''every supplier in the list has an id and a name'''
#     headers = {"API_KEY": _data['api_key']}

#     response = requests.get(_data['url'] + 'suppliers', headers=headers)

#     assert response.status_code == 200
#     suppliers = response.json()
#     assert isinstance(suppliers, list), "API returned a non-list response"
#     for supplier in suppliers:
#         assert "id" in supplier and "name" in supplier, f"Supplier is missing id or name: {supplier}"


# def test_GET_supplier_by_id_returns_requested_supplier(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     response = requests.get(_data['url'] + f"suppliers/{supplier['id']}", headers=headers)

#     assert response.status_code == 200
#     assert response.json()["id"] == supplier["id"]
#     assert response.json()["name"] == supplier["name"]


# def test_GET_supplier_unknown_id(_data):
#     headers = {"API_KEY": _data['api_key']}

#     response = requests.get(_data['url'] + 'suppliers/987654321', headers=headers)

#     assert is_not_found(response), f"Expected not found, got {response.status_code}: {response.text[:200]}"


# def test_GET_supplier_items(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     response = requests.get(_data['url'] + f"suppliers/{supplier['id']}/items", headers=headers)

#     assert response.status_code == 200
#     assert isinstance(response.json(), list), "Items of a supplier should be a list"


# def test_GET_supplier_items_unknown_supplier(_data):
#     headers = {"API_KEY": _data['api_key']}

#     response = requests.get(_data['url'] + 'suppliers/987654321/items', headers=headers)

#     # A missing supplier must not produce a server error
#     assert response.status_code < 500


# def test_GET_suppliers_without_api_key(_data):
#     response = requests.get(_data['url'] + 'suppliers')

#     assert response.status_code in UNAUTHORIZED


# def test_GET_suppliers_with_wrong_api_key(_data):
#     response = requests.get(_data['url'] + 'suppliers', headers={"API_KEY": "not-a-real-key"})

#     assert response.status_code in UNAUTHORIZED


# #Testing create

# def test_POST_supplier_appears_in_list(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     suppliers = requests.get(_data['url'] + 'suppliers', headers=headers).json()

#     assert supplier["id"] in [s["id"] for s in suppliers], "Created supplier is missing from the supplier list"


# def test_POST_supplier_can_be_read_back_with_same_data(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     stored = requests.get(_data['url'] + f"suppliers/{supplier['id']}", headers=headers).json()

#     for field in ("name", "address", "city", "zip_code", "province", "country"):
#         assert stored[field] == supplier[field], f"Field '{field}' was stored incorrectly"


# def test_POST_supplier_duplicate_id_is_rejected(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     second = requests.post(_data['url'] + 'suppliers', headers=headers, json=supplier)

#     assert second.status_code in REJECTED, (
#         f"Duplicate supplier id {supplier['id']} was accepted with status {second.status_code}"
#     )


# def test_POST_supplier_duplicate_id_does_not_add_second_record(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     requests.post(_data['url'] + 'suppliers', headers=headers, json=supplier)

#     suppliers = requests.get(_data['url'] + 'suppliers', headers=headers).json()
#     assert [s["id"] for s in suppliers].count(supplier["id"]) == 1, "Duplicate supplier was stored"


# def test_POST_supplier_duplicate_id_does_not_overwrite_original(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier(name="Original Name")

#     requests.post(_data['url'] + 'suppliers', headers=headers, json=dict(supplier, name="Duplicate Attempt"))

#     stored = requests.get(_data['url'] + f"suppliers/{supplier['id']}", headers=headers).json()
#     assert stored["name"] == "Original Name", "A rejected duplicate changed the stored supplier"


# def test_POST_supplier_with_same_name_but_new_id_is_accepted(_data, new_supplier):
#     '''only the id has to be unique, two suppliers may share a name'''
#     headers = {"API_KEY": _data['api_key']}
#     first = new_supplier(name="Shared Name Supplier")
#     second = new_supplier(create=False, name="Shared Name Supplier")

#     response = requests.post(_data['url'] + 'suppliers', headers=headers, json=second)

#     assert response.status_code == 201, "A supplier with a shared name but a new id was rejected"
#     assert first["id"] != second["id"]


# def test_POST_supplier_empty_body_is_rejected(_data):
#     headers = {"API_KEY": _data['api_key']}

#     response = requests.post(_data['url'] + 'suppliers', headers=headers, json={})

#     assert response.status_code in REJECTED


# def test_POST_supplier_missing_required_fields_is_rejected(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier(create=False)

#     response = requests.post(_data['url'] + 'suppliers', headers=headers, json={"id": supplier["id"]})

#     assert response.status_code in REJECTED, "A supplier with only an id was accepted"


# def test_POST_supplier_without_api_key(_data, new_supplier):
#     supplier = new_supplier(create=False)

#     response = requests.post(_data['url'] + 'suppliers', json=supplier)

#     assert response.status_code in UNAUTHORIZED


# #Testing update

# def test_PUT_supplier_updates_changed_fields(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()
#     changes = {"name": "Renamed Supplier", "city": "Amsterdam", "address": "Damrak 1"}

#     response = requests.put(_data['url'] + f"suppliers/{supplier['id']}", headers=headers,
#                             json=dict(supplier, **changes))

#     assert response.status_code == 200
#     stored = requests.get(_data['url'] + f"suppliers/{supplier['id']}", headers=headers).json()
#     for field, value in changes.items():
#         assert stored[field] == value, f"Field '{field}' was not updated. Expected {value}, got {stored[field]}"


# def test_PUT_supplier_keeps_id(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     requests.put(_data['url'] + f"suppliers/{supplier['id']}", headers=headers,
#                  json=dict(supplier, name="Renamed Supplier"))

#     stored = requests.get(_data['url'] + f"suppliers/{supplier['id']}", headers=headers).json()
#     assert stored["id"] == supplier["id"]


# def test_PUT_supplier_unknown_id(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier(create=False)

#     response = requests.put(_data['url'] + 'suppliers/987654321', headers=headers, json=supplier)

#     assert is_not_found(response) or response.status_code == 404


# def test_PUT_supplier_without_api_key(_data, new_supplier):
#     supplier = new_supplier()

#     response = requests.put(_data['url'] + f"suppliers/{supplier['id']}", json=dict(supplier, name="No Key"))

#     assert response.status_code in UNAUTHORIZED


# #Testing delete

# def test_DELETE_supplier_removes_it_from_list(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     response = requests.delete(_data['url'] + f"suppliers/{supplier['id']}", headers=headers)

#     assert response.status_code == 200
#     suppliers = requests.get(_data['url'] + 'suppliers', headers=headers).json()
#     assert supplier["id"] not in [s["id"] for s in suppliers], "Deleted supplier is still in the list"


# def test_DELETE_supplier_twice(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()
#     requests.delete(_data['url'] + f"suppliers/{supplier['id']}", headers=headers)

#     second = requests.delete(_data['url'] + f"suppliers/{supplier['id']}", headers=headers)

#     assert second.status_code == 404, f"Second delete returned {second.status_code}"


# def test_DELETE_supplier_unknown_id(_data):
#     headers = {"API_KEY": _data['api_key']}

#     response = requests.delete(_data['url'] + 'suppliers/987654321', headers=headers)

#     assert response.status_code == 404


# def test_DELETE_supplier_without_api_key(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()

#     response = requests.delete(_data['url'] + f"suppliers/{supplier['id']}")

#     assert response.status_code in UNAUTHORIZED
#     # The supplier must still exist
#     assert requests.get(_data['url'] + f"suppliers/{supplier['id']}", headers=headers).status_code == 200


# def test_supplier_can_be_recreated_after_delete(_data, new_supplier):
#     headers = {"API_KEY": _data['api_key']}
#     supplier = new_supplier()
#     requests.delete(_data['url'] + f"suppliers/{supplier['id']}", headers=headers)

#     response = requests.post(_data['url'] + 'suppliers', headers=headers, json=supplier)

#     assert response.status_code == 201, "A deleted supplier id could not be reused"