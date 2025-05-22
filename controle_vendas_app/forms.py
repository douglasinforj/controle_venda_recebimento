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
        fields = ['nome', 'descricao', 'categoria', 'preco_custo', 'preco', 'estoque']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control'}),
            #'lucro': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ImagemProdutoForm(forms.ModelForm):
    class Meta:
        model = ImagemProduto
        fields = ['imagem']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

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