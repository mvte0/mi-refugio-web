from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Cliente
from .forms import RegisterForm
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Contraseña ya queda hasheada por UserCreationForm, no plaintext
                user.is_staff = False
                user.is_superuser = False
                user.save(update_fields=["is_staff", "is_superuser"])
                Cliente.objects.create(user=user, rut=form.cleaned_data["rut"])
                login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class LoginViewRemember(LoginView):
    def form_valid(self, form):
        remember = self.request.POST.get('remember') == 'on'
        response = super().form_valid(form)
        if remember:
            # 30 días en segundos
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            # Expira al cerrar el navegador
            self.request.session.set_expiry(0)
        return response


def logout_then_home(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('home')
