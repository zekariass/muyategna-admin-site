from django.contrib import admin
from .models import *


@admin.register(AddOnPlan)
class AddOnPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'country',
        'price_amount',
        'credits_included',
        'sort_order',
        'expires_at',
        'is_default',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'country',
        'is_active',
        'is_default',
    )

    search_fields = (
        'name',
        'country__name',
    )

    ordering = ('sort_order', 'name')

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            'fields': (
                'country',
                'name',
                'price_amount',
                'credits_included',
                'sort_order',
                'expires_at',
                'is_default',
                'is_active',
                'extra_data',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


@admin.register(DiscountPlan)
class DiscountPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'is_active', 'starts_at', 'expires_at')
    list_filter = ('country', 'is_active')
    search_fields = ('name',)


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
    list_display = ('id', 'name', 'country', 'code')
    search_fields = ('name', 'code')
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
        'balance',
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


# @admin.register(ServiceProviderCredit)
# class ServiceProviderCreditAdmin(admin.ModelAdmin):
#     list_display = ('provider', 'balance', 'auto_add_on_enabled', 'last_used_at', 'created_at', 'updated_at')
#     list_filter = ('auto_add_on_enabled',)
#     search_fields = ('provider__business_name',)
#     readonly_fields = ('created_at', 'updated_at', 'last_used_at')
#     ordering = ('-created_at',)


@admin.register(ServiceCreditCost)
class ServiceCreditCostAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'payg_claim_cost_per_lead',
        'payg_acceptance_cost_per_lead',
        'subs_claim_cost_per_lead',
        'subs_acceptance_cost_per_lead',
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



@admin.register(CreditUsage)
class CreditUsageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'provider',
        'used_amount',
        'credit_source',
        'used_at',
        'is_partial',
    )
    list_filter = ('credit_source', 'used_at', 'is_partial')
    search_fields = ('provider__business_name',)
    readonly_fields = ('used_at',)
    ordering = ('-used_at',)


@admin.register(PayGoCredit)
class PayGoCreditAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'provider',
        'balance',
        'auto_add_on_enabled',
        'last_used_at',
        'created_at',
        'updated_at',
    )
    list_filter = ('auto_add_on_enabled',)
    search_fields = ('provider__business_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceProviderWallet)
class ServiceProviderWalletAdmin(admin.ModelAdmin):
    list_display = (
        'provider_name',
        'total_credit',
        'available_credit',
        'total_hold_credit',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'subscription',
        'paygo_credit',
    )
    search_fields = (
        'provider__business_name',
        'provider__id',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def provider_name(self, obj):
        return obj.provider.business_name
    provider_name.short_description = 'Provider'



@admin.register(HoldCredit)
class HoldCreditAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'provider_wallet',
        'hold_amount',
        'credit_source',
        'status',
        'hold_at',
        'released_at',
        'converted_at',
        'expired_at',
    )
    list_filter = ('credit_source', 'status', 'hold_at')
    search_fields = ('provider_wallet__provider__business_name',)
    readonly_fields = ('hold_at',)
    ordering = ('-hold_at',)




from django.contrib import admin
from .models import PlatformBankInformation, BankTransferTransaction


@admin.register(PlatformBankInformation)
class PlatformBankInformationAdmin(admin.ModelAdmin):
    list_display = (
        "bank_name",
        "account_holder_name",
        "bank_account_number",
        "currency",
        "country",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "currency", "country")
    search_fields = (
        "bank_name",
        "account_holder_name",
        "bank_account_number",
        "swift_code",
        "iban",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": (
                "bank_name",
                "bank_account_number",
                "account_holder_name",
                "currency",
                "country",
                "is_active",
            )
        }),
        ("Optional Details", {
            "fields": (
                "bank_sort_code",
                "swift_code",
                "iban",
                "branch_name",
            ),
            "classes": ("collapse",),  # collapsible in admin UI
        }),
        ("Meta", {
            "fields": ("extra_data", "created_at", "updated_at"),
        }),
    )


@admin.register(BankTransferTransaction)
class BankTransferTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction",
        "payee_bank_account",
        "payer_full_name",
        "amount",
        "currency",
        "status",
        "bank_reference_number",
        "created_at",
        "verified_at",
    )
    list_filter = ("status", "currency", "created_at", "verified_at")
    search_fields = (
        "payer_full_name",
        "payer_bank_name",
        "payer_bank_account_number",
        "bank_reference_number",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "verified_at")
    fieldsets = (
        (None, {
            "fields": (
                "transaction",
                "payee_bank_account",
                "payer_full_name",
                "payer_bank_name",
                "payer_bank_branch_name",
                "payer_bank_account_number",
                "amount",
                "currency",
                "status",
                "bank_reference_number",
                "proof_of_payment_url",
            )
        }),
        ("Extra Data", {
            "fields": ("extra_data",),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "verified_at"),
        }),
    )
