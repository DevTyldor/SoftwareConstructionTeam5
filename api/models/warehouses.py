from models.base import Base

WAREHOUSES = []

class Warehouses(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "warehouse.json", WAREHOUSES, is_debug)

    def get_warehouses(self):
        return self.get_all()

    def get_warehouse(self, warehouse_id):
        return self.get_by_id(warehouse_id)

    def add_warehouse(self, warehouse):
        self.add(warehouse)

    def update_warehouse(self, warehouse_id, warehouse):
        self.update(warehouse_id, warehouse)

    def remove_warehouse(self, warehouse_id):
        self.remove(warehouse_id)
