import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.test import TestCase

from common.utils.timezone import TimezoneUtil


class TimezoneUtilTestCase(TestCase):
    def setUp(self):
        self.local_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
        self.utc_time = datetime.datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
        )

    def test_convert_local_to_utc(self):
        local_dt = self.local_time.replace(tzinfo=ZoneInfo(settings.TIME_ZONE))
        utc_dt = TimezoneUtil.convert_local_to_utc(self.local_time)
        self.assertEqual(utc_dt, local_dt.astimezone(datetime.timezone.utc))

    def test_convert_str_local_to_utc(self):
        local_str = "2023-01-01 12:00:00"
        utc_dt = TimezoneUtil.convert_str_local_to_utc(local_str)
        expected_utc = self.local_time.replace(
            tzinfo=ZoneInfo(settings.TIME_ZONE)
        ).astimezone(datetime.timezone.utc)
        self.assertEqual(utc_dt, expected_utc)

    def test_convert_utc_to_local(self):
        local_dt = TimezoneUtil.convert_utc_to_local(self.utc_time)
        self.assertEqual(
            local_dt, self.utc_time.astimezone(ZoneInfo(settings.TIME_ZONE))
        )
