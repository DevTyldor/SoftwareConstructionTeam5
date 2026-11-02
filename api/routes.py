from router import Router

from endpoints.warehouses import (
    handle_get_warehouses, handle_post_warehouses, handle_put_warehouses, handle_delete_warehouses,
)
from endpoints.locations import (
    handle_get_locations, handle_post_locations, handle_put_locations, handle_delete_locations,
)
from endpoints.transfers import (
    handle_get_transfers, handle_post_transfers, handle_put_transfers, handle_delete_transfers,
)
from endpoints.items import (
    handle_get_items, handle_post_items, handle_put_items, handle_delete_items,
)
from endpoints.item_lines import (
    handle_get_item_lines, handle_post_item_lines, handle_put_item_lines, handle_delete_item_lines,
)
from endpoints.item_groups import (
    handle_get_item_groups, handle_post_item_groups, handle_put_item_groups, handle_delete_item_groups,
)
from endpoints.item_types import (
    handle_get_item_types, handle_post_item_types, handle_put_item_types, handle_delete_item_types,
)
from endpoints.inventories import (
    handle_get_inventories, handle_post_inventories, handle_put_inventories, handle_delete_inventories,
)
from endpoints.suppliers import (
    handle_get_suppliers, handle_post_suppliers, handle_put_suppliers, handle_delete_suppliers,
)
from endpoints.orders import (
    handle_get_orders, handle_post_orders, handle_put_orders, handle_delete_orders,
)
from endpoints.clients import (
    handle_get_clients, handle_post_clients, handle_put_clients, handle_delete_clients,
)
from endpoints.shipments import (
    handle_get_shipments, handle_post_shipments, handle_put_shipments, handle_delete_shipments,
)


# ROUTES
app = Router()

# warehouses
app.add_route("GET", "/warehouses", handle_get_warehouses)
app.add_route("GET", "/warehouses/{warehouse_id}", handle_get_warehouses)
app.add_route("GET", "/warehouses/{warehouse_id}/locations", handle_get_warehouses, get_locations=True)
app.add_route("POST", "/warehouses", handle_post_warehouses)
app.add_route("PUT", "/warehouses/{warehouse_id}", handle_put_warehouses)
app.add_route("DELETE", "/warehouses/{warehouse_id}", handle_delete_warehouses)

# locations
app.add_route("GET", "/locations", handle_get_locations)
app.add_route("GET", "/locations/{location_id}", handle_get_locations)
app.add_route("POST", "/locations", handle_post_locations)
app.add_route("PUT", "/locations/{location_id}", handle_put_locations)
app.add_route("DELETE", "/locations/{location_id}", handle_delete_locations)

# transfers
app.add_route("GET", "/transfers", handle_get_transfers)
app.add_route("GET", "/transfers/{transfer_id}", handle_get_transfers)
app.add_route("GET", "/transfers/{transfer_id}/items", handle_get_transfers, get_items=True)
app.add_route("POST", "/transfers", handle_post_transfers)
app.add_route("PUT", "/transfers/{transfer_id}", handle_put_transfers)
app.add_route("PUT", "/transfers/{transfer_id}/commit", handle_put_transfers, commit=True)
app.add_route("DELETE", "/transfers/{transfer_id}", handle_delete_transfers)

# items
app.add_route("GET", "/items", handle_get_items)
app.add_route("GET", "/items/{item_id}", handle_get_items)
app.add_route("GET", "/items/{item_id}/inventory", handle_get_items, get_inventory=True)
app.add_route("GET", "/items/{item_id}/inventory/totals", handle_get_items, get_totals=True)
app.add_route("POST", "/items", handle_post_items)
app.add_route("PUT", "/items/{item_id}", handle_put_items)
app.add_route("DELETE", "/items/{item_id}", handle_delete_items)

