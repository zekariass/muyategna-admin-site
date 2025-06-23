from django.contrib import admin
from .models import *

@admin.register(ServiceEmployee)
class ServiceEmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user_profile", "provider", "is_active", "is_blocked", "created_at")
    search_fields = ("user_profile__username", "provider__business_name")
    list_filter = ("is_active", "is_blocked", "provider")


@admin.register(ServiceEmployeeRole)
class ServiceEmployeeRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "employee", "assigned_at")
    search_fields = ("employee__user_profile__username", "role__name")
    list_filter = ("role",)


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "business_name", "country", "verification_status", "is_verified", 'is_active', "is_blocked", "registered_at", "updated_at")
    search_fields = ("business_name", "business_description")
    list_filter = ("verification_status", "country")


@admin.register(ServiceProviderAgreement)
class ServiceProviderAgreementAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "is_signed", "created_at")
    search_fields = ("provider__business_name",)
    list_filter = ("is_signed",)


@admin.register(ServiceProviderRole)
class ServiceProviderRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)


@admin.register(ServiceProviderServices)
class ServiceProviderServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "service", "is_active", "linked_at")
    search_fields = ("provider__business_name", "service__name")
    list_filter = ("is_active", "linked_at")


@admin.register(ServiceProviderTaxInfo)
class ServiceProviderTaxInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "service_provider", "tax_payer_id_number", "is_vat_registered", "is_tax_exempt")
    search_fields = ("service_provider__business_name", "tax_payer_id_number")
    list_filter = ("is_vat_registered", "is_tax_exempt")


@admin.register(ServiceProviderVerification)
class ServiceProviderVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "type", "verification_status", "created_at")
    search_fields = ("provider__business_name", "type__name", "verification_status")
    list_filter = ("verification_status", "type")


@admin.register(ServiceProviderVerificationType)
class ServiceProviderVerificationTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "provider_type", "is_mandatory", "document_required")
    search_fields = ("name",)
    list_filter = ("is_mandatory", "document_required")