from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status




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


# POST /item_groups
def handle_post_item_groups(self, user):
    if not check_access(self, user, "item_groups", "post"):
        return

    new_item_group = read_json(self)

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.add_item_group(new_item_group)
    item_group_manager.save()

    send_status(self, 201)


# PUT /item_groups/{id}
def handle_put_item_groups(self, user, item_group_id):
    if not check_access(self, user, "item_groups", "put"):
        return

    updated_item_group = read_json(self)

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.update_item_group(item_group_id, updated_item_group)
    item_group_manager.save()

    send_status(self, 200)


# DELETE /item_groups/{id}
def handle_delete_item_groups(self, user, item_group_id):
    if not check_access(self, user, "item_groups", "delete"):
        return

    item_group_manager = data_provider.fetch_item_group_pool()
    item_group_manager.remove_item_group(item_group_id)
    item_group_manager.save()

    send_status(self, 200)