from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import EditProfileForm
from django.contrib.auth.decorators import user_passes_test


def home_perfiles(request):
    return render(request, "usuarios/home_perfiles.html")


def home_cuentas(request):
    return render(request, "usuarios/home_cuentas.html")


def crear_perfil(request):
    return render(request, "usuarios/crear_perfil.html")


def login_request(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    context = {
        "form": form,
        "title": title,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            # Check if the user is logging in for the first time
            is_first_time_login = user.last_login is None

            # Now, log the user in
            login(request, user)

            if is_first_time_login:
                return redirect(
                    "reset_pw"
                )  # Redirect to the page where they can reset their temporary password
            return redirect("home")
        else:
            # Handle the case where authentication fails
            messages.error(request, "Invalid username or password.")
    else:
        print(form.errors)
    return render(request, "usuarios/login.html", context=context)


def generate_random_password():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(12)
    )


@login_required
def regist_user(request):
    if not request.user.groups.filter(name="Admin").exists():
        messages.error(
            request,
            "Acceso denegado. Debes ser un administrador para acceder a esta vista.",
        )
        return redirect("home")

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            role = form.cleaned_data.get("role")  # Obtén el grupo seleccionado

            # Verificar si el nombre de usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "El nombre de usuario ya existe. Por favor, elige otro."
                )
                return render(request, "usuarios/regist_user.html", {"form": form})

            random_password = User.objects.make_random_password()

            user = User.objects.create_user(
                username=username, email=email, password=random_password
            )

            # Asigna el usuario al grupo correspondiente
            group = Group.objects.get(name=role)
            user.groups.add(group)

            current_site = get_current_site(request)

            mail_subject = "Activa tu cuenta"
            message = f"""Hola {username},
Por favor haz clic en el siguiente enlace para iniciar sesión:
http://{current_site}/usuarios/login/
Tu contraseña temporal es: {random_password}
"""
            send_mail(mail_subject, message, "codemintest@gmail.com", [email])

            messages.success(request, "Usuario creado exitosamente.")
            return redirect("home")
        else:
            messages.error(
                request,
                "Error al crear el usuario. Por favor, corrija los errores abajo.",
            )
    else:
        form = CreateUserForm()

    return render(request, "usuarios/regist_user.html", {"form": form})


@login_required
def update_user_info(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, instance=request.user
        )  # Assuming you have a form to update user info
        if form.is_valid():
            form.save()
            messages.success(request, "Información actualizada exitosamente.")
            return redirect(
                "perfil"
            )  # Redirect to the page that displays user's current info
        else:
            messages.error(request, "Por favor, corrige los errores abajo.")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "usuarios/update_user_info.html", {"form": form})


@login_required
def perfil(request):
    return render(request, "usuarios/perfil.html", {"user": request.user})


from django.contrib.auth.models import User, Group
from django.db.models import Q

@login_required
def list_perfil(request):
    if not request.user.groups.filter(name="Admin").exists():
        messages.error(
            request,
            "Acceso denegado. Debes ser un administrador para acceder a esta vista.",
        )
        return redirect("home")

    query_name = request.GET.get("q_name", "")
    query_email = request.GET.get("q_email", "")
    query_role = request.GET.get("role", "")

    # Filtrar por nombre y/o email
    user_list = User.objects.filter(is_active=True)
    if query_name:
        user_list = user_list.filter(username__icontains=query_name)
    if query_email:
        user_list = user_list.filter(email__icontains=query_email)

    # Filtrar por grupo
    if query_role:
        user_list = user_list.filter(groups__name=query_role)

    paginator = Paginator(user_list, 10)  # 10 usuarios por página

    page = request.GET.get("page")
    users = paginator.get_page(page)

    return render(
        request,
        "usuarios/list_perfil.html",
        {"users": users, "query_name": query_name, "query_email": query_email, "query_role": query_role},
    )

    


@login_required
def reset_pw(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.user
            new_password = form.cleaned_data["new_password1"]

            if user.check_password(form.cleaned_data["old_password"]):
                user.set_password(new_password)
                user.save()
                login(request, user)  # Log the user in
                messages.success(
                    request, "Tu contraseña ha sido cambiada exitosamente."
                )
                return redirect("perfil")
            else:
                form.add_error("old_password", "La contraseña actual es incorrecta.")
                messages.error(request, "Por favor, corrige el error abajo.")
        else:
            messages.error(request, "Por favor, corrige el error abajo.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "usuarios/reset_pw.html", {"form": form})


@login_required
def edit_perfil(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("list_perfil")
    else:
        form = EditProfileForm(instance=user)
    return render(request, "usuarios/edit_perfil.html", {"form": form})


@login_required
def delete_perfil(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        user.delete()
        return redirect("list_perfil")
    return render(request, "usuarios/delete_perfil.html", {"user": user})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


##### Olvide Contraseña #####

from django.contrib.auth.forms import PasswordResetForm


def password_reset(request):
    if request.method == "POST":
        # Si el formulario se envió
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect("password_reset_done")
    else:
        form = PasswordResetForm()

    return render(request, "usuarios/password_reset.html", {"form": form})
