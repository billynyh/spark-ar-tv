import isodate

def format_duration(raw_duration):
    total = isodate.parse_duration(raw_duration).total_seconds()
    hour = total / 3600
    minute = (total / 60) % 60
    sec = total % 60

    if minute < 60:
        return "%d:%02d" % (minute, sec)
    return "%d:%02d:%02d" % (hour, minute, sec)

def formate_date(raw_date):
    return isodate.parse_date(raw_date)

