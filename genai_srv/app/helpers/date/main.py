from datetime import datetime


def now_datetime() -> str:
    data = datetime.strptime("2024-12-01 11:30:00", "%Y-%m-%d %H:%M:%S")
    return str(data.date())
