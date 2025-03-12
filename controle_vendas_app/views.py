from django.shortcuts import render

from datetime import date, timedelta
from .models import Parcela

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    hoje = date.today()
    proximo = hoje + timedelta(days=5)

    vencidos = Parcela.objects.filter(data_vencimento__lt=hoje, pago=False)
    proximo_a_vencer = Parcela.objects.filter(data_vencimento__range=(hoje, proximo), pago=False)

    context = {
        "vencidos": vencidos,
        "proximo_a_vencer": proximo_a_vencer
    }
    return render(request, "controle_vendas_app/home.html", context)

# Lógica para login e logout

class CustomLoginView(LoginView):
    template_name = "controle_vendas_app/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos.")
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
        
    
