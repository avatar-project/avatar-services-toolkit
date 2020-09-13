from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Optional

SAINT_PETERSBURG_TIME_ZONE = timezone(timedelta(hours=3))


class DefaultTimezones(Enum):
    input = timezone.utc
    output = SAINT_PETERSBURG_TIME_ZONE


class TimeCastMixin:

    def datetime_field_to_iso(self,
                              field_name: str,
                              time_zone: timezone = DefaultTimezones.output.value) -> Optional[str]:
        value: datetime = getattr(self, field_name)
        if value is None:
            return None
        if not isinstance(value, datetime):
            raise KeyError
        return self.datetime_to_iso(value, time_zone)

    def iso_field_to_datetime(self,
                              field_name: str,
                              time_zone: timezone = DefaultTimezones.output.value) -> Optional[datetime]:
        value: str = getattr(self, field_name)
        if value is None:
            return None
        if not isinstance(value, str):
            raise KeyError
        return self.iso_to_datetime(value, time_zone)

    @staticmethod
    def datetime_to_iso(value: datetime,
                        time_zone: timezone = DefaultTimezones.output.value) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=DefaultTimezones.input.value)
        value = value.astimezone(time_zone)
        return value.isoformat()

    @staticmethod
    def iso_to_datetime(value: str,
                        time_zone: timezone = DefaultTimezones.output.value) -> datetime:
        timestamp = datetime.fromisoformat(value)
        if timestamp.tzinfo is None:
            timestamp.replace(tzinfo=DefaultTimezones.input.value)
        timestamp = timestamp.astimezone(time_zone)
        return timestamp

    @staticmethod
    def utc_now():
        return datetime.utcnow().replace(tzinfo=timezone.utc)
