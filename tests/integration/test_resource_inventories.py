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
        'smartglass_key': 's8m3a9r2t7g1l4a5s0s',
    }


# Happy flow

def test_get_inventories(_data):
    url = _data['url'] + 'inventories'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and a list
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_inventory_of_item(_data):
    url = _data['url'] + 'items/1/inventory'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and only rows of item 1
    assert response.status_code == 200
    for row in response.json():
        assert row['item_id'] == 1


def test_get_inventory_totals_of_item(_data):
    url = _data['url'] + 'items/1/inventory/totals'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 200 and the totals
    assert response.status_code == 200
    assert 'total_expected' in response.json()
    assert 'total_ordered' in response.json()
    assert 'total_allocated' in response.json()
    assert 'total_available' in response.json()


def test_post_inventory(_data):
    url = _data['url'] + 'inventories'

    new_inventory = {
        'item_id': 1,
        'location_id': 1,
        'quantity_on_hand': 123,
        'quantity_expected': 0,
        'quantity_ordered': 0,
        'quantity_allocated': 0,
    }

    response = requests.post(url, json=new_inventory, headers={'API_KEY': _data['receiving_key']})

    # Should give 201
    assert response.status_code == 201

    # Check if the inventory is really saved
    response = requests.get(_data['url'] + 'items/1/inventory', headers={'API_KEY': _data['api_key']})
    rows = [row for row in response.json() if row['location_id'] == 1]
    assert len(rows) == 1
    assert rows[0]['quantity_on_hand'] == 123


def test_post_inventory_that_already_exists(_data):
    url = _data['url'] + 'inventories'

    inventory = {
        'item_id': 1,
        'location_id': 1,
        'quantity_on_hand': 123,
        'quantity_expected': 0,
        'quantity_ordered': 0,
        'quantity_allocated': 0,
    }

    # Post it 2 times with a different quantity
    requests.post(url, json=inventory, headers={'API_KEY': _data['receiving_key']})
    inventory['quantity_on_hand'] = 456
    response = requests.post(url, json=inventory, headers={'API_KEY': _data['receiving_key']})

    # Should give 201
    assert response.status_code == 201

    # Should update the row and not make a second one
    response = requests.get(_data['url'] + 'items/1/inventory', headers={'API_KEY': _data['api_key']})
    rows = [row for row in response.json() if row['location_id'] == 1]
    assert len(rows) == 1
    assert rows[0]['quantity_on_hand'] == 456


# Bad flow

def test_get_inventory_by_id(_data):
    url = _data['url'] + 'inventories/1'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404 because inventories have no id
    assert response.status_code == 404


def test_put_inventory_by_id(_data):
    url = _data['url'] + 'inventories/1'

    response = requests.put(url, json={}, headers={'API_KEY': _data['receiving_key']})

    # Should give 404
    assert response.status_code == 404


def test_delete_inventory_by_id(_data):
    url = _data['url'] + 'inventories/1'

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # Should give 404 not 403
    assert response.status_code == 404


def test_get_inventory_of_negative_item_id(_data):
    url = _data['url'] + 'items/-1/inventory'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_inventory_of_item_that_does_not_exist(_data):
    url = _data['url'] + 'items/999999/inventory'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


def test_get_inventory_wrong_path(_data):
    url = _data['url'] + 'items/1/inventory/qwerty'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 404
    assert response.status_code == 404


# Validation flow

