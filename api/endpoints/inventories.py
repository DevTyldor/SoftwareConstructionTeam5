from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


# GET /inventories
def handle_get_inventories(self, user):
    if not check_access(self, user, "inventories", "get"):
        return

    inventories = data_provider.fetch_inventory_pool().get_inventories()

    send_json(self, inventories)


# POST /inventories
def handle_post_inventories(self, user):
    if not check_access(self, user, "inventories", "post"):
        return

    new_inventory = read_json(self)

    inventory_manager = data_provider.fetch_inventory_pool()
    inventory_manager.add_inventory(new_inventory)
    inventory_manager.save()

    send_status(self, 201)


# PUT /inventories/{id}
def handle_put_inventories(self, user, inventory_id=None):
    if not check_access(self, user, "inventories", "put"):
        return

    # Inventory rows are keyed on a composite (item_id, location_id);
    # a single surrogate id is not meaningful in the new schema.
    send_status(self, 404)


# DELETE /inventories/{id}
def handle_delete_inventories(self, user, inventory_id=None):
    if not check_access(self, user, "inventories", "delete"):
        return

    send_status(self, 404)