from datetime import datetime
from time import strptime, mktime


def form2datetime(formtime):
    str_format = "%Y-%m-%d"  # TODO fix format to support hours and minutes! to specify exact start time
    return datetime.fromtimestamp(mktime((strptime(formtime, str_format))))

