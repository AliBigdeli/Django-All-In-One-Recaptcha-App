from django import forms
from .models import NewsLetter
from aio_recaptcha.fields import ReCaptchaField
from aio_recaptcha.widgets import ReCaptchaV3


class NewsLetterForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())
    class Meta:
        model = NewsLetter
        fields = ('email','captcha' )