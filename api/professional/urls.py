from django.urls import path

from api.professional.views import WorkingPlanView, SetIntervalView, ServiceView, \
    UpdateServiceView, DeleteServiceView, AppointmentTimesAvailableView, ScheduleListView

urlpatterns = [
    path('working-plan/', WorkingPlanView.as_view(), name='working_plan'),
    path('set-interval/', SetIntervalView.as_view(), name='set_interval'),
    path('services/', ServiceView.as_view(), name='services'),
    path('update-service/<uuid:service_id>/', UpdateServiceView.as_view(), name='update_service'),
    path('delete-service/<uuid:service_id>/', DeleteServiceView.as_view(), name='delete_service'),

    path('<str:professional_slug>/appointment-times-available/', AppointmentTimesAvailableView.as_view(), name='appointment_times_available'),
    path('schedules/<str:schedule_date>/', ScheduleListView.as_view(), name='schedules'),
]
