# Em urls.py
from django.urls import path

from api.customer.views import SchedulerCreateView, GetSchedulerCustomerView

urlpatterns = [
    path('<str:professional_slug>/scheduler/', SchedulerCreateView.as_view(), name='set_customer_schedule'),
    path('schedules/<str:phone>/', GetSchedulerCustomerView.as_view(), name='set_customer_schedule'),
]
