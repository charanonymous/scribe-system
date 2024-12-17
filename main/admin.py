from django.contrib import admin
from .models import Scribe , UserProfile
# Ensure the correct app name is used when registering models

@admin.register(Scribe)  # Use the decorator or admin.site.register
class ScribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'qualification', 'dob')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_scribe')
    list_filter = ('is_scribe',)
