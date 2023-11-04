from django.db import models

from api.professional.models import Professional

class Scheduler(models.Model):
    token = models.CharField(max_length=255, db_index=True)
    service_ids = models.JSONField()  # Assuming you're using PostgreSQL which has a native JSONB field
    customer_name = models.CharField(max_length=255, db_index=True)
    customer_phone = models.CharField(max_length=255, db_index=True)
    schedule_date = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='scheduling')  # 'Professional' is another model you should define

    class Meta:
        db_table = 'scheduler'
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"Scheduler for {self.customer_name} on {self.schedule_date}"