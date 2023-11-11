# Em urls.py
from django.urls import path

from api.customer.views import SchedulerCreateView, GetSchedulerCustomerView, CancelSchedulerCustomerView

urlpatterns = [
    path('<str:professional_slug>/schedules/', SchedulerCreateView.as_view(), name='set_customer_schedule'),
    path('schedules/<str:phone>/', GetSchedulerCustomerView.as_view(), name='get_customer_schedule'),
    path('cancel-schedules/<uuid:id>/', CancelSchedulerCustomerView.as_view(), name='cancel_customer_schedule'),
]
