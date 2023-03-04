from django.urls import path,include
from . import views

app_name = "api"

urlpatterns = [
    path(
        "newsletter",
        views.NewsLetterModelViewSet.as_view(
            {"post": "create"}
        ),
        name="newsletter",
    ),

]