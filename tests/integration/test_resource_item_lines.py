from concurrent.futures import ThreadPoolExecutor

import pytest
import requests


@pytest.fixture
def _data():
    return {
        'url': 'http://127.0.0.1:3000/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',
        'receiving_key': 'r2e4c6e8i0v3i5n7g9s',
        'analytics_key': 'd4s2a0b0a1n4a0l0y7t',
    }


# Happy flow

def test_get_item_lines(_data):
    url = _data['url'] + 'item_lines'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and a list
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_item_line_by_id(_data):
    url = _data['url'] + 'item_lines/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and item line 1
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_get_items_of_item_line(_data):
    url = _data['url'] + 'item_lines/1/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and the items themselves and not only the ids
    assert response.status_code == 200
    assert len(response.json()) > 0
    for item in response.json():
        assert type(item) == dict
        assert item['item_line_id'] == 1


def test_post_item_line(_data):
    url = _data['url'] + 'item_lines'

    new_item_line = {'id': 99981, 'name': 'qwerty', 'description': 'qwerty'}

    response = requests.post(url, json=new_item_line, headers={'API_KEY': _data['api_key']})

    # Should give 201
    assert response.status_code == 201

    # Check if the item line is really saved
    response = requests.get(url + '/99981', headers={'API_KEY': _data['api_key']})
    assert response.json() is not None
    assert response.json()['name'] == 'qwerty'

    # Clean up
    requests.delete(url + '/99981', headers={'API_KEY': _data['api_key']})


def test_post_item_line_with_receiving_key(_data):
    url = _data['url'] + 'item_lines'

    new_item_line = {'id': 99982, 'name': 'qwerty', 'description': 'qwerty'}

    # Receiving key may post on item_lines
    response = requests.post(url, json=new_item_line, headers={'API_KEY': _data['receiving_key']})

    # Clean up
    requests.delete(url + '/99982', headers={'API_KEY': _data['api_key']})

    # Should give 201
    assert response.status_code == 201


def test_put_item_line(_data):
    url = _data['url'] + 'item_lines/3'

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


