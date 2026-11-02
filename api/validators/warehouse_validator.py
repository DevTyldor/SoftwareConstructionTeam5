import re
from datetime import datetime


def validate_warehouse(warehouse: dict) -> bool:
    required_fields = {
        "id": int,
        "code": str,
        "name": str,
        "address": str,
        "city": str,
        "zip_code": str,
        "province": str,
        "country": str,
        "contact_name": str,
        "contact_phone": str,
        "contact_email": str,
    }

    optional_fields = {"created_at": str, "updated_at": str}

    allowed_fields = set(required_fields) | set(optional_fields)

    if not isinstance(warehouse, dict):
        return False

    if not set(required_fields).issubset(warehouse):
        return False

    if not set(warehouse).issubset(allowed_fields):
        return False

    for field, expected_type in required_fields.items():
        value = warehouse[field]

        if not isinstance(value, expected_type):
            return False

        if isinstance(value, str) and not value.strip():
            return False

        if isinstance(value, str) and len(value) > 255:
            return False

    for field, expected_type in optional_fields.items():
        if field in warehouse:
            value = warehouse[field]

            if not isinstance(value, expected_type):
                return False

            if not value.strip() or len(value) > 255:
                return False

    if warehouse["id"] <= 0:
        return False

    if not re.fullmatch(r"[A-Za-z0-9-]+", warehouse["code"]):
        return False

    if not re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", warehouse["contact_email"]):
        return False

    phone = warehouse["contact_phone"]

    if not re.fullmatch(r"\+?[0-9 ()-]{8,20}", phone):
        return False

    if len(re.sub(r"[^0-9]", "", phone)) < 8:
        return False

    if not re.fullmatch(r"[0-9]{4}\s?[A-Za-z]{2}", warehouse["zip_code"]):
        return False

    for field in ("created_at", "updated_at"):
        if field in warehouse:
            try:
                datetime.fromisoformat(warehouse[field].replace("Z", "+00:00"))
            except ValueError:
                return False

    return True
