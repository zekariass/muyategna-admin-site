from django.db import models
from service_app.models import Service, ServiceCategory, ServiceCountryAvailability
from location_app.models import Country, Region
from common_app.models import Language
from user_app.models import UserProfile
from service_provider_app.models import ServiceProvider, ServiceProviderTaxInfo


class CalculationMethod(models.TextChoices):
    PERCENTAGE = 'PERCENTAGE', 'Percentage'
    FIXED = 'FIXED', 'Fixed'
    PERCENTAGE_PLUS_FIXED = 'PERCENTAGE_PLUS_FIXED', 'Percentage + Fixed'


class PayerEntityType(models.TextChoices):
    SERVICE_PROVIDER = 'SERVICE_PROVIDER', 'Service Provider'
    CUSTOMER = 'CUSTOMER', 'Customer'


class ProductType(models.TextChoices):
    SUBSCRIPTION = 'SUBSCRIPTION', 'Subscription'
    ADD_ON = 'ADD_ON', 'Add-on'


class PaymentIntentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    SUCCEEDED = 'SUCCEEDED', 'Succeeded'
    FAILED = 'FAILED', 'Failed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    EXPIRED = 'EXPIRED', 'Expired'


class TransactionStatus(models.TextChoices):
    INITIATED = 'INITIATED', 'Initiated'
    PROCESSING = 'PROCESSING', 'Processing'
    SUCCEEDED = 'SUCCEEDED', 'Succeeded'
    FAILED = 'FAILED', 'Failed'
    TIMEOUT = 'TIMEOUT', 'Timeout'
    DISPUTED = 'DISPUTED', 'Disputed'
    REFUNDED = 'REFUNDED', 'Refunded'


class InvoiceStatus(models.TextChoices):
    ISSUED = 'ISSUED', 'Issued'
    PAID = 'PAID', 'Paid'
    CANCELLED = 'CANCELLED', 'Cancelled'


class BillingCycle(models.TextChoices):
    DAY = 'DAY', 'Day'
    WEEK = 'WEEK', 'Week'
    MONTH = 'MONTH', 'Month'
    YEAR = 'YEAR', 'Year'


class CouponStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    REDEEMED = 'REDEEMED', 'Redeemed'
    EXPIRED = 'EXPIRED', 'Expired'


class DiscountUserType(models.TextChoices):
    NEW_USER = 'NEW_USER', 'New User'
    EXISTING_USER = 'EXISTING_USER', 'Existing User'
    ANY_USER = 'ANY_USER', 'Any User'


