from django.contrib import admin
from .models import Produto, Categoria, ImagemProduto

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque')
    inlines = [ImagemProdutoInline]

admin.site.register(Categoria)
