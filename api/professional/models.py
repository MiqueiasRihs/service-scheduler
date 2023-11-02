from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

import uuid
import random
from unidecode import unidecode

class Professionals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
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
        return self.email