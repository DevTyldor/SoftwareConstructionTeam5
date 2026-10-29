from providers import data_provider
from processors import notification_processor
from endpoints.base import check_access, read_json, send_json, send_status

# GET /transfers
# GET /transfers/{id}
# GET /transfers/{id}/items
def handle_get_transfers(self, user, transfer_id=None, get_items=False):
    if not check_access(self, user, "transfers", "get"):
        return

    if get_items:
        transfers = data_provider.fetch_transfer_pool().get_items_in_transfer(
            transfer_id
        )

    elif transfer_id is None:
        transfers = data_provider.fetch_transfer_pool().get_transfers()

    else:
        transfers = data_provider.fetch_transfer_pool().get_transfer(transfer_id)

    send_json(self, transfers)


# POST /transfers
def handle_post_transfers(self, user):
    if not check_access(self, user, "transfers", "post"):
        return

    new_transfer = read_json(self)

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.add_transfer(new_transfer)
    transfer_manager.save()

    notification_processor.push(f"Scheduled batch transfer {new_transfer['id']}")

    send_status(self, 201)


# PUT /transfers/{id}
# PUT /transfers/{id}/commit
def handle_put_transfers(self, user, transfer_id, commit=False):
    if not check_access(self, user, "transfers", "put"):
        return

    if not commit:
        updated_transfer = read_json(self)

        transfer_manager = data_provider.fetch_transfer_pool()
        transfer_manager.update_transfer(transfer_id, updated_transfer)
        transfer_manager.save()

        send_status(self, 200)
        return

    transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
    from_location_id = transfer["from_location_id"]
    to_location_id = transfer["to_location_id"]

    inventory_pool = data_provider.fetch_inventory_pool()

    for x in transfer["items"]:
        item_id = x["item_id"]
        amount = x["amount"]

        # decrease on-hand at the source location
        src = inventory_pool.get_inventory(item_id, from_location_id)

        if src is not None:
            src["quantity_on_hand"] -= amount
            inventory_pool.update_inventory(item_id, from_location_id, src)

        # increase (or create) on-hand at the destination location
        dst = inventory_pool.get_inventory(item_id, to_location_id)

        if dst is not None:
            dst["quantity_on_hand"] += amount
            inventory_pool.update_inventory(item_id, to_location_id, dst)

        else:
            inventory_pool.add_inventory(
                {
                    "item_id": item_id,
                    "location_id": to_location_id,
                    "quantity_on_hand": amount,
                    "quantity_expected": 0,
                    "quantity_ordered": 0,
                    "quantity_allocated": 0,
                }
            )

    transfer["transfer_status"] = "Processed"
    transfer.pop("items", None)

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.update_transfer(transfer_id, transfer)

    notification_processor.push(f"Processed batch transfer with id:{transfer['id']}")

    transfer_manager.save()
    inventory_pool.save()

    send_status(self, 200)
    

# DELETE /transfers/{id}
def handle_delete_transfers(self, user, transfer_id):
    if not check_access(self, user, "transfers", "delete"):
        return

    transfer_manager = data_provider.fetch_transfer_pool()
    transfer_manager.remove_transfer(transfer_id)
    transfer_manager.save()

    send_status(self, 200)