from rest_framework import serializers
from desktop_ui.models import DailyLog

class DailyLogSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        max_length=100,
        help_text="Nombre del proyecto asociado a la tarea"
    )
    project_type = serializers.ChoiceField(
        choices=DailyLog.PROJECT_TYPE_CHOICES,
        help_text="Tipo de proyecto: frontend, backend o fullstack"
    )
    imagen_1_url = serializers.SerializerMethodField()
    imagen_2_url = serializers.SerializerMethodField()
    imagen_3_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyLog
        fields = [
            "id",
            "project_name",
            "project_type",
            "nombre_tarea",
            "descripcion",
            "horas",
            "tecnologias_utilizadas",
            "fecha_creacion",
            "imagen_1",
            "imagen_2",
            "imagen_3",
            "imagen_1_url",
            "imagen_2_url",
            "imagen_3_url",
            "link_publicacion_linkedin",
            "link_ia_principal",
            "link_ia_secundaria",
            "link_ia_terciaria",
            "link_respositorio",
            "commit_principal",
        ]
        read_only_fields = [
            "fecha_creacion",
            "imagen_1_url",
            "imagen_2_url",
            "imagen_3_url",
        ]

    def get_imagen_1_url(self, obj):
        return self._build_url(obj.imagen_1)

    def get_imagen_2_url(self, obj):
        return self._build_url(obj.imagen_2)

    def get_imagen_3_url(self, obj):
        return self._build_url(obj.imagen_3)

    def _build_url(self, imagen_field):
        request = self.context.get("request")
        if imagen_field and request:
            return request.build_absolute_uri(imagen_field.url)
        if imagen_field:
            return imagen_field.url
        return None
