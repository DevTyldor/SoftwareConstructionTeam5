from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


# GET /clients
# GET /clients/{id}
# GET /clients/{id}/orders
def handle_get_clients(self, user, client_id=None, get_orders=False):
    if not check_access(self, user, "clients", "get"):
        return

    if get_orders:
        clients = data_provider.fetch_order_pool().get_orders_for_client(client_id)

    elif client_id is None:
        clients = data_provider.fetch_client_pool().get_clients()

    else:
        clients = data_provider.fetch_client_pool().get_client(client_id)

    send_json(self, clients)


# POST /clients
def handle_post_clients(self, user):
    if not check_access(self, user, "clients", "post"):
        return

    new_client = read_json(self)

    client_manager = data_provider.fetch_client_pool()
    client_manager.add_client(new_client)
    client_manager.save()

    send_status(self, 201)


# PUT /clients/{id}
def handle_put_clients(self, user, client_id):
    if not check_access(self, user, "clients", "put"):
        return

    updated_client = read_json(self)

    client_manager = data_provider.fetch_client_pool()
    client_manager.update_client(client_id, updated_client)
    client_manager.save()

    send_status(self, 200)


# DELETE /clients/{id}
def handle_delete_clients(self, user, client_id):
    if not check_access(self, user, "clients", "delete"):
        return

    client_manager = data_provider.fetch_client_pool()
    client_manager.remove_client(client_id)
    client_manager.save()

    send_status(self, 200)