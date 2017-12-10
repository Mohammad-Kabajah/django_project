from datetime import datetime
import pytz

__author__ = 'omar'

def date_str_to_str(date_str, original_format, result_format, utc_tz=None):
    date_obj = datetime.strptime(date_str, original_format)

    # force utc timezone aware object
    if utc_tz:
        date_obj = pytz.utc.localize(date_obj)

    return date_obj.strftime(result_format)