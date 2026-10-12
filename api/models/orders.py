from models.base import Base
from providers import data_provider

ORDERS = []

class Orders(Base):
    def __init__(self, root_path, is_debug=False):
        Base.__init__(self, root_path + "order.json", ORDERS, is_debug)

    def get_orders(self):
        result = []
        for x in self.get_all():
            result.append(self._with_items(x))
        return result

    def get_order(self, order_id):
        order = self.get_by_id(order_id)
        if order is None:
            return None
        return self._with_items(order)

    def get_items_in_order(self, order_id):
        rows = data_provider.fetch_order_item_pool().get_items_for_order(order_id)
        return [{"item_id": r["item_id"], "amount": r["amount"]} for r in rows]

    def get_orders_for_client(self, client_id):
        result = []
        for x in self.data:
            if (x["client_id"] == client_id
                    or x["ship_to_client_id"] == client_id
                    or x["bill_to_client_id"] == client_id):
                result.append(self._with_items(x))
        return result

    def add_order(self, order):
        items = order.pop("items", [])
        self.add(order)
        data_provider.fetch_order_item_pool().set_items_for_order(order["id"], items)

    def update_order(self, order_id, order):
        items = order.pop("items", None)
        self.update(order_id, order)
        if items is not None:
            self.update_items_in_order(order_id, items)

    def update_items_in_order(self, order_id, items):
        """Replace the items of an order and keep `quantity_allocated` in sync.

        For each item, the change in ordered amount (new - old) is applied to the
        inventory row with the most on-hand stock for that item, clamped at 0 so
        `quantity_allocated` never goes negative."""
        current = self.get_items_in_order(order_id)
        current_by_item = {x["item_id"]: x["amount"] for x in current}
        new_by_item = {x["item_id"]: x["amount"] for x in items}

        inventory_pool = data_provider.fetch_inventory_pool()
        for item_id, new_amount in new_by_item.items():
            old_amount = current_by_item.get(item_id, 0)
            delta = new_amount - old_amount
            if delta != 0:
                self._apply_allocation_delta(inventory_pool, item_id, delta)
        for item_id, old_amount in current_by_item.items():
            if item_id not in new_by_item:
                self._apply_allocation_delta(inventory_pool, item_id, -old_amount)

        data_provider.fetch_order_item_pool().set_items_for_order(order_id, items)

    @staticmethod
    def _apply_allocation_delta(inventory_pool, item_id, delta):
        inventories = inventory_pool.get_inventories_for_item(item_id)
        if not inventories:
            return
        target = max(inventories, key=lambda z: z["quantity_on_hand"])
        target["quantity_allocated"] = max(0, target["quantity_allocated"] + delta)
        inventory_pool.update_inventory(item_id, target["location_id"], target)

    def remove_order(self, order_id):
        self.remove(order_id)
        data_provider.fetch_order_item_pool().remove_items_for_order(order_id)

    def _with_items(self, order):
        order = dict(order)
        order["items"] = self.get_items_in_order(order["id"])
        return order
