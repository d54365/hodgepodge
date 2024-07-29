import os
import sys
from pathlib import Path

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Queue, Exchange

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR.parent))

# 设置默认的 Django 设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hodgepodge.settings")

app = Celery("hodgepodge")

# celery -A hodgepodge worker -Q log -l info -c 1
# celery -A hodgepodge worker -Q default -l info -c 1
# celery -A hodgepodge beat -l info -c 1

app.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("log", Exchange("log"), routing_key="log"),
)

app.conf.task_routes = {
    "audit.tasks.save_operation_log": {
        "queue": "log",
    },
    "audit.tasks.save_exception_log": {
        "queue": "log",
    },
    "audit.tasks.save_login_log": {
        "queue": "log",
    },
}

app.conf.update(
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
)

# 使用 Django 的设置文件进行配置
app.config_from_object("django.conf:settings", namespace="CELERY")

# 配置定时任务
app.conf.beat_schedule = {
    "update-exchange-rates-every-day": {
        "task": "bill.tasks.update_currency_exchange_rate",
        "schedule": crontab(hour="00"),
    },
}

# 自动发现每个已注册的 Django 应用中的 tasks.py 文件
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
