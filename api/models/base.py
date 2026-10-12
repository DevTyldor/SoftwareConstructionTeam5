import json
from datetime import datetime, timezone

class DataFileError(Exception):
    """Exception class for error throwing"""
    
    def __init__(self, path, action, cause):
        self.path = path
        self.cause = cause
        Exception.__init__(self, f"Could not {action} data file '{path}': {cause}")

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
            return
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except OSError as e:          # missing file or no permission
            raise DataFileError(self.data_path, "read", e) from e
        except ValueError as e:       # broken JSON
            raise DataFileError(self.data_path, "parse", e) from e
        if not isinstance(data, list): # not a list
            raise DataFileError(self.data_path, "load", "expected a JSON list")
        self.data = data

    def save(self):
        try:
            content = json.dumps(self.data)
        except (TypeError, ValueError) as e:
            raise DataFileError(self.data_path, "serialise data for", e) from e
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise DataFileError(self.data_path, "write", e) from e

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
                
