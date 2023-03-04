from django.contrib.admin.forms import AdminAuthenticationForm 


from aio_recaptcha.fields import ReCaptchaField
from aio_recaptcha.widgets import ReCaptchaV3

class CustomAdminAuthenticationForm(AdminAuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())