from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status

# GET /warehouses
# GET /warehouses/{id}
# GET /warehouses/{id}/locations
def handle_get_warehouses(self, user, warehouse_id=None, locations=False):
    if not check_access(self, user, "warehouses", "get"):
        return

    if locations:
        result = data_provider.fetch_location_pool().get_locations_in_warehouse(
            warehouse_id
        )

    elif warehouse_id is None:
        result = data_provider.fetch_warehouse_pool().get_warehouses()

    else:
        result = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)

    send_json(self, result)


# POST /warehouses
def handle_post_warehouses(self, user):
    if not check_access(self, user, "warehouses", "post"):
        return

    new_warehouse = read_json(self)

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.add_warehouse(new_warehouse)
    warehouse_manager.save()

    send_status(self, 201)


# PUT /warehouses/{id}
def handle_put_warehouses(self, user, warehouse_id):
    if not check_access(self, user, "warehouses", "put"):
        return

    updated_warehouse = read_json(self)

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.update_warehouse(warehouse_id, updated_warehouse)
    warehouse_manager.save()

    send_status(self, 200)
    

# DELETE /warehouses/{id}
def handle_delete_warehouses(self, user, warehouse_id):
    if not check_access(self, user, "warehouses", "delete"):
        return

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.remove_warehouse(warehouse_id)
    warehouse_manager.save()

    send_status(self, 200)