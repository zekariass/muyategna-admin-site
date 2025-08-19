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
    list_display = (
        'id', 'business_name', 'business_description', 'service_provider_type', 'country',
        'business_address', 'num_employees', 'max_travel_distance_in_km', 'portfolio_url',
        'portfolio_type', 'business_logo_url', 'verification_status', 'average_rating',
        'number_of_reviews', 'years_of_experience', 'is_verified', 'is_active', 'is_blocked',
        'business_email', 'business_phone', 'website', 'default_language'
    )

    list_filter = (
        'service_provider_type', 'portfolio_type', 'verification_status', 'is_verified',
        'is_active', 'is_blocked', 'is_deleted', 'country'
    )
    search_fields = ('business_name', 'business_email', 'business_phone')
    readonly_fields = ('registered_at', 'updated_at')


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
    list_display = ("id", "provider", "service", "delivery_mode", "is_active", "linked_at")
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



@admin.register(ServiceProviderRankingWeights)
class ServiceProviderRankingWeightsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'distance_weight',
        'total_claims_weight',
        'avg_claim_time_in_mins_weight',
        'avg_rating_weight',
        'completed_leads_weight',
        'total_quotes_weight',
        'accepted_quotes_weight',
        'daily_claim_count_weight',
        'weekly_claim_count_weight',
        'two_weekly_claim_count_weight',
        'monthly_claim_count_weight',
        'is_active',
        'created_at',
        'updated_at',
    ]
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['id']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServiceProviderStatistics)
class ServiceProviderStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'provider',
        'total_claims',
        'avg_claim_time_in_mins',
        'avg_rating',
        'completed_leads',
        'total_quotes',
        'accepted_quotes',
        'daily_claim_count',
        'weekly_claim_count',
        'two_weekly_claim_count',
        'monthly_claim_count',
        'total_new_job_notifs', 
        'daily_new_job_notifs', 
        'weekly_new_job_notifs',
        'created_at',
        'updated_at',
    )
    search_fields = ('provider__business_name',)
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
