from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Customer(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=255)
    verified_email= models.BooleanField(default=False)
    status= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True , blank= True , null=True)
    updated_at = models.DateTimeField(auto_now=True , blank= True , null=True)
    deleted_at = models.DateTimeField(auto_now=True , blank= True , null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []