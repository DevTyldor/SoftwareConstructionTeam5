from models.base import Base

ITEM_TYPES = []

class ItemTypes(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "item_type.json", ITEM_TYPES, is_debug)

    def get_item_types(self):
        return self.get_all()

    def get_item_type(self, item_type_id):
        return self.get_by_id(item_type_id)

    def add_item_type(self, item_type):
        self.add(item_type)

    def update_item_type(self, item_type_id, item_type):
        self.update(item_type_id, item_type)

    def remove_item_type(self, item_type_id):
        self.remove(item_type_id)
