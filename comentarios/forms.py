from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario', 'email']

class CambiarEstadoComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['esta_publicado']

