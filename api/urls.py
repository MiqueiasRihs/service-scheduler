from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from  django.conf.urls.static import static 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.professional.views import ProfessionalData

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('auth/', include("api.user_auth.urls")),
    path('customer/', include("api.customer.urls")),
    path('professional/', include("api.professional.urls")),
    
    path('<slug:professional_slug>/', ProfessionalData.as_view(), name='professional_data'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
