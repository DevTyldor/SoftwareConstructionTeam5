from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


# GET /items
# GET /items/{id}
# GET /items/{id}/inventory
# GET /items/{id}/inventory/totals
def handle_get_items(self, user, item_id=None, get_inventory=False, get_totals=False):
    if not check_access(self, user, "items", "get"):
        return

    if get_totals:
        items = data_provider.fetch_inventory_pool().get_inventory_totals_for_item(
            item_id
        )

    elif get_inventory:
        items = data_provider.fetch_inventory_pool().get_inventories_for_item(item_id)

    elif item_id is None:
        items = data_provider.fetch_item_pool().get_items()

    else:
        items = data_provider.fetch_item_pool().get_item(item_id)

    send_json(self, items)


# POST /items
def handle_post_items(self, user):
    if not check_access(self, user, "items", "post"):
        return

    new_item = read_json(self)

    item_manager = data_provider.fetch_item_pool()
    item_manager.add_item(new_item)
    item_manager.save()

    send_status(self, 201)


# PUT /items/{id}
def handle_put_items(self, user, item_id):
    if not check_access(self, user, "items", "put"):
        return

    updated_item = read_json(self)

    item_manager = data_provider.fetch_item_pool()
    item_manager.update_item(item_id, updated_item)
    item_manager.save()

    send_status(self, 200)


# DELETE /items/{id}
def handle_delete_items(self, user, item_id):
    if not check_access(self, user, "items", "delete"):
        return

    item_manager = data_provider.fetch_item_pool()
    item_manager.remove_item(item_id)
    item_manager.save()

    send_status(self, 200)