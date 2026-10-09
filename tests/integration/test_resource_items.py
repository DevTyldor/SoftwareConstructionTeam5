
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
 
def test_get_items_with_analytics_key(_data):
    url = _data['url'] + 'items'
 
    response = requests.get(url, headers={'API_KEY': _data['analytics_key']})
 
    # Should give 200
    assert response.status_code == 200
    assert type(response.json()) == list
 
 
def test_get_item_inventory(_data):
    url = _data['url'] + 'items/1/inventory'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 200 and only inventory of item 1
    assert response.status_code == 200
    assert type(response.json()) == list
    for inventory in response.json():
        assert inventory['item_id'] == 1
 
 
def test_get_item_inventory_totals(_data):
    url = _data['url'] + 'items/1/inventory/totals'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 200 and all totals
    assert response.status_code == 200
    assert 'total_expected' in response.json()
    assert 'total_ordered' in response.json()
    assert 'total_allocated' in response.json()
    assert 'total_available' in response.json()
 
 
def test_get_item_inventory_totals_match_inventory(_data):
    url = _data['url'] + 'items/1/inventory'
 
    inventories = requests.get(url, headers={'API_KEY': _data['api_key']}).json()
    totals = requests.get(url + '/totals', headers={'API_KEY': _data['api_key']}).json()
 
    assert totals['total_expected'] == sum(x['quantity_expected'] for x in inventories)
    assert totals['total_ordered'] == sum(x['quantity_ordered'] for x in inventories)
    assert totals['total_allocated'] == sum(x['quantity_allocated'] for x in inventories)
    assert totals['total_available'] == sum(x['quantity_on_hand'] - x['quantity_allocated'] for x in inventories)
 
 
# Bad flow
 
def test_get_items_trailing_slash(_data):
    url = _data['url'] + 'items/'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    assert response.status_code == 200
 
 
def test_get_item_zero_id(_data):
    url = _data['url'] + 'items/0'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404
    assert response.status_code == 404

 
def test_get_inventory_of_item_that_does_not_exist(_data):
    url = _data['url'] + 'items/999999/inventory'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404, not an empty list
    assert response.status_code == 404
 
 
def test_get_inventory_totals_of_negative_id(_data):
    url = _data['url'] + 'items/-1/inventory/totals'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404, not totals of 0
    assert response.status_code == 404
 
 
def test_get_inventory_totals_of_item_that_does_not_exist(_data):
    url = _data['url'] + 'items/999999/inventory/totals'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 404, not totals of 0
    assert response.status_code == 404
 
 
def test_get_inventory_wrong_path(_data):
    url = _data['url'] + 'items/1/inventory/qwerty'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    assert response.status_code == 404
 
 
def test_put_item_negative_id(_data):
    url = _data['url'] + 'items/-1'
 
    response = requests.put(url, json={'id': -1, 'code': 'ITM-000000'}, headers={'API_KEY': _data['receiving_key']})
 
    # Should give 404
    assert response.status_code == 404
 
 
# Validation flow
 
def test_post_item_wrong_type(_data):
    url = _data['url'] + 'items'
 
    new_item = {'id': 99995, 'code': 'ITM-099995', 'unit_weight': 'zwaar', 'item_line_id': 5}
 
    response = requests.post(url, json=new_item, headers={'API_KEY': _data['receiving_key']})
 
    # unit_weight is not a number, should give 400
    assert response.status_code == 400
 
 
def test_post_item_item_group_does_not_exist(_data):
    url = _data['url'] + 'items'
 
    new_item = {
        'id': 99993,
        'code': 'ITM-099993',
        'description': 'Test item',
        'unit_weight': 0.5,
        'item_line_id': 5,
        'item_group_id': 999999,
        'item_type_id': 2,
        'supplier_id': 17,
    }
 
    response = requests.post(url, json=new_item, headers={'API_KEY': _data['receiving_key']})
 
    # Item group 999999 does not exist, should give 400
    assert response.status_code == 400
 
 
def test_put_item_partial_body(_data):
    url = _data['url'] + 'items/3'
 
    # Only the description, all other fields are missing
    response = requests.put(url, json={'description': 'Alleen beschrijving'}, headers={'API_KEY': _data['receiving_key']})
 
    # Should give 400
    assert response.status_code == 400
 
 
# Error flow
 
def test_get_inventory_id_not_a_number(_data):
    url = _data['url'] + 'items/abc/inventory'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_get_inventory_totals_id_not_a_number(_data):
    url = _data['url'] + 'items/abc/inventory/totals'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_get_item_id_is_decimal(_data):
    url = _data['url'] + 'items/1.5'
 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_post_item_without_body(_data):
    url = _data['url'] + 'items'
 
    response = requests.post(url, headers={'API_KEY': _data['receiving_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_put_item_id_not_a_number(_data):
    url = _data['url'] + 'items/abc'
 
    response = requests.put(url, json={'id': 1, 'code': 'ITM-000001'}, headers={'API_KEY': _data['receiving_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
def test_put_item_broken_json(_data):
    url = _data['url'] + 'items/1'
 
    broken_json = '{"id": 1, "code": '
 
    response = requests.put(url, data=broken_json, headers={'API_KEY': _data['receiving_key']})
 
    # Should give 400, not 500
    assert response.status_code == 400
 
 
# Security flow
 
def test_get_item_without_api_key(_data):
    url = _data['url'] + 'items/1'
 
    response = requests.get(url)
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_get_inventory_without_api_key(_data):
    url = _data['url'] + 'items/1/inventory'
 
    response = requests.get(url)
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_get_inventory_totals_without_api_key(_data):
    url = _data['url'] + 'items/1/inventory/totals'
 
    response = requests.get(url)
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_post_item_without_api_key(_data):
    url = _data['url'] + 'items'
 
    response = requests.post(url, json={'id': 99992, 'code': 'ITM-099992'})
 
    # Should give 401
    assert response.status_code == 401
 
 
def test_put_item_with_analytics_key(_data):
    url = _data['url'] + 'items/1'
 
    response = requests.put(url, headers={'API_KEY': _data['analytics_key']})
 
    # Analytics may only GET items, should give 403
    assert response.status_code == 403
 
 
def test_delete_item_with_facility_key(_data):
    url = _data['url'] + 'items/1'
 
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
 
    # No key may delete items, should give 403
    assert response.status_code == 403
 
 
def test_delete_item_without_api_key(_data):
    url = _data['url'] + 'items/1'
 
    response = requests.delete(url)
 
    # Should give 401
    assert response.status_code == 401
 