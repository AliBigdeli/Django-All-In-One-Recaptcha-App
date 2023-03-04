from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import NewsLetter


class NewsLetterSerializer(serializers.Serializer):
    
    class Meta:
        model = NewsLetter

