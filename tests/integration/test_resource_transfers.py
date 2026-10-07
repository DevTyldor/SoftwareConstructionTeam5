import pytest
import requests


@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',
        'receiving_key': 'r2e4c6e8i0v3i5n7g9s',
    }


# Happy flow

def test_get_transfers(_data):
    url = _data['url'] + 'transfers'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and a list
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_transfer_by_id(_data):
    url = _data['url'] + 'transfers/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and transfer 1 with items
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert 'items' in response.json()


def test_get_transfer_items(_data):
    url = _data['url'] + 'transfers/1/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and every item has an item_id and amount
    assert response.status_code == 200
    for item in response.json():
        assert 'item_id' in item
        assert 'amount' in item


def test_post_transfer(_data):
    url = _data['url'] + 'transfers'

    new_transfer = {
        'id': 99999,
        'reference': 'TRF-099999',
        'from_location_id': 369,
        'to_location_id': 320,
        'items': [
            {'item_id': 190, 'amount': 10}
        ]
    }

    response = requests.post(url, json=new_transfer, headers={'API_KEY': _data['receiving_key']})

    # Should give 201
    assert response.status_code == 201

    # Check if the transfer is really saved
    response = requests.get(url + '/99999', headers={'API_KEY': _data['api_key']})
    assert response.json() is not None
    assert response.json()['reference'] == 'TRF-099999'


# Bad flow

def test_get_transfer_negative_id(_data):
    url = _data['url'] + 'transfers/-1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_transfer_that_does_not_exist(_data):
    url = _data['url'] + 'transfers/999999'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_items_of_negative_id(_data):
    url = _data['url'] + 'transfers/-1/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_transfer_wrong_path(_data):
    url = _data['url'] + 'transfers/1/qwerty'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


# Validation flow

def test_post_transfer_empty_body(_data):
    url = _data['url'] + 'transfers'

    response = requests.post(url, json={}, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_transfer_negative_amount(_data):
    url = _data['url'] + 'transfers'

    new_transfer = {
        'id': 99998,
        'reference': 'TRF-099998',
        'from_location_id': 369,
        'to_location_id': 320,
        'items': [
            {'item_id': 190, 'amount': -50}
        ]
    }

    response = requests.post(url, json=new_transfer, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


def test_put_transfer_different_id_in_body(_data):
    url = _data['url'] + 'transfers/1'

    # Id 2 in the body but id 1 in the url
    transfer = {
        'id': 2,
        'reference': 'TRF-000001',
        'from_location_id': 369,
        'to_location_id': 320,
    }

    response = requests.put(url, json=transfer, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


# Error flow

def test_get_transfer_id_not_a_number(_data):
    url = _data['url'] + 'transfers/abc'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_post_transfer_broken_json(_data):
    url = _data['url'] + 'transfers'

    # Broken json
    broken_json = '{"id": 99997, "reference": '

    response = requests.post(url, data=broken_json, headers={'API_KEY': _data['receiving_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_commit_transfer_that_does_not_exist(_data):
    url = _data['url'] + 'transfers/999999/commit'

    response = requests.put(url, headers={'API_KEY': _data['receiving_key']})

    # Should give 404, not 500
    assert response.status_code == 404


# Security flow

def test_get_transfers_without_api_key(_data):
    url = _data['url'] + 'transfers'

    response = requests.get(url)

    # Should give 401
    assert response.status_code == 401


def test_get_transfers_with_wrong_api_key(_data):
    url = _data['url'] + 'transfers'

    response = requests.get(url, headers={'API_KEY': 'qwerty'})

    # Should give 401
    assert response.status_code == 401


def test_commit_transfer_with_wrong_api_key(_data):
    url = _data['url'] + 'transfers/1/commit'

    response = requests.put(url, headers={'API_KEY': 'qwerty'})

    # Should give 401
    assert response.status_code == 401


def test_post_transfer_with_facility_key(_data):
    url = _data['url'] + 'transfers'

    response = requests.post(url, headers={'API_KEY': _data['api_key']})

    # Should give 403
    assert response.status_code == 403


def test_commit_transfer_with_facility_key(_data):
    url = _data['url'] + 'transfers/1/commit'

    response = requests.put(url, headers={'API_KEY': _data['api_key']})

    # Should give 403
    assert response.status_code == 403


def test_delete_transfer(_data):
    url = _data['url'] + 'transfers/1'

    response = requests.delete(url, headers={'API_KEY': _data['receiving_key']})

    # Should give 403
    assert response.status_code == 403