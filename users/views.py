from rest_framework import generics, permissions, filters
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
import requests
from .serializers import UserSerializer, RegisterSerializer
from .models import ClienteProfile, PrestadorProfile

# Usa o modelo customizado definido em AUTH_USER_MODEL
UserModel = get_user_model()

# ---------- AJAX CEP ----------
@require_GET
def consulta_cep(request):
    cep = request.GET.get('cep', '').replace('-', '').strip()
    if not cep or len(cep) != 8:
        return JsonResponse({'error': 'CEP inválido'}, status=400)
    resp = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    data = resp.json()
    if data.get('erro'):
        return JsonResponse({'error': 'CEP não encontrado'}, status=404)
    return JsonResponse({
        'cep': data.get('cep'),
        'endereco': data.get('logradouro'),
        'complemento': data.get('complemento'),
        'bairro': data.get('bairro'),
        'cidade': data.get('localidade'),
        'estado': data.get('uf'),
    })


# ---------- VIEWS BASEADAS EM TEMPLATE ----------
@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html', {'user': request.user})

@login_required
def perfil_view(request):
    return render(request, 'users/perfil.html', {'user': request.user})

@login_required
@require_http_methods(["GET", "POST"])
def editar_perfil_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.phone = request.POST.get('phone', '').strip()
        user.bio = request.POST.get('bio', '').strip()
        user.save()
        if user.user_type == 'client':
            perfil = getattr(user, 'cliente_profile')
            perfil.cep = request.POST.get('cep', '').strip()
            perfil.endereco = request.POST.get('endereco', '').strip()
            perfil.cidade = request.POST.get('cidade', '').strip()
            perfil.estado = request.POST.get('estado', '').strip()
            perfil.data_nascimento = request.POST.get('data_nascimento') or perfil.data_nascimento
            perfil.save()
        elif user.user_type == 'provider':
            perfil = getattr(user, 'prestador_profile')
            perfil.cep = request.POST.get('cep', '').strip()
            perfil.endereco = request.POST.get('endereco', '').strip()
            perfil.cidade = request.POST.get('cidade', '').strip()
            perfil.estado = request.POST.get('estado', '').strip()
            perfil.especialidade = request.POST.get('especialidade', '').strip()
            perfil.experiencia = request.POST.get('experiencia', '').strip()
            perfil.tempo_atuacao_anos = request.POST.get('tempo_atuacao_anos') or perfil.tempo_atuacao_anos
            perfil.portfolio_url = request.POST.get('portfolio_url', '').strip()
            perfil.preco_hora = request.POST.get('preco_hora') or perfil.preco_hora
            perfil.disponibilidade = request.POST.get('disponibilidade', '').strip()
            perfil.save()
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('users:user_profile')
    return render(request, 'users/editar_perfil.html', {'user': user})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users:dashboard')  # redireciona para dashboard
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'users/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email', '').strip()
        user_type = data.get('user_type', 'client')

        if UserModel.objects.filter(username=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
        else:
            user = UserModel.objects.create_user(
                username=email,
                email=email,
                first_name=data.get('first_name', '').strip(),
                last_name=data.get('last_name', '').strip(),
                password=data.get('password'),
                user_type=user_type
            )
            if user_type == 'client':
                ClienteProfile.objects.get_or_create(user=user)
            else:
                PrestadorProfile.objects.get_or_create(user=user)

            login(request, user)
            return redirect('users:dashboard')  # redireciona para dashboard

    return render(request, 'users/register.html')

@require_GET
def logout_view(request):
    logout(request)
    return redirect('users:login_form')

# ---------- VIEWS BASEADAS EM API (DRF) ----------
class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']
    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.query_params.get('type')
        if user_type == 'cliente':
            queryset = queryset.filter(user_type='client')
        elif user_type == 'prestador':
            queryset = queryset.filter(user_type='provider')
        return queryset

class UserDetailView(generics.RetrieveAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]