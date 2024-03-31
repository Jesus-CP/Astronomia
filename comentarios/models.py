from django.db import models
from publicaciones.models import Publicacion

class Comentario(models.Model):
    comentario = models.TextField()
    email = models.EmailField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    esta_publicado = models.BooleanField(default=False)
    idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f'Comentario por {self.email}'
