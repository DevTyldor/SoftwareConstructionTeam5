import json
import socketserver
import http.server
from urllib.parse import urlparse

from processors import notification_processor
from providers import auth_provider

from api import (
    handle_get_warehouses,
    handle_get_locations,
    handle_get_transfers,
    handle_get_items,
    handle_get_item_lines,
    handle_get_item_groups,
    handle_get_item_types,
    handle_get_inventories,
    handle_get_suppliers,
    handle_get_orders,
    handle_get_clients,
    handle_get_shipments,
    handle_post_warehouses,
    handle_post_locations,
    handle_post_transfers,
    handle_post_items,
    handle_post_item_lines,
    handle_post_item_groups,
    handle_post_item_types,
    handle_post_inventories,
    handle_post_suppliers,
    handle_post_orders,
    handle_post_clients,
    handle_post_shipments,
    handle_put_warehouses,
    handle_put_locations,
    handle_put_transfers,
    handle_put_items,
    handle_put_item_lines,
    handle_put_item_groups,
    handle_put_item_types,
    handle_put_inventories,
    handle_put_suppliers,
    handle_put_orders,
    handle_put_clients,
    handle_put_shipments,
    handle_delete_warehouses,
    handle_delete_locations,
    handle_delete_transfers,
    handle_delete_items,
    handle_delete_item_lines,
    handle_delete_item_groups,
    handle_delete_item_types,
    handle_delete_inventories,
    handle_delete_suppliers,
    handle_delete_orders,
    handle_delete_clients,
    handle_delete_shipments,
)


