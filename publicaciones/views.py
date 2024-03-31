from django.shortcuts import render,get_object_or_404, redirect
from .forms import NoticiaForm, ArticulosForm, GaleriaForm, AboutForm

from .models import Publicacion,Seccion
from imagen.models import Imagen
from django.contrib.auth.decorators import login_required

from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from comentarios.forms import ComentarioForm
from comentarios.models import Comentario
from comentarios.views import *
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail





######## ARTICULOS ############

def gestionar_articulo(request):
    return render(request, 'articulos/gestionar_articulos.html')


def home_articulos(request):
    if request.method == "POST":
        articuloo = ArticulosForm(request.POST, request.FILES)
        if articuloo.is_valid():
            articuloo.save()

    query = request.GET.get('q')
    tag_filtro = request.GET.get('tag')
    estado = request.GET.get('estado')  # Obtener el estado del formulario

    if request.user.is_authenticated:
        # Filtrar las publicaciones por la sección "Articulo"
        articulos = Publicacion.objects.filter(seccion__tipo_seccion='Articulo')
        if estado and estado != "Todo":
            articulos = articulos.filter(estado=estado)
    else:
        # Filtrar las publicaciones por la sección "Articulo"
        articulos = Publicacion.objects.filter(seccion__tipo_seccion='Articulo').exclude(estado__in=["Archivado", "Borrador"])

    if tag_filtro:
        articulos = articulos.filter(tags__name__in=[tag_filtro])

    if query:
        articulos = articulos.filter(Q(titulo__icontains=query))

    articulos = articulos.order_by('-fecha_creacion')
    paginator = Paginator(articulos, 12)
    page = request.GET.get('page')

    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)

    context = {
        'articulos': articulos
    }
    return render(request, 'articulos/home_articulos.html', context=context)




@login_required(login_url='login')
def crear_articulo(request):
    if Seccion.objects.count() == 0:
        secciones = [
            {'id_seccion': 1, 'tipo_seccion': 'Noticias'},
            {'id_seccion': 2, 'tipo_seccion': 'Articulo'},
            {'id_seccion': 3, 'tipo_seccion': 'Galeria'}
        ]
        for datos in secciones:
            crear_secciones = Seccion(**datos)
            crear_secciones.save()
        # Código para crear secciones...

        if request.method == 'POST':
            articulo_form = ArticulosForm(request.POST, request.FILES)
            if articulo_form.is_valid():
                articulo = articulo_form.save(commit=False)
                articulo.editor = request.user
                articulo.usuario_creador = request.user
                articulo.seccion = Seccion.objects.get(id_seccion=2)  
                articulo.save()
                articulo_form.save_m2m()  
                return redirect('lista_articulos')

    if request.method == 'POST':
        articulo_form = ArticulosForm(request.POST, request.FILES)
        if articulo_form.is_valid():
            articulo = articulo_form.save(commit=False)
            articulo.editor = request.user
            articulo.usuario_creador = request.user
            articulo.seccion = Seccion.objects.get(id_seccion=2)  
            articulo.save()
            articulo_form.save_m2m()  
            return redirect('lista_articulos')
    else:
        articulo_form = ArticulosForm()

    context = {
        'articulos_form': articulo_form,
    }
    return render(request, 'articulos/crear_articulos.html', context)


def ver_articulo(request, id_articulo):
    articulo = get_object_or_404(Publicacion, idPublicacion=id_articulo)

    if request.method == 'POST' and 'change_state' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.esta_publicado = 'is_published' in request.POST
        comentario.save()

    elif 'delete_comment' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.delete()

        return HttpResponseRedirect(request.path_info)

    elif request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.idPublicacion = articulo
            nuevo_comentario.save()

            # Enviar correo al usuario creador de la noticia
            subject = 'Nuevo comentario en tu publicación'
            message = f'Se ha añadido un nuevo comentario a tu publicación "{articulo.titulo}".'
            from_email = 'codemintest@gmail.com'
            recipient_list = [articulo.usuario_creador.email]

            send_mail(subject, message, from_email, recipient_list)

            return HttpResponseRedirect(request.path_info)

    if request.user.is_authenticated:
        comentarios = Comentario.objects.filter(idPublicacion=id_articulo)
    else:
        comentarios = Comentario.objects.filter(idPublicacion=id_articulo, esta_publicado=True)

    form = ComentarioForm()

    context = {
        'articulo': articulo,
        'comentarios': comentarios,
        'form': form,
    }

    return render(request, 'articulos/ver_articulo.html', context)



