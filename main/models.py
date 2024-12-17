from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , User
from django.contrib.auth.hashers import make_password, check_password

class ScribeManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


class Scribe(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    qualification = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    languages = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    objects = ScribeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
class ScribeRequest(models.Model):
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()
    exam_center = models.CharField(max_length=200)
    languages = models.JSONField()  # Use a JSON field to store selected languages

    def __str__(self):
        return f"Scribe request for {self.subject} on {self.exam_date}"
    
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    languages = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    exam_center = models.CharField(max_length=100)
    exam_date = models.DateField()

    def __str__(self):
        return f"Request for {self.exam_name} by {self.user.username}"



    
class Scribe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scribe_requests')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # To store the hashed password
    dob = models.DateField()
    qualification = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    languages = models.CharField(max_length=255)  # Comma-separated values

    def set_password(self, raw_password):
        """Hashes the password and saves it."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks if the raw password matches the hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    is_scribe = models.BooleanField(default=False)  # Indicates if the user is a scribe

    def __str__(self):
        return self.user.username