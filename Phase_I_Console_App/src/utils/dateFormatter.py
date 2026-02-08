"""
Date formatting utilities for human-readable timestamps.

This module provides functions to format dates in a human-readable way
for display in the CLI application.
"""

from datetime import datetime
from typing import Optional


def format_datetime(dt: Optional[datetime]) -> str:
    """Format datetime object to human-readable string"""
    if dt is None:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(dt: Optional[datetime]) -> str:
    """Format datetime object to date only (YYYY-MM-DD)"""
    if dt is None:
        return ""
    return dt.strftime("%Y-%m-%d")


def format_time(dt: Optional[datetime]) -> str:
    """Format datetime object to time only (HH:MM:SS)"""
    if dt is None:
        return ""
    return dt.strftime("%H:%M:%S")


def format_datetime_for_display(dt: Optional[datetime]) -> str:
    """Format datetime in a user-friendly way for display in the application"""
    if dt is None:
        return "N/A"

    now = datetime.now()
    diff = now - dt

    # If the date is today
    if diff.days == 0:
        return f"Today at {dt.strftime('%H:%M')}"
    # If the date is yesterday
    elif diff.days == 1:
        return f"Yesterday at {dt.strftime('%H:%M')}"
    # If it's within the last week
    elif diff.days < 7:
        return dt.strftime('%A at %H:%M')  # e.g., "Monday at 14:30"
    # Otherwise, show the date
    else:
        return dt.strftime('%Y-%m-%d %H:%M')


def parse_datetime(date_str: str) -> Optional[datetime]:
    """Parse a date string to datetime object"""
    if not date_str:
        return None

    # Try different common formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # If no format worked, return None
    return None