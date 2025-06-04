from django.db import models
from django.contrib.auth.models import User

size = models.BigIntegerField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

class MediaFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    filename = models.CharField(max_length=255)
    size = models.BigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
