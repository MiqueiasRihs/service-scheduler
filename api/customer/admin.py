from django.contrib import admin

from api.customer.models import Scheduler

class SchedulerAdmin(admin.ModelAdmin):
  list_display = ("customer_name", "customer_phone", "schedule_date", "professional")
  search_fields = ['customer_phone', 'professional__user_username', ]
  readonly_fields = [x.name for x in Scheduler._meta.fields if x.name not in (
        'status',
    )]

admin.site.register(Scheduler, SchedulerAdmin)