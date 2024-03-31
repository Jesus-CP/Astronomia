from django.db import models
from django.contrib.auth.models import User  # Importar el modelo de usuario
from seccion.models import Seccion  # Importar el modelo Seccion de la app seccion
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Seccion(models.Model):
    id_seccion = models.AutoField(primary_key=True)
    secciones = (
        ('Articulo', 'Articulo'),
        ('Noticia','Noticia'),
        ('Galeria','Galeria'),
        ('About','About')

    )
    tipo_seccion = models.CharField(max_length=10, choices=secciones)

class Publicacion(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='editor_post')
    idPublicacion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    bajada = models.TextField(null=True)
    cuerpo = RichTextUploadingField(blank=True, null=True)
    fuente = models.CharField(max_length=200, null=True, blank=True)
    documento = models.FileField(upload_to='documentos/', null=True, blank=True)
    imagen_portada = models.ImageField(upload_to='imagen_portada/', null=True, blank=True)
    equipamiento = RichTextUploadingField(blank=True, null=True)
    detalle = RichTextUploadingField(blank=True, null=True)
    imagen_marcador = models.ImageField(upload_to='imagen_marcador/', null=True, blank=True)
    
    ESTADOS = (
        ('Borrador', 'Borrador'),
        ('Publicado', 'Publicado'),
        ('Archivado', 'Archivado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='Borrador')
    
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, null=True)

    usuario_creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones_creadas')
    
    tags = TaggableManager()
    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
