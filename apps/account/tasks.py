from celery import shared_task
from django.core.cache import cache

from common.constants.cache import CacheConstants
from common.utils.random import RandomUtil


@shared_task
def send_sms_code(mobile):
    code = RandomUtil.generate_number(6)

    # 发送短信...

    cache.set(
        CacheConstants.ACCOUNT_SMS_CODE.format(mobile=mobile),
        code,
        CacheConstants.ACCOUNT_SMS_CODE_TIMEOUT,
    )
