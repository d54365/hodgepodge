class RegexConstants:
    USERNAME = r"^[a-zA-Z0-9_-]{3,16}$"
    MOBILE = r"^1[3-9]\d{9}$"
    PASSWORD = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*?-]{6,16}$"  # nosec
