"""
URL configuration for django_tools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.urls import path, include

from .routers import router

urlpatterns = [
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )

# drf异常捕获捕获不到中间件里的异常, 这样设置后, 非 debug 模式下, 中间件异常也能正常捕获
handler500 = "common.exceptions.exception_handler.page_error"
