from django.urls import path

from api.professional.views import WorkingPlanView, SetIntervalView

urlpatterns = [
    path('working-plan/', WorkingPlanView.as_view(), name='working-plan'),
    path('set-interval/', SetIntervalView.as_view(), name='set-interval'),
]
