from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# recaptcha v3 configs
RECAPTCHAV3_SITE_KEY = getattr(
    settings, "RECAPTCHAV3_SITE_KEY", "6LcBC_kZAAAAAEZLiwQ2C0FGQE1VD7yYX2FSwW0r"
)
RECAPTCHAV3_SECRET_KEY = getattr(
    settings, "RECAPTCHAV3_SECRET_KEY", "6LcBC_kZAAAAADHV8gVD-GMLhr-rZ7c3IMa3hCh7"
)
RECAPTCHA_REQUIRED_SCORE = getattr(settings, "RECAPTCHA_REQUIRED_SCORE", 0.5)
RECAPTCHA_ADMIN_ENABLE = getattr(settings, "RECAPTCHA_ADMIN_ENABLE", False)


# module general configs
RECAPTCHA_VERIFY_REQUEST_TIMEOUT = getattr(
    settings, "RECAPTCHA_VERIFY_REQUEST_TIMEOUT", 10
)
RECAPTCHA_DEV_MODE = getattr(settings, "RECAPTCHA_DEV_MODE", True)
RECAPTCHA_ALWAYS_FAIL = getattr(settings, "RECAPTCHA_ALWAYS_FAIL", True)
RECAPTCHA_PROXY = getattr(settings, "RECAPTCHA_PROXY", None)
RECAPTCHA_DOMAIN = getattr(settings, "RECAPTCHA_DOMAIN", "www.google.com")

if not RECAPTCHA_DEV_MODE and RECAPTCHA_ALWAYS_FAIL:
    raise ImproperlyConfigured(
        "You cannot be in Always Fail Mode when you are not running dev mode"
    )
