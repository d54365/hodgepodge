from django.core.cache import caches, cache
from django.test import TestCase, RequestFactory
from user_agents import parse

from common.constants.cache import CacheConstants
from common.utils.header import HeaderUtil


class HeaderUtilTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_host(self):
        request = self.factory.get("/", HTTP_HOST="example.com")
        host = HeaderUtil.get_host(request)
        self.assertEqual(host, "example.com")

    def test_get_referer(self):
        request = self.factory.get("/", HTTP_REFERER="http://example.com")
        referer = HeaderUtil.get_referer(request)
        self.assertEqual(referer, "http://example.com")

    def test_get_client_ip(self):
        request = self.factory.get("/", REMOTE_ADDR="8.8.8.8")
        client_ip = HeaderUtil.get_client_ip(request)
        self.assertEqual(client_ip, "8.8.8.8")

    def test_get_ua(self):
        request = self.factory.get("/", HTTP_USER_AGENT="Mozilla/5.0")
        user_agent = HeaderUtil.get_ua(request)
        self.assertEqual(user_agent, "Mozilla/5.0")

    def test_get_user_agent_with_no_cache(self):
        ua = "Mozilla/5.0"
        key = CacheConstants.USER_AGENT.format(ua=ua)

        disk_cache = caches["disk"]

        disk_cache.delete(key)
        cache.delete(key)

        request = self.factory.get("/", HTTP_USER_AGENT=ua)
        user_agent = HeaderUtil.get_user_agent(request)
        parsed_ua = parse(ua)
        self.assertEqual(str(user_agent), str(parsed_ua))

    def test_get_user_agent_with_disk_cache(self):
        request = self.factory.get("/", HTTP_USER_AGENT="Mozilla/5.0")
        user_agent = HeaderUtil.get_user_agent(request)
        parsed_ua = parse("Mozilla/5.0")
        self.assertEqual(str(user_agent), str(parsed_ua))

    def test_get_user_agent_with_redis_cache(self):
        ua = "Mozilla/5.0"
        key = CacheConstants.USER_AGENT.format(ua=ua)

        disk_cache = caches["disk"]
        disk_cache.delete(key)

        request = self.factory.get("/", HTTP_USER_AGENT=ua)
        user_agent = HeaderUtil.get_user_agent(request)
        parsed_ua = parse(ua)
        self.assertEqual(str(user_agent), str(parsed_ua))

    def test_get_auth_header(self):
        request = self.factory.get("/", HTTP_AUTHORIZATION="Bearer token")
        auth_header = HeaderUtil.get_auth_header(request)
        self.assertEqual(auth_header, "Bearer token")

    def test_get_user_id(self):
        request = self.factory.get("/", HTTP_X_USER_ID="123")
        user_id = HeaderUtil.get_user_id(request)
        self.assertEqual(user_id, 123)

    def test_get_user_id_invalid(self):
        request = self.factory.get("/", HTTP_X_USER_ID="invalid")
        user_id = HeaderUtil.get_user_id(request)
        self.assertIsNone(user_id)
