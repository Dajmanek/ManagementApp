import time
import datetime


def current_time_mills() -> int:
    return round(time.time() * 1000)


def mills_to_date_time(mills: int) -> str:
    return datetime.datetime.fromtimestamp(mills / 1000).strftime('%Y-%m-%d %H:%M:%S')[:-3]
