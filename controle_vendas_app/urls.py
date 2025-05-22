from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),

    path('listar_produtos/', views.listar_produtos, name='listar_produtos'), 
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
]
