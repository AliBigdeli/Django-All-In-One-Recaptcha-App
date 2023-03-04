from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import *
from ..models import *


class NewsLetterModelViewSet(viewsets.ModelViewSet):
    
    serializer_class = NewsLetterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details":"successfully signed up to newsletter"}, status=status.HTTP_201_CREATED)
