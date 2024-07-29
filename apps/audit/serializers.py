from rest_framework import serializers

from .models import LoginLog, OperationLog, ExceptionLog


class LoginLogOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = (
            "id",
            "user_id",
            "ip",
            "browser",
            "os",
            "device",
            "login_result",
            "content",
            "created_at",
        )


class OperationLogOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = (
            "id",
            "user_id",
            "ip",
            "browser",
            "os",
            "device",
            "api",
            "duration",
            "status_code",
            "response",
            "method",
            "query_params",
            "body",
            "headers",
            "created_at",
        )


class ExceptionLogOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionLog
        fields = (
            "id",
            "context",
            "exception_stack",
            "created_at",
        )
