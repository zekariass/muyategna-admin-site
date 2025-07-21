from django.contrib import admin
from .models import *


@admin.register(AddOnPlan)
class AddOnPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'service', 'country', 'price_amount', 'is_active', 'is_default', 'plan_order')
    search_fields = ('name', 'service__name', 'country__name')
    list_filter = ('is_active', 'is_default', 'country', 'service')


@admin.register(DiscountPlan)
class DiscountPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'starts_at', 'expires_at', 'is_active', 'coupon_required')
    search_fields = ('name', 'description', 'country__name')
    list_filter = ('is_active', 'coupon_required', 'country')


@admin.register(AddOnPlanDiscountEligibility)
class AddonPlanDiscountEligibilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'add_on_plan', 'discount_plan', 'is_active')
    search_fields = ('add_on_plan__name', 'discount_plan__name')
    list_filter = ('is_active',)


@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payer_entity_type', 'payer_entity_id', 'amount_before_tax', 'currency', 'product_type', 'status', 'payment_due_at')
    search_fields = ('payer_entity_id',)
    list_filter = ('payer_entity_type', 'product_type', 'status', 'currency')


@admin.register(AddOnPlanTranslation)
class AddOnPlanTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'add_on_plan', 'language', 'display_name')
    search_fields = ('display_name',)
    list_filter = ('language',)


@admin.register(ServiceProviderAddOn)
class ServiceProviderAddOnAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'add_on_plan', 'initial_leads', 'used_leads', 'purchased_at', 'is_active')
    search_fields = ('provider__name',)
    list_filter = ('is_active',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'status', 'discount_plan', 'starts_at', 'expires_at', 'is_global')
    search_fields = ('code',)
    list_filter = ('status', 'is_global')


@admin.register(DiscountPlanTranslation)
class DiscountPlanTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'discount_plan', 'language', 'display_name')
    search_fields = ('display_name',)
    list_filter = ('language',)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)


@admin.register(PaymentMethodTranslation)
class PaymentMethodTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_method', 'language', 'display_name')
    search_fields = ('display_name',)
    list_filter = ('language',)


@admin.register(ServiceProviderCouponTracker)
class ServiceProviderCouponTrackerAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'coupon', 'usage_limit', 'use_count', 'is_active')
    search_fields = ('provider__name', 'coupon__code')
    list_filter = ('is_active',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'txn_reference', 'payment_method', 'amount_paid', 'status', 'currency', 'created_at')
    search_fields = ('txn_reference',)
    list_filter = ('status', 'currency')


@admin.register(ServiceProviderDiscountUsageTracker)
class ServiceProviderDiscountUsageTrackerAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'discount', 'use_count', 'usage_limit', 'is_active')
    search_fields = ('provider__name', 'discount__name')
    list_filter = ('is_active',)


@admin.register(ServiceProviderInvoice)
class ServiceProviderInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'status', 'currency', 'total_amount', 'issued_at')
    search_fields = ('provider__name',)
    list_filter = ('status', 'currency', 'is_locked')


@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'region', 'tax_type', 'is_active')
    search_fields = ('name', 'tax_type')
    list_filter = ('country', 'region', 'is_active')


@admin.register(ServiceProviderInvoiceItem)
class ServiceProviderInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_invoice', 'product_type', 'unit_price', 'quantity', 'total_amount')
    search_fields = ('parent_invoice__id',)
    list_filter = ('product_type',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'country',
        'price_amount',
        'credits_included',
        'billing_cycle',
        'billing_cycle_count',
        'trial_period_days',
        'is_active',
        'is_default',
        'upgradeable',
        'downgradeable',
        'sort_order',
    )
    list_filter = (
        'is_active',
        'is_default',
        'upgradeable',
        'downgradeable',
        'country',
        'billing_cycle',
    )
    search_fields = (
        'name',
        'country__name',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    ordering = ('country', 'sort_order')

    def get_queryset(self, request):
        # Optimize foreign key fetching
        qs = super().get_queryset(request)
        return qs.select_related('country')



@admin.register(ServiceProviderSubscription)
class ServiceProviderSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'provider',
        'subscription_plan',
        'is_active',
        'initial_credits',
        'used_credits',
        'auto_renew',
        'renewal_status',
        'started_at',
        'end_date',
        'next_billing_date',
        'cancelled_at',
    )
    list_filter = (
        'is_active',
        'auto_renew',
        'subscription_plan',
        'renewal_status',
    )
    search_fields = (
        'provider__business_name',
        'subscription_plan__name',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'last_billing_date',
        'renewal_attempted_at',
        # 'trial_period_started_at',
        # 'trial_period_ends_at',
        'grace_period_started_at',
        'grace_period_ends_at',
    )
    date_hierarchy = 'started_at'

    def get_queryset(self, request):
        # Ensure related fields are fetched efficiently
        qs = super().get_queryset(request)
        return qs.select_related('provider', 'subscription_plan')


@admin.register(SubscriptionPlanDiscountEligibility)
class SubscriptionPlanDiscountEligibilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription_plan', 'discount_plan', 'is_active')
    search_fields = ('subscription_plan__name', 'discount_plan__name')
    list_filter = ('is_active',)


@admin.register(SubscriptionPlanTranslation)
class SubscriptionPlanTranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription_plan', 'language', 'display_name')
    search_fields = ('display_name',)
    list_filter = ('language',)


@admin.register(ServiceCreditPlan)
class ServiceCreditPlanAdmin(admin.ModelAdmin):
    list_display = ('service', 'credits_per_lead', 'created_at', 'updated_at')
    search_fields = ('service__name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceProviderCredit)
class ServiceProviderCreditAdmin(admin.ModelAdmin):
    list_display = ('provider', 'balance', 'auto_add_on_enabled', 'last_used_at', 'created_at', 'updated_at')
    list_filter = ('auto_add_on_enabled',)
    search_fields = ('provider__business_name',)
    readonly_fields = ('created_at', 'updated_at', 'last_used_at')
    ordering = ('-created_at',)


@admin.register(ServiceCreditCost)
class ServiceCreditCostAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'payg_credits_per_lead',
        'subs_credits_per_lead',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'service__name',  # Assuming Service has a name field
    )
    list_filter = (
        'created_at',
        'updated_at',
    )
    ordering = ('-created_at',)