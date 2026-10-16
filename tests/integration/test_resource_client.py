import os
import pytest
import requests

#This file runs integration tests on resource clients
@pytest.fixture
def _data():
    return {
        'url': 'http://127.0.0.1:3000/api/v1',
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
    '''create client with id 11'''
    id = 11
    url = _data['url'] + '/clients/{id}'
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

# Extra client tests
#
# These tests do not depend on client 1 (the tests above rename and delete it).
# They create their own clients with a unique id and delete them afterwards.
# Assumptions about the API: a rejected duplicate or invalid body gives 400/409/422,
# a missing or wrong API key gives 401/403, and an unknown id gives 404.
# REJECTED = (400, 409, 422)
# UNAUTHORIZED = (401, 403)


# @pytest.fixture
# def new_client(_data):
#     """Factory for test clients: new_client() creates one through the API,
#     new_client(create=False) only builds the payload. Created clients are
#     deleted again after the test."""
#     headers = {'API_KEY': _data['api_key']}
#     created = []

#     def factory(create=True, **overrides):
#         client = {
#             "id": 900000,
#             "name": "Test Client",
#             "address": "Laan van Mathenesse 9a",
#             "city": "Utrecht",
#             "zip_code": "2665 MZ",
#             "province": "Utrecht",
#             "country": "Netherlands",
#             "contact_phone": "0801-845146",
#             "contact_email": "test.client@example.com",
#             "created_at": "2024-02-11T05:19:57Z",
#             "updated_at": "2024-03-09T12:13:49Z"
#         }
#         client.update(overrides)
#         created.append(client["id"])
#         if create:
#             response = requests.post(_data['url'] + '/clients', headers=headers, json=client)
#             assert response.status_code == 201, f"Setup failed: POST returned {response.status_code}: {response.text}"
#         return client

#     yield factory

#     for client_id in created:
#         requests.delete(_data['url'] + f'/clients/{client_id}', headers=headers)

# #Testing read
# def test_GET_clients_returns_list_of_clients(_data):
#     headers = {'API_KEY': _data['api_key']}

#     response = requests.get(_data['url'] + '/clients', headers=headers)

#     assert response.status_code == 200
#     clients = response.json()
#     assert isinstance(clients, list), "API returned a non-list response"
#     for client in clients:
#         assert "id" in client and "name" in client, f"Client is missing id or name: {client}"


# def test_GET_client_by_id_returns_requested_client(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     response = requests.get(_data['url'] + f"/clients/{client['id']}", headers=headers)

#     assert response.status_code == 200
#     assert response.json()["id"] == client["id"]
#     assert response.json()["name"] == client["name"]


# def test_GET_client_unknown_id(_data):
#     headers = {'API_KEY': _data['api_key']}

#     response = requests.get(_data['url'] + '/clients/987654321', headers=headers)

#     assert response.status_code == 404


# def test_GET_client_orders(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     response = requests.get(_data['url'] + f"/clients/{client['id']}/orders", headers=headers)

#     assert response.status_code == 200
#     assert isinstance(response.json(), list), "Orders of a client should be a list"


# def test_GET_client_orders_unknown_client(_data):
#     headers = {'API_KEY': _data['api_key']}

#     response = requests.get(_data['url'] + '/clients/987654321/orders', headers=headers)

#     # A missing client must not produce a server error
#     assert response.status_code < 500


# def test_GET_clients_without_api_key(_data):
#     response = requests.get(_data['url'] + '/clients')

#     assert response.status_code in UNAUTHORIZED


# def test_GET_clients_with_wrong_api_key(_data):
#     response = requests.get(_data['url'] + '/clients', headers={'API_KEY': 'not-a-real-key'})

#     assert response.status_code in UNAUTHORIZED

# #Testing POST
# def test_POST_client_appears_in_list(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     clients = requests.get(_data['url'] + '/clients', headers=headers).json()

#     assert client["id"] in [c["id"] for c in clients], "Created client is missing from the client list"


# def test_POST_client_duplicate_id_is_rejected(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     second = requests.post(_data['url'] + '/clients', headers=headers, json=client)

#     assert second.status_code in REJECTED, (
#         f"Duplicate client id {client['id']} was accepted with status {second.status_code}"
#     )


# def test_POST_client_duplicate_id_does_not_add_second_record(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     requests.post(_data['url'] + '/clients', headers=headers, json=client)

#     clients = requests.get(_data['url'] + '/clients', headers=headers).json()
#     assert [c["id"] for c in clients].count(client["id"]) == 1, "Duplicate client was stored"


# def test_POST_client_duplicate_id_does_not_overwrite_original(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client(name="Original Name")

#     requests.post(_data['url'] + '/clients', headers=headers, json=dict(client, name="Duplicate Attempt"))

#     stored = requests.get(_data['url'] + f"/clients/{client['id']}", headers=headers).json()
#     assert stored["name"] == "Original Name", "A rejected duplicate changed the stored client"


# def test_POST_client_empty_body_is_rejected(_data):
#     headers = {'API_KEY': _data['api_key']}

#     response = requests.post(_data['url'] + '/clients', headers=headers, json={})

#     assert response.status_code in REJECTED


# def test_POST_client_missing_required_fields_is_rejected(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client(create=False)

#     response = requests.post(_data['url'] + '/clients', headers=headers, json={"id": client["id"]})

#     assert response.status_code in REJECTED, "A client with only an id was accepted"


# def test_POST_client_without_api_key(_data, new_client):
#     client = new_client(create=False)

#     response = requests.post(_data['url'] + '/clients', json=client)

#     assert response.status_code in UNAUTHORIZED

# #Testing update
# def test_PUT_client_updates_all_changed_fields(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()
#     changes = {"name": "Renamed Client", "city": "Amsterdam", "address": "Damrak 1"}

#     response = requests.put(_data['url'] + f"/clients/{client['id']}", headers=headers,
#                             json=dict(client, **changes))

#     assert response.status_code == 200
#     stored = requests.get(_data['url'] + f"/clients/{client['id']}", headers=headers).json()
#     for field, value in changes.items():
#         assert stored[field] == value, f"Field '{field}' was not updated. Expected {value}, got {stored[field]}"


# def test_PUT_client_keeps_id(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     requests.put(_data['url'] + f"/clients/{client['id']}", headers=headers,
#                  json=dict(client, name="Renamed Client"))

#     stored = requests.get(_data['url'] + f"/clients/{client['id']}", headers=headers).json()
#     assert stored["id"] == client["id"]


# def test_PUT_client_unknown_id(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client(create=False)

#     response = requests.put(_data['url'] + '/clients/987654321', headers=headers, json=client)

#     assert response.status_code == 404


# def test_PUT_client_without_api_key(_data, new_client):
#     client = new_client()

#     response = requests.put(_data['url'] + f"/clients/{client['id']}", json=dict(client, name="No Key"))

#     assert response.status_code in UNAUTHORIZED

# #Testing Delete
# def test_DELETE_client_removes_it_from_list(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     response = requests.delete(_data['url'] + f"/clients/{client['id']}", headers=headers)

#     assert response.status_code == 200
#     clients = requests.get(_data['url'] + '/clients', headers=headers).json()
#     assert client["id"] not in [c["id"] for c in clients], "Deleted client is still in the list"


# def test_DELETE_client_twice(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()
#     requests.delete(_data['url'] + f"/clients/{client['id']}", headers=headers)

#     second = requests.delete(_data['url'] + f"/clients/{client['id']}", headers=headers)

#     assert second.status_code == 404, f"Second delete returned {second.status_code}"


# def test_DELETE_client_unknown_id(_data):
#     headers = {'API_KEY': _data['api_key']}

#     response = requests.delete(_data['url'] + '/clients/987654321', headers=headers)

#     assert response.status_code == 404


# def test_DELETE_client_without_api_key(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()

#     response = requests.delete(_data['url'] + f"/clients/{client['id']}")

#     assert response.status_code in UNAUTHORIZED
#     # The client must still exist
#     assert requests.get(_data['url'] + f"/clients/{client['id']}", headers=headers).status_code == 200


# def test_client_can_be_recreated_after_delete(_data, new_client):
#     headers = {'API_KEY': _data['api_key']}
#     client = new_client()
#     requests.delete(_data['url'] + f"/clients/{client['id']}", headers=headers)

#     response = requests.post(_data['url'] + '/clients', headers=headers, json=client)

#     assert response.status_code == 201, "A deleted client id could not be reused"