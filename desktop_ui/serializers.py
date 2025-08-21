from rest_framework import serializers
from desktop_ui.models import DailyLog

class DailyLogSerializer(serializers.ModelSerializer):
    imagen_1_url = serializers.SerializerMethodField()
    imagen_2_url = serializers.SerializerMethodField()
    imagen_3_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyLog
        fields = [
            "id",
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
        read_only_fields = ["fecha_creacion", "imagen_1_url", "imagen_2_url", "imagen_3_url"]

    def get_imagen_1_url(self, obj):
        if obj.imagen_1:
            return self.context["request"].build_absolute_uri(obj.imagen_1.url)
        return None

    def get_imagen_2_url(self, obj):
        if obj.imagen_2:
            return self.context["request"].build_absolute_uri(obj.imagen_2.url)
        return None

    def get_imagen_3_url(self, obj):
        if obj.imagen_3:
            return self.context["request"].build_absolute_uri(obj.imagen_3.url)
        return None