@login_required(login_url='login')
def lista_articulos(request):
    # Filtrar los artículos por usuario actual y sección 'Articulo'
    articulos = Publicacion.objects.filter(
        seccion__tipo_seccion='Articulo',
        usuario_creador=request.user
    )

    paginator = Paginator(articulos, 10)
    page = request.GET.get('page')

    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página.
        articulos = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página de resultados.
        articulos = paginator.page(paginator.num_pages)

    context = {
        'articulos': articulos,
    }

    return render(request, 'articulos/lista_articulos.html', context)

@login_required(login_url='login')
def editar_articulo(request, id_articulo):
    articulo = get_object_or_404(Publicacion, idPublicacion=id_articulo)

    if request.method == 'POST':
        articulo_form = ArticulosForm(request.POST, request.FILES, instance=articulo)

        if articulo_form.is_valid():
            articulo_form.save()
            return redirect('lista_articulos')  
    else:
        articulo_form = ArticulosForm(instance=articulo)

    context = {
        'articulo_form': articulo_form,
        'articulo': articulo,
    }
    return render(request, 'articulos/editar_articulo.html', context)

@login_required(login_url='login')
def eliminar_articulo(request, articulo_id):
    articulo = get_object_or_404(Publicacion, idPublicacion=articulo_id)
    if request.user == articulo.editor:
        articulo.delete()
        return redirect('lista_articulos')


####### GALERIA ################

def home_galeria(request):
    if request.method == "POST":
        galeria = GaleriaForm(request.POST, request.FILES)
        if galeria.is_valid():
            galeria.save()

    query = request.GET.get('q')  
    tag_filtro = request.GET.get('tag')
    estado = request.GET.get('estado')  # Obtener el estado del formulario

    if request.user.is_authenticated:
        galeria = Publicacion.objects.filter(seccion__tipo_seccion='Galeria')
        if estado and estado != "Todo":
            galeria = galeria.filter(estado=estado)
    else:
        galeria = Publicacion.objects.filter(seccion__tipo_seccion='Galeria').exclude(estado__in=["Archivado", "Borrador"])


    if tag_filtro:
        galeria = galeria.filter(tags__name__in=[tag_filtro])

    if query:
        galeria = galeria.filter(Q(titulo__icontains=query)) 

    galeria = galeria.order_by('-fecha_creacion')
    paginator = Paginator(galeria, 12)  
    page = request.GET.get('page')

    try:
        galeria = paginator.page(page)
    except PageNotAnInteger:
        galeria = paginator.page(1)
    except EmptyPage:
        galeria = paginator.page(paginator.num_pages)

    context = {
        'galerias': galeria
    }
    return render(request, 'galeria/home_galeria.html', context=context)




@login_required(login_url='login')
def crear_galeria(request):
    if Seccion.objects.count() == 0:
        secciones = [
            {'id_seccion': 1, 'tipo_seccion': 'Noticias'},
            {'id_seccion': 2, 'tipo_seccion': 'Articulo'},
            {'id_seccion': 3, 'tipo_seccion': 'Galeria'}
        ]
        for datos in secciones:
            crear_secciones = Seccion(**datos)
            crear_secciones.save()

    if request.method == 'POST':
        galeria_form = GaleriaForm(request.POST, request.FILES)
        if galeria_form.is_valid():
            galeria = galeria_form.save(commit=False)
            galeria.editor = request.user
            galeria.usuario_creador = request.user
            galeria.seccion = Seccion.objects.get(id_seccion=3)  
            galeria.save()
            galeria_form.save_m2m()  # Guarda las etiquetas (tags) si existen
            return redirect('lista_galeria')  # Reemplaza con tu URL de éxito

    else:
        galeria_form = GaleriaForm()

    context = {
        'galeria_form': galeria_form,
    }
    return render(request, 'galeria/crear_galeria.html', context)


