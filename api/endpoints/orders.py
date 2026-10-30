from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


# GET /orders
# GET /orders/{id}
# GET /orders/{id}/items
def handle_get_orders(self, user, order_id=None, get_items=False):
    if not check_access(self, user, "orders", "get"):
        return

    if get_items:
        orders = data_provider.fetch_order_pool().get_items_in_order(order_id)

    elif order_id is None:
        orders = data_provider.fetch_order_pool().get_orders()

    else:
        orders = data_provider.fetch_order_pool().get_order(order_id)

    send_json(self, orders)


# POST /orders
def handle_post_orders(self, user):
    if not check_access(self, user, "orders", "post"):
        return

    new_order = read_json(self)

    order_manager = data_provider.fetch_order_pool()
    order_manager.add_order(new_order)
    order_manager.save()

    send_status(self, 201)


# PUT /orders/{id}
# PUT /orders/{id}/items
def handle_put_orders(self, user, order_id, update_items=False):
    if not check_access(self, user, "orders", "put"):
        return

    if update_items:
        updated_items = read_json(self)

        order_manager = data_provider.fetch_order_pool()
        order_manager.update_items_in_order(order_id, updated_items)
        order_manager.save()

    else:
        updated_order = read_json(self)

        order_manager = data_provider.fetch_order_pool()
        order_manager.update_order(order_id, updated_order)
        order_manager.save()

    send_status(self, 200)


# DELETE /orders/{id}
def handle_delete_orders(self, user, order_id):
    if not check_access(self, user, "orders", "delete"):
        return

    order_manager = data_provider.fetch_order_pool()
    order_manager.remove_order(order_id)
    order_manager.save()

    send_status(self, 200)