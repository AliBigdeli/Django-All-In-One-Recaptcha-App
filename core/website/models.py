from django.db import models


# Create your models here.

class NewsLetter(models.Model):
    email = models.EmailField()