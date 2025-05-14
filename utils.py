def clamp(value, min_value, max_value):
    if min_value > max_value:
        raise ValueError("min_value must be less than max_value")
    return max(min(value, max_value), min_value)