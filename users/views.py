from rest_framework import generics, permissions, filters, status
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

@login_required
def perfil_view(request):
    user = request.user
    return render(request, 'users/perfil.html', {'user': user})

@login_required
@require_http_methods(["GET", "POST"])
def editar_perfil_view(request):
    user = request.user

    if request.method == 'POST':
        # Atualiza os dados do usuário via formulário
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Aqui você pode adicionar validações se desejar

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('user_profile')  # redireciona para a página de perfil

    # GET - mostra formulário com dados atuais
    return render(request, 'users/editar_perfil.html', {'user': user})

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
