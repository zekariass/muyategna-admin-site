from django.contrib import admin
from .models import *

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'language_id', 'name', 'locale', 'country', 'is_active', 'is_default',
        'is_global', 'direction', 'created_at', 'updated_at'
    )
    list_filter = ('is_active', 'is_default', 'is_global', 'country')
    search_fields = ('name', 'locale', 'native_name', 'country__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': (
                'name', 'native_name', 'locale', 'country', 'flag_emoji', 'direction'
            )
        }),
        ('Status', {
            'fields': ('is_active', 'is_default', 'is_global')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'version', 'country', 'is_required', 'is_active', 'effective_at')
    list_filter = ('is_active', 'is_required', 'country')
    search_fields = ('type', 'version')


@admin.register(LegalDocumentTranslation)
class LegalDocumentTranslationAdmin(admin.ModelAdmin):
    list_display = ('document', 'display_name', 'document_url', 'language', 'created_at', 'updated_at')
    search_fields = ('document__type',)
