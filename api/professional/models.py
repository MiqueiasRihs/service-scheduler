from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from api.professional.constants import HolidayType, HOLIDAY_TYPE_CHOICES

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
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

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
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

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
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    class Meta:
        db_table = 'service'
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.name


class Holiday(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nome do Feriado")
    date = models.DateField(verbose_name="Data")
    start_time = models.CharField('Hora de início', blank=True, null=True)
    end_time = models.CharField('Hora de término', blank=True, null=True)
    every_year = models.BooleanField(default=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='holidays', verbose_name='Profissional')
    holiday_type = models.SmallIntegerField(choices=HOLIDAY_TYPE_CHOICES, default=HolidayType.FULL_DAY, verbose_name="Tipo de Feriado")
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'holiday'
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"
        

class Absence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name="Data")
    start_time = models.CharField('Hora de início', blank=True, null=True)
    end_time = models.CharField('Hora de término', blank=True, null=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='absence', verbose_name='Profissional')
    absence_type = models.SmallIntegerField(choices=HOLIDAY_TYPE_CHOICES, default=HolidayType.FULL_DAY, verbose_name="Tipo de Ausência")
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    def __str__(self):
        return self.date

    class Meta:
        db_table = 'absence'
        verbose_name = "Ausência"
        verbose_name_plural = "Ausências"


class BlockHour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(unique=True)
    hours = ArrayField(models.TimeField())
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='block_hour', verbose_name='Profissional')
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    def __str__(self):
        return str(self.date)
    
    class Meta:
        db_table = 'block_hour'
        verbose_name = "Horário bloqueado"
        verbose_name_plural = "Horários bloqueados"
        
        
class Vacation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField(verbose_name='Data de início')
    end_date = models.DateField(verbose_name='Data de fim')
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='vacations', verbose_name='Profissional')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return f"Férias de {self.professional} de {self.start_date} até {self.end_date}"

    class Meta:
        db_table = 'vacation'
        verbose_name = "Férias"
        verbose_name_plural = "Férias"
        ordering = ['start_date']

    def clean(self):
        # Validação adicional para garantir que a data de início é antes da data de fim
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('A data de início das férias deve ser anterior à data de fim.')