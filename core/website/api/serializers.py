from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import NewsLetter
from aio_recaptcha.serializers import ReCaptchaV3Field


class NewsLetterSerializer(serializers.ModelSerializer):
    captcha =  ReCaptchaV3Field(
        action="validate_captcha",  
    )
    class Meta:
        model = NewsLetter
        fields = ['email','captcha']
    
    
    def validate(self, attrs):
        attrs.pop("captcha",None)
        return super().validate(attrs)
