import http.client
from concurrent.futures import ThreadPoolExecutor

import pytest
import requests


@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',
        'receiving_key': 'r2e4c6e8i0v3i5n7g9s',
        'analytics_key': 'd4s2a0b0a1n4a0l0y7t',
    }


# Happy flow

def test_get_item_types(_data):
    url = _data['url'] + 'item_types'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and a list
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_item_type_by_id(_data):
    url = _data['url'] + 'item_types/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and item type 1
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_get_items_of_item_type(_data):
    url = _data['url'] + 'item_types/1/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and the items themselves and not only the ids
    assert response.status_code == 200
    assert len(response.json()) > 0
    for item in response.json():
        assert type(item) == dict
        assert item['item_type_id'] == 1


def test_post_item_type(_data):
    url = _data['url'] + 'item_types'

    new_item_type = {'id': 99901, 'name': 'qwerty', 'description': 'qwerty'}

    response = requests.post(url, json=new_item_type, headers={'API_KEY': _data['api_key']})

    # Should give 201
    assert response.status_code == 201

    # Check if the item type is really saved
    response = requests.get(url + '/99901', headers={'API_KEY': _data['api_key']})
    assert response.json() is not None
    assert response.json()['name'] == 'qwerty'

    # Clean up
    requests.delete(url + '/99901', headers={'API_KEY': _data['api_key']})


def test_put_item_type(_data):
    url = _data['url'] + 'item_types/3'

    original = requests.get(url, headers={'API_KEY': _data['api_key']}).json()
    changed = dict(original)
    changed['name'] = 'qwerty'

    response = requests.put(url, json=changed, headers={'API_KEY': _data['api_key']})

    # Should give 200
    assert response.status_code == 200

    # Check if the name is really changed
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    name = response.json()['name']

    # Put the original back
    requests.put(url, json=original, headers={'API_KEY': _data['api_key']})

    assert name == 'qwerty'


def test_delete_item_type(_data):
    url = _data['url'] + 'item_types'

    # Make a new one so we don't delete real data
    new_item_type = {'id': 99902, 'name': 'qwerty', 'description': 'qwerty'}
    requests.post(url, json=new_item_type, headers={'API_KEY': _data['api_key']})

    response = requests.delete(url + '/99902', headers={'API_KEY': _data['api_key']})

    # Should give 200
    assert response.status_code == 200

    # Check if the item type is really gone
    response = requests.get(url + '/99902', headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404


# Bad flow

def test_get_item_type_negative_id(_data):
    url = _data['url'] + 'item_types/-1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_item_type_that_does_not_exist(_data):
    url = _data['url'] + 'item_types/999999'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_items_of_negative_id(_data):
    url = _data['url'] + 'item_types/-1/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_item_type_wrong_path(_data):
    url = _data['url'] + 'item_types/1/qwerty'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_item_type_too_many_parts(_data):
    url = _data['url'] + 'item_types/1/2/3'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_put_item_type_that_does_not_exist(_data):
    url = _data['url'] + 'item_types/999999'

    item_type = {'id': 999999, 'name': 'qwerty', 'description': 'qwerty'}

    response = requests.put(url, json=item_type, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_delete_item_type_that_does_not_exist(_data):
    url = _data['url'] + 'item_types/999999'

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


# Validation flow

def test_post_item_type_empty_body(_data):
    url = _data['url'] + 'item_types'

    response = requests.post(url, json={}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_type_without_name(_data):
    url = _data['url'] + 'item_types'

    response = requests.post(url, json={'id': 99903, 'description': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_type_negative_id(_data):
    url = _data['url'] + 'item_types'

    response = requests.post(url, json={'id': -5, 'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_type_id_not_a_number(_data):
    url = _data['url'] + 'item_types'

    response = requests.post(url, json={'id': 'abc', 'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_type_id_already_exists(_data):
    url = _data['url'] + 'item_types'

    # Id 1 already exists
    response = requests.post(url, json={'id': 1, 'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 409
    assert response.status_code == 409


def test_post_item_type_twice_at_the_same_time(_data):
    url = _data['url'] + 'item_types'
    item_type = {'id': 99904, 'name': 'qwerty', 'description': 'qwerty'}

    # Send the same post 2 times at the same time
    # https://stackoverflow.com/a/40392029
    # https://www.reddit.com/r/learnpython/comments/ei57y3/requestsget_how_to_submit_multiple_simultaneous/
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(requests.post, url, json=item_type, headers={'API_KEY': _data['api_key']})
            for _ in range(2)
        ]
        codes = [future.result().status_code for future in futures]

    # Clean up
    requests.delete(url + '/99904', headers={'API_KEY': _data['api_key']})

    # Only 1 of them may work
    assert codes.count(201) == 1


def test_put_item_type_different_id_in_body(_data):
    url = _data['url'] + 'item_types/1'

    # Id 2 in the bodyy but id 1 in the url
    item_type = {'id': 2, 'name': 'qwerty', 'description': 'qwerty'}

    response = requests.put(url, json=item_type, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_put_item_type_only_one_field(_data):
    url = _data['url'] + 'item_types/3'

    original = requests.get(url, headers={'API_KEY': _data['api_key']}).json()

    response = requests.put(url, json={'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    name = requests.get(url, headers={'API_KEY': _data['api_key']}).json()['name']

    # Put the original back
    requests.put(url, json=original, headers={'API_KEY': _data['api_key']})

    # Should give 400 or 200 and then the name should really be changed
    assert response.status_code in (200, 400)
    if response.status_code == 200:
        assert name == 'qwerty'


# Error flow

def test_get_item_type_id_not_a_number(_data):
    url = _data['url'] + 'item_types/abc'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_post_item_type_broken_json(_data):
    url = _data['url'] + 'item_types'

    # This is not valid json
    broken_json = '{"id": 99905, "name": '

    response = requests.post(url, data=broken_json, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


# Security flow

def test_get_item_types_without_api_key(_data):
    url = _data['url'] + 'item_types'

    response = requests.get(url)

    # Should give 401
    assert response.status_code == 401


def test_get_item_types_with_wrong_api_key(_data):
    url = _data['url'] + 'item_types'

    response = requests.get(url, headers={'API_KEY': 'verzonnenkey123'})

    # Should give 401
    assert response.status_code == 401


def test_post_item_type_with_analytics_key(_data):
    url = _data['url'] + 'item_types'

    # Analytics key cant post on item_types
    response = requests.post(url, headers={'API_KEY': _data['analytics_key']})

    # Should give 403
    assert response.status_code == 403


def test_put_item_type_with_analytics_key(_data):
    url = _data['url'] + 'item_types/1'

    # Analytics key cant put on item_types
    response = requests.put(url, headers={'API_KEY': _data['analytics_key']})

    # Should give 403
    assert response.status_code == 403


def test_delete_item_type_with_receiving_key(_data):
    url = _data['url'] + 'item_types/1'

    # Receiving key cant delete on item_types
    response = requests.delete(url, headers={'API_KEY': _data['receiving_key']})

    # Should give 403
    assert response.status_code == 403
