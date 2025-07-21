from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_profile_id',
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'phone_number',
        'default_language',
        'is_staff',
        'country',
        'joined_at',
        'last_login',
    )
    list_filter = ('is_staff', 'default_language', 'joined_at', 'last_login')
    search_fields = ('first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'referral_code')
    ordering = ('first_name', 'last_name')
    readonly_fields = ('joined_at', 'updated_at', 'last_login')
    list_editable = ('is_staff',)

    fieldsets = (
        (None, {
            'fields': ('keycloak_user_id', 'email', 'first_name', 'middle_name', 'last_name', 'phone_number', 'referral_code')
        }),
        ('Profile Info', {
            'fields': ('country', 'default_language', 'profile_picture_url')
        }),
        ('Access & Activity', {
            'fields': ('is_staff', 'joined_at', 'last_login', 'updated_at')
        }),
    )