# item_lines
app.add_route("GET", "/item_lines", handle_get_item_lines)
app.add_route("GET", "/item_lines/{item_line_id}", handle_get_item_lines)
app.add_route("GET", "/item_lines/{item_line_id}/items", handle_get_item_lines, get_items=True)
app.add_route("POST", "/item_lines", handle_post_item_lines)
app.add_route("PUT", "/item_lines/{item_line_id}", handle_put_item_lines)
app.add_route("DELETE", "/item_lines/{item_line_id}", handle_delete_item_lines)

# item_groups
app.add_route("GET", "/item_groups", handle_get_item_groups)
app.add_route("GET", "/item_groups/{item_group_id}", handle_get_item_groups)
app.add_route("GET", "/item_groups/{item_group_id}/items", handle_get_item_groups, get_items=True)
app.add_route("POST", "/item_groups", handle_post_item_groups)
app.add_route("PUT", "/item_groups/{item_group_id}", handle_put_item_groups)
app.add_route("DELETE", "/item_groups/{item_group_id}", handle_delete_item_groups)

# item_types
app.add_route("GET", "/item_types", handle_get_item_types)
app.add_route("GET", "/item_types/{item_type_id}", handle_get_item_types)
app.add_route("GET", "/item_types/{item_type_id}/items", handle_get_item_types, get_items=True)
app.add_route("POST", "/item_types", handle_post_item_types)
app.add_route("PUT", "/item_types/{item_type_id}", handle_put_item_types)
app.add_route("DELETE", "/item_types/{item_type_id}", handle_delete_item_types)

# inventories
app.add_route("GET", "/inventories", handle_get_inventories)
app.add_route("POST", "/inventories", handle_post_inventories)
app.add_route("PUT", "/inventories/{inventory_id}", handle_put_inventories)
app.add_route("DELETE", "/inventories/{inventory_id}", handle_delete_inventories)

# suppliers
app.add_route("GET", "/suppliers", handle_get_suppliers)
app.add_route("GET", "/suppliers/{supplier_id}", handle_get_suppliers)
app.add_route("GET", "/suppliers/{supplier_id}/items", handle_get_suppliers, get_items=True)
app.add_route("POST", "/suppliers", handle_post_suppliers)
app.add_route("PUT", "/suppliers/{supplier_id}", handle_put_suppliers)
app.add_route("DELETE", "/suppliers/{supplier_id}", handle_delete_suppliers)

# orders
app.add_route("GET", "/orders", handle_get_orders)
app.add_route("GET", "/orders/{order_id}", handle_get_orders)
app.add_route("GET", "/orders/{order_id}/items", handle_get_orders, get_items=True)
app.add_route("POST", "/orders", handle_post_orders)
app.add_route("PUT", "/orders/{order_id}", handle_put_orders)
app.add_route("PUT", "/orders/{order_id}/items", handle_put_orders, update_items=True)
app.add_route("DELETE", "/orders/{order_id}", handle_delete_orders)

# clients
app.add_route("GET", "/clients", handle_get_clients)
app.add_route("GET", "/clients/{client_id}", handle_get_clients)
app.add_route("GET", "/clients/{client_id}/orders", handle_get_clients, get_orders=True)
app.add_route("POST", "/clients", handle_post_clients)
app.add_route("PUT", "/clients/{client_id}", handle_put_clients)
app.add_route("DELETE", "/clients/{client_id}", handle_delete_clients)

# shipments
app.add_route("GET", "/shipments", handle_get_shipments)
app.add_route("GET", "/shipments/{shipment_id}", handle_get_shipments)
app.add_route("GET", "/shipments/{shipment_id}/orders", handle_get_shipments, get_orders=True)
app.add_route("GET", "/shipments/{shipment_id}/items", handle_get_shipments, get_items=True)
app.add_route("POST", "/shipments", handle_post_shipments)
app.add_route("PUT", "/shipments/{shipment_id}", handle_put_shipments)
app.add_route("PUT", "/shipments/{shipment_id}/orders", handle_put_shipments, update_orders=True)
app.add_route("PUT", "/shipments/{shipment_id}/items", handle_put_shipments, update_items=True)
app.add_route("DELETE", "/shipments/{shipment_id}", handle_delete_shipments)