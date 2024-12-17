from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            # Attempt to get the user by email
            user = User.objects.get(email=email)
            # Check if the password matches
            if user.check_password(password):
                return user  # Return the authenticated user
            return None
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
