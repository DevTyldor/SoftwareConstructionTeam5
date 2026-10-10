from models.base import Base

LOCATIONS = []

class Locations(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "location.json", LOCATIONS, is_debug)

    def get_locations(self):
        return self.get_all()

    def get_location(self, location_id):
        return self.get_by_id(location_id)

    def get_locations_in_warehouse(self, warehouse_id):
        result = []
        for x in self.data:
            if x["warehouse_id"] == warehouse_id:
                result.append(x)
        return result

    def add_location(self, location):
        self.add(location)

    def update_location(self, location_id, location):
        self.update(location_id, location)

    def remove_location(self, location_id):
        self.remove(location_id)
