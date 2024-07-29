import re

from functools import lru_cache


class IpWare:
    private_ip_pattern = re.compile(
        r"^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.|169\.254\.|::1|fc00:|fe80:)",
        re.IGNORECASE,
    )

    @classmethod
    @lru_cache(maxsize=128)
    def is_private_ip(cls, ip):
        return bool(cls.private_ip_pattern.match(ip))

    @classmethod
    def get_client_ip(cls, request, right_most_proxy=False):
        ip_address = None

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_list = [ip.strip() for ip in x_forwarded_for.split(",")]
            if right_most_proxy:
                ip_address = ip_list[-1]
            else:
                ip_address = next(
                    (ip for ip in ip_list if not cls.is_private_ip(ip)), None
                )

        if not ip_address:
            ip_address = request.META.get("HTTP_X_REAL_IP") or request.META.get(
                "REMOTE_ADDR"
            )

        return ip_address


def get_client_ip(request, right_most_proxy=False):
    return IpWare.get_client_ip(request, right_most_proxy)
