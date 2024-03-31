from django.shortcuts import render

from publicaciones.models import Publicacion

def home(request):
    articulos = Publicacion.objects.filter(seccion__tipo_seccion='Articulo').exclude(estado__in=["Archivado", "Borrador"])
    noticias = Publicacion.objects.filter(seccion__tipo_seccion='Noticias').exclude(estado__in=["Archivado", "Borrador"])
    galerias = Publicacion.objects.filter(seccion__tipo_seccion='Galeria').exclude(estado__in=["Archivado", "Borrador"])

    todas_las_noticias = Publicacion.objects.filter(seccion__tipo_seccion='Noticias')
    todas_los_articulos = Publicacion.objects.filter(seccion__tipo_seccion='Articulo')
    todas_las_galerias = Publicacion.objects.filter(seccion__tipo_seccion='Galeria')

    noticias_publicadas = todas_las_noticias.filter(estado='Publicado').count()
    noticias_archivadas = todas_las_noticias.filter(estado='Archivado').count()
    noticias_borrador = todas_las_noticias.filter(estado='Borrador').count()

    articulos_publicados = todas_los_articulos.filter(estado='Publicado').count()
    articulos_archivados = todas_los_articulos.filter(estado='Archivado').count()
    articulos_borrador = todas_los_articulos.filter(estado='Borrador').count()

    galerias_publicadas = todas_las_galerias.filter(estado='Publicado').count()
    galerias_archivadas = todas_las_galerias.filter(estado='Archivado').count()
    galerias_borrador = todas_las_galerias.filter(estado='Borrador').count()

    labels_pie_noticias = ['Publicadas', 'Archivadas', 'Borrador']
    data_pie_noticias = [noticias_publicadas, noticias_archivadas, noticias_borrador]

    labels_pie_articulos = ['Publicados', 'Archivados', 'Borrador']
    data_pie_articulos = [articulos_publicados, articulos_archivados, articulos_borrador]

    labels_pie_galerias = ['Publicadas', 'Archivadas', 'Borrador']
    data_pie_galerias = [galerias_publicadas, galerias_archivadas, galerias_borrador]

    context = {
        'articulos': articulos,
        'noticias': noticias,
        'galerias': galerias,
        'noticias_publicadas': noticias_publicadas,
        'noticias_archivadas': noticias_archivadas,
        'noticias_borrador': noticias_borrador,
        'articulos_publicados': articulos_publicados,
        'articulos_archivados': articulos_archivados,
        'articulos_borrador': articulos_borrador,
        'galerias_publicadas': galerias_publicadas,
        'galerias_archivadas': galerias_archivadas,
        'galerias_borrador': galerias_borrador,
        'labels_pie_noticias': labels_pie_noticias,
        'data_pie_noticias': data_pie_noticias,
        'labels_pie_articulos': labels_pie_articulos,
        'data_pie_articulos': data_pie_articulos,
        'labels_pie_galerias': labels_pie_galerias,
        'data_pie_galerias': data_pie_galerias,
    }
    return render(request, 'home.html', context=context)


def base(request):
    return render(request, 'base.html')