from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from desktop_ui.views.api.dailylog_views import DailyLogListCreateAPIView, DailyLogDetailAPIView
from desktop_ui.views.api.auth_views import CustomTokenObtainPairView as TokenObtainPairView
from desktop_ui.views.api.auth_views import CustomTokenRefreshView as TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
import os

print(f"MEDIA_ROOT real: {os.path.abspath(settings.MEDIA_ROOT)}")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/dailylog/', DailyLogListCreateAPIView.as_view(), name='dailylog-list-create'),
    path('api/dailylog/<int:pk>/', DailyLogDetailAPIView.as_view(), name='dailylog-detail'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
