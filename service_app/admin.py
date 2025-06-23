from django.contrib import admin
from .models import *


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")

@admin.register(ServiceCategoryTranslation)
class ServiceCategoryTranslationAdmin(admin.ModelAdmin):
    list_display = ("id", "language", "name", "description", "created_at", "updated_at")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "service_category", "name", "description", "created_at", "updated_at")

@admin.register(ServiceTranslation)
class ServiceTranslationAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "language", "name", "description", "created_at", "updated_at")


@admin.register(ServiceCountryAvailability)
class ServiceCountryAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "country", "is_active", "price_model", "base_price", "notes", "created_at", "updated_at")


