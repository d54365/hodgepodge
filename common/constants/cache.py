class CacheConstants:
    USER_JWT_REFRESH_TOKEN = "jwt:user:refresh_token:{device}:{user_id}"  # nosec
    USER = "user:{user_id}"
    USER_TIMEOUT = 60 * 60 * 24
    USER_AGENT = "user_agent:{ua}"
    USER_AGENT_TIMEOUT = 60 * 60 * 24 * 30

    ACCOUNT_SMS_CODE = "account:sms_code:{mobile}"
    ACCOUNT_SMS_CODE_TIMEOUT = 60 * 5
    # 限制每分钟最多发送次数
    ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE = "account:sms_code:limit:minute:{ip}"
    ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE_TIMEOUT = 60
    # 限制每天最多发送次数
    ACCOUNT_SMS_CODE_LIMIT_IP_DAY = "account:sms_code:limit:day:{ip}"
    ACCOUNT_SMS_CODE_LIMIT_IP_DAY_TIMEOUT = 60 * 60 * 24
    ACCOUNT_SMS_CODE_LIMIT_IP_DAY_MAX = 10
    # 限制每个号码每天最多发送次数
    ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY = "account:sms_code:limit:day:{mobile}"
    ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY_TIMEOUT = 60 * 60 * 24
    ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY_MAX = 10
