from models.base import Base

ITEM_LINES = []

class ItemLines(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "item_line.json", ITEM_LINES, is_debug)

    def get_item_lines(self):
        return self.get_all()

    def get_item_line(self, item_line_id):
        return self.get_by_id(item_line_id)

    def add_item_line(self, item_line):
        self.add(item_line)

    def update_item_line(self, item_line_id, item_line):
        self.update(item_line_id, item_line)

    def remove_item_line(self, item_line_id):
        self.remove(item_line_id)
