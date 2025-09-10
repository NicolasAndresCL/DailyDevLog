from rest_framework import generics, mixins, filters, parsers
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from desktop_ui.models import DailyLog
from desktop_ui.serializers import DailyLogSerializer
from rest_framework.permissions import IsAuthenticated

# 🔧 Paginación personalizada
class DailyLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# 📋 Vista para listar y crear tareas
@extend_schema_view(
    get=extend_schema(
        summary="Listar tareas diarias",
        description=(
            "Devuelve una lista paginada de registros con campos "
            "'project_name' y 'project_type', "
            "búsqueda, filtrado por tipo de proyecto, ordenamiento y URLs de imágenes."
        ),
        tags=["DailyLog"],
        operation_id="dailylog_list",
        parameters=[
            OpenApiParameter(
                name="project_type",
                description="Filtrar por tipo de proyecto: frontend, backend o fullstack",
                required=False,
                type=str
            ),
        ],
    ),
    post=extend_schema(
        summary="Registrar nueva tarea diaria",
        description=(
            "Crea un nuevo registro con nombre de proyecto, tipo de proyecto, "
            "nombre de tarea, horas, tecnologías, descripción, links e imágenes."
        ),
        tags=["DailyLog"],
        operation_id="dailylog_create",
        auth=[{"Bearer": []}],
    ),
)
class DailyLogListCreateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    permission_classes = []
    queryset = DailyLog.objects.all().order_by("fecha_creacion")
    serializer_class = DailyLogSerializer
    pagination_class = DailyLogPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["project_type"]
    search_fields = [
        "project_name",
        "nombre_tarea",
        "descripcion",
        "tecnologias_utilizadas",
    ]
    ordering_fields = [
        "fecha_creacion",
        "horas",
        "project_name",
        "project_type",
    ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Aquí podrías inyectar usuario u otros datos por defecto
        serializer.save()

# 📌 Vista para detalle, actualización y eliminación
@extend_schema_view(
    get=extend_schema(
        summary="Ver detalle de tarea diaria",
        description="Obtiene registro completo incluyendo proyecto, tipo, imágenes y links.",
        tags=["DailyLog"],
        operation_id="dailylog_retrieve",
    ),
    put=extend_schema(
        summary="Actualizar tarea diaria",
        description="Modifica todos los campos de un registro existente.",
        tags=["DailyLog"],
        operation_id="dailylog_update",
        auth=[{"Bearer": []}],
    ),
    patch=extend_schema(
        summary="Actualizar parcialmente tarea diaria",
        description="Modifica uno o más campos sin reemplazar el registro completo.",
        tags=["DailyLog"],
        operation_id="dailylog_partial_update",
        auth=[{"Bearer": []}],
    ),
    delete=extend_schema(
        summary="Eliminar tarea diaria",
        description="Elimina un registro específico por ID.",
        tags=["DailyLog"],
        operation_id="dailylog_delete",
        auth=[{"Bearer": []}],
    ),
)
class DailyLogDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    permission_classes = []
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return self.destroy(request, *args, **kwargs)
