from models.base import Base
from providers import data_provider

TRANSFERS = []

class Transfers(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "transfer.json", TRANSFERS, is_debug)

    def get_transfers(self):
        result = []
        for x in self.get_all():
            result.append(self._with_items(x))
        return result

    def get_transfer(self, transfer_id):
        transfer = self.get_by_id(transfer_id)
        if transfer is None:
            return None
        return self._with_items(transfer)

    def get_items_in_transfer(self, transfer_id):
        rows = data_provider.fetch_transfer_item_pool().get_items_for_transfer(transfer_id)
        return [{"item_id": r["item_id"], "amount": r["amount"]} for r in rows]

    def add_transfer(self, transfer):
        items = transfer.pop("items", [])
        transfer["transfer_status"] = "Scheduled"
        self.add(transfer)
        data_provider.fetch_transfer_item_pool().set_items_for_transfer(transfer["id"], items)

    def update_transfer(self, transfer_id, transfer):
        items = transfer.pop("items", None)
        self.update(transfer_id, transfer)
        if items is not None:
            data_provider.fetch_transfer_item_pool().set_items_for_transfer(transfer_id, items)

    def remove_transfer(self, transfer_id):
        self.remove(transfer_id)
        data_provider.fetch_transfer_item_pool().remove_items_for_transfer(transfer_id)

    def _with_items(self, transfer):
        transfer = dict(transfer)
        transfer["items"] = self.get_items_in_transfer(transfer["id"])
        return transfer
