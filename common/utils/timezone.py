import datetime
from zoneinfo import ZoneInfo

from django.conf import settings


class TimezoneUtil:
    @staticmethod
    def convert_local_to_utc(dt: datetime.datetime):
        tz = ZoneInfo(settings.TIME_ZONE)
        return dt.replace(tzinfo=tz).astimezone(datetime.timezone.utc)

    @classmethod
    def convert_str_local_to_utc(cls, s: str):
        dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return cls.convert_local_to_utc(dt)

    @staticmethod
    def convert_utc_to_local(dt: datetime.datetime):
        return dt.astimezone(ZoneInfo(settings.TIME_ZONE))
