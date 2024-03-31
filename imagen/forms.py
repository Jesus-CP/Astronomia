from django import forms

from publicaciones.models import Publicacion, Seccion
from imagen.models import Imagen
from django.forms import inlineformset_factory,ClearableFileInput


class BaseImagenFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['DELETE'].label = 'Eliminar'

imagen_list = inlineformset_factory(
    Publicacion,
    Imagen,
    fields=['urls'],
    extra=10,
    can_delete=True,
    formset=BaseImagenFormSet
)

class Seccion(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ['tipo_seccion']