@login_required(login_url='login')
def lista_galeria(request):
    # Filtrar las publicaciones por usuario actual
    galeria_list = Publicacion.objects.filter(
        seccion__tipo_seccion='Galeria',
        usuario_creador=request.user  # Filtrar por el usuario actual
    )
 
    estado = request.GET.get('estado')
    if estado:
        galeria_list = galeria_list.filter(estado=estado)

    query = request.GET.get('q')
    if query:
        galeria_list = galeria_list.filter(titulo__icontains=query)

    # Paginación
    paginator = Paginator(galeria_list, 10)  
    page = request.GET.get('page')
    try:
        galeria = paginator.page(page)
    except PageNotAnInteger:
        galeria = paginator.page(1)
    except EmptyPage:
        galeria = paginator.page(paginator.num_pages)

    context = {
        'galerias': galeria  # Corregir aquí, asegurándote de que la variable se llame 'galeria'
    }

    return render(request, 'galeria/lista_galeria.html', context)




def ver_galeria(request, id_galeria):
    galeria = get_object_or_404(Publicacion, idPublicacion=id_galeria)

    if request.method == 'POST' and 'change_state' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.esta_publicado = 'is_published' in request.POST
        comentario.save()

    elif 'delete_comment' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.delete()

        # Use HttpResponseRedirect to redirect with a GET request
        return HttpResponseRedirect(request.path_info)

    elif request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.idPublicacion = galeria
            nuevo_comentario.save()

            # Enviar correo al usuario creador de la noticia
            subject = 'Nuevo comentario en tu publicación'
            message = f'Se ha añadido un nuevo comentario a tu publicación "{galeria.titulo}".'
            from_email = 'codemintest@gmail.com'
            recipient_list = [galeria.usuario_creador.email]

            send_mail(subject, message, from_email, recipient_list)

            return HttpResponseRedirect(request.path_info)

    if request.user.is_authenticated:
        comentarios = Comentario.objects.filter(idPublicacion=id_galeria)
    else:
        comentarios = Comentario.objects.filter(idPublicacion=id_galeria, esta_publicado=True)

    form = ComentarioForm()

    context = {
        'galeria': galeria,
        'comentarios': comentarios,
        'form': form,
    }

    return render(request, 'galeria/ver_galeria.html', context)


@login_required(login_url='login')
def editar_galeria(request, id_galeria):
    galeria = get_object_or_404(Publicacion, idPublicacion=id_galeria)

    if request.method == 'POST':
        galeria_form = GaleriaForm(request.POST, request.FILES, instance=galeria)

        if galeria_form.is_valid():
            galeria_form.save()
            return redirect('lista_galeria')  
    else:
        galeria_form = GaleriaForm(instance=galeria)

    context = {
        'galeria_form': galeria_form,
        'galeria': galeria,
    }
    return render(request, 'galeria/editar_galeria.html', context)

@login_required(login_url='login')
def eliminar_galeria(request, galeria_id):
    galeria = get_object_or_404(Publicacion, idPublicacion=galeria_id)
    if request.user == galeria.editor:
        galeria.delete()
        return redirect('lista_galeria')



































######### NOTICIAS ###############


from django.db.models import Q

def gestionar_noticia(request):
    return render(request, 'noticias/gestionar_noticia.html')


