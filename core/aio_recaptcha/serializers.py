from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import CharField


from .app_settings import RECAPTCHA_REQUIRED_SCORE,RECAPTCHAV3_PRIVATE_KEY
from .validators import ReCaptchaV3Validator



def validate_v3_settings_score_value(value: int or float or None, action: str = None):
    if value is None:
        return

    if not isinstance(value, (int, float)):
        if action:
            message = f"Score value for action '{action}' should be int or float"
        else:
            message = "Default score value should be int or float"

        raise ImproperlyConfigured(message)

    if value < 0.0 or 1.0 < value:
        if action:
            message = f"Score value for action '{action}' should be between 0.0 - 1.0"
        else:
            message = "Default score value should be between 0.0 - 1.0"

        raise ImproperlyConfigured(message)






class ReCaptchaV3Field(CharField):
    def __init__(self, action: str, required_score: float = None, **kwargs):
        super().__init__(**kwargs)

        self.write_only = True


        validate_v3_settings_score_value(required_score, action)
        self.required_score = (
            required_score
            or RECAPTCHA_REQUIRED_SCORE
        )

        self.__validator = ReCaptchaV3Validator(
            action=action,
            required_score=self.required_score,
            secret_key=RECAPTCHAV3_PRIVATE_KEY,
        )
        self.validators.append(self.__validator)

    @property
    def score(self):
        score = self.__validator.score
        if score is None:
            msg = (
                "You must call the serializer `.is_valid()` method before "
                "attempting to access the `.score` property of this field."
            )
            raise AssertionError(msg)
        return score