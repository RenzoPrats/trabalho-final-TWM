from operator import index
from django.urls import path, include
from django.urls import re_path as url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import index_view, login_view, cadastro_view, login_usuario_view, cadastrar_usuario_view, logout_view, funcionario_view, cliente_view, nova_ordem_servico, criar_nova_ordem

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^entrar', login_view, name='entrar'),
    url(r'^cadastrar', cadastro_view, name='cadastrar'),
    url(r'^registrar', cadastrar_usuario_view, name='registrar_usuario'),
    url(r'^login', login_usuario_view, name='logar_usuario'),
    url(r'^logout', logout_view, name='logout'),
    url(r'^cliente', cliente_view, name='cliente'),
    url(r'^funcionario', funcionario_view, name='funcionario'),
    url(r'^nova_ordem_servico', nova_ordem_servico, name='nova_ordem_servico'),
    url(r'^criar_nova_ordem', criar_nova_ordem, name='criar_nova_ordem'),
]