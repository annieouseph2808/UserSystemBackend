from django.db import models

# Create your models here.
class User(models.Model):
    ROLES=(("superadmin","Super Admin"),("user","User"))
    email=models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255,choices=ROLES)
    is_active = models.BooleanField(default=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    lastUpdatedOn =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email