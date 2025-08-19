from django.db import models
from service_app.models import Service
from location_app.models import Address, Country
from user_app.models import UserProfile
from common_app.models import LegalDocument, Language
from django.core.validators import MinValueValidator, MaxValueValidator

class ServiceProviderType(models.TextChoices):
    FREELANCER = 'FREELANCER', 'Freelancer'
    SOLE_TRADER = 'SOLE_TRADER', 'Sole Trader'
    LIMITED_COMPANY = 'LIMITED_COMPANY', 'Limited Company'


class PortfolioType(models.TextChoices):
    WEBSITE = 'WEBSITE', 'Website'
    IMAGE = 'IMAGE', 'Image'
    VIDEO = 'VIDEO', 'Video'
    DOCUMENT = 'DOCUMENT', 'Document'
    OTHER = 'OTHER', 'Other'


class VerificationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_REVIEW = 'IN_REVIEW', 'In Review'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class ServiceProvider(models.Model):
    business_name = models.CharField(max_length=255)
    business_description = models.TextField(blank=True, null=True)
    service_provider_type = models.CharField(max_length=20, choices=ServiceProviderType.choices, default=ServiceProviderType.SOLE_TRADER)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    business_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    num_employees = models.IntegerField(null=True, blank=True)
    max_travel_distance_in_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    portfolio_url = models.TextField(blank=True, null=True)
    portfolio_type = models.CharField(max_length=20, choices=PortfolioType.choices, default=PortfolioType.WEBSITE)
    business_logo_url = models.TextField(blank=True, null=True)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    number_of_reviews = models.IntegerField(default=0)
    years_of_experience = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    business_email = models.CharField(max_length=100, unique=True)
    business_phone = models.CharField(max_length=50, unique=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=50, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    default_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_reason = models.CharField(max_length=255, blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

    class Meta:
        managed = False
        db_table = 'service_provider'


class ServiceEmployee(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, models.DO_NOTHING)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_blocked = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.user_profile} - {self.provider}"

    class Meta:
        managed = False
        db_table = 'service_employee'



class ServiceProviderAgreement(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(LegalDocument, models.DO_NOTHING)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    is_signed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Agreement for {self.provider} - Signed: {self.is_signed}"

    class Meta:
        managed = False
        db_table = 'service_provider_agreement'


class ServiceProviderRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'service_provider_role'



class ServiceEmployeeRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(ServiceProviderRole, models.DO_NOTHING)
    employee = models.ForeignKey(ServiceEmployee, models.DO_NOTHING)
    assigned_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.employee} - {self.role.name}"

    class Meta:
        managed = False
        db_table = 'service_employee_role'


class DeliveryMode(models.TextChoices):
    ONSITE = 'ONSITE', 'Onsite'
    REMOTE = 'REMOTE', 'Remote'
    BOTH = 'BOTH', 'Both'


class ServiceProviderServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    delivery_mode = models.CharField(max_length=20, choices=DeliveryMode, default=DeliveryMode.ONSITE)
    linked_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.provider} - {self.service}"

    class Meta:
        managed = False
        db_table = 'service_provider_services'
        unique_together = (('service', 'provider'),)


class ServiceProviderTaxInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    tax_payer_id_number = models.CharField(max_length=50, blank=True, null=True)
    is_vat_registered = models.BooleanField()
    is_tax_exempt = models.BooleanField()
    tax_exempt_certificate_number = models.CharField(max_length=50, blank=True, null=True)
    tax_exemption_reason = models.TextField(blank=True, null=True)
    income_tax_classification = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.service_provider} - Tax ID: {self.tax_payer_id_number or 'N/A'}"

    class Meta:
        managed = False
        db_table = 'service_provider_tax_info'



class ServiceProviderVerificationType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    provider_type = models.TextField(choices=ServiceProviderType, default=ServiceProviderType.SOLE_TRADER)
    is_mandatory = models.BooleanField()
    document_required = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'service_provider_verification_type'



class ServiceProviderVerification(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    type = models.ForeignKey(ServiceProviderVerificationType, models.DO_NOTHING)
    verification_status = models.TextField(choices=VerificationStatus, default=VerificationStatus.PENDING)
    document_url = models.TextField(blank=True, null=True)
    reason_for_rejection = models.TextField(blank=True, null=True)
    verification_note = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(UserProfile, models.DO_NOTHING, db_column='verified_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.provider} - {self.type} - Status: {self.verification_status}"

    class Meta:
        managed = False
        db_table = 'service_provider_verification'





class ServiceProviderRankingWeights(models.Model):
    id = models.BigAutoField(primary_key=True)
    total_claims_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avg_claim_time_in_mins_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avg_rating_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    completed_leads_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_quotes_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accepted_quotes_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    daily_claim_count_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weekly_claim_count_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    two_weekly_claim_count_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_claim_count_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(unique=True, blank=True, null=True)
    distance_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_provider_ranking_weights'

    def __str__(self):
        return f"Weight - {self.id} - Active: {self.is_active}"




class ServiceProviderStatistics(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.OneToOneField(ServiceProvider, models.DO_NOTHING)
    total_claims = models.IntegerField(blank=True, null=True)
    avg_claim_time_in_mins = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    completed_leads = models.IntegerField(blank=True, null=True)
    total_quotes = models.IntegerField(blank=True, null=True)
    accepted_quotes = models.IntegerField(blank=True, null=True)
    daily_claim_count = models.IntegerField(blank=True, null=True)
    weekly_claim_count = models.IntegerField(blank=True, null=True)
    two_weekly_claim_count = models.IntegerField(blank=True, null=True)
    monthly_claim_count = models.IntegerField(blank=True, null=True)
    total_new_job_notifs = models.IntegerField(blank=False, null=False, default=0)
    daily_new_job_notifs = models.IntegerField(blank=False, null=False, default=0)
    weekly_new_job_notifs = models.IntegerField(blank=False, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_provider_statistics'

    def __str__(self):
        return f"Statistics for {self.provider.business_name} - Total Claims: {self.total_claims or 0}"