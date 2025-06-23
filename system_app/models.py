from django.db import models
from user_app.models import UserProfile


class SystemConfig(models.Model):
    config_id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    value = models.TextField()
    type = models.TextField()  # This field type is a guess.
    created_by = models.ForeignKey(UserProfile, models.DO_NOTHING, db_column='created_by')
    updated_by = models.ForeignKey(UserProfile, models.DO_NOTHING, db_column='updated_by', related_name='systemconfig_updated_by_set')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'system_config'

    def __str__(self):
        return self.name