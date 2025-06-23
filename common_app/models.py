from django.db import models

class Language(models.Model):
    language_id = models.BigAutoField(primary_key=True)
    country = models.OneToOneField('location_app.Country', models.DO_NOTHING)
    name = models.CharField(max_length=50)
    locale = models.CharField(unique=True, max_length=10)
    is_active = models.BooleanField()
    is_default = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_global = models.BooleanField(unique=True)
    native_name = models.CharField(max_length=255, blank=True, null=True)
    direction = models.CharField(max_length=3, blank=True, null=True)
    flag_emoji = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'language'

    def __str__(self):
        if self.country:
            return f"{self.name} ({self.country})"
        return self.name
    


class LegalDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey('location_app.Country', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100) # name such as "Terms of Service"
    display_name = models.CharField(max_length=100, blank=True, null=True)  # internal name for reference
    version = models.CharField(max_length=20, blank=True, null=True)
    is_required = models.BooleanField()
    is_active = models.BooleanField()
    effective_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'legal_document'
        unique_together = (('name', 'country'),)

    def __str__(self):
        return f"{self.name} ({self.version or 'v1'}) - {self.country or 'Global'}"


class LegalDocumentTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(LegalDocument, models.DO_NOTHING)
    display_name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, models.DO_NOTHING, related_name='legal_document_translations')
    document_url = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'legal_document_translation'

    def __str__(self):
        return f"Translation for {self.document}"
