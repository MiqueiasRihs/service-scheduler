from django.urls import path

from api.professional.views import WorkingPlanView, SetIntervalView, ServiceView, \
    UpdateServiceView

urlpatterns = [
    path('working-plan/', WorkingPlanView.as_view(), name='working_plan'),
    path('set-interval/', SetIntervalView.as_view(), name='set_interval'),
    path('services/', ServiceView.as_view(), name='services'),
    path('service/<uuid:service_id>/', UpdateServiceView.as_view(), name='update_service'),
]
