from models.base import Base

CLIENTS = []

class Clients(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "client.json", CLIENTS, is_debug)

    def get_clients(self):
        return self.get_all()

    def get_client(self, client_id):
        return self.get_by_id(client_id)

    def add_client(self, client):
        self.add(client)

    def update_client(self, client_id, client):
        self.update(client_id, client)

    def remove_client(self, client_id):
        self.remove(client_id)
