import sys
from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import gettext_lazy as _
from urllib.error import HTTPError


from aio_recaptcha.client import submit
from aio_recaptcha.form.widgets import ReCaptchaBase, ReCaptchaV3
from aio_recaptcha.app_settings import RECAPTCHAV3_SITE_KEY, RECAPTCHAV3_SECRET_KEY, RECAPTCHA_DEV_MODE ,RECAPTCHA_ALWAYS_FAIL


class ReCaptchaField(forms.CharField):
    widget = ReCaptchaV3
    default_error_messages = {
        "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
        "captcha_error": _("Error verifying reCAPTCHA, please try again."),
    }

    def __init__(self, *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed to the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://developers.google.com/recaptcha/docs/display#render_param
        """
        super().__init__(*args, **kwargs)

        # check if the widget is an instance of Recaptcha
        if not isinstance(self.widget, ReCaptchaBase):
            raise ImproperlyConfigured(
                """aio_recaptcha.fields.ReCaptchaField.widget must be a subclass of aio_recaptcha.widgets.ReCaptchaBase"""
            )

        # reCAPTCHA fields are always required.
        self.required = True

        # Setup instance variables.
        self.secret_key = RECAPTCHAV3_SECRET_KEY
        self.site_key = RECAPTCHAV3_SITE_KEY

        # Update widget attrs with data-sitekey.
        self.widget.attrs["data-sitekey"] = self.site_key
        
        # check to see if we are running on dev mode
        self.dev_mode = RECAPTCHA_DEV_MODE

        self.fail_mode = RECAPTCHA_ALWAYS_FAIL
    def get_remote_ip(self):
        frame = sys._getframe()
        while frame and frame.f_back is not None:
            frame = frame.f_back
            if request := frame.f_locals.get("request"):
                x_forwarded_for = request.META.get('HTTP_REMOTE_ADDR') or request.META.get("HTTP_X_FORWARDED_FOR", "")
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR',"")
                return ip


    def validate(self, value):
        super().validate(value)
        if self.fail_mode:
            raise ValidationError(
                    self.error_messages["captcha_error"], code="captcha_error"
                )
        if not self.dev_mode:
            try:
                check_captcha = submit(
                    recaptcha_response=value,
                    secret_key=self.secret_key,
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
