from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from desktop_ui.views.api.dailylog_views import (
    DailyLogListCreateAPIView,
    DailyLogDetailAPIView,
    FrontendAppView,
)
from desktop_ui.views.api.auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/dailylog/', DailyLogListCreateAPIView.as_view(), name='dailylog-list-create'),
    path('api/dailylog/<int:pk>/', DailyLogDetailAPIView.as_view(), name='dailylog-detail'),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),

    re_path(r'^(?!api/|admin/).*$', FrontendAppView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
