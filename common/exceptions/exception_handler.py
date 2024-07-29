import traceback

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from loguru import logger
from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler as exception_handler_

from audit import tasks


def exception_handler(exc, ctx):
    """
    参考自Django-Styleguide
    {
        "message": "Error message",
        "extra": {}
    }
    """
    print(exc)
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    response = exception_handler_(exc, ctx)

    exception_log_data = {
        "context": {
            "api": ctx["request"].path,
            "method": ctx["request"].method,
            "body": ctx["request"].data,
            "query_params": ctx["request"].query_params,
        }
        if ctx
        else {},
    }

    # If unexpected error occurs (server error, etc.)
    if response is None:
        stack_trace = traceback.format_exc()
        exception_log_data["exception_stack"] = stack_trace

        exception_log_data["exception_stack"] = stack_trace
        tasks.save_exception_log.delay(exception_log_data)

        logger.error(stack_trace)

        data = {"message": _("服务器开了小差, 请稍后再试"), "extra": {}}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if hasattr(exc, "detail") and isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}
    else:
        if (
            isinstance(response.data["detail"], dict)
            and "detail" in response.data["detail"]
        ):
            response.data["message"] = response.data["detail"]["detail"]
        else:
            response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response


def page_error(exception):
    from django.http.response import JsonResponse

    resp = exception_handler(exception, {})
    return JsonResponse(resp.data, status=resp.status_code)
