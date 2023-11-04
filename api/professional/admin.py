from django.contrib import admin

from api.professional.models import Professional, Service

class ServiceAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "time", "value")
  
admin.site.register(Service, ServiceAdmin)

class ProfessionalAdmin(admin.ModelAdmin):
  list_display = ("id", "phone",)
  prepopulated_fields = {"slug": ("phone", "store")}
  
admin.site.register(Professional, ProfessionalAdmin)