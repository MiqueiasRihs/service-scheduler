from django.urls import path

from api.professional.views import WorkingPlanView

urlpatterns = [
    path('working-plan/', WorkingPlanView.as_view(), name='working-plan'),
]