class RequestHandler(http.server.BaseHTTPRequestHandler):
    # BUGFIX: status 500 upon letters as IDs (e.g: locations/noNumber) --> should be 400: bad request
    # Safe ID conversion
    def parse_id(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            return None

        return value if value > 0 else None

    def get_id(self, value):
        parsed_id = self.parse_id(value)

        if parsed_id is None:
            self.send_response(400)
            self.end_headers()
            return None

        return parsed_id

    # ROUTING
    # This large function routes each request to the right handler from api.py
    def route_request(self, method):
        paths = [path for path in urlparse(self.path).path.split("/") if path]

        # Validate API path
        if len(paths) < 3 or paths[0] != "api" or paths[1] != "v1":
            self.send_response(404)
            self.end_headers()
            return

        # Remove /api/v1/ from the path
        paths = paths[2:]

        # No resource specified
        if not paths:
            self.send_response(404)
            self.end_headers()
            return

        user = self.get_user()

        # No or invalid API key: 401
        if user is None:
            self.send_response(401)
            self.end_headers()
            return

        # ============================================================
        # GET
        # ============================================================

        if method == "GET":

            if paths[0] == "warehouses":
                if len(paths) == 1:
                    handle_get_warehouses(self, user)

                elif len(paths) == 2:
                    warehouse_id = self.get_id(paths[1])

                    if warehouse_id is None:
                        return

                    handle_get_warehouses(self, user, warehouse_id=warehouse_id)

                elif len(paths) == 3 and paths[2] == "locations":
                    warehouse_id = self.get_id(paths[1])

                    if warehouse_id is None:
                        return

                    handle_get_warehouses(
                        self, user, warehouse_id=warehouse_id, locations=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "locations":
                if len(paths) == 1:
                    handle_get_locations(self, user)

                elif len(paths) == 2:
                    location_id = self.get_id(paths[1])

                    if location_id is None:
                        return

                    handle_get_locations(self, user, location_id=location_id)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "transfers":
                if len(paths) == 1:
                    handle_get_transfers(self, user)

                elif len(paths) == 2:
                    transfer_id = self.get_id(paths[1])

                    if transfer_id is None:
                        return

                    handle_get_transfers(self, user, transfer_id=transfer_id)

                elif len(paths) == 3 and paths[2] == "items":
                    transfer_id = self.get_id(paths[1])

                    if transfer_id is None:
                        return

                    handle_get_transfers(
                        self, user, transfer_id=transfer_id, get_items=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "items":
                if len(paths) == 1:
                    handle_get_items(self, user)

                elif len(paths) == 2:
                    item_id = self.get_id(paths[1])

                    if item_id is None:
                        return

                    handle_get_items(self, user, item_id=item_id)

                elif len(paths) == 3 and paths[2] == "inventory":
                    item_id = self.get_id(paths[1])

                    if item_id is None:
                        return

                    handle_get_items(self, user, item_id=item_id, get_inventory=True)

                elif (
                    len(paths) == 4 and paths[2] == "inventory" and paths[3] == "totals"
                ):
                    item_id = self.get_id(paths[1])

                    if item_id is None:
                        return

                    handle_get_items(self, user, item_id=item_id, get_totals=True)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "item_lines":
                if len(paths) == 1:
                    handle_get_item_lines(self, user)

                elif len(paths) == 2:
                    item_line_id = self.get_id(paths[1])

                    if item_line_id is None:
                        return

                    handle_get_item_lines(self, user, item_line_id=item_line_id)

                elif len(paths) == 3 and paths[2] == "items":
                    item_line_id = self.get_id(paths[1])

                    if item_line_id is None:
                        return

                    handle_get_item_lines(
                        self, user, item_line_id=item_line_id, get_items=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "item_groups":
                if len(paths) == 1:
                    handle_get_item_groups(self, user)

                elif len(paths) == 2:
                    item_group_id = self.get_id(paths[1])

                    if item_group_id is None:
                        return

                    handle_get_item_groups(self, user, item_group_id=item_group_id)

                elif len(paths) == 3 and paths[2] == "items":
                    item_group_id = self.get_id(paths[1])

                    if item_group_id is None:
                        return

                    handle_get_item_groups(
                        self, user, item_group_id=item_group_id, get_items=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "item_types":
                if len(paths) == 1:
                    handle_get_item_types(self, user)

                elif len(paths) == 2:
                    item_type_id = self.get_id(paths[1])

                    if item_type_id is None:
                        return

                    handle_get_item_types(self, user, item_type_id=item_type_id)

                elif len(paths) == 3 and paths[2] == "items":
                    item_type_id = self.get_id(paths[1])

                    if item_type_id is None:
                        return

                    handle_get_item_types(
                        self, user, item_type_id=item_type_id, get_items=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "inventories":
                if len(paths) == 1:
                    handle_get_inventories(self, user)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "suppliers":
                if len(paths) == 1:
                    handle_get_suppliers(self, user)

                elif len(paths) == 2:
                    supplier_id = self.get_id(paths[1])

                    if supplier_id is None:
                        return

                    handle_get_suppliers(self, user, supplier_id=supplier_id)

                elif len(paths) == 3 and paths[2] == "items":
                    supplier_id = self.get_id(paths[1])

                    if supplier_id is None:
                        return

                    handle_get_suppliers(
                        self, user, supplier_id=supplier_id, get_items=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "orders":
                if len(paths) == 1:
                    handle_get_orders(self, user)

                elif len(paths) == 2:
                    order_id = self.get_id(paths[1])

                    if order_id is None:
                        return

                    handle_get_orders(self, user, order_id=order_id)

                elif len(paths) == 3 and paths[2] == "items":
                    order_id = self.get_id(paths[1])

                    if order_id is None:
                        return

                    handle_get_orders(self, user, order_id=order_id, get_items=True)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "clients":
                if len(paths) == 1:
                    handle_get_clients(self, user)

                elif len(paths) == 2:
                    client_id = self.get_id(paths[1])

                    if client_id is None:
                        return

                    handle_get_clients(self, user, client_id=client_id)

                elif len(paths) == 3 and paths[2] == "orders":
                    client_id = self.get_id(paths[1])

                    if client_id is None:
                        return

                    handle_get_clients(self, user, client_id=client_id, get_orders=True)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "shipments":
                if len(paths) == 1:
                    handle_get_shipments(self, user)

                elif len(paths) == 2:
                    shipment_id = self.get_id(paths[1])

                    if shipment_id is None:
                        return

                    handle_get_shipments(self, user, shipment_id=shipment_id)

                elif len(paths) == 3 and paths[2] == "orders":
                    shipment_id = self.get_id(paths[1])

                    if shipment_id is None:
                        return

                    handle_get_shipments(
                        self, user, shipment_id=shipment_id, get_orders=True
                    )

                elif len(paths) == 3 and paths[2] == "items":
                    shipment_id = self.get_id(paths[1])

                    if shipment_id is None:
                        return

                    handle_get_shipments(
                        self, user, shipment_id=shipment_id, get_items=True
                    )

                else:
                    self.send_response(404)
                    self.end_headers()

            else:
                self.send_response(404)
                self.end_headers()

        # ============================================================
        # POST
        # ============================================================

        elif method == "POST":

            if len(paths) != 1:
                self.send_response(404)
                self.end_headers()
                return

            if paths[0] == "warehouses":
                handle_post_warehouses(self, user)

            elif paths[0] == "locations":
                handle_post_locations(self, user)

            elif paths[0] == "transfers":
                handle_post_transfers(self, user)

            elif paths[0] == "items":
                handle_post_items(self, user)

            elif paths[0] == "item_lines":
                handle_post_item_lines(self, user)

            elif paths[0] == "item_groups":
                handle_post_item_groups(self, user)

            elif paths[0] == "item_types":
                handle_post_item_types(self, user)

            elif paths[0] == "inventories":
                handle_post_inventories(self, user)

            elif paths[0] == "suppliers":
                handle_post_suppliers(self, user)

            elif paths[0] == "orders":
                handle_post_orders(self, user)

            elif paths[0] == "clients":
                handle_post_clients(self, user)

            elif paths[0] == "shipments":
                handle_post_shipments(self, user)

            else:
                self.send_response(404)
                self.end_headers()

        # ============================================================
        # PUT
        # ============================================================

        elif method == "PUT":
            if len(paths) < 2:
                self.send_response(404)
                self.end_headers()
                return

            ID = self.get_id(paths[1])
            if ID is None:
                return

            if paths[0] == "warehouses" and len(paths) == 2:
                handle_put_warehouses(self, user, ID)

            elif paths[0] == "locations" and len(paths) == 2:
                handle_put_locations(self, user, ID)

            elif paths[0] == "transfers":
                if len(paths) == 2:
                    handle_put_transfers(self, user, ID)

                elif len(paths) == 3 and paths[2] == "commit":
                    handle_put_transfers(self, user, ID, commit=True)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "items" and len(paths) == 2:
                handle_put_items(self, user, ID)

            elif paths[0] == "item_lines" and len(paths) == 2:
                handle_put_item_lines(self, user, ID)

            elif paths[0] == "item_groups" and len(paths) == 2:
                handle_put_item_groups(self, user, ID)

            elif paths[0] == "item_types" and len(paths) == 2:
                handle_put_item_types(self, user, ID)

            elif paths[0] == "inventories" and len(paths) == 2:
                handle_put_inventories(self, user, ID)

            elif paths[0] == "suppliers" and len(paths) == 2:
                handle_put_suppliers(self, user, ID)

            elif paths[0] == "orders":
                if len(paths) == 2:
                    handle_put_orders(self, user, ID)

                elif len(paths) == 3 and paths[2] == "items":
                    handle_put_orders(self, user, ID, update_items=True)

                else:
                    self.send_response(404)
                    self.end_headers()

            elif paths[0] == "clients" and len(paths) == 2:
                handle_put_clients(self, user, ID)

            elif paths[0] == "shipments":
                if len(paths) == 2:
                    handle_put_shipments(self, user, ID)

                elif len(paths) == 3 and paths[2] == "orders":
                    handle_put_shipments(self, user, ID, update_orders=True)

                elif len(paths) == 3 and paths[2] == "items":
                    handle_put_shipments(self, user, ID, update_items=True)

                else:
                    self.send_response(404)
                    self.end_headers()

            else:
                self.send_response(404)
                self.end_headers()

        # ============================================================
        # DELETE
        # ============================================================

        elif method == "DELETE":
            if len(paths) != 2:
                self.send_response(404)
                self.end_headers()
                return

            ID = self.get_id(paths[1])
            if ID is None:
                return

            if paths[0] == "warehouses":
                handle_delete_warehouses(self, user, ID)

            elif paths[0] == "locations":
                handle_delete_locations(self, user, ID)

            elif paths[0] == "transfers":
                handle_delete_transfers(self, user, ID)

            elif paths[0] == "items":
                handle_delete_items(self, user, ID)

            elif paths[0] == "item_lines":
                handle_delete_item_lines(self, user, ID)

            elif paths[0] == "item_groups":
                handle_delete_item_groups(self, user, ID)

            elif paths[0] == "item_types":
                handle_delete_item_types(self, user, ID)

            elif paths[0] == "inventories":
                handle_delete_inventories(self, user, ID)

            elif paths[0] == "suppliers":
                handle_delete_suppliers(self, user, ID)

            elif paths[0] == "orders":
                handle_delete_orders(self, user, ID)

            elif paths[0] == "clients":
                handle_delete_clients(self, user, ID)

            elif paths[0] == "shipments":
                handle_delete_shipments(self, user, ID)

            else:
                self.send_response(404)
                self.end_headers()

        else:
            self.send_response(405)
            self.end_headers()

    # HTTP METHODS
    def do_GET(self):
        try:
            self.route_request("GET")
        except Exception:
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        try:
            self.route_request("POST")
        except Exception:
            self.send_response(500)
            self.end_headers()

    def do_PUT(self):
        try:
            self.route_request("PUT")
        except Exception:
            self.send_response(500)
            self.end_headers()

    def do_DELETE(self):
        try:
            self.route_request("DELETE")
        except Exception:
            self.send_response(500)
            self.end_headers()

    # AUTHENTICATION
    def get_user(self):
        api_key = self.headers.get("API_KEY")

        if not api_key:
            return None

        return auth_provider.get_user(api_key)


# SERVER STARTUP
if __name__ == "__main__":
    PORT = 3000
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        notification_processor.start()
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()
