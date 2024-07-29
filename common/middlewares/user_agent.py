from django.utils.deprecation import MiddlewareMixin

from common.utils.header import HeaderUtil


class UserAgentMiddleware(MiddlewareMixin):
    def __call__(self, request):
        # 在请求对象上添加一个懒加载的 user_agent 属性
        request.__class__.user_agent = property(self._get_user_agent)
        response = self.get_response(request)
        return response

    @staticmethod
    def _get_user_agent(request):
        return HeaderUtil.get_user_agent(request)