class AddOnPlan(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    price_amount = models.DecimalField(max_digits=15, decimal_places=4)
    leads_included = models.IntegerField()
    plan_order = models.IntegerField()
    expire_on = models.DateTimeField(blank=True, null=True)
    is_default = models.BooleanField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"

    class Meta:
        managed = False
        db_table = 'add_on_plan'
        unique_together = (('service', 'plan_order'),)


class DiscountPlan(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_calculation_method = models.TextField(choices=CalculationMethod, default=CalculationMethod.PERCENTAGE)  # This field type is a guess.
    fixed_value = models.DecimalField(max_digits=15, decimal_places=4)
    percentage_value = models.DecimalField(max_digits=15, decimal_places=4)
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    usage_limit = models.IntegerField()
    per_user_limit = models.IntegerField()
    total_use_count = models.IntegerField()
    max_discount_value = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    coupon_required = models.BooleanField()
    applies_to = models.TextField(choices=DiscountUserType, default=DiscountUserType.ANY_USER)  # This field type is a guess.

    def __str__(self):
        return f"{self.name} ({self.country})"

    class Meta:
        managed = False
        db_table = 'discount_plan'


class PaymentIntent(models.Model):
    id = models.BigAutoField(primary_key=True)
    payer_entity_type = models.TextField(choices=PayerEntityType)  # This field type is a guess.
    payer_entity_id = models.BigIntegerField()
    amount_before_tax = models.DecimalField(max_digits=15, decimal_places=4)
    currency = models.CharField(max_length=10)
    product_type = models.TextField(choices=ProductType)  # This field type is a guess.
    status = models.TextField(choices=PaymentIntentStatus)  # This field type is a guess.
    payment_due_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.product_type} - {self.status} - {self.currency} {self.amount_before_tax}"

    class Meta:
        managed = False
        db_table = 'payment_intent'


class AddOnPlanDiscountEligibility(models.Model):
    id = models.BigAutoField(primary_key=True)
    add_on_plan = models.ForeignKey(AddOnPlan, models.DO_NOTHING)
    discount_plan = models.ForeignKey(DiscountPlan, models.DO_NOTHING)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Eligibility: {self.add_on_plan.name} ↔ {self.discount_plan.name}"

    class Meta:
        managed = False
        db_table = 'add_on_plan_discount_eligibility'
        unique_together = (('add_on_plan', 'discount_plan'), ('add_on_plan', 'is_active'),)




class AddOnPlanTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    add_on_plan = models.ForeignKey(AddOnPlan, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.display_name} ({self.language})"

    class Meta:
        managed = False
        db_table = 'add_on_plan_translation'


class ServiceProviderAddOn(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    payment_intent = models.ForeignKey(PaymentIntent, models.DO_NOTHING)
    add_on_plan = models.ForeignKey(AddOnPlan, models.DO_NOTHING)
    initial_leads = models.IntegerField()
    used_leads = models.IntegerField()
    purchased_at = models.DateTimeField()
    upgraded_from = models.ForeignKey('self', models.DO_NOTHING, db_column='upgraded_from', blank=True, null=True)
    is_active = models.BooleanField()
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.provider} - {self.add_on_plan} ({self.purchased_at.date()})"

    class Meta:
        managed = False
        db_table = 'service_provider_add_on'


class Coupon(models.Model):
    id = models.BigAutoField(primary_key=True)
    discount_plan = models.ForeignKey(DiscountPlan, models.DO_NOTHING)
    code = models.CharField(unique=True, max_length=100)
    usage_limit = models.IntegerField()
    per_user_limit = models.IntegerField()
    total_use_count = models.IntegerField()
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    status = models.TextField(choices=CouponStatus)  # This field type is a guess.
    created_by = models.ForeignKey(UserProfile, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_global = models.BooleanField(unique=True)

    def __str__(self):
        return f"{self.code} ({self.status})"

    class Meta:
        managed = False
        db_table = 'coupon'


class DiscountPlanTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    discount_plan = models.ForeignKey(DiscountPlan, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.display_name} ({self.language})"

    class Meta:
        managed = False
        db_table = 'discount_plan_translation'
        unique_together = (('discount_plan', 'language'),)



class PaymentMethod(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'payment_method'


class PaymentMethodTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    payment_method = models.ForeignKey(PaymentMethod, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.display_name} ({self.language})"

    class Meta:
        managed = False
        db_table = 'payment_method_translation'
        unique_together = (('payment_method', 'language'),)


class ServiceProviderCouponTracker(models.Model):
    id = models.BigAutoField(primary_key=True)
    coupon = models.ForeignKey(Coupon, models.DO_NOTHING)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    usage_limit = models.IntegerField()
    use_count = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.provider} - {self.coupon} ({self.use_count}/{self.usage_limit})"

    class Meta:
        managed = False
        db_table = 'service_provider_coupon_tracker'


# =====================================================================

class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    payment_intent = models.ForeignKey(PaymentIntent, models.DO_NOTHING, blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, models.DO_NOTHING, blank=True, null=True)
    sub_total_amount = models.DecimalField(max_digits=15, decimal_places=4)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=4)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=4)
    txn_reference = models.CharField(unique=True, max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    status = models.TextField(choices=TransactionStatus, blank=False, null=False)  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.txn_reference or self.id} - {self.status}"


    class Meta:
        managed = False
        db_table = 'transaction'


class ServiceProviderDiscountUsageTracker(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    discount = models.ForeignKey(DiscountPlan, models.DO_NOTHING)
    usage_limit = models.IntegerField()
    use_count = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    first_used_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.provider} - {self.discount} ({self.use_count}/{self.usage_limit})"

    class Meta:
        managed = False
        db_table = 'service_provider_discount_usage_tracker'


class ServiceProviderInvoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    provider_tax_info = models.ForeignKey(ServiceProviderTaxInfo, models.DO_NOTHING, blank=True, null=True)
    transaction = models.ForeignKey(Transaction, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sub_total_amount = models.DecimalField(max_digits=15, decimal_places=4)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=4)
    total_amount = models.DecimalField(max_digits=15, decimal_places=4)
    currency = models.CharField(max_length=10)
    status = models.TextField(choices=InvoiceStatus)  # This field type is a guess.
    is_locked = models.BooleanField()
    issued_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Invoice #{self.id} - {self.provider} - {self.status}"

    class Meta:
        managed = False
        db_table = 'service_provider_invoice'



class TaxRule(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True)
    tax_type = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tax_calculation_method = models.TextField(choices=CalculationMethod)  # This field type is a guess.
    percentage_value = models.DecimalField(max_digits=12, decimal_places=4)
    fixed_value = models.DecimalField(max_digits=12, decimal_places=4)
    is_active = models.BooleanField()
    effective_start_date = models.DateTimeField()
    effective_end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.tax_type})"

    class Meta:
        managed = False
        db_table = 'tax_rule'


class ServiceProviderInvoiceItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_invoice = models.ForeignKey(ServiceProviderInvoice, models.DO_NOTHING)
    tax_rule = models.ForeignKey(TaxRule, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    product_type = models.TextField(choices=ProductType)  # This field type is a guess.
    unit_price = models.DecimalField(max_digits=15, decimal_places=4)
    quantity = models.IntegerField()
    sub_total_amount = models.DecimalField(max_digits=15, decimal_places=4)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=4)
    total_amount = models.DecimalField(max_digits=15, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Item #{self.id} - {self.product_type} - {self.total_amount}"

    class Meta:
        managed = False
        db_table = 'service_provider_invoice_item'


class BillingCycleEnum(models.TextChoices):
    DAY = 'DAY', 'Day'
    WEEK = 'WEEK', 'Week'
    MONTH = 'MONTH', 'Month'
    YEAR = 'YEAR', 'Year'


class SubscriptionPlan(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    price_amount = models.DecimalField(max_digits=15, decimal_places=4)
    billing_cycle = models.TextField(choices=BillingCycleEnum)
    billing_cycle_count = models.IntegerField()
    trial_period_days = models.IntegerField()
    sort_order = models.IntegerField()
    is_default = models.BooleanField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    upgradeable = models.BooleanField(blank=True, null=True)
    downgradeable = models.BooleanField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    credits_included = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'subscription_plan'
        unique_together = (('name', 'country'),)

    def __str__(self):
        return f"{self.name} ({self.country}) - {self.price_amount} {self.billing_cycle} ({self.billing_cycle_count})"


class RenewalStatusEnum(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUCCESSFUL = 'SUCCESSFUL', 'Successful'
    FAILED = 'FAILED', 'Failed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    EXPIRED = 'EXPIRED', 'Expired'


class ServiceProviderSubscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.OneToOneField(ServiceProvider, models.DO_NOTHING)
    subscription_plan = models.ForeignKey(SubscriptionPlan, models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    next_billing_date = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    renewal_attempted_at = models.DateTimeField(blank=True, null=True)
    upgraded_from = models.ForeignKey('self', models.DO_NOTHING, db_column='upgraded_from', blank=True, null=True)
    downgraded_from = models.ForeignKey('self', models.DO_NOTHING, db_column='downgraded_from', related_name='serviceprovidersubscription_downgraded_from_set', blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField()
    initial_credits = models.DecimalField(max_digits=10, decimal_places=2)
    used_credits = models.DecimalField(max_digits=10, decimal_places=2)
    auto_renew = models.BooleanField()
    started_at = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    last_billing_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    trial_period_started_at = models.DateTimeField(blank=True, null=True)
    trial_period_ends_at = models.DateTimeField(blank=True, null=True)
    grace_period_started_at = models.DateTimeField(blank=True, null=True)
    grace_period_ends_at = models.DateTimeField(blank=True, null=True)
    renewal_status = models.TextField(choices=RenewalStatusEnum)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'service_provider_subscription'

    def __str__(self):
        return f"{self.provider.business_name} - {self.subscription_plan.name if self.subscription_plan else 'No Plan'} ({'Active' if self.is_active else 'Inactive'})"


class SubscriptionPlanDiscountEligibility(models.Model):
    id = models.BigAutoField(primary_key=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, models.DO_NOTHING)
    discount_plan = models.ForeignKey(DiscountPlan, models.DO_NOTHING)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.subscription_plan} - {self.discount_plan}"

    class Meta:
        managed = False
        db_table = 'subscription_plan_discount_eligibility'
        unique_together = (('subscription_plan', 'discount_plan'), ('subscription_plan', 'is_active'),)


class SubscriptionPlanTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.display_name} ({self.language})"

    class Meta:
        managed = False
        db_table = 'subscription_plan_translation'
        unique_together = (('subscription_plan', 'language'),)



class ServiceCreditPlan(models.Model):
    service = models.OneToOneField(Service, models.DO_NOTHING)
    credits_per_lead = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_credit_plan'
    
    def __str__(self):
        return f"{self.service.name} - {self.credits_per_lead}"



class ServiceProviderCredit(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.OneToOneField(ServiceProvider, models.DO_NOTHING)
    balance = models.DecimalField(max_digits=15, decimal_places=4)
    auto_add_on_enabled = models.BooleanField()
    extra_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    last_used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_provider_credit'

    def __str__(self):
        return f"{self.provider.business_name} - Balance: {self.balance}"



class ServiceCreditCost(models.Model):
    service = models.OneToOneField(Service, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    payg_credits_per_lead = models.DecimalField(max_digits=10, decimal_places=2)
    subs_credits_per_lead = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'service_credit_cost'

    def __str__(self):
        return f"{self.service.name} - PAYG: {self.payg_credits_per_lead}, SUBS: {self.subs_credits_per_lead}"
    
