
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
 
def test_get_item_groups(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 200 and a list
    assert response.status_code == 200
    assert type(response.json()) == list
 
 
def test_get_item_group_by_id(_data):
    url = _data['url'] + 'item_groups/1'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 200 and item group 1
    assert response.status_code == 200
    assert response.json()['id'] == 1
 
 
def test_get_items_in_item_group(_data):
    url = _data['url'] + 'item_groups/1/items'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 200 and a list
    assert response.status_code == 200
    assert type(response.json()) == list
 
 
def test_get_items_in_item_group_gives_full_items(_data):
    url = _data['url'] + 'item_groups/1/items'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give the full items of group 1, not only the ids
    for item in response.json():
        assert type(item) == dict
        assert item['item_group_id'] == 1
 
 
def test_get_items_in_item_group_match_items(_data):
    url = _data['url']
 
    all_items = requests.get(url + 'items', headers={'API_KEY': _data['api_key']}).json()
    response = requests.get(url + 'item_groups/1/items', headers={'API_KEY': _data['api_key']})
 
    # Should give exactly the items that have item_group_id 1
    expected_ids = [x['id'] for x in all_items if x['item_group_id'] == 1]
    found_ids = [x['id'] if type(x) == dict else x for x in response.json()]
    assert sorted(found_ids) == sorted(expected_ids)
 
 
def test_post_item_group(_data):
    url = _data['url'] + 'item_groups'
 
    new_item_group = {
        'id': 99999,
        'name': 'Test groep',
        'description': 'Temperature/handling regime: Test',
    }
 
    response = requests.post(url, json=new_item_group, headers={'API_KEY': _data['api_key']})
 
    # Should give 201
    assert response.status_code == 201
 
    # Check if the item group is really saved
    response = requests.get(url + '/99999', headers={'API_KEY': _data['api_key']})
    assert response.json() is not None
    assert response.json()['name'] == 'Test groep'
 
 
def test_post_item_group_with_receiving_key(_data):
    url = _data['url'] + 'item_groups'
 
    new_item_group = {
        'id': 99998,
        'name': 'Test groep receiving',
        'description': 'Temperature/handling regime: Test',
    }
 
    response = requests.post(url, json=new_item_group, headers={'API_KEY': _data['receiving_key']})
 
    # Receiving may also POST item groups, should give 201
    assert response.status_code == 201
 
 
def test_put_item_group(_data):
    url = _data['url'] + 'item_groups/2'
 
    item_group = requests.get(url, headers={'API_KEY': _data['api_key']}).json()
    item_group['description'] = 'Aangepast door test'
 
    response = requests.put(url, json=item_group, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
 
    # Check if the item group is really changed
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.json()['description'] == 'Aangepast door test'
 
 
def test_delete_item_group(_data):
    url = _data['url'] + 'item_groups'
 
    # First make an item group without items, so no real data is deleted
    new_item_group = {'id': 99997, 'name': 'Te verwijderen', 'description': 'Test'}
    requests.post(url, json=new_item_group, headers={'API_KEY': _data['api_key']})
 
    response = requests.delete(url + '/99997', headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
 
    # Check if the item group is really deleted
    response = requests.get(url + '/99997', headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404
 
 
# Bad flow
 
def test_get_item_groups_trailing_slash(_data):
    url = _data['url'] + 'item_groups/'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    assert response.status_code == 200
 
 
def test_get_item_group_negative_id(_data):
    url = _data['url'] + 'item_groups/-1'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404
    assert response.status_code == 404
 
 
def test_get_item_group_that_does_not_exist(_data):
    url = _data['url'] + 'item_groups/999999'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404
    assert response.status_code == 404
 
 
def test_get_items_of_item_group_negative_id(_data):
    url = _data['url'] + 'item_groups/-1/items'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404, not an empty list
    assert response.status_code == 404
 
 
def test_get_items_of_item_group_that_does_not_exist(_data):
    url = _data['url'] + 'item_groups/999999/items'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404, not an empty list
    assert response.status_code == 404
 
 
def test_get_item_group_wrong_path(_data):
    url = _data['url'] + 'item_groups/1/qwerty'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    assert response.status_code == 404
 
 
def test_put_item_group_that_does_not_exist(_data):
    url = _data['url'] + 'item_groups/999999'
 
    response = requests.put(url, json={'id': 999999, 'name': 'Bestaat niet'}, headers={'API_KEY': _data['api_key']})
 
    # Should give 404
    assert response.status_code == 404
 
 
def test_delete_item_group_that_does_not_exist(_data):
    url = _data['url'] + 'item_groups/999999'
 
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404
    assert response.status_code == 404
 
 
def test_delete_item_group_negative_id(_data):
    url = _data['url'] + 'item_groups/-1'
 
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404
    assert response.status_code == 404
 
 
# Validation flow
 
def test_post_item_group_empty_body(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.post(url, json={}, headers={'API_KEY': _data['api_key']})
 
    # Should give 400
    assert response.status_code == 400
 
 
def test_post_item_group_existing_id(_data):
    url = _data['url'] + 'item_groups'
 
    # Item group 1 already exists
    response = requests.post(url, json={'id': 1, 'name': 'Vers'}, headers={'API_KEY': _data['api_key']})
 
    # Should not give 201
    assert response.status_code != 201
 
 
def test_post_item_group_without_name(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.post(url, json={'id': 99996, 'description': 'Geen naam'}, headers={'API_KEY': _data['api_key']})
 
    # Name is missing, should give 400
    assert response.status_code == 400
 
 
def test_put_item_group_different_id_in_body(_data):
    url = _data['url'] + 'item_groups/1'
 
    # Id 2 in the body, but id 1 in the url
    response = requests.put(url, json={'id': 2, 'name': 'Vers'}, headers={'API_KEY': _data['api_key']})
 
    # Should give 400
    assert response.status_code == 400
 
 
def test_put_item_group_partial_body(_data):
    url = _data['url'] + 'item_groups/1'
 
    # Only the name, all other fields are missing
    response = requests.put(url, json={'name': 'Alleen naam'}, headers={'API_KEY': _data['api_key']})
 
    # Should give 400
    assert response.status_code == 400
 
 
def test_delete_item_group_with_items(_data):
    url = _data['url'] + 'item_groups/3'
 
    # Item group 3 still has items
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 409, items may not lose their group
    assert response.status_code == 409
 
 
# Error flow
 
def test_get_item_group_id_not_a_number(_data):
    url = _data['url'] + 'item_groups/abc'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_get_items_of_item_group_id_not_a_number(_data):
    url = _data['url'] + 'item_groups/abc/items'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_post_item_group_broken_json(_data):
    url = _data['url'] + 'item_groups'
 
    broken_json = '{"id": 99995, "name": '
 
    response = requests.post(url, data=broken_json, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_post_item_group_without_body(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.post(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_put_item_group_id_not_a_number(_data):
    url = _data['url'] + 'item_groups/abc'
 
    response = requests.put(url, json={'id': 1, 'name': 'Vers'}, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_put_item_group_broken_json(_data):
    url = _data['url'] + 'item_groups/1'
 
    broken_json = '{"id": 1, "name": '
 
    response = requests.put(url, data=broken_json, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_delete_item_group_id_not_a_number(_data):
    url = _data['url'] + 'item_groups/abc'
 
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
# Security flow
 
def test_get_item_groups_without_api_key(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.get(url)
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_get_item_groups_with_wrong_api_key(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.get(url, headers={'API_KEY': 'verzonnenkey123'})
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_get_items_of_item_group_without_api_key(_data):
    url = _data['url'] + 'item_groups/1/items'
 
    response = requests.get(url)
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_post_item_group_with_analytics_key(_data):
    url = _data['url'] + 'item_groups'
 
    response = requests.post(url, headers={'API_KEY': _data['analytics_key']})
 
    # Should give 403
    assert response.status_code == 403
 
 
def test_put_item_group_with_analytics_key(_data):
    url = _data['url'] + 'item_groups/1'
 
    response = requests.put(url, headers={'API_KEY': _data['analytics_key']})
 
    # Should give 403
    assert response.status_code == 403
 
 
def test_delete_item_group_with_receiving_key(_data):
    url = _data['url'] + 'item_groups/1'
 
    response = requests.delete(url, headers={'API_KEY': _data['receiving_key']})
 
    # Should give 403
    assert response.status_code == 403
 
 
def test_delete_item_group_with_analytics_key(_data):
    url = _data['url'] + 'item_groups/1'
 
    response = requests.delete(url, headers={'API_KEY': _data['analytics_key']})
 
    # Should give 403
    assert response.status_code == 403
 
 
def test_delete_item_group_without_api_key(_data):
    url = _data['url'] + 'item_groups/1'
 
    response = requests.delete(url)
 
    # Should give 401
    assert response.status_code == 401
 