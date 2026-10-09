# This file will handle each indivual API endpoint.
# Each endpoint will be it's own function. This will then be routed through the router in main.py
# Main.py will be reserved to server startup and routing only. No more API endpoint handling.
import json

from providers import auth_provider
from providers import data_provider
from processors import notification_processor


# AUTHENTICATION
def check_user_access(handler, paths, user, method):
    if not auth_provider.has_access(user, paths, method):
        # Dit is een fix voor connection timed out (Stefano)
        length = int(handler.headers.get("Content-Length", 0) or 0)
        if length:
            handler.rfile.read(length)

        handler.send_response(403)
        handler.send_header("Content-Type", "text/plain")
        handler.end_headers()
        handler.wfile.write(b"Access denied to this resource.")
        return False

    return True



# GET /warehouses
# GET /warehouses/{id}
# GET /warehouses/{id}/locations
def handle_get_warehouses(self, user, warehouse_id=None, locations=False):
    if not check_user_access(self, ["warehouses"], user, "get"):
        return

    if locations:
        result = data_provider.fetch_location_pool().get_locations_in_warehouse(
            warehouse_id
        )

    elif warehouse_id is None:
        result = data_provider.fetch_warehouse_pool().get_warehouses()

    else:
        result = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(result).encode("utf-8"))


# GET /locations
# GET /locations/{id}
def handle_get_locations(self, user, location_id=None):
    if not check_user_access(self, ["locations"], user, "get"):
        return

    if location_id is None:
        locations = data_provider.fetch_location_pool().get_locations()

    else:
        locations = data_provider.fetch_location_pool().get_location(location_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(locations).encode("utf-8"))


# GET /transfers
# GET /transfers/{id}
# GET /transfers/{id}/items
def handle_get_transfers(self, user, transfer_id=None, get_items=False):
    if not check_user_access(self, ["transfers"], user, "get"):
        return

    if get_items:
        transfers = data_provider.fetch_transfer_pool().get_items_in_transfer(
            transfer_id
        )

    elif transfer_id is None:
        transfers = data_provider.fetch_transfer_pool().get_transfers()

    else:
        transfers = data_provider.fetch_transfer_pool().get_transfer(transfer_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(transfers).encode("utf-8"))


# GET /items
# GET /items/{id}
# GET /items/{id}/inventory
# GET /items/{id}/inventory/totals
def handle_get_items(self, user, item_id=None, get_inventory=False, get_totals=False):
    if not check_user_access(self, ["items"], user, "get"):
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

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(items).encode("utf-8"))


# GET /item_lines
# GET /item_lines/{id}
# GET /item_lines/{id}/items
def handle_get_item_lines(self, user, item_line_id=None, get_items=False):
    if not check_user_access(self, ["item_lines"], user, "get"):
        return

    if get_items:
        item_lines = data_provider.fetch_item_pool().get_items_for_item_line(
            item_line_id
        )

    elif item_line_id is None:
        item_lines = data_provider.fetch_item_line_pool().get_item_lines()

    else:
        item_lines = data_provider.fetch_item_line_pool().get_item_line(item_line_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(item_lines).encode("utf-8"))


# GET /item_groups
# GET /item_groups/{id}
# GET /item_groups/{id}/items
def handle_get_item_groups(self, user, item_group_id=None, get_items=False):
    if not check_user_access(self, ["item_groups"], user, "get"):
        return

    if get_items:
        item_groups = data_provider.fetch_item_pool().get_items_for_item_group(
            item_group_id
        )

    elif item_group_id is None:
        item_groups = data_provider.fetch_item_group_pool().get_item_groups()

    else:
        item_groups = data_provider.fetch_item_group_pool().get_item_group(
            item_group_id
        )

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(item_groups).encode("utf-8"))


# GET /item_types
# GET /item_types/{id}
# GET /item_types/{id}/items
def handle_get_item_types(self, user, item_type_id=None, get_items=False):
    if not check_user_access(self, ["item_types"], user, "get"):
        return

    if get_items:
        item_types = data_provider.fetch_item_pool().get_items_for_item_type(
            item_type_id
        )

    elif item_type_id is None:
        item_types = data_provider.fetch_item_type_pool().get_item_types()

    else:
        item_types = data_provider.fetch_item_type_pool().get_item_type(item_type_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(item_types).encode("utf-8"))


# GET /inventories
def handle_get_inventories(self, user):
    if not check_user_access(self, ["inventories"], user, "get"):
        return

    inventories = data_provider.fetch_inventory_pool().get_inventories()

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(inventories).encode("utf-8"))


