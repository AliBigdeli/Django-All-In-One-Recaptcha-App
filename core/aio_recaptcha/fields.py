import logging
import sys
from urllib.error import HTTPError

from django import forms
from .app_settings import RECAPTCHAV3_PUBLIC_KEY,RECAPTCHAV3_PRIVATE_KEY,RECAPTCHA_DEV_MODE
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import gettext_lazy as _

from aio_recaptcha import client
from aio_recaptcha.widgets import ReCaptchaBase, ReCaptchaV3


class ReCaptchaField(forms.CharField):
    widget = ReCaptchaV3
    default_error_messages = {
        "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
        "captcha_error": _("Error verifying reCAPTCHA, please try again."),
    }

    def __init__(self,*args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed to the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://developers.google.com/recaptcha/docs/display#render_param
        """
        super().__init__(*args, **kwargs)

        if not isinstance(self.widget, ReCaptchaBase):
            raise ImproperlyConfigured(
                "captcha.fields.ReCaptchaField.widget"
                " must be a subclass of captcha.widgets.ReCaptchaBase"
            )

        # reCAPTCHA fields are always required.
        self.required = True

        # Setup instance variables.
        self.private_key =  RECAPTCHAV3_PRIVATE_KEY
        self.public_key = RECAPTCHAV3_PUBLIC_KEY

        # Update widget attrs with data-sitekey.
        self.widget.attrs["data-sitekey"] = self.public_key
        self.dev_mode = RECAPTCHA_DEV_MODE

    def get_remote_ip(self):
        f = sys._getframe()
        while f:
            request = f.f_locals.get("request")
            if request:
                remote_ip = request.META.get("REMOTE_ADDR", "")
                forwarded_ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
                ip = remote_ip if not forwarded_ip else forwarded_ip
                return ip
            f = f.f_back

    def validate(self, value):
        super().validate(value)
        if not self.dev_mode:
            try:
                check_captcha = client.submit(
                    recaptcha_response=value,
                    private_key=self.private_key,
                    remoteip=self.get_remote_ip(),
                )

            except HTTPError:  # Catch timeouts, etc
                raise ValidationError(
                    self.error_messages["captcha_error"], code="captcha_error"
                )

            if not check_captcha.is_valid:
                # logger.warning(
                #     "ReCAPTCHA validation failed due to: %s" % check_captcha.error_codes
                # )
                raise ValidationError(
                    self.error_messages["captcha_invalid"], code="captcha_invalid"
                )

            required_score = self.widget.attrs.get("required_score")
            if float(required_score) > float(check_captcha.extra_data.get("score", 0)):
                # logger.warning(
                #     "ReCAPTCHA validation failed due to its score of %s"
                #     " being lower than the required amount." % score
                # )
                raise ValidationError(
                    self.error_messages["captcha_invalid"], code="captcha_invalid"
                )