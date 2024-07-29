from django.utils import timezone

from audit import tasks
from common.utils.header import HeaderUtil
from common.utils.json import JsonUtil, JSONDecodeError


class LoggingMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.sensitive_headers = ("Authorization", "Proxy-Authorization")
        self.sensitive_body = ("password",)
        self.max_body_length = 50000

    def __call__(self, request):
        cached_request_body = request.body
        start_at = timezone.now()

        response = self.get_response(request)

        query_params = {}
        for k in request.GET.keys():
            query_params[k] = request.GET.getlist(k)

        end_at = timezone.now()

        body = self._get_request_body(cached_request_body)
        if body:
            try:
                body = JsonUtil.loads(body)
                body = self._log_request_body(body)
            except JSONDecodeError:
                pass

        user_agents = request.user_agent
        data = {
            "user_id": HeaderUtil.get_user_id(request),
            "ip": HeaderUtil.get_client_ip(request),
            "browser": user_agents.browser.family,
            "os": user_agents.os.family,
            "device": user_agents.device.family,
            "api": request.path,
            "start_at": start_at,
            "end_at": end_at,
            "duration": int((end_at - start_at).total_seconds() * 1000),
            "status_code": response.status_code,
            "response": response.content.decode()
            if response.status_code in range(400, 500)
            else None,
            "method": request.method,
            "headers": {
                "host": HeaderUtil.get_host(request),
                "referer": HeaderUtil.get_referer(request),
                "ua": user_agents.ua_string,
            },
            "query_params": query_params,
            "body": body if isinstance(body, dict) else None,
        }
        tasks.save_operation_log.delay(data)
        return response

    def _log_request_headers(self, request):
        return {
            k: v if k not in self.sensitive_headers else "*****"
            for k, v in request.headers.items()
        }

    def _get_request_body(self, cached_request_body):
        if cached_request_body is not None:
            return self._chunked_to_max(cached_request_body)
        return cached_request_body

    def _log_request_body(self, body):
        if not body or not isinstance(body, dict):
            return
        return {
            k: v if k not in self.sensitive_body else "*****" for k, v in body.items()
        }

    def _chunked_to_max(self, msg):
        return msg[0 : self.max_body_length]  # noqa
