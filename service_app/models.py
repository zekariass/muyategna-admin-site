from django.db import models
from location_app.models import Country
from common_app.models import Language
# ===================== SERVICE RELATED MODELS =====================


class ServiceCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_category'

    def __str__(self):
        return self.name
    

class ServiceCategoryTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_category = models.ForeignKey(ServiceCategory, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING, related_name='service_category_translations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_category_translation'
        unique_together = (('service_category', 'language'),)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_category = models.ForeignKey('ServiceCategory', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service'
    def __str__(self):
        return self.name


class ServiceTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING, related_name='service_translations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_translation'
        unique_together = (('service', 'language'),)

    def __str__(self):
        return self.name



class ServiceCountryAvailability(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING, related_name='available_services')
    is_active = models.BooleanField(blank=True, null=True)
    price_model = models.TextField()  # This field type is a guess.
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'service_country_availability'
        unique_together = (('service', 'country'),)

    def __str__(self):
        return f"{self.service.name} in {self.country.name}"
