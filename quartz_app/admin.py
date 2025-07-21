from django.contrib import admin
from .models import SchedulerConfig

# Register your models here.
@admin.register(SchedulerConfig)
class SchedulerConfigAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'job_name', 
        'job_group', 
        'trigger_type', 
        'cron_expression', 
        'interval_value', 
        'interval_unit', 
        'is_active',
        'created_at',
        'updated_at'
    )
    list_filter = ('is_active', 'trigger_type', 'interval_unit', 'job_group')
    search_fields = ('job_name', 'job_group', 'job_class', 'description')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')