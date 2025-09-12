from django.contrib import admin
from django.utils.html import format_html
from .models import DailyLog

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_creacion',
        'project_name',
        'project_type',
        'nombre_tarea',
        'horas',
        'tecnologias_utilizadas',
        'commit_principal',
        'link_publicacion_linkedin_display',
        'link_ia_principal_display',
        'link_ia_secundaria_display',
        'link_ia_terciaria_display',
        'link_repositorio_display',
        'imagen_1_preview',
        'imagen_2_preview',
        'imagen_3_preview',
    )
    search_fields = (
        'project_name',
        'nombre_tarea',
        'descripcion',
        'tecnologias_utilizadas',
        'commit_principal',
    )
    list_filter = (
        'fecha_creacion',
        'project_type',
    )

    def _preview(self, obj, field_name):
        img = getattr(obj, field_name)
        if not img:
            return "—"
        return format_html(
            '<img src="{}" style="max-width:50px; max-height:50px; '
            'object-fit:cover; border:1px solid #ddd; margin:2px;" />',
            img.url
        )

    def imagen_1_preview(self, obj):
        return self._preview(obj, 'imagen_1')
    imagen_1_preview.short_description = "Img 1"
    imagen_1_preview.admin_order_field = 'imagen_1'

    def imagen_2_preview(self, obj):
        return self._preview(obj, 'imagen_2')
    imagen_2_preview.short_description = "Img 2"
    imagen_2_preview.admin_order_field = 'imagen_2'

    def imagen_3_preview(self, obj):
        return self._preview(obj, 'imagen_3')
    imagen_3_preview.short_description = "Img 3"
    imagen_3_preview.admin_order_field = 'imagen_3'

    def _link_display(self, obj, field_name, label):
        url = getattr(obj, field_name)
        if not url:
            return "—"
        return format_html('<a href="{}" target="_blank">{}</a>', url, label)

    def link_publicacion_linkedin_display(self, obj):
        return self._link_display(obj, 'link_publicacion_linkedin', 'LinkedIn')
    link_publicacion_linkedin_display.short_description = "LinkedIn"
    link_publicacion_linkedin_display.admin_order_field = 'link_publicacion_linkedin'

    def link_ia_principal_display(self, obj):
        return self._link_display(obj, 'link_ia_principal', 'IA Principal')
    link_ia_principal_display.short_description = "IA Principal"
    link_ia_principal_display.admin_order_field = 'link_ia_principal'

    def link_ia_secundaria_display(self, obj):
        return self._link_display(obj, 'link_ia_secundaria', 'IA Secundaria')
    link_ia_secundaria_display.short_description = "IA Secundaria"
    link_ia_secundaria_display.admin_order_field = 'link_ia_secundaria'

    def link_ia_terciaria_display(self, obj):
        return self._link_display(obj, 'link_ia_terciaria', 'IA Terciaria')
    link_ia_terciaria_display.short_description = "IA Terciaria"
    link_ia_terciaria_display.admin_order_field = 'link_ia_terciaria'

    def link_repositorio_display(self, obj):
        return self._link_display(obj, 'link_respositorio', 'Repositorio')
    link_repositorio_display.short_description = "Repositorio"
    link_repositorio_display.admin_order_field = 'link_respositorio'
