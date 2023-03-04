from django.conf import settings


# recaptcha v3 configs
RECAPTCHAV3_PUBLIC_KEY  = getattr(settings, "RECAPTCHAV3_PUBLIC_KEY", "6LcBC_kZAAAAAEZLiwQ2C0FGQE1VD7yYX2FSwW0r")
RECAPTCHAV3_PRIVATE_KEY = getattr(settings, "RECAPTCHAV3_PRIVATE_KEY", "6LcBC_kZAAAAADHV8gVD-GMLhr-rZ7c3IMa3hCh7")
RECAPTCHA_REQUIRED_SCORE = getattr(settings, "RECAPTCHA_REQUIRED_SCORE", 0.5)
RECAPTCHA_ADMIN_ENABLE = getattr(settings, "RECAPTCHA_ADMIN_ENABLE", False)


# module general configs

RECAPTCHA_VERIFY_REQUEST_TIMEOUT = getattr(settings, "RECAPTCHA_VERIFY_REQUEST_TIMEOUT", 10)
RECAPTCHA_DEV_MODE = getattr(settings, "RECAPTCHA_DEV_MODE", False)
RECAPTCHA_PROXY = getattr(settings, "RECAPTCHA_PROXY", None)
RECAPTCHA_DOMAIN = getattr(settings, "RECAPTCHA_DOMAIN", 'www.google.com')