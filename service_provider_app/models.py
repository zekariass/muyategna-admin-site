from django.db import models
from service_app.models import Service
from location_app.models import Address, Country
from user_app.models import UserProfile
from common_app.models import LegalDocument

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
    id = models.BigAutoField(primary_key=True)
    business_name = models.CharField(max_length=255)
    business_description = models.TextField(blank=True, null=True)
    service_provider_type = models.TextField(choices=ServiceProviderType, default=ServiceProviderType.SOLE_TRADER)
    business_address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    num_employees = models.IntegerField(blank=True, null=True)
    max_travel_distance_in_km = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    portfolio_url = models.TextField(blank=True, null=True)
    portfolio_type = models.TextField(choices=PortfolioType, default=PortfolioType.WEBSITE)  
    business_logo_url = models.TextField(blank=True, null=True)
    verification_status = models.TextField(choices=VerificationStatus, default=VerificationStatus.PENDING)  
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    number_of_reviews = models.IntegerField(blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)

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



class ServiceProviderServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    is_active = models.BooleanField(blank=True, null=True)
    linked_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.provider} - {self.service}"

    class Meta:
        managed = False
        db_table = 'service_provider_services'


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

