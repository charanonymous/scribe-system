import json
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse, HttpResponseForbidden , HttpResponseRedirect
from .forms import LoginForm , CustomUserCreationForm , CustomLoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Scribe , ScribeRequest , Request
import re
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from .forms import ExamDetailsForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from main.models import Scribe , Request
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Login view for "Register as a Scribe"
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import check_password  # Use this for hashed passwords
from .models import Scribe

def register_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get the scribe instance using the email
            scribe = Scribe.objects.get(email=email)

            # Check if the scribe has an associated User
            if scribe.user:
                # Authenticate the user
                user = scribe.user  # Get the associated User instance
                if user.check_password(password):
                    # If password is correct, log the user in
                    login(request, user)
                    messages.success(request, f"Welcome {scribe.name}!")

                    # Redirect after login
                    next_url = request.GET.get('next', 'scribe_requests')
                    return HttpResponseRedirect(next_url)  # Redirect to the next URL
                else:
                    messages.error(request, "Invalid email or password.")
            else:
                messages.error(request, "This scribe does not have an associated user.")
        except Scribe.DoesNotExist:
            messages.error(request, "No scribe found with this email.")

    return render(request, 'main/register_login.html')

# Other views
def book_login(request):
    if request.method == 'POST':
        # Get email and password from the form
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Print the POST data for debugging
        print(f"POST Data: email={email}, password={password}")

        # Try to authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')  # Redirect to the welcome page
        else:
            # If authentication fails, show error message
            messages.error(request, "Invalid login credentials.")

    return render(request, 'main/book_login.html')

def scribe_login(request):
    return render(request, 'main/scribe_login.html')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Registration successful! Please log in.")
            return redirect('book_login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, "There was an error with your registration. Please check the form.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Scribe

def scribe_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        qualification = request.POST.get('qualification')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        languages = request.POST.getlist('languages')  # List of selected languages

        # Password matching check
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('scribe_register')

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists!")
            return redirect('scribe_register')

        # Create User account
        user = User.objects.create_user(username=email, email=email, password=password)

        # Create the Scribe profile and link to the user
        scribe = Scribe(
            user=user,
            name=name,
            email=email,
            dob=dob,
            qualification=qualification,
            phone=phone,
            gender=gender,
            languages=languages  # Store as a list directly, or you can join as string if needed
        )
        scribe.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('register_login')  # Redirect to login page

    return render(request, 'main/scribe_register.html')

def home(request):
    return render(request, 'main/home.html')

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or dashboard after successful login
            else:
                return HttpResponse("Invalid credentials, please try again.")
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout



# Welcome page view after login
@login_required
def welcome(request):
    if request.method == 'POST':
        # Get the form data
        languages = request.POST.get('languages')
        details = request.POST.get('details')

        # Log the data to check if it's being received correctly
        print(f"Languages: {languages}, Details: {details}")

        # Create and save the request
        request_data = Request(
            user=request.user,  # Link the request to the logged-in user
            languages=languages,
            details=details
        )
        request_data.save()

        # Log that the request was saved
        print(f"Request saved for user {request.user.username}")

        # Return a JSON response to show success message
        return JsonResponse({'message': 'Scribe requested successfully!'})

    return render(request, 'main/welcome.html')

from django.http import JsonResponse
from .models import ScribeRequest  # Assuming you have a model for saving requests

@login_required
@login_required
def request_scribe(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        languages = request.POST.get('languages')
        exam_name = request.POST.get('exam_name')
        course = request.POST.get('course')
        subject = request.POST.get('subject')
        exam_center = request.POST.get('exam_center')
        exam_date = request.POST.get('exam_date')

        try:
            # Save the request in the database
            Request.objects.create(
                user=request.user,
                full_name=full_name,
                languages=languages,
                exam_name=exam_name,
                course=course,
                subject=subject,
                exam_center=exam_center,
                exam_date=exam_date
            )
            # Pass a success message to the template
            return render(request, 'welcome.html', {'success': True})
        except Exception as e:
            # Pass an error message to the template
            return render(request, 'welcome.html', {'error': True, 'message': str(e)})

    return render(request, 'main/welcome.html')

    
@login_required
def scribe_profile(request):
    try:
        # Fetch the Scribe profile associated with the logged-in user
        scribe = request.user.scribe_profile  # Using the related_name 'scribe_profile'
        return render(request, 'main/scribe_profile.html', {'scribe': scribe})
    except Scribe.DoesNotExist:
        # If no Scribe profile exists for the user, show an error message
        return render(request, 'main/scribe_profile.html', {'error': 'No scribe profile found. Please ensure you are logged in as a scribe.'})

@login_required
def scribe_requests(request):
    # Check if the logged-in user is a scribe
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_scribe:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('welcome')  # Redirect if not a scribe

    # Retrieve all scribe requests
    scribe_requests = Request.objects.all()
    return render(request, 'main/scribe_requests.html', {'scribe_requests': scribe_requests})