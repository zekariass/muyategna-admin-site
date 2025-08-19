from django.contrib.gis.db import models
from common_app.models import Language


class ChannelNameEnum(models.TextChoices):
    EMAIL = 'EMAIL', 'Email'
    SMS = 'SMS', 'SMS'
    PUSH = 'PUSH', 'Push'
    WHATSAPP = 'WHATSAPP', 'WhatsApp'
    TELEGRAM = 'TELEGRAM', 'Telegram'


class NotificationRecipientTypeEnum(models.TextChoices):
    SERVICE_PROVIDER = 'SERVICE_PROVIDER', 'Service Provider'
    CUSTOMER = 'CUSTOMER', 'Customer'
    EMPLOYEE = 'EMPLOYEE', 'Employee'
    OWNER = 'OWNER', 'Owner'
    MANAGER = 'MANAGER', 'Manager'
    ALL = 'ALL', 'All'


class NotificationStatusEnum(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SENT = 'SENT', 'Sent'
    FAILED = 'FAILED', 'Failed'
    QUEUED = 'QUEUED', 'Queued'

class NotificationCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    recipient_type = models.TextField(choices=NotificationRecipientTypeEnum.choices)
    user_can_opt_out = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'notification_category'
    
    def __str__(self):
        return f"Category: {self.name} (Recipient: {self.recipient_type})"


class NotificationCategoryTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    notification_category = models.ForeignKey(NotificationCategory, models.DO_NOTHING)
    display_name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'notification_category_translation'
        unique_together = (('notification_category', 'language'),)

    def __str__(self):
        return f"Category Translation: {self.display_name} [{self.language.code}]"


class NotificationChannel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(choices=ChannelNameEnum, unique=True)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'notification_channel'
    
    def __str__(self):
        return f"Channel: {self.name}"
    


class NotificationChannelTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    notification_channel = models.ForeignKey(NotificationChannel, models.DO_NOTHING)
    display_name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'notification_channel_translation'
        unique_together = (('notification_channel_id', 'language'),)
    
    def __str__(self):
        return f"Channel Translation: {self.display_name} [{self.language.code}]"




class NotificationTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    notification_channel = models.ForeignKey(NotificationChannel, models.DO_NOTHING, db_column='notification_channel_id')
    notification_category = models.ForeignKey(NotificationCategory, models.DO_NOTHING)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'notification_template'
        unique_together = (('name', 'notification_channel_id', 'notification_category'),)

    def __str__(self):
        return f"Template: {self.name} | Category: {self.notification_category.name} | Channel ID: {self.notification_channel_id}"



class NotificationTemplateTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    subject_template = models.CharField(max_length=255, blank=True, null=True)
    body_template = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'notification_template_translation'
        unique_together = (('template', 'language'),)

    def __str__(self):
        return f"Translation: {self.template.name} [{self.language.locale}]"



class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipient_entity_type = models.CharField(max_length=30, choices=NotificationRecipientTypeEnum.choices)
    recipient_entity_id = models.BigIntegerField()
    notification_template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, db_column='notification_template_id')
    notification_channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE, db_column='notification_channel_id')
    notification_category = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE, db_column='notification_category_id')
    status = models.CharField(max_length=20, choices=NotificationStatusEnum.choices, default=NotificationStatusEnum.PENDING)
    payload = models.JSONField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'notification'
        managed = False

    def __str__(self):
        return f"Notification #{self.id} to {self.recipient_entity_type} ({self.recipient_entity_id})"


class ServiceProviderNotificationPreference(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_provider_id = models.BigIntegerField()
    notification_channel = models.ForeignKey(NotificationChannel, models.DO_NOTHING)
    notification_category = models.ForeignKey(NotificationCategory, models.DO_NOTHING)
    is_enabled = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_provider_notification_preference'
        unique_together = (('service_provider_id', 'notification_channel', 'notification_category'),)
    
    def __str__(self):
        return f"ServiceProvider {self.service_provider_id} | {self.notification_category.name} via {self.notification_channel.name}"



class UserNotificationPreference(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_profile_id = models.BigIntegerField()
    notification_channel = models.ForeignKey(NotificationChannel, models.DO_NOTHING)
    notification_category = models.ForeignKey(NotificationCategory, models.DO_NOTHING)
    is_enabled = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'user_notification_preference'
        unique_together = (('user_profile_id', 'notification_channel', 'notification_category'),)

    def __str__(self):
        return f"User {self.user_profile_id} | {self.notification_category.name} via {self.notification_channel.name}"

