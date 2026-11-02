from datetime import datetime
import re


def validate_location(location: dict) -> bool:
    required_fields = {
        "id": int,
        "warehouse_id": int,
        "code": str,
        "name": str,
    }

    optional_fields = {
        "created_at": str,
        "updated_at": str,
    }

    allowed_fields = set(required_fields) | set(optional_fields)

    if not isinstance(location, dict):
        return False

    if not set(required_fields).issubset(location):
        return False

    if not set(location).issubset(allowed_fields):
        return False

    for field, expected_type in required_fields.items():
        value = location[field]

        if isinstance(value, bool) or not isinstance(value, expected_type):
            return False

        if isinstance(value, str):
            if not value.strip() or len(value) > 255:
                return False

        if isinstance(value, int) and value <= 0:
            return False

    for field, expected_type in optional_fields.items():
        if field in location:
            value = location[field]

            if not isinstance(value, expected_type):
                return False

            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return False

    if not re.fullmatch(r"[A-Za-z0-9-]+", location["code"]):
        return False

    return True
