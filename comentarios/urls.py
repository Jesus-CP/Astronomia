from django.urls import path
from . import views  

urlpatterns = [
    path('estado_comentario/<int:id_comentario>/', views.estado_comentario, name='estado_comentario'),
    path('eliminar_comentario/<int:id_comentario>/', views.eliminar_comentario, name='eliminar_comentario'),

]
