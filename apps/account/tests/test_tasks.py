from rest_framework.test import APITestCase

from account import tasks


class AccountTaskTestCase(APITestCase):
    @staticmethod
    def test_send_sms_code():
        tasks.send_sms_code("13000000000")
