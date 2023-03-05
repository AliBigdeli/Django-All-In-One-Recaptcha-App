from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import CharField


from aio_recaptcha.app_settings import RECAPTCHA_REQUIRED_SCORE,RECAPTCHAV3_SECRET_KEY
from aio_recaptcha.api.validators import ReCaptchaV3Validator

# Recaptcha Field class base on char field 
class ReCaptchaV3Field(CharField):
    def __init__(self, action: str, required_score: float = None, **kwargs):
        super().__init__(**kwargs)

        # make the field writeonly
        self.write_only = True

        # validate the score and action
        self.validate_score_value(required_score, action)
        
        # assign the score value based on default or given to class
        self.required_score = (
            required_score
            or RECAPTCHA_REQUIRED_SCORE
        )

        # validating the action and score based on the secret key 
        self.__validator = ReCaptchaV3Validator(
            action=action,
            required_score=self.required_score,
            secret_key=RECAPTCHAV3_SECRET_KEY,
        )
        # adding the results to the validator property
        self.validators.append(self.__validator)

    # check to see if the given score is set correctly
    def validate_score_value(self,value, action):
        if value is None:
            return

        # check to be sure that the value is int or float
        if not isinstance(value, (int, float)):
            if action:
                message = f"Score value for action '{action}' should be int or float"
            else:
                message = "Default score value should be int or float"

            raise ImproperlyConfigured(message)

        # check to see if the score value is between 0 and 1
        if 0.0 < value < 1.0:
            if action:
                message = f"Score value for action '{action}' should be between 0.0 - 1.0"
            else:
                message = "Default score value should be between 0.0 - 1.0"

            raise ImproperlyConfigured(message)
    
    # property to get score value
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