from urllib.error import HTTPError

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import ValidationError

from aio_recaptcha.client import RecaptchaResponse,submit
from aio_recaptcha.app_settings import RECAPTCHA_DEV_MODE,RECAPTCHA_ALWAYS_FAIL


class ReCaptchaValidator:
    requires_context = True

    # sample messages for each type of errors
    messages = {
        "captcha_invalid": "Error verifying reCAPTCHA, please try again.",
        "captcha_error": "Error verifying reCAPTCHA, please try again.",
    }
    
    # creating the properties as empty
    recaptcha_client_ip = ""
    recaptcha_secret_key = ""

    # setting client ip address based on request from serializers
    def set_client_ip(self, serializer_field):
        request = serializer_field.context.get("request")
        if not request:
            raise ImproperlyConfigured(
                "Couldn't get client ip address. Check your serializer gets context with request."
            )

        self.recaptcha_client_ip= self.get_client_ip(request)

    # function to  extract ip address from serializer request
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_REMOTE_ADDR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    # getting the response from the client request
    def get_response(self, value: str) -> RecaptchaResponse:
        try:
            check_captcha = submit(
                recaptcha_response=value,
                secret_key=self.recaptcha_secret_key,
                remoteip=self.recaptcha_client_ip,
            )
        except HTTPError: 
            # logger.exception("Couldn't get response, HTTPError")
            raise ValidationError(self.messages["captcha_error"], code="captcha_error")

        return check_captcha

    # check if the captcha is valid
    def pre_validate_response(self, check_captcha: RecaptchaResponse):
        if not check_captcha.is_valid:
            # logger.error(
            #     "ReCAPTCHA validation failed due to: %s", check_captcha.error_codes
            # )
            raise ValidationError(
                self.messages["captcha_invalid"], code="captcha_invalid"
            )


class ReCaptchaV3Validator(ReCaptchaValidator):
    
    
    def __init__(self, action, required_score, secret_key):
        
        # setup base property of object
        self.recaptcha_action = action
        self.recaptcha_required_score = required_score
        self.recaptcha_secret_key = secret_key
        self.score = None
        
        # getting the global configs
        self.dev_mode = RECAPTCHA_DEV_MODE
        self.fail_mode = RECAPTCHA_ALWAYS_FAIL
        
    
    def __call__(self, value, serializer_field=None):
        # on call get the client ip address
        if serializer_field and not self.recaptcha_client_ip:
            self.set_client_ip(serializer_field)

        # check to see if we are running in dev mode or not to by pass validations
        if self.dev_mode:
            # if we are running in always fail mode we will get errors
            if self.fail_mode:
                raise ValidationError(self.messages["captcha_error"], code="captcha_error")
            return

        # checking recaptcha with the api
        check_captcha = self.get_response(value)

        # pre validate recaptcha
        self.pre_validate_response(check_captcha)

        # setup score based on the response
        self.score = check_captcha.extra_data.get("score", None)
        
        # if there is no score in payload then raise an error
        if self.score is None:
            # logger.error(
            #     "The response not contains score, reCAPTCHA v3 response must"
            #     " contains score, probably secret key for reCAPTCHA v2"
            # )
            raise ValidationError(self.messages["captcha_error"], code="captcha_error")

        # setting up action name
        action = check_captcha.extra_data.get("action", "")

        # check to validate if we are right to pass the validation of minimum required score
        if self.recaptcha_required_score >= float(self.score):
            # logger.error(
            #     "ReCAPTCHA validation failed due to score of %s"
            #     " being lower than the required amount for action '%s'.",
            #     self.score,
            #     action,
            # )
            raise ValidationError(
                self.messages["captcha_invalid"], code="captcha_invalid"
            )

        # check out action name and validate it
        if self.recaptcha_action != action:
            # logger.error(
            #     "ReCAPTCHA validation failed due to value of action '%s'"
            #     " is not equal with defined '%s'.",
            #     action,
            #     self.recaptcha_action,
            # )
            raise ValidationError(
                self.messages["captcha_invalid"], code="captcha_invalid"
            )