def test_post_inventory_empty_body(_data):
    url = _data['url'] + 'inventories'

    response = requests.post(url, json={}, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_inventory_without_item_id(_data):
    url = _data['url'] + 'inventories'

    response = requests.post(url, json={'location_id': 1, 'quantity_on_hand': 123}, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_inventory_without_location_id(_data):
    url = _data['url'] + 'inventories'

    response = requests.post(url, json={'item_id': 1, 'quantity_on_hand': 123}, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_inventory_negative_quantity(_data):
    url = _data['url'] + 'inventories'

    response = requests.post(url, json={'item_id': 1, 'location_id': 1, 'quantity_on_hand': -99}, headers={'API_KEY': _data['receiving_key']})

    # Should give 400
    assert response.status_code == 400


def test_post_inventory_item_does_not_exist(_data):
    url = _data['url'] + 'inventories'

    response = requests.post(url, json={'item_id': 999999, 'location_id': 1, 'quantity_on_hand': 123}, headers={'API_KEY': _data['receiving_key']})

    # Should give 404
    assert response.status_code == 404


def test_post_inventory_location_does_not_exist(_data):
    url = _data['url'] + 'inventories'

    response = requests.post(url, json={'item_id': 1, 'location_id': 999999, 'quantity_on_hand': 123}, headers={'API_KEY': _data['receiving_key']})

    # Should give 404
    assert response.status_code == 404


def test_post_inventory_twice_at_the_same_time(_data):
    url = _data['url'] + 'inventories'
    inventory = {'item_id': 1, 'location_id': 1, 'quantity_on_hand': 123}

    # Send the same post 2 times at the same time
    # https://stackoverflow.com/a/40392029
    # https://www.reddit.com/r/learnpython/comments/ei57y3/requestsget_how_to_submit_multiple_simultaneous/
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(requests.post, url, json=inventory, headers={'API_KEY': _data['receiving_key']})
            for _ in range(2)
        ]
        [future.result() for future in futures]

    # Should be only 1 row for this item and location
    response = requests.get(_data['url'] + 'items/1/inventory', headers={'API_KEY': _data['api_key']})
    rows = [row for row in response.json() if row['location_id'] == 1]
    assert len(rows) == 1


def test_commit_transfer_changes_inventory(_data):
    # Get the item and location of transfer 1
    transfer = requests.get(_data['url'] + 'transfers/1', headers={'API_KEY': _data['api_key']}).json()
    item_id = transfer['items'][0]['item_id']
    amount = transfer['items'][0]['amount']
    from_location_id = transfer['from_location_id']

    # Quantity before the commit
    rows = requests.get(_data['url'] + 'items/' + str(item_id) + '/inventory', headers={'API_KEY': _data['api_key']}).json()
    before = [row for row in rows if row['location_id'] == from_location_id][0]['quantity_on_hand']

    response = requests.put(_data['url'] + 'transfers/1/commit', headers={'API_KEY': _data['receiving_key']})

    # Should give 200
    assert response.status_code == 200

    # Quantity after the commit
    rows = requests.get(_data['url'] + 'items/' + str(item_id) + '/inventory', headers={'API_KEY': _data['api_key']}).json()
    after = [row for row in rows if row['location_id'] == from_location_id][0]['quantity_on_hand']

    # The amount should be gone from the from location
    assert after == before - amount


def test_commit_transfer_makes_quantity_negative(_data):
    # Use the item and location of transfer 1
    transfer = requests.get(_data['url'] + 'transfers/1', headers={'API_KEY': _data['api_key']}).json()

    # Way more than there is on hand
    new_transfer = {
        'id': 99990,
        'reference': 'TRF-099990',
        'from_location_id': transfer['from_location_id'],
        'to_location_id': transfer['to_location_id'],
        'items': [
            {'item_id': transfer['items'][0]['item_id'], 'amount': 999999}
        ]
    }
    requests.post(_data['url'] + 'transfers', json=new_transfer, headers={'API_KEY': _data['receiving_key']})

    response = requests.put(_data['url'] + 'transfers/99990/commit', headers={'API_KEY': _data['receiving_key']})

    # Should give 400 because the quantity cant be negative
    assert response.status_code == 400


# Error flow

def test_get_inventory_of_item_id_not_a_number(_data):
    url = _data['url'] + 'items/abc/inventory'

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Should give 400 not 500
    assert response.status_code == 400


def test_post_inventory_broken_json(_data):
    url = _data['url'] + 'inventories'

    # This is not valid json
    broken_json = '{"item_id": 1, "location_id": '

    response = requests.post(url, data=broken_json, headers={'API_KEY': _data['receiving_key']})

    # Should give 400 not 500
    assert response.status_code == 400


# Security flow

def test_get_inventories_without_api_key(_data):
    url = _data['url'] + 'inventories'

    response = requests.get(url)

    # Should give 401
    assert response.status_code == 401


def test_get_inventories_with_wrong_api_key(_data):
    url = _data['url'] + 'inventories'

    response = requests.get(url, headers={'API_KEY': 'verzonnenkey123'})

    # Should give 401
    assert response.status_code == 401


def test_post_inventory_with_analytics_key(_data):
    url = _data['url'] + 'inventories'

    # Analytics key cant post on inventories
    response = requests.post(url, headers={'API_KEY': _data['analytics_key']})

    # Should give 403
    assert response.status_code == 403


def test_put_inventory_with_facility_key(_data):
    url = _data['url'] + 'inventories/1'

    # Facility key cant put on inventories
    response = requests.put(url, headers={'API_KEY': _data['api_key']})

    # Should give 403
    assert response.status_code == 403


def test_commit_transfer_with_smartglass_key(_data):
    # Get the item and location of transfer 1
    transfer = requests.get(_data['url'] + 'transfers/1', headers={'API_KEY': _data['api_key']}).json()
    item_id = transfer['items'][0]['item_id']
    from_location_id = transfer['from_location_id']

    # Quantity before the commit
    rows = requests.get(_data['url'] + 'items/' + str(item_id) + '/inventory', headers={'API_KEY': _data['api_key']}).json()
    before = [row for row in rows if row['location_id'] == from_location_id][0]['quantity_on_hand']

    response = requests.put(_data['url'] + 'transfers/1/commit', headers={'API_KEY': _data['smartglass_key']})

    # Commit changes the inventories so it should give 403
    # or the inventories should really be changed
    assert response.status_code in (200, 403)
    if response.status_code == 200:
        rows = requests.get(_data['url'] + 'items/' + str(item_id) + '/inventory', headers={'API_KEY': _data['api_key']}).json()
        after = [row for row in rows if row['location_id'] == from_location_id][0]['quantity_on_hand']
        assert after != before
