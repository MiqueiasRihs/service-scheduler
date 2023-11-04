# Em urls.py
from django.urls import path

from api.customer.views import SchedulerCreateView

urlpatterns = [
    path('<str:professional_slug>/scheduler/', SchedulerCreateView.as_view(), name='set_customer_schedule'),
]
