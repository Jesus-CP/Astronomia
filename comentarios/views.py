from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CambiarEstadoComentarioForm
from .models import Comentario

@login_required
def estado_comentario(request, id_comentario):
    comentario = get_object_or_404(Comentario, id=id_comentario)
    
    if request.method == 'POST':
        form = CambiarEstadoComentarioForm(request.POST, instance=comentario)
        
        if form.is_valid():
            form.save()
            return redirect('home_noticias')  
    else:
        form = CambiarEstadoComentarioForm(instance=comentario)
        
    context = {'form': form}
    return render(request, 'comentarios/estado_comentario.html', context)


from django.http import HttpResponseRedirect
from django.contrib import messages


@login_required
def eliminar_comentario(request, id_comentario):
    comentario = get_object_or_404(Comentario, id=id_comentario)

    if request.method == 'POST':
        try:
            # Get the associated 'galeria' ID
            galeria_id = comentario.idPublicacion.id

            comentario.delete()

            # Use the messages framework to display a success message
            messages.success(request, 'Comentario eliminado con éxito.')

            # Use HttpResponseRedirect to redirect with a GET request
            return HttpResponseRedirect(request.path_info)
        except Exception as e:
            print(f"Error deleting comment: {e}")
            messages.error(request, 'Error al eliminar el comentario.')
            return redirect('home_galeria')  

    return redirect('home_galeria')




