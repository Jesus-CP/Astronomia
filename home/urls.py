from . import views
from django.urls import include, path


urlpatterns = [

    path('', views.home, name='home'),
    path('publicaciones/', include('publicaciones.urls')),
    path('base/',views.base,name='base')
    
]