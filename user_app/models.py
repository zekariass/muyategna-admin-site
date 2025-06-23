from django.db import models
from common_app.models import Language


class UserProfile(models.Model):
    user_profile_id = models.BigAutoField(primary_key=True)
    keycloak_user_id = models.UUIDField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    address_id = models.BigIntegerField(blank=True, null=True)
    profile_picture_url = models.TextField(blank=True, null=True)
    default_language = models.ForeignKey(Language, models.DO_NOTHING)
    last_login = models.DateTimeField(blank=True, null=True)
    referral_code = models.CharField(max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    joined_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'

    def __str__(self):
        if self.address_id:
            return f"{self.email} ({self.address_id})"
        return self.email