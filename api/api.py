# This file will handle each indivual API endpoint.
# Each endpoint will be it's own function. This will then be routed through the router in main.py
# Main.py will be reserved to server startup and routing only. No more API endpoint handling.
from providers import data_provider
from processors import notification_processor
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


# GET /locations
# GET /locations/{id}
def handle_get_locations(self, user, location_id=None):
    if not check_access(self, user, "locations", "get"):
        return

    if location_id is None:
        locations = data_provider.fetch_location_pool().get_locations()

    else:
        locations = data_provider.fetch_location_pool().get_location(location_id)

    send_json(self, locations)


# GET /transfers
# GET /transfers/{id}
# GET /transfers/{id}/items
def handle_get_transfers(self, user, transfer_id=None, get_items=False):
    if not check_access(self, user, "transfers", "get"):
        return

    if get_items:
        transfers = data_provider.fetch_transfer_pool().get_items_in_transfer(
            transfer_id
        )

    elif transfer_id is None:
        transfers = data_provider.fetch_transfer_pool().get_transfers()

    else:
        transfers = data_provider.fetch_transfer_pool().get_transfer(transfer_id)

    send_json(self, transfers)


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


# GET /item_lines
# GET /item_lines/{id}
# GET /item_lines/{id}/items
def handle_get_item_lines(self, user, item_line_id=None, get_items=False):
    if not check_access(self, user, "item_lines", "get"):
        return

    if get_items:
        item_lines = data_provider.fetch_item_pool().get_items_for_item_line(
            item_line_id
        )

    elif item_line_id is None:
        item_lines = data_provider.fetch_item_line_pool().get_item_lines()

    else:
        item_lines = data_provider.fetch_item_line_pool().get_item_line(item_line_id)

    send_json(self, item_lines)


# GET /item_groups
# GET /item_groups/{id}
# GET /item_groups/{id}/items
def handle_get_item_groups(self, user, item_group_id=None, get_items=False):
    if not check_access(self, user, "item_groups", "get"):
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

    send_json(self, item_groups)


# GET /item_types
# GET /item_types/{id}
# GET /item_types/{id}/items
def handle_get_item_types(self, user, item_type_id=None, get_items=False):
    if not check_access(self, user, "item_types", "get"):
        return

    if get_items:
        item_types = data_provider.fetch_item_pool().get_items_for_item_type(
            item_type_id
        )

    elif item_type_id is None:
        item_types = data_provider.fetch_item_type_pool().get_item_types()

    else:
        item_types = data_provider.fetch_item_type_pool().get_item_type(item_type_id)

    send_json(self, item_types)


# GET /inventories
def handle_get_inventories(self, user):
    if not check_access(self, user, "inventories", "get"):
        return

    inventories = data_provider.fetch_inventory_pool().get_inventories()

    send_json(self, inventories)


# GET /suppliers
# GET /suppliers/{id}
# GET /suppliers/{id}/items
def handle_get_suppliers(self, user, supplier_id=None, get_items=False):
    if not check_access(self, user, "suppliers", "get"):
        return

    if get_items:
        suppliers = data_provider.fetch_item_pool().get_items_for_supplier(supplier_id)

    elif supplier_id is None:
        suppliers = data_provider.fetch_supplier_pool().get_suppliers()

    else:
        suppliers = data_provider.fetch_supplier_pool().get_supplier(supplier_id)

    send_json(self, suppliers)


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


# POST /warehouses
def handle_post_warehouses(self, user):
    if not check_access(self, user, "warehouses", "post"):
        return

    new_warehouse = read_json(self)

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.add_warehouse(new_warehouse)
    warehouse_manager.save()

    send_status(self, 201)


# POST /locations
def handle_post_locations(self, user):
    if not check_access(self, user, "locations", "post"):
        return

    new_location = read_json(self)

    location_manager = data_provider.fetch_location_pool()
    location_manager.add_location(new_location)
    location_manager.save()

    send_status(self, 201)


# POST /transfers
def handle_post_transfers(self, user):
    if not check_access(self, user, "transfers", "post"):
        return

    new_transfer = read_json(self)

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.add_transfer(new_transfer)
    transfer_manager.save()

    notification_processor.push(f"Scheduled batch transfer {new_transfer['id']}")

    send_status(self, 201)


