from publicaciones import views
from django.urls import include, path
from comentarios.views import estado_comentario


urlpatterns = [
    path('home_articulos/',views.home_articulos,name='home_articulos'),
    path('home_galeria/',views.home_galeria,name='home_galeria'),
    path('noticias/ver/<int:id_noticia>/',views.ver_noticias,name='ver_noticias'),
    path('gestionar_noticia/',views.gestionar_noticia,name='gestionar_noticia'),
    path('noticias/home/',views.home_noticias,name='home_noticias'), 
    path('noticias/crear/', views.crear_noticia, name='crear_noticia'), 
    path('noticias/eliminar/<int:noticia_id>/',views.eliminar_noticia,name='eliminar_noticia'),
    path('noticias/lista/',views.lista_noticias,name='lista_noticias'),
    path('noticias/editar/<int:id_noticia>/', views.editar_noticia, name='editar_noticia'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('estado_comentario/<int:id_comentario>/', views.estado_comentario, name='estado_comentario'),
    path('eliminar_comentario/<int:id_comentario>/', views.eliminar_comentario, name='eliminar_comentario'),

    #Articulos
    path('articulos/home/',views.home_articulos,name='home_articulos'),
    path('articulos/crear/', views.crear_articulo, name='crear_articulo'),
    path('articulos/lista/',views.lista_articulos,name='lista_articulos'),
    path('articulos/editar/<int:id_articulo>/', views.editar_articulo, name='editar_articulo'),
    path('articulos/eliminar/<int:articulo_id>/',views.eliminar_articulo,name='eliminar_articulo'),
    path('gestionar_articulo/',views.gestionar_articulo,name='gestionar_articulos'),
    path('articulos/ver/<int:id_articulo>/',views.ver_articulo,name='ver_articulos'),
    
    #GALERIA
    path('galeria/home/',views.home_galeria,name='home_galeria'),
    path('galeria/crear/', views.crear_galeria, name='crear_galeria'),
    path('galeria/lista/',views.lista_galeria, name='lista_galeria'),
    path('galeria/editar/<int:id_galeria>/', views.editar_galeria, name='editar_galeria'),
    path('galeria/eliminar/<int:galeria_id>/',views.eliminar_galeria,name='eliminar_galeria'),
    path('galeria/ver/<int:id_galeria>/',views.ver_galeria,name='ver_galeria'),

    #ACERCA DE
    path('about/home/',views.home_acercade,name='home_acercade'),
    path('about/editar_acerca_de/', views.edit_my_about, name='editar_acerca_de'),


    
]