def home_noticias(request):
    if request.method == "POST":
        noticiaa = NoticiaForm(request.POST, request.FILES)
        if noticiaa.is_valid():
            noticiaa.save()

    query = request.GET.get('q')  
    tag_filtro = request.GET.get('tag')
    estado = request.GET.get('estado')  # Obtener el estado del formulario

    if request.user.is_authenticated:
        noticias = Publicacion.objects.filter(seccion__tipo_seccion='Noticias')
        if estado and estado != "Todo":
            noticias = noticias.filter(estado=estado)
    else:
        noticias = Publicacion.objects.filter(seccion__tipo_seccion='Noticias').exclude(estado__in=["Archivado", "Borrador"])


    if tag_filtro:
        noticias = noticias.filter(tags__name__in=[tag_filtro])

    if query:
        noticias = noticias.filter(Q(titulo__icontains=query)) 

    noticias = noticias.order_by('-fecha_creacion')
    paginator = Paginator(noticias, 12)  
    page = request.GET.get('page')

    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        noticias = paginator.page(1)
    except EmptyPage:
        noticias = paginator.page(paginator.num_pages)

    context = {
        'noticias': noticias
    }
    return render(request, 'noticias/home_noticias.html', context=context)



def ver_noticias(request, id_noticia):
    noticia = get_object_or_404(Publicacion, idPublicacion=id_noticia)

    if request.method == 'POST' and 'change_state' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.esta_publicado = 'is_published' in request.POST
        comentario.save()

    elif 'delete_comment' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.delete()


        return HttpResponseRedirect(request.path_info)

    elif request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.idPublicacion = noticia
            nuevo_comentario.save()

            subject = 'Nuevo comentario en tu publicación'
            message = f'Se ha añadido un nuevo comentario a tu publicación "{noticia.titulo}".'
            from_email = 'codemintest@gmail.com'
            recipient_list = [noticia.usuario_creador.email]

            send_mail(subject, message, from_email, recipient_list)

          
            return HttpResponseRedirect(request.path_info)

    if request.user.is_authenticated:
        comentarios = Comentario.objects.filter(idPublicacion=id_noticia)
    else:
        comentarios = Comentario.objects.filter(idPublicacion=id_noticia, esta_publicado=True)

    form = ComentarioForm()

    context = {
        'noticia': noticia,
        'comentarios': comentarios,
        'form': form,
    }

    return render(request, 'noticias/ver_noticias.html', context)





@login_required(login_url='login')
@ensure_csrf_cookie
def upload_image(request):
    csrf_token = get_token(request)

    if request.method == 'POST':
        image = request.FILES.get('upload')
        publicacion_id = request.POST.get('publicacion_id')
        
        if not image or not publicacion_id:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        try:
            publicacion = Publicacion.objects.get(id=publicacion_id)
        except Publicacion.DoesNotExist:
            return JsonResponse({'error': 'Publicacion does not exist'}, status=404)

        imagen = Imagen.objects.create(publicacion=publicacion, imagen_url=image)
        
        return JsonResponse({
            'uploaded': 1,
            'fileName': image.name,
            'url': imagen.imagen_url.url,
        })

    context = {
        "csrf_token": csrf_token,
    }
    return JsonResponse({'error': 'Only POST method is allowed', 'context': context}, status=400)


@login_required(login_url='login')
def crear_noticia(request):
    if Seccion.objects.count() == 0:
        secciones = [
            {'id_seccion': 1, 'tipo_seccion': 'Noticias'},
            {'id_seccion': 2, 'tipo_seccion': 'Articulo'},
            {'id_seccion': 3, 'tipo_seccion': 'Galeria'}
        ]
        for datos in secciones:
            crear_secciones = Seccion(**datos)
            crear_secciones.save()

    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST, request.FILES)
        if noticia_form.is_valid():
            noticia = noticia_form.save(commit=False)
            noticia.editor = request.user
            noticia.usuario_creador = request.user
            noticia.seccion = Seccion.objects.get(id_seccion=1)  

            imagen_portada = request.FILES.get('imagen_portada')
            if imagen_portada:
                noticia.imagen_portada = imagen_portada

            noticia.save()
            noticia_form.save_m2m()  
            return redirect('lista_noticias')
    else:
        noticia_form = NoticiaForm()

    context = {
        'noticia_form': noticia_form,
    }
    return render(request, 'noticias/crear_noticia.html', context)