# GET /suppliers
# GET /suppliers/{id}
# GET /suppliers/{id}/items
def handle_get_suppliers(self, user, supplier_id=None, get_items=False):
    if not check_user_access(self, ["suppliers"], user, "get"):
        return

    if get_items:
        suppliers = data_provider.fetch_item_pool().get_items_for_supplier(supplier_id)

    elif supplier_id is None:
        suppliers = data_provider.fetch_supplier_pool().get_suppliers()

    else:
        suppliers = data_provider.fetch_supplier_pool().get_supplier(supplier_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(suppliers).encode("utf-8"))


# GET /orders
# GET /orders/{id}
# GET /orders/{id}/items
def handle_get_orders(self, user, order_id=None, get_items=False):
    if not check_user_access(self, ["orders"], user, "get"):
        return

    if get_items:
        orders = data_provider.fetch_order_pool().get_items_in_order(order_id)

    elif order_id is None:
        orders = data_provider.fetch_order_pool().get_orders()

    else:
        orders = data_provider.fetch_order_pool().get_order(order_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(orders).encode("utf-8"))


# GET /clients
# GET /clients/{id}
# GET /clients/{id}/orders
def handle_get_clients(self, user, client_id=None, get_orders=False):
    if not check_user_access(self, ["clients"], user, "get"):
        return

    if get_orders:
        clients = data_provider.fetch_order_pool().get_orders_for_client(client_id)

    elif client_id is None:
        clients = data_provider.fetch_client_pool().get_clients()

    else:
        clients = data_provider.fetch_client_pool().get_client(client_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(clients).encode("utf-8"))


# GET /shipments
# GET /shipments/{id}
# GET /shipments/{id}/orders
# GET /shipments/{id}/items
def handle_get_shipments(
    self, user, shipment_id=None, get_orders=False, get_items=False
):
    if not check_user_access(self, ["shipments"], user, "get"):
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

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(shipments).encode("utf-8"))


