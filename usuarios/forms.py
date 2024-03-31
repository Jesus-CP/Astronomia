from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "validate", "placeholder": "Enter Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Este usuario no existe")
            if not user.check_password(password):
                raise forms.ValidationError("Contraseña incorrecta")
            if not user.is_active:
                raise forms.ValidationError("Este usuario no esta activado")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nombre"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Correo"}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )
    password2 = (
        forms.CharField(
            label="Confirmar contraseña",
            help_text="Repetir contraseña",
            widget=forms.PasswordInput(attrs={"placeholder": "Re Enter Password"}),
        ),
    )
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "group"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    email = forms.EmailField(label="Correo electrónico")
    role = forms.ChoiceField(
        label="Selecciona un Perfil",
        choices=(
            ("Admin", "Administrador"),
            ("Editor", "Editor"),
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con ese correo electrónico ."
            )
        return email

    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        role = self.cleaned_data.get("role")
        random_password = User.objects.make_random_password()

        user = User.objects.create_user(
            username=username, email=email, password=random_password
        )

        # Asigna el usuario al grupo correspondiente
        group = Group.objects.get(name=role)
        user.groups.add(group)

        return user


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nombre"}),
        label="Nombre",
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Apellido"}),
        label="Apellido",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("Este campo es obligatorio.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Este campo es obligatorio.")
        return last_name
