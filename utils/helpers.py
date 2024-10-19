def format_minutes(minutes):
    sign = "-" if minutes < 0 else ""
    abs_minutes = abs(minutes)
    hours = abs_minutes // 60
    mins = abs_minutes % 60
    return f"{sign}{hours}:{mins:02d}"
