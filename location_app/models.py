from django.db import models
from django.contrib.gis.db import models as gis_models
from common_app.models import Language


class Country(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    iso_code2 = models.CharField(unique=True, max_length=2)
    iso_code3 = models.CharField(unique=True, max_length=3, blank=True, null=True)
    iso_code_numeric = models.CharField(unique=True, max_length=3, blank=True, null=True)
    continent = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_global = models.BooleanField()
    taxpayer_id_type = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    geo_point = gis_models.PointField(geography=True, srid=4326, null=False)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'country'
    
    def __str__(self):
        return self.name


class CountryTranslation(models.Model):
    translation_id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'country_translation'
        unique_together = (('country', 'language'),)
    
    def __str__(self):
        if self.country:
            return f"{self.name} ({self.country})"
        if self.language:
            return f"{self.name} ({self.language})"
        return self.name


class Region(models.Model):
    region_id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    geo_point = gis_models.PointField(geography=True, srid=4326, null=False)  # This field type is a guess.


    class Meta:
        managed = False
        db_table = 'region'
        unique_together = (('name', 'country'),)

    def __str__(self):
        if self.country:
            return f"{self.name} ({self.country})"
        return self.name


class City(models.Model):
    city_id = models.BigAutoField(primary_key=True)
    region = models.ForeignKey(Region, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, db_default=models.functions.Now())
    updated_at = models.DateTimeField(editable=False, db_default=models.functions.Now())
    geo_point = gis_models.PointField(geography=True, srid=4326, null=False)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'city'
        unique_together = (('name', 'region'),)

    def __str__(self):
        if self.region:
            return f"{self.name} ({self.region})"
        return self.name



class CityTranslation(models.Model):
    translation_id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'city_translation'
        unique_together = (('city', 'language'),)
    
    def __str__(self):
        if self.city:
            return f"{self.name} ({self.city})"
        if self.language:
            return f"{self.name} ({self.language})"
        return self.name


class RegionTranslation(models.Model):
    translation_id = models.BigAutoField(primary_key=True)
    region = models.ForeignKey(Region, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'region_translation'
        unique_together = (('region', 'language'),)

    def __str__(self):
        if self.region:
            return f"{self.name} ({self.region})"
        if self.language:
            return f"{self.name} ({self.language})"
        return self.name


class SubCityOrDivision(models.Model):
    sub_city_or_division_id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    geo_point = gis_models.PointField(geography=True, srid=4326, null=False)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sub_city_or_division'
        unique_together = (('name', 'city'),)

    def __str__(self):
        if self.city:
            return f"{self.name} ({self.city})"
        return self.name


class SubCityOrDivisionTranslation(models.Model):
    translation_id = models.BigAutoField(primary_key=True)
    sub_city_or_division = models.ForeignKey(SubCityOrDivision, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'sub_city_or_division_translation'
        unique_together = (('sub_city_or_division', 'language'),)

    def __str__(self):
        if self.sub_city_or_division:
            return f"{self.name} ({self.sub_city_or_division})"
        if self.language:
            return f"{self.name} ({self.language})"
        return self.name


class Address(models.Model):
    address_id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    region = models.ForeignKey(Region, models.DO_NOTHING)
    city = models.ForeignKey(City, models.DO_NOTHING)
    sub_city_or_division = models.ForeignKey(SubCityOrDivision, models.DO_NOTHING, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    geo_point = gis_models.PointField(geography=True, srid=4326, null=False)
    h3_index_res7 = models.CharField(max_length=30, blank=False, null=False)  # H3 index at resolution 7
    h3_index_res8 = models.CharField(max_length=30, blank=False, null=False)  # H3 index at resolution 8
    h3_index_res9 = models.CharField(max_length=30, blank=False, null = False)  # H3 index at resolution 9  
    full_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'

    def __str__(self):
        return self.sub_city_or_division.name if self.sub_city_or_division is not None else self.city.name
