import uuid
from urllib.parse import urlencode
from django.forms import widgets

from .app_settings import RECAPTCHA_DOMAIN,RECAPTCHA_REQUIRED_SCORE

class ReCaptchaBase(widgets.Widget):
    """
    Base widget to be used for Google ReCAPTCHA.
    public_key -- String value: can optionally be passed to not make use of the
        project wide Google Site Key.
    """

    recaptcha_response_name = "g-recaptcha-response"

    def __init__(self, api_params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid.uuid4().hex
        self.api_params = api_params or {}

    def value_from_datadict(self, data, files, name):
        return data.get(self.recaptcha_response_name, None)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        params = urlencode(self.api_params)
        context.update(
            {
                "public_key": self.attrs["data-sitekey"],
                "widget_uuid": self.uuid,
                "api_params": params,
                "recaptcha_domain": RECAPTCHA_DOMAIN,
            }
        )
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-widget-uuid"] = self.uuid

        # Support the ability to override some of the Google data attrs.
        attrs["data-callback"] = base_attrs.get(
            "data-callback", "onSubmit_%s" % self.uuid
        )
        attrs["data-size"] = base_attrs.get("data-size", "normal")
        return attrs



class ReCaptchaV3(ReCaptchaBase):
    template_name = "aio_recaptcha/widget_v3.html"

    def __init__(self, api_params=None, *args, **kwargs):
        super().__init__(api_params=api_params, *args, **kwargs)
        if not self.attrs.get("required_score", None):
            self.attrs["required_score"] = RECAPTCHA_REQUIRED_SCORE

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        return attrs

    def value_from_datadict(self, data, files, name):
        return data.get(name)