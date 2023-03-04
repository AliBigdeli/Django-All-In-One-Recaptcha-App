from django.contrib import admin
from aio_recaptcha.forms import CustomAdminAuthenticationForm


admin.autodiscover()
admin.site.login_form = CustomAdminAuthenticationForm
admin.site.login_template = 'aio_recaptcha/login.html'