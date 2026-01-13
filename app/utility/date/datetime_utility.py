from datetime import datetime, timedelta


class DatetimeUtility:
    """Utility class for datetime operations"""

    def to_string(self, dt: datetime, format: str = "%Y/%m/%d %H:%M:%S") -> str | None:
        """Convert datetime to string"""
        if dt is not None:
            return dt.strftime(format)
        return None

    def to_date_string(self, dt: datetime) -> str | None:
        """Convert datetime to date string (YYYY-MM-DD)"""
        if dt is not None:
            return dt.strftime("%Y-%m-%d")
        return None

    def from_string(self, string_temp: str, format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """Convert string to datetime"""
        return datetime.strptime(string_temp, format)

    def add_minutes(self, dt: datetime, minutes: int) -> datetime:
        """Add minutes to datetime"""
        delta = timedelta(minutes=minutes)
        return dt + delta

    def add_days(self, dt: datetime, days: int) -> datetime:
        """Add days to datetime"""
        delta = timedelta(days=days)
        return dt + delta

    def get_today(self) -> datetime:
        """Get current datetime"""
        return datetime.now()

    def get_timestamp(self) -> float:
        """Get current timestamp"""
        return datetime.now().timestamp()

    def compare_dates(self, date1: datetime, date2: datetime) -> int:
        """
        Compare two dates
        Returns: 1 if date1 > date2, -1 if date1 < date2, 0 if equal
        """
        if date1 > date2:
            return 1
        elif date1 < date2:
            return -1
        return 0