# POST /items
def handle_post_items(self, user):
    if not check_access(self, user, "items", "post"):
        return

    new_item = read_json(self)

    item_manager = data_provider.fetch_item_pool()
    item_manager.add_item(new_item)
    item_manager.save()

    send_status(self, 201)


# POST /item_lines
def handle_post_item_lines(self, user):
    if not check_access(self, user, "item_lines", "post"):
        return

    new_item_line = read_json(self)

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.add_item_line(new_item_line)
    item_line_manager.save()

    send_status(self, 201)


# POST /item_groups
def handle_post_item_groups(self, user):
    if not check_access(self, user, "item_groups", "post"):
        return

    new_item_group = read_json(self)

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.add_item_group(new_item_group)
    item_group_manager.save()

    send_status(self, 201)


# POST /item_types
def handle_post_item_types(self, user):
    if not check_access(self, user, "item_types", "post"):
        return

    new_item_type = read_json(self)

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.add_item_type(new_item_type)
    item_type_manager.save()

    send_status(self, 201)


# POST /inventories
def handle_post_inventories(self, user):
    if not check_access(self, user, "inventories", "post"):
        return

    new_inventory = read_json(self)

    inventory_manager = data_provider.fetch_inventory_pool()
    inventory_manager.add_inventory(new_inventory)
    inventory_manager.save()

    send_status(self, 201)


# POST /suppliers
def handle_post_suppliers(self, user):
    if not check_access(self, user, "suppliers", "post"):
        return

    new_supplier = read_json(self)

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.add_supplier(new_supplier)
    supplier_manager.save()

    send_status(self, 201)


# POST /orders
def handle_post_orders(self, user):
    if not check_access(self, user, "orders", "post"):
        return

    new_order = read_json(self)

    order_manager = data_provider.fetch_order_pool()
    order_manager.add_order(new_order)
    order_manager.save()

    send_status(self, 201)


# POST /clients
def handle_post_clients(self, user):
    if not check_access(self, user, "clients", "post"):
        return

    new_client = read_json(self)

    client_manager = data_provider.fetch_client_pool()
    client_manager.add_client(new_client)
    client_manager.save()

    send_status(self, 201)


# POST /shipments
def handle_post_shipments(self, user):
    if not check_access(self, user, "shipments", "post"):
        return

    new_shipment = read_json(self)

    shipment_manager = data_provider.fetch_shipment_pool()
    shipment_manager.add_shipment(new_shipment)
    shipment_manager.save()

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


# PUT /locations/{id}
def handle_put_locations(self, user, location_id):
    if not check_access(self, user, "locations", "put"):
        return

    updated_location = read_json(self)

    location_manager = data_provider.fetch_location_pool()
    location_manager.update_location(location_id, updated_location)
    location_manager.save()

    send_status(self, 200)


# PUT /transfers/{id}
# PUT /transfers/{id}/commit
def handle_put_transfers(self, user, transfer_id, commit=False):
    if not check_access(self, user, "transfers", "put"):
        return

    if not commit:
        updated_transfer = read_json(self)

        transfer_manager = data_provider.fetch_transfer_pool()
        transfer_manager.update_transfer(transfer_id, updated_transfer)
        transfer_manager.save()

        send_status(self, 200)
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

    send_status(self, 200)


# PUT /items/{id}
def handle_put_items(self, user, item_id):
    if not check_access(self, user, "items", "put"):
        return

    updated_item = read_json(self)

    item_manager = data_provider.fetch_item_pool()
    item_manager.update_item(item_id, updated_item)
    item_manager.save()

    send_status(self, 200)


# PUT /item_lines/{id}
def handle_put_item_lines(self, user, item_line_id):
    if not check_access(self, user, "item_lines", "put"):
        return

    updated_item_line = read_json(self)

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.update_item_line(item_line_id, updated_item_line)
    item_line_manager.save()

    send_status(self, 200)


# PUT /item_groups/{id}
def handle_put_item_groups(self, user, item_group_id):
    if not check_access(self, user, "item_groups", "put"):
        return

    updated_item_group = read_json(self)

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.update_item_group(item_group_id, updated_item_group)
    item_group_manager.save()

    send_status(self, 200)


# PUT /item_types/{id}
def handle_put_item_types(self, user, item_type_id):
    if not check_access(self, user, "item_types", "put"):
        return

    updated_item_type = read_json(self)

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.update_item_type(item_type_id, updated_item_type)
    item_type_manager.save()

    send_status(self, 200)


