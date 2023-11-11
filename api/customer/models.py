from django.db import models
from django.contrib.postgres.fields import ArrayField

from api.professional.models import Professional

from api.customer.constants import SchedulerStatus, SCHEDULER_STATUS_CHOICES

import uuid

class Scheduler(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    services = ArrayField(models.UUIDField(), blank=True, null=True)  # Assuming you're using PostgreSQL which has a native JSONB field
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=15)
    schedule_date = models.DateTimeField()
    end_time = models.DateTimeField()
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='scheduling')  # 'Professional' is another model you should define
    status = models.SmallIntegerField(choices=SCHEDULER_STATUS_CHOICES, verbose_name='Status', default=SchedulerStatus.SCHEDULED)

    class Meta:
        db_table = 'scheduler'
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.customer_name} em {self.schedule_date}"