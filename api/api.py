# This file will handle each indivual API endpoint.
# Each endpoint will be it's own function. This will then be routed through the router in main.py
# Main.py will be reserved to server startup and routing only. No more API endpoint handling.
import json

from providers import auth_provider
from providers import data_provider


# AUTHENTICATION
def check_user_access(self, paths, user, method):
    if not auth_provider.has_access(user, paths, method):
        self.send_response(403)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Access denied to this resource.")
        return False

    return True


# GET /warehouses
# GET /warehouses/{id}
# GET /warehouses/{id}/locations
def handle_get_warehouses(self, user, warehouse_id=None, locations=False):
    if not self.check_user_access(["warehouses"], user, "get"):
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
    if not self.check_user_access(["locations"], user, "get"):
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
    if not self.check_user_access(["transfers"], user, "get"):
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
    if not self.check_user_access(["items"], user, "get"):
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
    if not self.check_user_access(["item_lines"], user, "get"):
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
    if not self.check_user_access(["item_groups"], user, "get"):
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
    if not self.check_user_access(["item_types"], user, "get"):
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
    if not self.check_user_access(["inventories"], user, "get"):
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
    if not self.check_user_access(["suppliers"], user, "get"):
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
    if not self.check_user_access(["orders"], user, "get"):
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
    if not self.check_user_access(["clients"], user, "get"):
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
def handle_get_shipments(self, user, shipment_id=None, get_orders=False, get_items=False):
    if not self.check_user_access(["shipments"], user, "get"):
        return

    if get_orders:
        shipments = data_provider.fetch_shipment_pool().get_order_ids_in_shipment(shipment_id)

    elif get_items:
        shipments = data_provider.fetch_shipment_pool().get_items_in_shipment(shipment_id)

    elif shipment_id is None:
        shipments = data_provider.fetch_shipment_pool().get_shipments()

    else:
        shipments = data_provider.fetch_shipment_pool().get_shipment(shipment_id)

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    self.wfile.write(json.dumps(shipments).encode("utf-8"))
