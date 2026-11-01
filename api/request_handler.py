import http.server
from urllib.parse import urlparse

from providers import auth_provider
from routes import app


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

    # error status helper to remove duplicated logic
    def error_status(self, status):
        self.send_response(status)
        self.end_headers()

    # ROUTING
    # Looks up the route for this request in the route table and calls its handler
    def route_request(self, method):
        paths = [path for path in urlparse(self.path).path.split("/") if path]

        # Validate API path
        if len(paths) < 3 or paths[0] != "api" or paths[1] != "v1":
            self.error_status(404)
            return

        # Remove /api/v1/ from the path
        paths = paths[2:]

        user = self.get_user()

        # No or invalid API key: 401
        if user is None:
            # Dit is een fix voor connection timed out (Stefano)
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length:
                self.rfile.read(length)

            self.error_status(401)
            return

        # PUT and DELETE check the ID before the url (same order as the old if/elif code)
        if (method == "PUT" and len(paths) >= 2) or (method == "DELETE" and len(paths) == 2):
            if self.get_id(paths[1]) is None:
                return

        match = app.find_route(method, paths)
        
        match = app.find_route(method, paths)

        # Unknown url, or this method is not allowed on it: 404
        if match is None:
            self.error_status(404)
            return

        route, params = match

        # Every path parameter is an ID: invalid ID -> 400 (sent by get_id)
        kwargs = dict(route.extra)
        for name, value in params.items():
            resource_id = self.get_id(value)
            if resource_id is None:
                return

            kwargs[name] = resource_id

        route.handler(self, user, **kwargs)

    # HTTP METHODS
    def do_GET(self):
        try:
            self.route_request("GET")
        except Exception:
            self.error_status(500)

    def do_POST(self):
        try:
            self.route_request("POST")
        except Exception:
            self.error_status(500)

    def do_PUT(self):
        try:
            self.route_request("PUT")
        except Exception:
            self.error_status(500)

    def do_DELETE(self):
        try:
            self.route_request("DELETE")
        except Exception:
            self.error_status(500)

    # AUTHENTICATION
    def get_user(self):
        api_key = self.headers.get("API_KEY")

        if not api_key:
            return None

        return auth_provider.get_user(api_key)