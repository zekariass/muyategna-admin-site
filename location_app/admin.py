from django.contrib import admin
from .models import *


# Register your models here.
# admin.site.register(Address)
# admin.site.register(SubCityOrDivision)
admin.site.register(SubCityOrDivisionTranslation)
# admin.site.register(City)
# admin.site.register(CityTranslation)
# admin.site.register(Region)
admin.site.register(RegionTranslation)
# admin.site.register(Country)
admin.site.register(CountryTranslation)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("country_id", "name", "iso_code2", "iso_code3", "iso_code_numeric", "continent", 
                    "description", "created_at", "updated_at", "is_global")


@admin.register(SubCityOrDivision)
class SubCityOrDivisionAdmin(admin.ModelAdmin):
    list_display = ("sub_city_or_division_id", "city", "name", "description", "created_at", "updated_at")

    

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_id", "country", "region", "city", "sub_city_or_division", "locality", 
                    "street", "landmark", "postal_code", "geo_point","full_address")
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_id", "region", "name", "description", "created_at", "updated_at")
    search_fields = ("region", "name")
    list_filter = ("region",)
    ordering = ("name",)
    # list_editable = ("region", "name", "description")

@admin.register(CityTranslation)
class CityTranslationAdmin(admin.ModelAdmin):
    list_display = ("translation_id", "city", "language", "name", "description", "created_at", "updated_at") 
    list_filter = ("city",)  


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("region_id", "country", "name", "description", "created_at", "updated_at" )

