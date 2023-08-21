import re
import argparse


def validate_time_delta(value):
    time_delta_pattern = r"^(\d+)(h|d|m|w)$"
    match = re.match(time_delta_pattern, value)
    if match:
        number = match.group(1)
        unit = match.group(2)
        return (number, unit)
    else:
        raise argparse.ArgumentTypeError(
            "Invalid time delta. Must be in the format of 1h, 1d, or 1m. Example: 3h"
        )
