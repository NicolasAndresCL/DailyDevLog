from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.response import Response

@extend_schema_view(
    post=extend_schema(
        summary="Obtener token JWT",
        description="Devuelve un par de tokens JWT (access y refresh) para autenticación de usuarios registrados.",
        tags=["Autenticación"],
        operation_id="api_token_create",
        responses={200: None}
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema_view(
    post=extend_schema(
        summary="Refrescar token JWT",
        description="Devuelve un nuevo token de acceso usando un token de refresh válido.",
        tags=["Autenticación"],
        operation_id="api_token_refresh_create",
        responses={200: None}
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
