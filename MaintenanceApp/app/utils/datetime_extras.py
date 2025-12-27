import calendar
from datetime import datetime


def group_datetimes_by_proximity(datetimes):
    """
    Groups datetime strings by 15-minute proximity, returning ranges or single datetimes.
    Input: List of datetime strings in format '%d/%m/%Y %H:%M'.
    Output: List of strings, either single datetimes or ranges formatted as 'start al end'.
    """
    if not datetimes:
        return []

    # Parse datetimes
    date_format = '%d/%m/%Y %H:%M:%S'
    parsed = sorted([datetime.strptime(dt, date_format) for dt in datetimes])

    result = []
    i = 0
    while i < len(parsed):
        start_dt = parsed[i]
        end_dt = start_dt
        j = i + 1

        # Check for consecutive 15-minute intervals
        while j < len(parsed) and (parsed[j] - end_dt).total_seconds() / 60.0 == 15:
            end_dt = parsed[j]
            j += 1 

        # Format output
        if start_dt == end_dt:
            result.append(f'{start_dt.day} a las {'00' if start_dt.hour==0 else start_dt.hour}:{'00' if start_dt.minute==0 else start_dt.minute}')

        elif start_dt.day==end_dt.day:
            result.append(f'{start_dt.day} entre las {'00' if start_dt.hour==0 else start_dt.hour}:{'00' if start_dt.minute==0 else start_dt.minute} y {'00' if end_dt.hour==0 else end_dt.hour}:{'00' if end_dt.minute==0 else end_dt.minute}')

        i = j

    return result

def get_month_boundaries_from_datetime(dt):
    """
    Receives a datetime string ('DD/MM/YYYY HH:MM') and returns a list of:
    [first_day_of_month at 00:15, first_day_of_next_month at 00:00]
    """
    # First day of current month at 00:15
    start = dt.replace(day=1, hour=0, minute=15, second=0, microsecond=0)

    # Handle year wrap
    if dt.month == 12:
        end = dt.replace(year=dt.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end = dt.replace(month=dt.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    return [start, end]

from datetime import datetime, timedelta

def reformat_datetime(date_str, subtract_15=False):
    """
    Converts a datetime string from 'dd/mm/YYYY HH:MM:SS' to 'YYYY-mm-dd HH:MM:SS'.
    Optionally subtracts 15 minutes if subtract_15 is True.
    
    :param date_str: str, input datetime in format 'dd/mm/YYYY HH:MM:SS'
    :param subtract_15: bool, default False, if True subtracts 15 minutes
    :return: str, reformatted datetime
    """
    # Parse the input string
    dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
    
    # Subtract 15 minutes if requested
    if subtract_15:
        dt -= timedelta(minutes=15)
    
    # Return in new format
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def days_in_months(date_obj):
    year = date_obj.year
    return [calendar.monthrange(year, month)[1] for month in range(1, 13)]