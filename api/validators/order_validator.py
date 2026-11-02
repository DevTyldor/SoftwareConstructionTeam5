import re
from datetime import datetime


def validate_order(order: dict) -> bool:
    required_fields = {
        "id": int,
        "client_id": int,
        "order_date": str,
        "request_date": str,
        "reference": str,
        "customer_po_number": str,
        "order_status": str,
        "shipping_notes": (str, type(None)),
        "warehouse_id": int,
        "ship_to_client_id": int,
        "bill_to_client_id": int,
    }

    optional_fields = {"created_at": str, "updated_at": str}

    allowed_fields = set(required_fields) | set(optional_fields)

    if not isinstance(order, dict):
        return False

    if not set(required_fields).issubset(order):
        return False

    if not set(order).issubset(allowed_fields):
        return False

    for field, expected_type in required_fields.items():
        value = order[field]

        if not isinstance(value, expected_type):
            return False

        if isinstance(value, str) and not value.strip():
            return False

        if isinstance(value, str) and len(value) > 255:
            return False

    for field, expected_type in optional_fields.items():
        if field in order:
            value = order[field]

            if not isinstance(value, expected_type):
                return False

            if not value.strip() or len(value) > 255:
                return False

    id_fields = (
        "id",
        "client_id",
        "warehouse_id",
        "ship_to_client_id",
        "bill_to_client_id",
    )

    for field in id_fields:
        if order[field] <= 0:
            return False

    if not re.fullmatch(r"[A-Za-z0-9-]+", order["reference"]):
        return False

    if not re.fullmatch(r"[A-Za-z0-9-]+", order["customer_po_number"]):
        return False

    valid_statuses = {"Pending", "Shipped", "Delivered"}

    if order["order_status"] not in valid_statuses:
        return False

    for field in ("order_date", "request_date", "created_at", "updated_at"):
        if field in order:
            try:
                datetime.fromisoformat(order[field].replace("Z", "+00:00"))
            except ValueError:
                return False

    return True


# needs team discussion on the format --> get returns smaller versions
# OUT OF USE
def validate_order_item(order_item: dict) -> bool:
    required_fields = {
        "id": int,
        "order_id": int,
        "item_id": int,
        "amount": int,
        "unit_price": (int, float),
    }

    allowed_fields = set(required_fields)

    if not isinstance(order_item, dict):
        return False

    if not set(required_fields).issubset(order_item):
        return False

    if not set(order_item).issubset(allowed_fields):
        return False

    for field, expected_type in required_fields.items():
        value = order_item[field]

        if not isinstance(value, expected_type):
            return False

        if value <= 0:
            return False

    if isinstance(order_item["unit_price"], bool):
        return False

    return True
