from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
import random
from unidecode import unidecode


class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Profissional', related_name='professional')
    store = models.CharField('Negócio', max_length=100, blank=True, null=True)
    phone = models.CharField('Telefone', max_length=15)
    interval = models.IntegerField('Intervalo', default=30)
    instagram = models.CharField('Instagram', max_length=100, blank=True, null=True)
    slug = models.SlugField('Slug', unique=True, max_length=250)
    profile_image_path = models.CharField('Imagem', max_length=250, blank=True, null=True)
    
    is_active = models.BooleanField('ativo', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    def generate_slug(self, name):
        slug = slugify(unidecode(name))
        slug = ''.join(e for e in slug if e.isalnum() or e.isspace())
        return f"{slug}-{random.randint(100000, 999999)}"

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug(self.user.first_name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'professional'
        verbose_name_plural = 'Profissionais'
        verbose_name = 'Profissional'

    def __str__(self):
        return self.user.username


class WorkingPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day_of_week = models.IntegerField('Dia da semana')
    start_time = models.CharField('Hora de início')
    end_time = models.CharField('Hora de término')
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='working_plans')

    class Meta:
        db_table = 'working_plan'
        verbose_name = 'Plano de trabalho'
        verbose_name_plural = 'Planos de trabalho'

    def __str__(self):
        return f"Dia da semana {self.day_of_week} - {self.professional.user.username}"


class BreakTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.CharField('Hora de início')
    end_time = models.CharField('Hora de término')
    working_plan = models.ForeignKey(WorkingPlan, on_delete=models.CASCADE, related_name='break_time')

    class Meta:
        db_table = 'break_time'
        verbose_name = 'Horário de pausa'
        verbose_name_plural = 'Horários de pausa'

    def __str__(self):
        return f"{self.start_time} to {self.end_time}"


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome', max_length=100)
    time = models.TimeField('Tempo')
    value = models.FloatField('Valor', blank=True, null=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='service', verbose_name='Profissional')

    class Meta:
        db_table = 'service'
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.name


class Scheduling(models.Model):
    token = models.CharField(max_length=255, db_index=True)
    service_ids = models.JSONField()  # Assuming you're using PostgreSQL which has a native JSONB field
    customer_name = models.CharField(max_length=255, db_index=True)
    customer_phone = models.CharField(max_length=255, db_index=True)
    schedule_date = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='scheduling')  # 'Professional' is another model you should define

    class Meta:
        db_table = 'scheduling'  # Defines the name of the table in the database
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"Scheduling for {self.customer_name} on {self.schedule_date}"