from models.base import Base

ITEMS = []

class Items(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "item.json", ITEMS, is_debug)

    def get_items(self):
        return self.get_all()

    def get_item(self, item_id):
        return self.get_by_id(item_id)

    def get_items_for_item_line(self, item_line_id):
        result = []
        for x in self.data:
            if x["item_line_id"] == item_line_id:
                result.append(x["id"])
        return result

    def get_items_for_item_group(self, item_group_id):
        result = []
        for x in self.data:
            if x["item_group_id"] == item_group_id:
                result.append(x["id"])
        return result

    def get_items_for_item_type(self, item_type_id):
        result = []
        for x in self.data:
            if x["item_type_id"] == item_type_id:
                result.append(x["id"])
        return result

    def get_items_for_supplier(self, supplier_id):
        result = []
        for x in self.data:
            if x["supplier_id"] == supplier_id:
                result.append(x)
        return result

    def add_item(self, item):
        self.add(item)

    def update_item(self, item_id, item):
        self.update(item_id, item)

    def remove_item(self, item_id):
        self.remove(item_id)
