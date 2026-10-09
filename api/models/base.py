import json
from datetime import datetime, timezone

class Base:
    def __init__(self, data_path, debug_data, is_debug=False):
        self.data_path = data_path
        self.debug_data = debug_data
        self.load(is_debug)

    def get_timestamp(self):
        # https://stackoverflow.com/a/10944136
        # https://stackoverflow.com/a/30724660
        return datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z"

    def load(self, is_debug):
        if is_debug:
            self.data = self.debug_data
        else:
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)

    def get_all(self):
        return self.data

    def get_by_id(self, id):
        for x in self.data:
            if x["id"] == id:
                return x
        return None

    def add(self, item):
        item["created_at"] = self.get_timestamp()
        item["updated_at"] = self.get_timestamp()
        self.data.append(item)

    def update(self, id, item):
        item["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == id:
                self.data[i] = item
                break

    def remove(self, id):
        for x in self.data:
            if x["id"] == id:
                self.data.remove(x)
