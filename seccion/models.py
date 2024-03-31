from django.db import models

class Seccion(models.Model):
    TIPOS_SECCION = (
        ('Noticia', 'Noticia'),
        ('Articulo', 'Articulo'),
        ('Galeria', 'Galeria'),
    )

    nombre = models.CharField(max_length=50, unique=True, choices=TIPOS_SECCION)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
