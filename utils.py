def parse_time(time_s):
    """
    Parse the given time string into a time (in minutes)
    Input:
        time_s (str): The time string to parse. Format is expected to be 'h:m'.
    """
    h, m = [int(s) for s in time_s.split(":")]
    return (h * 60) + m