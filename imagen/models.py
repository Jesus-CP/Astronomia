from django.db import models
from publicaciones.models import Publicacion 

class Imagen(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='imagenes',null=True)
    imagen_url = models.ImageField(upload_to='imagen/media/',null=True) 

    def __str__(self):
        return f'Imagen para la publicación {self.publicacion.id}'

