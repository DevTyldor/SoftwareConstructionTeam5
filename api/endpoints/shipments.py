from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


# GET /shipments
# GET /shipments/{id}
# GET /shipments/{id}/orders
# GET /shipments/{id}/items
def handle_get_shipments(
    self, user, shipment_id=None, get_orders=False, get_items=False
):
    if not check_access(self, user, "shipments", "get"):
        return

    if get_orders:
        shipments = data_provider.fetch_shipment_pool().get_order_ids_in_shipment(
            shipment_id
        )

    elif get_items:
        shipments = data_provider.fetch_shipment_pool().get_items_in_shipment(
            shipment_id
        )

    elif shipment_id is None:
        shipments = data_provider.fetch_shipment_pool().get_shipments()

    else:
        shipments = data_provider.fetch_shipment_pool().get_shipment(shipment_id)

    send_json(self, shipments)


# POST /shipments
def handle_post_shipments(self, user):
    if not check_access(self, user, "shipments", "post"):
        return

    new_shipment = read_json(self)

    shipment_manager = data_provider.fetch_shipment_pool()
    shipment_manager.add_shipment(new_shipment)
    shipment_manager.save()

    send_status(self, 201)


# PUT /shipments/{id}
# PUT /shipments/{id}/orders
# PUT /shipments/{id}/items
def handle_put_shipments(
    self,
    user,
    shipment_id,
    update_orders=False,
    update_items=False,
):
    if not check_access(self, user, "shipments", "put"):
        return

    shipment_manager = data_provider.fetch_shipment_pool()

    if update_orders:
        updated_orders = read_json(self)
        shipment_manager.update_orders_in_shipment(shipment_id, updated_orders)

    elif update_items:
        updated_items = read_json(self)
        shipment_manager.update_items_in_shipment(shipment_id, updated_items)

    else:
        updated_shipment = read_json(self)
        shipment_manager.update_shipment(shipment_id, updated_shipment)

    shipment_manager.save()

    send_status(self, 200)


# DELETE /shipments/{id}
def handle_delete_shipments(self, user, shipment_id):
    if not check_access(self, user, "shipments", "delete"):
        return

    shipment_manager = data_provider.fetch_shipment_pool()
    shipment_manager.remove_shipment(shipment_id)
    shipment_manager.save()

    send_status(self, 200)