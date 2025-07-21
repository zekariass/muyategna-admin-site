from django import forms
from django.contrib.gis.geos import Point
from .models import Country, SubCityOrDivision, Address, City, CityTranslation, Region, RegionTranslation, CountryTranslation


class CountryForm(forms.ModelForm):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = Country
        # fields = '__all__'  # Include all original model fields automatically
        exclude = ['geo_point']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate lat/lon fields from the PointField if editing an existing instance
        if self.instance and self.instance.geo_point:
            self.fields['latitude'].initial = self.instance.geo_point.y
            self.fields['longitude'].initial = self.instance.geo_point.x

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat is not None and lon is not None:
            instance.geo_point = Point(lon, lat)  # Note Point(longitude, latitude)

        if commit:
            instance.save()
        return instance
    


class RegionForm(forms.ModelForm):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = Region
        # fields = '__all__'  # Include all original model fields automatically
        exclude = ['geo_point']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate lat/lon fields from the PointField if editing an existing instance
        if self.instance and self.instance.geo_point:
            self.fields['latitude'].initial = self.instance.geo_point.y
            self.fields['longitude'].initial = self.instance.geo_point.x

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat is not None and lon is not None:
            instance.geo_point = Point(lon, lat)  # Note Point(longitude, latitude)

        if commit:
            instance.save()
        return instance



class CityForm(forms.ModelForm):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = City
        # fields = '__all__'  # Include all original model fields automatically
        exclude = ['geo_point']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate lat/lon fields from the PointField if editing an existing instance
        if self.instance and self.instance.geo_point:
            self.fields['latitude'].initial = self.instance.geo_point.y
            self.fields['longitude'].initial = self.instance.geo_point.x

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat is not None and lon is not None:
            instance.geo_point = Point(lon, lat)  # Note Point(longitude, latitude)

        if commit:
            instance.save()
        return instance



class SubCityOrDivisionForm(forms.ModelForm):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = SubCityOrDivision
        # fields = '__all__'  # Include all original model fields automatically
        exclude = ['geo_point']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate lat/lon fields from the PointField if editing an existing instance
        if self.instance and self.instance.geo_point:
            self.fields['latitude'].initial = self.instance.geo_point.y
            self.fields['longitude'].initial = self.instance.geo_point.x

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat is not None and lon is not None:
            instance.geo_point = Point(lon, lat)  # Note Point(longitude, latitude)

        if commit:
            instance.save()
        return instance



class AddressForm(forms.ModelForm):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = Address
        # fields = '__all__'  # Include all original model fields automatically
        exclude = ['geo_point']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate lat/lon fields from the PointField if editing an existing instance
        if self.instance and self.instance.geo_point:
            self.fields['latitude'].initial = self.instance.geo_point.y
            self.fields['longitude'].initial = self.instance.geo_point.x

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat is not None and lon is not None:
            instance.geo_point = Point(lon, lat)
        elif not instance.geo_point:
            raise forms.ValidationError("Latitude and longitude are required.")

        if commit:
            instance.save()
        return instance