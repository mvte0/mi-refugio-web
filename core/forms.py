from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import normalize_rut
from .models import Cliente


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    rut = forms.CharField(required=True, label="RUT", max_length=14)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "rut", "password1", "password2")

    def clean_rut(self):
        value = self.cleaned_data.get("rut")
        rut = normalize_rut(value)
        if Cliente.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")
        return rut

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
