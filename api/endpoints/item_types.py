from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


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


# POST /item_types
def handle_post_item_types(self, user):
    if not check_access(self, user, "item_types", "post"):
        return

    new_item_type = read_json(self)

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.add_item_type(new_item_type)
    item_type_manager.save()

    send_status(self, 201)


# PUT /item_types/{id}
def handle_put_item_types(self, user, item_type_id):
    if not check_access(self, user, "item_types", "put"):
        return

    updated_item_type = read_json(self)

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.update_item_type(item_type_id, updated_item_type)
    item_type_manager.save()

    send_status(self, 200)


# DELETE /item_types/{id}
def handle_delete_item_types(self, user, item_type_id):
    if not check_access(self, user, "item_types", "delete"):
        return

    item_type_manager = data_provider.fetch_item_type_pool()
    item_type_manager.remove_item_type(item_type_id)
    item_type_manager.save()

    send_status(self, 200)