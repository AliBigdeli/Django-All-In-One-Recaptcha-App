from django.contrib import admin
from aio_recaptcha.forms import CustomAdminAuthenticationForm
from .app_settings  import RECAPTCHA_ADMIN_ENABLE


if RECAPTCHA_ADMIN_ENABLE:
    admin.autodiscover()
    admin.site.login_form = CustomAdminAuthenticationForm
    admin.site.login_template = 'aio_recaptcha/login.html'