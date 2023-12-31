# Generated by Django 4.2.4 on 2023-11-27 13:50

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('store', models.CharField(blank=True, max_length=100, null=True, verbose_name='Negócio')),
                ('phone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('interval', models.IntegerField(default=30, verbose_name='Intervalo')),
                ('instagram', models.CharField(blank=True, max_length=100, null=True, verbose_name='Instagram')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Slug')),
                ('profile_image_path', models.CharField(blank=True, max_length=250, null=True, verbose_name='Imagem')),
                ('is_active', models.BooleanField(default=True, verbose_name='ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professional', to=settings.AUTH_USER_MODEL, verbose_name='Profissional')),
            ],
            options={
                'verbose_name': 'Profissional',
                'verbose_name_plural': 'Profissionais',
                'db_table': 'professional',
            },
        ),
        migrations.CreateModel(
            name='WorkingPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField(verbose_name='Dia da semana')),
                ('start_time', models.CharField(verbose_name='Hora de início')),
                ('end_time', models.CharField(verbose_name='Hora de término')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_plans', to='professional.professional')),
            ],
            options={
                'verbose_name': 'Plano de trabalho',
                'verbose_name_plural': 'Planos de trabalho',
                'db_table': 'working_plan',
            },
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField(verbose_name='Data de início')),
                ('end_date', models.DateField(verbose_name='Data de fim')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to='professional.professional', verbose_name='Profissional')),
            ],
            options={
                'verbose_name': 'Férias',
                'verbose_name_plural': 'Férias',
                'db_table': 'vacation',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('time', models.TimeField(verbose_name='Tempo')),
                ('value', models.FloatField(blank=True, null=True, verbose_name='Valor')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='professional.professional', verbose_name='Profissional')),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Feriado')),
                ('date', models.DateField(verbose_name='Data')),
                ('start_time', models.CharField(blank=True, null=True, verbose_name='Hora de início')),
                ('end_time', models.CharField(blank=True, null=True, verbose_name='Hora de término')),
                ('every_year', models.BooleanField(default=True)),
                ('holiday_type', models.SmallIntegerField(choices=[(1, 'Dia inteiro'), (2, 'Meio horário')], default=1, verbose_name='Tipo de Feriado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holidays', to='professional.professional', verbose_name='Profissional')),
            ],
            options={
                'verbose_name': 'Feriado',
                'verbose_name_plural': 'Feriados',
                'db_table': 'holiday',
            },
        ),
        migrations.CreateModel(
            name='BreakTime',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.CharField(verbose_name='Hora de início')),
                ('end_time', models.CharField(verbose_name='Hora de término')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('working_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='break_time', to='professional.workingplan')),
            ],
            options={
                'verbose_name': 'Horário de pausa',
                'verbose_name_plural': 'Horários de pausa',
                'db_table': 'break_time',
            },
        ),
        migrations.CreateModel(
            name='BlockHour',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(unique=True)),
                ('hours', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_hour', to='professional.professional', verbose_name='Profissional')),
            ],
            options={
                'verbose_name': 'Horário bloqueado',
                'verbose_name_plural': 'Horários bloqueados',
                'db_table': 'block_hour',
            },
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Data')),
                ('start_time', models.CharField(blank=True, null=True, verbose_name='Hora de início')),
                ('end_time', models.CharField(blank=True, null=True, verbose_name='Hora de término')),
                ('absence_type', models.SmallIntegerField(choices=[(1, 'Dia inteiro'), (2, 'Meio horário')], default=1, verbose_name='Tipo de Ausência')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='atualizado em ')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absence', to='professional.professional', verbose_name='Profissional')),
            ],
            options={
                'verbose_name': 'Ausência',
                'verbose_name_plural': 'Ausências',
                'db_table': 'absence',
            },
        ),
    ]
