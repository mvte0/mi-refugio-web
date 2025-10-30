from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Cliente
from .validators import normalize_rut


class RegisterForm(UserCreationForm):
    """Formulario de registro que exige RUT y correo unicos."""

    email = forms.EmailField(required=True, label="Correo electronico")
    rut = forms.CharField(required=True, label="RUT", max_length=14)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "rut", "password1", "password2")

    def clean_rut(self):
        value = self.cleaned_data.get("rut")
        rut = normalize_rut(value)
        if Cliente.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya esta registrado.")
        return rut

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya esta registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
