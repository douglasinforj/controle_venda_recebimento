from django import forms 
from .models import Cliente, Produto, ImagemProduto
from django.forms import modelformset_factory

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf_cnpj', 'telefone', 'email', 'endereco']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'preco_custo', 'preco', 'estoque']     #campo lucro fica de fora, poiis ele não é editavel

class ImagemProdutoForm(forms.ModelForm):
    class Meta:
        model = ImagemProduto
        fields = ['imagem']

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')

        if imagem:
            if imagem.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("A imagem não pode ser maior que 2MB.")
            if not imagem.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("A imagem deve estar em formato JPEG ou PNG.")
        return imagem

ImagemProdutoFormSet = modelformset_factory(
    ImagemProduto,
    form=ImagemProdutoForm,
    extra=3,  # quantidade de campos vazios para adicionar
    can_delete=True,
)