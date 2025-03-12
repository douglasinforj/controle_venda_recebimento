from django.shortcuts import render

from datetime import date, timedelta
from .models import Parcela

def home(request):
    hoje = date.today()
    proximo = hoje + timedelta(days=5)

    vencidos = Parcela.objects.filter(data_venciemnto__lt=hoje, pago=False)
    proximo_a_vencer = Parcela.objects.filter(data_vencimento__range=(hoje, proximo), pago=False)

    context = {
        "vencidos": vencidos,
        "proximo_a_vencer": proximo_a_vencer
    }
    return render(request, "controle_vendas_app/home.html", context)
