from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("home_perfiles/", views.home_perfiles, name="home_perfiles"),
    path("home_cuentas/", views.home_cuentas, name="home_cuentas"),
    path("update_user_info/", views.update_user_info, name="update_user_info"),
    path("perfil/", views.perfil, name="perfil"),
    path("logout/", views.logout_request, name="logout"),
    path("crear_perfil/", views.crear_perfil, name="crear_perfil"),
    path("regist_user/", views.regist_user, name="regist_user"),
    path("reset_pw/", views.reset_pw, name="reset_pw"),
    path("list_perfil/", views.list_perfil, name="list_perfil"),
    path("edit_perfil/<int:user_id>/", views.edit_perfil, name="edit_perfil"),
    path("delete_perfil/<int:user_id>/", views.delete_perfil, name="delete_perfil"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="usuarios/password_reset.html",
            email_template_name="usuarios/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="usuarios/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="usuarios/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="usuarios/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
