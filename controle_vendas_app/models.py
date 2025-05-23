from django.db import models

from datetime import date, timedelta
from django.db.models import Q

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=15, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    endereco = models.TextField()

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        self.nome

    
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    lucro = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Não editável manualmente
    estoque = models.PositiveIntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)

    #calcula o campo lucro
    def save(self, *args, **kwargs):
        self.lucro = self.preco - self.preco_custo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    

class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='static/imagens/produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"




    
    
class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_venda = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    parcelado = models.BooleanField(default=False)
    parcelas = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"


class Parcela(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="parcelas_venda")
    numero = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Parcela {self.numero} - Venda {self.venda.id}"
    

# Função lista clientes com parcelas vencidas ou próximo de vencimento

def listar_alertas():
    hoje = date.today()
    proximo = hoje + timedelta(days=5)

    #busca clientes com parcelas vencidas
    vencidos = Parcela.objects.filter(data_vencimento__lt=hoje, pago=False)

    #busca clientes com parcelas a vencer em até 5 dias
    proximo_a_vencer = Parcela.objects.filter(data_vencimento__range=(hoje, proximo), pago=False)

    return {
        "vencidos": vencidos,
        "proximo_a_vencer": proximo_a_vencer
    }
