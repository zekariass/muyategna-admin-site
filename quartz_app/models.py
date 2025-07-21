from django.contrib.gis.db import models


class TriggerType(models.TextChoices):
    CRON = 'CRON', 'CRON'
    CALENDAR = 'CALENDAR', 'CALENDAR'

class IntervalUnit(models.TextChoices):
    SECONDS = 'SECONDS', 'SECONDS'
    MINUTES = 'MINUTES', 'MINUTES'
    HOURS = 'HOURS', 'HOURS'
    DAYS = 'DAYS', 'DAYS'
    WEEKS = 'WEEKS', 'WEEKS'
    MONTHS = 'MONTHS', 'MONTHS'
    YEARS = 'YEARS', 'YEARS'


class SchedulerConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_name = models.CharField(max_length=200)
    job_group = models.CharField(max_length=200)
    job_class = models.CharField(max_length=255)
    trigger_type = models.TextField(choices=TriggerType.choices, default=TriggerType.CRON) 
    cron_expression = models.CharField(max_length=100, blank=True, null=True)
    interval_value = models.IntegerField(blank=True, null=True)
    interval_unit = models.TextField(choices=IntervalUnit.choices, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    job_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'scheduler_config'

    def __str__(self):
        return f"{self.job_name} ({self.job_group})"