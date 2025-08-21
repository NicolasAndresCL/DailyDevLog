from rest_framework import generics, mixins, filters, parsers
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_view, extend_schema
from desktop_ui.models import DailyLog
from desktop_ui.serializers import DailyLogSerializer

class DailyLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema_view(
    get=extend_schema(
        summary="Listar tareas diarias",
        description="Devuelve una lista paginada de tareas registradas con filtros, ordenamiento y previews de imágenes.",
        tags=["DailyLog"],
        operation_id="dailylog_list",
    ),
    post=extend_schema(
        summary="Registrar nueva tarea diaria",
        description="Crea un nuevo registro con nombre, horas, tecnologías, descripción, links técnicos e imágenes adjuntas.",
        tags=["DailyLog"],
        operation_id="dailylog_create",
    ),
)
class DailyLogListCreateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = DailyLog.objects.all().order_by('-fecha_creacion')
    serializer_class = DailyLogSerializer
    pagination_class = DailyLogPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre_tarea', 'descripcion', 'tecnologias_utilizadas']
    ordering_fields = ['fecha_creacion', 'horas']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@extend_schema_view(
    get=extend_schema(
        summary="Ver detalle de tarea diaria",
        description="Devuelve los datos completos de una tarea específica por ID, incluyendo imágenes y links.",
        tags=["DailyLog"],
        operation_id="dailylog_retrieve",
    ),
    put=extend_schema(
        summary="Actualizar tarea diaria",
        description="Modifica los datos de una tarea existente, incluyendo descripción, links e imágenes.",
        tags=["DailyLog"],
        operation_id="dailylog_update",
    ),
    delete=extend_schema(
        summary="Eliminar tarea diaria",
        description="Elimina un registro específico del historial de tareas por ID.",
        tags=["DailyLog"],
        operation_id="dailylog_delete",
    ),
)
class DailyLogDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