# PUT /inventories/{id}
def handle_put_inventories(self, user, inventory_id=None):
    if not check_access(self, user, "inventories", "put"):
        return

    # Inventory rows are keyed on a composite (item_id, location_id);
    # a single surrogate id is not meaningful in the new schema.
    send_status(self, 404)


# PUT /suppliers/{id}
def handle_put_suppliers(self, user, supplier_id):
    if not check_access(self, user, "suppliers", "put"):
        return

    updated_supplier = read_json(self)

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.update_supplier(supplier_id, updated_supplier)
    supplier_manager.save()

    send_status(self, 200)


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


# PUT /clients/{id}
def handle_put_clients(self, user, client_id):
    if not check_access(self, user, "clients", "put"):
        return

    updated_client = read_json(self)

    client_manager = data_provider.fetch_client_pool()
    client_manager.update_client(client_id, updated_client)
    client_manager.save()

    send_status(self, 200)


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


# DELETE /warehouses/{id}
def handle_delete_warehouses(self, user, warehouse_id):
    if not check_access(self, user, "warehouses", "delete"):
        return

    warehouse_manager = data_provider.fetch_warehouse_pool()
    warehouse_manager.remove_warehouse(warehouse_id)
    warehouse_manager.save()

    send_status(self, 200)


# DELETE /locations/{id}
def handle_delete_locations(self, user, location_id):
    if not check_access(self, user, "locations", "delete"):
        return

    location_manager = data_provider.fetch_location_pool()
    location_manager.remove_location(location_id)
    location_manager.save()

    send_status(self, 200)


# DELETE /transfers/{id}
def handle_delete_transfers(self, user, transfer_id):
    if not check_access(self, user, "transfers", "delete"):
        return

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.remove_transfer(transfer_id)
    transfer_manager.save()

    send_status(self, 200)


# DELETE /items/{id}
def handle_delete_items(self, user, item_id):
    if not check_access(self, user, "items", "delete"):
        return

    item_manager = data_provider.fetch_item_pool()
    item_manager.remove_item(item_id)
    item_manager.save()

    send_status(self, 200)


# DELETE /item_lines/{id}
def handle_delete_item_lines(self, user, item_line_id):
    if not check_access(self, user, "item_lines", "delete"):
        return

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.remove_item_line(item_line_id)
    item_line_manager.save()

    send_status(self, 200)


# DELETE /item_groups/{id}
def handle_delete_item_groups(self, user, item_group_id):
    if not check_access(self, user, "item_groups", "delete"):
        return

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.remove_item_group(item_group_id)
    item_group_manager.save()

    send_status(self, 200)


# DELETE /item_types/{id}
def handle_delete_item_types(self, user, item_type_id):
    if not check_access(self, user, "item_types", "delete"):
        return

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.remove_item_type(item_type_id)
    item_type_manager.save()

    send_status(self, 200)


# DELETE /inventories/{id}
def handle_delete_inventories(self, user, inventory_id=None):
    if not check_access(self, user, "inventories", "delete"):
        return

    send_status(self, 404)


# DELETE /suppliers/{id}
def handle_delete_suppliers(self, user, supplier_id):
    if not check_access(self, user, "suppliers", "delete"):
        return

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.remove_supplier(supplier_id)
    supplier_manager.save()

    send_status(self, 200)


# DELETE /orders/{id}
def handle_delete_orders(self, user, order_id):
    if not check_access(self, user, "orders", "delete"):
        return

    order_manager = data_provider.fetch_order_pool()
    order_manager.remove_order(order_id)
    order_manager.save()

    send_status(self, 200)


# DELETE /clients/{id}
def handle_delete_clients(self, user, client_id):
    if not check_access(self, user, "clients", "delete"):
        return

    client_manager = data_provider.fetch_client_pool()
    client_manager.remove_client(client_id)
    client_manager.save()

    send_status(self, 200)


# DELETE /shipments/{id}
def handle_delete_shipments(self, user, shipment_id):
    if not check_access(self, user, "shipments", "delete"):
        return

    shipment_manager = data_provider.fetch_shipment_pool()
    shipment_manager.remove_shipment(shipment_id)
    shipment_manager.save()

    send_status(self, 200)