from models.base import Base

ITEM_GROUPS = []

class ItemGroups(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "item_group.json", ITEM_GROUPS, is_debug)

    def get_item_groups(self):
        return self.get_all()

    def get_item_group(self, item_group_id):
        return self.get_by_id(item_group_id)

    def add_item_group(self, item_group):
        self.add(item_group)

    def update_item_group(self, item_group_id, item_group):
        self.update(item_group_id, item_group)

    def remove_item_group(self, item_group_id):
        self.remove(item_group_id)
