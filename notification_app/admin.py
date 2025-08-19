from django.contrib import admin
from .models import (
    NotificationCategory,
    NotificationTemplate,
    NotificationTemplateTranslation,
    NotificationCategoryTranslation,
    NotificationChannel,
    NotificationChannelTranslation,
    ServiceProviderNotificationPreference,
    UserNotificationPreference,
    Notification,
)

# --- Inlines for Translations ---

class NotificationTemplateTranslationInline(admin.TabularInline):
    model = NotificationTemplateTranslation
    extra = 0


class NotificationCategoryTranslationInline(admin.TabularInline):
    model = NotificationCategoryTranslation
    extra = 0


class NotificationChannelTranslationInline(admin.TabularInline):
    model = NotificationChannelTranslation
    extra = 0

# --- Admins ---

@admin.register(NotificationCategory)
class NotificationCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recipient_type', 'user_can_opt_out')
    search_fields = ('name', 'recipient_type')
    inlines = [NotificationCategoryTranslationInline]


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notification_channel_id', 'notification_category', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'notification_category')
    inlines = [NotificationTemplateTranslationInline]


@admin.register(NotificationTemplateTranslation)
class NotificationTemplateTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'language', 'subject_template')
    search_fields = ('subject_template', 'body_template')
    list_filter = ('language',)


@admin.register(NotificationCategoryTranslation)
class NotificationCategoryTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_category', 'display_name', 'language')
    search_fields = ('display_name',)
    list_filter = ('language',)


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    inlines = [NotificationChannelTranslationInline]


@admin.register(NotificationChannelTranslation)
class NotificationChannelTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_channel_id', 'display_name', 'language')
    search_fields = ('display_name',)
    list_filter = ('language',)


@admin.register(ServiceProviderNotificationPreference)
class ServiceProviderNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider_id', 'notification_channel', 'notification_category', 'is_enabled')
    list_filter = ('notification_channel', 'notification_category', 'is_enabled')


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile_id', 'notification_channel', 'notification_category', 'is_enabled')
    list_filter = ('notification_channel', 'notification_category', 'is_enabled')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipient_entity_type',
        'recipient_entity_id',
        'notification_channel',
        'notification_category',
        'status',
        'sent_at',
        'created_at',
    )
    list_filter = (
        'recipient_entity_type',
        'notification_channel',
        'notification_category',
        'status',
        'created_at',
        'sent_at',
    )
    search_fields = (
        'id',
        'recipient_entity_id',
        'subject',
        'body',
        'error_message',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'sent_at',
        'error_message',
    )