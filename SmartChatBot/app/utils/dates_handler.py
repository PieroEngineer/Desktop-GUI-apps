def extract_month_year(dt):
    """
    Receives a datetime object and returns:
    - month as integer (0 = January, 1 = February, ...)
    - year as string
    """
    month_zero_based = dt.month - 1  # datetime.month is 1-based
    year_str = str(dt.year)
    return month_zero_based, year_str

def merge_time_ranges_by_device(df, device_name):
    """
    Filters the DataFrame by 'EQUIPO' name and merges overlapping or touching time ranges.
    Parameters:
    - df (pd.DataFrame): DataFrame with 'EQUIPO', 'INICIO', and 'FINAL' columns.
    - equipo_name (str): The value to filter in the 'EQUIPO' column.
    Returns:
    - List[List[datetime, datetime]]: Merged list of ranges.
    """
    # Filter rows by equipo
    df_filtered = df[df['EQUIPO'] == device_name].copy()
    if df_filtered.empty:
        return []

    # Sort by start time
    df_filtered.sort_values(by="INICIO", inplace=True)

    merged = []
    current_start = None
    current_end = None

    for _, row in df_filtered.iterrows():
        start = row['INICIO']
        end = row['FINAL']

        if current_start is None:
            current_start = start
            current_end = end
        elif start <= current_end:  # overlapping or touching
            current_end = max(current_end, end)
        else:
            merged.append([current_start, current_end])
            current_start = start
            current_end = end

    # Append the last range
    if current_start is not None:
        merged.append([current_start, current_end])

    return merged