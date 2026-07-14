from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, parsers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from desktop_ui.models import DailyLog
from desktop_ui.serializers import DailyLogSerializer

# drf-spectacular tipa `auth` de forma estricta; en runtime acepta list[dict].
_BEARER_AUTH: list[Any] = [{"Bearer": []}]


class DailyLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(
        summary="Listar tareas diarias",
        description=(
            "Lista paginada de registros con búsqueda, filtrado por tipo de "
            "proyecto, ordenamiento y URLs de imágenes."
        ),
        tags=["DailyLog"],
        parameters=[
            OpenApiParameter(
                name="project_type",
                description="Filtrar por tipo de proyecto: frontend, backend o fullstack",
                required=False,
                type=str,
            ),
        ],
    ),
    retrieve=extend_schema(summary="Ver detalle de tarea diaria", tags=["DailyLog"]),
    create=extend_schema(summary="Registrar tarea diaria", tags=["DailyLog"], auth=_BEARER_AUTH),
    update=extend_schema(summary="Actualizar tarea diaria", tags=["DailyLog"], auth=_BEARER_AUTH),
    partial_update=extend_schema(
        summary="Actualizar parcialmente tarea diaria", tags=["DailyLog"], auth=_BEARER_AUTH
    ),
    destroy=extend_schema(summary="Eliminar tarea diaria", tags=["DailyLog"], auth=_BEARER_AUTH),
)
class DailyLogViewSet(viewsets.ModelViewSet):
    """CRUD de tareas diarias. Lectura pública; escritura sólo autenticada (JWT)."""

    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DailyLogPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["project_type"]
    search_fields = ["project_name", "nombre_tarea", "descripcion", "tecnologias_utilizadas"]
    ordering_fields = ["fecha_creacion", "horas", "project_name", "project_type"]
    ordering = ["-fecha_creacion"]
