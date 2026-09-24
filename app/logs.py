import time

request_log = []  # list of (timestamp, uuid) tuples

def log_request(uuid: str):
    request_log.append((time.time(), uuid))

def count_requests_last_n_seconds(n: int = 30) -> int:
    cutoff = time.time() - n
    return sum(1 for ts, _ in request_log if ts >= cutoff)