from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


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


# POST /item_lines
def handle_post_item_lines(self, user):
    if not check_access(self, user, "item_lines", "post"):
        return

    new_item_line = read_json(self)

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.add_item_line(new_item_line)
    item_line_manager.save()

    send_status(self, 201)


# PUT /item_lines/{id}
def handle_put_item_lines(self, user, item_line_id):
    if not check_access(self, user, "item_lines", "put"):
        return

    updated_item_line = read_json(self)

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.update_item_line(item_line_id, updated_item_line)
    item_line_manager.save()

    send_status(self, 200)


# DELETE /item_lines/{id}
def handle_delete_item_lines(self, user, item_line_id):
    if not check_access(self, user, "item_lines", "delete"):
        return

    item_line_manager = data_provider.fetch_item_line_pool()
    item_line_manager.remove_item_line(item_line_id)
    item_line_manager.save()

    send_status(self, 200)