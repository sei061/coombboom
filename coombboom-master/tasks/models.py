from django.db import models
from django.utils.timezone import now

from groups.models import Project


class Task(models.Model):
    task_name = models.CharField(max_length=45)
    task_status = models.CharField(max_length=45)
    start_date = models.DateField(default=now)
    expected_time = models.FloatField(default=1)
    est_time = models.DateField(default=now)
    original_time = models.FloatField(default=1)
    time_changed = models.BooleanField(default=False)
    when_changed = models.DateField(default=now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.task_name
