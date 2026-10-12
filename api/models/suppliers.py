from models.base import Base

SUPPLIERS = []

class Suppliers(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "supplier.json", SUPPLIERS, is_debug)

    def get_suppliers(self):
        return self.get_all()

    def get_supplier(self, supplier_id):
        return self.get_by_id(supplier_id)

    def add_supplier(self, supplier):
        self.add(supplier)

    def update_supplier(self, supplier_id, supplier):
        self.update(supplier_id, supplier)

    def remove_supplier(self, supplier_id):
        self.remove(supplier_id)
