from django.contrib import admin
from .models import DailyLog

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_creacion",
        "nombre_tarea",
        "horas",
        "tecnologias_utilizadas",
        "link_publicacion_linkedin",
        "link_ia_principal",
        "imagen_1_preview",
        "imagen_2_preview",
        "imagen_3_preview",
    )
    search_fields = (
        "nombre_tarea",
        "descripcion",
        "tecnologias_utilizadas",
        "link_publicacion_linkedin",
        "link_ia_principal",
    )
    list_filter = ("fecha_creacion",)

    def imagen_1_preview(self, obj):
        if obj.imagen_1:
            return f"✅"
        return "—"
    imagen_1_preview.short_description = "Img 1"

    def imagen_2_preview(self, obj):
        if obj.imagen_2:
            return f"✅"
        return "—"
    imagen_2_preview.short_description = "Img 2"

    def imagen_3_preview(self, obj):
        if obj.imagen_3:
            return f"✅"
        return "—"
    imagen_3_preview.short_description = "Img 3"