@login_required(login_url='login')
def lista_noticias(request):
    # Filtrar las noticias por usuario actual y sección 'Noticias'
    noticias_list = Publicacion.objects.filter(
        seccion__tipo_seccion='Noticias',
        usuario_creador=request.user
    )

    # Filtrar por estado si es necesario
    estado = request.GET.get('estado')
    if estado:
        noticias_list = noticias_list.filter(estado=estado)

    # Filtrar por título si es necesario
    query = request.GET.get('q')
    if query:
        noticias_list = noticias_list.filter(titulo__icontains=query)

    # Paginación
    paginator = Paginator(noticias_list, 10)  # 10 noticias por página
    page = request.GET.get('page')
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, entregar la primera página.
        noticias = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, entregar la última página de resultados.
        noticias = paginator.page(paginator.num_pages)

    context = {
        'noticias': noticias
    }

    return render(request, 'noticias/lista_noticias.html', context)


@login_required(login_url='login')
def editar_noticia(request, id_noticia):
    noticia = get_object_or_404(Publicacion, idPublicacion=id_noticia)

    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST, request.FILES, instance=noticia)

        if noticia_form.is_valid():
            noticia_form.save()
            return redirect('lista_noticias')  
    else:
        noticia_form = NoticiaForm(instance=noticia)

    context = {
        'noticia_form': noticia_form,
        'noticia': noticia,
    }
    return render(request, 'noticias/editar_noticia.html', context)

@login_required(login_url='login')
def eliminar_noticia(request, noticia_id):
    noticia = get_object_or_404(Publicacion, idPublicacion=noticia_id)
    if request.user == noticia.editor:
        noticia.delete()
        return redirect('lista_noticias')


def publicacion_detalle(request, id):
    publicacion = get_object_or_404(Publicacion, idPublicacion=id)
    comentarios = Comentario.objects.filter(idPublicacion=id, estado='Publicado')
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.idPublicacion = publicacion
            nuevo_comentario.estado = 'Revision'
            nuevo_comentario.save()
            return redirect('nombre_de_la_url_para_detalle_de_publicacion', id=id)
    else:
        form = ComentarioForm()

    return render(request, 'nombre_de_tu_template.html', {'publicacion': publicacion, 'comentarios': comentarios, 'form': form})


#ACERCA DEEEEE

from django.contrib.auth.models import AnonymousUser

def home_acercade(request):
    if Seccion.objects.count() == 0:
        secciones = [
            {'id_seccion': 1, 'tipo_seccion': 'Noticias'},
            {'id_seccion': 2, 'tipo_seccion': 'Articulo'},
            {'id_seccion': 3, 'tipo_seccion': 'Galeria'}
        ]
        for datos in secciones:
            crear_secciones = Seccion(**datos)
            crear_secciones.save()
        

    if Seccion.objects.count() == 3:
        new_section = [
            {'id_seccion': 4, 'tipo_seccion':'About'}

        ]
        for datos in new_section:
            crear_seccion = Seccion(**datos)
            crear_seccion.save()
        superusuario = User.objects.create_superuser(
        username='Super_User_default',
        email='super_user_default@gmail.com',
        password='@@_superuser_@@'
        )
        superusuario.first_name = 'Nombre'
        superusuario.last_name = 'Apellido'
        superusuario.save()
        my_about = Publicacion.objects.create(
            editor= superusuario,
            usuario_creador = superusuario,
            cuerpo='Vacio',
            seccion= Seccion.objects.get(id_seccion=4) 
        )
        my_about.save()

    my_about = Publicacion.objects.filter(seccion=4)


    return render(request, 'acerca_de/home_acercade.html', {'my_about': my_about})



@login_required(login_url='login')
def edit_my_about(request):

    my_about = get_object_or_404(Publicacion, seccion__id_seccion=4)

    if request.method == 'POST':
        noticia_form = AboutForm(request.POST, instance=my_about)
        if noticia_form.is_valid():
            noticia_form.save()
            return redirect('home_acercade')
    else:
        noticia_form = AboutForm(instance=my_about)
    
    context = {
        'noticia_form': noticia_form,
        'my_about': my_about,
    }
        

    return render(request, 'acerca_de/editar_acercade.html',context)







