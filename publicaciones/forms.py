from django import forms

from publicaciones.models import Publicacion, Seccion
from django.forms import inlineformset_factory,ClearableFileInput
from imagen.models import Imagen 
from taggit.forms import TagWidget



class NoticiaForm(forms.ModelForm):
    imagen_portada = forms.ImageField(label='Imagen portada', widget=forms.FileInput)

    class Meta:
        model = Publicacion
        fields = ['titulo', 'bajada', 'cuerpo', 'estado', 'tags', 'imagen_portada']
        labels = {
            'imagen_portada': 'Imagen portada',
        }
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Etiqueta1, Etiqueta2, Etiqueta3 ...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen_portada'].required = True



class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'bajada', 'cuerpo', 'estado', 'tags','imagen_portada']
        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 5}),
            'tags': TagWidget(attrs={'placeholder': 'Etiqueta1, Etiqueta2, Etiqueta3 ...'}),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'cuerpo': 'Cuerpo',
            'estado': 'Estado',
            'imagen_portada': 'Imagen de Portada',
            'tags': 'Tags',
        }
        required_fields = ['titulo', 'bajada', 'cuerpo', 'estado', 'imagen_portada', 'tags']

    def __init__(self, *args, **kwargs):
        super(ArticulosForm, self).__init__(*args, **kwargs)
        for field in self.Meta.required_fields:
            self.fields[field].required = True

        


class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['estado', 'titulo', 'imagen_portada', 'imagen_marcador', 'equipamiento', 'detalle', 'cuerpo', 'tags']
        labels = {
            'imagen_portada': 'Imagen portada',
            'imagen_marcador': 'Imagen marcador',
        }
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Etiqueta1, Etiqueta2, Etiqueta3 ...'}),
        }
        required_fields = ['estado', 'titulo', 'imagen_portada', 'imagen_marcador', 'equipamiento', 'detalle', 'cuerpo', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required_fields:
            self.fields[field].required = True
            
class AboutForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['cuerpo']