from django.db import models
from django.contrib.postgres.fields import ArrayField

from api.professional.models import Professional

import uuid

class Scheduler(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255)
    services = ArrayField(models.UUIDField(), blank=True, null=True)  # Assuming you're using PostgreSQL which has a native JSONB field
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    schedule_date = models.DateTimeField()
    end_time = models.DateTimeField()
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='scheduling')  # 'Professional' is another model you should define

    class Meta:
        db_table = 'scheduler'
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"Scheduler for {self.customer_name} on {self.schedule_date}"