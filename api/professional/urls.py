from django.urls import path

from api.professional.views import WorkingPlanView, SetIntervalView, ServiceView, \
    UpdateServiceView, DeleteServiceView, AppointmentTimesAvailableView, ScheduleListView, \
    HolidayList, HolidayCreate, HolidayUpdate, HolidayDelete, BlockHourList, VacationList, \
    VacationDelete, ProfessionalUpdateData

urlpatterns = [
    path('working-plan/', WorkingPlanView.as_view(), name='working-plan'),

    path('set-interval/', SetIntervalView.as_view(), name='set-interval'),
    
    path('services/', ServiceView.as_view(), name='services'),
    path('service/<uuid:service_id>/update/', UpdateServiceView.as_view(), name='service-update'),
    path('service/<uuid:service_id>/delete/', DeleteServiceView.as_view(), name='service-delete'),

    path('holidays/', HolidayList.as_view(), name='holiday-list'),
    path('holidays/create/', HolidayCreate.as_view(), name='holiday-create'),
    path('holidays/<uuid:holiday_id>/update/', HolidayUpdate.as_view(), name='holiday-update'),
    path('holidays/<uuid:holiday_id>/delete/', HolidayDelete.as_view(), name='holiday-delete'),

    path('block-hour/', BlockHourList.as_view(), name='block-hour'),
    
    path('vacations/', VacationList.as_view(), name='vacation-list'),
    path('vacations/<uuid:vacations_id>/delete/', VacationDelete.as_view(), name='vacation-delete'),

    path('update-data/', ProfessionalUpdateData.as_view(), name='updata-professional-data'),
    path('<str:professional_slug>/appointment-times-available/', AppointmentTimesAvailableView.as_view(), name='appointment-times-available'),
    path('schedules/<str:schedule_date>/', ScheduleListView.as_view(), name='schedules'),
]
