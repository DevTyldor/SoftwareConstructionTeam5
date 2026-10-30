from providers import data_provider
from endpoints.base import check_access, read_json, send_json, send_status


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
    

# POST /suppliers
def handle_post_suppliers(self, user):
    if not check_access(self, user, "suppliers", "post"):
        return

    new_supplier = read_json(self)

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.add_supplier(new_supplier)
    supplier_manager.save()

    send_status(self, 201)
    
    
# PUT /suppliers/{id}
def handle_put_suppliers(self, user, supplier_id):
    if not check_access(self, user, "suppliers", "put"):
        return

    updated_supplier = read_json(self)

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.update_supplier(supplier_id, updated_supplier)
    supplier_manager.save()

    send_status(self, 200)
    
    
# DELETE /suppliers/{id}
def handle_delete_suppliers(self, user, supplier_id):
    if not check_access(self, user, "suppliers", "delete"):
        return

    supplier_manager = data_provider.fetch_supplier_pool()
    supplier_manager.remove_supplier(supplier_id)
    supplier_manager.save()

    send_status(self, 200)