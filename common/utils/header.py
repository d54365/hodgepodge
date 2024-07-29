from django.core.cache import caches, cache
from user_agents import parse

from common.constants.cache import CacheConstants
from common.ipware import get_client_ip


class HeaderUtil:
    @staticmethod
    def get_host(request):
        return request.META.get("HTTP_HOST")

    @staticmethod
    def get_referer(request):
        return request.META.get("HTTP_REFERER", "")

    @staticmethod
    def get_client_ip(request):
        return get_client_ip(request)

    @staticmethod
    def get_ua(request):
        return request.META.get("HTTP_USER_AGENT") or ""

    @classmethod
    def get_user_agent(cls, request):
        disk_cache = caches["disk"]
        ua = cls.get_ua(request)
        key = CacheConstants.USER_AGENT.format(ua=ua)
        user_agent = disk_cache.get(key)
        if user_agent:
            return user_agent

        user_agent = cache.get(key)
        if user_agent:
            return user_agent

        user_agent = parse(ua)

        disk_cache.set(key, user_agent, timeout=CacheConstants.USER_AGENT_TIMEOUT)
        cache.set(key, user_agent, timeout=CacheConstants.USER_AGENT_TIMEOUT)

        return user_agent

    @staticmethod
    def get_auth_header(request):
        return request.headers.get("Authorization")

    @staticmethod
    def get_user_id(request):
        user_id = request.META.get("HTTP_X_USER_ID")
        if not user_id:
            return None
        try:
            user_id = int(user_id)
        except ValueError:
            return None
        return user_id
