from django.test import TestCase, RequestFactory

from common.ipware.ip import get_client_ip, IpWare


class IpWareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_is_private_ip(self):
        private_ips = [
            "10.0.0.1",
            "172.16.0.1",
            "192.168.0.1",
            "127.0.0.1",
            "::1",
            "fc00::",
            "fe80::",
        ]
        public_ips = ["8.8.8.8", "1.1.1.1", "2001:4860:4860::8888"]

        for ip in private_ips:
            self.assertTrue(
                IpWare.is_private_ip(ip), f"{ip} should be recognized as private"
            )

        for ip in public_ips:
            self.assertFalse(
                IpWare.is_private_ip(ip), f"{ip} should be recognized as public"
            )

    def test_get_client_ip_no_proxies(self):
        request = self.factory.get("/", REMOTE_ADDR="8.8.8.8")
        ip = get_client_ip(request)
        self.assertEqual(ip, "8.8.8.8")

    def test_get_client_ip_with_x_forwarded_for(self):
        request = self.factory.get("/", HTTP_X_FORWARDED_FOR="8.8.8.8, 192.168.0.1")
        ip = get_client_ip(request)
        self.assertEqual(ip, "8.8.8.8")

    def test_get_client_ip_with_x_real_ip(self):
        request = self.factory.get("/", HTTP_X_REAL_IP="8.8.8.8")
        ip = get_client_ip(request)
        self.assertEqual(ip, "8.8.8.8")

    def test_get_client_ip_with_private_x_forwarded_for(self):
        request = self.factory.get("/", HTTP_X_FORWARDED_FOR="192.168.0.1, 8.8.8.8")
        ip = get_client_ip(request)
        self.assertEqual(ip, "8.8.8.8")

    def test_get_client_ip_with_right_most_proxy(self):
        request = self.factory.get("/", HTTP_X_FORWARDED_FOR="192.168.0.1, 8.8.8.8")
        ip = get_client_ip(request, right_most_proxy=True)
        self.assertEqual(ip, "8.8.8.8")

    def test_get_client_ip_no_forwarded_for_or_real_ip(self):
        request = self.factory.get("/", REMOTE_ADDR="8.8.8.8")
        ip = get_client_ip(request)
        self.assertEqual(ip, "8.8.8.8")
