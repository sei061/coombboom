from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import pre_save, pre_delete
from django.utils.timezone import now
from datetime import datetime, time
from groups.models import Project
from tasks.models import Task
from django.contrib.auth.models import Group

class Entry(models.Model):
    """
    Represent record a log created by user to track Project.
    """
    comment = models.CharField(max_length=255)
    start_date = models.DateField(default=now)
    end_date = models.DateField(null=True)
    place = models.CharField(max_length=100)
    time_spent = models.FloatField(default=1)
    from_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='entries', blank=True, null=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='entries'
    )

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        return self.comment

    @property
    def total_duration(self):
        """
        Entry's property for the total duration alloted
        """
        delta = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.from_time)
        return delta.days * 24 + delta.seconds / 3600


