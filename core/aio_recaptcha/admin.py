from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm

from aio_recaptcha.form.fields import ReCaptchaField
from aio_recaptcha.form.widgets import ReCaptchaV3

from aio_recaptcha.app_settings  import RECAPTCHA_ADMIN_ENABLE

# adding recaptcha to admin form
class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())


if RECAPTCHA_ADMIN_ENABLE:
    admin.autodiscover()
    admin.site.login_form = CustomAdminAuthenticationForm
    admin.site.login_template = 'aio_recaptcha/login.html'