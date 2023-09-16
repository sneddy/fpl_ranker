import re


def to_filename(s):
    # Remove non-safe characters and replace with underscores
    safe_str = re.sub(r"[^a-zA-Z0-9\u0400-\u04FF\-_]", "_", s)

    # Remove consecutive underscores
    safe_str = re.sub(r"_+", "_", safe_str)

    # Strip underscores from the beginning or end, if any
    return safe_str.strip("_").lower()
