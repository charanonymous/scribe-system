from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from main.models import Request

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ExamDetailsForm(forms.Form):
    subject = forms.CharField(max_length=100, label="Subject")
    exam_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 2031)), label="Exam Date")
    exam_center = forms.CharField(max_length=200, label="Exam Center")
    languages = forms.MultipleChoiceField(
        choices=[('telugu', 'Telugu'), ('hindi', 'Hindi'), ('english', 'English')],
        widget=forms.CheckboxSelectMultiple,
        label="Medium"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding custom CSS classes for styling
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email Address')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken")
        if len(username) < 3 or len(username) > 150:
            raise ValidationError("Username must be between 3 and 150 characters")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("Passwords must match")
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password1):  # At least one uppercase letter
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password1):  # At least one lowercase letter
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password1):  # At least one number
            raise ValidationError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*()_+={}\[\]:;"<>,.?/-]', password1):  # Special characters
            raise ValidationError("Password must contain at least one special character")
        return password2
    
class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


