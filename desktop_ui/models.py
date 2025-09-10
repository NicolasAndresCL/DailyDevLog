from django.db import models
from django.conf import settings

class DailyLog(models.Model):
    project_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del proyecto"
    )

    PROJECT_TYPE_CHOICES = [
        ("frontend", "Frontend"),
        ("backend",  "Backend"),
        ("fullstack", "Fullstack"),
    ]
    project_type = models.CharField(
        max_length=20,
        choices=PROJECT_TYPE_CHOICES,
        default='frontend',
        blank=True,
        verbose_name="Tipo de proyecto"
    )
    nombre_tarea = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    horas = models.DecimalField(max_digits=4, decimal_places=2)
    tecnologias_utilizadas = models.CharField(max_length=255)

    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def get_imagen_url(self, imagen_field):
        if imagen_field:
            return imagen_field.url
        return None


    # Imágenes adjuntas
    imagen_1 = models.ImageField(upload_to='dailylog/', blank=True, null=True)
    imagen_2 = models.ImageField(upload_to='dailylog/', blank=True, null=True)
    imagen_3 = models.ImageField(upload_to='dailylog/', blank=True, null=True)

    # Links técnicos
    link_publicacion_linkedin = models.URLField(blank=True, null=True)
    link_ia_principal = models.URLField(blank=True, null=True)
    link_ia_secundaria = models.URLField(blank=True, null=True)
    link_ia_terciaria = models.URLField(blank=True, null=True)
    link_respositorio = models.URLField(blank=True, null=True)
    commit_principal = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_tarea} ({self.fecha_creacion.date()})"
