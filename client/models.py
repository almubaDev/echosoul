import uuid
from django.db import models

class Secreto(models.Model):
    TIPO_CHOICES = [
        ('texto', 'Texto'),
        ('audio', 'Audio'),
    ]

    id_usuario = models.UUIDField()  # Lo obtenemos desde sesión
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    contenido_texto = models.TextField(blank=True, null=True)
    contenido_audio = models.FileField(upload_to='audios/', blank=True, null=True)
    idioma = models.CharField(max_length=2, choices=[('es', 'Español'), ('en', 'English')])
    fecha_creado = models.DateTimeField(auto_now_add=True)
    publico = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo.capitalize()} secreto – {self.idioma.upper()}"
