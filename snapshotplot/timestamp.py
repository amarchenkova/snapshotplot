"""
Centralized timestamp handling for snapshotplot.

This module provides a single source of truth for timestamps used across
all snapshot operations to ensure consistency.
"""

import time
from datetime import datetime, timezone
from typing import Optional

# Global variable to store the run-wide timestamp
_GLOBAL_TIMESTAMP: Optional[str] = None
_GLOBAL_DATETIME: Optional[datetime] = None

# Track the last emitted timestamp string to ensure monotonicity across calls
_LAST_EMITTED_TIMESTAMP: Optional[str] = None


def generate_timestamp() -> str:
    """
    Generate a new UTC timestamp for the current snapshot run.
    Returns:
        str: Timestamp in format YYYYMMDD_HHMMSS_milliseconds (3 digits)
    """
    global _GLOBAL_TIMESTAMP, _GLOBAL_DATETIME, _LAST_EMITTED_TIMESTAMP

    # Ensure uniqueness at millisecond precision
    while True:
        dt = datetime.now(timezone.utc)
        candidate = dt.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Trim to milliseconds
        if candidate != _LAST_EMITTED_TIMESTAMP:
            break
        # Wait for the next millisecond to avoid duplicates
        time.sleep(0.001)

    _GLOBAL_TIMESTAMP = candidate
    _GLOBAL_DATETIME = dt
    _LAST_EMITTED_TIMESTAMP = candidate
    return candidate


def get_current_timestamp() -> str:
    """
    Get the current timestamp. Generate one if not exists.
    Returns:
        str: Current timestamp
    """
    global _GLOBAL_TIMESTAMP
    if _GLOBAL_TIMESTAMP is None:
        return generate_timestamp()
    return _GLOBAL_TIMESTAMP


def get_current_datetime() -> datetime:
    """
    Get the current datetime object. Generate one if not exists.
    Returns:
        datetime: Current datetime in UTC
    """
    global _GLOBAL_DATETIME
    if _GLOBAL_DATETIME is None:
        generate_timestamp()
    return _GLOBAL_DATETIME


def reset_timestamp() -> None:
    """Reset the current timestamp (for new snapshot runs)."""
    global _GLOBAL_TIMESTAMP, _GLOBAL_DATETIME
    _GLOBAL_TIMESTAMP = None
    _GLOBAL_DATETIME = None

# Aliases for compatibility with previous code
get_timestamp = get_current_timestamp
generate_new_timestamp = get_current_timestamp
get_datetime = get_current_datetime 