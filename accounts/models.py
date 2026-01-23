from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICE=(
        ('user','User'),
        ('admin','Admin')
    )
    username = None
    email = models.EmailField(unique=True)
    role=models.CharField(max_length=10,choices=ROLE_CHOICE,default='user')
    profile_image = models.ImageField(upload_to='profile_images/',null=True,blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD='email'
    objects=CustomUserManager()

