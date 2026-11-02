class Route:
    def __init__(self, method, path, handler, extra):
        self.method = method
        self.path = path
        self.handler = handler
        self.extra = extra  # extra arguments for example {get_items}=True
        self.route_pattern_splits = [rps for rps in path.split("/") if rps] # split the path into segments, ignoring empty splits

    # returns dict with parameter name as key and it''s value as value if the route matches the url_parts otherwise None
    def match(self, url_parts):
        if len(url_parts) != len(self.route_pattern_splits):
            return None

        parameters = {}
        for split, part in zip(self.route_pattern_splits, url_parts):
            if split.startswith("{") and split.endswith("}"):
                parameters[split[1:-1]] = part

            elif split != part:
                return None

        return parameters


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, method, path, handler, **extra):
        self.routes.append(Route(method, path, handler, extra))

    # Returns (route, parameters) for the first matching route otherwise None
    def find_route(self, method, url_parts):
        for route in self.routes:
            if route.method != method:
                continue

            parameters = route.match(url_parts)
            if parameters is not None:
                return route, parameters

        return None