def test_delete_item_line(_data):
    # Regression test for issue #122
    url = _data['url'] + 'item_lines'

    # Make a new one so we don't delete real data
    new_item_line = {'id': 99980, 'name': 'qwerty', 'description': 'qwerty'}
    requests.post(url, json=new_item_line, headers={'API_KEY': _data['api_key']})

    response = requests.delete(url + '/99980', headers={'API_KEY': _data['api_key']})

    # Should give 200
    assert response.status_code == 200

    # Check if the item line is really gone
    response = requests.get(url + '/99980', headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404


# Bad flow

def test_get_item_lines_trailing_slash(_data):
    url = _data['url'] + 'item_lines/'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200
    assert response.status_code == 200


def test_get_item_line_negative_id(_data):
    url = _data['url'] + 'item_lines/-1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_item_line_that_does_not_exist(_data):
    url = _data['url'] + 'item_lines/999999'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_items_of_item_line_that_does_not_exist(_data):
    url = _data['url'] + 'item_lines/999999/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404, not an empty list
    assert response.status_code == 404


def test_get_item_line_wrong_path(_data):
    url = _data['url'] + 'item_lines/1/qwerty'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_item_line_too_many_parts(_data):
    url = _data['url'] + 'item_lines/1/2/3'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_put_item_line_that_does_not_exist(_data):
    url = _data['url'] + 'item_lines/999999'

    item_line = {'id': 999999, 'name': 'qwerty', 'description': 'qwerty'}

    response = requests.put(url, json=item_line, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_delete_item_line_that_does_not_exist(_data):
    url = _data['url'] + 'item_lines/999999'

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


# Validation flow

@pytest.mark.skip(reason="Saves an item line without an id and breaks item_line.json until POST validates the body")
def test_post_item_line_empty_body(_data):
    url = _data['url'] + 'item_lines'

    response = requests.post(url, json={}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_line_without_name(_data):
    url = _data['url'] + 'item_lines'

    response = requests.post(url, json={'id': 99983, 'description': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Clean up in case it was saved anyway
    requests.delete(url + '/99983', headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_line_negative_id(_data):
    url = _data['url'] + 'item_lines'

    response = requests.post(url, json={'id': -5, 'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_line_id_not_a_number(_data):
    url = _data['url'] + 'item_lines'

    response = requests.post(url, json={'id': 'abc', 'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_item_line_id_already_exists(_data):
    url = _data['url'] + 'item_lines'
    item_line = {'id': 99984, 'name': 'qwerty', 'description': 'qwerty'}

    # Make it once, then post the same id again
    requests.post(url, json=item_line, headers={'API_KEY': _data['api_key']})
    response = requests.post(url, json=item_line, headers={'API_KEY': _data['api_key']})

    # Clean up (2 times in case it was saved twice)
    requests.delete(url + '/99984', headers={'API_KEY': _data['api_key']})
    requests.delete(url + '/99984', headers={'API_KEY': _data['api_key']})

    # Should give 409
    assert response.status_code == 409


def test_post_item_line_twice_at_the_same_time(_data):
    url = _data['url'] + 'item_lines'
    item_line = {'id': 99985, 'name': 'qwerty', 'description': 'qwerty'}

    # Send the same post 2 times at the same time
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(requests.post, url, json=item_line, headers={'API_KEY': _data['api_key']})
            for _ in range(2)
        ]
        codes = [future.result().status_code for future in futures]

    # Clean up (2 times in case it was saved twice)
    requests.delete(url + '/99985', headers={'API_KEY': _data['api_key']})
    requests.delete(url + '/99985', headers={'API_KEY': _data['api_key']})

    # Only 1 of them may work
    assert codes.count(201) == 1


def test_put_item_line_different_id_in_body(_data):
    url = _data['url'] + 'item_lines'

    # Make a new one so we don't change real data
    requests.post(url, json={'id': 99986, 'name': 'qwerty', 'description': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Id 99987 in the body but id 99986 in the url
    item_line = {'id': 99987, 'name': 'qwerty', 'description': 'qwerty'}
    response = requests.put(url + '/99986', json=item_line, headers={'API_KEY': _data['api_key']})

    # Clean up both ids in case the id was changed
    requests.delete(url + '/99986', headers={'API_KEY': _data['api_key']})
    requests.delete(url + '/99987', headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


@pytest.mark.skip(reason="Saves the item line without an id and breaks item_line.json until PUT validates the body")
def test_put_item_line_partial_body(_data):
    url = _data['url'] + 'item_lines/3'

    # Only the description, all other fields are missing
    response = requests.put(url, json={'description': 'Alleen beschrijving'}, headers={'API_KEY': _data['api_key']})

    # Should give 400
    assert response.status_code == 400


# Error flow

def test_get_item_line_id_not_a_number(_data):
    url = _data['url'] + 'item_lines/abc'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_get_items_of_item_line_id_not_a_number(_data):
    url = _data['url'] + 'item_lines/abc/items'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_post_item_line_broken_json(_data):
    url = _data['url'] + 'item_lines'

    # This is not valid json
    broken_json = '{"id": 99988, "name": '

    response = requests.post(url, data=broken_json, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_post_item_line_without_body(_data):
    url = _data['url'] + 'item_lines'

    response = requests.post(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_put_item_line_id_not_a_number(_data):
    url = _data['url'] + 'item_lines/abc'

    response = requests.put(url, json={'id': 1, 'name': 'qwerty'}, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_delete_item_line_id_not_a_number(_data):
    url = _data['url'] + 'item_lines/abc'

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


# Security flow

def test_get_item_lines_without_api_key(_data):
    url = _data['url'] + 'item_lines'

    response = requests.get(url)

    # Should give 401
    assert response.status_code == 401


def test_get_item_lines_with_wrong_api_key(_data):
    url = _data['url'] + 'item_lines'

    response = requests.get(url, headers={'API_KEY': 'verzonnenkey123'})

    # Should give 401
    assert response.status_code == 401


def test_get_items_of_item_line_without_api_key(_data):
    url = _data['url'] + 'item_lines/1/items'

    response = requests.get(url)

    # Should give 401
    assert response.status_code == 401


def test_post_item_line_with_analytics_key(_data):
    url = _data['url'] + 'item_lines'

    # Analytics key cant post on item_lines
    response = requests.post(url, headers={'API_KEY': _data['analytics_key']})

    # Should give 403
    assert response.status_code == 403


def test_put_item_line_with_analytics_key(_data):
    url = _data['url'] + 'item_lines/1'

    # Analytics key cant put on item_lines
    response = requests.put(url, headers={'API_KEY': _data['analytics_key']})

    # Should give 403
    assert response.status_code == 403


def test_delete_item_line_with_receiving_key(_data):
    url = _data['url'] + 'item_lines/1'

    # Receiving key cant delete on item_lines
    response = requests.delete(url, headers={'API_KEY': _data['receiving_key']})

    # Should give 403
    assert response.status_code == 403


def test_delete_item_line_with_analytics_key(_data):
    url = _data['url'] + 'item_lines/1'

    # Analytics key cant delete on item_lines
    response = requests.delete(url, headers={'API_KEY': _data['analytics_key']})

    # Should give 403
    assert response.status_code == 403


def test_delete_item_line_without_api_key(_data):
    url = _data['url'] + 'item_lines/1'

    response = requests.delete(url)

    # Should give 401
    assert response.status_code == 401