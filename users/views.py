from rest_framework import generics, permissions, filters
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import User
from .serializers import UserSerializer, RegisterSerializer

# pega o User customizado definido em AUTH_USER_MODEL
UserModel = get_user_model()

# ---------- VIEWS BASEADAS EM TEMPLATE ----------

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
        user.save()
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
            return redirect('users:user_profile')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'users/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email', '').strip()

        if UserModel.objects.filter(username=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
        else:
            user = UserModel.objects.create_user(
                username=email,
                email=email,
                first_name=data.get('first_name', '').strip(),
                last_name=data.get('last_name', '').strip(),
                password=data.get('password')
            )
            login(request, user)
            return redirect('users:user_profile')

    return render(request, 'users/register.html')


@require_GET
def logout_view(request):
    logout(request)
    return redirect('users:login_form')


# ---------- VIEWS BASEADAS EM API (DRF) ----------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.query_params.get('type')
        if user_type == 'cliente':
            queryset = queryset.filter(is_cliente=True)
        elif user_type == 'prestador':
            queryset = queryset.filter(is_prestador=True)
        return queryset


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
