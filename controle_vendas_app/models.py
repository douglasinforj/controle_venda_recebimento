from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=15, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    endereco = models.TextField()

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()

    def __str__(self):
        return self.nome
    
class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_venda = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    parcelado = models.BooleanField(default=False)
    parcelas = models.PositiveIntegerField(default=1)


class Parcela(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="parcelas")
    numero = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Parcela {self.numero} - Venda {self.venda.id}"