from datetime import datetime


def get_current_timestamp() -> int:
    return int(datetime.utcnow().timestamp())
