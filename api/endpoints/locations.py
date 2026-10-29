from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


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


# POST /locations
def handle_post_locations(self, user):
    if not check_access(self, user, "locations", "post"):
        return

    new_location = read_json(self)

    location_manager = data_provider.fetch_location_pool()
    location_manager.add_location(new_location)
    location_manager.save()

    send_status(self, 201)


# PUT /locations/{id}
def handle_put_locations(self, user, location_id):
    if not check_access(self, user, "locations", "put"):
        return

    updated_location = read_json(self)

    location_manager = data_provider.fetch_location_pool()
    location_manager.update_location(location_id, updated_location)
    location_manager.save()

    send_status(self, 200)


# DELETE /locations/{id}
def handle_delete_locations(self, user, location_id):
    if not check_access(self, user, "locations", "delete"):
        return

    location_manager = data_provider.fetch_location_pool()
    location_manager.remove_location(location_id)
    location_manager.save()

    send_status(self, 200)