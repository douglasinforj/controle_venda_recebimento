from django.shortcuts import render, redirect

from datetime import date, timedelta
from .models import Parcela, Cliente, Produto
from .forms import ClienteForm, ProdutoForm

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q


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
        


#------------------------------------Clientes---------------------------------------
@login_required
def listar_clientes(request):

    query = request.GET.get("q", "")
    clientes = Cliente.objects.filter(
        Q(nome__icontains=query) |
        Q(email__icontains=query) |
        Q(cpf_cnpj__icontains=query)

    ) if query else Cliente.objects.all()

    return render(request, "controle_vendas_app/listar_clientes.html", {"clientes": clientes, "query": query})

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


#--------------------------------Produtos---------------------------------------

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "controle_vendas_app/listar_produtos.html", {"produtos": produtos})

def cadastrar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, "controle_vendas_app/cadastrar_produto.html", {"form": form})

    
