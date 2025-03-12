from django.shortcuts import render, redirect

from datetime import date, timedelta
from .models import Parcela, Cliente
from .forms import ClienteForm

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
        

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "controle_vendas_app/listar_clientes.html", {"clientes": clientes})

@login_required
def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, "controle_vendas_app/cadastrar_cliente.html", {"form": form})







    
