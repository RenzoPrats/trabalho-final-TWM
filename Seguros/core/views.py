from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import OrdemServico, TipoSeguro, User


def index_view(request):
    context = {
    }
    return HttpResponse(loader.get_template('index.html').render(context,request))

def login_view(request):
    context = {
    }
    return HttpResponse(loader.get_template('login.html').render(context,request))

def cadastro_view(request):
    context = {
    }
    return HttpResponse(loader.get_template('cadastro.html').render(context,request))


def login_usuario_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['senha']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                if user.is_funcionario:
                    return redirect('funcionario')
                else:
                    return redirect('cliente')
            else:
                #informa que deu erro e volta para entrar
                messages.error(request, 'Erro ao efetuar login, conta inválida!')
                return redirect('entrar')
        else:
            messages.error(request, 'Erro ao efetuar login, verifique seus dados!')
            return redirect('entrar')
    else:
        return redirect('/')
    
def cadastrar_usuario_view(request):
    try:
       if request.method == 'POST':
            nome = request.POST.get('nome','')
            email = request.POST.get('email','')
            senha1 = request.POST.get('senha1','')
            senha2 = request.POST.get('senha2','')
            is_funcionario = request.POST.get('is_funcionario','')
            
            if nome != '' and senha1 != '' and senha2 != '' and email != '':
                if senha1 == senha2:
                    
                    if(is_funcionario == "1"):
                        is_funcionario = True
                    else:
                        is_funcionario = False
                    
                    User = get_user_model()

                    user = User.objects.filter(email=email)
            
                    if len(user) > 0:
                        messages.error(request, 'Erro ao efetuar cadastro, este e-mail já está em uso!')
                        return redirect('cadastrar')
                    else:
                        User.objects.create_user(
                            email=email,
                            name=nome,
                            password=senha1,
                            is_funcionario=is_funcionario
                        )
                        user = authenticate(email=email,password=senha1)
                        login(request, user)

                else:
                    messages.error(request, 'Erro ao efetuar cadastro, as senhas não são iguais!')
                    return redirect('cadastrar')
            else:
                messages.error(request, 'Erro ao efetuar cadastro, verifique seus dados!')
                return redirect('cadastrar')
            
            context = {}
            
            if user.is_funcionario:
                return redirect('funcionario')
            else:
                return redirect('cliente')
    except:
        return redirect('entrar')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def funcionario_view(request):
    if not request.user.is_authenticated:
        return redirect('entrar')
    if not request.user.is_funcionario:
        return redirect('cliente')
    
    ordens_servico = OrdemServico.objects.all()
    context = {
        "ordens_servico":ordens_servico
    }
    return HttpResponse(loader.get_template('funcionario.html').render(context,request))

def cliente_view(request):
    if not request.user.is_authenticated:
        return redirect('entrar')
    if request.user.is_funcionario:
        return redirect('funcionario')
    
    ordens_servico = OrdemServico.objects.filter(cliente=request.user)
    context = {
        "ordens_servico":ordens_servico
    }
    return HttpResponse(loader.get_template('cliente.html').render(context,request))

def nova_ordem_servico(request):
    
    ordem_servico = []
    if 'id_ordem' in request.GET:
        ordem_servico = OrdemServico.objects.filter(id=request.GET['id_ordem'])[0]
    
    tipos_seguros = TipoSeguro.objects.all()
    context = {
        "tipos_seguros" : tipos_seguros,
        "ordem_servico" : ordem_servico
    }
    return HttpResponse(loader.get_template('nova_ordem_servico.html').render(context,request))


def criar_nova_ordem(request):    
    try:
        if request.method == 'POST':
            usuario = User.objects.filter(email=request.user)[0]

            ordem_servico = request.POST.get('id_ordem_servico', '')
            if ordem_servico == '0' or ordem_servico == '':
                ordem_servico = 0
            else:
                ordem_servico = OrdemServico.objects.filter(id=request.POST['id_ordem_servico'])[0]
                
            tipo = request.POST.get('tipo', '')
            descricao = request.POST.get('descricao', '')
            
            tipo = TipoSeguro.objects.filter(id=tipo)[0]    
             
            if ordem_servico == 0:
                nova_ordem_servico = OrdemServico(
                    cliente = usuario,
                    tipo=tipo,
                    descricao=descricao,
                )
                nova_ordem_servico.save(force_insert=True)
            else:
                if not usuario.is_funcionario:
                    ordem_servico.tipo = tipo
                    ordem_servico.descricao = descricao
                else:
                    ordem_servico.funcionario = usuario
                    ordem_servico.relatorio = request.POST.get('relatorio', '')
                    ordem_servico.status = 1
                ordem_servico.save(force_update=True)
            
            if(request.user.is_funcionario):
                return redirect('funcionario')
            
            return redirect('cliente')
                    
        else:
            messages.error(request, 'Erro ao criar nova ordem de serviço, verifique seus dados!')
            return redirect(request.META['HTTP_REFERER'])
        pass
    except:
        messages.error(request, 'Erro ao criar nova ordem de serviço, verifique seus dados!')
        return redirect(request.META['HTTP_REFERER'])

