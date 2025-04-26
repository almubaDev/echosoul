from django.db import models

class IdentidadAnonima(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    user_hash = models.CharField(max_length=64)  # SHA-256 tiene 64 caracteres hexadecimales
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creditos = models.IntegerField(default=0)  # Se inicializa con 0 créditos

    def __str__(self):
        return f"Anon {self.user_id[:8]}... | Créditos: {self.creditos}"
