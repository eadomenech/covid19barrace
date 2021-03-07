from datetime import date, timedelta


def date_range(date_init, date_end, idays=1):
    dater = []
    date_current = date.fromisoformat(date_init)
    date_end = date.fromisoformat(date_end)
    oneDay = timedelta(days=+idays)
    while date_current <= date_end:
        dater.append(date_current.isoformat())
        date_current += oneDay
    if date_end.isoformat() not in dater:
        dater.append(date_end.isoformat())
    return dater


def pretty_resolution(resolution):
    return f"{int(100 * resolution[0])}x{int(100 * resolution[1])}"