# POST /warehouses
def handle_post_warehouses(self, user):
    if not check_user_access(self, ["warehouses"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_warehouse = json.loads(post_data.decode())

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.add_warehouse(new_warehouse)
    warehouse_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /locations
def handle_post_locations(self, user):
    if not check_user_access(self, ["locations"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_location = json.loads(post_data.decode())

    location_manager = data_provider.fetch_location_pool()
    location_manager.add_location(new_location)
    location_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /transfers
def handle_post_transfers(self, user):
    if not check_user_access(self, ["transfers"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_transfer = json.loads(post_data.decode())

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.add_transfer(new_transfer)
    transfer_manager.save()

    notification_processor.push(f"Scheduled batch transfer {new_transfer['id']}")

    self.send_response(201)
    self.end_headers()


# POST /items
def handle_post_items(self, user):
    if not check_user_access(self, ["items"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_item = json.loads(post_data.decode())

    item_manager = data_provider.fetch_item_pool()
    item_manager.add_item(new_item)
    item_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /item_lines
def handle_post_item_lines(self, user):
    if not check_user_access(self, ["item_lines"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_item_line = json.loads(post_data.decode())

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.add_item_line(new_item_line)
    item_line_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /item_groups
def handle_post_item_groups(self, user):
    if not check_user_access(self, ["item_groups"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_item_group = json.loads(post_data.decode())

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.add_item_group(new_item_group)
    item_group_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /item_types
def handle_post_item_types(self, user):
    if not check_user_access(self, ["item_types"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_item_type = json.loads(post_data.decode())

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.add_item_type(new_item_type)
    item_type_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /inventories
def handle_post_inventories(self, user):
    if not check_user_access(self, ["inventories"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_inventory = json.loads(post_data.decode())

    inventory_manager = data_provider.fetch_inventory_pool()
    inventory_manager.add_inventory(new_inventory)
    inventory_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /suppliers
def handle_post_suppliers(self, user):
    if not check_user_access(self, ["suppliers"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_supplier = json.loads(post_data.decode())

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.add_supplier(new_supplier)
    supplier_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /orders
def handle_post_orders(self, user):
    if not check_user_access(self, ["orders"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_order = json.loads(post_data.decode())

    order_manager = data_provider.fetch_order_pool()
    order_manager.add_order(new_order)
    order_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /clients
def handle_post_clients(self, user):
    if not check_user_access(self, ["clients"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_client = json.loads(post_data.decode())

    client_manager = data_provider.fetch_client_pool()
    client_manager.add_client(new_client)
    client_manager.save()

    self.send_response(201)
    self.end_headers()


# POST /shipments
def handle_post_shipments(self, user):
    if not check_user_access(self, ["shipments"], user, "post"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    new_shipment = json.loads(post_data.decode())

    shipment_manager = data_provider.fetch_shipment_pool()
    shipment_manager.add_shipment(new_shipment)
    shipment_manager.save()

    self.send_response(201)
    self.end_headers()


# PUT /warehouses/{id}
def handle_put_warehouses(self, user, warehouse_id):
    if not check_user_access(self, ["warehouses"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_warehouse = json.loads(post_data.decode())

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.update_warehouse(warehouse_id, updated_warehouse)
    warehouse_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /locations/{id}
def handle_put_locations(self, user, location_id):
    if not check_user_access(self, ["locations"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_location = json.loads(post_data.decode())

    location_manager = data_provider.fetch_location_pool()
    location_manager.update_location(location_id, updated_location)
    location_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /transfers/{id}
# PUT /transfers/{id}/commit
def handle_put_transfers(self, user, transfer_id, commit=False):
    if not check_user_access(self, ["transfers"], user, "put"):
        return

    if not commit:
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        updated_transfer = json.loads(post_data.decode())

        transfer_manager = data_provider.fetch_transfer_pool()
        transfer_manager.update_transfer(transfer_id, updated_transfer)
        transfer_manager.save()

        self.send_response(200)
        self.end_headers()
        return

    transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
    from_location_id = transfer["from_location_id"]
    to_location_id = transfer["to_location_id"]

    inventory_pool = data_provider.fetch_inventory_pool()

    for x in transfer["items"]:
        item_id = x["item_id"]
        amount = x["amount"]

        # decrease on-hand at the source location
        src = inventory_pool.get_inventory(item_id, from_location_id)

        if src is not None:
            src["quantity_on_hand"] -= amount
            inventory_pool.update_inventory(item_id, from_location_id, src)

        # increase (or create) on-hand at the destination location
        dst = inventory_pool.get_inventory(item_id, to_location_id)

        if dst is not None:
            dst["quantity_on_hand"] += amount
            inventory_pool.update_inventory(item_id, to_location_id, dst)

        else:
            inventory_pool.add_inventory(
                {
                    "item_id": item_id,
                    "location_id": to_location_id,
                    "quantity_on_hand": amount,
                    "quantity_expected": 0,
                    "quantity_ordered": 0,
                    "quantity_allocated": 0,
                }
            )

    transfer["transfer_status"] = "Processed"
    transfer.pop("items", None)

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.update_transfer(transfer_id, transfer)

    notification_processor.push(f"Processed batch transfer with id:{transfer['id']}")

    transfer_manager.save()
    inventory_pool.save()

    self.send_response(200)
    self.end_headers()


# PUT /items/{id}
def handle_put_items(self, user, item_id):
    if not check_user_access(self, ["items"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_item = json.loads(post_data.decode())

    item_manager = data_provider.fetch_item_pool()
    item_manager.update_item(item_id, updated_item)
    item_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /item_lines/{id}
def handle_put_item_lines(self, user, item_line_id):
    if not check_user_access(self, ["item_lines"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_item_line = json.loads(post_data.decode())

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.update_item_line(item_line_id, updated_item_line)
    item_line_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /item_groups/{id}
def handle_put_item_groups(self, user, item_group_id):
    if not check_user_access(self, ["item_groups"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_item_group = json.loads(post_data.decode())

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.update_item_group(item_group_id, updated_item_group)
    item_group_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /item_types/{id}
def handle_put_item_types(self, user, item_type_id):
    if not check_user_access(self, ["item_types"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_item_type = json.loads(post_data.decode())

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.update_item_type(item_type_id, updated_item_type)
    item_type_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /inventories/{id}
def handle_put_inventories(self, user, inventory_id=None):
    if not check_user_access(self, ["inventories"], user, "put"):
        return

    # Inventory rows are keyed on a composite (item_id, location_id);
    # a single surrogate id is not meaningful in the new schema.
    self.send_response(404)
    self.end_headers()


# PUT /suppliers/{id}
def handle_put_suppliers(self, user, supplier_id):
    if not check_user_access(self, ["suppliers"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_supplier = json.loads(post_data.decode())

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.update_supplier(supplier_id, updated_supplier)
    supplier_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /orders/{id}
# PUT /orders/{id}/items
def handle_put_orders(self, user, order_id, update_items=False):
    if not check_user_access(self, ["orders"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)

    if update_items:
        updated_items = json.loads(post_data.decode())

        order_manager = data_provider.fetch_order_pool()
        order_manager.update_items_in_order(order_id, updated_items)
        order_manager.save()

    else:
        updated_order = json.loads(post_data.decode())

        order_manager = data_provider.fetch_order_pool()
        order_manager.update_order(order_id, updated_order)
        order_manager.save()

    self.send_response(200)
    self.end_headers()


# PUT /clients/{id}
def handle_put_clients(self, user, client_id):
    if not check_user_access(self, ["clients"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)
    updated_client = json.loads(post_data.decode())

    client_manager = data_provider.fetch_client_pool()
    client_manager.update_client(client_id, updated_client)
    client_manager.save()

    self.send_response(200)
    self.end_headers()


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
    if not check_user_access(self, ["shipments"], user, "put"):
        return

    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length)

    shipment_manager = data_provider.fetch_shipment_pool()

    if update_orders:
        updated_orders = json.loads(post_data.decode())
        shipment_manager.update_orders_in_shipment(shipment_id, updated_orders)

    elif update_items:
        updated_items = json.loads(post_data.decode())
        shipment_manager.update_items_in_shipment(shipment_id, updated_items)

    else:
        updated_shipment = json.loads(post_data.decode())
        shipment_manager.update_shipment(shipment_id, updated_shipment)

    shipment_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /warehouses/{id}
def handle_delete_warehouses(self, user, warehouse_id):
    if not check_user_access(self, ["warehouses"], user, "delete"):
        return

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.remove_warehouse(warehouse_id)
    warehouse_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /locations/{id}
def handle_delete_locations(self, user, location_id):
    if not check_user_access(self, ["locations"], user, "delete"):
        return

    location_manager = data_provider.fetch_location_pool()
    location_manager.remove_location(location_id)
    location_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /transfers/{id}
def handle_delete_transfers(self, user, transfer_id):
    if not check_user_access(self, ["transfers"], user, "delete"):
        return

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.remove_transfer(transfer_id)
    transfer_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /items/{id}
def handle_delete_items(self, user, item_id):
    if not check_user_access(self, ["items"], user, "delete"):
        return

    item_manager = data_provider.fetch_item_pool()
    item_manager.remove_item(item_id)
    item_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /item_lines/{id}
def handle_delete_item_lines(self, user, item_line_id):
    if not check_user_access(self, ["item_lines"], user, "delete"):
        return

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.remove_item_line(item_line_id)
    item_line_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /item_groups/{id}
def handle_delete_item_groups(self, user, item_group_id):
    if not check_user_access(self, ["item_groups"], user, "delete"):
        return

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.remove_item_group(item_group_id)
    item_group_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /item_types/{id}
def handle_delete_item_types(self, user, item_type_id):
    if not check_user_access(self, ["item_types"], user, "delete"):
        return

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.remove_item_type(item_type_id)
    item_type_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /inventories/{id}
def handle_delete_inventories(self, user, inventory_id=None):
    if not check_user_access(self, ["inventories"], user, "delete"):
        return

    self.send_response(404)
    self.end_headers()


# DELETE /suppliers/{id}
def handle_delete_suppliers(self, user, supplier_id):
    if not check_user_access(self, ["suppliers"], user, "delete"):
        return

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.remove_supplier(supplier_id)
    supplier_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /orders/{id}
def handle_delete_orders(self, user, order_id):
    if not check_user_access(self, ["orders"], user, "delete"):
        return

    order_manager = data_provider.fetch_order_pool()
    order_manager.remove_order(order_id)
    order_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /clients/{id}
def handle_delete_clients(self, user, client_id):
    if not check_user_access(self, ["clients"], user, "delete"):
        return

    client_manager = data_provider.fetch_client_pool()
    client_manager.remove_client(client_id)
    client_manager.save()

    self.send_response(200)
    self.end_headers()


# DELETE /shipments/{id}
def handle_delete_shipments(self, user, shipment_id):
    if not check_user_access(self, ["shipments"], user, "delete"):
        return

    shipment_manager = data_provider.fetch_shipment_pool()
    shipment_manager.remove_shipment(shipment_id)
    shipment_manager.save()

    self.send_response(200)
    self.end_headers()
