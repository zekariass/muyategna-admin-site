from django.contrib import admin
from .models import *

admin.site.register(Language)

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'version', 'country', 'is_required', 'is_active', 'effective_at')
    list_filter = ('is_active', 'is_required', 'country')
    search_fields = ('type', 'version')


@admin.register(LegalDocumentTranslation)
class LegalDocumentTranslationAdmin(admin.ModelAdmin):
    list_display = ('document', 'display_name', 'document_url', 'language', 'created_at', 'updated_at')
    search_fields = ('document__type',)
